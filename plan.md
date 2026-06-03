1. The function `gnc_split_register_get_type_value` is defined but not used anymore because we removed its usage in both `gnc_split_register_get_ddue_io_flags` and `gnc_split_register_get_due_date_entry`.
2. I need to remove the definition of `gnc_split_register_get_type_value`.

```c
<<<<<<< SEARCH
static char
gnc_split_register_get_type_value (SplitRegister* reg,
                                   VirtualLocation virt_loc)
{
    RecnCell* cell;

    cell = (RecnCell*)gnc_table_layout_get_cell (reg->table->layout, TYPE_CELL);
    if (!cell)
        return '\0';

    return gnc_recn_cell_get_flag (cell);
}

static const char*
gnc_split_register_get_due_date_entry (VirtualLocation virt_loc,
=======
static const char*
gnc_split_register_get_due_date_entry (VirtualLocation virt_loc,
>>>>>>> REPLACE
```
