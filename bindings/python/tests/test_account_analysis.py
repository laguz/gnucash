import sys
import os
from unittest import TestCase, main
from unittest.mock import patch, MagicMock
from datetime import date

# Add the example_scripts directory to sys.path to find the script
script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'example_scripts'))
if script_dir not in sys.path:
    sys.path.append(script_dir)


class TestAccountAnalysis(TestCase):
    def setUp(self):
        # Isolate the test by mocking required modules using patch.dict
        self.mock_gnucash = MagicMock()
        self.patcher = patch.dict('sys.modules', {"gnucash": self.mock_gnucash})
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_next_period_start_monthly(self):
        """Test next_period_start for monthly period"""
        from account_analysis import next_period_start
        self.assertEqual(next_period_start(2010, 1, "monthly"), (2010, 2))
        self.assertEqual(next_period_start(2010, 12, "monthly"), (2011, 1))

    def test_next_period_start_quarterly(self):
        """Test next_period_start for quarterly period"""
        from account_analysis import next_period_start
        self.assertEqual(next_period_start(2010, 1, "quarterly"), (2010, 4))
        self.assertEqual(next_period_start(2010, 10, "quarterly"), (2011, 1))
        self.assertEqual(next_period_start(2010, 11, "quarterly"), (2011, 2))
        self.assertEqual(next_period_start(2010, 12, "quarterly"), (2011, 3))

    def test_next_period_start_yearly(self):
        """Test next_period_start for yearly period"""
        from account_analysis import next_period_start
        self.assertEqual(next_period_start(2010, 1, "yearly"), (2011, 1))
        self.assertEqual(next_period_start(2010, 6, "yearly"), (2011, 6))

    def test_next_period_start_edge_cases(self):
        """Test next_period_start with year wrap edge cases"""
        from account_analysis import next_period_start
        # Edge case: Period lands exactly on the end of a year (month 12)
        # e.g., start_month 9 + 3 months (quarterly) = 12 (same year)
        self.assertEqual(next_period_start(2010, 9, "quarterly"), (2010, 12))

        # Edge case: Period lands exactly on the beginning of a year (month 1)
        # e.g., start_month 10 + 3 months (quarterly) = 13 (next year, month 1)
        self.assertEqual(next_period_start(2010, 10, "quarterly"), (2011, 1))

    def test_next_period_start_invalid_period(self):
        """Test next_period_start with invalid period_type"""
        from account_analysis import next_period_start
        with self.assertRaises(KeyError):
            next_period_start(2010, 1, "weekly")

    def test_period_end_monthly(self):
        """Test period_end for monthly period"""
        from account_analysis import period_end
        self.assertEqual(period_end(2010, 1, "monthly"), date(2010, 1, 31))

    def test_period_end_quarterly(self):
        """Test period_end for quarterly period"""
        from account_analysis import period_end
        self.assertEqual(period_end(2010, 1, "quarterly"), date(2010, 3, 31))

    def test_period_end_yearly(self):
        """Test period_end for yearly period"""
        from account_analysis import period_end
        self.assertEqual(period_end(2010, 1, "yearly"), date(2010, 12, 31))

    def test_period_end_leap_year(self):
        """Test period_end for leap year"""
        from account_analysis import period_end
        self.assertEqual(period_end(2012, 2, "monthly"), date(2012, 2, 29))
        self.assertEqual(period_end(2011, 2, "monthly"), date(2011, 2, 28))

    def test_period_end_invalid_period(self):
        """Test period_end with invalid period_type"""
        from account_analysis import period_end
        with self.assertRaises(Exception):
            period_end(2010, 1, "weekly")

    def test_period_end_year_wrap(self):
        """Test period_end when the period crosses into the next year"""
        from account_analysis import period_end
        # Monthly crossing into next year
        self.assertEqual(period_end(2010, 12, "monthly"), date(2010, 12, 31))
        # Quarterly crossing into next year
        self.assertEqual(period_end(2010, 11, "quarterly"), date(2011, 1, 31))
        self.assertEqual(period_end(2010, 12, "quarterly"), date(2011, 2, 28))
        # Yearly starting mid-year
        self.assertEqual(period_end(2010, 2, "yearly"), date(2011, 1, 31))

    def test_invalid_period_type_raises_exception_extra(self):
        """Testing invalid period_type which raises an Exception as requested"""
        from account_analysis import period_end
        with self.assertRaises(Exception):
            period_end(2010, 1, "weekly_invalid")

    def test_period_end_other_than_monthly_extra(self):
        """Testing period types other than monthly as requested"""
        from account_analysis import period_end
        self.assertEqual(period_end(2010, 1, "quarterly"), date(2010, 3, 31))
        self.assertEqual(period_end(2010, 1, "yearly"), date(2010, 12, 31))

if __name__ == "__main__":
    main()
