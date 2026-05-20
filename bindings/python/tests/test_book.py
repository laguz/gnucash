from unittest import TestCase, main

from gnucash import Session

class BookSession(TestCase):
    def setUp(self):
        self.ses = Session()
        self.book = self.ses.get_book()
        self.table = self.book.get_table()
        self.currency = self.table.lookup('CURRENCY', 'EUR')

class TestBook(BookSession):
    def test_markclosed(self):
        self.ses.end()

    def test_tax_table_get_tables(self):
        import unittest.mock
        import sys

        # Setup mocks
        mock_instance_1 = unittest.mock.MagicMock()
        mock_instance_2 = unittest.mock.MagicMock()

        # When TaxTableGetTables is called, it uses gncTaxTableGetTables
        # We need to test if we are running under the mock test suite.
        # gnucash_mock_helper inserts 'gnucash' as a mocked ModuleType.
        running_mock = type(sys.modules.get('gnucash')) == type(sys) and sys.modules.get('gnucash').__path__ == []

        if running_mock:
            # We are running with gnucash_mock_helper in the test suite
            gnucash_core_c = sys.modules['gnucash.gnucash_core_c']

            import gnucash.gnucash_core
            with unittest.mock.patch('gnucash.gnucash_core.gncTaxTableGetTables') as mock_core_get_tables:
                mock_core_get_tables.return_value = [mock_instance_1, mock_instance_2]
                gnucash_core_c.gncTaxTableGetTables.return_value = [mock_instance_1, mock_instance_2]

                result = self.book.TaxTableGetTables()

                # Assertions
                if mock_core_get_tables.called:
                    mock_core_get_tables.assert_called_once_with(self.book.instance)
                else:
                    gnucash_core_c.gncTaxTableGetTables.assert_called_once_with(self.book.instance)

                self.assertEqual(len(result), 2)
                sys.modules['gnucash.gnucash_business'].TaxTable.assert_has_calls([
                    unittest.mock.call(instance=mock_instance_1),
                    unittest.mock.call(instance=mock_instance_2),
                ])
        else:
            # We are running under `ctest`, where gnucash is a real module and we patch real methods.
            import gnucash.gnucash_core
            with unittest.mock.patch('gnucash.gnucash_core.gncTaxTableGetTables', create=True) as mock_get_tables:
                with unittest.mock.patch('gnucash.gnucash_business.TaxTable') as mock_taxtable:
                    mock_get_tables.return_value = [mock_instance_1, mock_instance_2]
                    mock_taxtable.side_effect = lambda instance: f"TaxTable({instance})"

                    result = self.book.TaxTableGetTables()

                    mock_get_tables.assert_called_once_with(self.book.instance)
                    self.assertEqual(len(result), 2)
                    self.assertEqual(result, [f"TaxTable({mock_instance_1})", f"TaxTable({mock_instance_2})"])

if __name__ == '__main__':
    main()
