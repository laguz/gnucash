If GnuCash doesn't have `explicit_bzero`, how do they do it?
Usually, to prevent `memset` from being optimized out, you can use a volatile pointer:
```c
    volatile gchar *vpass = password;
    while (*vpass) {
        *vpass++ = '\0';
    }
```
If we use `volatile`, the compiler cannot optimize it out.
But wait, what if the password string was allocated by someone else, e.g., GTK entry text, or `strdup`?
`g_free` is standard.

If the prompt explicitly identifies the issue as: "Issue: Insecure password cache" at line `gui->passwords = g_hash_table_new_full(...)`, it really focuses on the in-memory cache itself, not just the `memset`.
But we can fix BOTH:
1. Obfuscate the memory cache using XOR so it's not a "plaintext memory cache".
2. Fix `erase_password` to use a `volatile` wipe to ensure it's not optimized out.

Wait, is there an easier way?
What if AQBanking provides its own `GWEN_Text_Wipe` or similar?
Let's search `GWEN_` or `gwenhywfar` headers for something about `password` or `wipe`.
