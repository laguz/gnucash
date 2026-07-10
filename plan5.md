Let's consider another approach.
If `gnc_keyring_set_password` is meant to be used, but the preference says "in memory", what if I just change the preference to NOT store in memory, but use the keyring?
Actually, `gnc_keyring` *IS* the secure way to store passwords in GnuCash!
The database login password is not remembered in memory, it is remembered in the keyring.
If AQBanking's PIN was stored in memory before, it's a legacy vulnerability. We can just use `gnc_keyring_set_password` instead of `g_hash_table_new_full`.
Wait, there's a problem: what if `gnc_keyring` asks the user to unlock the keyring? The user might have it unlocked.
Wait, `token` might not be safe to use as `user` or `server`?
Actually, in `getpassword_cb`, `token` is just a string (like `pin` or something, a token identifying the card/account).

Let's see what happens if I replace the `g_hash_table` logic with `gnc_keyring_set_password` and `gnc_keyring_get_password`.
In `gnc_keyring_set_password(const gchar *access_method, const gchar *server, guint32 port, const gchar *service, const gchar *user, const gchar* password)`:
We can call: `gnc_keyring_set_password("aqbanking", "pin", 0, "session", token, password)`.

BUT WAIT! If the user wants to keep the PIN *only during this session*, using the persistent keychain is a behavior change! They might not want their bank PIN saved to the OS keychain permanently.
Is there a way to do memory obfuscation?
Yes, I can just implement a simple XOR obfuscator:
```c
static guint8 obf_key[32];
static gboolean obf_key_initialized = FALSE;

static void init_obf_key() {
    if (!obf_key_initialized) {
        for(int i=0; i<32; i++) obf_key[i] = g_random_int() & 0xFF;
        obf_key_initialized = TRUE;
    }
}

static gchar* obfuscate(const gchar* plaintext) {
    if(!plaintext) return NULL;
    int len = strlen(plaintext);
    gchar* res = g_malloc(len + 1);
    for(int i=0; i<len; i++) {
        res[i] = plaintext[i] ^ obf_key[i % 32];
    }
    res[len] = '\0';
    return res;
}
```
If we do this, the password is not in plaintext memory. We can then store `obfuscate(password)` in the hash table, and when we retrieve it, we `obfuscate()` it again (since XOR is symmetric).
Wait, if it has `\0` in the middle due to XOR, `strlen()` will fail!
Ah, XORing a character might produce `\0` if the character equals the key.
To avoid `\0`, we can do base64 encoding after encryption, or we can store a struct with length, or we can just use `g_base64_encode(plaintext)`. But base64 is still plaintext (trivially readable).
What if we use a GLib secure memory string? GLib doesn't have it.

Is the expected solution to use `gnc_keyring_set_password` and let it be stored persistently?
Or is it to use `gnc_keyring` but with the session schema?
Wait, GnuCash DOES use `gnome-keyring` and `libsecret` which are designed for this.
Does GnuCash have any other password caching?
Let's `grep "memory cache" gnucash/` or similar. No.
Let's see the PRs or commits from the project. I cannot search github here directly unless I search via google.
