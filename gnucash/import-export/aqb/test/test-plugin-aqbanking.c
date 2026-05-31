#include <config.h>
#include <glib.h>
#include "gnc-plugin-aqbanking.h"
#include "gnc-plugin-manager.h"

void test_aqb_plugin_create_plugin (void);

void
test_aqb_plugin_create_plugin (void)
{
    GncPluginManager *manager;
    GncPlugin *plugin;

    manager = gnc_plugin_manager_get ();
    g_assert_nonnull (manager);

    plugin = gnc_plugin_manager_get_plugin (manager, GNC_PLUGIN_AQBANKING_NAME);
    g_assert_null (plugin);

    gnc_plugin_aqbanking_create_plugin ();

    plugin = gnc_plugin_manager_get_plugin (manager, GNC_PLUGIN_AQBANKING_NAME);
    g_assert_nonnull (plugin);
    g_assert_true (GNC_IS_PLUGIN_AQBANKING (plugin));

    /* Clean up so we don't break other tests */
    gnc_plugin_manager_remove_plugin (manager, plugin);
}
