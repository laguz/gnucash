with open("gnucash/register/ledger-core/split-register-model.c", "r") as f:
    content = f.read()

print("gnc_numeric_zero" in content)
