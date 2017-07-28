# TRIBITS_PACKAGE() will be called by default
IF(NOT ${PACKAGE_NAME}_SKIP_TRIBITS_PACKAGE_INIT)
  TRIBITS_PACKAGE(PkgWithUserErrors)
ENDIF()

INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR})

# Not added by defult
IF(${PACKAGE_NAME}_ADD_LIBRARY_BEFORE_POST_PROCESS)
  MESSAGE("building library")
  TRIBITS_ADD_LIBRARY(
    pkgwithusererrors
    HEADERS PkgWithUserErrorsLib.hpp
    SOURCES PkgWithUserErrorsLib.cpp
    )
ENDIF()

# Not added by defult
IF(${PACKAGE_NAME}_ADD_EXECUTABLE_BEFORE_POST_PROCESS)
  MESSAGE("building exectuable")
  TRIBITS_ADD_EXECUTABLE(
    usererrorexec
    SOURCES  PkgWithUserErrorsEX.cpp
    )
ENDIF()

IF(NOT ${PACKAGE_NAME}_SKIP_PACKAGE_TESTS)
  TRIBITS_ADD_TEST_DIRECTORIES(test)
ENDIF()

# TRIBITS_PACKAGE_POSTPROCESS() will be called by default
IF (NOT ${PACKAGE_NAME}_SKIP_PACKAGE_POST_PROCESS)
  TRIBITS_PACKAGE_POSTPROCESS()
ENDIF()

# Not added by defult
IF (${PACKAGE_NAME}_ADD_LIBRARY_AFTER_POST_PROCESS)
  TRIBITS_ADD_LIBRARY(
    pkgwithusererrors2
    HEADERS PkgWithUserErrorsLib.hpp
    SOURCES PkgWithUserErrorsLib.cpp
    )
ENDIF()

# Not added by defult
IF(${PACKAGE_NAME}_ADD_EXECUTABLE_AFTER_POST_PROCESS)
  TRIBITS_ADD_EXECUTABLE(
    usererrorexec
    SOURCES  PkgWithUserErrorsEX.cpp
    )
ENDIF()
