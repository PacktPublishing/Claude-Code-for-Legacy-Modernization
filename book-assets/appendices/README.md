# Appendix B and C examples

These files accompany the revised Appendix B and C listings. They are separate from the cumulative settlement lab.

For Appendix B, keep `validate_task_return.py` and its `validate_artifacts.py` dependency together under `tools/contracts/` in the reviewed workspace. Place `return.schema.json` at the contract path. `run-task.sh TASK_ID EXPECTED_TYPE` requires independently admitted contract values, reviewed settings and the companion capture helper. It launches Claude and uses Git; do not run it as an offline test.

For Appendix C, `run_subject.py INPUT LEGACY_COMMAND_JSON REPLACEMENT_COMMAND_JSON REPORT` requires approved absolute executables in an isolated environment. The subjects must be bounded single processes without descendants. The report and its `.streams` sibling must not exist. Original input and raw streams are retained; storage failure or interruption may leave a partial packet and must block acceptance. Agreement does not grant approval.

For synthetic local tests, set `APPENDIX_TEST_ROOT` to a dedicated retained directory and run `python3 book-assets/appendices/test_harness_listing.py`. These tests cover local synthetic subjects, not live CLI containment, production side effects or human decisions.
