import json
import unittest
from scripts.validate_artifacts import validate, validate_schema_dialect, ValidationError
from scripts.claude_compat import extract_structured_output


class StringKeywordTests(unittest.TestCase):
    def test_min_length_boundaries_and_unicode_codepoints(self):
        for value, minimum in [("", 0), ("abcdefg", 7), ("abcdefgh", 7), ("😀", 1), ("e\u0301", 2), ("a\nb", 3)]:
            with self.subTest(value=value, minimum=minimum):
                validate(value, {"type": "string", "minLength": minimum})
        for value, minimum in [("", 1), ("abcdef", 7), ("😀", 2), ("é", 2)]:
            with self.subTest(value=value, minimum=minimum):
                with self.assertRaisesRegex(ValidationError, "too short"):
                    validate(value, {"minLength": minimum})

    def test_min_length_schema_strictness(self):
        for value in [-1, True, False, 1.0, 0.0, "1", None, [], {}]:
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValidationError, "non-negative integer"):
                    validate_schema_dialect({"minLength": value})

    def test_valid_timestamps(self):
        for value in ["2024-02-29T23:59:59Z", "2000-02-29t00:00:00z", "2026-01-01T00:00:00+05:30", "2026-01-01T00:00:00-00:00", "2026-01-01T00:00:00+23:59", "0001-01-01T00:00:00Z", "9999-12-31T23:59:59-23:59", "2026-01-01T00:00:00.0Z", "2026-01-01T00:00:00.12345678901234567890Z"]:
            with self.subTest(value=value):
                validate(value, {"type": "string", "format": "date-time"})

    def test_invalid_timestamps(self):
        for value in ["", "2023-02-29T00:00:00Z", "1900-02-29T00:00:00Z", "2026-04-31T00:00:00Z", "0000-01-01T00:00:00Z", "2026-00-01T00:00:00Z", "2026-13-01T00:00:00Z", "2026-01-00T00:00:00Z", "2026-01-01T24:00:00Z", "2026-01-01T00:60:00Z", "2026-01-01T00:00:61Z", "2016-12-31T23:59:60Z", "2026-01-01T00:00:00", "2026-01-01", "2026-01-01 00:00:00Z", "2026-01-01T00:00Z", "2026-01-01T00:00:00+24:00", "2026-01-01T00:00:00+00:60", "2026-01-01T00:00:00+0000", "2026-01-01T00:00:00.Z", "2026-01-01T00:00:00,1Z", "2026-01-01T00:00:00Z\n", " 2026-01-01T00:00:00Z", "２０２６-01-01T00:00:00Z", "2026-1-01T00:00:00Z"]:
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValidationError, "date-time"):
                    validate(value, {"format": "date-time"})

    def test_unknown_formats_and_keywords_fail_closed_even_unused(self):
        for value in ["duration", "email", "DATE-TIME", "", None, True, [], {}]:
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValidationError, "unsupported format"):
                    validate({}, {"properties": {"absent": {"format": value}}})
        for schema in [{"maxLength": 10}, {"items": {"exclusiveMinimum": 0}}, {"properties": {"absent": {"unknown": True}}}]:
            with self.assertRaisesRegex(ValidationError, "unsupported schema keywords"):
                validate(None, schema)

    def test_keywords_apply_only_to_strings_type_still_enforced(self):
        for value in [None, 1, True, [], {}]:
            validate(value, {"minLength": 7, "format": "date-time"})
            with self.assertRaisesRegex(ValidationError, "expected type"):
                validate(value, {"type": "string", "minLength": 7, "format": "date-time"})

    def test_wrapper_main_checks_new_keywords_offline(self):
        import contextlib
        import io
        from pathlib import Path
        from tempfile import TemporaryDirectory
        from subprocess import CompletedProcess
        from unittest.mock import patch
        from scripts import claude_compat

        schema = {"type": "object", "required": ["revision", "captured_at"],
                  "properties": {"revision": {"type": "string", "minLength": 7},
                                 "captured_at": {"type": "string", "format": "date-time"}}}
        with TemporaryDirectory(dir=claude_compat.ROOT / "evidence/runs") as directory:
            root = Path(directory)
            prompt = root / "prompt.txt"
            schema_path = root / "schema.json"
            prompt.write_text("Offline regression fixture", encoding="utf-8")
            schema_path.write_text(json.dumps(schema), encoding="utf-8")
            for revision, stamp, expected in [("abcdefg", "2026-01-01T00:00:00Z", 0), ("short", "2026-01-01T00:00:00Z", 1), ("abcdefg", "2026-02-30T00:00:00Z", 1)]:
                payload = {"revision": revision, "captured_at": stamp}
                responses = [CompletedProcess([], 0, "2.1.170", ""),
                             CompletedProcess([], 0, json.dumps({"structured_output": payload}).encode(), b"")]
                out, err = io.StringIO(), io.StringIO()
                with patch.object(claude_compat.subprocess, "run", side_effect=responses) as run, contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                    status = claude_compat.main(["structured-task", "--claude", "offline-never-executed", "--cwd", str(root), "--prompt", str(prompt), "--schema", str(schema_path), "--run-dir", str(root / ("run-" + stamp.replace(":", "_") + revision))])
                self.assertEqual(expected, status)
                self.assertEqual(2, run.call_count)
                self.assertIn(json.dumps(schema), run.call_args.args[0])
                if expected == 0:
                    self.assertEqual(payload, json.loads(out.getvalue()))
                else:
                    self.assertEqual("", out.getvalue())
                    self.assertIn("COMPATIBILITY FAIL", err.getvalue())

    def test_nested_wrapper_payload_checks_both_keywords(self):
        schema = {"type": "object", "required": ["revision", "model_record"], "additionalProperties": False,
                  "properties": {"revision": {"type": "string", "minLength": 7},
                                 "model_record": {"type": "object", "required": ["captured_at"],
                                                  "properties": {"captured_at": {"type": "string", "format": "date-time"}}}}}
        for revision, stamp, valid in [("abcdefg", "2026-01-01T00:00:00Z", True), ("abcdef", "2026-01-01T00:00:00Z", False), ("abcdefg", "2026-02-30T00:00:00Z", False)]:
            payload = {"revision": revision, "model_record": {"captured_at": stamp}}
            envelope = json.dumps({"structured_output": payload})
            if valid:
                self.assertEqual(payload, extract_structured_output(envelope, schema))
            else:
                with self.assertRaises(ValidationError):
                    extract_structured_output(envelope, schema)
        with self.assertRaisesRegex(ValidationError, r"\$\[0\].*date-time"):
            validate(["bad"], {"items": {"format": "date-time"}})


if __name__ == "__main__":
    unittest.main()
