from unittest import TestCase, main
from gnucash import Session, GncPrice, GncNumeric, GncCommodity
from gnucash.gnucash_core_c import PRICE_SOURCE_USER_PRICE

class TestPrice(TestCase):
    def setUp(self):
        self.ses = Session()
        self.book = self.ses.get_book()
        self.table = self.book.get_table()
        self.eur = self.table.lookup('CURRENCY', 'EUR')
        self.usd = self.table.lookup('CURRENCY', 'USD')
        self.pricedb = self.book.get_price_db()
        self.price = GncPrice(self.book)

    def tearDown(self):
        self.ses.end()

    def test_commodity(self):
        self.price.set_commodity(self.eur)
        c = GncCommodity(instance=self.price.get_commodity())
        self.assertEqual(c.get_fullname(), self.eur.get_fullname())

    def test_currency(self):
        self.price.set_currency(self.usd)
        c = GncCommodity(instance=self.price.get_currency())
        self.assertEqual(c.get_fullname(), self.usd.get_fullname())

    def test_value(self):
        v = GncNumeric(1234, 100)
        self.price.set_value(v)
        val = GncNumeric(instance=self.price.get_value())
        self.assertEqual(val.num(), v.num())
        self.assertEqual(val.denom(), v.denom())

    def test_source(self):
        self.price.set_source(PRICE_SOURCE_USER_PRICE)
        self.assertEqual(self.price.get_source(), PRICE_SOURCE_USER_PRICE)

    def test_typestr(self):
        self.price.set_typestr("last")
        self.assertEqual(self.price.get_typestr(), "last")

    def test_pricedb_add(self):
        self.price.set_commodity(self.eur)
        self.price.set_currency(self.usd)
        self.price.set_value(GncNumeric(1234, 100))
        self.price.set_source(PRICE_SOURCE_USER_PRICE)
        self.price.set_typestr("last")
        self.pricedb.add_price(self.price)

        # Test basic pricedb functionality since we are adding it here
        p2 = self.pricedb.lookup_latest(self.eur, self.usd)
        self.assertIsNotNone(p2)
        val = GncNumeric(instance=p2.get_value())
        self.assertEqual(val.num(), 1234)

if __name__ == '__main__':
    main()
