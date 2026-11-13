# Decision rights and vocabulary

This is the common local contract for Chapters 13, 16, 19, 20, 22 to 24 and 26.
Each decision record names the actual person, scope, evidence and delegation;
a role label is not an approval. Examples are unsigned.

| Decision | Accountable authority | Executes / consults |
|---|---|---|
| meaning, fee rule, accepted behavioural difference | business/domain owner | engineer proposes; data owner consulted on representation |
| schema representation, lineage, retention | data owner | domain owner agrees business meaning |
| merge into repository | repository maintainer | integration owner assembles evidence; release authority does not merge by implication |
| planned go/no-go, cohort, cutover or rollback | release authority (also called cutover authority) | operations executes; reconciliation owner verifies effects |
| emergency stop or restoration | incident commander under recorded release delegation | operations executes; reconciliation owner checks partial effects |
| reconciliation closure / replay scope | reconciliation owner | domain and data owners accept any financial correction |
| retirement scope and retention | accountable system owner | data/records owners accept retention; repository maintainer authorizes exact protection changes |
| execution of approved retirement | release authority | operations/maintainer execute only approved scope |

A runbook saying operations "owns rollback" means execution, not independent
permission. An integration owner cannot authorize merge. No green test grants
release, reconciliation, business-rule or deletion authority. If delegated
emergency authority is absent, stop and seek it rather than inferring it.

## Behaviour and evidence are separate dimensions

Use behaviour statuses `observed`, `documented`, `hypothesis`, `disputed`,
`accepted`, `tolerated`, `unknown`. Map old labels: `approved` → `accepted`
(with a named decision); `expected`/`intended` → `documented` until accepted;
`characterised`/`characterized` → `observed`; `unclassified` → `unknown`;
`contradicted` → `disputed`; `legacy defect` → `disputed` pending decision.
A schema with an enum must admit these statuses or declare an explicit translation;
never translate disputed to accepted. Acceptance is human, not test success.
Use the six evidence labels separately: Observed, Documented, Vendor-reported,
Practitioner guidance, Illustrative, Hypothesis.

For missingness use `not-run` when execution was not attempted; `not-observed`
when an attempted observation found no event; `missing` for required absent
evidence; `not-applicable` with a reason for an absent lab capability.
`not-executed` is an alias of `not-run`, never a pass.

Disposition vocabulary is `preserve`, `correct`, `retire`, `defer`, `investigate`.
Preserve/correct refer to BUSINESS BEHAVIOUR. Fixing replacement code to preserve
legacy HALF_UP is `preserve legacy rule / correct replacement implementation`.
`remove` aliases `retire`; a code fix does not itself authorize a corrected rule.

## Routing and reconciliation mappings

Use five routing authority states: `legacy_only`, `candidate_observe`,
`candidate_cohort`, `candidate_slice`, `legacy_slice_retired`.
Inventory/baseline stays `legacy_only`; observe/shadow/compare are activities in
`candidate_observe`; canary and bounded expansion use `candidate_cohort`; full
bounded-slice cutover uses `candidate_slice`; retirement reaches
`legacy_slice_retired`. Restore returns to a previously approved state, never a
sixth state. The three-box routing figure groups legacy, mixed/observed and
candidate authority; it does not replace the five-state model. The local retirement
state retires the selector route, not the protected evidence implementation.

The reconciliation ledger uses seven classes: `matched`, `missing-old`,
`missing-new`, `changed`, `duplicate`, `out-of-order`, `pending`.
`old-only` → `missing-new`; `new-only` → `missing-old`; `equal` → `matched`;
`value/state/error/effect mismatch` → `changed` with a dimension;
`repeated key` → `duplicate`; `sequence mismatch` → `out-of-order`;
`awaiting completion` → `pending`. An invalid observation is not a behavioural
class: retain it as an invalid run and stop comparison. Exception types and
workflow states remain dimensions on a class, not competing taxonomies.
