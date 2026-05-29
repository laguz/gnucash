import sys

# the jobs lists are GList* containing GncJob*
# we can iterate them and use guid_equal or gncJobEqual.
# using guids directly is safer against infinite recursion and standard practice.

# the memory mentioned:
# In GnuCash C/C++ development, when comparing lists of child QOF instances (like GncJob inside GncCustomer or GncVendor) for parent equality, use shallow GUID comparisons (guid_equal(qof_instance_get_guid(...))) instead of deep equality functions (like gncJobEqual) to prevent infinite recursion loops caused by circular parent-child references.

print("Use guid_equal!!!")
