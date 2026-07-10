Wait, let's understand how passwords are being cached in memory vs GNOME keyring.
Does GNOME keyring provide a safe way to store things securely?
Let's see if we can use GNOME keyring for `gui->passwords`.
Actually, if the problem is that `gui->passwords` uses `g_hash_table_new_full`, the simplest fix to the "Passwords shouldn't be stored in plaintext memory caches" vulnerability might be to encrypt the passwords before putting them in the hash table, and decrypt them when taking them out? No, storing the key would have the same problem.
Or maybe we should store them in GNOME Keyring instead of memory?
BUT wait, this memory cache seems to just map `token` to `password` temporarily for a session.
Wait, libsecret / GNOME keyring provides `gnc_keyring_set_password` and `gnc_keyring_get_password`. However, `gnc_keyring_set_password` takes an `access_method`, `server`, etc. and stores them persistently.
Wait, let's look at libsecret. There is `secret_password_store_sync` which is persistent.
What if the vulnerability is exactly that `g_free` is used on passwords, but `erase_password` does `memset` then `g_free`. However, the hash table keys are `g_free`, and values are `erase_password`. BUT! Wait! `g_str_equal`, `g_str_hash`. Wait, if we use `g_hash_table_insert(gui->passwords, g_strdup(token), password)`, `password` is stored in the hash table without any protection, and if memory is swapped out, the password could be leaked. Wait... Is there a secure memory allocator available in GNOME or GnuCash?
Actually, `Gwenhywfar` (which is AQBanking's underlying lib) might have a secure memory allocator?
Let's check `gwenhywfar/crypttoken.h` or similar? No.
GnuCash uses `g_str_hash` and `g_str_equal`.
If the user wants to *not* store passwords in plaintext memory caches, maybe we should just *remove* the `enable_password_cache` entirely?
Wait! Look at the task details carefully:
"File: gnucash/import-export/aqb/gnc-gwen-gui.c:501"
"Issue: Insecure password cache"
"Rationale: Passwords shouldn't be stored in plaintext memory caches."

If I check the commit history or bugs for "Passwords shouldn't be stored in plaintext memory caches", what is the typical fix?
Wait! `g_hash_table_new_full` stores pointers. If the pointer points to a plaintext string, it's a plaintext memory cache.
Can we use a secure memory allocator? Libgcrypt has `gcry_malloc_secure` which prevents the memory from being swapped to disk.
Does GnuCash link to libgcrypt? Let's check `CMakeLists.txt` or `#include <gcrypt.h>`.
Or maybe we just delete the caching logic altogether? If it's a security risk, maybe it's better to just drop it?
Let's see if there's an AQBanking function for securely storing passwords.
