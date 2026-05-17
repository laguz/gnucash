/********************************************************************
 * utest-Policy.cpp: GLib g_test test suite for policy.cpp.         *
 ********************************************************************/

#include "unittest-support.h"

#include <config.h>

#include "Account.h"
#include "Transaction.h"
#include "Split.h"
#include "SplitP.hpp"
#include "gnc-lot.h"
#include "policy.h"
#include "policy-p.h"

typedef struct
{
    QofBook *book;
    Account *acc;
    gnc_commodity *usd;
    gnc_commodity *eur;
} Fixture;

static void
setup (Fixture *fixture, gconstpointer pData)
{
    fixture->book = qof_book_new();
    fixture->acc = xaccMallocAccount(fixture->book);
    fixture->usd = gnc_commodity_new(fixture->book, "US Dollar", "CURRENCY", "USD", "0", 100);
    fixture->eur = gnc_commodity_new(fixture->book, "Euro", "CURRENCY", "EUR", "0", 100);
    xaccAccountSetCommodity(fixture->acc, fixture->usd);
}

static void
teardown (Fixture *fixture, gconstpointer pData)
{
    qof_book_destroy(fixture->book);
}

static Split* create_test_split(Fixture *fixture, gnc_numeric amount, time64 posted, gnc_commodity* curr = nullptr)
{
    if (!curr) curr = fixture->usd;
    Transaction *txn = xaccMallocTransaction(fixture->book);
    Split *split = xaccMallocSplit(fixture->book);

    xaccTransBeginEdit(txn);
    xaccTransSetCurrency(txn, curr);
    xaccTransSetDatePostedSecs(txn, posted);

    split->acc = fixture->acc;
    xaccSplitSetParent(split, txn);

    xaccSplitSetAmount(split, amount);
    xaccSplitSetValue(split, amount);

    xaccTransCommitEdit(txn);
    gnc_account_insert_split(fixture->acc, split);
    return split;
}

static void
FIFOGetPolicy (Fixture *fixture, gconstpointer pData)
{
    GNCPolicy *pcy = xaccGetFIFOPolicy();
    g_assert(pcy != nullptr);
    g_assert(pcy->PolicyGetLot != nullptr);
    g_assert(pcy->PolicyGetSplit != nullptr);
    g_assert(pcy->PolicyGetLotOpening != nullptr);
    g_assert(pcy->PolicyIsOpeningSplit != nullptr);
}

static void
FIFOPolicyGetLot (Fixture *fixture, gconstpointer pData)
{
    GNCPolicy *pcy = xaccGetFIFOPolicy();

    /* Test with NULL split */
    g_assert(pcy->PolicyGetLot(pcy, nullptr) == nullptr);

    /* Setup a split (SELL) */
    Split *split = create_test_split(fixture, gnc_numeric_create(-50, 1), 2000);

    /* FIFOPolicyGetLot calls xaccAccountFindEarliestOpenLot
       Since there are no lots, it should return NULL */
    GNCLot *lot = pcy->PolicyGetLot(pcy, split);
    g_assert(lot == nullptr);

    /* Create a lot and add an earlier split (BUY) */
    GNCLot *new_lot = gnc_lot_new(fixture->book);
    xaccAccountInsertLot(fixture->acc, new_lot);

    Split *split2 = create_test_split(fixture, gnc_numeric_create(100, 1), 1000);
    gnc_lot_add_split(new_lot, split2);

    gnc_numeric bal = gnc_lot_get_balance(new_lot);
    g_assert(!gnc_numeric_zero_p(bal));
    g_assert(!gnc_lot_is_closed(new_lot));

    lot = pcy->PolicyGetLot(pcy, split);
    g_assert(lot != nullptr);
    g_assert(lot == new_lot);
}

static void
FIFOPolicyGetSplit_Basic (Fixture *fixture, gconstpointer pData)
{
    GNCPolicy *pcy = xaccGetFIFOPolicy();

    /* Test with NULL lot */
    g_assert(pcy->PolicyGetSplit(pcy, nullptr) == nullptr);

    GNCLot *lot = gnc_lot_new(fixture->book);
    xaccAccountInsertLot(fixture->acc, lot);

    /* Empty lot */
    g_assert(pcy->PolicyGetSplit(pcy, lot) == nullptr);

    /* Add a split to the lot to establish balance and currency (BUY) */
    Split *split1 = create_test_split(fixture, gnc_numeric_create(100, 1), 1000);
    gnc_lot_add_split(lot, split1);

    /* Add an unassigned split to the account (SELL) */
    Split *split2 = create_test_split(fixture, gnc_numeric_create(-50, 1), 2000);

    Split *found = pcy->PolicyGetSplit(pcy, lot);
    g_assert(found != nullptr);
    g_assert(found == split2);
}

static void
FIFOPolicyGetSplit_ClosedLot (Fixture *fixture, gconstpointer pData)
{
    GNCPolicy *pcy = xaccGetFIFOPolicy();
    GNCLot *lot = gnc_lot_new(fixture->book);
    xaccAccountInsertLot(fixture->acc, lot);

    Split *split1 = create_test_split(fixture, gnc_numeric_create(100, 1), 1000);
    gnc_lot_add_split(lot, split1);

    Split *split2 = create_test_split(fixture, gnc_numeric_create(-100, 1), 2000);
    gnc_lot_add_split(lot, split2);

    g_assert(gnc_lot_is_closed(lot));

    /* Even if there's another unassigned split, PolicyGetSplit should return nullptr for a closed lot */
    create_test_split(fixture, gnc_numeric_create(-50, 1), 3000);

    g_assert(pcy->PolicyGetSplit(pcy, lot) == nullptr);
}

static void
FIFOPolicyGetSplit_NoUnassignedSplits (Fixture *fixture, gconstpointer pData)
{
    GNCPolicy *pcy = xaccGetFIFOPolicy();
    GNCLot *lot = gnc_lot_new(fixture->book);
    xaccAccountInsertLot(fixture->acc, lot);

    Split *split1 = create_test_split(fixture, gnc_numeric_create(100, 1), 1000);
    gnc_lot_add_split(lot, split1);

    g_assert(pcy->PolicyGetSplit(pcy, lot) == nullptr);
}

static void
FIFOPolicyGetSplit_DifferentCurrency (Fixture *fixture, gconstpointer pData)
{
    GNCPolicy *pcy = xaccGetFIFOPolicy();
    GNCLot *lot = gnc_lot_new(fixture->book);
    xaccAccountInsertLot(fixture->acc, lot);

    Split *split1 = create_test_split(fixture, gnc_numeric_create(100, 1), 1000, fixture->usd);
    gnc_lot_add_split(lot, split1);

    /* Unassigned split with different currency */
    create_test_split(fixture, gnc_numeric_create(-50, 1), 2000, fixture->eur);

    g_assert(pcy->PolicyGetSplit(pcy, lot) == nullptr);
}

static void
FIFOPolicyGetSplit_NegativeBalanceLot (Fixture *fixture, gconstpointer pData)
{
    GNCPolicy *pcy = xaccGetFIFOPolicy();
    GNCLot *lot = gnc_lot_new(fixture->book);
    xaccAccountInsertLot(fixture->acc, lot);

    /* Lot opened with a SELL */
    Split *split1 = create_test_split(fixture, gnc_numeric_create(-100, 1), 1000);
    gnc_lot_add_split(lot, split1);

    /* Should find a BUY split to offset the SELL */
    Split *split2 = create_test_split(fixture, gnc_numeric_create(50, 1), 2000);

    Split *found = pcy->PolicyGetSplit(pcy, lot);
    g_assert(found != nullptr);
    g_assert(found == split2);
}

static void
FIFOPolicyLotOpening (Fixture *fixture, gconstpointer pData)
{
    GNCPolicy *pcy = xaccGetFIFOPolicy();
    GNCLot *lot = gnc_lot_new(fixture->book);

    gnc_numeric amt = gnc_numeric_create(100, 1);
    Split *split = create_test_split(fixture, amt, 1000);
    gnc_lot_add_split(lot, split);

    gnc_numeric ret_amt, ret_val;
    gnc_commodity *ret_curr;

    pcy->PolicyGetLotOpening(pcy, lot, &ret_amt, &ret_val, &ret_curr);

    g_assert(gnc_numeric_equal(ret_amt, xaccSplitGetAmount(split)));
    g_assert(gnc_numeric_equal(ret_val, xaccSplitGetValue(split)));
    g_assert(ret_curr == fixture->usd);
}

static void
FIFOPolicyIsOpening (Fixture *fixture, gconstpointer pData)
{
    GNCPolicy *pcy = xaccGetFIFOPolicy();
    GNCLot *lot = gnc_lot_new(fixture->book);

    Split *split1 = create_test_split(fixture, gnc_numeric_create(100, 1), 1000);
    gnc_lot_add_split(lot, split1);

    Split *split2 = create_test_split(fixture, gnc_numeric_create(50, 1), 2000);
    gnc_lot_add_split(lot, split2);

    g_assert(pcy->PolicyIsOpeningSplit(pcy, lot, split1));
    g_assert(!pcy->PolicyIsOpeningSplit(pcy, lot, split2));
}

extern "C" {
  void test_suite_policy(void);
}

void test_suite_policy(void)
{
    const gchar *suitename = "/engine/Policy";
    GNC_TEST_ADD (suitename, "FIFOGetPolicy", Fixture, NULL, setup, FIFOGetPolicy, teardown);
    GNC_TEST_ADD (suitename, "FIFOPolicyGetLot", Fixture, NULL, setup, FIFOPolicyGetLot, teardown);
    GNC_TEST_ADD (suitename, "FIFOPolicyGetSplit_Basic", Fixture, NULL, setup, FIFOPolicyGetSplit_Basic, teardown);
    GNC_TEST_ADD (suitename, "FIFOPolicyGetSplit_ClosedLot", Fixture, NULL, setup, FIFOPolicyGetSplit_ClosedLot, teardown);
    GNC_TEST_ADD (suitename, "FIFOPolicyGetSplit_NoUnassignedSplits", Fixture, NULL, setup, FIFOPolicyGetSplit_NoUnassignedSplits, teardown);
    GNC_TEST_ADD (suitename, "FIFOPolicyGetSplit_DifferentCurrency", Fixture, NULL, setup, FIFOPolicyGetSplit_DifferentCurrency, teardown);
    GNC_TEST_ADD (suitename, "FIFOPolicyGetSplit_NegativeBalanceLot", Fixture, NULL, setup, FIFOPolicyGetSplit_NegativeBalanceLot, teardown);
    GNC_TEST_ADD (suitename, "FIFOPolicyLotOpening", Fixture, NULL, setup, FIFOPolicyLotOpening, teardown);
    GNC_TEST_ADD (suitename, "FIFOPolicyIsOpening", Fixture, NULL, setup, FIFOPolicyIsOpening, teardown);
}
