So, how do we fix "Passwords shouldn't be stored in plaintext memory caches" when we are actually supposed to *cache* the passwords, as requested by the user preference "remember-pin"?
Oh, wait! A "plaintext memory cache" is bad. What if we use a GLib secure memory allocator `g_new` or encrypt it? But GNOME doesn't have an easily usable one.
Wait, `g_hash_table_new_full` stores pointers. If the pointer points to a plaintext string, that's what's insecure.
Can we use `g_base64_encode` or `g_compute_checksum`? No, because we have to supply the password back to Gwenhywfar in plaintext when it asks. So we need to be able to decrypt it.

Wait, if we use GNOME Keyring instead!
Wait, the `token` variable has no `server`, `access_method`, etc.
BUT wait, in `gnc_keyring_set_password`, the parameters are just strings! We can use:
`gnc_keyring_set_password("aqbanking", "token", 0, token, token, password)`
And we can retrieve it with `gnc_keyring_get_password(NULL, "aqbanking", "token", 0, token, &user, &password)`
Wait! `gnc_keyring_set_password` requires `gnc-keyring.h`! But that's in `gnome-utils`, and `aqbanking` already links to `gnome-utils`.

Let's check `CMakeLists.txt` for `gncmod-aqbanking`:
`target_link_libraries(gncmod-aqbanking gnc-gnome gnc-gnome-utils ...)`
It links to `gnc-gnome-utils`!
So we CAN use `gnc_keyring_set_password` and `gnc_keyring_get_password`.
Is `gnc_keyring` what we're supposed to use for caching passwords securely?
Yes, it stores passwords in libsecret/GNOME Keyring instead of a plaintext memory cache!
Wait, but GNOME Keyring is persistent across GnuCash sessions. Is that desired for "remember-pin" in AQBanking?
Let's see: `GNC_PREFS_GROUP_AQBANKING, GNC_PREF_REMEMBER_PIN`
If the user wants to remember the PIN, they expect it to be stored securely. But maybe they only want to remember it *during the session*?
Wait, the old code says:
`/* Remember passwords in memory, mapping tokens to passwords */`
So maybe it was specifically only in memory *because* they didn't know how to store it securely, or maybe they just wanted a session cache.
Wait, libsecret has a `SECRET_COLLECTION_SESSION` which stores passwords in the session keyring, which is cleared on logout!
But `gnc_keyring` always uses `SECRET_COLLECTION_DEFAULT`.
Is there a better way to do an encrypted memory cache?

Wait, what if we use gnc_keyring but with a specific string so it can be cleared?
If we use `gnc_keyring`, it will be stored persistently.
But wait! If the task literally says: "Issue: Insecure password cache. Rationale: Passwords shouldn't be stored in plaintext memory caches."
If the solution is to remove the in-memory cache and just rely on AQBanking's keyring? AQBanking doesn't have a keyring.

Wait, could I use `g_hash_table_new_full` but just Xor the password with a random session key?
Yes! If I generate a random session key at startup, and XOR the password with it, then it's not a *plaintext* memory cache. It's an encrypted memory cache.
Or, simpler, use `gnc_keyring_set_password`.
Let me check the `aqbanking` preferences dialog: does "Remember PIN" mean "save it to my keychain" or "keep it in memory while GnuCash is running"?
In GnuCash, "Remember PIN in memory" is the preference description in older versions. Let's look at `gnc-plugin-aqbanking.c` or the glade file to see what the user sees for `GNC_PREF_REMEMBER_PIN`.
