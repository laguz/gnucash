import sys
import time
from unittest.mock import MagicMock

# Create a mock tree
class MockAccount:
    def __init__(self, name, guid):
        self.name = name
        self.guid = guid
        self.children = []
        self.parent = None

    def GetName(self):
        return self.name

    def get_children_sorted(self):
        # Simulate query latency
        time.sleep(0.001)
        return sorted(self.children, key=lambda c: c.name)

    def get_parent(self):
        return self.parent

def build_mock_tree(depth, breadth):
    def _build(parent, current_depth, prefix=""):
        if current_depth == 0:
            return
        for i in range(breadth):
            name = f"{prefix}Account_{i}"
            child = MockAccount(name, name)
            child.parent = parent
            parent.children.append(child)
            _build(child, current_depth - 1, f"{name}_")

    root = MockAccount("Root", "root")
    _build(root, depth)
    return root

def get_all_sub_accounts_orig(account, prefix=''):
    for child in account.get_children_sorted():
        name = child.GetName()
        full_name = f"{prefix}::{name}" if prefix else name
        yield child, full_name
        yield from get_all_sub_accounts_orig(child, full_name)

def get_all_sub_accounts_new(account, prefix=''):
    # Fetch all descendants in one go (assuming account.get_descendants() exists and is fast)
    # Actually wait, how do we get all accounts from the book?
    pass

if __name__ == '__main__':
    root = build_mock_tree(4, 5) # 5^1 + 5^2 + 5^3 + 5^4 = 5 + 25 + 125 + 625 = 780 accounts

    t0 = time.time()
    res = list(get_all_sub_accounts_orig(root))
    t1 = time.time()
    print(f"Orig: {t1-t0:.4f} sec, count={len(res)}")
