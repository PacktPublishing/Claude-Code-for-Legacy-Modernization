import unittest
from scripts.review_gate import validate

VALID = """**Status:** accepted for local exercise
**Disposition:** preserve legacy rule / correct replacement implementation
**Reviewer:** synthetic validator fixture, not approval
**Date:** 2026-11-05
**Revision:** 0000000000000000000000000000000000000000
**Evidence:** synthetic fixture
"""

class ReviewGateTests(unittest.TestCase):
    def test_complete_fixture(self):
        self.assertEqual("synthetic fixture", validate(VALID)["Evidence"])

    def test_every_field_is_required(self):
        for line in VALID.splitlines():
            with self.assertRaises(ValueError):
                validate(VALID.replace(line, ""))
        for value in ("", VALID.replace("2026-11-05", "2026-99-99"), VALID.replace("0" * 40, "main")):
            with self.assertRaises(ValueError):
                validate(value)
