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


    def test_bill_lookup_by_id(self):
        from gnucash.gnucash_business import Bill

        try:
            res = self.book.BillLookupByID("123")
            self.assertTrue(res is None or isinstance(res, Bill))
        except Exception as e:
            self.fail(f"BillLookupByID failed with {e}")

    def test_invoice_lookup_by_id(self):
        from gnucash.gnucash_business import Invoice

        try:
            res = self.book.InvoiceLookupByID("123")
            self.assertTrue(res is None or isinstance(res, Invoice))
        except Exception as e:
            self.fail(f"InvoiceLookupByID failed with {e}")

    def test_customer_lookup_by_id(self):
        from gnucash.gnucash_business import Customer

        try:
            res = self.book.CustomerLookupByID("123")
            self.assertTrue(res is None or isinstance(res, Customer))
        except Exception as e:
            self.fail(f"CustomerLookupByID failed with {e}")

    def test_vendor_lookup_by_id(self):
        from gnucash.gnucash_business import Vendor

        try:
            res = self.book.VendorLookupByID("123")
            self.assertTrue(res is None or isinstance(res, Vendor))
        except Exception as e:
            self.fail(f"VendorLookupByID failed with {e}")

    def test_invoice_next_id(self):
        from gnucash.gnucash_business import Customer
        customer = Customer(self.book, "id", self.currency)

        try:
            res = self.book.InvoiceNextID(customer)
            self.assertTrue(isinstance(res, str))
        except Exception as e:
            self.fail(f"InvoiceNextID failed with {e}")

    def test_bill_next_id(self):
        from gnucash.gnucash_business import Vendor
        vendor = Vendor(self.book, "id", self.currency)

        try:
            res = self.book.BillNextID(vendor)
            self.assertTrue(isinstance(res, str))
        except Exception as e:
            self.fail(f"BillNextID failed with {e}")

    def test_customer_next_id(self):
        try:
            res = self.book.CustomerNextID()
            self.assertTrue(isinstance(res, str))
        except Exception as e:
            self.fail(f"CustomerNextID failed with {e}")

    def test_vendor_next_id(self):
        try:
            res = self.book.VendorNextID()
            self.assertTrue(isinstance(res, str))
        except Exception as e:
            self.fail(f"VendorNextID failed with {e}")

    def test_invoice_lookup(self):
        from gnucash import GUID
        from gnucash.gnucash_business import Invoice
        from gnucash.gnucash_core_c import guid_null
        guid = GUID(instance=guid_null())

        try:
            res = self.book.InvoiceLookup(guid)
            self.assertTrue(res is None or isinstance(res, Invoice))
        except Exception as e:
            self.fail(f"InvoiceLookup failed with {e}")

    def test_entry_lookup(self):
        from gnucash import GUID
        from gnucash.gnucash_business import Entry
        from gnucash.gnucash_core_c import guid_null
        guid = GUID(instance=guid_null())

        try:
            res = self.book.EntryLookup(guid)
            self.assertTrue(res is None or isinstance(res, Entry))
        except Exception as e:
            self.fail(f"EntryLookup failed with {e}")

    def test_customer_lookup(self):
        from gnucash import GUID
        from gnucash.gnucash_business import Customer
        from gnucash.gnucash_core_c import guid_null
        guid = GUID(instance=guid_null())

        try:
            res = self.book.CustomerLookup(guid)
            self.assertTrue(res is None or isinstance(res, Customer))
        except Exception as e:
            self.fail(f"CustomerLookup failed with {e}")

    def test_job_lookup(self):
        from gnucash import GUID
        from gnucash.gnucash_business import Job
        from gnucash.gnucash_core_c import guid_null
        guid = GUID(instance=guid_null())

        try:
            res = self.book.JobLookup(guid)
            self.assertTrue(res is None or isinstance(res, Job))
        except Exception as e:
            self.fail(f"JobLookup failed with {e}")

    def test_vendor_lookup(self):
        from gnucash import GUID
        from gnucash.gnucash_business import Vendor
        from gnucash.gnucash_core_c import guid_null
        guid = GUID(instance=guid_null())

        try:
            res = self.book.VendorLookup(guid)
            self.assertTrue(res is None or isinstance(res, Vendor))
        except Exception as e:
            self.fail(f"VendorLookup failed with {e}")

    def test_employee_lookup(self):
        from gnucash import GUID
        from gnucash.gnucash_business import Employee
        from gnucash.gnucash_core_c import guid_null
        guid = GUID(instance=guid_null())

        try:
            res = self.book.EmployeeLookup(guid)
            self.assertTrue(res is None or isinstance(res, Employee))
        except Exception as e:
            self.fail(f"EmployeeLookup failed with {e}")

    def test_tax_table_lookup(self):
        from gnucash import GUID
        from gnucash.gnucash_business import TaxTable
        from gnucash.gnucash_core_c import guid_null
        guid = GUID(instance=guid_null())

        try:
            res = self.book.TaxTableLookup(guid)
            self.assertTrue(res is None or isinstance(res, TaxTable))
        except Exception as e:
            self.fail(f"TaxTableLookup failed with {e}")

    def test_tax_table_get_tables(self):
        try:
            res = self.book.TaxTableGetTables()
            self.assertTrue(isinstance(res, list))
        except Exception as e:
            self.fail(f"TaxTableGetTables failed with {e}")

if __name__ == '__main__':
    main()
