###############################################################
# test a passing call order, will be run by default turn this 
# off when you turn on one of the other sections
###############################################################
IF(NOT subpackageA_turn_off_passing_call_order)
  #
  # A) Define the subpackage
  #

  TRIBITS_SUBPACKAGE(A)

  #
  # B) Set up subpackage-specific options
  #
  # Typically there are none or are few as most options are picked up from the
  # parent package's CMakeLists.txt file!
  
  #
  # C) Add the libraries, tests, and examples
  #

  INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR})
  TRIBITS_ADD_LIBRARY(pwswue_a
    SOURCES A.cpp
    HEADERS A.hpp
    NOINSTALLHEADERS 
  )

  TRIBITS_ADD_TEST_DIRECTORIES(tests)

  #
  # D) Do standard post processing
  #

  TRIBITS_SUBPACKAGE_POSTPROCESS()
ENDIF()


###############################################################
# Add a library after the postprocess call
###############################################################
IF(subPackageA_ADD_LIBRARY_AFTER_POST_PROCESS)
  MESSAGE("Adding library in subpackage after post process")
  
  TRIBITS_SUBPACKAGE(A)
  TRIBITS_SUBPACKAGE_POSTPROCESS()
  TRIBITS_ADD_LIBRARY(lib_after_post_process
    SOURCES A.cpp
    HEADERS A.hpp
    NOINSTALLHEADERS 
  )
ENDIF()


###############################################################
# Add an executable after the postprocess call
###############################################################
IF(subPackageA_ADD_EXECUTABLE_AFTER_POST_PROCESS)
  MESSAGE("Adding executable in subpackage after post process")

  TRIBITS_SUBPACKAGE(A)
  TRIBITS_SUBPACKAGE_POSTPROCESS()
  TRIBITS_ADD_EXECUTABLE(exe_after_post_process
    SOURCES A.cpp
    HEADERS A.hpp
  )
ENDIF()


###############################################################
# no subpackage call before adding librbary
###############################################################
IF(subPackageA_add_lib_no_PREPROCESS)
  TRIBITS_ADD_LIBRARY(lib_after_post_process
    SOURCES A.cpp
    HEADERS A.hpp
    NOINSTALLHEADERS 
  )
  TRIBITS_SUBPACKAGE_POSTPROCESS()
ENDIF()


###############################################################
# no subpackage call before adding executable
###############################################################
IF(subPackageA_add_exe_no_PREPROCESS)
  TRIBITS_ADD_EXECUTABLE(exe_after_post_process
    SOURCES A.cpp
    HEADERS A.hpp
  )
  TRIBITS_SUBPACKAGE_POSTPROCESS()
ENDIF()


###############################################################
# Multiple calls to SUBPACKAGE
###############################################################
IF(subPackageA_DOUBLE_SUBPACKAGE_INIT)
  TRIBITS_SUBPACKAGE(A)
  TRIBITS_SUBPACKAGE(A)
  TRIBITS_SUBPACKAGE_POSTPROCESS()
ENDIF()


###############################################################
# Multiple calls to SUBPACKAGE_POSTPROCESS
###############################################################
IF(subPAckageA_DOUBLE_SUBPACKAGE_POSTPROCESS)
  TRIBITS_SUBPACKAGE(A)
  TRIBITS_SUBPACKAGE_POSTPROCESS()
  TRIBITS_SUBPACKAGE_POSTPROCESS()
ENDIF()


###############################################################
# no call to SUBPACKAGE before SUBPACKAGE_POSTPROCESS
###############################################################
IF(subPackageA_no_SUBPACKAGE_before_POSTPROCESS)
  TRIBITS_SUBPACKAGE_POSTPROCESS()
ENDIF()


###############################################################
# call PACKAGE from a subpackage file
###############################################################
IF(subPackageA_call_PACKAGE)
  TRIBITS_PACKAGE(A)
ENDIF()

###############################################################
# call PACKAGE_DECL from a subpackage file
###############################################################
IF(subPackageA_call_PACKAGE_DECL)
  TRIBITS_PACKAGE_DECL(A)
ENDIF()

###############################################################
# call PACKAGE_DEF from a subpackage file
###############################################################
IF(subPackageA_call_PACKAGE_DEF)
  TRIBITS_PACKAGE_DEF(A)
ENDIF()


###############################################################
# call PACKAGE_POSTPROCESS from a subpackage file
###############################################################
IF(subPackageA_call_PACKAGE_POSTPROCESS)
  TRIBITS_SUBPACKAGE(A)
  TRIBITS_PACKAGE_POSTPROCESS()
ENDIF()


###############################################################
# call PROCESS_SUBPACKAGES from a subpackage file
###############################################################
IF(subPackageA_call_PROCESS_SUBPACKAGES)
  TRIBITS_SUBPACKAGE(A)
  TRIBITS_PROCESS_SUBPACKAGES()
  TRIBITS_SUBPACKAGE_POSTPROCESS()
ENDIF()

###############################################################
# ADD_TEST_DIRECTORIES without SUBPACKAGE call
###############################################################
IF(subPackageA_call_ADD_TEST_DIRECTORY_without_SUBPACKAGE)
  TRIBITS_ADD_TEST_DIRECTORIES(tests)
  TRIBITS_SUBPACKAGE_POSTPROCESS()
ENDIF()

###############################################################
# ADD_TEST_DIRECTORIES after POSTPROCESS
###############################################################
IF(subPackageA_call_ADD_TEST_DIRECTORY_after_POSTPROCESS)
  TRIBITS_SUBPACKAGE(A)
  TRIBITS_SUBPACKAGE_POSTPROCESS()
  TRIBITS_ADD_TEST_DIRECTORIES(tests)
ENDIF()

###############################################################
# ADD_EXAMPLE_DIRECTORIES without SUBPACKAGE call
###############################################################
IF(subPackageA_call_ADD_EXAMPLE_DIRECTORY_without_SUBPACKAGE)
  TRIBITS_ADD_EXAMPLE_DIRECTORIES(tests)
  TRIBITS_SUBPACKAGE_POSTPROCESS()
ENDIF()

###############################################################
# ADD_EXAMPLE_DIRECTORIES after POSTPROCESS
###############################################################
IF(subPackageA_call_ADD_EXAMPLE_DIRECTORY_after_POSTPROCESS)
  TRIBITS_SUBPACKAGE(A)
  TRIBITS_SUBPACKAGE_POSTPROCESS()
  TRIBITS_ADD_EXAMPLE_DIRECTORIES(tests)
ENDIF()
