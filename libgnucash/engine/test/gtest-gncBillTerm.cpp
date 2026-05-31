#include <config.h>
#include <gtest/gtest.h>
#include "../gncBillTermP.h"
#include "../qof.h"

class GncBillTermTest : public ::testing::Test {
protected:
    void SetUp() override {
        qof_init();
    }
    void TearDown() override {
        qof_close();
    }
};

TEST_F(GncBillTermTest, RegisterTest) {
    EXPECT_TRUE(gncBillTermRegister());
    EXPECT_NE(qof_object_lookup(GNC_ID_BILLTERM), nullptr);
}
