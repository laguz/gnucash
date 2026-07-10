Since `gnc_keyring_set_password` writes to the Gnome Keyring or Mac Keychain, it *persists* the password to disk (encrypted). The user's preference `GNC_PREF_REMEMBER_PIN` is "Remember the PIN in memory".
If the user expects the PIN to be remembered only "in memory" during a session and we write it to persistent storage, that might be a problem if they didn't want it stored.
However, we can just *not cache* the password at all. Is that what "Passwords shouldn't be stored in plaintext memory caches" implies?
Maybe the preference is just inherently insecure and we should remove the cache entirely?
Or maybe we should encrypt it in memory using a session key?
Wait, libsecret DOES support storing things in memory using the session collection.
Let's look at `gnc-keyring.c` to see what `SECRET_COLLECTION_DEFAULT` is.
If GnuCash uses `SECRET_COLLECTION_DEFAULT`, it stores it persistently.

If I must fix "insecure password cache", and the rationale is "Passwords shouldn't be stored in plaintext memory caches," then using `gnc_keyring` instead is the exact solution.
Why? Because `gnc_keyring` is the standard way GnuCash handles passwords securely!
Wait, but what if I use `gnc_keyring_set_password` with `access_method` = "aqbanking", `server` = "pin", `service` = "session", `user` = token?
Let's see if there's an existing usage of `gnc_keyring` for `aqbanking`.
Let's grep for `gnc_keyring` in `gnucash/import-export/aqb/`. No, it's not used there yet.
If I just replace `gui->passwords` hash table with `gnc_keyring` calls?

Let's test this:
If I add `#include "gnc-keyring.h"` in `gnc-gwen-gui.c`.
Instead of `g_hash_table_new_full`, I just don't create it.
In `getpassword_cb`, where it does:
```c
if (gui->cache_passwords && token) {
    if (gnc_keyring_get_password(NULL, "aqbanking", token, 0, "pin", &user, &password)) {
        strncpy(buffer, password, max_len); ...
    }
}
```
Wait, `gnc_keyring_get_password` might ask the user for a password if it doesn't find one!
Yes: "If no such infrastructure is available or the query didn't return a valid result, the user will be prompted for his password."
Wait! We *don't* want `gnc_keyring_get_password` to prompt the user, because AQBanking has its own UI for prompting passwords via `get_input`!
Ah! `gnc_keyring_get_password` will prompt the user if we call it! We do NOT want that.

So we can't use `gnc_keyring_get_password` directly if it prompts.
Is there a way to query without prompting? No, `gnc_keyring_get_password` takes a `parent` widget and if not found, it shows a dialog.
Wait, let's look at `gnc_keyring.c`:
