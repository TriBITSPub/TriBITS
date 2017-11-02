###############################################################
# test a passing call order, will be run by default turn this 
# off when you turn on one of the other sections
###############################################################
IF(NOT ${PACKAGE_NAME}_turn_off_passing_call_order)
  TRIBITS_PACKAGE(PkgWithUserErrors)
  INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR})
  TRIBITS_ADD_LIBRARY(
    pkgwithusererrors
    HEADERS PkgWithUserErrorsLib.hpp
    SOURCES PkgWithUserErrorsLib.cpp
    )
  TRIBITS_ADD_TEST_DIRECTORIES(test)
  TRIBITS_PACKAGE_POSTPROCESS()
ENDIF()


###############################################################
# User forgets to call TRIBITS_PACKAGE_POSTPROCESS 
###############################################################
IF(${PACKAGE_NAME}_no_POSTPROCESS_call)
  MESSAGE("User forgets to call TRIBITS_PACKAGE_POSTPROCESS")
  TRIBITS_PACKAGE(PkgWithUserErrors)
  INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR})
  TRIBITS_ADD_LIBRARY(
    pkgwithusererrors
    HEADERS PkgWithUserErrorsLib.hpp
    SOURCES PkgWithUserErrorsLib.cpp
    )
  TRIBITS_ADD_TEST_DIRECTORIES(test)
ENDIF()


###############################################################
# User forgets to call TRIBITS_PACKAGE before adding lib
###############################################################
IF(${PACKAGE_NAME}_ADD_LIBRARY_with_no_package_init)
  MESSAGE("")
  INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR})
  TRIBITS_ADD_LIBRARY(
    pkgwithusererrors
    HEADERS PkgWithUserErrorsLib.hpp
    SOURCES PkgWithUserErrorsLib.cpp
    )
  TRIBITS_ADD_TEST_DIRECTORIES(test)
  TRIBITS_PACKAGE_POSTPROCESS()
ENDIF()


###############################################################
# User forgets to call TRIBITS_PACKAGE before adding exe
###############################################################
IF(${PACKAGE_NAME}_ADD_EXECUTABLE_with_no_package_init)
  MESSAGE("User forgets to call TRIBITS_PACKAGE before adding exe")
  INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR})
  TRIBITS_ADD_EXECUTABLE(
    usererrorexec
    SOURCES  PkgWithUserErrorsEX.cpp
  )
  TRIBITS_ADD_TEST_DIRECTORIES(test)
  TRIBITS_PACKAGE_POSTPROCESS()
ENDIF()


###############################################################
# no call to TRIBITS_PACKAGE before call to POSTPROCESS
###############################################################
IF(${PACKAGE_NAME}_POSTPROCESS_with_no_package_init)
  MESSAGE("no call to TRIBITS_PACKAGE before call to POSTPROCESS")
  TRIBITS_PACKAGE_POSTPROCESS()
ENDIF()


###############################################################
# multiple calls to TRIBITS_PACKAGE
###############################################################
IF(${PACKAGE_NAME}_multiple_calls_to_PACKAGE)
  MESSAGE("multiple calls to TRIBITS_PACKAGE")
  TRIBITS_PACKAGE(PkgWithUserErrors)
  TRIBITS_PACKAGE(PkgWithUserErrors)
  TRIBITS_PACKAGE_POSTPROCESS()
ENDIF()


###############################################################
# adding a library after POSTPROCESS
###############################################################
IF(${PACKAGE_NAME}_ADD_LIBRARY_after_POSTPROCESS)
  MESSAGE("adding a library after POSTPROCESS")
  TRIBITS_PACKAGE(PkgWithUserErrors)
  INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR})
  TRIBITS_PACKAGE_POSTPROCESS()
  TRIBITS_ADD_LIBRARY(
    pkgwithusererrors
    HEADERS PkgWithUserErrorsLib.hpp
    SOURCES PkgWithUserErrorsLib.cpp
    )
ENDIF()


###############################################################
# adding an exe after POSTPROCESS
###############################################################
IF(${PACKAGE_NAME}_ADD_EXECUTABLE_after_POSTPROCESS)
  MESSAGE("adding an exe after POSTPROCESS")
  TRIBITS_PACKAGE(PkgWithUserErrors)
  INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR})
  TRIBITS_PACKAGE_POSTPROCESS()
  TRIBITS_ADD_EXECUTABLE(
    usererrorexec
    SOURCES  PkgWithUserErrorsEX.cpp
  )
ENDIF()


###############################################################
# multiple calls to POSTPROCESS
###############################################################
IF(${PACKAGE_NAME}_multiple_calls_to_POSTPROCESS)
  MESSAGE("multiple calls to POSTPROCESS")
  TRIBITS_PACKAGE(PkgWithUserErrors)
  TRIBITS_PACKAGE_POSTPROCESS()
  TRIBITS_PACKAGE_POSTPROCESS()
ENDIF()


###############################################################
# unparsed arguments in ADD_LIBRARY
###############################################################
IF(${PACKAGE_NAME}_UNPARSED_ARGS_ADD_LIBRARY)
  MESSAGE("unparsed arguments in ADD_LIBRARY")
  TRIBITS_PACKAGE(PkgWithUserErrors)
  INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR})
  MESSAGE("building library")
  TRIBITS_ADD_LIBRARY(
    pkgwithusererrors
    this_shouldnt_be_here
    HEADERS PkgWithUserErrorsLib.hpp
    SOURCES PkgWithUserErrorsLib.cpp
    )
  TRIBITS_ADD_TEST_DIRECTORIES(test)
  TRIBITS_PACKAGE_POSTPROCESS()
ENDIF()


###############################################################
# unparsed arguments in ADD_EXECUTABLE
###############################################################
IF(${PACKAGE_NAME}_UNPARSED_ARGS_ADD_EXECUTABLE)
  MESSAGE("unparsed arguments in ADD_EXECUTABLE")
  TRIBITS_PACKAGE(PkgWithUserErrors)
  INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR})
  MESSAGE("building exectuable")
  TRIBITS_ADD_EXECUTABLE(
    usererrorexec
    misspelled_argument
    SOURCES  PkgWithUserErrorsEX.cpp
    SPORCOOS some_file.cpp
  )
  TRIBITS_ADD_TEST_DIRECTORIES(test)
  TRIBITS_PACKAGE_POSTPROCESS()
ENDIF()
