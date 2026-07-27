#!/bin/bash
set -e
echo "Running baseline test..."
cd build
time ./bin/test-engine -p /engine/Transaction/xaccTransClone > /dev/null
