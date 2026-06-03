#!/bin/bash
export GNC_UNINSTALLED=1
export GNC_BUILDDIR=/app/build
export PYTHONPATH=/app/build/bindings/python:/app/gnucash/python:/app/common/test-core:/app/bindings/python/tests:/app/bindings/python
python3 bindings/python/tests/test_book_lookup.py
