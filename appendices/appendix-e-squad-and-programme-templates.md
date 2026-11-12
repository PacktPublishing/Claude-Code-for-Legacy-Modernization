# Appendix E: Squad and programme templates

## Local schema and vocabulary

The enterprise utilities and return formats in this appendix are illustrative prerequisites, not installed Python lab utilities. The supplied lab schema is `contracts/returns/task-return.schema.json` with required fields `claims`, `changed_files`, `commands`, `artifact_paths`, `unknowns`, and `stop_reason`. Use the [shared decision and alias table](../../companion/northstar-modernization-lab/docs/runbooks/decision-rights.md): `approved` maps to `accepted` only with human approval; `not-executed` maps to `not-run`; missing required evidence is `missing`, not success. Behaviour labels, evidence labels and dispositions are separate dimensions.

> **Practical handbook use:** Chapters 1 to 3, 7, 13, 19, and 24 to 26.
>

A modernisation programme needs enough structure to make ownership visible, but not so much structure that completing a form becomes a substitute for producing evidence. I use the templates in this appendix to answer practical questions: who can decide, what a squad may start, how much review it can absorb, when work must stop, and whether a faster implementation actually shortened the full path to an accepted slice.

These PDF examples are illustrative templates, not copy-ready files. PDF selection may alter newlines or indentation; use the matching distributed text source and validate the completed record before use. Replace every angle-bracketed field. Delete roles and rows that do not apply, but do not delete an authority merely because no one has been assigned to it. Record that condition as a gap and resolve it before the affected work begins. A person may hold several roles in a small squad. The record must still show which authority that person exercised.

All Northstar examples are illustrative. They are worked examples, not observed staffing levels, timings, capacities, costs, or programme results. Claude Code roles in these templates are bounded execution roles. They may search, draft, test, compare, and report within an approved task contract. They do not own outcomes, approve behaviour, accept risk, merge changes, transfer production authority, or declare retirement.

## Choose the smallest template that fits the decision

Use a pilot squad for one bounded slice when the main purpose is to prove the method, workspace, evidence flow, and review gates. Move to a standard delivery squad when the pilot carries sustained implementation and operational work. Use the programme template when two or more squads share interfaces, platform controls, specialists, release windows, or transitional architecture.

Do not scale from pilot to programme by adding ceremonies. Scale when dependencies and authority cross the boundary of one squad. Complete the role charters and decision-rights map first. Then use the sprint evidence contract, capacity plans, and handoff records during delivery. Use the full-flow baseline before claiming improvement.

## Template 1: Pilot squad charter

### When to use it

Use this charter to admit one reversible, bounded slice. Run a short admission workshop with the outcome charter, slice boundary, control profile, current build evidence, and known operational constraints available. The pilot should prove that the team can reproduce the baseline, return a cited discovery result, review it, and preserve a rejection before it accepts migration code.

### Copy-ready template

Exact text source (illustrative; not a run): [Appendix E, block 1](../../companion/northstar-modernization-lab/book-assets/editorial-source/appendix-e-squad-and-programme-templates-block-001.yaml).

```yaml
charter_id: <pilot-charter-id>
status: draft
slice:
  outcome: <measurable business or operational outcome>
  boundary: <included capability, repositories, interfaces, and data>
  non_goals: [<explicit exclusion>]
  stop_conditions: [<condition that stops admission or delivery>]
  base_revision: <approved revision or not-yet-captured>
core_people:
  product_owner: <person>
  modernization_lead: <person>
  legacy_specialist: <person>
  quality_engineer: <person>
reserved_specialists:
  platform: <person, hours per iteration, response expectation>
  operations: <person, gates, hours per iteration>
  security_or_risk: <person, gates, response expectation>
  domain: <person, question limit, review windows>
human_authorities:
  outcome: <person>
  current_behavior_interpretation: <person>
  test_oracle_acceptance: <person>
  workspace_control: <person>
  merge: <person>
  go_pause_rollback: <person>
first_gate_requires:
  - clean worktree and pinned revision
  - reproducible baseline with known failures
  - approved read-only task contract
  - named technical and domain reviewers
  - evidence ledger and failure record location
ai_boundary:
  allowed_roles: [<read-only discovery, evidence curation>]
  prohibited_authority: [behavior, architecture, security, merge, release, rollback]
escalation_path: <escalation-record-id>
review_date: <date>
owner: <modernization-lead>
```

### Illustrative Northstar example

Northstar's worked pilot covers the GBP month-end fee path, not the whole settlement monolith. The core group contains a product owner, a modernisation lead who also codes, a legacy specialist, and a quality engineer. Platform reserves four hours in the first iteration to reproduce the build. Operations reviews batch failure handling on Tuesday. The domain owner accepts no more than four high-consequence rule questions on Thursday. The first gate permits a read-only trace of the fee from calculation to export. It does not permit a replacement patch.

### Failure warning

A four-person pilot is not a staffing formula. If a database move, safety obligation, unknown consumer set, or irreversible side effect needs dedicated expertise, add it before work starts. "Available when needed" is not reserved capacity. A pilot with no named rollback authority or no reviewer for behaviour claims is not compact. It is incomplete.

## Template 2: Standard delivery squad charter

### When to use it

Use this charter when one slice has moved beyond method discovery into sustained test, implementation, integration, cutover preparation, and operational support. Separate responsibilities that the pilot combined, and set work limits from review capacity rather than developer count.

### Copy-ready template

Exact text source (illustrative; not a run): [Appendix E, block 2](../../companion/northstar-modernization-lab/book-assets/editorial-source/appendix-e-squad-and-programme-templates-block-002.yaml).

```yaml
charter_id: <delivery-squad-id>
outcome_id: <approved-outcome-id>
owned_scope:
  repositories: [<repository and paths>]
  interfaces: [<owned contracts>]
  runtime_authority: <current production owner>
  evidence_view: <ledger or evidence index>
people:
  product_owner: <person and allocation>
  modernization_lead: <person and allocation>
  engineers:
    - <person, legacy or target strengths, allocation>
  architect: <person, decision windows>
  quality_engineer: <person, review capacity>
  platform_engineer: <person, service expectation>
  operations_owner: <person, gates and on-call boundary>
  security_owner: <person, required gates>
  domain_owner: <person, review capacity>
working_limits:
  max_active_discovery_bundles: <number>
  max_active_write_tasks: <number>
  max_bundles_waiting_for_domain_review: <number>
  max_unmerged_worktrees: <number>
definition_of_accepted_slice: <evidence and authority state>
merge_policy: <required reviews, evidence links, and merge order>
cutover_and_support_boundary: <squad duties and external duties>
ai_roles:
  - role: <discovery, test, migration, adversarial review, evidence curation>
    tools: <bounded tool set>
    writes: <exact paths or none>
    human_reviewer: <person>
    cannot_decide: <listed decisions>
dependencies: [<programme dependency ids>]
```

### Illustrative Northstar example

The worked fee delivery squad has a product owner, modernisation lead, two engineers with complementary Java and target-runtime skills, a quality engineer, and a platform engineer. The architect attends two scheduled decision windows each week. Operations and the domain owner have reserved review slots. The squad allows two active write tasks because it can complete two technical reviews in the iteration. A third engineer does not raise that limit until review capacity changes.

### Failure warning

Do not count agent sessions or pull requests as delivery capacity. If four engineers can return four bundles a day but quality can inspect one, the useful rate is at most one quality-bearing bundle a day. Starting the other three creates aging context, rework, and pressure to merge around the gate.

## Template 3: Multi-squad programme charter

### When to use it

Use this charter when squads can affect one another through shared contracts, data, platform controls, specialist queues, release windows, or retirement obligations. Keep each squad's local outcome and ledger view bounded. Put only cross-squad decisions in the programme layer.

### Copy-ready template

Exact text source (illustrative; not a run): [Appendix E, block 3](../../companion/northstar-modernization-lab/book-assets/editorial-source/appendix-e-squad-and-programme-templates-block-003.yaml).

```yaml
programme_id: <programme-id>
sponsor: <accountable-human>
programme_outcomes: [<outcome-id>]
squads:
  - id: <squad-id>
    outcome: <bounded outcome>
    repositories_and_paths: [<owned areas>]
    interfaces: [<owned interfaces>]
    release_authority: <person or forum>
shared_ownership:
  architecture_register: <owner and location>
  interface_register: <owner and location>
  evidence_schema: <owner and version>
  platform_profile: <owner and version>
  dependency_board: <owner and location>
  transitional_components: <owner and register>
programme_gates:
  cross_squad_design: <entry and approver>
  shared_contract_change: <consumer evidence and approver>
  merge_order: <decision owner>
  cutover_window: <decision owner>
  retirement: <decision owner>
coordination_cadence:
  dependency_review: <frequency and decision purpose>
  specialist_allocation: <frequency>
  evidence_health: <frequency>
  release_readiness: <frequency>
shared_work_limits:
  architecture_decisions_in_review: <number>
  interface_changes_in_flight: <number>
  specialist_queue_limits: <limits by role>
ai_boundary:
  permitted_programme_use: <schema checks, dependency extraction, gap reports>
  prohibited_programme_use: <priority, risk acceptance, release, staffing decisions>
```

### Illustrative Northstar example

Northstar's worked programme has fee calculation, accounting integration, and batch operations squads. The fee squad owns candidate calculation paths. The integration squad owns the posting contract. The operations squad owns scheduler and repair procedures. A shared forum owns contract versions, platform controls, evidence schema, and merge order. The fee squad cannot change the posting representation until the integration owner supplies consumer evidence and the programme architect accepts the transition sequence.

### Failure warning

A weekly status meeting is not programme coordination. Require versioned decisions, owners, dates, and affected squads. Git can reveal overlapping text, but it cannot detect two squads giving different meanings to fields changed in different files. Stop parallel work when semantic ownership overlaps.

## Template 4: Role charter

### When to use it

Complete one charter for every human role that holds authority or supplies scarce review. Use it when a title hides the actual decision. If one person holds several roles, create separate charters or clearly separated authority sections.

{pagebreak}

### Copy-ready template

Exact text source (illustrative; not a run): [Appendix E, block 4](../../companion/northstar-modernization-lab/book-assets/editorial-source/appendix-e-squad-and-programme-templates-block-004.yaml).

```yaml
role_charter_id: <id>
role: <role-name>
assigned_to: <person>
purpose: <why this role exists for the slice>
accountable_for:
  - <decision or outcome>
responsible_for:
  - <work product or review>
required_inputs:
  - <evidence needed before deciding>
outputs:
  - <signed decision, reviewed artefact, or executed action>
not_authorized_to:
  - <important adjacent authority>
availability:
  reserved_time: <hours or windows>
  response_expectation: <service expectation>
delegate_rules: <what may be delegated and how it is recorded>
conflicts_of_interest: <segregation rule or none>
escalates_when: [<trigger>]
backup: <named person or no backup>
```

### Illustrative Northstar example

The worked quality engineer is accountable for oracle strategy and evidence validity. They review generated tests, comparator independence, failed checks, and coverage of high-consequence rules. They are not authorised to accept an unexplained financial difference, approve target architecture, or release the candidate. They reserve eight review hours per iteration and escalate when the queue exceeds two substantive bundles.

### Failure warning

Avoid verbs such as "supports," "helps," or "oversees" unless the output is named. A role charter must identify a decision, artefact, or action. Claude Code may perform a bounded task associated with a role, but it cannot be assigned a human role charter or made the accountable owner.

## Template 5: Responsibility map

### When to use it

Use this RACI map during squad admission and whenever scope changes. `A` means one accountable human. `R` means people who perform the work. `C` means consulted before the decision. `I` means informed after it. Use `AI-contributes` separately so tool activity is not mistaken for accountability.

### Copy-ready template

Exact text source (illustrative; not a run): [Appendix E, block 5](../../companion/northstar-modernization-lab/book-assets/editorial-source/appendix-e-squad-and-programme-templates-block-005.yaml).

```yaml
responsibility_map:
  - activity: select or change outcome
    accountable: <one human>
    responsible: [<people>]
    consulted: [<people>]
    informed: [<people>]
    ai_contributes: impact trace only
    required_evidence: <outcome evidence>
  - activity: interpret current behaviour
    accountable: <one human>
    responsible: [<people>]
    consulted: [<people>]
    informed: [<people>]
    ai_contributes: candidate rules and citations
    required_evidence: <sources and contradictions>
  - activity: accept test oracle
    accountable: <one human>
    responsible: [<people>]
    consulted: [<people>]
    informed: [<people>]
    ai_contributes: draft or execute tests
    required_evidence: <independence and failure cases>
  - activity: accept architecture
    accountable: <one human>
    responsible: [<people>]
    consulted: [<people>]
    informed: [<people>]
    ai_contributes: option comparison
    required_evidence: <constraints and removal plan>
  - activity: change workspace control
    accountable: <one human>
    responsible: [<people>]
    consulted: [<people>]
    informed: [<people>]
    ai_contributes: configuration proposal
    required_evidence: <control tests>
  - activity: merge
    accountable: <one human>
    responsible: [<people>]
    consulted: [<people>]
    informed: [<people>]
    ai_contributes: diff and gap report
    required_evidence: <reviews and checks>
  - activity: go, pause, or rollback
    accountable: <one human>
    responsible: [<people>]
    consulted: [<people>]
    informed: [<people>]
    ai_contributes: assemble evidence only
    required_evidence: <frozen pack and observations>
  - activity: retire legacy path
    accountable: <one human>
    responsible: [<people>]
    consulted: [<people>]
    informed: [<people>]
    ai_contributes: inventory proposal only
    required_evidence: <consumer proof and disposition>
```

### Illustrative Northstar example

For an unexplained fee difference, the product owner is accountable for intended behaviour, the domain owner and quality engineer are responsible for classification evidence, finance and the consumer owner are consulted, and operations is informed. Claude Code may group difference records and locate cited rules. It cannot mark the difference acceptable.

### Failure warning

More than one `A` usually means no one can close the decision. No `A` means the work is not admitted. Do not hide segregation conflicts by putting one person in every column. Record the conflict and add an independent gate where policy or consequence requires it.

## Template 6: Decision-rights map

### When to use it

Use this map for consequential decisions, especially where signal ownership, recommendation, decision, execution, and verification belong to different people. It is more precise than RACI for rollback and production authority.

### Copy-ready template

Exact text source (illustrative; not a run): [Appendix E, block 6](../../companion/northstar-modernization-lab/book-assets/editorial-source/appendix-e-squad-and-programme-templates-block-006.yaml).

```yaml
decision_rights:
  - decision_or_event: <event>
    signal_owner: <human or monitored system>
    recommends: <human>
    decides: <one human authority>
    executes: <human operator>
    verifies: <independent human role>
    deadline: <time>
    default_if_unresolved: <pause, reject, or safe state>
```

Record these minimum decisions: scope change, behaviour interpretation, oracle acceptance, architecture, data admission, control exception, merge, cutover, pause, rollback, difference acceptance, and retirement.

### Illustrative Northstar example

For missing comparison telemetry, operations owns the signal, the service owner recommends, the release authority decides, platform restores the observation path, and operations verifies completeness. The decision deadline is the approved pause limit. If unresolved, candidate promotion stops and the runbook returns to the named safe authority state.

### Failure warning

The person who detects a breach does not automatically own risk acceptance. Automation may execute a pre-authorised stop for an exact tested trigger. It cannot waive a threshold, accept a business difference, or declare reconciliation complete. Never leave the default state blank.

## Template 7: Sprint evidence contract

### When to use it

Complete this contract before iteration planning. It converts a backlog of activities into a dependency-ordered set of evidence bundles. Start only work whose inputs are accepted and whose reviewer has capacity.

### Copy-ready template

Exact text source (illustrative; not a run): [Appendix E, block 7](../../companion/northstar-modernization-lab/book-assets/editorial-source/appendix-e-squad-and-programme-templates-block-007.yaml).

```yaml
sprint_id: <id>
iteration_window: <start and end>
accepted_slice_definition: <state required>
entry_evidence:
  - <approved outcome, boundary, contract, or baseline revision>
tasks:
  - task_id: <id>
    question_or_decision_supported: <narrow purpose>
    depends_on: [<accepted task or evidence ids>]
    mode: <read-only or write-capable>
    base_revision: <revision>
    read_set: [<paths>]
    write_set: [<paths or none>]
    allowed_commands: [<fixed commands>]
    return_requires:
      - claims with revision-bound sources
      - commands and observed exit states
      - changed files and diff identity
      - contradictions, failures, and unknowns
      - human decisions required
    technical_reviewer: <person and reserved slot>
    domain_or_quality_reviewer: <person and reserved slot>
    merge_order: <position or not-applicable>
    stop_conditions: [<boundary or evidence failure>]
    ai_role: <bounded role or none>
iteration_work_limits: <limits tied to review plan>
rejected_work_treatment: <preserve, classify, and allocation rule>
```

### Illustrative Northstar example

The worked sprint starts fee discovery and synthetic fixture preparation in parallel because they read separate accepted inputs. The characterisation task waits for reviewed discovery claims. The migration task waits for accepted behaviour and oracle evidence. An adversarial review receives the candidate diff in a separate context after implementation. Each write task has its own worktree. Rejected bundles remain in the evidence record and count in effort.

### Failure warning

Do not pass an agent's unreviewed conclusion directly into another agent as fact. That creates a fast chain of correlated assumptions. A task ending on Friday without a booked reviewer is not complete enough to start. It is inventory waiting in a queue.

## Template 8: Review-capacity plan

### When to use it

Create this plan before committing sprint work. Estimate capacity in substantive bundles, not comments or hours alone. Use recent observations where available. Keep technical, domain, quality, security, architecture, and operations reviews separate because they are not interchangeable.

{pagebreak}

### Copy-ready template

Exact text source (illustrative; not a run): [Appendix E, block 8](../../companion/northstar-modernization-lab/book-assets/editorial-source/appendix-e-squad-and-programme-templates-block-008.yaml).

```yaml
review_capacity:
  - bundle_type: discovery claims
    expected_count: <n>
    review_effort: <hours or range>
    named_reviewers: [<people>]
    reserved_capacity: <hours or bundles>
    queue_limit: <n>
    maximum_age: <time>
    response_when_exceeded: <stop or reduce starts>
  - bundle_type: generated tests
    expected_count: <n>
    review_effort: <hours or range>
    named_reviewers: [<people>]
    reserved_capacity: <capacity>
    queue_limit: <n>
    maximum_age: <time>
    response_when_exceeded: <action>
  - bundle_type: implementation diff
    expected_count: <n>
    review_effort: <hours or range>
    named_reviewers: [<people>]
    reserved_capacity: <capacity>
    queue_limit: <n>
    maximum_age: <time>
    response_when_exceeded: <action>
  - bundle_type: behaviour differences
    expected_count: <n>
    review_effort: <hours or range>
    named_reviewers: [<people>]
    reserved_capacity: <capacity>
    queue_limit: <n>
    maximum_age: <time>
    response_when_exceeded: <action>
  - bundle_type: architecture decision
    expected_count: <n>
    review_effort: <hours or range>
    named_reviewers: [<people>]
    reserved_capacity: <capacity>
    queue_limit: <n>
    maximum_age: <time>
    response_when_exceeded: <action>
  - bundle_type: operational change
    expected_count: <n>
    review_effort: <hours or range>
    named_reviewers: [<people>]
    reserved_capacity: <capacity>
    queue_limit: <n>
    maximum_age: <time>
    response_when_exceeded: <action>
```

Add: planning assumptions, absence dates, interruption allowance, re-review allowance, and the owner who can lower work in progress.

### Illustrative Northstar example

Northstar's worked quality engineer can finish two generated-test bundles in the iteration after allowing for one re-review. The domain owner can settle four high-consequence rule questions during one reserved session. The sprint therefore admits two test bundles and no more than four open rule decisions. Extra agent availability does not change either limit.

### Failure warning

A reviewer calendar full of meetings is not review capacity. Reserve time against named bundles and include rework. When the queue limit is breached, stop starting review-bearing work. Asking the reviewer to "catch up" while generation continues is not a capacity response.

## Template 9: Scarce-specialist allocation

### When to use it

Use this plan for legacy experts, domain owners, architects, security reviewers, database specialists, and operations staff whose absence can stop several squads. Allocate their time to decisions, not broad attendance.

{pagebreak}

### Copy-ready template

Exact text source (illustrative; not a run): [Appendix E, block 9](../../companion/northstar-modernization-lab/book-assets/editorial-source/appendix-e-squad-and-programme-templates-block-009.yaml).

```yaml
specialist_allocation:
  - specialist: <person or role>
    authority_or_knowledge: <scope>
    decision_questions: [<bounded questions>]
    evidence_prepared: [<links and examples>]
    reserved_windows: [<times>]
    maximum_questions: <n>
    backup_or_transfer_plan: <plan>
    queue_owner: <person>
```

For each question record: consequence if delayed, deadline, requesting squad, evidence bundle, decision owner, disposition, and knowledge-transfer artefact.

### Illustrative Northstar example

The worked calendar specialist receives four questions, each with source citations, observed outputs, contradictions, and one proposed verification action. They do not receive six transcripts and a request to "review the fee logic." Their decisions update the rule register and characterisation cases so later slices do not need the same explanation.

### Failure warning

Reducing specialist hours is not automatically an improvement. Hours can fall because the team skipped review. Pair demand with queue delay, unresolved rule confidence, defects, and evidence transferred into maintained tests or records. Do not use Claude Code to impersonate an unavailable specialist.

## Template 10: Handoff record

### When to use it

Use a handoff when work changes squad, role, repository, authority state, or operational owner. The receiving party accepts a defined package, not an oral summary.

{pagebreak}

### Copy-ready template

Exact text source (illustrative; not a run): [Appendix E, block 10](../../companion/northstar-modernization-lab/book-assets/editorial-source/appendix-e-squad-and-programme-templates-block-010.yaml).

```yaml
handoff_id: <id>
from: <person or squad>
to: <person or squad>
subject: <slice, interface, operation, or evidence bundle>
subject_revision: <revision or digest>
current_authority_state: <legacy, candidate cohort, candidate, paused, or other>
accepted_inputs: [<evidence and decision revisions>]
open_items:
  - id: <gap or risk id>
    consequence: <effect>
    owner: <person>
    deadline: <date or gate>
required_actions: [<receiving actions>]
prohibited_assumptions: [<what must not be inferred>]
operational_details:
  alerts: <links>
  runbooks: <links>
  schedules_and_windows: <details>
  rollback_or_recovery: <state and owner>
acceptance_check: <build, test, rehearsal, or walkthrough>
receiver_disposition: <accepted, rejected, or accepted-with-named-limits>
receiver: <human name>
date: <date>
```

### Illustrative Northstar example

The worked fee squad hands the candidate repair queue to operations only after a walkthrough using synthetic failed cases. The record links the runbook, alerts, queue identity, known unsupported repair, current rollback state, and escalation route. Operations rejects the first handoff because the runbook explains replay but not duplicate-posting containment.

### Failure warning

A link collection is not a handoff. The receiver must perform an acceptance check and record a disposition. Claude Code may check references and missing fields. It cannot accept operational ownership or certify that a receiving team can recover the service.

## Template 11: Escalation record

### When to use it

Use escalation for unresolved authority, material evidence conflict, boundary breach, capacity failure, shared-interface collision, or loss of a safe operational state. Define triggers before the crisis.

### Copy-ready template

Exact text source (illustrative; not a run): [Appendix E, block 11](../../companion/northstar-modernization-lab/book-assets/editorial-source/appendix-e-squad-and-programme-templates-block-011.yaml).

```yaml
escalation_id: <id>
trigger: <observable condition>
raised_by: <person or automated signal>
time_raised: <time>
affected_scope: <slice, squads, systems, and authority>
current_safe_state: <who owns new work and what is stopped>
evidence: [<retained records>]
material_unknowns: [<unknowns>]
automatic_containment: <pre-authorized action or none>
decision_required: <specific decision>
decision_owner: <one accountable human>
consulted_roles: [<roles>]
deadline: <time>
default_at_deadline: <pause, reject, rollback, or other safe state>
communications_owner: <person>
resolution: <decision and rationale>
follow_up: [<repair, review, or policy change>]
```

### Illustrative Northstar example

A worked fee and integration squad both plan changes to the posting identity. The conflict triggers a programme escalation before either write task begins. Candidate work pauses at the accepted base revision. The interface owner decides the transition version after consumer evidence arrives. The programme architect sets merge order. Claude Code may compare proposed schemas, but it cannot choose the authoritative contract.

### Failure warning

Escalation must preserve a safe current state. "Discuss tomorrow" is not a disposition when two writers or an expiring cutover window are possible. Do not let the person with the loudest channel become the decision owner. Do not ask an agent to break an organisational tie.

## Template 12: Programme coordination board

### When to use it

Use this board in the cross-squad dependency review. Review exceptions and decisions, not every local task. A row remains open until the dependency has an accepted disposition and downstream squads acknowledge it.

{pagebreak}

### Copy-ready template

Exact text source (illustrative; not a run): [Appendix E, block 12](../../companion/northstar-modernization-lab/book-assets/editorial-source/appendix-e-squad-and-programme-templates-block-012.yaml).

```yaml
programme_dependencies:
  - dependency_id: <id>
    provider_squad: <squad>
    consumer_squads: [<squads>]
    shared_subject: <interface, data, control, or window>
    current_revision: <revision>
    proposed_change: <change>
    evidence_needed: <evidence>
    decision_owner: <human>
    needed_by: <date>
    merge_or_release_order: <order>
    state: <open, blocked, accepted, or retired>
```

Track alongside the board:

- shared architecture decisions and affected squads
- platform and permission-profile versions
- evidence-schema versions and migrations
- scarce-specialist queues
- active transitional components, owners, cost, and removal conditions
- shared environment and cutover-window capacity
- cross-squad risks, escalations, and late changes

### Illustrative Northstar example

The worked board shows that the posting-contract expansion must merge before the candidate fee writer. The reconciliation fixture update can proceed in parallel because it reads the accepted expansion and writes a separate path. Schema contraction remains blocked until every approved consumer has migrated and the rollback obligation has expired.

### Failure warning

Do not make every local decision a programme decision. That slows squads and hides the few collisions that matter. Conversely, do not leave shared temporary components on a local backlog. A gateway, adapter, comparison store, or duplicate on-call path needs one programme-visible owner and removal condition.

## Template 13: Full-flow time and resource baseline

### When to use it

Create the baseline before changing the delivery method or introducing more agent work. The unit is an accepted slice, not a prompt, task, branch, pull request, or deployment. Record active effort and waiting separately. Preserve missing values as `not_observed`.

### Copy-ready template

Exact text source (illustrative; not a run): [Appendix E, block 13](../../companion/northstar-modernization-lab/book-assets/editorial-source/appendix-e-squad-and-programme-templates-block-013.yaml).

```yaml
measurement_id: <id>
unit: accepted_slice
decision_supported: <repeat, change, or stop the method>
decision_owner: <human>
scope:
  outcome_revision: <revision>
  slice_boundary: <description>
  dependency_radius: <description>
  criticality: <classification>
  rule_uncertainty: <classification and basis>
  test_deficit: <classification and basis>
  cutover_type: <type>
comparison_method: <recent comparable, within-slice, matched cohort, or none>
window:
  start: <observed time>
  acceptance: <observed time or not_observed>
segments:
  - name: outcome_and_scope
    active_human_hours_by_role: <values or not_observed>
    elapsed_time: <value or not_observed>
    waiting_time_and_queue: <value, reason, or not_observed>
  - name: discovery
    active_human_hours_by_role: <values>
    agent_activity: <sessions and cost, not human effort>
    elapsed_time: <value>
    waiting_time_and_queue: <value and reason>
  - name: oracle_creation
    active_human_hours_by_role: <values>
    elapsed_time: <value>
    waiting_time_and_queue: <value and reason>
  - name: implementation
    active_human_hours_by_role: <values>
    agent_activity: <values>
    elapsed_time: <value>
    waiting_time_and_queue: <value and reason>
  - name: review_and_rework
    active_human_hours_by_role: <values>
    elapsed_time: <value>
    waiting_time_and_queue: <value and reason>
  - name: cutover_observation_and_reconciliation
    active_human_hours_by_role: <values>
    elapsed_time: <value>
    waiting_time_and_queue: <value and reason>
costs:
  human_loaded_cost: <observed, allocated, estimated, or missing>
  billed_model_and_tool_cost: <value or missing>
  estimated_session_cost: <separate value or missing>
  build_test_replay_and_parallel_infrastructure: <value or missing>
  external_assurance: <value or missing>
  cutover_and_observation_staffing: <value or missing>
  incident_and_rework: <value or missing>
  shared_enablement_allocation: <rule and value>
quality_and_completion:
  rejected_or_abandoned_work: <count, effort, and allocation>
  unresolved_differences: <count and materiality>
  escaped_defects_and_incidents: <records>
  observation_coverage: <record>
  legacy_specialist_hours_and_queue: <record>
  domain_specialist_hours_and_queue: <record>
  transitional_components_remaining: <count and continuing cost>
  retirement_state: <state>
data_quality:
  observed_fields: [<fields>]
  estimated_fields: [<fields and method>]
  allocated_fields: [<fields and rule>]
  missing_fields: [<fields>]
confounders: [<scope, staffing, freeze, platform, or learning differences>]
interpretation: <human decision after balanced review>
```

### Illustrative Northstar example

Northstar's worked baseline begins when the fee outcome is authorised and ends when the heightened observation window closes. It includes discovery, characterisation, implementation, technical and domain review, rework, cutover staffing, and reconciliation. Model activity is attributed to task identifiers, while billed cost remains separate from session estimates. The baseline records the calendar specialist's hours and queue delay. It also records the continuing cost of the comparison store and duplicate on-call path until retirement.

Suppose the illustrative implementation segment becomes shorter while domain-review waiting becomes longer. The record does not claim a productivity gain. It states that work moved from implementation to a constrained review queue. Suppose total elapsed time falls but unresolved reconciliation cases rise. The balanced review treats the result as incomplete rather than averaging speed and safety into one favorable score.

### Failure warning

Do not reconstruct missing history with plausible numbers. Do not exclude rejected work, weekend operations, shared platform effort, or a second cutover window. Do not compare unlike slices without recording scope and learning effects. Tokens, generated lines, and session count are activity measures. They never replace accepted-slice time, full cost, quality, specialist demand, and retirement state.

## Operating the templates as one system

The templates should agree. The squad charter names roles that have role charters. The responsibility map assigns one accountable human to each consequential decision. The decision-rights map defines the safe default when a deadline expires. The sprint evidence contract admits no more work than the review and specialist plans can absorb. Handoffs preserve revision and authority state. Escalations feed the programme board. The full-flow baseline includes the queues and rejected work exposed by all of them.

Version these records beside the relevant change and evidence index, or store them in an approved system with immutable revisions. A changed owner, threshold, work limit, interface, or authority state creates a new revision. Do not silently edit the record that governed earlier work.

Claude Code can validate required fields, compare identifiers, locate missing links, prepare queue summaries, and flag rows with no owner. Keep accepted decisions read-only to agent tasks. A schema-valid record can still contain an unsupported claim, copied model identity, invented capacity, or false approval. A named human reviews the underlying evidence and signs the disposition.

## Final checks before use

Before admitting work, confirm that:

- every outcome, behaviour, oracle, architecture, control, merge, release, rollback, and retirement decision has one accountable human
- every specialist commitment has reserved time, a bounded question set, and an escalation path
- every active evidence bundle has accepted inputs, an isolated write set where needed, and a booked reviewer
- review and specialist queue limits can stop new starts
- every handoff names the subject revision, current authority, open limits, and receiver disposition
- every escalation has a decision deadline and safe default
- cross-squad interface and merge order are recorded before parallel writes begin
- the baseline covers full-flow elapsed time, human effort, waiting, rework, costs, quality, specialist demand, continuing transitional cost, and retirement
- agent roles have explicit tools, paths, returns, stop conditions, and prohibited decisions
- no agent output is treated as approval, risk acceptance, release authority, or proof of absence

The paperwork is useful only when it changes what the programme starts, stops, reviews, or accepts. If a template cannot block work with missing authority or missing evidence, it is merely a formatted status report.
