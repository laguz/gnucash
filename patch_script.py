import re

with open("libgnucash/engine/gncOwner.c", "r") as f:
    content = f.read()

# Replace the specific block
old_block = """/* XXX: Yea, this is broken, but it should work fine for Queries.
 * We're single-threaded, right?
 */
static GncOwner *
owner_from_lot (GNCLot *lot)
{
    static GncOwner owner;

    if (!lot) return NULL;
    if (gncOwnerGetOwnerFromLot (lot, &owner))
        return &owner;

    return NULL;
}"""

new_block = """static GncOwner *
owner_from_lot (GNCLot *lot)
{
    GncOwner *owner;

    if (!lot) return NULL;

    owner = gncOwnerNew();
    if (gncOwnerGetOwnerFromLot (lot, owner))
        return owner;

    gncOwnerFree(owner);
    return NULL;
}"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open("libgnucash/engine/gncOwner.c", "w") as f:
        f.write(content)
    print("Patch applied successfully.")
else:
    print("Old block not found.")
