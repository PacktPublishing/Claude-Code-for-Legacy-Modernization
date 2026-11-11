from __future__ import annotations

import hashlib
import json
import math
import os
import subprocess
import sys
from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

VOLATILE_FIELDS = {"run_id", "generated_at", "host_name"}
ALLOWED_ENV = {
    "LANG": "C",
    "LC_ALL": "C",
    "TZ": "UTC",
    "PATH": os.environ.get("PATH", ""),
}


@dataclass(frozen=True)
class SubjectResult:
    name: str
    command: list[str]
    returncode: int | None
    stdout_sha256: str
    stderr_sha256: str
    stdout_path: str
    stderr_path: str
    parsed: Any | None
    parse_error: str | None
    execution_error: dict[str, Any] | None = None


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    text = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return (text + "\n").encode("utf-8")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON member: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number: {value}")


def require_finite(value: Any) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("non-finite JSON number (including exponent overflow)")
    if isinstance(value, dict):
        for item in value.values():
            require_finite(item)
    elif isinstance(value, list):
        for item in value:
            require_finite(item)


def strict_json(raw: bytes | str) -> Any:
    value = json.loads(raw, object_pairs_hook=unique_object, parse_constant=reject_constant)
    require_finite(value)
    return value


def same_json(left: Any, right: Any) -> bool:
    if isinstance(left, bool) or isinstance(right, bool):
        return type(left) is type(right) and left == right
    if isinstance(left, dict) and isinstance(right, dict):
        return left.keys() == right.keys() and all(
            same_json(left[key], right[key]) for key in left
        )
    if isinstance(left, list) and isinstance(right, list):
        return len(left) == len(right) and all(
            same_json(a, b) for a, b in zip(left, right)
        )
    return left == right


def normalize(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: normalize(item)
            for key, item in sorted(value.items())
            if key not in VOLATILE_FIELDS
        }
    if isinstance(value, list):
        return [normalize(item) for item in value]
    return value


def amount_minor_units(value: Any) -> int:
    try:
        amount = Decimal(str(value))
    except InvalidOperation as error:
        raise ValueError(f"invalid decimal amount: {value!r}") from error
    scaled = amount * 100
    if scaled != scaled.to_integral_value():
        raise ValueError(f"amount has more than two decimal places: {value!r}")
    return int(scaled)


def semantic_compare(left: Any, right: Any) -> list[dict[str, Any]]:
    left_n = normalize(left)
    right_n = normalize(right)
    differences: list[dict[str, Any]] = []

    if not isinstance(left_n, dict) or not isinstance(right_n, dict):
        if not same_json(left_n, right_n):
            differences.append({"path": "$", "legacy": left_n, "replacement": right_n})
        return differences

    keys = sorted(set(left_n) | set(right_n))
    for key in keys:
        if key not in left_n or key not in right_n:
            differences.append({
                "path": f"$.{key}",
                "legacy": left_n.get(key, "<MISSING>"),
                "replacement": right_n.get(key, "<MISSING>"),
            })
            continue
        if key == "amount":
            left_value = amount_minor_units(left_n[key])
            right_value = amount_minor_units(right_n[key])
        else:
            left_value = left_n[key]
            right_value = right_n[key]
        if not same_json(left_value, right_value):
            differences.append({
                "path": f"$.{key}",
                "legacy": left_n[key],
                "replacement": right_n[key],
            })
    return differences


def run_subject(
    name: str,
    command: list[str],
    input_value: Any,
    timeout_seconds: float,
    capture_root: Path,
) -> SubjectResult:
    if not command or any(not isinstance(part, str) or not part for part in command):
        raise ValueError("command must be a nonempty string array")
    if not name or name in {".", ".."} or Path(name).name != name:
        raise ValueError("subject name must be one path component")
    directory = capture_root.resolve(strict=True) / name
    directory.mkdir()  # Refuse reuse; retain every run, including failures.
    work = directory / "work"
    work.mkdir()
    payload = canonical_bytes(input_value)
    with (directory / "input.json").open("xb") as stream:
        stream.write(payload)
    stdout_path = directory / "stdout.bin"
    stderr_path = directory / "stderr.bin"
    returncode = None
    execution_error = None
    with stdout_path.open("xb") as stdout_file, stderr_path.open("xb") as stderr_file:
        try:
            completed = subprocess.run(
                command, input=payload, stdout=stdout_file, stderr=stderr_file,
                cwd=work, env=ALLOWED_ENV, timeout=timeout_seconds,
                check=False, shell=False,
            )
            returncode = completed.returncode
        except (OSError, subprocess.TimeoutExpired) as error:
            execution_error = {
                "kind": "timeout" if isinstance(error, subprocess.TimeoutExpired) else "spawn-error",
                "exception": type(error).__name__,
                "errno": getattr(error, "errno", None),
                "message": str(error),
            }
    stdout = stdout_path.read_bytes()
    stderr = stderr_path.read_bytes()
    parsed = None
    parse_error = None
    if execution_error is None:
        try:
            parsed = strict_json(stdout)
        except (ValueError, UnicodeDecodeError) as error:
            parse_error = str(error)
    return SubjectResult(
        name=name, command=command, returncode=returncode,
        stdout_sha256=digest(stdout), stderr_sha256=digest(stderr),
        stdout_path=str(stdout_path), stderr_path=str(stderr_path),
        parsed=parsed, parse_error=parse_error, execution_error=execution_error,
    )


def main() -> None:
    if len(sys.argv) != 5:
        raise SystemExit(
            "usage: run_subject.py INPUT LEGACY_COMMAND_JSON "
            "REPLACEMENT_COMMAND_JSON REPORT"
        )

    input_path = Path(sys.argv[1])
    input_bytes = input_path.read_bytes()
    legacy_command = strict_json(sys.argv[2])
    replacement_command = strict_json(sys.argv[3])
    report_path = Path(sys.argv[4])

    if report_path.exists():
        raise FileExistsError(report_path)
    capture_root = report_path.with_name(report_path.name + ".streams")
    capture_root.mkdir(parents=True)  # No reuse or cleanup.
    original_path = capture_root / "original-input.bin"
    with original_path.open("xb") as stream:
        stream.write(input_bytes)
    try:
        input_value = strict_json(input_bytes)
    except (ValueError, UnicodeDecodeError) as error:
        failure = {
            "input_path": str(input_path), "input_sha256": digest(input_bytes),
            "original_input_path": str(original_path.resolve()),
            "subjects": [], "blockers": [f"input was not valid JSON: {error}"],
            "decision": "human-review-required",
        }
        with report_path.open("x", encoding="utf-8") as stream:
            stream.write(json.dumps(failure, indent=2, allow_nan=False) + "\n")
        raise SystemExit(1)
    legacy = run_subject("legacy", legacy_command, input_value, 30, capture_root)
    replacement = run_subject("replacement", replacement_command, input_value, 30, capture_root)

    blockers = []
    for result in (legacy, replacement):
        if result.execution_error is not None:
            blockers.append(f"{result.name}: {result.execution_error['kind']}")
        elif result.returncode != 0:
            blockers.append(f"{result.name} returned {result.returncode}")
        if result.parse_error is not None:
            blockers.append(f"{result.name} output was not valid JSON")

    differences = []
    if not blockers:
        try:
            differences = semantic_compare(legacy.parsed, replacement.parsed)
        except (ValueError, InvalidOperation, OverflowError) as error:
            blockers.append(f"comparison invalid: {error}")

    report = {
        "schema_version": "1.0",
        "claim_type": "execution-record",
        "input_path": str(input_path),
        "input_sha256": digest(input_bytes),
        "original_input_path": str(original_path.resolve()),
        "subject_input_sha256": digest(canonical_bytes(input_value)),
        "subjects": [asdict(legacy), asdict(replacement)],
        "blockers": blockers,
        "differences": differences,
        "decision": "human-review-required",
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("x", encoding="utf-8") as report_file:
        report_file.write(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n")
    if blockers or differences:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
