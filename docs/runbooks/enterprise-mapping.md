# Python lab and enterprise examples

The Python lab is not an abbreviated Java service deployment. Enterprise examples
name capabilities to investigate; their paths do not exist here unless listed.
A reader-created file must be admitted by the current contract before writing it.
A supplied wrapper does not make a missing prompt or schema runnable.

| Enterprise term or path | Python lab observation point | Limit to record |
|---|---|---|
| `src/fees/`, `FeeCalculator.java` | `legacy_app/settlement.py`, `settle` | GBP only; no service boundary |
| `batch/`, scheduler | `legacy_app.run_batch`, `scripts/baseline.py`, Makefile | manual invocation; scheduler absent |
| request/message schema | `fixtures/synthetic/settlements.csv` columns | no broker or schema registry |
| fee result/decision ID | returned settlement dictionary and CSV headers | no decision_id field; keep CSV shape unchanged |
| reference calendar | `HOLIDAYS` in both settlement modules | three explicit dates, not a complete UK calendar |
| ledger posting | gross, fee, net in output CSV | no durable ledger or external posting |
| retry/idempotency store | `process` local seen-ID set | duplicate suppression within one batch only |
| trace, runtime logs | capture stdout/stderr, argv, revision, hashes, CSV | no tracing daemon; no span claim |
| `deploy/`, `ops/production/` | local selector exercise and runbook | no production routing or deployment |
| `testdata/` | `fixtures/synthetic/` | approved synthetic data only |
| path/evidence gate | `.claude/hooks/protect_files.py`, settings, verify helpers | no general path-gate/evidence-hook files |

For Chapters 5 to 7 read `scripts/`, Makefile, tests and both package entry points.
`docs/architecture/` is a reader-created output, not a supplied source. Record
absent broker, scheduler, retry store and tracing fields as `not-applicable` with
reason; do not fabricate logs. Trace the 0.35 minimum fee, 0.15% fee, HALF_UP,
three-date HOLIDAYS set, and duplicate `STL-1002` row with amount 999.00. Preserve
the dropped second-row observation and the original order. The local capture
shows commands and outputs, not unobserved internal runtime calls.

## One local output set per chapter

Chapter 1 uses `evidence/decisions/01-slice-charter.md` and
`evidence/slice-candidates.csv`; Chapter 4 reads that same charter. Other charter
paths in an enterprise layout are not additional lab writes.

Chapter 5 returns two artifacts only, saved by the human after plan-mode review:
`docs/architecture/05-code-runtime-map.md` and
`evidence/claims/05-path-claims.json`. The JSON is one array of claims with ID,
statement, source path/line or run, evidence label, confidence and unknowns.
The map contains static and runtime sections; it is not two independent discovery
packs. Enterprise `evidence/discovery/` and JSONL layouts are alternatives, not
extra deliverables.

Chapter 6 saves `evidence/data-flows/06-fee-flow-trace.yaml`,
`docs/architecture/06-data-side-effect-trace.md` and
`evidence/claims/06-flow-claims.json`. The YAML contains source revision, input key,
ordered hops, cardinality, field transformations, output key, side effects,
evidence references and unknowns. Chapter 7 saves
`evidence/rules/07-fee-rules.yaml`, `evidence/claims/07-rule-ledger.json`,
`docs/runbooks/07-operational-knowledge.md` and
`evidence/decisions/07-rule-review.md`. YAML rules include trigger, condition,
outcome, source, counter-evidence, confidence, owner and next action. Only the
named human may save these plan-mode outputs after review. Nested enterprise
folders shown in body examples are not extra local permissions.

Chapter 15 reads `replacement_service/`, `tests/`, `Makefile`, `fixtures/synthetic/`,
`docs/decisions/14-fee-seam.md`, `contracts/acceptance/13-fee-acceptance.json`,
`docs/runbooks/13-fee-rollback.md` and retained `evidence/`. Its canonical decision
`docs/decisions/15-strangler-route.md` is an admitted human-reviewed write along
with design, stage runbook, routing contract and review. It deploys nothing.

## Example labels

**Supplied runnable** means a file exists at this companion revision; it does not
mean inputs exist, the command succeeds, or the output constitutes approval.
**Reader-created prerequisite** identifies a prompt, schema, fixture or evidence
file the reader must create and review under its contract first.
**Enterprise-only** identifies a larger-system example with Java/Gradle, brokers,
production adapters or a different contract schema. Translate its question using
the table; do not copy its paths or commands into the lab.

Structured commands with `prompts/CONTRACT-*.txt`, `contracts/*/*-return.schema.json`
and enterprise output folders are NOT ready-to-run lab commands. The lab ships
`prompts/rounding-analysis.txt` and `contracts/returns/task-return.schema.json`.
That schema requires claims, changed_files, commands, artifact_paths, unknowns,
and stop_reason. A worked Appendix B enterprise return is not a valid lab return
until explicitly adapted and validated. Appendix B helpers are printed in the book and author working asset
`practical-edition/working-assets/task-contracts.md`; they are not installed
`tools/contracts/` utilities. The companion exporter includes chapter JSON, YAML
and SQL listings, not those appendix Python helpers. Their rejection table is a
worked test specification, not a claim of a run in this lab.
Do not grant extra permission to make an illustrative command run.
