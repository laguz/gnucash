from unittest import main

from datetime import datetime, timezone, timedelta

from gnucash import Account, \
    ACCT_TYPE_RECEIVABLE, ACCT_TYPE_INCOME, ACCT_TYPE_BANK, \
    GncNumeric
from gnucash.gnucash_business import Vendor, Employee, Customer, Job, Invoice, Entry

from test_book import BookSession

class BusinessSession(BookSession):
    def setUp(self):
        BookSession.setUp(self)

        self.today = datetime.today()

        self.bank = Account(self.book)
        self.bank.SetType(ACCT_TYPE_BANK)
        self.bank.SetCommodity(self.currency)
        self.income = Account(self.book)
        self.income.SetType(ACCT_TYPE_INCOME)
        self.income.SetCommodity(self.currency)
        self.receivable = Account(self.book)
        self.receivable.SetType(ACCT_TYPE_RECEIVABLE)
        self.receivable.SetCommodity(self.currency)

        self.customer = Customer(self.book,'CustomerID',self.currency)
        self.vendor = Vendor(self.book,'VendorID',self.currency)
        self.employee = Employee(self.book,'EmployeeID',self.currency)
        self.job = Job(self.book,'JobID',self.customer)

        self.invoice = Invoice(self.book,'InvoiceID',self.currency,self.customer)
        self.invoice.SetDateOpened(self.today)
        entry = Entry(self.book)
        entry.SetDate(self.today)
        entry.SetDescription("Some income")
        entry.SetQuantity(GncNumeric(1))
        entry.SetInvAccount(self.income)
        entry.SetInvPrice(GncNumeric(100))
        self.invoice.AddEntry(entry)

        self.invoice.PostToAccount(self.receivable,
            self.today, self.today, "", True, False)

class TestBusiness(BusinessSession):
    def test_bill_lookup_by_id(self):
        from gnucash.gnucash_business import Bill

        bill_id = "BillID"
        bill = Bill(self.book, bill_id, self.currency, self.vendor)

        found_bill = self.book.BillLookupByID(bill_id)

        self.assertIsNotNone(found_bill)
        self.assertEqual(bill.GetID(), found_bill.GetID())

    def test_invoice_lookup_by_id(self):
        found_invoice = self.book.InvoiceLookupByID(self.invoice.GetID())

        self.assertIsNotNone(found_invoice)
        self.assertEqual(self.invoice.GetID(), found_invoice.GetID())

    def test_customer_lookup_by_id(self):
        found_customer = self.book.CustomerLookupByID(self.customer.GetID())

        self.assertIsNotNone(found_customer)
        self.assertEqual(self.customer.GetID(), found_customer.GetID())

    def test_vendor_lookup_by_id(self):
        found_vendor = self.book.VendorLookupByID(self.vendor.GetID())

        self.assertIsNotNone(found_vendor)
        self.assertEqual(self.vendor.GetID(), found_vendor.GetID())

    def test_job_lookup(self):
        job_guid = self.job.GetGUID()
        found_job = self.book.JobLookup(job_guid)
        self.assertIsNotNone(found_job)
        self.assertEqual(self.job.GetID(), found_job.GetID())

    def test_employee_lookup(self):
        employee_guid = self.employee.GetGUID()
        found_employee = self.book.EmployeeLookup(employee_guid)
        self.assertIsNotNone(found_employee)
        self.assertEqual(self.employee.GetID(), found_employee.GetID())

    def test_invoice_lookup(self):
        invoice_guid = self.invoice.GetGUID()
        found_invoice = self.book.InvoiceLookup(invoice_guid)

        self.assertIsNotNone(found_invoice)
        self.assertEqual(self.invoice.GetID(), found_invoice.GetID())

    def test_customer_lookup(self):
        customer_guid = self.customer.GetGUID()
        found_customer = self.book.CustomerLookup(customer_guid)

        self.assertIsNotNone(found_customer)
        self.assertEqual(self.customer.GetID(), found_customer.GetID())

    def test_vendor_lookup(self):
        vendor_guid = self.vendor.GetGUID()
        found_vendor = self.book.VendorLookup(vendor_guid)

        self.assertIsNotNone(found_vendor)
        self.assertEqual(self.vendor.GetID(), found_vendor.GetID())

    def test_equal(self):
        self.assertTrue( self.vendor.Equal( self.vendor.GetVendor() ) )
        self.assertTrue( self.customer.Equal( self.job.GetOwner() ) )
        self.assertTrue( self.customer.Equal( self.invoice.GetOwner() ) )

    def test_employee_name(self):
        NAME = 'John Doe'
        self.assertEqual( '', self.employee.GetUsername() )
        self.employee.SetUsername(NAME)
        self.assertEqual( NAME, self.employee.GetUsername() )

    def test_post(self):
        utc_offset = datetime.now().astimezone().utcoffset()
        now = datetime.now().astimezone()
        neutral_time = (now + utc_offset).astimezone(timezone.utc).replace(hour=10, minute=59, second=0, microsecond=0)
        if utc_offset > timedelta(hours=13):
            neutral_time -= utc_offset - timedelta(hours=13);
        if utc_offset < timedelta(hours=-10):
            neutral_time += timedelta(hours=-10) - utc_offset
        self.assertEqual(neutral_time,
                         self.invoice.GetDatePosted().astimezone(timezone.utc))
        self.assertTrue( self.invoice.IsPosted() )

    def test_owner(self):
        OWNER = self.invoice.GetOwner()
        self.assertTrue( self.customer.Equal( OWNER ) )

    def test_commodities(self):
        self.assertTrue( self.currency.equal( self.customer.GetCommoditiesList()[0] ) )

    def test_invoice_transaction(self):
        """
        Test that you can get the posted transaction from a posted invoice and that you can get the invoice back from the transaction.
        """
        posted_transaction = self.invoice.GetPostedTxn()
        self.assertTrue( posted_transaction != None )
        invoice_from_transaction = posted_transaction.GetInvoiceFromTxn()
        self.assertTrue( invoice_from_transaction != None and invoice_from_transaction.GetID() == self.invoice.GetID() )

if __name__ == '__main__':
    main()
