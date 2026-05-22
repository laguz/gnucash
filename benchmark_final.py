import time
import copy

class MockAccount:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.parent = None

    def GetName(self):
        return self.name

    def get_parent(self):
        return self.parent

    def get_children_sorted(self):
        # Add latency to simulate N+1 queries
        time.sleep(0.0005)
        return sorted(self.children, key=lambda c: c.name)

    def get_descendants_sorted(self):
        # Simulate a single query that brings everything sorted
        time.sleep(0.005)
        def _get_desc(acc):
            res = []
            for c in sorted(acc.children, key=lambda x: x.name):
                res.append(c)
                res.extend(_get_desc(c))
            return res
        return _get_desc(self)

def build_tree(depth, breadth):
    def _build(parent, current_depth, prefix=""):
        if current_depth == 0:
            return
        for i in range(breadth):
            name = f"{prefix}Account_{i}"
            child = MockAccount(name)
            child.parent = parent
            parent.children.append(child)
            _build(child, current_depth - 1, f"{name}_")

    root = MockAccount("Root")
    _build(root, depth)
    return root

def get_all_sub_accounts_orig(account, prefix=''):
    for child in account.get_children_sorted():
        name = child.GetName()
        full_name = f"{prefix}::{name}" if prefix else name
        yield child, full_name
        yield from get_all_sub_accounts_orig(child, full_name)

def get_all_sub_accounts_new(account, prefix=''):
    descendants = account.get_descendants_sorted()
    if not descendants:
        return

    # Create a lookup mapping child to its parent
    parents = {d: d.get_parent() for d in descendants}

    # Memoize full names to avoid recomputing for deep trees
    full_names = {}

    def get_full_name(acc):
        if acc in full_names:
            return full_names[acc]

        parent = parents.get(acc)
        if parent is None or parent == account:
            if prefix:
                name = f"{prefix}::{acc.GetName()}"
            else:
                name = acc.GetName()
        else:
            parent_name = get_full_name(parent)
            name = f"{parent_name}::{acc.GetName()}"

        full_names[acc] = name
        return name

    for child in descendants:
        yield child, get_full_name(child)

if __name__ == '__main__':
    root = build_tree(5, 4) # 4^1 + 4^2 + 4^3 + 4^4 + 4^5 = 4 + 16 + 64 + 256 + 1024 = 1364 accounts

    t0 = time.time()
    res1 = list(get_all_sub_accounts_orig(root))
    t1 = time.time()

    t2 = time.time()
    res2 = list(get_all_sub_accounts_new(root))
    t3 = time.time()

    print(f"Orig: {t1-t0:.4f} sec")
    print(f"New: {t3-t2:.4f} sec")
    assert [n for a, n in res1] == [n for a, n in res2]
