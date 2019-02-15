
# Set the locations of things for this project
#

SET(TRIBITS_PROJECT_ROOT "${CMAKE_CURRENT_LIST_DIR}/../..")
SET(TriBITS_TRIBITS_DIR "${CMAKE_CURRENT_LIST_DIR}/../../tribits")

#
# Include the TriBITS file to get other modules included
#

INCLUDE("${CMAKE_CURRENT_LIST_DIR}/../../tribits/ctest_driver/TribitsCTestDriverCore.cmake")

#
# Define a caller for the TriBITS Project
#

MACRO(TRIBITS_PROJ_CTEST_DRIVER)
  SET_DEFAULT(TriBITS_REPOSITORY_LOCATION_DEFAULT
    "https://github.com/TriBITSPub/TriBITS.git")
  SET_DEFAULT(TriBITS_REPOSITORY_LOCATION_NIGHTLY_DEFAULT 
    "${TriBITS_REPOSITORY_LOCATION_DEFAULT}")
  PRINT_VAR(TriBITS_REPOSITORY_LOCATION_DEFAULT)
  TRIBITS_CTEST_DRIVER()
ENDMACRO()