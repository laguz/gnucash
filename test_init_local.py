import sys
import unittest
from unittest.mock import MagicMock, patch

# Mock out gnucash module
mock_gnucash = MagicMock()
sys.modules['gnucash'] = mock_gnucash
sys.modules['gnucash._sw_app_utils'] = MagicMock()
sys.modules['gnucash._sw_core_utils'] = MagicMock()
sys.modules['gnucash._sw_core_utils'].gnc_prefs_is_extra_enabled = MagicMock(return_value=False)
sys.modules['gnucash._sw_core_utils'].gnc_prefs_is_debugging_enabled = MagicMock(return_value=False)

# Mock GTK
mock_gi = MagicMock()
sys.modules['gi'] = mock_gi
mock_gi_repository = MagicMock()
sys.modules['gi.repository'] = mock_gi_repository
mock_gi_repository.Gtk = MagicMock()
mock_gi_repository.Gtk.Justification.CENTER = "CENTER"

class MockConsConsole:
    def __init__(self, *args, **kwargs):
        self.buffer = MagicMock()
        self.view = MagicMock()

mock_cons = MagicMock()
mock_cons.Console = MockConsConsole
sys.modules['pycons.console'] = mock_cons

sys.path.insert(0, './gnucash/python')
import init as init_module

class TestConsoleInit(unittest.TestCase):
    def test_console_init(self):
        console = init_module.Console()

        self.assertEqual(console.figures, [])
        self.assertEqual(console.callbacks, [])
        self.assertIsNone(console.last_figure)
        self.assertIsNone(console.active_canvas)
        console.buffer.create_tag.assert_called_with('center', justification='CENTER', font='Mono 4')

        # Check event connections
        console.view.connect.assert_any_call('key-press-event', console.key_press_event)
        console.view.connect.assert_any_call('button-press-event', console.button_press_event)
        console.view.connect.assert_any_call('scroll-event', console.scroll_event)

if __name__ == '__main__':
    unittest.main()
