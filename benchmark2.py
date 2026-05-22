import sys
import time

def get_all_sub_accounts_new(account, prefix=''):
    descendants = account.get_descendants()

    # We want to build the full name for each descendant.
    # To do this efficiently, we can build a parent-child mapping
    # or just look up the parent chain for each descendant.
    # But get_descendants() might not be sorted.
    pass
