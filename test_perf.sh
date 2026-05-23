export GNC_UNINSTALLED=1
export GNC_BUILDDIR=$(pwd)/build
export PYTHONPATH=$GNC_BUILDDIR/lib/python3.12/site-packages:$GNC_BUILDDIR/common/test-core
python3 test_perf.py
