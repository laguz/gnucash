Ah! "If active, the PIN for HBCI/AqBanking actions will be remembered in memory during a session. Otherwise it will have to be entered again each time during a session when it is needed."
The issue is simply that the memory cache is *plaintext*, so it is vulnerable if memory is swapped to disk or read by another process (if no proper memory protections).

Wait, the description specifically says "remembered in memory during a session", not "saved to keychain". So maybe we shouldn't use `gnc_keyring_set_password` since that writes to persistent storage (the keychain/libsecret).
Or maybe we DO want to use it? GNOME Keyring has a session keyring. But GnuCash's `gnc_keyring_set_password` doesn't differentiate - it just stores it in the default keyring.

If we don't use GNOME Keyring, how do we fix "plaintext memory caches" in C?
Is there a memory wiping function? Yes, `erase_password` does wiping (`memset`, then `g_free`).
But `gui->passwords` keeps it in memory indefinitely during the session, which makes it a "plaintext memory cache".
Can we use a simple XOR obfuscation using a randomly generated key for the duration of the process?
This is a standard way to prevent *casual* memory scraping from finding plaintext strings like passwords.
If we generate a random byte array when the app starts, and then XOR passwords before storing them in `gui->passwords`, and XOR them back when retrieving, they won't be stored in plaintext memory.

Let's check if GnuCash has a utility for this, like `gnc_password_obfuscate` or something.
