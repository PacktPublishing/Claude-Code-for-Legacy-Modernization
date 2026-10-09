import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from scripts.validate_artifacts import validate, ValidationError

ROOT = Path(__file__).resolve().parents[1]

class IndependentRegressionTests(unittest.TestCase):
    def test_null_schema_keywords_are_invalid_not_absent(self):
        for key in ('type', 'items', 'additionalProperties'):
            with self.subTest(key=key):
                with self.assertRaises(ValidationError):
                    validate({'unapproved': True}, {key: None})
        validate({'unapproved': True}, {})
        validate(None, {'type': 'null'})

    def test_malformed_hook_events_fail_closed_without_traceback(self):
        for value in ([], None, 'event', 12):
            with self.subTest(value=value):
                result = subprocess.run(
                    [sys.executable, str(ROOT / '.claude/hooks/protect_files.py')],
                    input=json.dumps(value), text=True, capture_output=True,
                    env={**os.environ, 'CLAUDE_PROJECT_DIR': str(ROOT)},
                )
                self.assertEqual(result.returncode, 2)
                self.assertNotIn('Traceback', result.stderr)

if __name__ == '__main__':
    unittest.main()
