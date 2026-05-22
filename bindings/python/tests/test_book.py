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

if __name__ == '__main__':
    main()
