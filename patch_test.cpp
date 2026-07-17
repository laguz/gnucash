#include <iostream>
#include <sstream>
int main() {
    std::ostringstream in_clause;
    in_clause << "test";
    std::cout << in_clause.str() << std::endl;
    return 0;
}
