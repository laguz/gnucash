import sys
import os

with open("bindings/python/tests/test_change_tax_code.py", "r") as f:
    content = f.read()

# Replace get_descendants with get_children in test setup
content = content.replace("child.get_descendants.return_value = []", "child.get_children.return_value = []")
content = content.replace("grandchild.get_descendants.return_value = []", "grandchild.get_children.return_value = []")
content = content.replace("child1.get_descendants.return_value = []", "child1.get_children.return_value = []")
content = content.replace("child2.get_descendants.return_value = []", "child2.get_children.return_value = []")

content = content.replace("self.root_account.get_descendants.return_value =", "self.root_account.get_children.return_value =")
content = content.replace("child.get_descendants.return_value = [grandchild]", "child.get_children.return_value = [grandchild]")

with open("bindings/python/tests/test_change_tax_code.py", "w") as f:
    f.write(content)
