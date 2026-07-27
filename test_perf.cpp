#include <iostream>
#include <chrono>
#include <glib.h>

struct Transaction {
    GList *splits;
};

struct Split {
    void* parent;
};

Split* xaccSplitClone(Split* s) {
    return new Split();
}

int main() {
    int num_splits = 10000;
    Transaction from_txn;
    from_txn.splits = nullptr;
    for (int i = 0; i < num_splits; ++i) {
        from_txn.splits = g_list_append(from_txn.splits, new Split());
    }

    Transaction to_txn;
    to_txn.splits = nullptr;

    auto start = std::chrono::high_resolution_clock::now();

    GList* node;
    for (node = from_txn.splits; node; node = node->next)
    {
        Split *split = xaccSplitClone (static_cast<Split*>(node->data));
        split->parent = &to_txn;
        to_txn.splits = g_list_append (to_txn.splits, split);
    }

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::milli> ms = end - start;
    std::cout << "Original took " << ms.count() << " ms" << std::endl;

    to_txn.splits = nullptr;

    start = std::chrono::high_resolution_clock::now();
    for (node = from_txn.splits; node; node = node->next)
    {
        Split *split = xaccSplitClone (static_cast<Split*>(node->data));
        split->parent = &to_txn;
        to_txn.splits = g_list_prepend(to_txn.splits, split);
    }
    to_txn.splits = g_list_reverse(to_txn.splits);

    end = std::chrono::high_resolution_clock::now();
    ms = end - start;
    std::cout << "Optimized took " << ms.count() << " ms" << std::endl;


    return 0;
}
