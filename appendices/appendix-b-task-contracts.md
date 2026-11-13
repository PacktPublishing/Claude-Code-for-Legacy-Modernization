# Appendix B: Repeatable task contracts

## Local schema and vocabulary

The enterprise utilities and return formats in this appendix are illustrative prerequisites, not installed Python lab utilities. The supplied lab schema is `contracts/returns/task-return.schema.json` with required fields `claims`, `changed_files`, `commands`, `artifact_paths`, `unknowns`, and `stop_reason`. Use the [shared decision and alias table](../docs/runbooks/decision-rights.md): `approved` maps to `accepted` only with human approval; `not-executed` maps to `not-run`; missing required evidence is `missing`, not success. Behaviour labels, evidence labels and dispositions are separate dimensions.

> **Practical handbook use:** Chapters 3, 5 to 8, 14, and 17 to 24.
>

A Claude Code task should be reviewable before the session starts and auditable after it ends. A prompt alone does neither job.

I use a task contract to connect an approved engineering question to a pinned input set, a permitted action set, an expected return, and a human decision. The contract tells Claude Code what it may inspect and change. It also tells the reviewer what evidence must exist before any result can be accepted.

This appendix supplies reusable contracts for discovery, test creation, bounded implementation, and adversarial review. It includes a JSON Schema for the return, a standard-library validator, a command wrapper, a review record, and rejection tests. All Northstar examples are illustrative. The templates were checked as worked templates, but no Northstar Claude Code task was run.

## What a task contract must settle

A useful contract answers eleven questions before model execution:

1. What decision or engineering question does this task support?
2. Which repository revision and evidence revisions are admitted?
3. Which paths, tools, data classes, and external systems are reachable?
4. Which actions are allowed?
5. Which actions are prohibited even if they would make the task easier?
6. What files may change?
7. Which commands may run, and what do they prove?
8. What return shape is required?
9. Which statements need direct evidence?
10. What makes the result rejectable?
11. Which person owns the next decision?

A contract that says "modernise the fee service and run the tests" leaves most of those questions open. It does not identify the accepted behaviour, writable boundary, test oracle, rollback obligation, evidence store, or reviewer. The model must infer programme policy from repository fragments. That is the wrong place to put authority.

Anthropic documents that `claude -p` runs Claude Code noninteractively and that `--json-schema` can constrain structured output.[^1][^2] Anthropic also states that permissions are enforced by Claude Code rather than by prompt text.[^3]

Hooks can add deterministic checks at lifecycle events. Command hooks run with the current user's permissions and need separate review.[^6]

I therefore keep the contract, permission profile, outer workspace controls, and human review distinct. The contract states intent. Permissions and isolation limit reachable actions. Retained records show what happened. A person decides whether the result is usable.

## Use one contract for one evidence dependency

A task should stop at a decision boundary. Discovery identifies candidate rules and contradictions. It does not decide which rule is correct. Test design proposes an oracle from an accepted behaviour record. It does not accept the oracle. Implementation changes named files against an accepted oracle. It does not approve deployment. Adversarial review finds unsupported claims and missed cases. It does not merge a repair.

This separation produces smaller returns and cleaner rejection. If a discovery result is wrong, no source patch needs to be untangled from it. If the test oracle is disputed, implementation waits. If implementation fails a semantic check, the raw return remains available while the patch is rejected.

The sequence for the illustrative Northstar fee slice is:

```text
NS-FEE-DISC-001   locate rules and contradictions
        |
        v
human domain decision and accepted rule record
        |
        v
NS-FEE-TEST-002   propose tests against accepted behavior
        |
        v
human quality decision and accepted oracle
        |
        v
NS-FEE-IMPL-003   change the bounded implementation
        |
        v
human technical review
        |
        v
NS-FEE-REVIEW-004 inspect claims, patch, and evidence independently
        |
        v
human merge decision
```

Every arrow crossing into an accepted state is a human gate. Claude Code may prepare the material on either side. It does not cross the gate.

## Store contracts as versioned files

I keep each task in a directory with explicit inputs, output paths, and review records:

```text
contracts/tasks/NS-FEE-DISC-001/
├── contract.yaml
├── prompt.txt
├── return.schema.json
├── input-manifest.json
└── review-policy.yaml

evidence/runs/NS-FEE-DISC-001/
├── invocation.json
├── stdout.json
├── stderr.txt
├── exit-status.txt
├── effective-controls.json
├── changed-files.json
├── return-validation.json
└── review.json
```

The tree is a target packet, not a claim that the wrapper generates every file.

| Ownership | Files |
|---|---|
| Operator supplies before admission | `invocation.json`, `effective-controls.json`, pinned contract and input manifest |
| Wrapper generates | `claude-version.txt`, `stdout.json`, `stderr.txt`, `exit-status.txt`, before/after revision and NUL-delimited status, raw change inventories, `changed-files.json`, extracted `agent-return.json` only on valid output, `return-validation.json` on return validation or envelope failure |
| Reviewer creates | `review.json`, signed acceptance or rejection |

A failed invocation can leave a partial packet. Its nonzero exit and retained raw output are failure evidence, not a complete accepted run. Missing operator or reviewer records block admission or promotion respectively.

The contract directory is reviewed and pinned before execution. The run directory is append-only for the task operator. Accepted evidence lives elsewhere and requires a separate promotion decision. The raw return is never edited to make validation pass.

The contract identifies all files by revision or digest. A mutable path such as `rules/current.yaml` is not enough. The input manifest should record the exact bytes admitted to the task.

A worked manifest is:

```json
{
  "task_id": "NS-FEE-DISC-001",
  "claim_type": "illustrative",
  "repository_revision": "replace-with-git-revision",
  "contract_revision": "replace-with-git-revision",
  "inputs": [
    {
      "path": "src/fees/FeeCalculator.java",
      "sha256": "replace-with-observed-digest",
      "classification": "internal-source"
    },
    {
      "path": "fixtures/synthetic/month-end.json",
      "sha256": "replace-with-observed-digest",
      "classification": "synthetic"
    }
  ],
  "excluded_classes": [
    "production-customer-data",
    "credentials",
    "accepted-evidence"
  ],
  "status": "not-observed"
}
```

The placeholder digest is intentional. Do not replace it with a plausible value. A real wrapper computes the digest from the admitted file and retains the command result.

## The canonical contract

YAML is convenient for human review, but YAML syntax alone does not enforce meaning. The organisation should define a schema or validator for its chosen contract format. The following contract contains the minimum fields I expect for modernisation work:

```yaml
schema_version: "1.0"
task_id: NS-FEE-DISC-001
claim_type: illustrative
task_type: discovery
status: approved-for-controlled-run

purpose:
  question: >
    Where is the GBP month-end fee calculated, modified, and emitted for the
    admitted Northstar batch path?
  supported_decision: domain-rule-review
  non_goals:
    - decide which contradictory rule is correct
    - edit source or tests
    - assess production readiness

subject:
  repository: northstar-settlements
  repository_revision: replace-with-approved-git-revision
  slice: fee-calculation
  evidence_revision: replace-with-approved-evidence-revision

context:
  instructions:
    - CLAUDE.md
    - contracts/policies/evidence-language.md
  admitted_paths:
    - src/fees/**
    - src/batch/FeeOutputWriter.java
    - tests/fees/**
    - fixtures/synthetic/**
  excluded_paths:
    - .env*
    - secrets/**
    - prod/**
    - evidence/accepted/**
  data_classes:
    allowed:
      - internal-source
      - synthetic
    prohibited:
      - production-customer-data
      - credentials

permissions:
  mode: dontAsk
  allowed_tools:
    - Read
    - Glob
    - Grep
  denied_capabilities:
    - agent-file-write
    - shell-execution
    - delegation
    - network
    - source-edit
    - test-edit
    - deployment
    - database
    - approval

inputs:
  manifest: contracts/tasks/NS-FEE-DISC-001/input-manifest.json
  required:
    - approved repository revision
    - synthetic month-end fixture
    - rule-register schema
  stop_if_missing: true

bounded_actions:
  - locate the named fee and documented aliases in admitted paths
  - trace candidate calculations to the emitted batch field
  - cite file, line range, symbol, and repository revision
  - label each claim as observation, documentation, or inference
  - report contradictions and excluded dependencies

writes:
  allowed_paths: []
  expected_files: []
  source_changes_allowed: false
operator_capture:
  owner: task-operator
  path: evidence/runs/NS-FEE-DISC-001/
  agent_access: read-only-or-excluded
  inventory: separate actor-attributed capture paths and digests

verification:
  executor: task-operator-outside-agent-session
  commands:
    - git status --short
    - git rev-parse HEAD
  required_observations:
    - repository revision before and after the task
    - changed file list
    - return-schema validation

return:
  schema: contracts/tasks/NS-FEE-DISC-001/return.schema.json
  format: json
  unknown_value: unknown

rejection:
  - input revision differs from the approved revision
  - a claim lacks an exact source
  - an inference is labelled as an observation
  - any agent-attributable file write, including proposal files
  - a prohibited tool or path is accessed
  - a contradiction is resolved without a named human decision
  - actual model identity or installed Claude Code version is absent
  - the return claims correctness, approval, equivalence, or readiness

human_boundary:
  task_owner: modernization-lead
  technical_reviewer: legacy-engineer
  domain_reviewer: settlement-product-owner
  evidence_reviewer: quality-engineer
  next_decision: accept, reject, or request a narrower discovery task
```

The task owner should be a named person in the real record, not merely a role. I use roles in the template to avoid inventing Northstar staff.

## Write the prompt from the contract

The prompt should not duplicate hundreds of lines of policy. It should point to the approved contract, restate the question, identify the stop conditions, and require the structured return.

```text
Execute task NS-FEE-DISC-001 against the exact repository revision and input
manifest named in contract.yaml.

Answer only the approved discovery question. Follow the admitted paths, bounded
actions, and prohibited capabilities in the contract. Cite repository revision,
file, line range, and symbol for every observation. Keep observation,
documentation, and inference separate. Report contradictions without choosing a
winner. Use unknown when required evidence is absent.

Stop if the repository revision differs, an input digest fails, a required source
is excluded, or a requested action is not allowed. Do not write any files, including proposals.
The operator captures the response outside the agent write boundary.
Return one JSON document matching return.schema.json.
```

A short prompt is acceptable because the pinned contract carries the detail. A short contract is not acceptable merely because the prompt is long.

## Constrain the return without confusing shape with truth

JSON Schema defines a JSON-based format for describing the structure of JSON data.[^4] It can require properties, reject extra properties, and constrain values. It cannot prove that a command ran or a cited line exists.

This schema works across the four contract types in this appendix:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.invalid/schemas/modernization-task-return-v1.json",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "task_id",
    "task_type",
    "model_record",
    "input_record",
    "claims",
    "commands",
    "files_read",
    "files_changed",
    "checks",
    "blocked_actions",
    "unknowns",
    "human_decisions_required"
  ],
  "properties": {
    "task_id": {
      "type": "string",
      "pattern": "^[A-Z0-9]+(?:-[A-Z0-9]+)+$"
    },
    "task_type": {
      "enum": ["discovery", "test-design", "implementation", "adversarial-review"]
    },
    "model_record": {
      "type": "object",
      "additionalProperties": false,
      "required": ["reported_model", "claude_code_version", "identity_source"],
      "properties": {
        "reported_model": {"type": "string", "pattern": "\\S", "minLength": 1},
        "claude_code_version": {"type": "string", "pattern": "\\S", "minLength": 1},
        "identity_source": {"type": "string", "pattern": "\\S", "minLength": 1}
      }
    },
    "input_record": {
      "type": "object",
      "additionalProperties": false,
      "required": ["repository_revision", "contract_revision", "manifest_digest"],
      "properties": {
        "repository_revision": {"type": "string", "pattern": "\\S", "minLength": 7},
        "contract_revision": {"type": "string", "pattern": "\\S", "minLength": 7},
        "manifest_digest": {"type": "string", "pattern": "\\S", "minLength": 1}
      }
    },
    "claims": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["statement", "kind", "source", "confidence", "verification"],
        "properties": {
          "statement": {"type": "string", "pattern": "\\S", "minLength": 1},
          "kind": {"enum": ["observation", "documentation", "inference", "proposal"]},
          "source": {"type": "string", "pattern": "\\S", "minLength": 1},
          "confidence": {"enum": ["low", "medium", "high", "not-applicable"]},
          "verification": {"type": "string", "pattern": "\\S", "minLength": 1}
        }
      }
    },
    "commands": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["command", "exit_status", "output_evidence"],
        "properties": {
          "command": {"type": "string", "pattern": "\\S", "minLength": 1},
          "exit_status": {"type": ["integer", "string"], "pattern": "\\S"},
          "output_evidence": {"type": "string", "pattern": "\\S", "minLength": 1}
        }
      }
    },
    "files_read": {"type": "array", "items": {"type": "string", "pattern": "\\S"}},
    "files_changed": {"type": "array", "items": {"type": "string", "pattern": "\\S"}},
    "checks": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["name", "status", "evidence"],
        "properties": {
          "name": {"type": "string", "pattern": "\\S", "minLength": 1},
          "status": {"enum": ["passed", "failed", "not-run", "blocked"]},
          "evidence": {"type": "string", "pattern": "\\S", "minLength": 1}
        }
      }
    },
    "blocked_actions": {"type": "array", "items": {"type": "string", "pattern": "\\S"}},
    "unknowns": {"type": "array", "items": {"type": "string", "pattern": "\\S"}},
    "human_decisions_required": {"type": "array", "items": {"type": "string", "pattern": "\\S"}}
  }
}
```

The `identity_source` field matters. A requested model name copied from a command is not observed runtime identity. A real programme should retain the runtime record supplied by the approved provider or tool and state what that record can prove.

The schema permits `not-run` and `blocked` checks. This is deliberate. Forcing every check to pass encourages false reports or omission. An honest blocked task can be useful evidence.

## Four reusable task profiles

The canonical fields remain stable. The question, writable boundary, checks, and rejection conditions change with task type.

### Discovery contract

Use discovery when the team needs repository facts, data paths, rule candidates, runtime references, or contradictions.

Inputs should include a pinned source revision, admitted paths, known names and aliases, relevant build or deployment records, and the evidence vocabulary. The task may search, read, trace, and classify. It may not settle business meaning or change implementation.

Expected return:

```json
{
  "task_id": "NS-FEE-DISC-001",
  "task_type": "discovery",
  "model_record": {
    "reported_model": "replace-with-observed-runtime-value",
    "claude_code_version": "replace-with-observed-version",
    "identity_source": "replace-with-retained-runtime-record"
  },
  "input_record": {
    "repository_revision": "replace-with-approved-revision",
    "contract_revision": "replace-with-approved-revision",
    "manifest_digest": "replace-with-observed-digest"
  },
  "claims": [],
  "commands": [],
  "files_read": [],
  "files_changed": [],
  "checks": [
    {
      "name": "repository-revision-match",
      "status": "not-run",
      "evidence": "No Northstar task was executed"
    }
  ],
  "blocked_actions": [],
  "unknowns": ["No repository evidence was admitted for this publication example"],
  "human_decisions_required": ["Approve and run against an authorized repository"]
}
```

Reject discovery if it turns naming similarity into a dependency claim, resolves contradictory rules, reports an excluded source as read, or presents generated explanation as observed behaviour.

### Test-design contract

Use test design only after the team has accepted the behaviour source or clearly labelled the behaviour as characterisation rather than correctness.

The contract should name:

- the accepted rule or observation record
- the test framework and approved version
- the exact test path that may change
- fixture rules and prohibited production data
- the observation point and oracle
- determinism controls for time, randomness, identifiers, ordering, and side effects
- the command that exercises the narrow test
- mutation, property, contract, or differential checks where applicable

A worked bounded section is:

```yaml
task_id: NS-FEE-TEST-002
task_type: test-design
purpose:
  question: >
    Add characterization cases for the accepted month-end fee observations
    without declaring the observed behavior correct.
accepted_inputs:
  - evidence/accepted/rules/NS-FEE-RULES-007.json
  - fixtures/synthetic/month-end-cases.json
writes:
  allowed_paths:
    - tests/fees/MonthEndFeeCharacterizationTest.java
    - evidence/proposals/NS-FEE-TEST-002/**
  source_changes_allowed: false
verification:
  commands:
    - ./gradlew test --tests MonthEndFeeCharacterizationTest
rejection:
  - a fixture contains production-derived personal data
  - expected values lack a link to the accepted observation record
  - volatile time or identifiers remain uncontrolled
  - the task changes production source
  - a passing test is described as proof of business correctness
human_boundary:
  oracle_acceptance: quality-owner
  business-meaning: settlement-product-owner
```

Claude Code helps by finding existing test conventions, drafting fixtures, implementing the named test, and reporting failures. It cannot decide that current behaviour should survive migration. The quality owner accepts the oracle, and the domain owner decides business meaning.

### Bounded implementation contract

Implementation begins from an accepted oracle and an approved design decision. The writable set should be small enough that a reviewer can explain every changed file.

```yaml
task_id: NS-FEE-IMPL-003
task_type: implementation
purpose:
  question: >
    Implement the approved fee adapter behind the existing seam while preserving
    the accepted contract and characterization behavior.
accepted_inputs:
  - evidence/accepted/rules/NS-FEE-RULES-007.json
  - evidence/accepted/tests/NS-FEE-ORACLE-004.json
  - decisions/ADR-042-fee-adapter.md
writes:
  allowed_paths:
    - src/fees/adapter/**
    - tests/fees/adapter/**
    - evidence/proposals/NS-FEE-IMPL-003/**
  forbidden_paths:
    - src/fees/legacy/**
    - deploy/**
    - evidence/accepted/**
bounded_actions:
  - implement the approved adapter interface
  - add narrow unit tests for new adapter branches
  - run the named verification commands
  - report every changed file and remaining unknown
verification:
  commands:
    - ./gradlew test --tests FeeAdapterTest
    - ./gradlew test --tests MonthEndFeeCharacterizationTest
    - python3 tools/contracts/check_changed_paths.py NS-FEE-IMPL-003
rejection:
  - an accepted test or baseline is changed to make the implementation pass
  - legacy source, deployment, or accepted evidence changes
  - a command is reported passed without retained output and exit status
  - the adapter changes rounding, calendar, or side-effect semantics without approval
  - the result claims merge, release, or cutover authority
human_boundary:
  design_owner: solution-architect
  merge_owner: repository-owner
  release_owner: release-manager
```

The task should state expected file classes, not an expected patch. Overprescribing the patch can hide a design mistake. Underprescribing the boundary invites unrelated cleanup. I allow Claude Code to choose local implementation details inside an approved interface while requiring it to stop when the design decision is insufficient.

### Adversarial-review contract

The review task should use an independent context where practical. It receives the contract, accepted inputs, patch, and raw execution record. It does not receive a narrative telling it why the implementation is good.

```yaml
task_id: NS-FEE-REVIEW-004
task_type: adversarial-review
purpose:
  question: >
    Find unsupported claims, contract breaches, semantic risks, and missing tests
    in NS-FEE-IMPL-003.
inputs:
  - contracts/tasks/NS-FEE-IMPL-003/contract.yaml
  - evidence/runs/NS-FEE-IMPL-003/stdout.json
  - evidence/runs/NS-FEE-IMPL-003/changed-files.json
  - evidence/runs/NS-FEE-IMPL-003/return-validation.json
  - patch produced from the pinned base revision
bounded_actions:
  - compare changed paths with the writable boundary
  - trace implementation claims to the patch and command evidence
  - inspect decimal, calendar, ordering, retry, and side-effect behavior
  - identify tests weakened or derived from the same assumption as the code
  - propose verification work without editing the patch
writes:
  allowed_paths:
    - evidence/proposals/NS-FEE-REVIEW-004/**
  source_changes_allowed: false
rejection:
  - the review edits the implementation
  - a concern has no source, mechanism, or reproduction path
  - missing evidence is converted into a pass
  - the review declares the patch approved or rejected
human_boundary:
  disposition_owner: technical-reviewer
  semantic-owner: settlement-product-owner
  merge_owner: repository-owner
```

An adversarial model review is an additional oracle, not an independent guarantee. The review may share model blind spots with implementation. Keep deterministic checks, human review, and production-shaped evidence in the chain.

The chapter `verify_artifact.py --require` checks are field-presence gates, not schema or authorization checks. A required name must be a complete bare/Markdown line label, a quoted JSON key, or a table/CSV cell; `decision` does not match `auto-mode decision`, and `approved` does not match `unapproved`. Whitespace-only files fail. The chapter commands list every required field advertised for their token-checked artefacts. Presence does not establish a value, signature, approval, provenance or truth; use the canonical schema commands for the structured workspace, claim and rule records and retain separate human approval evidence.

## Run a contract without losing the execution record

Anthropic recommends bare mode for scripted and SDK calls because it skips automatically discovered project and user configuration unless those inputs are explicitly supplied.[^2] That can improve reproducibility, but it also skips `CLAUDE.md`, hooks, skills, plugins, MCP servers, and other configuration. The operator must decide which controls to supply explicitly. Bare mode does not create a sandbox. The pinned 2.1.170 release’s [embedded `--bare` help definition](https://github.com/anthropics/claude-code/releases/tag/v2.1.170) says that bare mode skips keychain reads and limits Anthropic authentication to `ANTHROPIC_API_KEY` or `apiKeyHelper` supplied through `--settings`; OAuth and keychain credentials are not read. Bedrock, Vertex and Foundry use their own credentials. Admit the chosen authentication route and verify it in a separately authorized exact-release runtime check before use; an existing OAuth login is not evidence that bare mode will authenticate.

The following wrapper uses normal project discovery, not `--bare`: required project instructions and hooks must remain loaded. Review the composed settings and run the sentinel drill before admission. The wrapper is illustrative and intentionally refuses to overwrite an existing run directory. Install the companion `scripts/capture_changes.py` at that path. Put run evidence in an explicitly ignored directory before taking the clean baseline; never broaden ignores to hide task edits. The helper retains NUL-delimited porcelain status, staged, unstaged, untracked and baseline-to-final revision diffs. `changed-files.json` includes both rename endpoints. Ignored and transient writes still need an outer audit boundary; this inventory is evidence, not a sandbox.

Use `changed-files.json` as the authoritative path inventory for boundary review. Parse it as a JSON array, not whitespace-separated text, and compare every entry, including both rename endpoints, with the admitted writable paths. The illustrative `check_changed_paths.py` policy check must consume this array; it is organisation-specific and is not supplied by the companion. The inventory includes wrapper-created evidence when those files are not ignored. Keep those paths visible and distinguish them from subject changes during review; do not add a broad ignore merely to make the inventory empty. It captures Git-observable boundary changes, not every transient write between boundaries.

```bash
#!/usr/bin/env bash
set -euo pipefail

TASK_ID="${1:?usage: run-task.sh TASK_ID EXPECTED_TYPE}"
EXPECTED_TYPE="${2:?expected type from the admitted contract is required}"
[[ "${TASK_ID}" =~ ^[A-Za-z0-9][A-Za-z0-9_-]*$ ]] || exit 24
CONTRACT_DIR="contracts/tasks/${TASK_ID}"
RUN_DIR="evidence/runs/${TASK_ID}"
SETTINGS_FILE="contracts/policies/controlled-settings.json"

if [[ ! -f "${CONTRACT_DIR}/prompt.txt" ]]; then
  printf 'missing prompt for %s\n' "${TASK_ID}" >&2
  exit 20
fi

if [[ ! -f "${CONTRACT_DIR}/return.schema.json" ]]; then
  printf 'missing return schema for %s\n' "${TASK_ID}" >&2
  exit 21
fi

if [[ -e "${RUN_DIR}" ]]; then
  printf 'run directory already exists: %s\n' "${RUN_DIR}" >&2
  exit 22
fi

mkdir -p "evidence/runs"
mkdir "${RUN_DIR}"  # Atomic refusal of ordinary directory reuse.
cp "${CONTRACT_DIR}/return.schema.json" "${RUN_DIR}/schema.original.json"
printf '%s\n' "${TASK_ID}" "${EXPECTED_TYPE}" > "${RUN_DIR}/invocation.txt"
if python3 tools/contracts/validate_task_return.py --preflight \
  "${RUN_DIR}/schema.original.json" "${TASK_ID}" "${EXPECTED_TYPE}" \
  > "${RUN_DIR}/schema.admitted.json" 2> "${RUN_DIR}/preflight.stderr"; then
  printf '0\n' > "${RUN_DIR}/preflight-status.txt"
else
  PREFLIGHT_STATUS=$?
  printf '%s\n' "${PREFLIGHT_STATUS}" > "${RUN_DIR}/preflight-status.txt"
  exit "${PREFLIGHT_STATUS}"
fi
SCHEMA_JSON="$(<"${RUN_DIR}/schema.admitted.json")"
python3 scripts/capture_changes.py begin "${RUN_DIR}"
claude --version > "${RUN_DIR}/claude-version.txt"

set +e
claude -p \
  --settings "${SETTINGS_FILE}" \
  --permission-mode dontAsk \
  --output-format json \
  --json-schema "${SCHEMA_JSON}" \
  "$(<"${CONTRACT_DIR}/prompt.txt")" \
  > "${RUN_DIR}/stdout.json" \
  2> "${RUN_DIR}/stderr.txt"
TASK_STATUS=$?
set -e

printf '%s\n' "${TASK_STATUS}" > "${RUN_DIR}/exit-status.txt"
python3 scripts/capture_changes.py end "${RUN_DIR}"

if [[ "${TASK_STATUS}" -eq 0 ]]; then
  if ! python3 -c 'import json,sys; from pathlib import Path; sys.path.insert(0,"tools/contracts"); from validate_artifacts import load_data; value=load_data(Path(sys.argv[1]),"json"); payload=value.get("structured_output") if isinstance(value,dict) else None; sys.exit("invalid or absent structured_output") if not isinstance(payload,dict) or value.get("is_error") is True else None; json.dump(payload, open(sys.argv[2], "w"), indent=2)' \
    "${RUN_DIR}/stdout.json" "${RUN_DIR}/agent-return.json"; then
    printf '%s\n' '{"structural_subset_valid":false,"reason":"invalid or absent envelope"}' > "${RUN_DIR}/return-validation.json"
    exit 23
  fi
  python3 tools/contracts/validate_task_return.py \
    "${RUN_DIR}/schema.admitted.json" \
    "${RUN_DIR}/agent-return.json" "${TASK_ID}" "${EXPECTED_TYPE}" \
    > "${RUN_DIR}/return-validation.json"
else
  printf '%s\n' \
    '{"structural_subset_valid":false,"status":"not-run","reason":"claude exit was nonzero"}' \
    > "${RUN_DIR}/return-validation.json"
  exit "${TASK_STATUS}"
fi
```

This command was not run against Northstar. Before use, verify every flag against the installed Claude Code release, test the wrapper in a disposable repository, and review whether command-line prompts or settings expose sensitive content through process inspection or logs. The wrapper still needs an input-digest check, timeout policy, effective-control capture, signal handling, and organisation-specific authentication.

Supply `TASK_ID EXPECTED_TYPE` from the independently admitted contract, never from the returned object. Preflight strictly decodes the retained original schema, checks the local dialect, checks the expected identity/type against its constraints and pins both as constants in the admitted schema. The wrapper checks preflight status before change capture or any Claude invocation, including the version probe. Failure retains the original schema, invocation, diagnostic output and exit status; `schema.admitted.json` contains a failure diagnostic when preflight fails and must not be used as a schema. The wrapper exits without launching the subject. Success uses the same admitted schema for invocation and return validation. This binds declared task type; it does not authenticate the operator's contract selection or prove filesystem containment.

The wrapper retains a failed exit. It does not treat nonzero status as permission to discard the run. It also does not promote the result.

## Validate syntax, then validate evidence

Save the following listing as `tools/contracts/validate_task_return.py`. Beside it, install the supplied companion `scripts/validate_artifacts.py` unchanged (SHA-256 `49d0b72444b96147d9279859653e94ee44b43f94e37207d9fa83e05b825b1c8c`). The runnable counterpart and schema are in `book-assets/appendices/`. The wrapper below depends on that reviewed standard-library module; it does not download dependencies or resolve remote schemas. Validate only reviewed schemas from the admitted input set.

```python
from __future__ import annotations

import json
import sys
from pathlib import Path

from validate_artifacts import ValidationError, load_data, validate, validate_schema_dialect


def admit_schema(path: Path, task_id: str, task_type: str) -> dict:
    schema = load_data(path, 'json')
    validate_schema_dialect(schema)
    if not task_id.strip() or not task_type.strip():
        raise ValidationError('expected identity and type must be nonblank')
    properties = schema.setdefault('properties', {})
    for key, expected in (('task_id', task_id), ('task_type', task_type)):
        validate(expected, properties.get(key, {}))
        properties.setdefault(key, {})['const'] = expected
    required = schema.setdefault('required', [])
    for key in ('task_id', 'task_type'):
        if key not in required:
            required.append(key)
    validate_schema_dialect(schema)
    return schema


def main() -> None:
    try:
        if len(sys.argv) == 5 and sys.argv[1] == '--preflight':
            schema = admit_schema(Path(sys.argv[2]), sys.argv[3], sys.argv[4])
            print(json.dumps(schema, sort_keys=True, allow_nan=False))
            return
        if len(sys.argv) != 5:
            raise ValidationError('usage: validate_task_return.py SCHEMA RETURN TASK_ID EXPECTED_TYPE; or --preflight SCHEMA TASK_ID EXPECTED_TYPE')
        schema = load_data(Path(sys.argv[1]), 'json')
        value = load_data(Path(sys.argv[2]), 'json')
        validate(value, schema)
        if not isinstance(value, dict):
            raise ValidationError('return must be an object')
        task_id = value.get('task_id')
        if not isinstance(task_id, str) or not task_id.strip():
            raise ValidationError('task_id must be nonblank')
        if task_id != sys.argv[3]:
            raise ValidationError('task_id does not match invocation')
        if not sys.argv[4].strip() or value.get('task_type') != sys.argv[4]:
            raise ValidationError('task_type does not match admitted invocation')
        if sys.argv[4] == 'discovery' and value.get('files_changed') != []:
            raise ValidationError('read-only discovery must have no agent file changes')
    except (ValidationError, ValueError, TypeError, OSError) as error:
        print(json.dumps({'structural_subset_valid': False, 'error': str(error)}, sort_keys=True))
        raise SystemExit(1)
    print(json.dumps({'structural_subset_valid': True, 'task_id': task_id}, sort_keys=True))


if __name__ == '__main__':
    main()
```

The script evaluates the supplied schema using the companion's fail-closed local subset, rejects duplicate members at every JSON object depth and applies the schema's nonblank string patterns. It checks nested records, declared types and unexpected fields. Discovery also requires an empty agent `files_changed`; operator capture has its own inventory as described in Appendix A. Empty arrays remain valid where the contract allows an honest incomplete return.

This is not full Draft 2020-12 evaluation. The dependency documents its supported keywords and rejects unsupported ones, including `$ref` and composition keywords. Patterns use Python regular expressions, integer values require JSON integer spelling, and date/time validation uses the dependency's documented bounded profile. Pin this local dialect with the schema. A pass establishes shape only: identity, command execution, input digests, citations, changed-path attribution and human decisions still require independent evidence review.

## Review with a disposition record

The reviewer should never overwrite the agent return. A separate record preserves the raw digest and assigns a disposition to each material claim.

```yaml
review_id: NS-FEE-DISC-001-R1
claim_type: illustrative
task_id: NS-FEE-DISC-001
raw_return:
  path: evidence/runs/NS-FEE-DISC-001/stdout.json
  sha256: replace-with-observed-digest
execution:
  exit_status: replace-with-observed-value
  repository_revision_match: not-reviewed
  contract_revision_match: not-reviewed
  input_digest_match: not-reviewed
  actual_model_identity: not-reviewed
  permission_record_reviewed: false
  changed_paths_within_boundary: not-reviewed
claim_dispositions: []
rejected_claims: []
open_contradictions: []
unknowns: []
decision: pending
next_permitted_action: none
reviewers:
  technical: pending
  domain: pending
  quality: pending
  security: not-required-until-assessed
```

Valid decisions are `accepted-as-proposal`, `rejected`, or `needs-more-evidence`. I avoid `approved` because it is unclear whether the word refers to the return, a business rule, a patch, a merge, or a release.

A discovery claim may be accepted as an observation while its business interpretation stays open. An implementation patch may be technically acceptable while release remains prohibited. Record those decisions separately.

## Rejection tests for the contract system

Test the control path with deliberately bad cases before relying on it:

| Case | Expected result | Reason |
|---|---|---|
| repository revision changed after approval | stop before task | inputs are no longer pinned |
| required input digest differs | stop before task | evidence set changed |
| return omits actual model identity | reject return | requested identity is not execution evidence |
| discovery modifies a test | reject return and preserve diff | task crossed its write boundary |
| implementation edits an accepted baseline | reject patch | oracle was changed by the subject under test |
| command says passed but no output exists | reject claim | status lacks retained evidence |
| schema passes with a nonexistent source path | reject claim | shape is valid, fact is unsupported |
| task reports a prohibited action as blocked | retain and review | the control may have worked as intended |
| task performs a prohibited action | stop and assess incident | boundary failed |
| reviewer edits raw JSON to correct a path | reject review method | raw evidence lost integrity |
| model finds no reference in admitted paths | record bounded absence | search scope cannot prove universal absence |
| human reviewer lacks domain authority | defer semantic decision | technical review cannot settle business meaning |

A blocked action is not automatically a failure. It may demonstrate that a permission or hook stopped an attempted boundary crossing. Review why the attempt occurred and whether the task wording, context, or control needs repair.

## Manage contract change

A task contract is immutable after execution starts. If scope changes, close the run and create a new contract revision or task ID. Do not add a writable path during the session and later describe it as originally approved.

The new record should explain:

- what changed
- who requested it
- why the first task could not continue
- whether any prior output remains admissible
- which input, permission, command, or decision changed
- who approved the new boundary

Minor wording changes can alter behaviour. Review prompt and contract diffs together. Permission changes receive separate control review because they change what Claude Code can do, not merely what it is asked to do.

Claude Code settings have managed, user, project, and local scopes with documented precedence.[^5] Capture the effective combination used for the run. A committed task contract cannot reveal a local approval saved outside the contract directory. A clean contract with permissive effective settings is not a controlled task.

## My position

I treat a task contract as an executable handoff between programme intent and bounded machine work. It pins evidence, limits actions, defines the return, names rejection conditions, and stops at a human decision.

I do not use a long prompt as a substitute for permissions, workspace isolation, retained command evidence, or accountable review. If the team cannot state what makes a result rejectable before execution, the task is not ready for Claude Code.

## Practice exercises

Exercise B-1. Split a broad task. Take "rewrite the settlement fee service" and separate it into discovery, rule decision, test design, implementation, adversarial review, and release decisions. Give each stage one owner and one stop condition.

Exercise B-2. Pin the inputs. In an authorised disposable repository, create an input manifest for three files. Record the Git revision and SHA-256 digest for each file. Change one byte and confirm that the pre-run check stops.

Exercise B-3. Test the return schema. Validate one complete illustrative return, then remove a required property, add an unexpected property, and use an unsupported check state. Preserve each validator result.

Exercise B-4. Test a write boundary. Create a contract that permits changes under one test directory. Make one permitted edit and one edit outside the directory in a disposable worktree. Confirm that the changed-path check rejects the second case.

Exercise B-5. Reject valid-shaped fiction. Construct a schema-valid discovery return that cites a nonexistent file and reports an unexecuted command as passed. Write a review record that rejects the claims without changing the raw return.

Exercise B-6. Exercise uncertainty. Remove one required evidence source from a discovery task. The return should identify the source as excluded or missing, report the resulting unknown, and request a human decision rather than infer a value.

Exercise B-7. Compare contexts. Run the same harmless read-only task once with explicitly supplied bare-mode configuration and once with normal project discovery in a disposable repository. Record loaded settings, instructions, hooks, tools, and output differences. Do not assume the runs are equivalent.

Exercise B-8. Review a blocked action. Configure a safe disposable deny case, ask the task to operate near that boundary, and retain the permission result. Decide whether the attempt indicates a useful control test, a bad contract, or a task that should stop.


[^1]: Anthropic, "CLI reference," Claude Code documentation. https://code.claude.com/docs/en/cli-reference (accessed 23 July 2026).

[^2]: Anthropic, "Run Claude Code programmatically," Claude Code documentation. https://code.claude.com/docs/en/headless (accessed 23 July 2026).

[^3]: Anthropic, "Configure permissions," Claude Code documentation. https://code.claude.com/docs/en/permissions (accessed 23 July 2026).

[^4]: JSON Schema project, "JSON Schema Core, Draft 2020-12." https://json-schema.org/draft/2020-12/json-schema-core.html (accessed 23 July 2026).

[^5]: Anthropic, "Claude Code settings," Claude Code documentation. https://code.claude.com/docs/en/settings (accessed 23 July 2026).

[^6]: Anthropic, "Hooks reference," Claude Code documentation. https://code.claude.com/docs/en/hooks (accessed 23 July 2026).
