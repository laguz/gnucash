#!/bin/bash
mkdir -p build
cd build
cmake -GNinja ..
ninja gnucash test-load-gnucash-plugins
ctest -R test-load-gnucash-plugins -V
