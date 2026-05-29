import unittest
from datetime import date
from ..example_scripts.account_analysis import next_period_start

class TestAccountAnalysis(unittest.TestCase):
    def test_next_period_start_monthly(self):
        # Monthly from Jan
        year, month = next_period_start(2010, 1, "monthly")
        self.assertEqual(year, 2010)
        self.assertEqual(month, 2)

        # Monthly from Dec (wraps to next year)
        year, month = next_period_start(2010, 12, "monthly")
        self.assertEqual(year, 2011)
        self.assertEqual(month, 1)

    def test_next_period_start_quarterly(self):
        # Quarterly from Jan
        year, month = next_period_start(2010, 1, "quarterly")
        self.assertEqual(year, 2010)
        self.assertEqual(month, 4)

        # Quarterly from Oct (wraps to next year)
        year, month = next_period_start(2010, 10, "quarterly")
        self.assertEqual(year, 2011)
        self.assertEqual(month, 1)

    def test_next_period_start_yearly(self):
        # Yearly from Jan
        year, month = next_period_start(2010, 1, "yearly")
        self.assertEqual(year, 2011)
        self.assertEqual(month, 1)

        # Yearly from June
        year, month = next_period_start(2010, 6, "yearly")
        self.assertEqual(year, 2011)
        self.assertEqual(month, 6)

if __name__ == '__main__':
    unittest.main()
