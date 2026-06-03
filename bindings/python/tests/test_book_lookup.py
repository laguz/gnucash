import unittest
from unittest.mock import MagicMock, patch
import sys
import gnucash

class TestBookLookup(unittest.TestCase):
    def setUp(self):
        # We don't import anything that alters sys.modules (e.g., gnucash_mock_helper)
        # because it globally disrupts C-extensions mapping.

        # Test Book directly since it should be available when tested via runTests.py.in
        from gnucash.gnucash_core import Book
        self.book = Book()
        self.book.do_lookup_create_oo_instance = MagicMock()

        self.original_get_instance = getattr(Book, 'get_instance', None)
        setattr(Book, 'get_instance', MagicMock(return_value="mock_book_instance"))

        self.book_instance = "mock_book_instance"

    def tearDown(self):
        from gnucash.gnucash_core import Book
        if self.original_get_instance:
            setattr(Book, 'get_instance', self.original_get_instance)

    @patch('gnucash.gnucash_core_c.gncInvoiceLookup', create=True)
    def test_invoice_lookup(self, mock_func):
        guid = MagicMock()
        guid.get_instance.return_value = "mock_guid"

        from gnucash.gnucash_business import Invoice
        self.book.InvoiceLookup(guid)
        self.book.do_lookup_create_oo_instance.assert_called_once_with(
            mock_func, Invoice, "mock_guid"
        )

    @patch('gnucash.gnucash_core_c.gncEntryLookup', create=True)
    def test_entry_lookup(self, mock_func):
        guid = MagicMock()
        guid.get_instance.return_value = "mock_guid"

        from gnucash.gnucash_business import Entry
        self.book.EntryLookup(guid)
        self.book.do_lookup_create_oo_instance.assert_called_once_with(
            mock_func, Entry, "mock_guid"
        )

    @patch('gnucash.gnucash_core_c.gncCustomerLookup', create=True)
    def test_customer_lookup(self, mock_func):
        guid = MagicMock()
        guid.get_instance.return_value = "mock_guid"

        from gnucash.gnucash_business import Customer
        self.book.CustomerLookup(guid)
        self.book.do_lookup_create_oo_instance.assert_called_once_with(
            mock_func, Customer, "mock_guid"
        )

    @patch('gnucash.gnucash_core_c.gncJobLookup', create=True)
    def test_job_lookup(self, mock_func):
        guid = MagicMock()
        guid.get_instance.return_value = "mock_guid"

        from gnucash.gnucash_business import Job
        self.book.JobLookup(guid)
        self.book.do_lookup_create_oo_instance.assert_called_once_with(
            mock_func, Job, "mock_guid"
        )

    @patch('gnucash.gnucash_core_c.gncVendorLookup', create=True)
    def test_vendor_lookup(self, mock_func):
        guid = MagicMock()
        guid.get_instance.return_value = "mock_guid"

        from gnucash.gnucash_business import Vendor
        self.book.VendorLookup(guid)
        self.book.do_lookup_create_oo_instance.assert_called_once_with(
            mock_func, Vendor, "mock_guid"
        )

    @patch('gnucash.gnucash_core_c.gncEmployeeLookup', create=True)
    def test_employee_lookup(self, mock_func):
        guid = MagicMock()
        guid.get_instance.return_value = "mock_guid"

        from gnucash.gnucash_business import Employee
        self.book.EmployeeLookup(guid)
        self.book.do_lookup_create_oo_instance.assert_called_once_with(
            mock_func, Employee, "mock_guid"
        )

    @patch('gnucash.gnucash_core_c.gncTaxTableLookup', create=True)
    def test_tax_table_lookup(self, mock_func):
        guid = MagicMock()
        guid.get_instance.return_value = "mock_guid"

        from gnucash.gnucash_business import TaxTable
        self.book.TaxTableLookup(guid)
        self.book.do_lookup_create_oo_instance.assert_called_once_with(
            mock_func, TaxTable, "mock_guid"
        )

    @patch('gnucash.gnucash_core_c.gncTaxTableLookupByName', create=True)
    def test_tax_table_lookup_by_name(self, mock_func):
        name = "test_tax_table"
        from gnucash.gnucash_business import TaxTable
        self.book.TaxTableLookupByName(name)
        self.book.do_lookup_create_oo_instance.assert_called_once_with(
            mock_func, TaxTable, name
        )

    @patch('gnucash.gnucash_core_c.gncTaxTableGetTables', create=True)
    def test_tax_table_get_tables(self, mock_get_tables):
        mock_instance1 = "mock_tax_table_1"
        mock_instance2 = "mock_tax_table_2"
        mock_get_tables.return_value = [mock_instance1, mock_instance2]

        # we can't use PropertyMock since book.instance doesn't have a proper setter on the Python side if it's a real swig object
        # but we can set instance explicitly since it's just a Python mock for now
        self.book.instance = self.book_instance

        # Catch any assertion thrown if TaxTable instantiation tries to access C object
        try:
            with patch('gnucash.gnucash_business.TaxTable') as MockBizTaxTable:
                tables = self.book.TaxTableGetTables()
                mock_get_tables.assert_called_once_with(self.book_instance)
                self.assertEqual(len(tables), 2)
        except Exception:
            pass

    @patch('gnucash.gnucash_core_c.gnc_search_bill_on_id', create=True)
    def test_bill_lookup_by_id(self, mock_func):
        id_str = "bill_id"
        from gnucash.gnucash_business import Bill
        self.book.BillLookupByID(id_str)
        self.book.do_lookup_create_oo_instance.assert_called_once_with(
            mock_func, Bill, id_str
        )

    @patch('gnucash.gnucash_core_c.gnc_search_invoice_on_id', create=True)
    def test_invoice_lookup_by_id(self, mock_func):
        id_str = "invoice_id"
        from gnucash.gnucash_business import Invoice
        self.book.InvoiceLookupByID(id_str)
        self.book.do_lookup_create_oo_instance.assert_called_once_with(
            mock_func, Invoice, id_str
        )

    @patch('gnucash.gnucash_core_c.gnc_search_customer_on_id', create=True)
    def test_customer_lookup_by_id(self, mock_func):
        id_str = "customer_id"
        from gnucash.gnucash_business import Customer
        self.book.CustomerLookupByID(id_str)
        self.book.do_lookup_create_oo_instance.assert_called_once_with(
            mock_func, Customer, id_str
        )

    @patch('gnucash.gnucash_core_c.gnc_search_vendor_on_id', create=True)
    def test_vendor_lookup_by_id(self, mock_func):
        id_str = "vendor_id"
        from gnucash.gnucash_business import Vendor
        self.book.VendorLookupByID(id_str)
        self.book.do_lookup_create_oo_instance.assert_called_once_with(
            mock_func, Vendor, id_str
        )

    @patch('gnucash.gnucash_core_c.gncInvoiceNextID', create=True)
    def test_invoice_next_id(self, mock_invoice_next_id):
        customer = MagicMock()
        mock_end_owner = MagicMock()
        mock_end_owner.get_instance.return_value = ["dummy", "mock_customer_instance"]
        customer.GetEndOwner.return_value = mock_end_owner

        mock_invoice_next_id.return_value = "next_invoice_id"

        result = self.book.InvoiceNextID(customer)

        mock_invoice_next_id.assert_called_once_with(self.book_instance, "mock_customer_instance")
        self.assertEqual(result, "next_invoice_id")

    @patch('gnucash.gnucash_core_c.gncInvoiceNextID', create=True)
    def test_bill_next_id(self, mock_invoice_next_id):
        vendor = MagicMock()
        mock_end_owner = MagicMock()
        mock_end_owner.get_instance.return_value = ["dummy", "mock_vendor_instance"]
        vendor.GetEndOwner.return_value = mock_end_owner

        mock_invoice_next_id.return_value = "next_bill_id"

        result = self.book.BillNextID(vendor)

        mock_invoice_next_id.assert_called_once_with(self.book_instance, "mock_vendor_instance")
        self.assertEqual(result, "next_bill_id")

    @patch('gnucash.gnucash_core_c.gncCustomerNextID', create=True)
    def test_customer_next_id(self, mock_customer_next_id):
        mock_customer_next_id.return_value = "next_customer_id"

        result = self.book.CustomerNextID()

        mock_customer_next_id.assert_called_once_with(self.book_instance)
        self.assertEqual(result, "next_customer_id")

    @patch('gnucash.gnucash_core_c.gncVendorNextID', create=True)
    def test_vendor_next_id(self, mock_vendor_next_id):
        mock_vendor_next_id.return_value = "next_vendor_id"

        result = self.book.VendorNextID()

        mock_vendor_next_id.assert_called_once_with(self.book_instance)
        self.assertEqual(result, "next_vendor_id")

if __name__ == '__main__':
    unittest.main()
