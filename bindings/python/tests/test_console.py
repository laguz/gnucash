import unittest
from unittest.mock import MagicMock, patch
import sys
import os

class TestConsole(unittest.TestCase):
    def setUp(self):
        # Let's cleanly set up mocked dependencies
        self.patchers = []

        # 1. Mock builtin _ (gettext) and gnucash_core_c
        import builtins
        if not hasattr(builtins, '_'):
            builtins._ = lambda x: x
        if not hasattr(builtins, 'gnucash_core_c'):
            builtins.gnucash_core_c = MagicMock()

        # 2. Mock specific modules in sys.modules
        mock_modules = {
            'gnucash': MagicMock(),
            'gnucash._sw_app_utils': MagicMock(),
            'gnucash._sw_core_utils': MagicMock(),
            'gi': MagicMock(),
            'gi.repository': MagicMock()
        }

        # Gtk Dummy
        mock_gtk = MagicMock()
        class DummyJustification:
            CENTER = 1
        mock_gtk.Justification = DummyJustification
        mock_modules['gi.repository.Gtk'] = mock_gtk

        # We need a proper Fake class for pycons.console.Console
        class FakeConsConsole:
            def __init__(self, argv=[], shelltype='python', banner=[], filename=None, size=100, user_local_ns=None, user_global_ns=None):
                self.buffer = MagicMock()
                self.view = MagicMock()
            def key_press_event(self, widget, event):
                return False
            def quit(self):
                return True

        # Use MagicMock for the modules themselves so they behave like packages
        # but attach the concrete FakeConsConsole class so it can be inherited correctly
        mock_pycons = MagicMock()
        mock_pycons_console = MagicMock()
        mock_pycons_console.Console = FakeConsConsole

        # Link them up
        mock_pycons.console = mock_pycons_console

        mock_modules['pycons'] = mock_pycons
        mock_modules['pycons.console'] = mock_pycons_console

        # Patch sys.modules
        p = patch.dict(sys.modules, mock_modules)
        self.patchers.append(p)
        p.start()

        # Need to fix the gnc_prefs execution when init imports it
        sys.modules['gnucash._sw_core_utils'].gnc_prefs_is_extra_enabled = lambda: False
        sys.modules['gnucash._sw_core_utils'].gnc_prefs_is_debugging_enabled = lambda: False

        # Load init module
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../gnucash/python')))
        if 'init' in sys.modules:
            del sys.modules['init']
        import init
        self.init = init
        sys.path.pop(0)

        # Instantiate console
        self.console = init.Console()
        self.console.write = MagicMock()

    def tearDown(self):
        for p in self.patchers:
            p.stop()
        if 'init' in sys.modules:
            del sys.modules['init']

    def test_refresh_calls_draw(self):
        mock_canvas1 = MagicMock()
        mock_canvas2 = MagicMock()

        self.console.figures = [
            ("figure1", mock_canvas1, "anchor1"),
            ("figure2", mock_canvas2, "anchor2")
        ]

        result = self.console.refresh()

        mock_canvas1.draw.assert_called_once()
        mock_canvas2.draw.assert_called_once()
        self.assertFalse(result)

    def test_refresh_empty_figures(self):
        self.console.figures = []
        result = self.console.refresh()
        self.assertFalse(result)

    def test_quit_writes_message(self):
        with patch('pycons.console.Console.quit') as mock_super_quit:
            self.console.quit()
            self.console.write.assert_called_once_with("\nHave a nice day!\n")
            mock_super_quit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
