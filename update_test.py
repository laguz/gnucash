import sys
import re

with open('bindings/python/tests/test_export_account_totals.py', 'r') as f:
    content = f.read()

# We need to add get_descendants_sorted and get_parent support to the mock
new_content = content.replace(
    'account.get_children_sorted.return_value = children if children else []',
    """account.get_children_sorted.return_value = children if children else []

        # Build descendants list to mock get_descendants_sorted
        def get_descendants(acc):
            desc = []
            for c in acc.get_children_sorted():
                desc.append(c)
                desc.extend(get_descendants(c))
            return desc

        account.get_descendants_sorted.return_value = get_descendants(account)"""
)

# And we also need to mock get_parent()
new_content = new_content.replace(
    'account.GetName.return_value = name',
    """account.GetName.return_value = name
        account.get_parent.return_value = None"""
)

new_content = new_content.replace(
    'account.get_children_sorted.return_value = children if children else []',
    """account.get_children_sorted.return_value = children if children else []
        for child in (children or []):
            child.get_parent.return_value = account"""
)

with open('bindings/python/tests/test_export_account_totals.py', 'w') as f:
    f.write(new_content)
