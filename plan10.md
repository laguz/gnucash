Is there anything else I need to wipe securely?
Let's look at `erase_password`:
```c
static void
erase_password(gchar *password)
{
    g_return_if_fail(password);
    ENTER(" ");
    memset(password, 0, strlen(password));
    g_free(password);
    LEAVE(" ");
}
```
Wait! As I noted before, `memset` followed immediately by `g_free` is often completely optimized out by modern compilers because the memory is about to be freed and no longer accessed! This is a classic CWE-14 vulnerability ("Compiler Removal of Code to Clear Buffers").
Wait, is GnuCash using `memset` securely?
If they do not use a `volatile` pointer or `#pragma GCC optimize ("O0")`, or `explicit_bzero`, the memset WILL be optimized out.
Wait, does GLib have an `explicit_bzero` equivalent?
GnuCash has `#include <glib.h>`. Since GLib 2.44, `g_clear_pointer` can be used? No, that just sets the pointer to NULL.
Wait, `memset_s` or `explicit_bzero`?
Let's see if GnuCash has a secure wipe function.
