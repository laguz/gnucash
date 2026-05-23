import sys
import time

try:
    from gnucash import Session, Account
    print("successfully imported gnucash!")
except ImportError as e:
    print(f"could not import gnucash: {e}")
    sys.exit(1)

print("creating session")
gnucash_session = Session("test_perf.gnucash", is_new=True)

book = gnucash_session.book
root = book.get_root_account()

# Create a deep and wide tree
print("creating tree")
def create_tree(parent, depth, width):
    if depth == 0:
        return
    for i in range(width):
        acc = Account(book)
        acc.SetName(f"Acc_{depth}_{i}")
        parent.append_child(acc)
        create_tree(acc, depth - 1, width)

create_tree(root, 5, 5) # 5^5 = 3125 accounts
print("tree created")

def test_recursive(account):
    count = 1
    for child in account.get_children():
        count += test_recursive(child)
    return count

def test_descendants(account):
    count = 1
    for child in account.get_descendants():
        count += 1
    return count

print("testing recursive")
start = time.time()
test_recursive(root)
end = time.time()
print(f"recursive took {end - start}s")

print("testing descendants")
start = time.time()
test_descendants(root)
end = time.time()
print(f"descendants took {end - start}s")

gnucash_session.end()
gnucash_session.destroy()
