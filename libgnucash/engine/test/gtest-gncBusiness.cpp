#include <gtest/gtest.h>
#include <config.h>

extern "C" {
#include "gncBusiness.h"
#include "gncOwner.h"
#include "qof.h"
#include "gncCustomer.h"
#include "gncInvoice.h"
#include "Account.h"
#include "gnc-engine.h"
#include "cashobjects.h"
}

class GncBusinessTest : public ::testing::Test {
protected:
    QofSession* session;
    QofBook* book;

    void SetUp() override {
        qof_init();
        gnc_engine_init(0, nullptr);
        book = qof_book_new();
        session = qof_session_new(book);
    }

    void TearDown() override {
        qof_session_destroy(session);
        qof_close();
    }
};

TEST_F(GncBusinessTest, TestIsPaymentAcctType) {
    // According to gncBusinessIsPaymentAcctType:
    // return xaccAccountIsAssetLiabType(type) || xaccAccountIsEquityType(type)
    // Assets, Bank, Cash, Credit, Liability, Mutual, Stock, Equity

    EXPECT_TRUE(gncBusinessIsPaymentAcctType(ACCT_TYPE_ASSET));
    EXPECT_TRUE(gncBusinessIsPaymentAcctType(ACCT_TYPE_LIABILITY));
    EXPECT_TRUE(gncBusinessIsPaymentAcctType(ACCT_TYPE_CREDIT));
    EXPECT_TRUE(gncBusinessIsPaymentAcctType(ACCT_TYPE_BANK));
    EXPECT_TRUE(gncBusinessIsPaymentAcctType(ACCT_TYPE_CASH));
    EXPECT_TRUE(gncBusinessIsPaymentAcctType(ACCT_TYPE_EQUITY));

    // ACCT_TYPE_PAYABLE and ACCT_TYPE_RECEIVABLE are AP/AR types, but they are not strictly simple asset/liab types in xaccAccountIsAssetLiabType.
    EXPECT_FALSE(gncBusinessIsPaymentAcctType(ACCT_TYPE_PAYABLE));
    EXPECT_FALSE(gncBusinessIsPaymentAcctType(ACCT_TYPE_RECEIVABLE));

    EXPECT_FALSE(gncBusinessIsPaymentAcctType(ACCT_TYPE_INCOME));
    EXPECT_FALSE(gncBusinessIsPaymentAcctType(ACCT_TYPE_EXPENSE));
    EXPECT_FALSE(gncBusinessIsPaymentAcctType(ACCT_TYPE_ROOT));
    EXPECT_FALSE(gncBusinessIsPaymentAcctType(ACCT_TYPE_NONE));
}

TEST_F(GncBusinessTest, TestGetList) {
    GncCustomer* c1 = gncCustomerCreate(book);
    gncCustomerBeginEdit(c1);
    gncCustomerSetActive(c1, TRUE);
    gncCustomerCommitEdit(c1);

    GncCustomer* c2 = gncCustomerCreate(book);
    gncCustomerBeginEdit(c2);
    gncCustomerSetActive(c2, FALSE);
    gncCustomerCommitEdit(c2);

    GList* list1 = gncBusinessGetList(book, GNC_ID_CUSTOMER, TRUE);
    EXPECT_EQ(g_list_length(list1), 2u);
    g_list_free(list1);

    GList* list2 = gncBusinessGetList(book, GNC_ID_CUSTOMER, FALSE);
    EXPECT_EQ(g_list_length(list2), 1u);
    EXPECT_EQ(list2->data, c1);
    g_list_free(list2);

    GncInvoice* i1 = gncInvoiceCreate(book);
    gncInvoiceBeginEdit(i1);
    gncInvoiceSetActive(i1, TRUE);
    gncInvoiceCommitEdit(i1);

    GList* list3 = gncBusinessGetList(book, GNC_ID_INVOICE, TRUE);
    EXPECT_EQ(g_list_length(list3), 1u);
    EXPECT_EQ(list3->data, i1);
    g_list_free(list3);
}

TEST_F(GncBusinessTest, TestGetOwnerList) {
    GncCustomer* c1 = gncCustomerCreate(book);
    gncCustomerBeginEdit(c1);
    gncCustomerSetActive(c1, TRUE);
    gncCustomerCommitEdit(c1);

    GncCustomer* c2 = gncCustomerCreate(book);
    gncCustomerBeginEdit(c2);
    gncCustomerSetActive(c2, FALSE);
    gncCustomerCommitEdit(c2);

    OwnerList* list1 = gncBusinessGetOwnerList(book, GNC_ID_CUSTOMER, TRUE);
    EXPECT_EQ(g_list_length(list1), 2u);

    for (GList* iter = list1; iter != nullptr; iter = iter->next) {
        GncOwner* owner = static_cast<GncOwner*>(iter->data);
        EXPECT_EQ(owner->type, GNC_OWNER_CUSTOMER);
        EXPECT_TRUE(owner->owner.customer == c1 || owner->owner.customer == c2);
        gncOwnerFree(owner);
    }
    g_list_free(list1);

    OwnerList* list2 = gncBusinessGetOwnerList(book, GNC_ID_CUSTOMER, FALSE);
    EXPECT_EQ(g_list_length(list2), 1u);
    GncOwner* owner2 = static_cast<GncOwner*>(list2->data);
    EXPECT_EQ(owner2->type, GNC_OWNER_CUSTOMER);
    EXPECT_EQ(owner2->owner.customer, c1);
    gncOwnerFree(owner2);
    g_list_free(list2);
}
