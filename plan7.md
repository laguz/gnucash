Wait, look at `g_hash_table_new_full`. The key is `token` (plaintext) and the value is `password` (plaintext).
If we don't store it in memory, maybe we just use `gnc_keyring_set_password` with `server` as `token` and `service` as `"session"`.
Wait! What if we use `gnc_keyring_set_password` but we DONT want it to be persistent?
Libsecret's `secret_password_store_sync` with `SECRET_COLLECTION_SESSION` stores it in the session memory.
But we are required to fix the vulnerability by writing a secure fix.
"Passwords shouldn't be stored in plaintext memory caches."
Does GnuCash use something like `gnc_password_cache_new`? Let's check `grep -ri "password_cache" gnucash/`.
