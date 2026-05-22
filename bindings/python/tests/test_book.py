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

    def test_tax_table_lookup_by_name(self):
        from gnucash import Account
        from gnucash.gnucash_business import TaxTableEntry, TaxTable

        # We need to setup an account to associate with the tax table entry
        root = self.book.get_root_account()
        tax_account = Account(self.book)
        tax_account.SetName("Tax Account")
        root.append_child(tax_account)

        # TaxTableEntry constructor expects an Account object
        entry = TaxTableEntry(tax_account)

        tax_table_name = "My Test Tax Table"
        # TaxTable constructor expects book, name, and an entry
        tax_table = TaxTable(self.book, tax_table_name, entry)

        looked_up_table = self.book.TaxTableLookupByName(tax_table_name)

        self.assertIsNotNone(looked_up_table)
        self.assertEqual(looked_up_table.GetName(), tax_table_name)

    def test_tax_table_get_tables(self):
        from gnucash import Account
        from gnucash.gnucash_business import TaxTableEntry, TaxTable

        root = self.book.get_root_account()
        tax_account = Account(self.book)
        tax_account.SetName("Tax Account")
        root.append_child(tax_account)

        entry = TaxTableEntry(tax_account)

        tax_table_name1 = "Tax Table 1"
        tax_table1 = TaxTable(self.book, tax_table_name1, entry)

        tax_table_name2 = "Tax Table 2"
        tax_table2 = TaxTable(self.book, tax_table_name2, entry)

        tables = self.book.TaxTableGetTables()

        self.assertIsInstance(tables, list)
        self.assertEqual(len(tables), 2)

        table_names = [table.GetName() for table in tables]
        self.assertIn(tax_table_name1, table_names)
        self.assertIn(tax_table_name2, table_names)

if __name__ == '__main__':
    main()
