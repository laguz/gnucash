import re

with open('libgnucash/engine/Transaction.cpp', 'r') as f:
    content = f.read()

# Replace the specific loop
old_loop = """    for (node = from->splits; node; node = node->next)
    {
        split = xaccSplitCloneNoKvp(GNC_SPLIT(node->data));
        split->parent = to;
        to->splits = g_list_append (to->splits, split);
    }"""

new_loop = """    for (node = from->splits; node; node = node->next)
    {
        split = xaccSplitCloneNoKvp(GNC_SPLIT(node->data));
        split->parent = to;
        to->splits = g_list_prepend (to->splits, split);
    }
    to->splits = g_list_reverse(to->splits);"""

if old_loop in content:
    content = content.replace(old_loop, new_loop)
    with open('libgnucash/engine/Transaction.cpp', 'w') as f:
        f.write(content)
    print("Replaced!")
else:
    print("Not found")
