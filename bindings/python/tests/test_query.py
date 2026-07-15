from unittest import TestCase, main

from gnucash import Query, QueryStringPredicate
from gnucash.gnucash_core_c import GNC_ID_INVOICE, QOF_COMPARE_EQUAL, QOF_STRING_MATCH_NORMAL, QOF_QUERY_AND


class TestQueryStringPredicate(TestCase):
    def test_create(self):
        qsp = QueryStringPredicate(QOF_COMPARE_EQUAL, "test", QOF_STRING_MATCH_NORMAL, False)
        self.assertIsNotNone(qsp)

    def test_add_term_to_query(self):
        q = Query()
        q.search_for(GNC_ID_INVOICE)
        qsp = QueryStringPredicate(QOF_COMPARE_EQUAL, "test_invoice", QOF_STRING_MATCH_NORMAL, False)

        q.add_term(["id"], qsp, QOF_QUERY_AND)


class TestQuery(TestCase):
    def test_create(self):
        query = Query()
        self.assertIsInstance(query, Query)

    def test_search_for(self):
        query = Query()

        query.search_for(GNC_ID_INVOICE)
        self.assertEqual(query.get_search_for(), GNC_ID_INVOICE)

        obj_type = 'gncInvoice'
        query.search_for(obj_type)
        self.assertEqual(query.get_search_for(), obj_type)

if __name__ == '__main__':
    main()
