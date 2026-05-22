import sys
import os
sys.path.append(os.path.abspath('bindings/python/example_scripts'))
from unittest.mock import MagicMock
sys.modules["gnucash"] = MagicMock()
from export_account_totals import get_all_sub_accounts

acc = MagicMock()
acc.get_children_sorted.return_value = []
print(list(get_all_sub_accounts(acc)))
