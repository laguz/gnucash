import sys
import os
from unittest import TestCase, main
from unittest.mock import MagicMock
from datetime import date

# Mock the gnucash module before importing the script that uses it
mock_gnucash = MagicMock()
sys.modules["gnucash"] = mock_gnucash

# Add the example_scripts directory to sys.path to find the script
script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'example_scripts'))
if script_dir not in sys.path:
    sys.path.append(script_dir)

# Now we can import the function to be tested
from account_analysis import period_end, next_period_start

class TestAccountAnalysis(TestCase):
    def test_period_end_monthly(self):
        """Test period_end for monthly period"""
        self.assertEqual(period_end(2010, 1, "monthly"), date(2010, 1, 31))

    def test_period_end_quarterly(self):
        """Test period_end for quarterly period"""
        self.assertEqual(period_end(2010, 1, "quarterly"), date(2010, 3, 31))

    def test_period_end_yearly(self):
        """Test period_end for yearly period"""
        self.assertEqual(period_end(2010, 1, "yearly"), date(2010, 12, 31))

    def test_period_end_leap_year(self):
        """Test period_end for leap year"""
        self.assertEqual(period_end(2012, 2, "monthly"), date(2012, 2, 29))
        self.assertEqual(period_end(2011, 2, "monthly"), date(2011, 2, 28))

    def test_period_end_invalid_period(self):
        """Test period_end with invalid period_type"""
        with self.assertRaises(Exception):
            period_end(2010, 1, "weekly")

    def test_period_end_year_wrap(self):
        """Test period_end when the period crosses into the next year"""
        # Monthly crossing into next year
        self.assertEqual(period_end(2010, 12, "monthly"), date(2010, 12, 31))
        # Quarterly crossing into next year
        self.assertEqual(period_end(2010, 11, "quarterly"), date(2011, 1, 31))
        self.assertEqual(period_end(2010, 12, "quarterly"), date(2011, 2, 28))
        # Yearly starting mid-year
        self.assertEqual(period_end(2010, 2, "yearly"), date(2011, 1, 31))

if __name__ == "__main__":
    main()
