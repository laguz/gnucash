#include <iostream>
#include <vector>

void test() {
    std::vector<int> a = {1, 2, 3};
    for (int v : a) {
        std::cout << v << std::endl;
    }
}
