#
# Set the locations of things for this project
#

SET(TRIBITS_PROJECT_ROOT "${CMAKE_CURRENT_LIST_DIR}/../../..")
SET(TriBITS_TRIBITS_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../tribits")

#
# Include the TriBITS file to get other modules included
#

INCLUDE("${CMAKE_CURRENT_LIST_DIR}/../../../tribits/ctest_driver/TribitsCTestDriverCore.cmake")

#
# Set the options specific to this build case
#

SET(COMM_TYPE SERIAL)
SET(BUILD_TYPE DEBUG)
SET(BUILD_DIR_NAME ${COMM_TYPE}_${BUILD_TYPE}_TravisCI)
#SET(CTEST_TEST_TIMEOUT 900)

SET_DEFAULT_AND_FROM_ENV( CTEST_BUILD_FLAGS "-j1 -i" )

SET_DEFAULT_AND_FROM_ENV( CTEST_PARALLEL_LEVEL "1" )

SET( EXTRA_CONFIGURE_OPTIONS
  "-DBUILD_SHARED_LIBS:BOOL=ON"
  "-DCMAKE_BUILD_TYPE=DEBUG"
  "-DCMAKE_C_COMPILER=gcc"
  "-DCMAKE_CXX_COMPILER=g++"
  "-DCMAKE_Fortran_COMPILER=gfortran"
  "-DTriBITS_ENABLE_Fortran=ON"
  "-DTriBITS_TRACE_ADD_TEST=ON"
  "-DTriBITS_HOSTNAME=travis-ci-server-linux"
  )

SET(CTEST_TEST_TYPE Continuous)

#
# Run the CTest driver and submit to CDash
#

TRIBITS_CTEST_DRIVER()
