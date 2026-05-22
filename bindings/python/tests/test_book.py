from unittest import TestCase, main

from gnucash import Session, Account, ACCT_TYPE_INCOME, GncNumeric

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
        from gnucash.gnucash_business import TaxTable, TaxTableEntry

        tables = self.book.TaxTableGetTables()
        self.assertEqual(len(tables), 0)

        account = Account(self.book)
        account.SetType(ACCT_TYPE_INCOME)
        account.SetCommodity(self.currency)

        entry = TaxTableEntry(account=account, percent=True, amount=GncNumeric(10, 100))
        table = TaxTable(self.book, name="TestTaxTable", first_entry=entry)

        tables2 = self.book.TaxTableGetTables()
        self.assertEqual(len(tables2), 1)
        self.assertEqual(tables2[0].GetName(), "TestTaxTable")

if __name__ == '__main__':
    main()
