set(test_core_app_SOURCES
  test-core-app.cpp
  ../gnucash-core-app.cpp
  ../gnucash-commands.cpp
)

set(test_core_app_INCLUDE_DIRS
  ${CMAKE_BINARY_DIR}/common
  ${CMAKE_SOURCE_DIR}/gnucash
  ${GUILE_INCLUDE_DIRS}
)

set(test_core_app_LIBS
  gtest
  gnc-app-utils
  gnc-engine
  gnc-core-utils
  gnucash-guile
  gnc-report
  ${GUILE_LDFLAGS} PkgConfig::GLIB2
  ${Boost_LIBRARIES}
)

gnc_add_test(test-core-app
  "${test_core_app_SOURCES}"
  test_core_app_INCLUDE_DIRS
  test_core_app_LIBS
)
