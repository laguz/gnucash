set(BI_IMPORT_TEST_INCLUDE_DIRS
  ${CMAKE_BINARY_DIR}/common # for config.h
  ${CMAKE_SOURCE_DIR}/gnucash/import-export/bi-import
  ${CMAKE_SOURCE_DIR}/common/test-core
  ${CMAKE_SOURCE_DIR}/libgnucash/engine
  ${CMAKE_SOURCE_DIR}/libgnucash/engine/test-core
  ${GUILE_INCLUDE_DIRS}
  ${GTEST_INCLUDE_DIR}
)

set(BI_IMPORT_TEST_LIBS gnc-bi-import gnc-test-engine test-core gtest)

gnc_add_test(test-bi-import-helper test-bi-import-helper.cpp
  BI_IMPORT_TEST_INCLUDE_DIRS BI_IMPORT_TEST_LIBS
)
