# Appendix C: Test scaffolding

## Local schema and vocabulary

The enterprise utilities and return formats in this appendix are illustrative prerequisites, not installed Python lab utilities. The supplied lab schema is `contracts/returns/task-return.schema.json` with required fields `claims`, `changed_files`, `commands`, `artifact_paths`, `unknowns`, and `stop_reason`. Use the [shared decision and alias table](../docs/runbooks/decision-rights.md): `approved` maps to `accepted` only with human approval; `not-executed` maps to `not-run`; missing required evidence is `missing`, not success. Behaviour labels, evidence labels and dispositions are separate dimensions.

> **Practical handbook use:** Chapters 8 to 12 and 20 to 23.
>

A modernisation test harness has two subjects. It tests the legacy and replacement implementations, but it must also test its own fixtures, normalizers, comparators, and side-effect controls.

I build the harness as production code with a narrower authority. It may execute approved subjects in an isolated environment, capture output, and report differences. It may not call production services, rewrite an accepted baseline, classify a business difference as harmless, or approve a migration.

This appendix supplies a reusable scaffold for characterisation, golden-master, contract, property, differential, and replay tests. The main Python example uses only the Python 3.11 standard library. Earlier revisions were exercised with synthetic fixtures; the current strict-number repair awaits authorized regression execution. It was not run against Northstar. Every Northstar path, amount, record, result, and decision remains illustrative.

## Start with the evidence question

A test type is useful only when its oracle answers the question at hand.

| Test layer | Question | Main retained evidence | Limit |
|---|---|---|---|
| characterisation | What does this revision do at this observation point? | fixture, raw result, assertion, revision | observed behaviour may be wrong |
| golden master | Did a broad normalised output change? | corpus, raw output, normalizer revision, baseline decision | normalization can hide meaning |
| contract | Does each side meet a named boundary obligation? | consumer test, provider verification, contract revision | deployed connectivity and timing remain open |
| property | Does an invariant hold across a bounded input domain? | strategy or generator, property, failing example | the property may be incomplete |
| differential | Where do old and new subjects disagree? | identical input, two raw results, comparator report | agreement can preserve a shared defect |
| replay | Does production-shaped input behave safely in isolation? | capture provenance, sanitization record, side-effect manifest | a sample is not the whole production population |
| mutation | Can the suite detect seeded code changes? | tool configuration, mutant report, survivor review | mutation score is not business correctness |

I do not begin by asking Claude Code to "add tests." I name the accepted observation or rule, the subject boundary, the input domain, the output and side effects to capture, and the person who can accept the oracle. Appendix B's test-design contract carries those decisions into one bounded task.

Python's `unittest` documentation separates fixtures, cases, suites, and runners, and says tests should run independently or in arbitrary combinations.[^1] That is a sound baseline for a modernisation harness. Shared mutable databases, wall-clock time, inherited environment variables, and live queues work against it.

## Use a repository layout that exposes authority

The layout below keeps test machinery, immutable inputs, received output, proposed evidence, and approved evidence apart:

```text
tests/modernization/
├── README.md
├── cases/
│   └── NS-FEE-001.json
├── corpora/
│   └── fee-v1/
│       ├── corpus.json
│       └── inputs/
├── contracts/
│   ├── recon-file-v1.json
│   └── return.schema.json
├── normalizers/
│   ├── fee_result.py
│   └── policy.yaml
├── comparators/
│   └── semantic_json.py
├── harness/
│   ├── run_subject.py
│   └── evidence.py
├── properties/
│   └── test_fee_properties.py
├── unit/
│   ├── test_normalizer.py
│   ├── test_comparator.py
│   └── test_side_effect_guard.py
└── replay/
    └── recording-adapters/

evidence/modernization/
├── received/
├── proposals/
└── accepted/
```

The harness may write `received/` and a task-specific proposal directory. It cannot write `accepted/`. An approval workflow owned by the evidence custodian performs promotion after review. File permissions, repository protection, and CI identity enforce that separation. A comment saying "do not edit" does not.

I version the harness with the source it tests when possible. If enterprise policy keeps evidence tooling in another repository, the execution record pins both revisions and stores the packaged harness digest. Otherwise, a later reviewer cannot tell which comparator produced a difference report.

## Define one case as data

A case manifest should contain facts needed to reproduce execution without embedding a verdict. This example uses placeholder revisions and digests rather than invented values:

```json
{
  "schema_version": "1.0",
  "case_id": "NS-FEE-001",
  "claim_type": "illustrative",
  "input": {
    "path": "tests/modernization/corpora/fee-v1/inputs/NS-FEE-001.json",
    "sha256": "replace-with-observed-digest",
    "classification": "synthetic"
  },
  "subjects": {
    "legacy": {
      "revision": "replace-with-approved-revision",
      "command": [
        "replace-with-approved-python-path",
        "replace-with-approved-absolute-legacy-wrapper-path"
      ]
    },
    "replacement": {
      "revision": "replace-with-approved-revision",
      "command": [
        "replace-with-approved-python-path",
        "replace-with-approved-absolute-replacement-wrapper-path"
      ]
    }
  },
  "controls": {
    "business_date": "2026-07-31",
    "timezone": "Europe/London",
    "locale": "en-GB",
    "seed": 41007,
    "network": "prohibited",
    "side_effect_route": "recording-adapter"
  },
  "oracle": {
    "mode": "differential",
    "normalizer_revision": "replace-with-approved-revision",
    "comparator_revision": "replace-with-approved-revision",
    "amount_tolerance_minor_units": 0
  },
  "human_boundary": {
    "oracle_owner": "quality-owner",
    "business_difference_owner": "settlement-product-owner",
    "release_owner": "release-manager"
  },
  "status": "not-executed"
}
```

The command is an argument array, not a shell string. Its executable and subject wrapper paths must resolve after the harness changes into an new retained working directory, so the manifest uses reviewed absolute paths. Python recommends an argument sequence for `subprocess`, and `subprocess.run()` can set a working directory, replace the child environment, capture streams, apply a timeout, and return the exit status.[^2] I keep `shell=False`. If the real subject needs a shell pipeline, I put it in a reviewed wrapper with a fixed interface rather than accepting arbitrary text from a manifest.

The environment field passed to `subprocess.run()` replaces the inherited environment. The harness must therefore admit required values deliberately. It should not copy every variable from the operator's login session, where cloud tokens and production endpoints may exist.

## A small differential harness

The following Python 3.11 program is runnable. It reads one JSON input, executes two approved command arrays in separate retained working directories, sends the same canonical input to each process on standard input, captures standard output and error, parses JSON output, normalises only named infrastructure fields, and writes a report plus raw stdout/stderr files, paths and hashes. Save this listing as `run_subject.py`; its runnable counterpart is in `book-assets/appendices/`.

It does not provide operating-system sandboxing or network isolation. Run it only inside an outer environment that already lacks production credentials and routes. The caller supplies a new retained capture directory. No cleanup runs automatically. Directory separation is not a security boundary. Subjects must be bounded single processes that do not spawn descendants; process-tree containment, disk quotas and interruption recovery need an approved outer runner.

```python
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
```

The report stores parsed output, which may contain sensitive data in a real programme. Apply the approved data classification, encryption, access, masking, and retention rules before use. A digest detects later byte changes. It does not prove where the bytes came from or whether the comparator was correct.

This scaffold treats only top-level `amount` as decimal money. Its normalizer removes the named volatile fields at every object depth, then compares the remaining values under the policy below while preserving list order. A real comparator should use an approved schema and field-specific policies. Do not add recursive numeric tolerance or list sorting merely to reduce differences.

The comparison gate fails on capture errors and semantic differences; successful capture alone does not pass it. The `same_json` policy keeps Booleans distinct from numbers, ignores object key order, and preserves array order. It treats equal JSON numeric values such as `1` and `1.0` as equal, so it does not preserve numeric type spelling or decimal scale. Outside top-level `amount`, strings are not coerced to numbers. For that field, `amount_minor_units` converts decimal strings and numbers to integer minor units, so equivalent representations can compare equal. This is an explicit two-decimal currency policy; it is not applied recursively by `same_json`. If an interface distinguishes decimal scale, integer versus floating representation, or another currency precision, replace this policy with a reviewed field-specific comparator before using the gate.

## Test the harness before trusting it

The unit tests below exercise exact agreement, a meaningful amount difference, ignored infrastructure fields, malformed amounts, and an executed synthetic subject. They use retained directories under an operator-supplied `APPENDIX_TEST_ROOT` and Python itself, so they do not require an external package.

```python
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

import os
import uuid

from run_subject import amount_minor_units, run_subject, semantic_compare


class SemanticComparatorTest(unittest.TestCase):
    def test_equal_values_have_no_differences(self) -> None:
        value = {"instruction_id": "I-1", "amount": "10.99", "status": "ACCEPTED"}
        self.assertEqual([], semantic_compare(value, value))

    def test_amount_difference_is_visible(self) -> None:
        left = {"instruction_id": "I-1", "amount": "10.99"}
        right = {"instruction_id": "I-1", "amount": "11.00"}
        self.assertEqual("$.amount", semantic_compare(left, right)[0]["path"])

    def test_named_infrastructure_fields_are_ignored(self) -> None:
        left = {"instruction_id": "I-1", "run_id": "A"}
        right = {"instruction_id": "I-1", "run_id": "B"}
        self.assertEqual([], semantic_compare(left, right))

    def test_fractional_minor_unit_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            amount_minor_units("10.999")

    def test_subject_receives_json_and_returns_json(self) -> None:
        program = (
            "import json,sys; value=json.load(sys.stdin); "
            "json.dump({'instruction_id': value['instruction_id'], "
            "'amount': '10.99'}, sys.stdout)"
        )
        result = run_subject(
            "synthetic-" + uuid.uuid4().hex,
            [sys.executable, "-c", program],
            {"instruction_id": "I-1"},
            5,
            Path(os.environ["APPENDIX_TEST_ROOT"]),
        )
        self.assertEqual(0, result.returncode)
        self.assertIsNone(result.parse_error)
        self.assertEqual("I-1", result.parsed["instruction_id"])


if __name__ == "__main__":
    unittest.main()
```

These tests are necessary but not sufficient. Add rejection cases for a timeout, nonzero exit, invalid JSON, unexpected field, missing field, nested amount, Unicode, oversized output, prohibited environment access, attempted network use, side-effect manifest mismatch, and report-directory reuse. Test on every supported operating system because process and temporary-file behaviour can differ.

I also test that meaningful pairs remain different after normalization. For each rule, the quality engineer supplies one pair that may collapse and one pair that must not. If both collapse, the normalizer has erased part of the oracle.

## Add properties without inventing the domain

A property test explores a defined input space. The generator is not allowed to choose the business rule.

For Northstar's worked fee result, useful candidate properties include:

- serialization followed by parsing preserves the accepted domain value
- replaying the same instruction with the same idempotency key emits no second posting
- splitting an input batch into approved partitions does not alter the combined signed amount
- adding a non-settlement metadata field does not change the fee
- moving a date within the same reviewed business-day class preserves the calendar outcome

Each property needs domain approval and boundary cases. "Fees are always positive" would be a bad generated assumption if rebates or reversals exist.

The standard library can exercise a fixed corpus of generated cases, but it does not shrink a failure. Hypothesis generates values from strategies and reports a smaller failing example when it can.[^4] If the programme admits Hypothesis, pin its version and profile, retain the failing example, and record its example database policy. Do not report the default example count as coverage.

A worked property test is:

```python
from decimal import Decimal

from hypothesis import given, strategies as st
from run_subject import amount_minor_units

minor_units = st.integers(min_value=-10_000_000, max_value=10_000_000)


@given(minor_units)
def test_minor_unit_round_trip(value: int) -> None:
    decimal_value = Decimal(value) / Decimal(100)
    rendered = format(decimal_value, ".2f")
    assert amount_minor_units(rendered) == value
```

This code was syntax checked but not executed in the project environment because Hypothesis is not installed there. The numerical bounds are illustrative. A real programme derives them from accepted interface and product limits.

Metamorphic testing is useful when an exact expected result is difficult to calculate but a relationship is known. For example, processing an approved batch permutation should preserve totals only if ordering has no business meaning. The domain owner must approve that relation before the test treats it as an oracle.

## Protect interfaces with contract scaffolds

A contract test should exercise the production consumer adapter or provider boundary, not a test-only imitation. Pact defines contract testing as checking each application in isolation against a shared understanding and generates consumer contracts during executable consumer tests.[^5]

For an HTTP consumer, the scaffold should contain:

1. the production client configured to use a local test endpoint
2. named provider states
3. minimal required request and response fields
4. boundary and rejection examples
5. contract revision and consumer revision
6. provider verification against selected deployed and pending consumer contracts
7. a retained result and deployment-selection record

For a file consumer, replace the local HTTP endpoint with an isolated directory and a completion protocol. Invoke the real parser. Include encoding, line endings, file name, record widths, header and trailer checks, ordering, duplicate behaviour, arrival window, and rejection route as separate obligations. A valid schema does not prove an operational file contract.

The harness must not publish a new contract from an unreviewed agent task. Contract publication changes what the provider may use as release evidence. Keep generated contracts under proposals until the consumer owner accepts the obligation and CI proves that the actual consumer created it.

## Record side effects rather than suppressing them silently

A replacement can return the correct JSON while posting twice to a ledger. The harness needs an explicit side-effect port for messages, files, database writes, email, and external calls.

A recording adapter should capture:

```json
{
  "case_id": "NS-FEE-001",
  "claim_type": "illustrative",
  "effects": [
    {
      "type": "ledger-posting",
      "destination": "recording-adapter",
      "business_key": "NS-ILL-0042",
      "payload_sha256": "replace-with-observed-digest",
      "sequence": 1
    }
  ],
  "prohibited_effect_attempts": [],
  "external_effect_count": 0,
  "status": "not-executed"
}
```

A stub that returns success and discards the call proves less. The recording adapter retains intent and lets the comparator inspect count, destination, business key, order, and payload. The outer sandbox blocks real destinations even if dependency injection fails.

Replay uses sanitised, approved input. It fixes clocks, random sources, identities, and completion signals. It starts each case from a known state and checks that no state leaks into the next case. Production sampling and sanitization decisions stay attached to the corpus. The harness does not label a sample representative without retained measurement.

## Use mutation testing to challenge the oracle

Line execution does not show whether an assertion would detect a changed comparison, boundary, return value, or branch. Mutation testing makes small code changes and checks whether the suite fails.

PIT's Maven plugin provides a `mutationCoverage` goal and allows target-class and target-test filters.[^6] Pin a reviewed plugin version. The official quick start uses `LATEST` for convenience, but a controlled build should not let an unreviewed release enter the evidence chain.

A worked, bounded Maven fragment is:

```xml
<plugin>
  <groupId>org.pitest</groupId>
  <artifactId>pitest-maven</artifactId>
  <version>replace-with-approved-version</version>
  <configuration>
    <targetClasses>
      <param>com.northstar.fees.adapter.*</param>
    </targetClasses>
    <targetTests>
      <param>com.northstar.fees.adapter.*Test</param>
    </targetTests>
    <threads>2</threads>
    <outputFormats>
      <param>XML</param>
      <param>HTML</param>
    </outputFormats>
  </configuration>
</plugin>
```

The command below is documented by PIT, but it was not executed for Northstar:

```bash
mvn test-compile org.pitest:pitest-maven:mutationCoverage
```

A surviving mutant starts an investigation. It can reveal a weak assertion, unreachable code, an equivalent change, a missing fixture, or an excluded test. I do not impose one universal score or ask Claude Code to delete survivors. The quality owner reviews changed-slice mutants and records dispositions.

## Bound Claude Code's role

Claude Code can inspect existing test conventions, draft a case manifest, add tests in named paths, implement a comparator from an approved policy, run fixed local commands, and return evidence pointers. It does not accept a baseline or tolerance.

The task runs in a clean worktree at a pinned revision. Project settings allow admitted reads, writes under `tests/modernization/` and a proposal directory, and fixed test commands. Production source, accepted evidence, network tools, deployment tools, and shared services remain denied. Anthropic documents project settings, managed precedence, noninteractive `-p`, and structured return options.[^7][^8]

A worked task contract is:

```text
Task ID: NS-FEE-HARNESS-001
Mode: bounded test-scaffold implementation
Goal: implement and test the approved semantic comparator for NS-FEE-001.

Pinned inputs:
1. approved repository and harness revisions
2. case manifest NS-FEE-001
3. accepted comparator policy CP-FEE-004
4. synthetic fixtures only
5. harness-return.schema.json

Allowed reads: named subject interfaces, accepted policy, existing test conventions,
and synthetic fixtures.
Allowed writes: tests/modernization/comparators/,
tests/modernization/unit/, and evidence/proposals/NS-FEE-HARNESS-001/.
Allowed commands: the named formatter, comparator unit test, and changed-path check.

Bounded actions:
1. implement only field rules present in CP-FEE-004
2. add one positive, one near-miss, and one must-remain-different case per rule
3. run the named unit tests
4. retain stdout, stderr, exit state, revision, and changed files
5. return one JSON document matching the supplied schema

Do not edit subjects, fixtures, approved baselines, accepted evidence, deployment files,
or permissions. Do not add a tolerance, sort a collection, suppress a field, access a
network, or classify a business difference. Use unknown when the policy is incomplete.
Stop if a required rule or input lies outside the admitted boundary.
```

The expected return needs these fields:

```json
{
  "task_id": "NS-FEE-HARNESS-001",
  "model_record": {
    "reported_model": "replace-with-observed-runtime-value",
    "claude_code_version": "replace-with-observed-version",
    "identity_source": "replace-with-retained-runtime-record"
  },
  "input_revisions": [],
  "rules_implemented": [],
  "tests_added": [],
  "commands": [],
  "files_read": [],
  "files_changed": [],
  "blocked_actions": [],
  "unknowns": [],
  "human_decisions_required": [],
  "status": "not-run"
}
```

A schema constrains shape. Reviewers still compare the return with Git, command logs, tool records, fixtures, and generated evidence. The actual runtime model identity must come from the approved runtime record, not the requested model string.

### Review and rejection criteria

I reject a generated scaffold when:

1. it changes a subject, accepted baseline, accepted evidence, or production configuration
2. a normalizer removes a field without an approved field-specific rule
3. a comparator introduces tolerance, sorting, coercion, or default values not present in policy
4. expected values are generated by the implementation under test
5. legacy and replacement paths share the same faulty helper as their only oracle
6. a contract test bypasses the production consumer adapter
7. replay can reach a real message, database, file-transfer, email, or payment endpoint
8. a test sleeps for completion rather than observing a protocol signal
9. a fixed seed is retained but the generated corpus bytes are not
10. a command is reported as passed without retained output and exit state
11. the actual model, tool version, repository revision, or changed-file record is absent
12. the return describes agreement as correctness or a passing suite as cutover approval

The quality owner accepts the oracle and comparator policy. The domain owner interprets business differences. The data owner approves replay inputs and sanitization. Security approves the execution boundary. Operations approves side-effect isolation and completion signals. The repository owner accepts code. Release authority decides whether evidence permits deployment. Claude Code holds none of these rights.

## Retain the run as evidence

The CLI copies the original input bytes to `<report>.streams/original-input.bin` before parsing input. `input_sha256` hashes that original copy; each subject's `input.json` is separately canonicalized and has `subject_input_sha256`. Whitespace and member order can differ between these representations. Invalid input retains the original bytes and a failure report with no subjects launched. Input and output decoding reject `NaN`, `Infinity`, `-Infinity`, and exponent overflow at every object/list depth before normalization can remove fields. Canonical input and report serialization use `allow_nan=False`. Output rejection preserves the raw stream files and adds a comparison blocker even when both subjects exit zero with identical invalid numbers.

For a report named `comparator-report.json`, the program creates `comparator-report.json.streams/legacy/` and `replacement/`. Each contains `input.json` (canonical subject input), `stdout.bin`, `stderr.bin`, and a retained `work/` directory. The report names absolute stream paths and SHA-256 digests, records exit or spawn/timeout errors, and leaves the decision `human-review-required`. Raw bytes survive malformed JSON and nonzero exits. Capture storage errors propagate as failures; retain the partial directory and do not claim a complete packet. Existing report or capture directories are refused before subject execution. No file is deleted.

The complete programme packet also needs the operator and reviewer records below. This program supplies the comparator report and its stream tree only; it does not invent environment, revision, side-effect or approval evidence. These missing records block complete-packet acceptance.

```text
evidence/modernization/received/NS-FEE-001/RUN-ID/
├── invocation.json
├── input-manifest.json
├── environment.json
├── comparator-report.json.streams/
│   ├── legacy/{input.json,stdout.bin,stderr.bin,work/}
│   └── replacement/{input.json,stdout.bin,stderr.bin,work/}
├── side-effects-legacy.json
├── side-effects-replacement.json
├── comparator-report.json
├── command-status.json
├── changed-files.json
└── digests.txt
```

The operator allocates a unique `RUN-ID` when execution starts and records the timestamp source. The small program uses the supplied report path; it does not generate a timestamp or attest run identity. If CI stores the directory as a workflow artefact, GitHub Actions supports retention configuration and returns a SHA-256 digest from `upload-artifact`.[^9] That digest and retention setting are useful evidence mechanics. They do not replace the programme's access, provenance, and archival policy.

The reviewer needs raw outputs as well as the parsed report. A parser defect can omit a field. Retaining only normalised JSON makes that defect hard to reconstruct. Binary output remains binary until an approved decoder records encoding and error policy.

## Failure file: the shared oracle

A worked Northstar team extracts a rounding helper from the legacy fee path and imports it into both the replacement service and the differential comparator. Every comparison agrees. Characterisation tests pass because their expected values were also generated through the helper.

The migration has three executions but one assumption. A mutation that changes the helper affects all three paths in the same way, so the suite remains green.

The repair separates the oracles. The team derives fixture outcomes from retained legacy observations and reviewed domain examples. The comparator converts decimal text to integer minor units through independently reviewed code. Property tests check round trips and boundaries. Mutation testing targets the replacement and comparator tests. The shared helper is removed from the evidence path.

No such Northstar run occurred. The example shows why more tests do not create independence when they share implementation code.

## My position

I keep modernisation test scaffolding small, inspectable, and less privileged than the systems it executes. Each normalizer and comparator rule has an owner, adversarial pair, revision, and retained raw input. Side effects are recorded and blocked at an outer boundary.

I do not treat a generated test suite as evidence until the harness itself has passed rejection tests and a human has accepted the oracle. Agreement between old and new code is one fact, not proof that either implementation is correct or ready to receive authority.

## Practice exercises

Exercise C-1. Build a case manifest. Select one authorised synthetic case and record its input digest, two subject revisions, controls, oracle mode, owners, and `not-executed` status. Verify that no placeholder looks like observed evidence.

Exercise C-2. Exercise the differential harness. Use two disposable Python subjects that read JSON from standard input. Make them agree, differ on amount, return invalid JSON, exit nonzero, and exceed the timeout. Retain each report and exit status.

Exercise C-3. Attack the normalizer. Add one approved volatile field and one meaningful timestamp. Create pairs that may collapse and must remain different. Reject any rule that removes both.

Exercise C-4. Add a side-effect recorder. Replace one local outbound port with a recording adapter. Verify count, destination, key, order, and payload digest. Add an outer deny control and confirm that a direct external call is blocked.

Exercise C-5. Write one property. Start from a reviewed invariant, state the valid input domain, add boundary examples, and run it with a pinned generator. Preserve the smallest failing example. Do not turn generated frequency into a coverage claim.

Exercise C-6. Test a consumer contract. Invoke the production consumer adapter against a local test boundary. Change one required field, add one reviewed optional field, alter one semantic value, and change the completion signal. Record which obligation detects each change.

Exercise C-7. Run bounded mutation analysis. Restrict mutation to one changed package and its tests. Review every survivor. Classify it as weak test, missing fixture, equivalent change, unreachable code, or unresolved. Do not use the score alone as acceptance.

Exercise C-8. Bound a Claude Code task. Apply the task contract in this appendix to a disposable repository. Reject changes outside test and proposal paths, unapproved tolerance, altered fixtures, missing command evidence, or any claim of compatibility approval.


[^1]: Python Software Foundation, "unittest, Unit testing framework," Python 3 documentation. https://docs.python.org/3/library/unittest.html (accessed 23 July 2026).

[^2]: Python Software Foundation, "subprocess, Subprocess management," Python 3 documentation. https://docs.python.org/3/library/subprocess.html (accessed 23 July 2026).

[^3]: Python Software Foundation, "tempfile, Generate temporary files and directories," Python 3 documentation. https://docs.python.org/3/library/tempfile.html (accessed 23 July 2026).

[^4]: Hypothesis project, "Quickstart," Hypothesis documentation. https://hypothesis.readthedocs.io/en/latest/quickstart.html (accessed 23 July 2026).

[^5]: Pact Foundation, "Pact Docs: Introduction." https://docs.pact.io/ (accessed 23 July 2026).

[^6]: PIT project, "Quickstart for Maven users." https://pitest.org/quickstart/maven/ (accessed 23 July 2026).

[^7]: Anthropic, "CLI reference," Claude Code documentation. https://code.claude.com/docs/en/cli-reference (accessed 23 July 2026).

[^8]: Anthropic, "Claude Code settings," Claude Code documentation. https://code.claude.com/docs/en/settings (accessed 23 July 2026).

[^9]: GitHub, "Store and share data with workflow artefacts." https://docs.github.com/en/actions/tutorials/store-and-share-data (accessed 23 July 2026).
