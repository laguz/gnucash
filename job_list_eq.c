#include <glib.h>
#include <stdio.h>
#include <stdbool.h>

bool guid_equal(void* a, void* b) { return true; }
void* qof_instance_get_guid(void* a) { return NULL; }
void* QOF_INSTANCE(void* a) { return a; }

bool check_jobs_equal(GList *a, GList *b) {
    if (g_list_length(a) != g_list_length(b)) {
        return false;
    }

    GList *iter_a, *iter_b;
    for (iter_a = a, iter_b = b; iter_a && iter_b; iter_a = iter_a->next, iter_b = iter_b->next) {
        if (!guid_equal(qof_instance_get_guid(QOF_INSTANCE(iter_a->data)), qof_instance_get_guid(QOF_INSTANCE(iter_b->data)))) {
            return false;
        }
    }
    return true;
}

int main() {
    return 0;
}
