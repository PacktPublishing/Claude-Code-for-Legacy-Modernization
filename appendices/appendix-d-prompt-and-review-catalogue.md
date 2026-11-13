# Appendix D: Prompt and review catalogue

## Local schema and vocabulary

The enterprise utilities and return formats in this appendix are illustrative prerequisites, not installed Python lab utilities. The supplied lab schema is `contracts/returns/task-return.schema.json` with required fields `claims`, `changed_files`, `commands`, `artifact_paths`, `unknowns`, and `stop_reason`. Use the [shared decision and alias table](../docs/runbooks/decision-rights.md): `approved` maps to `accepted` only with human approval; `not-executed` maps to `not-run`; missing required evidence is `missing`, not success. Behaviour labels, evidence labels and dispositions are separate dimensions.

> **Practical handbook use:** Chapters 1 to 26.
>

A useful Claude Code prompt does not ask for confidence. It creates conditions under which a reviewer can detect an incomplete or unsupported result.

The patterns in this appendix are copy-ready task contracts for recurring modernisation work. Each one fixes the scope, permissions, inputs, output, evidence, stop conditions, human review, and rejection criteria. Replace every value in angle brackets before use. If a value is not known, write `unknown` and decide whether that unknown blocks the task. Do not let Claude Code fill a missing approval, architecture decision, or acceptance rule with a plausible default.

These templates complement Appendix B's contract machinery and Appendix C's test scaffold. They do not replace repository permissions, an isolated worktree, protected evidence storage, CI controls, or review by people who know the system. A prompt can prohibit an action, but the workspace should also make the action unavailable.

All Northstar names and examples are illustrative. The templates were checked as template text. No Northstar task, test, build, release, or production operation was run for this appendix.

## How to use the catalogue

Start with the smallest pattern that answers one engineering question. Discovery should usually precede implementation. A returned task remains a proposal until the named reviewers accept specific claims or changes.

Before starting a session:

1. Replace every placeholder.
2. Pin the repository revision and each evidence input.
3. Confirm that allowed paths and commands match effective permissions.
4. Reserve the reviewers named in the contract.
5. Decide what makes the task stop rather than expand.
6. Store the raw return, command output, diff, and review record separately.

Every contract below preserves the same authority boundary. People decide architecture, business meaning, risk treatment, release, rollback, and acceptance. Claude Code may trace, propose, implement inside an accepted boundary, execute allowed checks, and package evidence. It may not promote its own result.

The suggested output tables are intentionally repetitive. Repetition makes omissions visible. A fluent narrative can hide a missing source, failed command, or unresolved contradiction. A row with an empty `evidence` field cannot.

## Pattern 1: Read-only discovery

Use this pattern to answer one bounded question before any edit is permitted.

```text
Task ID: <DISCOVERY-ID>
Mode: read-only discovery
Question: <one question about one component, behavior, flow, or boundary>

Scope:
- Repository: <repository identifier>
- Revision: <immutable revision>
- Included paths: <exact paths or globs>
- Included symbols or flows: <names>
- Excluded paths and systems: <exact exclusions>

Permissions:
- May read only the included paths and admitted evidence inputs.
- May run only: <fixed search, inspection, or build-metadata commands>.
- Must return the final answer on stdout; the caller stores it outside the repository.
- Must not write repository files; files_changed must remain empty.
- Must not edit source, tests, configuration, baselines, or accepted evidence.
- Must not use network, production data, credentials, deployment tools, or database clients.

Inputs:
1. <repository revision record>
2. <system or slice boundary revision>
3. <known aliases, entry points, or identifiers>
4. <output schema or table format>
5. <project instructions and permission profile revision>

Outputs:
Return:
1. a direct answer, or `unknown`
2. a claim table with claim ID, claim text, claim type, source location, confidence, and verification action
3. entry points, exits, side effects, and external references found
4. contradictions and missing evidence
5. files read and commands executed, including exit states
6. blocked actions and human decisions required
7. confirmation that no repository files changed

Evidence expectations:
- Cite repository revision, path, symbol, and line range for each source claim.
- Separate observed code structure, documented intent, and inference.
- Link command claims to retained stdout, stderr, and exit state.
- Treat excluded references as gaps, not evidence.

Stop conditions:
- Stop when a required path, data class, tool, or system lies outside scope.
- Stop when the pinned revision differs from the workspace revision.
- Stop after <time, file-count, or path boundary>, even if the question remains open.
- Return partial findings and the exact blocker. Do not broaden the search.

Human review:
- <legacy specialist> checks trace completeness.
- <domain owner> reviews business interpretation.
- <security owner> reviews any boundary event.
- <modernization lead> decides the next task. Claude Code makes none of these decisions.

Rejection criteria:
Reject if a claim lacks an exact source, an inference is presented as observation,
a file changed, a command is omitted, an exclusion was crossed, a contradiction
was resolved by guessing, or the return claims correctness, approval, or readiness.
```

A good discovery return can be incomplete. The required result is an inspectable boundary between what the admitted evidence supports and what it does not.

## Pattern 2: Dependency mapping

Use this pattern to build evidence-backed edges rather than a directory diagram.

```text
Task ID: <DEPENDENCY-ID>
Mode: read-only dependency mapping
Question: Which dependencies can affect <bounded component or outcome>?

Scope:
- Repository and revision: <identifier and immutable revision>
- Components: <component list>
- Dependency layers: repository, build, package, packaged artifact,
  configuration, runtime candidate, external service, owner, and change risk
- Exclusions: <paths, environments, data, and systems>

Permissions:
- Read included source, build manifests, lock files, deployment descriptions,
  configuration templates, approved inventories, and ownership records.
- Run only <fixed dependency and repository inspection commands>.
- No edits, dependency resolution from the network, package upgrades, runtime
  probes, production access, or calls to external services.

Inputs:
1. pinned source and build revisions
2. approved component boundary
3. lock files or resolved dependency reports at <revision>
4. admitted configuration and deployment records
5. ownership and risk register revisions
6. dependency-edge output schema

Outputs:
- component census with build and packaged artifacts
- one row per edge: source node, target node, edge layer, mechanism, evidence,
  confidence, owner, consequence, and verification action
- unresolved binaries, aliases, generated files, configured endpoints, and plugins
- static versus observed distinctions
- dead-code hypotheses, never dead-code conclusions
- commands, files read, gaps, blocked actions, and required human decisions

Evidence expectations:
- A source import supports a declared-code edge only.
- A lock file or resolved report supports a resolved-package edge.
- Packaging evidence supports inclusion, not runtime use.
- Configuration supports a possible runtime edge unless execution evidence confirms it.
- Every edge cites its evidence revision and location.
- Every ownership claim cites a maintained record or is marked unknown.

Stop conditions:
- Stop at an excluded repository, unresolved generated artifact, unavailable package
  registry, secret-backed configuration, or production-only observation.
- Stop if a command would mutate caches or lock files beyond the admitted policy.
- Do not infer a target from a similar name.

Human review:
- <build or platform owner> checks build and package edges.
- <architect> reviews boundary and risk implications.
- <service owners> confirm external and ownership edges.
- Humans decide architecture and whether an unknown edge blocks change.

Rejection criteria:
Reject if all arrows mean the same thing, evidence layers are collapsed, runtime use
is inferred from an import, owner is guessed from Git activity, dead code is declared
without runtime and consumer evidence, commands changed the workspace, or the map
claims architectural approval.
```

The output should allow a reviewer to challenge one edge without redrawing the whole map.

## Pattern 3: Business-rule extraction

Use this pattern to create candidate rules with provenance and consequence.

```text
Task ID: <RULE-ID>
Mode: read-only candidate rule extraction
Question: What candidate rules govern <bounded decision or output>?

Scope:
- Revision and paths: <immutable revision and exact paths>
- Entry and observation points: <symbols or interfaces>
- Rule classes: eligibility, calculation, ordering, timing, default, exception,
  negative rule, side effect, and manual control
- Excluded products, regions, paths, and records: <list>

Permissions:
- Read admitted code, tests, approved fixtures, documentation, tickets, and runbooks.
- Run only <fixed read-only commands>.
- Do not edit, query production, interview people autonomously, or access excluded data.
- Do not decide policy, intent, defect status, or required future behavior.

Inputs:
1. repository revision
2. admitted source and evidence inventory
3. terminology and identifier list
4. rule-catalogue schema and confidence rubric
5. named decision owners

Outputs:
For each candidate rule return:
- stable ID and plain-language statement
- trigger, preconditions, action, output, side effects, and exceptions
- positive, negative, ordering, or timing classification
- exact source and test locations
- corroborating and conflicting evidence
- confidence as high, medium, or low, with rationale
- consequence if wrong
- next verification action and human owner
Also return untraced outputs, unreachable references, commands, and gaps.

Evidence expectations:
- Executable behavior, comments, tests, documentation, and operational practice remain
  separate evidence types.
- A comment does not override executable behavior.
- A test proves only its observed assertion at its revision.
- Confidence reflects provenance and corroboration, not writing fluency.
- Every summarized rule remains linked to source fragments that a reviewer can inspect.

Stop conditions:
- Stop at a rule whose meaning depends on excluded data, configuration, consumer
  behavior, or domain judgment.
- Stop when two sources disagree. Record the contradiction instead of selecting one.
- Stop if determining reachability requires production access.

Human review:
- <legacy specialist> checks source tracing.
- <domain owner> decides intended meaning and rule disposition.
- <operations owner> confirms manual controls and exceptions.
- <risk owner> decides how much uncertainty is acceptable.

Rejection criteria:
Reject if candidate is called approved, intent is inferred from a comment, an exception
or negative rule is omitted, confidence lacks rationale, contradictory evidence is
merged into one statement, a policy decision is made, or a source citation cannot be
reproduced at the pinned revision.
```

A high-confidence source trace can still describe an unwanted defect. Confidence and approval answer different questions.

## Pattern 4: Contradiction check

Use this pattern after discovery or rule extraction and before deriving tests or implementation requirements.

```text
Task ID: <CONTRADICTION-ID>
Mode: read-only contradiction analysis
Question: Where do admitted sources disagree about <bounded claim set>?

Scope:
- Claim IDs: <exact IDs>
- Evidence revisions: <catalogues, source, tests, contracts, runbooks, observations>
- Comparison dimensions: trigger, value, ordering, time, exception, side effect,
  consumer meaning, and operational treatment
- Exclusions: <list>

Permissions:
- Read only the named claims and admitted supporting evidence.
- Run only <fixed inspection commands>.
- No edits, baseline updates, policy decisions, production queries, or source expansion.

Inputs:
1. candidate claim catalogue revision
2. complete admitted evidence index
3. source priority labels, not an automatic winner hierarchy
4. contradiction-return format
5. named claim owners

Outputs:
- one contradiction row per disagreement
- claim IDs and exact competing statements
- evidence type, revision, and location for each side
- whether the disagreement concerns execution, intent, environment, time period,
  product scope, or terminology
- consequence, affected tests or consumers, and smallest next verification action
- duplicates that are equivalent only after an explicit normalization
- unresolved unknowns, commands, and decisions required

Evidence expectations:
- Quote or precisely summarise both sides without harmonizing their wording.
- Show whether evidence applies to the same product, date, environment, and input class.
- Preserve source chronology without assuming newer is correct.
- Link each proposed verification action to the disagreement it could resolve.

Stop conditions:
- Stop when resolution requires business authority, consumer confirmation, production
  observation, or access outside scope.
- Stop if the evidence index is incomplete for a claim marked complete.
- Do not create a synthesized third rule.

Human review:
- <domain owner> resolves business meaning.
- <quality owner> decides whether tests represent competing hypotheses.
- <architect or operations owner> resolves system-boundary or runtime disputes.
- <modernization lead> records blocked downstream tasks.

Rejection criteria:
Reject if the return chooses a winner, uses confidence as authority, silently narrows
scope, rewrites evidence to remove disagreement, omits consequence, changes an accepted
record, or allows dependent implementation to proceed while the contradiction is material.
```

Contradiction work is valuable because it stops one plausible interpretation from producing both code and proof.

## Pattern 5: Characterisation-test design

Use this pattern to preserve observed behaviour without certifying that behaviour as correct.

```text
Task ID: <CHARACTERIZATION-ID>
Mode: bounded characterization-test proposal
Question: What does <legacy revision> do for <approved case partition> at <observation point>?

Scope:
- Legacy revision and seam: <revision and boundary>
- Writable paths: <test proposal and synthetic fixture paths only>
- Case partitions: normal, boundary, error, retry, duplicate, ordering, and <domain cases>
- Side effects to capture: <state, events, files, calls, exceptions>
- Exclusions: production code, approved baselines, real endpoints, and production data

Permissions:
- Read admitted legacy source, accepted rule records, incidents, and fixture contracts.
- Edit only <exact test and proposal paths>.
- Run only <fixed fixture setup and focused test commands> in an isolated environment.
- No production source edits, network, shared database, baseline promotion, or acceptance.

Inputs:
1. pinned legacy revision and clean worktree record
2. approved observation point and side-effect inventory
3. admitted synthetic or sanitized fixtures with revisions
4. accepted rules plus unresolved contradiction IDs
5. test framework and return schema revisions

Outputs:
- test cases with case ID, evidence source, input, setup, observation, raw actual result,
  assertion proposal, and behavior status
- deterministic clock, randomness, identifier, locale, timezone, and dependency controls
- captured response, state, event, exception, and prohibited-call evidence
- commands, exit states, changed files, failed tests, gaps, and human decisions
- no assertion update merely to obtain a pass

Evidence expectations:
- Expected values come from retained observation or separately approved evidence.
- Record a first-run failure and its cause rather than hiding it.
- Label behavior `observed`, `approved`, `disputed`, `known defect`, or `unknown`.
- Retain raw observations before normalization.
- Cite the independent evidence that would expose a wrong source interpretation.

Stop conditions:
- Stop if a fixture requires real customer data or an external effect.
- Stop if determinism requires a production-code change outside the accepted seam.
- Stop when a disputed rule would become an oracle.
- Stop if the legacy subject cannot run in the isolated environment.

Human review:
- <quality owner> approves observation points, fixtures, and oracles.
- <domain owner> assigns behavior status.
- <operations or security owner> approves side-effect isolation and data treatment.
- Humans decide whether a failing observation is preserved, corrected, or investigated.

Rejection criteria:
Reject if tests mirror private methods without an external claim, expected values come
from the same unverified interpretation, volatile fields are ignored broadly, side
effects are absent, a known failure is converted to green, production code changed,
or the return claims correctness or acceptance.
```

Characterisation tests are alarms around selected observations. They are not votes for the legacy implementation.

## Pattern 6: Contract-test design

Use this pattern when a consumer-facing interface, message, file, or state boundary must survive a migration.

```text
Task ID: <CONTRACT-ID>
Mode: bounded contract-test proposal
Question: Which observable obligations must <provider> satisfy for <named consumers>?

Scope:
- Interface and version: <API, event, file, schema, protocol, or table boundary>
- Providers and consumers: <named systems and owners>
- Writable paths: <contract proposal, fixtures, and contract-test paths>
- Dimensions: syntax, required fields, types, semantics, ordering, errors, retries,
  idempotency, compatibility, and timing class
- Exclusions: provider implementation, production deployment, and unowned consumers

Permissions:
- Read approved interface descriptions, consumer code, fixtures, and change records.
- Edit only named contract proposal and test paths.
- Run only fixture-local provider and consumer verification commands.
- Do not publish contracts, call live consumers, change schemas, or select a version policy.

Inputs:
1. provider and consumer revisions
2. approved interface inventory and owner list
3. current contract and compatibility decisions
4. admitted consumer examples and sanitized fixtures
5. test runner and return schema revisions

Outputs:
- obligation table with consumer, field or interaction, meaning, evidence, and owner
- positive and negative fixtures, including missing, extra, invalid, duplicate, reordered,
  retry, timeout, and version cases where applicable
- provider verification proposal and consumer expectation proposal
- uncovered consumers and conflicting expectations
- commands, raw results, changed files, gaps, and decisions required

Evidence expectations:
- Each obligation cites consumer-owned evidence or a human-approved contract decision.
- Distinguish wire equality from semantic compatibility.
- Preserve unknown fields and consumer-specific parsing behavior in the evidence.
- Record which side authored each oracle and how correlated it is with implementation.

Stop conditions:
- Stop at an ownerless consumer, incompatible consumer expectations, missing version
  decision, restricted fixture, or need for a live endpoint.
- Stop if a contract change would be required to make a test pass.

Human review:
- <consumer owners> accept their obligations.
- <provider owner> confirms feasibility without redefining consumer need.
- <architect> owns versioning and boundary decisions.
- <quality owner> accepts the oracle. <release authority> owns rollout timing.

Rejection criteria:
Reject if one consumer is treated as all consumers, schema validity is called semantic
compatibility, unknown consumers disappear, a generated fixture becomes an approved
contract, errors or retries are omitted, implementation is edited, or Claude Code claims
that a provider is safe to release.
```

Contract tests protect obligations at a boundary. They do not grant either provider or consumer authority over the whole business process.

## Pattern 7: Bounded implementation

Use this pattern only after the seam, behaviour inputs, acceptance rows, and rollback implications have human approval.

```text
Task ID: <IMPLEMENTATION-ID>
Mode: bounded candidate implementation in an isolated worktree
Goal: implement <one accepted behavior or structural change> behind <accepted seam>.

Scope:
- Base revision: <immutable revision>
- Writable production paths: <exact paths>
- Writable test and proposal paths: <exact paths>
- Expected files: <list or maximum>
- Non-goals: <architecture changes, upgrades, cleanup, adjacent behavior>

Permissions:
- Read only named source, accepted contracts, rules, tests, and architecture decisions.
- Edit only the declared write set.
- Run only <fixed formatter, build, unit, characterization, and contract commands>.
- No network, dependency upgrades, baseline edits, deployment, push, merge, production
  access, data-authority change, or release action.

Inputs:
1. clean worktree and base-revision record
2. accepted seam and architecture decision revisions
3. accepted rule, contract, and behavior IDs
4. acceptance rows and prohibited-difference list
5. approved fixtures and focused verification commands
6. return schema and reviewer assignments

Outputs:
- minimal diff implementing only the goal
- mapping from each behavior branch to an accepted input ID
- tests added or changed, with oracle provenance
- commands with stdout, stderr, exit states, and output locations
- changed-file list, diff digest, assumptions, unsupported cases, and remaining gaps
- explicit confirmation that deployment, release, rollback, and acceptance were not attempted

Evidence expectations:
- Every material code path cites an accepted behavior, contract, or architecture input.
- Preserve failed commands and full focused test reports.
- Explain every changed file and any generated file.
- Report tests not run and why.
- Do not use the implementation itself as the sole source of expected results.

Stop conditions:
- Stop if the change needs a new business rule, architecture decision, contract change,
  dependency upgrade, data migration, wider write set, or weaker oracle.
- Stop after <diff-size, file-count, or elapsed-work limit>.
- Stop on an unexpected existing failure unless the contract defines its treatment.
- Return a partial diff as unaccepted work. Do not improvise around the blocker.

Human review:
- <architect> accepts structure and dependency direction.
- <domain owner> confirms behavior links.
- <quality owner> reviews tests and oracles.
- <security and operations owners> review relevant consequences.
- <repository owner> controls merge. <release authority> controls release and rollback.

Rejection criteria:
Reject if the diff leaves the write set, includes opportunistic cleanup, changes an
oracle or accepted baseline to pass, omits a failed command, adds an unapproved library,
invents a rule, changes architecture or data authority, or claims merge, release,
rollback, production safety, equivalence, or acceptance authority.
```

The implementation return is a candidate patch. Passing allowed checks does not change its status.

## Pattern 8: Adversarial review

Use this pattern with a context independent from the implementation session. The reviewer reports findings and does not repair them in the same task.

```text
Task ID: <ADVERSARIAL-ID>
Mode: read-only adversarial review
Question: What could make <candidate return or diff> unsafe, unsupported, incomplete,
misleading, or difficult to reverse?

Scope:
- Base and candidate revisions: <immutable revisions>
- Diff and task contract: <identifiers>
- Accepted evidence inputs: <exact revisions>
- Review dimensions: scope, behavior, architecture, data, security, operations,
  tests, oracle independence, failure handling, observability, and reversibility
- Exclusions: repair, merge, deployment, and production execution

Permissions:
- Read the contract, diff, admitted source, test reports, and evidence links.
- Run only <fixed diff, static, and focused read-only verification commands>.
- No edits, new implementation, baseline changes, external calls, or approval actions.

Inputs:
1. raw implementation return and diff digest
2. original task contract and effective permission record
3. accepted behavior, contract, architecture, acceptance, and rollback inputs
4. actual command and test records
5. known-risk and unsupported-case lists

Outputs:
- finding table with severity proposal, claim challenged, evidence, consequence,
  reproduction or inspection step, and human owner
- scope escapes and unexplained changed files
- missing failure, boundary, retry, concurrency, and side-effect cases
- correlated oracles and tests that could agree with a wrong implementation
- rollback, monitoring, and operational assumptions
- clean findings section stating what was checked but not proven
- commands, gaps, and no file changes

Evidence expectations:
- Cite the exact diff hunk, source, test, or missing contract field behind each finding.
- Distinguish demonstrated defect, supported concern, and hypothesis.
- Try at least <named adversarial cases> supplied by the quality owner.
- A missing finding is not proof that the patch is safe.

Stop conditions:
- Stop when reproduction would mutate data, call a live system, exceed permissions,
  require sensitive inputs, or become a repair task.
- Stop if accepted evidence revisions differ from those used by implementation.

Human review:
- <technical owner> validates technical findings.
- <domain, quality, security, and operations owners> classify findings in their areas.
- <architect> decides design consequences.
- <modernization lead> decides rework or rejection. Claude Code assigns no final severity.

Rejection criteria:
Reject if review edits the candidate, invents evidence, treats absence of findings as
approval, ignores failed checks, uses unapproved attacks or data, collapses hypotheses
into defects, or claims architecture acceptance, release readiness, or acceptable risk.
```

A useful adversarial review is specific enough to reproduce and modest enough to admit what it did not inspect.

## Pattern 9: Unsupported-claim check

Use this pattern on reports, pull-request descriptions, rule catalogues, test summaries, and evidence narratives before human approval.

```text
Task ID: <CLAIM-CHECK-ID>
Mode: read-only unsupported-claim audit
Question: Which material statements in <document set> exceed their cited evidence?

Scope:
- Documents: <exact files and revisions>
- Claims in scope: behavior, completeness, correctness, equivalence, performance,
  security, ownership, compliance, readiness, and productivity
- Evidence index: <approved index revision>
- Exclusions: rewriting claims, creating missing evidence, or deciding acceptance

Permissions:
- Read only the named documents and admitted evidence index.
- Follow only local, revision-pinned links inside the admitted boundary.
- Run only <fixed link, schema, and repository inspection commands>.
- No edits, web research, production queries, execution of unapproved tests, or approvals.

Inputs:
1. immutable document revisions
2. evidence-label definitions
3. approved evidence index and retention locations
4. claim-audit output schema
5. materiality and reviewer-owner map

Outputs:
For each material claim return:
- exact quotation and location
- claim category and evidence label used
- cited evidence, revision, and location
- support status: supported, partly supported, unsupported, contradicted, or unverifiable
- reasoning limited to the admitted evidence
- consequence of overstatement
- smallest correction or verification request
Also return broken links, mutable references, missing execution records, and scope limits.

Evidence expectations:
- A passing test supports only the cases, revision, environment, and observations run.
- A schema-valid return supports shape, not truth.
- Generated code volume does not support productivity or outcome claims.
- A matching differential result does not support correctness outside compared observations.
- Vendor documentation supports documented product behavior, not local control effectiveness.

Stop conditions:
- Stop at a claim needing external research, privileged evidence, or human judgment.
- Mark it unverifiable rather than supplying remembered facts.
- Stop if the document revision changes during review.

Human review:
- <evidence owner> checks links and provenance.
- <claim owner> accepts correction or supplies evidence.
- <quality, security, compliance, or operations owner> reviews specialist claims.
- <release authority> decides whether unsupported readiness claims block release.

Rejection criteria:
Reject if the audit silently rewrites the source, relies on uncited memory, treats missing
evidence as falsehood without distinction, accepts a self-reported command as execution
proof, ignores qualifiers or scope, or itself declares risk, compliance, release, or
acceptance approved.
```

This check is especially useful when a technically accurate result has acquired a stronger headline during reporting.

## Pattern 10: Evidence packaging

Use this pattern after work returns and before a human gate. Packaging preserves provenance. It does not approve content.

```text
Task ID: <EVIDENCE-ID>
Mode: evidence packaging and integrity check
Question: Is the evidence packet for <task or slice> complete, internally linked,
and ready for named human review?

Scope:
- Task and slice IDs: <identifiers>
- Proposal artefacts: <exact paths or object identifiers>
- Required packet schema: <revision>
- Accepted inputs may be read but never edited.
- Exclusions: promotion, signature, approval, merge, deployment, release, and rollback

Permissions:
- Read admitted contracts, inputs, raw returns, command logs, test reports, diffs,
  review findings, and decision records.
- Write only a proposed manifest and copy list under <proposal path>.
- Run only <fixed digest, schema, link, and Git inspection commands>.
- No content repair, result rerun, accepted-store write, signing, or external transfer.

Inputs:
1. original task contract and input digests
2. workspace, model, tool, revision, and permission records
3. raw agent return, stdout, stderr, exit states, and tool history
4. changed-file list, diff, build and test reports
5. contradiction, unknown, failure, and adversarial-review records
6. human review records received so far
7. evidence-manifest schema and retention policy

Outputs:
- proposed manifest listing every artefact, revision, digest, producer, time, and location
- trace from task question to inputs, claims, changes, checks, findings, and decisions
- missing, mutable, duplicated, inconsistent, or inaccessible artefacts
- redaction and classification flags without modifying raw evidence
- packet status: structurally complete, structurally incomplete, or blocked
- required human reviews and promotion steps

Evidence expectations:
- Compute digests from actual retained files with the approved tool.
- Link reported commands to raw output and exit states.
- Link tests to subject, fixture, environment, and revision.
- Preserve rejected and failed artefacts with disposition.
- Distinguish requested model from runtime-reported model identity.
- Never replace raw evidence with a summary.

Stop conditions:
- Stop on a digest mismatch, missing raw output, mutable input, unknown producer,
  classification conflict, or inaccessible required artefact.
- Stop if packaging would copy restricted data into a less protected store.
- Return the blocked manifest. Do not fabricate or repair the missing record.

Human review:
- <evidence owner> checks provenance and retention.
- <technical and quality owners> verify command, diff, and test links.
- <security or compliance owner> handles restricted artefacts.
- Named authorities decide architecture, risk, acceptance, release, rollback, and promotion.

Rejection criteria:
Reject if a digest is copied rather than computed, raw failures disappear, missing fields
are filled from narrative, mutable links are accepted, restricted material crosses its
boundary, requested and actual model identity are confused, or the package claims that
structural completeness proves correctness or authorizes release.
```

A Verification Harness record should make rejection easy when a required link is absent. A polished PDF with no raw command record is presentation, not provenance.

## Bad prompt counterexamples

The following prompts are short because their failures are structural, not subtle.

### Broad rewrite

```text
Modernize this monolith into microservices, preserve all business logic, add tests,
and make it production ready.
```

This prompt delegates scope, architecture, rule interpretation, test oracles, production readiness, and acceptance at once. It contains no pinned inputs, write set, evidence return, stop condition, rollback constraint, or reviewer. The resulting diff cannot show which unknown behaviours were never discovered.

### Confident rule summary

```text
Read the fee code and document the definitive business rules. Resolve inconsistencies
and remove obsolete cases.
```

Source can reveal executable behaviour, not definitive business authority. "Resolve" invites unsupported synthesis. "Obsolete" requires consumer, runtime, and owner evidence. The prompt also destroys contradictions that reviewers need to see.

### Tests that make the build green

```text
Add comprehensive tests for the legacy component. Fix any failures and update snapshots.
```

"Comprehensive" has no boundary. Fixing failures combines observation with change. Updating snapshots lets candidate output define its own oracle. There is no fixture provenance, behaviour status, side-effect inventory, or human baseline approval.

### Unbounded dependency map

```text
Map every dependency and identify dead code we can delete.
```

The prompt collapses declared, resolved, packaged, configured, and observed edges. It gives no repository or runtime boundary. Dead-code deletion needs evidence from consumers, jobs, reflection, configuration, and operations that a static search cannot supply.

### Self-review

```text
Implement the migration, review your work, fix all issues, and approve it for merge.
```

One context produces the assumptions, implementation, tests, findings, and approval. Repair erases the raw review trail. Approval belongs to accountable people under repository policy, not to the implementation session.

### Security assurance from a diff

```text
Check that this change is secure and compliant. If tests pass, mark it ready to deploy.
```

A code diff and test run cannot establish the entire security or compliance claim. The prompt lacks threat scope, control requirements, environment evidence, specialist review, and release authority. A pass result has been assigned a meaning it cannot support.

### Difference suppression

```text
Compare old and new outputs. Ignore harmless formatting and timing differences and
update expected results until everything passes.
```

"Harmless" is an acceptance decision. Formatting can be contractual, and timing can affect ordering or a batch window. Updating expected results destroys the evidence needed to classify a difference. Raw observations and approved normalization must precede any equivalence claim.

### Evidence summary without provenance

```text
Summarize the work into an audit-ready evidence pack. Fill in any missing details from
context so the report is complete.
```

The instruction explicitly asks for fabrication. Audit evidence needs immutable inputs, raw outputs, actual identities, commands, exit states, digests, and named reviews. Missing detail should block the package, not invite completion by inference.

## Review catalogue

A reviewer can use the following sequence for any returned pattern. It is not a scoring model. One material failure can reject the task even when every other row looks good.

### Boundary review

- Does the returned repository revision equal the approved revision?
- Is every path, command, data class, and external system inside the admitted boundary?
- Did the changed-file list match an independent Git inspection?
- Did a read-only task leave the worktree unchanged?
- Were blocked actions retained rather than worked around?

### Claim review

- Can every material statement be traced to a revision-bound source?
- Are observation, documentation, inference, and human decision separated?
- Does confidence describe evidence strength rather than authority?
- Are contradictions, unknowns, excluded references, and failed searches visible?
- Would the wording still be accurate if read outside the agent's narrative?

### Test and oracle review

- Who or what supplied each expected result?
- Could the same mistaken interpretation have produced implementation and test?
- Are response, state, events, exceptions, timing classes, and prohibited effects covered where relevant?
- Were raw observations retained before normalization?
- Did a failing case cause investigation rather than a weaker assertion?
- What independent evidence would expose a shared mistake?

### Execution review

- Is each command paired with actual stdout, stderr, exit state, environment, and revision?
- Are unexecuted checks listed plainly?
- Do retained reports agree with the summary?
- Is actual model and tool identity recorded rather than copied from the request?
- Are generated files and dependency changes explained?

### Decision review

- Did Claude Code select architecture, business meaning, risk tolerance, normalization, release treatment, or rollback triggers?
- Are decisions linked to named people acting in defined roles?
- Does the reviewer have the expertise and reserved capacity for the claim?
- Are unresolved material findings blocking dependent work?
- Is proposal status distinct from accepted evidence, merged code, and released behaviour?

### Evidence-package review

- Does the manifest preserve raw returns, failures, rejected findings, diffs, and review records?
- Were digests computed from retained artefacts?
- Do links resolve without crossing a data-classification boundary?
- Can another authorised reviewer reconstruct the claim from the packet?
- Does structural completeness avoid claiming correctness?

## Preserve human authority

The templates repeatedly name human gates because consequential authority should not be hidden in prompt wording.

The architect decides whether a boundary, seam, dependency direction, or transitional structure is acceptable. Domain and product owners decide business meaning. Quality owners decide whether an oracle and evidence set support the stated claim. Security and risk owners decide control treatment and residual risk. Operations decides whether monitoring, recovery, and rollback procedures are workable. Release authority decides whether to proceed, pause, cut over, or roll back. Repository owners control merge under the organisation's review policy. An evidence owner controls promotion and retention.

Claude Code can prepare information for those decisions. It can also expose that a decision is missing. It does not gain authority because a prompt says "act as the architect," because all tests pass, or because its return matches a schema.

A practical final question applies to every pattern:

> If this return is wrong, which retained evidence, independent check, or accountable reviewer is expected to catch it?

If the contract cannot answer that question, narrow the task or strengthen the evidence before starting the session.
