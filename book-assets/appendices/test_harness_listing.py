from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

import os
import uuid

from run_subject import amount_minor_units, run_subject, semantic_compare


class SemanticComparatorTest(unittest.TestCase):
    def test_equal_values_have_no_differences(self) -> None:
        value = {"instruction_id": "I-1", "amount": "10.99", "status": "ACCEPTED"}
        self.assertEqual([], semantic_compare(value, value))

    def test_amount_difference_is_visible(self) -> None:
        left = {"instruction_id": "I-1", "amount": "10.99"}
        right = {"instruction_id": "I-1", "amount": "11.00"}
        self.assertEqual("$.amount", semantic_compare(left, right)[0]["path"])

    def test_named_infrastructure_fields_are_ignored(self) -> None:
        left = {"instruction_id": "I-1", "run_id": "A"}
        right = {"instruction_id": "I-1", "run_id": "B"}
        self.assertEqual([], semantic_compare(left, right))

    def test_fractional_minor_unit_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            amount_minor_units("10.999")

    def test_subject_receives_json_and_returns_json(self) -> None:
        program = (
            "import json,sys; value=json.load(sys.stdin); "
            "json.dump({'instruction_id': value['instruction_id'], "
            "'amount': '10.99'}, sys.stdout)"
        )
        result = run_subject(
            "synthetic-" + uuid.uuid4().hex,
            [sys.executable, "-c", program],
            {"instruction_id": "I-1"},
            5,
            Path(os.environ["APPENDIX_TEST_ROOT"]),
        )
        self.assertEqual(0, result.returncode)
        self.assertIsNone(result.parse_error)
        self.assertEqual("I-1", result.parsed["instruction_id"])


if __name__ == "__main__":
    unittest.main()
