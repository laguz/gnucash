import unittest

from test_book import BookSession
from gnucash.gnucash_core import GUID

class TestGUID(BookSession):
    def test_guid_to_string(self):
        guid = GUID()
        guid_str = guid.to_string()
        self.assertIsInstance(guid_str, str)
        self.assertEqual(len(guid_str), 32)
        # uninitialized GUID shouldn't crash
        self.assertRegex(guid_str, r'^[0-9a-f]{32}$')

        # Test edge case: multiple calls to to_string
        self.assertEqual(guid.to_string(), guid_str)

    def test_guid_equality(self):
        guid1 = GUID()
        guid2 = GUID()
        self.assertNotEqual(guid1.to_string(), guid2.to_string())

    def test_guid_null_to_string(self):
        from gnucash.gnucash_core_c import guid_null
        guid = GUID(instance=guid_null())
        self.assertEqual(guid.to_string(), '00000000000000000000000000000000')


    def test_guid_empty_to_string(self):
        class FakeGUID(GUID):
            def __new__(cls):
                return super(GUID, cls).__new__(cls)
            def __init__(self):
                self._ClassFromFunctions__instance = None

        guid = FakeGUID()
        self.assertIsNone(guid.to_string())

if __name__ == '__main__':

    unittest.main()
