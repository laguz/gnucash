#include <gtest/gtest.h>

extern "C" {
#include "dialog-bi-import-helper.h"
#include <qof.h>
}

class BiImportHelperTest : public ::testing::Test {
protected:
    QofDateFormat original_format;

    void SetUp() override {
        // Save the original date format
        original_format = qof_date_format_get();
    }

    void TearDown() override {
        // Restore the original date format
        qof_date_format_set(original_format);
    }
};

TEST_F(BiImportHelperTest, text2bool) {
    // Valid true strings
    EXPECT_TRUE(text2bool("y"));
    EXPECT_TRUE(text2bool("Y"));
    EXPECT_TRUE(text2bool("yes"));
    EXPECT_TRUE(text2bool("t"));
    EXPECT_TRUE(text2bool("T"));
    EXPECT_TRUE(text2bool("true"));
    EXPECT_TRUE(text2bool("1"));
    EXPECT_TRUE(text2bool("x"));
    EXPECT_TRUE(text2bool("X"));
    EXPECT_TRUE(text2bool(" y ")); // with spaces

    // Valid false strings
    EXPECT_FALSE(text2bool("n"));
    EXPECT_FALSE(text2bool("no"));
    EXPECT_FALSE(text2bool("f"));
    EXPECT_FALSE(text2bool("false"));
    EXPECT_FALSE(text2bool("0"));
    EXPECT_FALSE(text2bool(""));
    EXPECT_FALSE(text2bool(nullptr));
    EXPECT_FALSE(text2bool("random"));
}

TEST_F(BiImportHelperTest, text2disc_type) {
    EXPECT_EQ(text2disc_type("%"), GNC_AMT_TYPE_PERCENT);
    EXPECT_EQ(text2disc_type(" % "), GNC_AMT_TYPE_PERCENT); // with spaces
    EXPECT_EQ(text2disc_type(""), GNC_AMT_TYPE_PERCENT); // empty string defaults to percent based on code
    EXPECT_EQ(text2disc_type(nullptr), GNC_AMT_TYPE_PERCENT); // null defaults to percent

    EXPECT_EQ(text2disc_type("$"), GNC_AMT_TYPE_VALUE);
    EXPECT_EQ(text2disc_type("value"), GNC_AMT_TYPE_VALUE);
    EXPECT_EQ(text2disc_type("v"), GNC_AMT_TYPE_VALUE);
}

TEST_F(BiImportHelperTest, text2disc_how) {
    EXPECT_EQ(text2disc_how("="), GNC_DISC_SAMETIME);
    EXPECT_EQ(text2disc_how(" = "), GNC_DISC_SAMETIME);
    EXPECT_EQ(text2disc_how(">"), GNC_DISC_POSTTAX);
    EXPECT_EQ(text2disc_how(" > "), GNC_DISC_POSTTAX);

    EXPECT_EQ(text2disc_how("pre"), GNC_DISC_PRETAX); // Anything else is pretax
    EXPECT_EQ(text2disc_how("<"), GNC_DISC_PRETAX);
    EXPECT_EQ(text2disc_how(""), GNC_DISC_PRETAX);
    EXPECT_EQ(text2disc_how(nullptr), GNC_DISC_PRETAX);
}

TEST_F(BiImportHelperTest, isDateValid) {
    // Test UK format: DD/MM/YYYY
    qof_date_format_set(QOF_DATE_FORMAT_UK);

    // Valid dates
    char date_uk_1[] = "15/01/2023";
    EXPECT_TRUE(isDateValid(date_uk_1));

    char date_uk_2[] = "29/02/2024"; // Leap year
    EXPECT_TRUE(isDateValid(date_uk_2));

    char date_uk_3[] = "01/12/1999";
    EXPECT_TRUE(isDateValid(date_uk_3));

    // Invalid dates for UK format
    char date_uk_garbage[] = "15/01/2023 ABC";
    EXPECT_FALSE(isDateValid(date_uk_garbage));

    char invalid_1[] = "invalid";
    EXPECT_FALSE(isDateValid(invalid_1));

    char date_uk_invalid_1[] = "2023-01-15"; // Wrong format
    EXPECT_FALSE(isDateValid(date_uk_invalid_1));

    // Test US format: MM/DD/YYYY
    qof_date_format_set(QOF_DATE_FORMAT_US);

    // Valid dates
    char date_us_1[] = "01/15/2023";
    EXPECT_TRUE(isDateValid(date_us_1));

    char date_us_2[] = "02/29/2024"; // Leap year
    EXPECT_TRUE(isDateValid(date_us_2));

    // Invalid dates for US format
    // Because strptime allows partial matching, depending on the format string (%m/%d/%Y)
    // it will fail if it cannot match the month first.
    char date_us_invalid_1[] = "15/01/2023"; // month 15 is invalid
    EXPECT_FALSE(isDateValid(date_us_invalid_1));

    // Test CE format: DD.MM.YYYY
    qof_date_format_set(QOF_DATE_FORMAT_CE);

    // Valid dates
    char date_ce_1[] = "15.01.2023";
    EXPECT_TRUE(isDateValid(date_ce_1));

    char date_ce_2[] = "29.02.2024"; // Leap year
    EXPECT_TRUE(isDateValid(date_ce_2));

    // Invalid dates for CE format
    char date_ce_invalid_1[] = "2023-01-15"; // Wrong format
    EXPECT_FALSE(isDateValid(date_ce_invalid_1));

    char date_ce_invalid_2[] = "32.01.2023"; // Day out of bounds
    EXPECT_FALSE(isDateValid(date_ce_invalid_2));

    char date_ce_invalid_3[] = "15.13.2023"; // Month out of bounds
    EXPECT_FALSE(isDateValid(date_ce_invalid_3));

    // Test UTC format: YYYY-MM-DDTHH:MM:SSZ
    qof_date_format_set(QOF_DATE_FORMAT_UTC);

    // Valid dates
    char date_utc_1[] = "2004-12-12T23:39:11Z";
    EXPECT_TRUE(isDateValid(date_utc_1));

    // Invalid dates for UTC format
    char date_utc_invalid_1[] = "2004-12-12 23:39:11Z"; // Missing T
    EXPECT_FALSE(isDateValid(date_utc_invalid_1));

    char date_utc_invalid_2[] = "2004-12-12T23:39:11"; // Missing Z
    EXPECT_FALSE(isDateValid(date_utc_invalid_2));

    // Test ISO format: YYYY-MM-DD
    qof_date_format_set(QOF_DATE_FORMAT_ISO);

    // Valid dates
    char date_iso_1[] = "2023-01-15";
    EXPECT_TRUE(isDateValid(date_iso_1));

    char date_iso_2[] = "2024-02-29"; // Leap year
    EXPECT_TRUE(isDateValid(date_iso_2));

    // Invalid dates for ISO format
    char date_iso_invalid_1[] = "2023-15-01"; // Wrong format (month 15)
    EXPECT_FALSE(isDateValid(date_iso_invalid_1));

    // Empty string
    char empty_string[] = "";
    EXPECT_FALSE(isDateValid(empty_string));

    // Null pointer
    EXPECT_FALSE(isDateValid(nullptr));
}
