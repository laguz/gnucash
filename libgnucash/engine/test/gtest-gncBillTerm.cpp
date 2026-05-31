#include <config.h>
#include <gtest/gtest.h>
#include "../gncBillTermP.h"
#include "../qof.h"

class GncBillTermTest : public ::testing::Test {
protected:
    QofBook *book;

    void SetUp() override {
        qof_init();
        gncBillTermRegister();
        book = qof_book_new();
    }
    void TearDown() override {
        qof_book_destroy(book);
        qof_close();
    }
};

TEST_F(GncBillTermTest, RegisterTest) {
    EXPECT_TRUE(qof_class_is_registered(GNC_ID_BILLTERM));
    EXPECT_NE(qof_object_lookup(GNC_ID_BILLTERM), nullptr);
}

TEST_F(GncBillTermTest, TestSetParentAndGetParent) {
    GncBillTerm *parent = gncBillTermCreate(book);
    GncBillTerm *child = gncBillTermCreate(book);

    EXPECT_EQ(gncBillTermGetParent(child), nullptr);

    // Note: gncBillTermSetParent calls gncBillTermBeginEdit internally,
    // so we shouldn't call it ourselves unless we call commit.
    // Let's just call gncBillTermSetParent directly.
    gncBillTermSetParent(child, parent);
    EXPECT_EQ(gncBillTermGetParent(child), parent);
    EXPECT_TRUE(gncBillTermGetInvisible(child));

    // Cleanup
    gncBillTermBeginEdit(child);
    gncBillTermDestroy(child);
    // child was disconnected, so parent might need edit
    gncBillTermBeginEdit(parent);
    gncBillTermDestroy(parent);
}

TEST_F(GncBillTermTest, TestSetChild) {
    GncBillTerm *term = gncBillTermCreate(book);
    GncBillTerm *child = gncBillTermCreate(book);

    gncBillTermSetChild(term, child);

    // We can verify this via gncBillTermReturnChild
    GncBillTerm *ret_child = gncBillTermReturnChild(term, FALSE);
    EXPECT_EQ(ret_child, child);

    gncBillTermBeginEdit(child);
    gncBillTermDestroy(child);
    gncBillTermBeginEdit(term);
    gncBillTermDestroy(term);
}

TEST_F(GncBillTermTest, TestSetRefcountAndGetRefcount) {
    GncBillTerm *term = gncBillTermCreate(book);

    EXPECT_EQ(gncBillTermGetRefcount(term), 0);
    gncBillTermSetRefcount(term, 42);
    EXPECT_EQ(gncBillTermGetRefcount(term), 42);

    gncBillTermBeginEdit(term);
    gncBillTermDestroy(term);
}

TEST_F(GncBillTermTest, TestMakeInvisibleAndGetInvisible) {
    GncBillTerm *term = gncBillTermCreate(book);

    EXPECT_FALSE(gncBillTermGetInvisible(term));
    gncBillTermMakeInvisible(term);
    EXPECT_TRUE(gncBillTermGetInvisible(term));

    gncBillTermBeginEdit(term);
    gncBillTermDestroy(term);
}
