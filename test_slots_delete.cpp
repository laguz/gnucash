#include <iostream>
#include <sstream>
#include <vector>

int main() {
    std::ostringstream sql;
    std::vector<std::string> guids = {"a", "b", "c"};
    sql << "DELETE FROM slots WHERE obj_guid IN (";
    for (size_t i = 0; i < guids.size(); ++i) {
        if (i > 0) sql << ", ";
        sql << "'" << guids[i] << "'";
    }
    sql << ")";
    std::cout << sql.str() << std::endl;
    return 0;
}
