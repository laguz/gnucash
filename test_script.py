import sys

def get_all_sub_accounts_optimized(root_account, prefix=''):
    descendants = root_account.get_descendants()

    # We need to build the hierarchy and yield sorted.
    # What if we build an in-memory tree first?
    pass
