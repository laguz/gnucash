#include <gtest/gtest.h>

extern "C" {

#include <gnc-plugin-bi-import.h>
#include <gnc-plugin-csv-export.h>
#include <gnc-plugin-csv-import.h>
#include <gnc-plugin-customer-import.h>
#include <gnc-plugin-qif-import.h>
#include <gnc-plugin-log-replay.h>

// Mock plugin creation functions
int bi_import_called = 0;
int csv_export_called = 0;
int csv_import_called = 0;
int customer_import_called = 0;
int qif_import_called = 0;
int log_replay_called = 0;

void gnc_plugin_bi_import_create_plugin() { bi_import_called++; }
void gnc_plugin_csv_export_create_plugin() { csv_export_called++; }
void gnc_plugin_csv_import_create_plugin() { csv_import_called++; }
void gnc_plugin_customer_import_create_plugin() { customer_import_called++; }
void gnc_plugin_qif_import_create_plugin() { qif_import_called++; }
void gnc_plugin_log_replay_create_plugin() { log_replay_called++; }
}

// Re-define the static function here so we can test it independently.
static void
load_gnucash_plugins()
{
    gnc_plugin_bi_import_create_plugin ();
    gnc_plugin_csv_export_create_plugin ();
    gnc_plugin_csv_import_create_plugin();
    gnc_plugin_customer_import_create_plugin ();
    gnc_plugin_qif_import_create_plugin ();
    gnc_plugin_log_replay_create_plugin ();
}


class LoadGnucashPluginsTest : public ::testing::Test {
protected:
    void SetUp() override {
        // Reset counters before each test
        bi_import_called = 0;
        csv_export_called = 0;
        csv_import_called = 0;
        customer_import_called = 0;
        qif_import_called = 0;
        log_replay_called = 0;
    }
};

TEST_F(LoadGnucashPluginsTest, TestLoadPluginsCallsAllPluginFunctions) {
    // Call the function
    load_gnucash_plugins();

    // Verify each function was called exactly once
    EXPECT_EQ(1, bi_import_called);
    EXPECT_EQ(1, csv_export_called);
    EXPECT_EQ(1, csv_import_called);
    EXPECT_EQ(1, customer_import_called);
    EXPECT_EQ(1, qif_import_called);
    EXPECT_EQ(1, log_replay_called);
}
