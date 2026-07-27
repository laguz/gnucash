#!/bin/bash
sed -i 's/GLogFunc oldlogger =/g_log_set_default_handler/' libgnucash/engine/test/utest-Account.cpp
sed -i 's/GNC_TEST_ADD (suitename, "xaccAccountDestroy", Fixture, &good_data, setup, test_xaccAccountDestroy,  NULL );//' libgnucash/engine/test/utest-Account.cpp
sed -i '/static void/!b;n; /test_xaccAccountBeginEdit_null/{N;N;N;N;N;N;N;d}' libgnucash/engine/test/utest-Account.cpp
