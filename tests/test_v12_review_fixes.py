from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from scripts.validate_artifacts import ValidationError, load_data
from scripts.verify_artifact import verify, EXIT_EMPTY, EXIT_TOKEN

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "book-assets/appendices"


def appendix_module(name):
    spec = importlib.util.spec_from_file_location("v12_" + name, EXAMPLES / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class V12ReviewFixesTests(unittest.TestCase):
    def test_nested_duplicate_json_members_rejected(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "value.json"
            for text in ['{"x":1,"x":2}', '{"outer":{"x":1,"x":2}}']:
                path.write_text(text)
                with self.subTest(text=text), self.assertRaisesRegex(ValidationError, "duplicate JSON member"):
                    load_data(path, "json")

    def test_whitespace_artifact_and_partial_label_rejected(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "evidence.md"
            path.write_text(" \n\t")
            self.assertEqual(EXIT_EMPTY, verify(path, ["Reviewer"], Path(tmp))[0])
            path.write_text("NotReviewer: someone\n")
            self.assertEqual(EXIT_TOKEN, verify(path, ["Reviewer"], Path(tmp))[0])

    def test_blank_required_label_rejected_by_cli(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/verify_artifact.py"),
                                 str(ROOT / "README.md"), "--require", " "], capture_output=True)
        self.assertEqual(2, result.returncode)

    def test_appendix_c_rejects_nested_nonfinite_before_normalization(self):
        module = appendix_module("run_subject")
        for raw in ['{"run_id":1e999}', '{"a":[NaN]}', '{"a":{"b":Infinity}}', '{"a":1,"a":2}']:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                module.strict_json(raw)

    def test_appendix_c_retains_raw_output_bytes(self):
        module = appendix_module("run_subject")
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            program = "import sys;sys.stdout.buffer.write(b'{bad json');sys.stderr.buffer.write(b'raw-error')"
            result = module.run_subject("raw", [sys.executable, "-c", program], {"id": "synthetic"}, 5, root)
            self.assertEqual(b"{bad json", Path(result.stdout_path).read_bytes())
            self.assertEqual(b"raw-error", Path(result.stderr_path).read_bytes())
            self.assertIsNotNone(result.parse_error)

    def test_appendix_b_preflight_binds_task_identity_and_type(self):
        result = subprocess.run([sys.executable, str(EXAMPLES / "validate_task_return.py"),
                                 "--preflight", str(EXAMPLES / "return.schema.json"), "TASK-1", "discovery"],
                                capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        schema = json.loads(result.stdout)
        self.assertEqual("TASK-1", schema["properties"]["task_id"]["const"])
        self.assertEqual("discovery", schema["properties"]["task_type"]["const"])

    def test_appendix_b_wrong_task_type_rejected(self):
        with TemporaryDirectory() as tmp:
            schema = Path(tmp) / "schema.json"
            value = Path(tmp) / "return.json"
            schema.write_text('{"type":"object"}')
            value.write_text('{"task_id":"TASK-1","task_type":"implementation","files_changed":[]}')
            result = subprocess.run([sys.executable, str(EXAMPLES / "validate_task_return.py"),
                                     str(schema), str(value), "TASK-1", "discovery"], capture_output=True, text=True)
            self.assertEqual(1, result.returncode)
            self.assertIn("task_type does not match", result.stdout)


class V12DecisionFieldTests(unittest.TestCase):
    def test_blank_and_padded_placeholders_rejected(self):
        from scripts.review_gate import validate
        from tests.test_review_gate import VALID
        for value in (" ", "   <human decision pending>"):
            for name, old in (("Reviewer", "synthetic validator fixture, not approval"),
                              ("Evidence", "synthetic fixture")):
                text = VALID.replace("**" + name + ":** " + old, "**" + name + ":** " + value)
                with self.subTest(name=name, value=value), self.assertRaises(ValueError):
                    validate(text)
