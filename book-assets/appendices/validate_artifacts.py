#!/usr/bin/env python3
"""Offline validation for registered JSON and JSON-compatible YAML artifacts.

The lab deliberately uses a documented, dependency-free subset of JSON Schema.
Schemas containing unsupported assertions are rejected rather than partially
validated.
"""
from __future__ import annotations

import json
import math
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "schemas/artifacts.manifest.json"
SUPPORTED_SCHEMA_KEYS = {
    "$id",
    "$schema",
    "additionalProperties",
    "const",
    "enum",
    "format",
    "items",
    "minItems",
    "maxItems",
    "minimum",
    "minLength",
    "pattern",
    "properties",
    "required",
    "type",
}
SUPPORTED_TYPES = {"object", "array", "string", "boolean", "null", "integer", "number"}
DATE_TIME = re.compile(
    r"([0-9]{4})-([0-9]{2})-([0-9]{2})[Tt]"
    r"([0-9]{2}):([0-9]{2}):([0-9]{2})(?:\.[0-9]+)?"
    r"(?:[Zz]|[+-]([0-9]{2}):([0-9]{2}))"
)


def _valid_date_time(value: str) -> bool:
    """Bounded RFC 3339 profile: years 0001–9999, seconds 00–59.

    Fractional seconds accept any positive number of ASCII digits; no rounding
    or microsecond conversion occurs. Leap seconds are deliberately rejected
    (no leap-second table). Offsets are mandatory, 00:00 through 23:59;
    -00:00 retains RFC 3339's unknown-local-offset meaning. Lowercase t/z work.
    This is validation, not instant conversion or offset normalization.
    """
    match = DATE_TIME.fullmatch(value)
    if match is None:
        return False
    year, month, day, hour, minute, second, offset_hour, offset_minute = match.groups()
    try:
        date(int(year), int(month), int(day))
    except ValueError:
        return False
    return (
        int(hour) <= 23 and int(minute) <= 59 and int(second) <= 59
        and (offset_hour is None or (int(offset_hour) <= 23 and int(offset_minute) <= 59))
    )


class ValidationError(ValueError):
    pass


def _reject_non_finite(value: str) -> None:
    raise ValidationError(f"non-finite JSON number is not allowed: {value}")


def unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError(f"duplicate JSON member: {key}")
        result[key] = value
    return result


def load_data(path: Path, format_name: str) -> Any:
    # JSON is a strict YAML 1.2 subset. This keeps the lab dependency-free and
    # rejects broader YAML instead of pretending a partial parser is complete.
    if format_name not in {"json", "yaml-json-subset"}:
        raise ValidationError(f"unsupported format: {format_name}")
    try:
        return json.loads(path.read_text(encoding="utf-8"), parse_constant=_reject_non_finite, object_pairs_hook=unique_json_object)
    except (OSError, json.JSONDecodeError, UnicodeError) as exc:
        label = "JSON-compatible YAML" if format_name == "yaml-json-subset" else "JSON"
        raise ValidationError(f"{path}: invalid {label}: {exc}") from exc


def _json_equal(left: Any, right: Any) -> bool:
    """Compare JSON values without Python's bool/int equality collision."""
    if isinstance(left, bool) or isinstance(right, bool):
        return isinstance(left, bool) and isinstance(right, bool) and left is right
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        return left == right
    if type(left) is not type(right):
        return False
    if isinstance(left, list):
        return len(left) == len(right) and all(
            _json_equal(a, b) for a, b in zip(left, right)
        )
    if isinstance(left, dict):
        return set(left) == set(right) and all(
            _json_equal(left[key], right[key]) for key in left
        )
    return left == right


def validate_schema_dialect(schema: Any, location: str = "$schema") -> None:
    if not isinstance(schema, dict):
        raise ValidationError(f"{location}: schema must be an object")
    unsupported = sorted(set(schema) - SUPPORTED_SCHEMA_KEYS)
    if unsupported:
        raise ValidationError(f"{location}: unsupported schema keywords {unsupported}")
    expected = schema.get("type")
    if "type" in schema:
        choices = expected if isinstance(expected, list) else [expected]
        if (
            not choices
            or not all(isinstance(item, str) and item in SUPPORTED_TYPES for item in choices)
            or len(set(choices)) != len(choices)
        ):
            raise ValidationError(f"{location}.type: unsupported type declaration")
    if "enum" in schema:
        enum = schema["enum"]
        if not isinstance(enum, list) or not enum:
            raise ValidationError(f"{location}.enum: expected a non-empty array")
        for index, item in enumerate(enum):
            if any(_json_equal(item, prior) for prior in enum[:index]):
                raise ValidationError(f"{location}.enum: values must be unique")
    properties = schema.get("properties", {})
    if not isinstance(properties, dict):
        raise ValidationError(f"{location}.properties: expected object")
    for key, child in properties.items():
        validate_schema_dialect(child, f"{location}.properties.{key}")
    items = schema.get("items")
    if "items" in schema:
        validate_schema_dialect(items, f"{location}.items")
    additional = schema.get("additionalProperties")
    if "additionalProperties" in schema and not isinstance(additional, bool):
        raise ValidationError(
            f"{location}.additionalProperties: only boolean values are supported"
        )
    required = schema.get("required", [])
    if (
        not isinstance(required, list)
        or not all(isinstance(key, str) for key in required)
        or len(set(required)) != len(required)
    ):
        raise ValidationError(f"{location}.required: expected unique strings")
    if "minItems" in schema and (
        not isinstance(schema["minItems"], int)
        or isinstance(schema["minItems"], bool)
        or schema["minItems"] < 0
    ):
        raise ValidationError(f"{location}.minItems: expected a non-negative integer")
    if "maxItems" in schema and (
        type(schema["maxItems"]) is not int or schema["maxItems"] < 0
    ):
        raise ValidationError(f"{location}.maxItems: expected a non-negative integer")
    if "minLength" in schema and (
        type(schema["minLength"]) is not int or schema["minLength"] < 0
    ):
        raise ValidationError(f"{location}.minLength: expected a non-negative integer")
    if "minimum" in schema and (type(schema["minimum"]) not in (int, float) or not math.isfinite(schema["minimum"])):
        raise ValidationError(f"{location}.minimum: expected finite number")
    if "format" in schema and schema["format"] not in ("date-time", "date"):
        raise ValidationError(f"{location}.format: unsupported format")
    if "pattern" in schema:
        try:
            re.compile(schema["pattern"])
        except (TypeError, re.error) as exc:
            raise ValidationError(f"{location}.pattern: invalid regular expression") from exc


def _type_matches(value: Any, expected: str) -> bool:
    if expected == "number":
        return (
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and (not isinstance(value, float) or math.isfinite(value))
        )
    return {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "boolean": isinstance(value, bool),
        "null": value is None,
        "integer": isinstance(value, int) and not isinstance(value, bool),
    }.get(expected, False)


def validate(value: Any, schema: dict[str, Any], location: str = "$") -> None:
    validate_schema_dialect(schema)
    _validate_value(value, schema, location)


def _validate_value(value: Any, schema: dict[str, Any], location: str) -> None:
    expected = schema.get("type")
    if expected is not None:
        choices = expected if isinstance(expected, list) else [expected]
        if not any(_type_matches(value, item) for item in choices):
            raise ValidationError(f"{location}: expected type {expected}")
    if "const" in schema and not _json_equal(value, schema["const"]):
        raise ValidationError(f"{location}: expected constant {schema['const']!r}")
    if "enum" in schema and not any(
        _json_equal(value, candidate) for candidate in schema["enum"]
    ):
        raise ValidationError(f"{location}: value is not in enum")
    if type(value) in (int, float) and "minimum" in schema and value < schema["minimum"]:
        raise ValidationError(f"{location}: below minimum")
    if isinstance(value, str):
        if schema.get("format") == "date":
            try:
                if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
                    raise ValueError("date shape")
                date.fromisoformat(value)
            except ValueError as exc:
                raise ValidationError(f"{location}: invalid date") from exc
        # Python len(str) counts Unicode code points, not UTF-8 bytes/graphemes.
        if len(value) < schema.get("minLength", 0):
            raise ValidationError(f"{location}: string too short (minLength {schema['minLength']})")
        if schema.get("format") == "date-time" and not _valid_date_time(value):
            raise ValidationError(f"{location}: invalid date-time (RFC 3339 profile; no leap seconds)")
    if isinstance(value, str) and "pattern" in schema and not re.search(schema["pattern"], value):
        raise ValidationError(f"{location}: does not match {schema['pattern']!r}")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise ValidationError(f"{location}: too few items")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            raise ValidationError(f"{location}: too many items")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                _validate_value(item, item_schema, f"{location}[{index}]")
    if isinstance(value, dict):
        required = schema.get("required", [])
        missing = [key for key in required if key not in value]
        if missing:
            raise ValidationError(f"{location}: missing required keys {missing}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extra = sorted(set(value) - set(properties))
            if extra:
                raise ValidationError(f"{location}: unexpected keys {extra}")
        for key, child_schema in properties.items():
            if key in value:
                _validate_value(value[key], child_schema, f"{location}.{key}")


def resolve_registered_path(root: Path, value: Any, label: str) -> Path:
    if not isinstance(value, str) or not value:
        raise ValidationError(f"{label}: expected a non-empty relative path")
    supplied = Path(value)
    if supplied.is_absolute() or ".." in supplied.parts:
        raise ValidationError(f"{label}: path must stay within the repository")
    base = root.resolve()
    resolved = (base / supplied).resolve()
    if not resolved.is_relative_to(base):
        raise ValidationError(f"{label}: path escapes the repository")
    return resolved


def validate_registered(root: Path = ROOT, registry_path: Path = REGISTRY) -> tuple[int, int]:
    registry = load_data(registry_path, "json")
    if not isinstance(registry, dict):
        raise ValidationError("invalid artifact registry")
    if registry.get("manifest_version") != 1 or not isinstance(registry.get("artifacts"), list):
        raise ValidationError("invalid artifact registry")
    checked = skipped = 0
    for index, entry in enumerate(registry["artifacts"]):
        label = f"artifacts[{index}]"
        if not isinstance(entry, dict):
            raise ValidationError(f"{label}: expected object")
        required_keys = {"path", "schema", "format", "required"}
        if set(entry) != required_keys or not isinstance(entry.get("required"), bool):
            raise ValidationError(f"{label}: malformed registry entry")
        artifact = resolve_registered_path(root, entry["path"], f"{label}.path")
        schema_path = resolve_registered_path(root, entry["schema"], f"{label}.schema")
        if not artifact.exists() and not entry["required"]:
            skipped += 1
            continue
        if not artifact.is_file():
            raise ValidationError(f"required artifact missing: {entry['path']}")
        if not schema_path.is_file():
            raise ValidationError(f"required schema missing: {entry['schema']}")
        schema = load_data(schema_path, "json")
        validate(load_data(artifact, entry["format"]), schema)
        checked += 1
    for path in sorted((root / "schemas").glob("*.schema.json")) + sorted(
        (root / "contracts").rglob("*.schema.json")
    ):
        schema = load_data(path, "json")
        validate_schema_dialect(schema, str(path.relative_to(root)))
        if "$schema" not in schema or "type" not in schema:
            raise ValidationError(f"{path}: incomplete local schema")
    return checked, skipped


def main() -> int:
    try:
        if len(sys.argv) == 4:
            validate(load_data(Path(sys.argv[1]), sys.argv[3]), load_data(Path(sys.argv[2]), "json"))
            print("SCHEMA PASS: shape only; not provenance or authorization")
            return 0
        if len(sys.argv) != 1:
            raise ValidationError("usage: validate_artifacts.py [ARTIFACT SCHEMA json|yaml-json-subset]")
        checked, skipped = validate_registered()
    except (ValidationError, KeyError, TypeError) as exc:
        print(f"SCHEMA FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"SCHEMA PASS: {checked} registered artifacts validated, {skipped} optional artifacts absent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
