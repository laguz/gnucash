import sys
import unittest
from unittest.mock import MagicMock
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../gnucash/python')))

# Make a stub for pycons.console.Console that isn't a MagicMock, so Python class inheritance works
class RealMockConsole(object):
    def __init__(self, argv=[], shelltype='python', banner=[], filename=None, size=100, user_local_ns=None, user_global_ns=None):
        self.buffer = MagicMock()
        self.view = MagicMock()

import types
mock_pycons = types.ModuleType('pycons')
mock_pycons_console = types.ModuleType('pycons.console')
mock_pycons_console.Console = RealMockConsole
sys.modules['pycons'] = mock_pycons
sys.modules['pycons.console'] = mock_pycons_console

sys.modules['gnucash'] = MagicMock()
sys.modules['gnucash._sw_app_utils'] = MagicMock()
sys.modules['gnucash._sw_core_utils'] = MagicMock()
sys.modules['gnucash._sw_core_utils'].gnc_prefs_is_extra_enabled = MagicMock(return_value=False)
sys.modules['gnucash._sw_core_utils'].gnc_prefs_is_debugging_enabled = MagicMock(return_value=False)

sys.modules['gi'] = MagicMock()
sys.modules['gi.repository'] = MagicMock()
sys.modules['gi.repository'].Gtk = MagicMock()
sys.modules['gi.repository'].Gtk.Justification.CENTER = "CENTER"

import init as init_module

class TestConsole(unittest.TestCase):
    def test_console_init(self):
        console = init_module.Console()

        # Verify initialization of class variables
        self.assertEqual(console.figures, [])
        self.assertEqual(console.callbacks, [])
        self.assertIsNone(console.last_figure)
        self.assertIsNone(console.active_canvas)

        # Verify buffer configuration
        console.buffer.create_tag.assert_called_with(
            'center', justification='CENTER', font='Mono 4'
        )

        # Verify event connections
        console.view.connect.assert_any_call('key-press-event', console.key_press_event)
        console.view.connect.assert_any_call('button-press-event', console.button_press_event)
        console.view.connect.assert_any_call('scroll-event', console.scroll_event)

if __name__ == '__main__':
    unittest.main()
