# Local reader route and evidence retention

## Local Stage 2 executable check

After signed scope approval, replace the reader-created replacement_service/batch_entrypoint.py with exercises/retired_batch_entrypoint.py. This removes its legacy route and selector parameter; it does not delete the protected reference oracle. Install exercises/retirement_checks.py as tests/test_retired_route.py. Run python3 -m unittest discover -s tests -p test_retired_route.py -v, then the accepted full suite and scripts/verify.py. No protection changes are needed. Retain historical baseline/compare checks as evidence only. The removal contract names these two writes, executor, approver, before/after revision and digests, rollback expiry and retained-reference owner. Never move a published tag.

These instructions apply to the companion revision containing this file. Published
`lab/*` tags are immutable teaching checkpoints; do not move a tag to install a
repair. Start from the stated tag on a new reader branch, then apply the reviewed
companion update before using helpers not present at that tag. Record both commit
IDs. Java, jqwik, PIT, database, broker and production selectors are not installed
by this Python lab. The chapter contract controls any additional writes.

## Commands and runners

The human runs baseline and Chapter 9 corpus capture, including all commands below.
The assistant proposes commands and interprets sealed captures; it does not run
capture, characterize, compare or replay in the Chapter 9 candidate-preparation task. `make baseline` is therefore not pre-approved
in the shared assistant allowlist. `scripts/capture.py` is a small local recorder,
not a production harness. Run from the companion root without a shell pipeline:

```sh
python3 scripts/capture.py baseline-01 -- python3 scripts/baseline.py
python3 scripts/capture.py compare-01 -- python3 scripts/compare.py
python3 scripts/capture.py corpus-a-01 -- python3 scripts/replay.py fixtures/synthetic/settlements.csv evidence/runs/corpus-a-output-01
python3 scripts/capture.py corpus-b-01 -- python3 scripts/replay.py fixtures/synthetic/rounding-boundaries.csv evidence/runs/corpus-b-output-01
```

Every capture directory contains stdout.log, stderr.log and manifest.json with
argv, working directory, interpreter, revision, tracked-change summary, timestamps,
exact child status and checksums. Replay output directories also contain legacy.csv,
replacement.csv and replay.json. The latter binds the selected input digest and
both implementation digests to output digests. A different corpus is not compared
to the original golden master; both independent subjects receive the same bytes.
Only reviewed, repository-local synthetic inputs are admitted.

| Command | 0 | 1 | 2 |
|---|---|---|---|
| `python3 scripts/compare.py` | equal | valid comparison with a difference | input, execution or comparison invalid |
| `python3 scripts/replay.py INPUT OUTPUT` | equal | valid comparison with a difference | invalid input, path or execution |
| Chapter 20 teaching comparator | equal | valid semantic difference | malformed shape/scale; deliberately invalid here |

The general comparison policy may classify shape differences as mismatches. The
Chapter 20 teaching comparator instead rejects shape/scale violations as invalid.
The Appendix C process gate has its own contract; it does not define this script's
exception status. `make` may translate a failing recipe to its own exit status;
retain the direct Python child status when distinguishing 1 from 2.

## Starter, reviewed correction and retained checkpoint

The starter test asserts that the known difference exists. A passing starter test
is not acceptance of replacement equivalence. At the starter, `make test` passes
and compare/verify fail. Preserve that state at the published tag.

After reviewing both rounding sites, the human records decision 0001 in
`docs/decisions/0001-rounding-mismatch.md`. Required fields are:

```text
**Status:** accepted for local exercise
**Disposition:** preserve legacy rule / correct replacement implementation
**Reviewer:** <actual accountable human>
**Date:** <YYYY-MM-DD>
**Revision:** <full reviewed source commit ID>
**Evidence:** <retained run paths and checksums>
```

The accepted rule is half-up at the fee calculation AND at `_money`. GBP 670.00
exercises the fee tie (1.005 becomes 1.01). GBP 100.005 exercises the independent
money boundary (gross 100.01, fee 0.35, net 99.66). Fixing the first alone is not
sufficient. Do not change legacy or the golden master.

The decision is a human-controlled input: direct-file hook, edit deny rule and
sandbox deny-write entry cover it. They do not authenticate a signer or replace
review. No assistant command may weaken these controls. The human makes the
accepted decision outside the assistant session, then authorizes only replacement
source and the differential test transition. `scripts/review_gate.py` checks
completeness; missing or malformed decisions stop the accepted test.

Once authorized, correct both replacement rounding sites and replace the starter
snapshot test with `exercises/accepted_differential.py` at
`tests/test_differential.py`. This is a reviewed test change, not deletion of a
failure to obtain green output. Run `make test`, `make compare`, `make verify`,
then `PYTHONOPTIMIZE=1 make PYTHON="python3 -O" test compare verify` so optimized
mode reaches verify.py child interpreters too. Reverse only the fee-calculation
rounding and require `AcceptedDifferentialTests.test_fee_rounding_670` to fail;
restore it before reversing only `_money` and requiring
`AcceptedDifferentialTests.test_money_rounding_is_a_second_site` to fail.
Run each with `python3 -m unittest tests.test_differential.<class.method> -v`,
substituting the named class and method, and repeat with `python3 -O`.
Retain assertion failures, not startup errors. Restore both sites and rerun.

The accepted suite also tests negative net below the minimum fee, unique-key batch
partitioning, within-batch duplicate suppression and same-day/holiday behaviour.
Its negative examples are intentional: a cross-batch duplicate is not deduplicated;
a positive 0.01 input has -0.34 net. Properties must not erase those observations.
Only finite decimal amounts are in the reviewed domain. Penny-valued amounts
0.35 through 1000.00 support nonnegative net and penny conservation. The explicit
100.005 example characterizes legacy sub-penny acceptance, not universal scale
validation. NaN, infinity and unbounded precision are outside the admitted input
contract; the legacy parser is not a complete external-input validator.

Copy accepted raw evidence to a NEW `evidence/checkpoints/<checkpoint>/` directory,
including both capture and replay directories and review.md. Run `git add` on the
explicit checkpoint, inspect `git diff --cached`, then commit. `.gitignore` retains
these checkpoint files, including logs; `make clean` touches only ephemeral runs.
Regenerate into new run directories and verify input/output digests match. Never
regenerate over accepted evidence. Charter and claim records are tracked too;
only transient characterization output remains ignored.

## Later checkpoints

- Chapter 9: the human captures the original and boundary corpora independently
  using replay, then seals complete capture/replay directories and input bytes
  under `evidence/captures/09-fee/` for read-only candidate preparation. CSV outputs,
  streams and process status are the local observations; state and external effects
  remain unavailable. Use legacy output for candidate expectations, never replacement
  output. Identity normalization needs no new normalizer code. Preserve the original
  golden master; proposed expansion is a separate corpus. Promotion is a recorded
  manual gate comparing complete relative-path/per-file SHA-256 inventories before
  and after the human copy. Record commands and decisions in
  `evidence/reviews/09-golden-master-review.md`; presence/token checks and replay.json
  do not enforce promotion digest equality. The shared profile has no Edit allow;
  without separately reviewed and tested grants the human applies proposed writes.
- Chapter 13: rehearse the decision, owner, trigger and reconciliation on paper.
  There is no selector yet, so this is a tabletop, not a route-switch test.
- Chapter 14: the admitted Python seam is `replacement_service/batch_entrypoint.py`.
  Use `exercises/batch_entrypoint.py` as the reviewed scaffold. Default is legacy;
  explicit replacement selection records the selected module. Keep comparator
  subjects directly bound to legacy and replacement, never to the same selector.
  Inject a labelled replacement drift in a disposable copy; prove the replacement
  function was called and the output differs. Never edit legacy to make this pass.
- Chapter 16: incoming evidence is the seam decision, tested legacy default and
  explicit replacement selection, original CSV shape and unchanged golden hashes.
  Create `docs/migrations/16-expand-migrate-contract.md` recording old/new fields,
  reader/writer compatibility, null/default rules, deployment order, rollback,
  owner and evidence. If the CSV shape stays unchanged, record that no-op expansion
  explicitly; do not invent a database migration or add columns to the oracle.
- Chapters 17/20/21: retain decision 0001, both tie regressions and reverse-mutant
  evidence. Manual mutation is enough: change one rule in a disposable copy, run
  its semantic test, save the failure, restore, rerun. Reduce a failing input by
  removing rows/fields or reducing amounts while retaining the SAME failure.
  Record original and reduced input, seed or deterministic enumeration, domain,
  command and assertion. jqwik/PIT are optional enterprise demonstrations.
- Chapter 24: include runbook AND rehearsal evidence, not only the index. Require
  selector prerequisite, revision, hashes, operator, human authority, trigger,
  before/after selection, observed output, reconciliation owner and disposition.
- Chapter 26 Stage 1 prepares the non-destructive retirement package and rehearses
  route disablement. Local Stage 2, under a separately signed removal contract,
  removes only the reader-created selector branch and parameter. Retain legacy,
  fixtures, baseline and the comparison harness as historical evidence.
  Enterprise decommissioning is outside both local stages. Removing the protected
  reference implementation requires a separate enterprise contract, protection-owner
  approval, retention/reconciliation approval and release authority. Before any
  such removal, replace dependent tests and Make targets with replacement-only
  checks against retained reviewed data, update verification and demonstrate
  archival recovery. No published lab task authorizes file deletion or weaker protections.
