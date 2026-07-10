set(GNUCASH_TEST_INCLUDE_DIRS
  ${CMAKE_BINARY_DIR}/common # for config.h
  ${CMAKE_SOURCE_DIR}/common/test-core
  ${CMAKE_SOURCE_DIR}/gnucash/
  ${CMAKE_SOURCE_DIR}/gnucash/gnome/
  ${CMAKE_SOURCE_DIR}/gnucash/gnome-utils/
  ${CMAKE_SOURCE_DIR}/gnucash/import-export/bi-import/
  ${CMAKE_SOURCE_DIR}/gnucash/import-export/csv-exp/
  ${CMAKE_SOURCE_DIR}/gnucash/import-export/csv-imp/
  ${CMAKE_SOURCE_DIR}/gnucash/import-export/customer-import/
  ${CMAKE_SOURCE_DIR}/gnucash/import-export/qif-imp/
  ${CMAKE_SOURCE_DIR}/gnucash/import-export/log-replay/
  ${CMAKE_SOURCE_DIR}/libgnucash/engine
  ${GUILE_INCLUDE_DIRS}
)

set(GNUCASH_TEST_LIBS
        gnc-gnome
        gnc-test-engine
        test-core
        gtest
        ${GUILE_LDFLAGS})

gnc_add_test(test-load-gnucash-plugins test-load-gnucash-plugins.cpp GNUCASH_TEST_INCLUDE_DIRS GNUCASH_TEST_LIBS)

set_dist_list(test_gnucash_DIST
  CMakeLists.txt
  test-load-gnucash-plugins.cpp
)
