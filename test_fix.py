import re

with open("libgnucash/backend/sql/gnc-tax-table-sql.cpp", "r") as f:
    content = f.read()

print("Found:")
print(content[content.find("buf = g_strdup_printf"):content.find("buf = g_strdup_printf")+150])

print("\n\nDesired fix:")
print("""    auto sql = std::string{"SELECT * FROM "} + TTENTRIES_TABLE_NAME;
    auto stmt = sql_be->create_statement_from_sql(sql);
    PairVec col_values{{"taxtable", sql_be->quote_string(guid_buf)}};
    stmt->add_where_cond(GNC_ID_TAXTABLE, col_values);""")
