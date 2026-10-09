import unittest

from scripts.compare import compare


class DifferentialHarnessTests(unittest.TestCase):
    def test_starting_state_exposes_known_gap(self):
        # Exact diff: an additional semantic or byte-level discrepancy must fail,
        # even if the intentional STL-1002 rounding rows are still present.
        self.assertEqual(compare(), [
            "--- legacy\n",
            "+++ replacement\n",
            "@@ -1,5 +1,5 @@\n",
            " settlement_id,gross_gbp,fee_gbp,net_gbp,requested_date,settlement_date,status\n",
            " STL-1001,100.00,0.35,99.65,2026-07-24,2026-07-24,SETTLED\n",
            "-STL-1002,670.00,1.01,668.99,2026-07-25,2026-07-27,SETTLED\n",
            "+STL-1002,670.00,1.00,669.00,2026-07-25,2026-07-27,SETTLED\n",
            " STL-1003,10000.00,15.00,9985.00,2026-08-31,2026-09-01,SETTLED\n",
            " STL-1004,250.00,0.38,249.62,2026-12-25,2026-12-29,SETTLED\n",
        ])


if __name__ == "__main__":
    unittest.main()
