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
        self.assertEqual(next_period_start(2010, 12, "yearly"), (2011, 12))

    def test_next_period_start_edge_cases(self):
        """Test next_period_start with year wrap edge cases"""
        from account_analysis import next_period_start
        # Edge case: Period lands exactly on the end of a year (month 12)
        # e.g., start_month 9 + 3 months (quarterly) = 12 (same year)
        self.assertEqual(next_period_start(2010, 9, "quarterly"), (2010, 12))

        # Edge case: Period lands exactly on the beginning of a year (month 1)
        # e.g., start_month 10 + 3 months (quarterly) = 13 (next year, month 1)
        self.assertEqual(next_period_start(2010, 10, "quarterly"), (2011, 1))

    def test_next_period_start_custom_period(self):
        """Test next_period_start with a dynamically added custom period length"""
        import account_analysis
        from account_analysis import next_period_start

        # Add a custom 18-month period to PERIODS
        account_analysis.PERIODS["eighteen_months"] = 18

        # 18 months from 2010-01 should be 2011-07
        self.assertEqual(next_period_start(2010, 1, "eighteen_months"), (2011, 7))

        # 18 months from 2010-10 should be 2012-04
        self.assertEqual(next_period_start(2010, 10, "eighteen_months"), (2012, 4))

        # 36 months from 2010-01 should be 2013-01
        account_analysis.PERIODS["three_years"] = 36
        self.assertEqual(next_period_start(2010, 1, "three_years"), (2013, 1))

        # Clean up
        del account_analysis.PERIODS["eighteen_months"]
        del account_analysis.PERIODS["three_years"]

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

    def test_gnc_numeric_to_python_Decimal_positive(self):
        """Test gnc_numeric_to_python_Decimal with positive values"""
        from account_analysis import gnc_numeric_to_python_Decimal
        mock_numeric = MagicMock()
        mock_numeric.negative_p.return_value = False
        mock_numeric.num.return_value = 1234
        mock_numeric.denom.return_value = 100
        # When creating the GncNumeric copy
        self.mock_gnucash.GncNumeric.return_value.to_decimal.return_value = True
        self.mock_gnucash.GncNumeric.return_value.num.return_value = 1234
        self.mock_gnucash.GncNumeric.return_value.denom.return_value = 100

        from decimal import Decimal
        self.assertEqual(gnc_numeric_to_python_Decimal(mock_numeric), Decimal('12.34'))

    def test_gnc_numeric_to_python_Decimal_negative(self):
        """Test gnc_numeric_to_python_Decimal with negative values"""
        from account_analysis import gnc_numeric_to_python_Decimal
        mock_numeric = MagicMock()
        mock_numeric.negative_p.return_value = True
        mock_numeric.num.return_value = -1234
        mock_numeric.denom.return_value = 100
        # When creating the GncNumeric copy
        self.mock_gnucash.GncNumeric.return_value.to_decimal.return_value = True
        self.mock_gnucash.GncNumeric.return_value.num.return_value = -1234
        self.mock_gnucash.GncNumeric.return_value.denom.return_value = 100

        from decimal import Decimal
        self.assertEqual(gnc_numeric_to_python_Decimal(mock_numeric), Decimal('-12.34'))

    def test_gnc_numeric_to_python_Decimal_failure(self):
        """Test gnc_numeric_to_python_Decimal with to_decimal returning None"""
        from account_analysis import gnc_numeric_to_python_Decimal
        mock_numeric = MagicMock()
        self.mock_gnucash.GncNumeric.return_value.to_decimal.return_value = None
        self.mock_gnucash.GncNumeric.return_value.to_string.return_value = "invalid"

        with self.assertRaisesRegex(Exception, "gnc numeric value invalid can't be converted to decimal"):
            gnc_numeric_to_python_Decimal(mock_numeric)

    def test_generate_period_boundaries(self):
        from account_analysis import generate_period_boundaries
        boundaries = list(generate_period_boundaries(2010, 1, "monthly", 3))
        self.assertEqual(boundaries, [
            (date(2010, 1, 1), date(2010, 1, 31)),
            (date(2010, 2, 1), date(2010, 2, 28)),
            (date(2010, 3, 1), date(2010, 3, 31))
        ])

    def test_account_from_path(self):
        from account_analysis import account_from_path
        mock_root = MagicMock()
        mock_child1 = MagicMock()
        mock_child2 = MagicMock()

        mock_root.lookup_by_name.return_value = mock_child1
        mock_child1.lookup_by_name.return_value = mock_child2

        account = account_from_path(mock_root, ["Assets", "Bank"])

        self.assertEqual(account, mock_child2)
        mock_root.lookup_by_name.assert_called_with("Assets")
        mock_child1.lookup_by_name.assert_called_with("Bank")

    def test_account_from_path_failure(self):
        """Test account_from_path when account not found"""
        from account_analysis import account_from_path
        mock_root = MagicMock()
        mock_root.lookup_by_name.return_value = None

        with self.assertRaisesRegex(Exception, "path AssetsBank could not be found"):
            account_from_path(mock_root, ["Assets", "Bank"])

    @patch('sys.argv', ['account_analysis.py'])
    def test_main_not_enough_parameters(self):
        """Test main with missing parameters"""
        from account_analysis import main

        # Capture the print statements
        with patch('builtins.print') as mock_print:
            main()
            mock_print.assert_any_call('not enough parameters')

    @patch('sys.argv', ['account_analysis.py', 'test.gnucash', '2010', '1', 'monthly', '1', 'debits-show', 'credits-show', 'Assets', 'Bank'])
    @patch('sys.stdout', new_callable=MagicMock)
    def test_main_success(self, mock_stdout):
        """Test main successful execution"""
        from account_analysis import main

        mock_session = MagicMock()
        mock_root = MagicMock()
        mock_account = MagicMock()
        mock_split = MagicMock()
        mock_trans = MagicMock()

        self.mock_gnucash.Session.return_value = mock_session
        mock_session.book.get_root_account.return_value = mock_root

        # Setup path lookup
        mock_root.lookup_by_name.return_value = MagicMock(lookup_by_name=MagicMock(return_value=mock_account))

        # Setup splits
        mock_account.GetSplitList.return_value = [mock_split]
        mock_split.parent = mock_trans

        import datetime
        mock_trans.GetDate.return_value = datetime.datetime(2010, 1, 15).timestamp()

        # Mock numeric
        mock_numeric = MagicMock()
        mock_numeric.negative_p.return_value = False
        mock_numeric.num.return_value = 1000
        mock_numeric.denom.return_value = 100
        mock_split.GetAmount.return_value = mock_numeric

        self.mock_gnucash.GncNumeric.return_value.to_decimal.return_value = True
        self.mock_gnucash.GncNumeric.return_value.num.return_value = 1000
        self.mock_gnucash.GncNumeric.return_value.denom.return_value = 100

        mock_trans.GetDescription.return_value = "Test Transaction"

        with patch('csv.writer') as mock_csv_writer:
            main()

        mock_session.end.assert_called_once()
        self.mock_gnucash.Session.assert_called_once_with('test.gnucash', self.mock_gnucash.SessionOpenMode.SESSION_NORMAL_OPEN)

    @patch('sys.argv', ['account_analysis.py', 'test.gnucash', '2010', '1', 'monthly', '12', 'debits-show', 'credits-show', 'Assets', 'Bank'])
    def test_main_exception(self):
        """Test main exception handling ensures session is closed"""
        from account_analysis import main

        mock_session = MagicMock()
        self.mock_gnucash.Session.return_value = mock_session

        mock_session.book.get_root_account.side_effect = Exception("Test Exception")

        with self.assertRaisesRegex(Exception, "Test Exception"):
            main()

        mock_session.end.assert_called_once()

    @patch('sys.argv', ['account_analysis.py', 'test.gnucash', '2010', '1', 'monthly', '1', 'debits-show', 'credits-show', 'Assets', 'Bank'])
    @patch('sys.stdout', new_callable=MagicMock)
    def test_main_success_negative_amount(self, mock_stdout):
        """Test main successful execution with negative amount (credit)"""
        from account_analysis import main

        mock_session = MagicMock()
        mock_root = MagicMock()
        mock_account = MagicMock()
        mock_split = MagicMock()
        mock_trans = MagicMock()

        self.mock_gnucash.Session.return_value = mock_session
        mock_session.book.get_root_account.return_value = mock_root

        # Setup path lookup
        mock_root.lookup_by_name.return_value = MagicMock(lookup_by_name=MagicMock(return_value=mock_account))

        # Setup splits
        mock_account.GetSplitList.return_value = [mock_split]
        mock_split.parent = mock_trans

        import datetime
        mock_trans.GetDate.return_value = datetime.datetime(2010, 1, 15).timestamp()

        # Mock numeric
        mock_numeric = MagicMock()
        mock_numeric.negative_p.return_value = True
        mock_numeric.num.return_value = -1000
        mock_numeric.denom.return_value = 100
        mock_split.GetAmount.return_value = mock_numeric

        self.mock_gnucash.GncNumeric.return_value.to_decimal.return_value = True
        self.mock_gnucash.GncNumeric.return_value.num.return_value = -1000
        self.mock_gnucash.GncNumeric.return_value.denom.return_value = 100

        mock_trans.GetDescription.return_value = "Test Transaction"

        with patch('csv.writer') as mock_csv_writer:
            main()

        mock_session.end.assert_called_once()
        self.mock_gnucash.Session.assert_called_once_with('test.gnucash', self.mock_gnucash.SessionOpenMode.SESSION_NORMAL_OPEN)

if __name__ == "__main__":
    main()
