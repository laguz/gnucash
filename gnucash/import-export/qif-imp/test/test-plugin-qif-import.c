#include <config.h>
#include <glib.h>
#include <libguile.h>
#include "gnc-plugin-qif-import.h"
#include "gnc-plugin-manager.h"
#include "assistant-qif-import.h"
#include "dialog-new-user.h"
#include "dialog-preferences.h"
#include "qof.h"

/* Mock dialog functions to prevent actually showing UI or failing */
void gnc_new_user_dialog_register_qif_assistant (void (*callback)(void)) {}
void gnc_preferences_add_to_page (const gchar *glade_file, const gchar *items_to_add, const gchar *preference_tab_name) {}

static void
test_qif_plugin_create_plugin (void)
{
    GncPluginManager *manager;
    GncPlugin *plugin;

    qof_init();

    manager = gnc_plugin_manager_get ();
    g_assert_nonnull (manager);

    plugin = gnc_plugin_manager_get_plugin (manager, GNC_PLUGIN_QIF_IMPORT_NAME);
    g_assert_null (plugin);

    gnc_ui_qif_import_create_plugin ();

    plugin = gnc_plugin_manager_get_plugin (manager, GNC_PLUGIN_QIF_IMPORT_NAME);
    g_assert_nonnull (plugin);
    g_assert_true (GNC_IS_PLUGIN_QIF_IMPORT (plugin));

    /* Clean up so we don't break other tests */
    gnc_plugin_manager_remove_plugin (manager, plugin);

    qof_close();
}

static void
guile_main(void *closure, int argc, char **argv)
{
    g_test_init (&argc, &argv, NULL);

    /* We need to define a dummy scheme module for `(gnucash qif-import)` because
       gnc_plugin_qif_import_create_plugin calls scm_c_use_module("gnucash qif-import").
       Normally this is loaded from gnucash/qif-import.scm.
       We can mock it by just defining it in Guile so it doesn't fail. */
    scm_c_eval_string("(define-module (gnucash qif-import))");

    g_test_add_func ("/qif-import/plugin/create_plugin", test_qif_plugin_create_plugin);

    g_test_run ();
}

int
main (int argc, char **argv)
{
    scm_boot_guile(argc, argv, guile_main, NULL);
    return 0;
}
