import os
import sys

# Try to mock gnucash or load actual test data
from unittest.mock import MagicMock
sys.modules["gnucash"] = MagicMock()
