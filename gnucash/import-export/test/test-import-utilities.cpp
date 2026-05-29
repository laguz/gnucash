/********************************************************************\
 * test-import-utilities.cpp - Tests for import-utilities           *
 *                                                                  *
 * This program is free software; you can redistribute it and/or    *
 * modify it under the terms of the GNU General Public License as   *
 * published by the Free Software Foundation; either version 2 of   *
 * the License, or (at your option) any later version.              *
 *                                                                  *
 * This program is distributed in the hope that it will be useful,  *
 * but WITHOUT ANY WARRANTY; without even the implied warranty of   *
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the    *
 * GNU General Public License for more details.                     *
 *                                                                  *
 * You should have received a copy of the GNU General Public License*
 * along with this program; if not, contact:                        *
 *                                                                  *
 * Free Software Foundation           Voice:  +1-617-542-5942       *
 * 51 Franklin Street, Fifth Floor    Fax:    +1-617-542-2652       *
 * Boston, MA  02110-1301,  USA       gnu@gnu.org                   *
\********************************************************************/

#include <glib.h>

#include <config.h>
#include <unittest-support.h>

#include "import-utilities.h"
#include "Split.h"
#include "Transaction.h"

static const gchar *suitename = "/import-export/import-utilities";

typedef struct
{
    QofBook *book;
    Split *split;
    Transaction *txn;
    Account *account;
} Fixture;

static void
setup (Fixture *fixture, gconstpointer pData)
{
    fixture->book = qof_book_new();
    fixture->account = xaccMallocAccount(fixture->book);
    xaccAccountBeginEdit(fixture->account);
    fixture->txn = xaccMallocTransaction(fixture->book);
    xaccTransBeginEdit(fixture->txn);
    fixture->split = xaccMallocSplit (fixture->book);

    // Connect split to transaction and account so it's fully formed
    xaccSplitSetParent(fixture->split, fixture->txn);
    xaccAccountInsertSplit(fixture->account, fixture->split);

    // We don't commit edit here to avoid engine scrubbing
}

static void
teardown (Fixture *fixture, gconstpointer pData)
{
    // Need to clean up safely.
    xaccSplitDestroy(fixture->split);
    xaccTransDestroy(fixture->txn);
    xaccAccountDestroy(fixture->account);

    qof_book_destroy(fixture->book);
    test_clear_error_list();
}

static void
test_split_has_online_id (Fixture *fixture, gconstpointer pData)
{
    /* Should be false initially since no ID is set */
    g_assert_false (gnc_import_split_has_online_id (fixture->split));

    /* Should be true after setting a valid ID */
    gnc_import_set_split_online_id (fixture->split, "12345");
    g_assert_true (gnc_import_split_has_online_id (fixture->split));

    /* Should be false after setting an empty ID */
    gnc_import_set_split_online_id (fixture->split, "");
    g_assert_false (gnc_import_split_has_online_id (fixture->split));
}

int
main (int argc, char *argv[])
{
    int result;
    qof_init();
    g_test_init (&argc, &argv, NULL);

    GNC_TEST_ADD (suitename, "split_has_online_id", Fixture, NULL, setup,
                  test_split_has_online_id, teardown);

    result = g_test_run();

    qof_close();

    return result;
}
