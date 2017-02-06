################################################################################
#                                                                              #
#              TriBITS Project and Package CMakeLists.txt File                 #
#                                                                              #
################################################################################

IF (NOT TRIBITS_PROCESSING_PACKAGE)
  # This CMakeLists.txt file is being processed as the TriBITS projects's base
  # CMakeLists.txt file!  (See comments at bottom of this file.)
  CMAKE_MINIMUM_REQUIRED(VERSION 2.8.11 FATAL_ERROR)
  INCLUDE("${CMAKE_CURRENT_SOURCE_DIR}/ProjectName.cmake")
  PROJECT(${PROJECT_NAME} NONE)
  SET(${PROJECT_NAME}_TRIBITS_DIR "${CMAKE_CURRENT_SOURCE_DIR}/tribits" CACHE PATH "")
  INCLUDE("${${PROJECT_NAME}_TRIBITS_DIR}/TriBITS.cmake")
  SET(${PROJECT_NAME}_ENABLE_TESTS ON CACHE BOOL "Enable tests by default.")
  INCLUDE("${CMAKE_CURRENT_SOURCE_DIR}/cmake/AssertSameVersionFile.cmake")
  TRIBITS_PROJECT_ENABLE_ALL()
ELSE()
  # This CMakeLists.txt file is being processed as the TriBITS package file.
  TRIBITS_PACKAGE(TriBITS  DISABLE_CIRCULAR_REF_DETECTION_FAILURE)
  TRIBITS_ADD_TEST_DIRECTORIES(test)
  TRIBITS_PACKAGE_POSTPROCESS()
ENDIF()

# NOTE: In order to allow the `TriBITS/` directory to be both a TriBITS
# package (for inclusion in other TriBITS projects) and to be a TriBITS
# project itself, you only have to put in a simple if statement in this
# top-level CMakeLists.txt file.  That is all!  In fact, this `TriBiTS/`
# directory shows how the same directory can be used for a TriBITS package, a
# TriBITS repository, and a TriBITS project!
