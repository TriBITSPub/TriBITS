set(TRIBITS_DIR "" CACHE FILEPATH "Must be set on commandline!")

set(${PROJECT_NAME}_TRACE_ADD_TEST TRUE)
set(${PROJECT_NAME}_TRIBITS_DIR ${TRIBITS_DIR}) 
set(PACKAGE_NAME ${PROJECT_NAME})
set(${PACKAGE_NAME}_ENABLE_TESTS TRUE)
list(PREPEND CMAKE_MODULE_PATH ${TRIBITS_DIR}/core/test_support)
include(TribitsAddAdvancedTest)
include(CTest)
enable_testing()
