Let's see if we can use g_string_new instead? No, g_string is still in memory.
What about `gnc_keyring`?
If AQBanking provides `token` for a password and asks us to cache it, we could save it to GNOME keyring using `gnc_keyring_set_password`.
Let's check `getpassword_cb` to see how it's used.
