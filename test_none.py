import sys
import unittest
import os

bindings_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'bindings', 'python'))
tests_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'bindings', 'python', 'tests'))
sys.path.insert(0, bindings_path)
sys.path.insert(0, tests_path)

from gnucash_mock_helper import setup_gnucash_mocks
setup_gnucash_mocks()

# make sure gnucash.gnucash_core can be imported from gnucash_core.py
import gnucash_core
sys.modules['gnucash.gnucash_core'] = gnucash_core

from unittest.mock import MagicMock
from test_decorate_monetary import TestDecorateMonetaryList

def test_decorator_none_commodity_mock():
    item = MagicMock()
    item.commodity = None
    item.value = "dummy"

    def mock_orig_function(self, *args):
        return [item]

    decorated = gnucash_core.decorate_monetary_list_returning_function(mock_orig_function)

    try:
        decorated(MagicMock())
        print("Did not raise error")
    except Exception as e:
        print("Raised:", type(e))

if __name__ == "__main__":
    test_decorator_none_commodity_mock()
