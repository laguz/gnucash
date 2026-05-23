import sys

with open("bindings/python/example_scripts/gnc_convenience.py", "r") as f:
    content = f.read()

# Replace find_account recursive call
old_find_account = """def find_account(account,name,account_list=None):
  \"\"\"Recursively searches full names of account and descendents

  returns a list of accounts which contain name.

  options:

  account:      account to start search in.
  name:         name to search for.
  account_list: (optional) list to append accounts to.

  \"\"\"

  if not account_list:
    account_list=[]

  for child in account.get_children():
    if type(child) != Account:
      child=Account(instance=child)
    account_list=find_account(child,name,account_list)

  account_name=account.GetName()
  if name in account_name:
    account_list.append(account)

  return account_list"""

new_find_account = """def find_account(account,name,account_list=None):
  \"\"\"Searches full names of account and descendents

  returns a list of accounts which contain name.

  options:

  account:      account to start search in.
  name:         name to search for.
  account_list: (optional) list to append accounts to.

  \"\"\"

  if not account_list:
    account_list=[]

  account_name=account.GetName()
  if name in account_name:
    account_list.append(account)

  for child in account.get_descendants():
    if type(child) != Account:
      child=Account(instance=child)
    account_name=child.GetName()
    if name in account_name:
      account_list.append(child)

  return account_list"""

content = content.replace(old_find_account, new_find_account)

# Replace find_split_recursive recursive call
old_find_split_recursive = """def find_split_recursive(account, search_string):
  \"\"\"Searches account and descendants for Splits containing search_string

  returns a list of splits that have search_string as part of
  memo or
  description of parent transaction.

  options:

  account:        Account to search in.
  search_string:  String to search for.

  \"\"\"

  rlist = []
  child_account_splits = []

  # Get all splits in descendants
  for child in account.get_children():
      if type(child) != Account:
          child = Account(instance=child)
      childsplits = find_split_recursive(child, search_string)
      for split in childsplits:
          if type(split) != Split:
              split = Split(instance=split)
      child_account_splits += childsplits

  # Get all splits in account
  splits=account.GetSplitList()
  for split in splits:
      if type(split) != Split:
          split = Split(instance=split)
  basic_account_splits=find_split(splits,search_string)

  rlist=child_account_splits+basic_account_splits
  return rlist"""

new_find_split_recursive = """def find_split_recursive(account, search_string):
  \"\"\"Searches account and descendants for Splits containing search_string

  returns a list of splits that have search_string as part of
  memo or
  description of parent transaction.

  options:

  account:        Account to search in.
  search_string:  String to search for.

  \"\"\"

  rlist = []
  child_account_splits = []

  # Get all splits in descendants
  for child in account.get_descendants():
      if type(child) != Account:
          child = Account(instance=child)
      splits = child.GetSplitList()
      for split in splits:
          if type(split) != Split:
              split = Split(instance=split)
      childsplits = find_split(splits, search_string)
      child_account_splits += childsplits

  # Get all splits in account
  splits=account.GetSplitList()
  for split in splits:
      if type(split) != Split:
          split = Split(instance=split)
  basic_account_splits=find_split(splits,search_string)

  rlist=child_account_splits+basic_account_splits
  return rlist"""

content = content.replace(old_find_split_recursive, new_find_split_recursive)

with open("bindings/python/example_scripts/gnc_convenience.py", "w") as f:
    f.write(content)
