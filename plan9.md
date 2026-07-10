Wait, actually! If I look at libsecret / GNOME Keyring again.
Why NOT use `gnc_keyring_set_password`?
If AQBanking's "remember-pin" is turned on, storing it in the keychain IS the standard GNOME/GnuCash way to remember passwords!
In fact, the other passwords (like database passwords) are stored using `gnc_keyring_set_password`!
If the user sets "Remember PIN", isn't it better to store it in the secure keychain?
Let's look at what `gnc_keyring_set_password` requires.
`access_method` = "aqbanking"
`server` = token
`port` = 0
`service` = "pin"
`user` = token (since aqbanking tokens are unique per user/account usually)
If we use `gnc_keyring`, it will be stored persistently. If the user doesn't want it persistently, they uncheck "Remember PIN".
Wait, the preference description explicitly says:
"If active, the PIN for HBCI/AqBanking actions will be remembered in memory during a session. Otherwise it will have to be entered again each time during a session when it is needed."
It VERY explicitly says "in memory during a session", and "entered again each time during a session" if inactive. So the intent of this checkbox is ONLY for the session.

If I must use obfuscation in memory:
```c
typedef struct {
    gsize len;
    guint8 data[];
} ObfuscatedPassword;

static ObfuscatedPassword* obfuscate_password(const gchar* password) {
    if (!password) return NULL;
    init_session_key();
    gsize len = strlen(password);
    ObfuscatedPassword* obf = g_malloc(sizeof(ObfuscatedPassword) + len);
    obf->len = len;
    for(gsize i = 0; i < len; i++) {
        obf->data[i] = password[i] ^ session_key[i % 32];
    }
    return obf;
}

static gchar* deobfuscate_password(const ObfuscatedPassword* obf) {
    if (!obf) return NULL;
    gchar* pwd = g_malloc(obf->len + 1);
    for(gsize i = 0; i < obf->len; i++) {
        pwd[i] = obf->data[i] ^ session_key[i % 32];
    }
    pwd[obf->len] = '\0';
    return pwd;
}

static void free_obfuscated_password(ObfuscatedPassword* obf) {
    if (!obf) return;
    memset(obf->data, 0, obf->len);
    obf->len = 0;
    g_free(obf);
}
```
Then use `(GDestroyNotify) free_obfuscated_password` in the hash table!
This perfectly solves the "plaintext memory caches" issue while preserving the session-only "in memory" behavior!
Let's verify if `g_hash_table_new_full` with `free_obfuscated_password` works. Yes!
And we need to change where the hash table is accessed:
```c
// Storing
ObfuscatedPassword *obf = obfuscate_password(password);
g_hash_table_insert(gui->passwords, g_strdup(token), obf);

// Retrieving
gpointer p_var;
if (g_hash_table_lookup_extended(gui->passwords, token, NULL, &p_var)) {
    ObfuscatedPassword *obf = (ObfuscatedPassword*) p_var;
    gchar *decrypted = deobfuscate_password(obf);
    strncpy(buffer, decrypted, max_len);
    buffer[max_len-1] = '\0';
    erase_password(decrypted); // We should wipe the decrypted copy after copying it!
    LEAVE("chose remembered password");
    return 0;
}
```
Wait, we need to check if we wipe `password` safely.
```c
    erase_password(decrypted);
```
Yes! Because `decrypted` is allocated by `g_malloc`, we must free it. `erase_password` does `memset` then `g_free`.
