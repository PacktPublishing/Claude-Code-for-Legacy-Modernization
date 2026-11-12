# Appendix F: Source and version register

Use this appendix to keep a claim tied to the source or execution that supports it. It is a working method for the 26-chapter route, not a second table of contents and not a release checklist.

## Use three evidence states

**Documented** means an identified source describes a mechanic, definition, or caution. Record the title, publisher, stable URL or document identifier, edition or version, retrieval date, and the exact claim it supports.

**Observed** means a retained run produced a result under named controls. Record the immutable source revision, fixture or corpus digest, environment, tool versions, exact command, stdout, stderr, exit status, output digest, and reviewer disposition.

**Illustrative** means the material teaches a method without reporting an execution. Keep examples explicit. Do not promote them to observed evidence because a schema validates or a command looks plausible.

One record may use all three states. Keep them on separate lines so documentation cannot quietly become execution evidence.

## Record a claim

Use a compact entry beside the work:

This is an illustrative record shape, not an observed execution. Replace every placeholder before changing its state to `observed`.

```yaml
claim_id: FEE-COMPARE-001
claim: comparator exposes the seeded STL-1002 rounding difference
state: illustrative
source_revision: <immutable commit>
execution_timestamp_utc: <actual run timestamp>
environment: <OS and Python version>
admitted_input:
  path: fixtures/synthetic/settlements.csv
  sha256: <input digest>
oracle:
  producer: legacy_app.run_batch at the recorded source_revision
  path: <retained copy of evidence/runs/compare-legacy.csv>
  sha256: <captured legacy-output digest>
baseline_reference_not_read_by_compare:
  path: fixtures/golden-master/settlements.expected.csv
  sha256: <baseline reference digest>
command: python3 scripts/compare.py
stdout:
  path: <immutable run-specific stdout file>
  sha256: <captured stdout digest>
stderr:
  path: <immutable run-specific stderr file>
  sha256: <captured stderr digest>
exit_status: <observed exit status>
comparison_artifact:
  path: <retained comparison result or diff>
  sha256: <comparison digest>
replacement_output:
  path: <retained copy of evidence/runs/compare-replacement.csv>
  sha256: <replacement output digest>
reviewer_disposition: pending-human-review
```

The comparator reads `fixtures/synthetic/settlements.csv`, executes both implementations and compares their captured outputs. Its oracle is the legacy output from that execution, not `fixtures/golden-master/settlements.expected.csv`; the latter belongs to the separate baseline check. The replacement CSV is not comparator stdout and is not a full comparison record. Copy generated output into an immutable run-specific evidence location before a later run overwrites it; do not rely on a git-ignored working file as a retained receipt.

A useful record answers five questions: what is claimed, what supports it, which boundary applied, what remains unknown, and who owns the next decision. A URL alone answers only where documentation was found. A passing command answers only what that command checked.

## Compatibility targets and evidence status

The earlier register combined compatibility targets with historical test claims without a revision and retained-output locator for each claim. Those entries are not certified execution records. The following are targets to verify against the exact distributed release:

| Target | Required check | Status here |
| --- | --- | --- |
| Python 3.11.15 | Record interpreter and run unit, baseline, characterisation and comparator commands | Historical run date and stdout not established by this register |
| Claude Code 2.1.170 | Check version policy and wrapper argument tests | Compatibility target; fake-executable tests do not establish an authenticated model workflow |
| JSON and JSON-compatible YAML | Validate registered artefacts | Structural validity does not establish truth |
| Northstar baseline and characterisation | Capture exact command, output and exit status | Expected passing baseline, not a retained run receipt |
| Northstar comparator | Retain the seeded STL-1002 difference | Expected negative case; legacy fee 1.01 versus replacement fee 1.00 is synthetic |
| Aggregate gate | Record individual and aggregate exit statuses | Do not substitute an expected summary for stdout |

For every observed claim, supply an immutable revision, exact input and oracle digests, command, stdout/stderr and exit status, execution timestamp, environment and evidence locator. Record release review, fixture execution and specimen generation as separate events. An event without its original record is unverified; a new run cannot prove its historical date.

The [compatibility manifest](../../companion/northstar-modernization-lab/compatibility/claude-code-2.1.170.json) describes the CLI target. Its existence alone is not a test receipt.

## Distribution and documentation identity

The historical public starter and corrected publisher distribution are separate artefacts even when they use the same `lab/00-start-v2` tag. Record repository identity, immutable commit, release/archive digest and README together. Do not substitute v3 or treat owner access as reader access. The release owner must test the corrected bundle with an unprivileged intended reader before claiming delivery. Local source retention does not close that acceptance gate.

For version-sensitive documentation, record `documentation_url`, `documentation_release_described`, `documentation_accessed_at`, `snapshot_digest_or_locator`, `release_tested` and `run_evidence_locator` separately. Mutable current documentation is not proof of Claude Code 2.1.170 semantics. If no dated snapshot or retained run exists, mark the relevant field unverified rather than copying an access date from another source.

## Add another tool or source

Before relying on a version-sensitive instruction:

1. Name the exact component and version.
2. Pin the source revision and fixture or corpus.
3. Run the positive case and a meaningful negative case.
4. Retain command text, raw output, exit status, environment, and digests.
5. State what the check cannot establish.
6. Link the human decision without implying that the tool made it.

For external sources, prefer normative standards and official product documentation for mechanics. Attribute vendor measurements to the vendor. Use practitioner guidance for patterns and cautions, not as proof of a local outcome. A source supports only the claim for which it was reviewed.

## Keep the boundary visible

The synthetic companion is designed to exercise a baseline, characterisation commands and one seeded rounding difference. Establish those observations for the supplied revision with retained runs; this register does not itself prove them. It does not show that all chapter states were completed, that the replacement is correct, or that anyone approved cutover. Those decisions require the chapter artefacts, retained execution evidence, and named human review.
