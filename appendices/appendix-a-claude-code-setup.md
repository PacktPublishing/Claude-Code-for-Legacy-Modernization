# Appendix A: Claude Code setup for bounded modernization work

**Version and date boundary.** Release-review dates, fixture-run dates and specimen-generation dates describe different events. A printed date without its original revision and retained receipt is not certified here. Record documentation access separately from the CLI release tested; Appendix F supplies the evidence fields.

> **Practical handbook use:** Chapters 2 and 3.
>

This appendix turns the workspace controls used throughout the book into a reusable starting point. It is deliberately conservative. The example gives Claude Code enough access to inspect admitted source, propose changes in a narrow area, and run fixed local checks. It does not give the tool production credentials, deployment authority, unrestricted shell access, or permission to approve its own evidence.

The inline setup files are worked templates for the illustrative Northstar fee slice. I validated their JSON, Python, and shell structure, but I did not install these snippets in a Northstar repository or execute a Claude Code session against them. Replace every placeholder, path, command, model rule, and owner with values reviewed for the real repository. The separately published companion lab is not one of these inline snippets. Its Python baseline and helper tests were exercised under the evidence boundary stated in the companion documentation.

## What this setup controls

A usable modernisation workspace needs several controls that do different jobs:

| Control | Job | What it cannot prove |
|---|---|---|
| pinned repository revision | fixes the source under review | source behaviour is correct |
| operating-system and repository access | limits reachable files and credentials | the model will choose a safe action |
| Claude Code permissions | allows, asks for, or denies tool use | an allowed command is semantically safe |
| `CLAUDE.md` | supplies project context and working rules | a rule is enforced |
| hooks | perform deterministic checks at lifecycle points | a human judgment is correct |
| task contract | bounds one question and its return | the returned claims are supported |
| return schema | constrains response shape | execution occurred or values are true |
| worktree | isolates file edits | changes are safe to merge |
| evidence store | retains inputs, outputs, checks, and decisions | the decision was competent |
| human gates | assign acceptance, security, and release authority | the underlying evidence is complete |

Anthropic documents settings scopes, permission evaluation, project instructions, hooks, worktrees, and noninteractive CLI operation.[^1][^2][^3][^4][^5][^6] These are product mechanisms. I still use operating-system controls, protected branches, CI, credential isolation, code review, and named release authority around them.

## Start with admission, not installation

Before installing a tool in a critical repository, the accountable team should approve the use case and data boundary. The admission record names the repository, slice, data classes, provider, authentication route, allowed model set, retention rule, network path, evidence owner, and exception process.

For Northstar, the illustrative admission is narrow: inspect and test the fee-calculation slice using synthetic fixtures in an isolated worktree. Production records, customer identifiers, secrets, deployment tools, accepted evidence, and approval systems remain outside the workspace. A separate security decision would be needed to expand that boundary.

I require these human decisions before the first session:

1. The system owner approves the bounded outcome and repository.
2. Security approves the data, identity, network, and credential boundary.
3. The repository owner approves shared instructions and settings.
4. The quality owner approves the initial verification commands and evidence format.
5. Operations names prohibited production and deployment actions.
6. The modernisation lead assigns task review and stop authority.

A tool installation completed by one engineer does not satisfy those decisions.

### Isolated installation of the companion pin

The companion pin is Claude Code `2.1.170`; a newer global executable does not satisfy its compatibility check. One recorded macOS arm64 acquisition used the exact npm package below with install scripts disabled. This is a platform-specific reproducibility route, not a recommendation to replace an organization-managed installation. Have the software-supply owner approve the registry, package integrity and executable before running it.

```sh
# Run from a disposable operator staging directory, not the reviewed checkout.
# Keep npm's cache and package files in that staging directory.
npm install --prefix "$PWD/cli" --cache "$PWD/npm-cache" \
  --ignore-scripts --no-audit --no-fund \
  @anthropic-ai/claude-code@2.1.170
"$PWD/cli/node_modules/@anthropic-ai/claude-code-darwin-arm64/claude" --version
```

The recorded acquisition returned `2.1.170 (Claude Code)`. Retain the lockfile, registry integrity metadata and version output. Other operating systems need their matching approved package; do not reuse the arm64 path. Pass the approved executable to the companion wrapper with `--claude` and leave its exact-version rejection enabled. Re-pinning requires a reviewed manifest change and the same compatibility and containment drills, not editing the check until a newer version passes.

Installation and version output do not establish authentication. The recorded synthetic authentication attempts returned HTTP 401 before a tool action; they are historical failures, not current-session acceptance. A newly authorized successful model turn and the allowed/denied sentinel drills remain prerequisites. Do not weaken settings or change global credentials to bypass that gate.

## Record the actual installation

Anthropic's current setup documentation lists a native installer, Homebrew, WinGet, and platform-specific requirements.[^7] Enterprises should select one controlled distribution route, then pin or constrain versions according to their change policy. The official settings documentation also describes managed version controls.[^1]

Do not paste an installer command into an administrative shell merely because it appears in documentation. Retrieve the approved package through the enterprise route, verify it according to the organisation's software-supply process, and retain the package identity. A native installer that updates automatically may conflict with a regulated test cycle. A package-manager installation that waits for manual upgrades has a different operational risk. Choose deliberately.

The setup record should capture facts rather than screenshots alone:

```yaml
setup_id: NS-CC-SETUP-001
claim_type: illustrative
scope: northstar-fee-slice
host:
  operating_system: replace-with-observed-value
  architecture: replace-with-observed-value
installation:
  route: replace-with-approved-route
  package_source: replace-with-authorized-source
  package_digest: replace-with-verified-digest
  installed_version: replace-with-command-output
  update_policy: replace-with-approved-policy
authentication:
  provider: replace-with-approved-provider
  organization: replace-with-approved-organization
  identity_type: named-user
  credential_location: excluded-from-record
repository:
  remote: replace-with-approved-identifier
  revision: replace-with-git-revision
  worktree: replace-with-isolated-path
controls:
  managed_settings_revision: replace-with-policy-revision
  project_settings_revision: replace-with-git-revision
  instructions_revision: replace-with-git-revision
reviewers:
  platform: pending
  security: pending
  repository_owner: pending
status: not_verified
```

The credential value does not belong in the record. The record should identify how authentication was approved and where the secret is managed, without exposing the secret.

After installation, capture diagnostic output in the approved evidence store:

```bash
claude --version
claude auth status
claude doctor
git --version
python3 --version
git status --short
git rev-parse HEAD
```

These commands were not run for Northstar. A real record retains stdout, stderr, exit status, time, host identity, operator, and command revision. Redact only under an approved rule. A failed diagnostic remains part of the setup evidence.

## Create the workspace structure

The smallest useful repository layout keeps shared policy, executable checks, task inputs, proposals, and accepted evidence distinct:

```text
repository-root/
├── CLAUDE.md
├── .claude/
│   ├── settings.json
│   ├── settings.local.json
│   └── hooks/
│       └── protect_files.py
├── contracts/
│   ├── tasks/
│   │   └── NS-FEE-DISC-001.txt
│   └── returns/
│       └── discovery-return.schema.json
├── prompts/
│   └── NS-FEE-DISC-001.txt
├── evidence/
│   ├── inputs/
│   ├── proposals/
│   └── accepted/
├── fixtures/
│   └── synthetic/
├── tools/
│   └── evidence/
└── tests/
```

Commit `CLAUDE.md`, `.claude/settings.json`, hook source, contracts, schemas, and safe test fixtures after review. Keep `.claude/settings.local.json` out of version control. Anthropic documents user, project, local, and managed settings scopes, with managed settings taking the highest precedence.[^1]

It also documents that permission rules are evaluated in deny, ask, allow order rather than by the most specific text alone.[^2]

The `evidence/accepted/` directory in this example is a protected local projection or metadata path. A real programme may keep accepted or sensitive evidence in a separate controlled store. Do not copy restricted material into Git merely to match the example tree.

### Isolate the work with Git

Create the task worktree from the reviewed base revision:

```bash
git status --short
git rev-parse HEAD
git worktree add ../northstar-fee-disc-001 -b ns-fee-disc-001
git -C ../northstar-fee-disc-001 status --short
git worktree list --porcelain
```

The commands are illustrative and were not executed for Northstar. The operator must stop if the base checkout is unexpectedly dirty, the branch already exists, the returned base revision differs from the approved revision, or the worktree path resolves outside the approved storage boundary.

Git worktrees isolate checked-out files and branch state while sharing repository history.[^8] They do not isolate credentials, network access, home-directory configuration, caches, services, or databases. Use a container, virtual machine, sandbox, or dedicated account when the risk requires stronger separation.

## Write concise project instructions

Anthropic documents `CLAUDE.md` as project context loaded into sessions, not as an access-control mechanism.[^3] Keep it short enough to review and specific enough to operate.

A worked root file is:

```markdown
# Northstar fee modernization

## Outcome
Preserve approved fee behavior for the admitted product slice while creating
an independently testable replacement path.

## Repository map
- src/fees: admitted legacy fee code
- tests/fees: admitted characterization and contract tests
- fixtures/synthetic: approved synthetic inputs
- evidence/proposals: task returns awaiting human review
- evidence/accepted: read-only to agent work

## Required working method
- Begin from the task's pinned revision in a clean worktree.
- Cite file, line, revision, and observation method for every behavior claim.
- Label observations, documentation, inferences, and human decisions separately.
- Preserve failed commands and contradictions. Use unknown when evidence is absent.
- Make only the changes permitted by the active task contract.

## Verification
- Run the repository's reviewed build wrapper.
- Run only the named fee test command from the task contract.
- Return command, exit state, changed files, and evidence paths.

## Prohibited actions
- Do not read production data, secrets, personal home files, or accepted evidence.
- Do not use network, cloud, deployment, database administration, or release tools.
- Do not alter baseline inputs, approve evidence, merge, push, deploy, or sign.
- Stop when a required source or command lies outside the admitted boundary.
```

Instructions should state the actual build wrapper and test command. If those commands vary by component, put the narrower instruction beside that component or in an applicable scoped rule. Do not make Claude infer the supported command from an obsolete pipeline file.

Review instruction changes like code. A relaxed prohibition can change every later task. The repository owner should reject vague phrases such as "be careful with production" because they supply no path, tool, or stop condition.

## Apply project permissions

The settings fragment below illustrates selected permission rules and a direct-file hook. It lists read paths and local checks, asks before edits inside proposal and test paths, and denies selected sensitive reads, shell commands, accepted-evidence edits and Git publication. It does not configure a sandbox or deny WebFetch and WebSearch. The control owner must supply and test the complete read, write and network boundary before use; this fragment alone is not the admission profile.

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "defaultMode": "default",
    "allow": [
      "Read(./src/fees/**)",
      "Read(./tests/fees/**)",
      "Read(./fixtures/synthetic/**)",
      "Read(./contracts/**)",
      "Read(./evidence/inputs/**)",
      "Bash(git status *)",
      "Bash(git diff --stat)",
      "Bash(git rev-parse *)",
      "Bash(python3 -m unittest tests/fees/*)",
      "Bash(python3 tools/evidence/validate_return.py *)"
    ],
    "ask": [
      "Edit(./tests/fees/**)",
      "Edit(./evidence/proposals/**)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(./prod/**)",
      "Read(./evidence/accepted/**)",
      "Edit(./src/**)",
      "Edit(./evidence/accepted/**)",
      "Bash(curl *)",
      "Bash(wget *)",
      "Bash(ssh *)",
      "Bash(aws *)",
      "Bash(kubectl *)",
      "Bash(terraform *)",
      "Bash(git push *)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/protect_files.py\""
          }
        ]
      }
    ]
  }
}
```

This profile is not universal. The exact build command, tool names, matching behaviour, and managed controls depend on the installed release and repository. Anthropic recommends inspecting effective permissions through its permission interface and checking loaded settings sources.[^1][^2] Test one allowed action, one asked action, and every material deny rule in a disposable fixture before admitting real source.

A permission allowlist is not a shell sandbox. A permitted script can contain behaviour that its command name does not reveal. Review every allowed executable and pin its source. Outer controls should remove production credentials and network routes even if the project settings already deny their common command names.

For unattended print-mode tasks, I use the stricter `dontAsk` mode with a complete allowlist. An unlisted operation then fails rather than waiting for a person. I do not use a bypass mode in a normal developer checkout. Anthropic's permission documentation warns that bypassing prompts belongs only in strongly isolated environments.[^2]

## Add a deterministic direct-file hook

Hooks can block a tool action before it occurs, but hook code is itself privileged control code. Anthropic documents lifecycle events, matchers, input on standard input, and blocking behaviour for pre-tool hooks.[^4] Keep a hook small, review it separately, and test its failure behaviour.

The following Python 3.11 hook rejects direct Edit and Write requests whose canonical path enters a protected tree. It complements permissions. It does not inspect Bash text and does not replace the sandbox, managed policy, operating-system isolation, credential removal, or network controls.

```python
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

PROTECTED_RELATIVE = (
    Path(".env"),
    Path("secrets"),
    Path("prod"),
    Path("evidence/accepted"),
    Path(".git"),
)


def project_root() -> Path:
    raw = os.environ.get("CLAUDE_PROJECT_DIR")
    if not raw:
        raise ValueError("CLAUDE_PROJECT_DIR is required")
    return Path(raw).expanduser().resolve()


def canonical_target(root: Path, raw_path: str) -> Path:
    target = Path(raw_path).expanduser()
    if not target.is_absolute():
        target = root / target
    return target.resolve(strict=False)


def protected_marker(root: Path, raw_path: str) -> str | None:
    target = canonical_target(root, raw_path)
    for relative in PROTECTED_RELATIVE:
        protected = (root / relative).resolve(strict=False)
        if target == protected or target.is_relative_to(protected):
            return relative.as_posix()
    return None


def deny(reason: str) -> None:
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        },
        sys.stdout,
    )


def main() -> None:
    try:
        event = json.load(sys.stdin)
        if not isinstance(event, dict):
            raise ValueError("event must be an object")
        root = project_root()
        tool = event.get("tool_name")
        if not isinstance(tool, str) or not tool:
            raise ValueError("tool_name must be a nonempty string")
        tool_input = event.get("tool_input")
        if not isinstance(tool_input, dict):
            raise ValueError("tool_input must be an object")
        if tool in {"Edit", "Write"}:
            raw_path = tool_input.get("file_path")
            if not isinstance(raw_path, str) or not raw_path.strip():
                raise ValueError("missing file path")
            marker = protected_marker(root, raw_path)
            if marker:
                deny(f"protected path: {marker}")
    except (OSError, TypeError, ValueError, RuntimeError) as error:
        print(f"invalid hook event: {error}", file=sys.stderr)
        raise SystemExit(2)


if __name__ == "__main__":
    main()
```

This hook is intentionally narrow. It parses the documented event object and canonicalises direct file paths, including traversal and symlink resolution. It makes no claim about Bash. Shell commands can hide behaviour behind aliases, wrappers, encoded programs, subprocesses, or another interpreter. A generic substring matcher, and even a Bash parser, cannot prove what every invoked program will do.

Use a grammar-aware parser or AST only when the command interface has a defined grammar and the policy engine evaluates the resolved executable plus arguments. For broader command execution, use a narrow allowlisted broker or an enterprise policy engine, and enforce the decision with managed settings, a mandatory sandbox, operating-system or container isolation, credential removal, and network controls. Security scanners and endpoint telemetry can add detection. They are not substitutes for the execution boundary.

The test fixture should cover at least:

| Case | Expected hook result |
|---|---|
| edit `tests/fees/example.py` | permit |
| edit `evidence/accepted/decision.json` | block |
| edit `.env` | block |
| run approved unit-test command | not evaluated by this Edit/Write hook; test permission and sandbox controls separately |
| omit the file path from an edit event | block |
| send malformed JSON | fail closed at the Claude Code control boundary |

Test shell aliases, wrappers, encoded commands, and subprocesses against the sandbox or external policy boundary, not against this direct-file hook. The test passes only when the protected write or network action fails even though the shell spelling changes.

A hook crash is not a reason to disable the control and continue. Record the failure, stop write-capable work, repair the hook in a disposable fixture, and repeat admission checks.

## Define one bounded discovery task

The first task is read-only for the agent. Its response is captured by the operator. The broader settings fragment above is not this task's admission profile: deny agent writes, shell execution and delegation in the effective discovery profile and enforce a read-only filesystem boundary before starting. Operator capture does not grant the agent a proposal-directory exception.

```text
Task ID: NS-FEE-DISC-001
Mode: read-only discovery
Question: where is the illustrative GBP month-end fee calculated, changed,
and emitted for the admitted batch path?

Pinned inputs:
1. approved repository revision
2. src/fees and named batch interface files
3. admitted test and synthetic fixture paths
4. Chapter 7 rule-record schema (ch07-listing-002; distinct from the discovery return)
5. discovery-return.schema.json

Bounded actions:
1. search admitted paths for the named fee and its aliases
2. trace each candidate calculation to its emitted field
3. cite file, line range, symbol, and revision
4. classify each statement as observation, documentation, or inference
5. report contradictory calculations and unresolved external references
6. return findings in the response; do not create or modify files

Agent writes: none. The operator captures the response and execution records.

Do not edit source or tests. Do not use network, production data, credentials,
deployment tools, database clients, or accepted evidence. Do not choose which
contradictory rule is correct. Stop when a required source is outside scope.

Return one JSON document matching the supplied schema. Use unknown when evidence
is absent. Include commands, files read, files changed, blocked actions, and human
decisions required.
```

The task contract says what counts as a useful incomplete result. Finding an excluded scheduler reference is not failure. Following it without approval is failure.

### Constrain the return shape

A return schema makes omissions visible:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "task_id",
    "model_record",
    "input_revision",
    "claims",
    "contradictions",
    "commands",
    "files_read",
    "files_changed",
    "blocked_actions",
    "unknowns",
    "human_decisions_required"
  ],
  "properties": {
    "task_id": {"const": "NS-FEE-DISC-001"},
    "model_record": {
      "type": "object",
      "additionalProperties": false,
      "required": ["reported_model", "claude_code_version"],
      "properties": {
        "reported_model": {"type": "string", "minLength": 1},
        "claude_code_version": {"type": "string", "minLength": 1}
      }
    },
    "input_revision": {"type": "string", "minLength": 7},
    "claims": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["claim", "kind", "source", "confidence", "verification"],
        "properties": {
          "claim": {"type": "string", "minLength": 1},
          "kind": {"enum": ["observation", "documentation", "inference"]},
          "source": {"type": "string", "minLength": 1},
          "confidence": {"enum": ["low", "medium", "high"]},
          "verification": {"type": "string", "minLength": 1}
        }
      }
    },
    "contradictions": {"type": "array", "items": {"type": "string"}},
    "commands": {"type": "array", "items": {"type": "string"}},
    "files_read": {"type": "array", "items": {"type": "string"}},
    "files_changed": {"type": "array", "maxItems": 0},
    "blocked_actions": {"type": "array", "items": {"type": "string"}},
    "unknowns": {"type": "array", "items": {"type": "string"}},
    "human_decisions_required": {"type": "array", "items": {"type": "string"}}
  }
}
```

`files_changed` records agent-attributable writes and must be empty for discovery, including writes to proposal paths. The operator-owned capture files are recorded separately with actor, path, digest and capture command. Keep the complete before/after inventory, including capture files, and reconcile it with tool records and the outer write audit. Do not subtract a proposal directory wholesale or hide it with a new ignore rule. Git alone misses ignored and transient writes; an unexplained write blocks acceptance. The operator must control capture storage outside the agent's writable boundary.

Schema validation proves only that JSON has the required shape. It does not prove that the model identity was observed, a file was read, a command ran, a citation exists, or a claim follows from source. The reviewer checks those facts against retained tool and repository evidence.

## Run the task with explicit controls

Anthropic documents interactive sessions, print mode, permission modes, model selection, structured return schemas, worktrees, and diagnostic commands in its CLI and workflow documentation.[^5][^6] Product behaviour changes. Verify the installed release before accepting the invocation. The companion manifest pins the reviewed 2.1.170 spelling. Its stable wrappers check that version before execution. The reviewed-worktree wrapper uses Git to create the worktree at the approved commit because the product worktree option may choose a fresh default branch rather than the reviewed `HEAD`.

The published compatibility entry point is `scripts/claude_compat.py`. Run it from the companion lab root. The wrapper presents three stable book commands while keeping the volatile direct Claude CLI surface in one reviewed file:

| Stable wrapper command | Checks and local preparation | Underlying Claude CLI behaviour for the pinned 2.1.170 manifest |
|---|---|---|
| `python3 scripts/claude_compat.py plan` | loads and validates `compatibility/claude-code-2.1.170.json`, runs `claude --version`, and requires the reported semantic version to equal `2.1.170` | starts `claude --permission-mode plan` with the companion lab root as its working directory |
| `python3 scripts/claude_compat.py reviewed-worktree NAME --base BASE --approved-revision REVISION` | performs the same version check; requires `BASE` to be a clean Git worktree whose `HEAD` resolves to `REVISION`; runs `git -C BASE worktree add -b NAME TARGET REVISION` | starts plain `claude` in `TARGET`; it deliberately does not call `claude --worktree`, because that direct option does not establish the wrapper's reviewed-base guarantee |
| `python3 scripts/claude_compat.py structured-task --cwd CWD --prompt PROMPT --schema SCHEMA` | performs the same version check; reads the prompt and schema; after execution, parses the JSON envelope, requires `.structured_output`, validates that object against `SCHEMA`, and prints only the validated object | runs `claude -p --output-format json --json-schema SCHEMA_TEXT --permission-mode dontAsk PROMPT_TEXT` in `CWD` |

These mappings describe the checked-in wrapper and its reviewed manifest. They are not promises about later Claude Code releases. A version mismatch fails before task execution. Review a new manifest and rerun the fake-executable tests before changing the pin. The structured-task wrapper also retains the raw CLI envelope, stderr, execution metadata and validated return in a new run directory. Use `--run-dir` to name that directory and `--expected-model` when the task requires an exact envelope-reported model identity. The latter rejects missing, different or additional identities; it does not select a model. Without it, the identity check remains unverified. Duplicate JSON members are rejected before validation. A matching identity record and a clean base revision still require the separate human admission and approval records.

The second published helper is `scripts/verify_artifact.py`. Chapter contracts use it to check that a path exists and that a file contains more than whitespace. A directory passes when it contains at least one nonzero-byte file; that weaker check does not inspect the file contents. For files, each repeated `--require` value must match a complete bare or Markdown line label, a quoted key, or a table/CSV cell, rather than a substring inside another name. Its exit states distinguish invalid use, missing paths, empty artefacts, and missing fields. It does not parse Markdown semantics, establish provenance, rerun the claimed work, verify a digest, or approve a decision. The companion tests target those narrow helper semantics with Python's standard library.

For compatibility testing only, the reviewed release spells the direct plan and product-managed worktree launches as follows:

```bash
claude --permission-mode plan
# Run only inside a disposable clone of the reviewed commit, never the base checkout.
claude --worktree compatibility-smoke
```

Do not use the second command to claim a reviewed base. Use the companion reviewed-worktree wrapper for real bounded work.

The following operator-owned capture sketch is not a complete execution wrapper. Its commands run outside the agent session; they do not authorize agent file writes. Use the retained-record wrapper in Appendix B after supplying its stated lifecycle prerequisites. A worked noninteractive command is:

```bash
mkdir -p evidence/proposals/NS-FEE-DISC-001
claude -p \
  --output-format json \
  --permission-mode dontAsk \
  --json-schema "$(cat contracts/returns/discovery-return.schema.json)" \
  "$(cat prompts/NS-FEE-DISC-001.txt)" \
  > evidence/proposals/NS-FEE-DISC-001/claude-envelope.json
python3 -c 'import json,sys; json.dump(json.load(open(sys.argv[1]))["structured_output"], open(sys.argv[2], "w"), indent=2)' \
  evidence/proposals/NS-FEE-DISC-001/claude-envelope.json \
  evidence/proposals/NS-FEE-DISC-001/agent-return.json
python3 tools/evidence/validate_return.py \
  evidence/proposals/NS-FEE-DISC-001/agent-return.json
```

No Northstar invocation was executed. The real command record must capture:

- setup and task identifiers
- approved repository and worktree paths
- pinned Git revision before and after the run
- installed Claude Code version
- actual reported model identity
- effective managed, project, local, and command-line settings
- authentication route without credential value
- input and contract digests
- command, start and end time, exit state, stdout, and stderr
- tools invoked and permission decisions
- changed-file list and diff
- return-schema validation result
- reviewer disposition and rejected claims

A successful exit does not approve the task. A model field copied from the requested configuration does not independently prove which model ran. Retain the runtime's identity record and reconcile it with the approved model policy.

## Review and reject deliberately

The technical reviewer traces every claim to the cited revision and line range. The domain reviewer handles business meaning. The quality reviewer checks the proposed verification action and whether the claim is derived from an independent source. Security reviews any boundary event. The modernisation lead decides whether the task may proceed, needs more evidence, or should stop.

Reject the return when any of these conditions holds:

1. The input revision differs from the approved revision.
2. The actual model identity or installed version is absent.
3. A source path lies outside the admitted boundary.
4. A claim has no exact source or labels inference as observation.
5. A contradiction is resolved without human authority.
6. A command, read, write, or blocked action is omitted.
7. `files_changed` is nonempty for the read-only task.
8. The response claims approval, equivalence, correctness, or production readiness.
9. The session accessed a credential, production record, network route, deployment tool, or accepted evidence.
10. The return schema passes but retained execution evidence disagrees with it.

Do not repair a rejected return by editing its JSON until it passes. Preserve the raw return. Create a reviewer record and either narrow the next task, correct the workspace, add an approved input, or stop.

## Promote work only through human gates

A discovery return enters the proposal area. It does not become accepted evidence automatically. Promotion needs a reviewer record that names the task, raw return digest, repository revision, accepted and rejected claims, contradictions, limits, decision owner, date, and next permitted action.

A later write-capable task needs a new contract. It should name exact writable paths, the accepted behaviour decision, allowed verification commands, expected files, return schema, rejection criteria, and merge gate. Do not mutate the discovery contract into an implementation assignment after the session begins.

The human boundary remains explicit:

| Decision | Accountable human |
|---|---|
| admit repository and data | system owner and security owner |
| approve shared setup | repository and platform owners |
| interpret business behaviour | product or domain owner |
| accept an oracle | quality owner |
| accept architecture | architect |
| merge a change | repository owner under review policy |
| deploy, pause, or roll back | release authority and operations |
| accept retained evidence | evidence owner |

Claude Code may prepare a candidate, run an allowed check, and report a gap. It does not exercise any authority in this table.

## Setup acceptance checklist

Do not admit write-capable modernisation work until the team can answer yes, with retained evidence, to each applicable item:

- The bounded outcome, repository, slice, and non-goals have named owners.
- Data classes and excluded paths are recorded.
- Authentication uses the approved provider and organisation.
- The installation source, version, update policy, and diagnostics are retained.
- The base revision and clean worktree are recorded.
- Managed policy is present where required and cannot be relaxed locally.
- Project settings parse and their effective source is known.
- Allowed, asked, and denied actions were tested in a disposable fixture.
- Production credentials and deployment routes are absent from the workspace.
- `CLAUDE.md` contains current commands, boundaries, and stop conditions.
- Hook source is reviewed, tested, versioned, and fails safely.
- The first task is read-only and has an approved contract.
- The return schema parses and rejects extra properties.
- Raw command, tool, diff, validation, and model records have an approved store.
- Reviewers have reserved capacity and named decision rights.
- A rejected return can be preserved without blocking evidence integrity.
- No automatic step promotes a proposal into accepted evidence.

## Failure file: the copied allowlist

A worked Northstar team copies a permissive settings file from a demonstration repository. It allows the generic build script and a cloud CLI used by that demonstration. The Northstar build script contains an optional publication target, and the engineer's shell already has production credentials. The project instruction says not to deploy, but the settings permit both tools.

No deployment is needed for the failure to be material. The workspace already violates the approved boundary because an agent task can reach a credentialed publication path. The team quarantines the worktree, preserves the settings and diagnostic record, revokes exposed credentials if policy requires it, and opens a control incident. It replaces the broad script permission with fixed verification commands, removes cloud credentials from the account, adds a deny rule and outer network control, then retests the profile.

This event did not occur. It shows why repository instructions, permissions, credentials, and operating-system controls must agree.

## My position

I treat Claude Code setup as an engineering artefact, not a personal preference file. The setup has an owner, a version, tested allow and deny cases, a data boundary, a task contract, a return schema, retained execution evidence, and named human gates.

I do not begin with unrestricted implementation access and try to add governance after the first useful patch. The first accepted result should prove that the workspace can stop, report uncertainty, preserve raw evidence, and leave consequential decisions with people.

## Practice exercises

Exercise A-1. Build a setup manifest. Replace every placeholder in the illustrative manifest with observed values from an authorised disposable repository. Preserve command output and leave unknown values unknown.

Exercise A-2. Test permission evaluation. Add one safe allow rule, one ask rule, and one deny rule. Verify the effective source and result for each. Add an overlapping allow and deny case, then confirm the deny rule wins.

Exercise A-3. Exercise the Edit/Write hook. Feed allowed and protected file edits to the Python hook, then add malformed events, path traversal and symlink cases. Capture the JSON decision, exit status and stderr. Move approved test execution and blocked deployment cases to the separate permission/sandbox drill: those actions are not Edit/Write hook events.

Exercise A-4. Run read-only discovery. Use a synthetic repository and the supplied task contract. Confirm that no agent writes occurred, reconcile the separately inventoried operator capture files, and check that every claim has a revision-bound source, and excluded evidence returns as an unknown rather than an invented answer.

Exercise A-5. Reject a valid-shaped return. Construct JSON that passes the schema but cites a nonexistent file. Record why schema validity does not make the claim acceptable.

Exercise A-6. Rehearse version change. Change the approved Claude Code version in a disposable environment, rerun diagnostics and control tests, compare behaviour, and require a new setup review before accepting the version.

## Required live admission drill

The source/unit checks in this book are not a successful CLI containment drill. The retained pinned-release attempt stopped at HTTP 401 before a model/tool turn; it proves neither an allowed edit nor a denial. Do not change global authentication or report that historical failure as a live success. An approved operator must authenticate through the selected enterprise route and retain the following tests against the pinned package and composed settings in a disposable checkout.

- Preserve the project/managed settings sources and instruction/hook sentinel receipts. Normal project discovery is required; the task wrapper does not use `--bare`.
- Prove one admitted file edit and one protected-file denial, including target bytes before and after. Exercise allowed, asked, denied and unmatched actions in each supported mode. In `dontAsk`, an ask requirement is denial, not an interactive approval.
- Require an outer filesystem boundary for reads and writes, an outer network policy, and sandbox startup failure to block execution. `Read` denial alone does not constrain shell reads. Probe credential-like synthetic paths through both `Read` and Bash; retain which boundary rejected each attempt.
- Probe deletion, `git diff --no-index`, `git diff --output`, deployment, shell networking and network tools. The illustrated `git diff --stat` allow rule is deliberately narrow; it does not prove flag parsing or authorize other Git forms. Keep the outer deny-read/deny-write/egress boundaries even when a tool permission rejects the call.
- Treat plan mode as a workflow mode, not a read-only security boundary. Deny write, shell execution and delegation routes in the effective read-only profile; if that mode can bypass a required denial or Auto Mode changes the decision, do not admit the profile. Do not enable a delegation route until its child permissions pass the same drill.
- Re-review newly executable test content even when `make test` remains the same allowed command. Change the command allowlist only for a newly required command; unchanged command spelling does not approve edited code, subprocesses or network access.

Configuration inspection may be local. A model-backed critique can send admitted content over the selected provider route and incur cost; do not describe it as an offline permission check. Commands available only in newer releases require a separately reviewed compatibility upgrade, not an unrecorded change to the `2.1.170` pin.

Acquire the approved release through the enterprise-controlled official distribution route and retain package provenance plus `claude --version`. The version-checking wrapper remains fail-closed. If that release cannot be acquired or authenticated through an approved route, stop: a newer installer result or an executable smoke is not admission. Public older starter files are not evidence that this corrected publisher checkout has been released.

The product-managed smoke worktree must be created inside a disposable clone pinned to the reviewed commit. Record that clone's status before and after, keep generated `.claude/worktrees/` there, and delete only that disposable clone after retaining evidence. Do not add a broad ignore rule to the reviewed base checkout merely to conceal smoke-test output.


[^1]: Anthropic, "Claude Code settings." https://code.claude.com/docs/en/settings (accessed 23 July 2026).

[^2]: Anthropic, "Configure permissions." https://code.claude.com/docs/en/permissions (accessed 23 July 2026).

[^3]: Anthropic, "How Claude remembers your project." https://code.claude.com/docs/en/memory (accessed 23 July 2026).

[^4]: Anthropic, "Automate actions with hooks" and "Hooks reference." https://code.claude.com/docs/en/hooks-guide and https://code.claude.com/docs/en/hooks (accessed 23 July 2026).

[^5]: Anthropic, "CLI reference." https://code.claude.com/docs/en/cli-reference (accessed 23 July 2026).

[^6]: Anthropic, "Common workflows" and "Run parallel sessions with worktrees." https://code.claude.com/docs/en/common-workflows and https://code.claude.com/docs/en/worktrees (accessed 23 July 2026).

[^7]: Anthropic, "Advanced setup." https://code.claude.com/docs/en/setup (accessed 23 July 2026).

[^8]: Git project, "git-worktree." https://git-scm.com/docs/git-worktree (accessed 23 July 2026).
