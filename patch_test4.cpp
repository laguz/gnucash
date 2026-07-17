#include <iostream>
#include <sstream>
#include <vector>

std::string format_guids(const std::vector<std::string>& guids) {
    std::ostringstream sql;
    sql << "IN (";
    for (size_t i = 0; i < guids.size(); ++i) {
        if (i > 0) sql << ", ";
        sql << "'" << guids[i] << "'";
    }
    sql << ")";
    return sql.str();
}

int main() {
    std::vector<std::string> guids = {"a", "b", "c"};
    std::cout << format_guids(guids) << std::endl;
    return 0;
}
