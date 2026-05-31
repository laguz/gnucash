import unittest
from unittest.mock import patch, MagicMock
import sys
import builtins

class RealMockConsole(object):
    def __init__(self, argv=[], shelltype='python', banner=[], filename=None, size=100, user_local_ns=None, user_global_ns=None):
        self.buffer = MagicMock()
        self.view = MagicMock()

class TestInit(unittest.TestCase):
    def setUp(self):
        self.mock_pycons = MagicMock()
        self.mock_pycons.console.Console = RealMockConsole

        self.mock_gtk = MagicMock()
        self.mock_gtk.Justification.CENTER = 'CENTER'

        self.mock_gi = MagicMock()
        self.mock_gi.repository.Gtk = self.mock_gtk
        self.mock_gi.require_version = MagicMock()

        self.mock_gnucash = MagicMock()
        self.mock_gnucash._sw_core_utils = MagicMock()
        self.mock_gnucash._sw_core_utils.gnc_prefs_is_extra_enabled.return_value = False

        self.patcher = patch.dict('sys.modules', {
            'pycons': self.mock_pycons,
            'pycons.console': self.mock_pycons.console,
            'gi': self.mock_gi,
            'gi.repository': self.mock_gi.repository,
            'gnucash': self.mock_gnucash,
            'gnucash._sw_core_utils': self.mock_gnucash._sw_core_utils,
            'gnucash._sw_app_utils': self.mock_gnucash
        })
        self.patcher.start()

        # safely patch builtins._
        self.original_gettext = getattr(builtins, '_', None)
        builtins._ = lambda x: x

        sys.path.insert(0, 'gnucash/python')

    def tearDown(self):
        self.patcher.stop()
        if self.original_gettext is not None:
            builtins._ = self.original_gettext
        else:
            if hasattr(builtins, '_'):
                del builtins._

        if 'gnucash/python' in sys.path:
            sys.path.remove('gnucash/python')

    def test_console_init(self):
        if 'init' in sys.modules:
            del sys.modules['init']
        import init

        console = init.Console()

        self.assertIsNotNone(console.buffer)
        console.buffer.create_tag.assert_called_once_with(
            'center',
            justification='CENTER',
            font='Mono 4'
        )
        self.assertEqual(console.figures, [])
        self.assertEqual(console.callbacks, [])
        self.assertIsNone(console.last_figure)
        self.assertIsNone(console.active_canvas)

        self.assertEqual(console.view.connect.call_count, 3)
        console.view.connect.assert_any_call('key-press-event', console.key_press_event)
        console.view.connect.assert_any_call('button-press-event', console.button_press_event)
        console.view.connect.assert_any_call('scroll-event', console.scroll_event)

if __name__ == '__main__':
    unittest.main()
