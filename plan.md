Let's make a plan.

1. Create a simple XOR obfuscation wrapper in `gnc-gwen-gui.c` to ensure the memory cache is NOT a plaintext memory cache.
2. The XOR obfuscation wrapper will use a random session key generated during the first obfuscation call.
3. Update `enable_password_cache` to use a `free_obfuscated_password` function instead of `erase_password` for the hash table value destroy notify.
4. Update `getpassword_cb` to obfuscate the password when inserting it into the hash table, and deobfuscate it when extracting it.
5. Fix `erase_password` to use a `volatile char *` to ensure it isn't optimized out by the compiler, protecting memory that's about to be freed.
6. Compile the code using CMake/Ninja.
7. Run the tests.
8. Request code review.
