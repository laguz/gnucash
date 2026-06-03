
set(test_qif_import_SOURCES test-plugin-qif-import.c)

set(test_qif_import_INCLUDE_DIRS
  ${CMAKE_BINARY_DIR}/common
  ${CMAKE_SOURCE_DIR}/gnucash/import-export/qif-imp
  ${CMAKE_SOURCE_DIR}/common
  ${CMAKE_SOURCE_DIR}/gnucash/import-export
  ${CMAKE_SOURCE_DIR}/gnucash/gnome
  ${CMAKE_SOURCE_DIR}/gnucash/register/ledger-core
  ${CMAKE_SOURCE_DIR}/gnucash/register/register-gnome
  ${CMAKE_SOURCE_DIR}/gnucash/register/register-core
  ${CMAKE_SOURCE_DIR}/gnucash/gnome-utils
  ${CMAKE_SOURCE_DIR}/libgnucash/app-utils
  ${CMAKE_SOURCE_DIR}/libgnucash/engine
  ${CMAKE_SOURCE_DIR}/libgnucash/core-utils
  ${CMAKE_SOURCE_DIR}/libgnucash/gnc-module
)

set(test_qif_import_LIBS
  gnc-qif-import gnc-generic-import gnc-gnome gnc-gnome-utils
  gnc-ledger-core gnc-app-utils
  gnc-backend-xml-utils gnc-engine gnc-core-utils gnc-module gnucash-guile
)

gnc_add_test(test-qif-import
  "${test_qif_import_SOURCES}"
  test_qif_import_INCLUDE_DIRS
  test_qif_import_LIBS SRCDIR=${CMAKE_CURRENT_SOURCE_DIR})

set(scm_qifimp_test_with_srfi64_SOURCES
  test-qif-imp.scm
  test-qif-parse.scm
  test-qif-merge-groups.scm
  )

set (GUILE_DEPENDS
  scm-app-utils
  scm-engine
  scm-test-engine
  scm-core-utils
  scm-qif-import-2
)

if (HAVE_SRFI64)
  gnc_add_scheme_tests("${scm_qifimp_test_with_srfi64_SOURCES}")

  gnc_add_scheme_test_targets(scm-test-qif-imp-srfi64
    SOURCES "${scm_qifimp_test_with_srfi64_SOURCES}"
    OUTPUT_DIR "tests"
    DEPENDS "${GUILE_DEPENDS};scm-srfi64-extras")
  add_dependencies(check scm-qif-import-2 scm-qif-import)
endif()

set_dist_list(test_qif_import_DIST CMakeLists.txt
  ${test_qif_import_SOURCES}
  ${scm_qifimp_test_with_srfi64_SOURCES})
