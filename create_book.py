import sys
from gnucash import Session, SessionOpenMode, Account

session = Session("sqlite3:///tmp/test.gnucash", SessionOpenMode.SESSION_NEW_STORE)
book = session.book
root = book.get_root_account()

# Create a tree of accounts
def create_tree(parent, depth, breadth):
    if depth == 0:
        return
    for i in range(breadth):
        acc = Account(book)
        acc.SetName(f"Account_{depth}_{i}")
        parent.append_child(acc)
        create_tree(acc, depth - 1, breadth)

create_tree(root, 4, 6) # 6 + 36 + 216 + 1296 = 1554 accounts
session.save()
session.end()
print("Book created!")
