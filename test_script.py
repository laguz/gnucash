import re
with open("gnucash/gtkbuilder/gnc-recurrence.glade") as f:
    print(f.read().find("same week"))
