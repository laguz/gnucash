import unittest
from unittest.mock import Mock

from gnucash.gnucash_core import GnuCashCoreClass

class DummyCoreClass(GnuCashCoreClass):
    # ClassFromFunctions requires these, but we bypass __init__ for the test if possible,
    # or just use the base class and mock out __init__
    pass

class TestGnuCashCoreClass(unittest.TestCase):
    def setUp(self):
        # We can bypass the __init__ of ClassFromFunctions by calling __new__ directly
        self.core_instance = GnuCashCoreClass.__new__(GnuCashCoreClass)
        # Mock get_instance which is called by do_lookup_create_oo_instance
        self.core_instance.get_instance = Mock(return_value="core_instance_mock")

    def test_do_lookup_create_oo_instance_success(self):
        """Test do_lookup_create_oo_instance when lookup returns a valid instance"""
        mock_lookup = Mock(return_value="found_thing")
        mock_cls = Mock(return_value="wrapper_thing")

        result = self.core_instance.do_lookup_create_oo_instance(
            mock_lookup, mock_cls, "arg1", "arg2"
        )

        # Verify lookup_function was called correctly with get_instance() and args
        mock_lookup.assert_called_once_with("core_instance_mock", "arg1", "arg2")

        # Verify cls constructor was called correctly with instance=thing
        mock_cls.assert_called_once_with(instance="found_thing")

        # Verify the returned object is the one created by cls
        self.assertEqual(result, "wrapper_thing")

    def test_do_lookup_create_oo_instance_not_found(self):
        """Test do_lookup_create_oo_instance when lookup returns None"""
        mock_lookup = Mock(return_value=None)
        mock_cls = Mock()

        result = self.core_instance.do_lookup_create_oo_instance(
            mock_lookup, mock_cls, "arg1"
        )

        # Verify lookup_function was called correctly
        mock_lookup.assert_called_once_with("core_instance_mock", "arg1")

        # Verify cls constructor was NOT called
        mock_cls.assert_not_called()

        # Verify None is returned
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
