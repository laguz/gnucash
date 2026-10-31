import sys
import os
from unittest import TestCase, main
from unittest.mock import MagicMock

# Mock the gnucash module before importing the script that uses it
mock_gnucash = MagicMock()

class MockSplit:
    def __init__(self, instance=None):
        self.instance = instance
        self._lot = None
    def GetLot(self):
        return self._lot

mock_gnucash.Split = MockSplit
sys.modules["gnucash"] = mock_gnucash

# Add the example_scripts directory to sys.path to find the script
script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'example_scripts'))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from gnc_convenience import get_splits_without_lot

class SwigPyObject:
    """Mock for SWIG-wrapped C pointer object."""
    pass

class TestGncConvenience(TestCase):
    def test_get_splits_without_lot_empty(self):
        """Test returning empty list when neither split_list nor account are provided."""
        self.assertEqual(get_splits_without_lot(), [])

        account = MagicMock()
        account.GetSplitList.return_value = []
        self.assertEqual(get_splits_without_lot(account=account), [])

    def test_get_splits_without_lot_split_instances(self):
        """Test filtering splits with and without lots when passed Split instances."""
        s1 = MockSplit()
        s1._lot = None

        s2 = MockSplit()
        s2._lot = MagicMock()

        s3 = MockSplit()
        s3._lot = None

        result = get_splits_without_lot(split_list=[s1, s2, s3])
        self.assertEqual(result, [s1, s3])

    def test_get_splits_without_lot_raw_swig_instances(self):
        """Test wrapping non-Split instances (such as SwigPyObject) into Split."""
        raw_swig1 = SwigPyObject()
        raw_swig2 = SwigPyObject()

        # In MockSplit, instances start with _lot = None by default
        result = get_splits_without_lot(split_list=[raw_swig1, raw_swig2])
        self.assertEqual(len(result), 2)
        self.assertTrue(all(isinstance(s, MockSplit) for s in result))
        self.assertEqual(result[0].instance, raw_swig1)
        self.assertEqual(result[1].instance, raw_swig2)

    def test_get_splits_without_lot_from_account(self):
        """Test getting splits from account object."""
        s1 = MockSplit()
        s1._lot = None

        s2 = MockSplit()
        s2._lot = "lot_obj"

        account = MagicMock()
        account.GetSplitList.return_value = [s1, s2]

        result = get_splits_without_lot(account=account)
        self.assertEqual(result, [s1])
        account.GetSplitList.assert_called_once()

if __name__ == "__main__":
    main()
