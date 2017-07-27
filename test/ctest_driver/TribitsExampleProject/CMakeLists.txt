# @HEADER
# ************************************************************************
#
#            TriBITS: Tribal Build, Integrate, and Test System
#                    Copyright 2013 Sandia Corporation
#
# Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
# the U.S. Government retains certain rights in this software.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the Corporation nor the names of the
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY SANDIA CORPORATION "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL SANDIA CORPORATION OR THE
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# ************************************************************************
# @HEADER


###############################################################################
#
# Strong automated testing of TribitsCTestDriverCore.cmake and
# 'dashboard' target using real TribitsExampleProject.
#
# The tests in this CMakeLists.txt file use the TribitsExampleProject to do
# real testing of TribitsCTestDriverCore.cmake using real CTest -S script
# functions and can submit to a CDash site.  By default, these tests don't
# submit to CDash.  To get them to submit to CDash, you must configure this
# TriBITS project with::
#
#   -D${PACKAGE_NAME}_CTEST_DRIVER_SUBMIT_TO=<site-name>
#
# where ``<cite-name>`` is one of the following values:
#
# * Empty "" (the default)
#
# * "MY_CDASH" (submits to the default TribitsExProj project site on
#   my.cdash.org)
#
# * "TRILINOS_CDASH" (submits to TribitsExProj project on
#   testing.sandia.gov/cdash/)
#
# * "EXP_CDASH" (submits to TribitsExProj on exp.cdash.org)
#
# In addition, tests can also be added to test coverage testing and memory
# testing.
#
# To enable the coverage testing tests (which assumes gcov and GCC), use:
#
#   -D${PACKAGE_NAME}_CTEST_DRIVER_COVERAGE_TESTS=ON
#
# To enable the memory testing tests (which assumes valgrind is set up to be
# used), use:
#
#   -D${PACKAGE_NAME}_ENABLE_CTEST_DRIVER_MEMORY_TESTS=ON
#
###############################################################################

SET(${PACKAGE_NAME}_CTEST_DRIVER_SUBMIT_TO ""
  CACHE STRING
  "Determines where CTestDriver test results are submitted to CDash (chose '' (nowhere), 'MY_CDASH', 'TRILINOS_CDASH', or 'EXP_CDASH'"
  )

SET(${PACKAGE_NAME}_CTEST_DRIVER_COVERAGE_TESTS OFF
  CACHE BOOL
  "Determine if coverage CTestDriver tests are run (requires gcov on local system)"
  )

SET(${PACKAGE_NAME}_CTEST_DRIVER_MEMORY_TESTS OFF
  CACHE BOOL
  "Determine if memory CTestDriver tests are run (requires valgrind on local system)"
  )

#
# Set up common vars/args for all direct CTest Driver tests
#

SET(TribitsExProj_DIR "${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject")

SET(PBP_COMMON_ENV_ARGS
  # Set back to default
  TribitsExProj_PACKAGES=
  CTEST_EXPLICITLY_ENABLE_IMPLICITLY_ENABLED_PACKAGES=
  CTEST_ENABLE_MODIFIED_PACKAGES_ONLY=OFF
  TribitsExProj_PRE_REPOSITORIES=
  TribitsExProj_EXTRA_REPOSITORIES=
  # Other args
  TribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
  TribitsExProj_EXTRAREPOS_FILE=NONE
  CTEST_DO_UPDATES=OFF
  CTEST_DO_SUBMIT=OFF
  )

SET(CTEST_S_SCRIPT_ARGS
  ${CMAKE_CTEST_COMMAND} -V -S
    ${TribitsExProj_DIR}/cmake/ctest/general_gcc/ctest_serial_debug.cmake
  )

#
# Set up to submit to CDash if reqeusted
#

IF ("${${PACKAGE_NAME}_CTEST_DRIVER_SUBMIT_TO}" STREQUAL "") 
  SET(${PACKAGE_NAME}_CTEST_DRIVER_SUBMIT_TO
    $ENV{${PACKAGE_NAME}_CTEST_DRIVER_SUBMIT_TO} )
ENDIF()

IF ("${${PACKAGE_NAME}_CTEST_DRIVER_SUBMIT_TO}" STREQUAL "")
  SET(CTEST_DROP_SITE_ENV_ARGS
    CTEST_DO_SUBMIT=OFF
    )
ELSEIF (${PACKAGE_NAME}_CTEST_DRIVER_SUBMIT_TO STREQUAL "MY_CDASH")
  SET(CTEST_DROP_SITE_ENV_ARGS CTEST_DO_SUBMIT=TRUE)
ELSEIF (${PACKAGE_NAME}_CTEST_DRIVER_SUBMIT_TO STREQUAL "TRILINOS_CDASH")
  SET(CTEST_DROP_SITE_ENV_ARGS
    CTEST_DO_SUBMIT=TRUE
    CTEST_DROP_SITE="testing.sandia.gov/cdash"
    CTEST_PROJECT_NAME="TribitsExProj"
    CTEST_DROP_LOCATION="/submit.php?project=TribitsExProj"
    )
ELSEIF (${PACKAGE_NAME}_CTEST_DRIVER_SUBMIT_TO STREQUAL "EXP_CDASH")
  SET(CTEST_DROP_SITE_ENV_ARGS
    CTEST_DO_SUBMIT=TRUE
    CTEST_DROP_SITE="exp.cdash.org"
    CTEST_PROJECT_NAME="TribitsExProj"
    CTEST_DROP_LOCATION="/submit.php?project=TribitsExProj"
    )
ELSEIF (${PACKAGE_NAME}_CTEST_DRIVER_SUBMIT_TO STREQUAL "TESTING_VM_SANDIA_CDASH")
  SET(CTEST_DROP_SITE_ENV_ARGS
    CTEST_DO_SUBMIT=TRUE
    CTEST_DROP_SITE="testing-vm.sandia.gov"
    CTEST_PROJECT_NAME="TribitsExProj"
    CTEST_DROP_LOCATION="/CDash/submit.php?project=TribitsExProj"
    )
ELSE()
  MESSAGE(FATAL_ERROR "Error, the value"
    " ${PACKAGE_NAME}_CTEST_DRIVER_SUBMIT_TO='${${PACKAGE_NAME}_CTEST_DRIVER_SUBMIT_TO}'"
    " is invalid!  Valid choices are '', 'MY_CDASH', 'TRILINOS_CDASH', 'EXP_CDASH',"
    " and 'TESTING_VM_SANDIA_CDASH'!"
   ) 
ENDIF()

IF (NOT "${${PACKAGE_NAME}_CTEST_DRIVER_SUBMIT_TO}" STREQUAL "")
  MESSAGE(
    "NOTE: The tests ${PACKAGE_NAME}_CTestDriver_XXX are set up to submit CDash!"
    " (See the test details for what CDash site is being targeted!)"
    )
ENDIF()


#
# Set up arguments for direct configures of TribitsExamleProject to test the
# 'dashboard' target.
#

INCLUDE("${CMAKE_CURRENT_LIST_DIR}/../../core/ExamplesUnitTests/GetCompilerPassthroughArgs.cmake")


SET(CTEST_DROP_SITE_CONFIG_ARGS)
FOREACH (CTEST_DROP_SITE_ENV_ARG ${CTEST_DROP_SITE_ENV_ARGS})
  LIST(APPEND CTEST_DROP_SITE_CONFIG_ARGS "-D${CTEST_DROP_SITE_ENV_ARG}")
ENDFOREACH()

SET(TribitsExampleProject_COMMON_CONFIG_ARGS
  ${COMMON_ENV_ARGS_PASSTHROUGH}
  -DTribitsExProj_ENABLE_Fortran=${${PROJECT_NAME}_ENABLE_Fortran}
  ${CTEST_DROP_SITE_CONFIG_ARGS}
  )


######################################################################
#
# Test package-by-package mode for TribitsCTestDriverCore.cmake
#
######################################################################


TRIBITS_ADD_ADVANCED_TEST( CTestDriver_PBP_ST_ALL_PASS
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  TEST_0
    MESSAGE "Symlink TribitsExampleProject so no need to clone (which would not work)."
    CMND ln
    ARGS -s ${TribitsExProj_DIR} .
  TEST_1
    MESSAGE "Run ctest driver testing everyting but no push."
    CMND env
    ARGS
      CTEST_DASHBOARD_ROOT=PWD
      ${PBP_COMMON_ENV_ARGS}
      TribitsExProj_ENABLE_SECONDARY_TESTED_CODE=TRUE
      ${CTEST_DROP_SITE_ENV_ARGS}
      CTEST_BUILD_NAME=${PACKAGE_NAME}_CTestDriver_PBP_ST_ALL_PASS
      ${CTEST_S_SCRIPT_ARGS}
    PASS_REGULAR_EXPRESSION_ALL
      "NONE does not exist, skipping extra repositories"
      "Setting TribitsExProj_ENABLE_ALL_PACKAGES=ON since TribitsExProj_PACKAGES_USER_SELECTED=''"
      "Final set of enabled packages:  SimpleCxx MixedLang WithSubpackages WrapExternal 4"
      "Final set of enabled SE packages:  SimpleCxx MixedLang WithSubpackagesA WithSubpackagesB WithSubpackagesC WithSubpackages WrapExternal"
      "SimpleCxx: Configure passed"
      "SimpleCxx: Libs build passed"
      "SimpleCxx: All build passed"
      "SimpleCxx_HelloWorldProg [.]+ +Passed"
      "MixedLang: Configure passed"
      "MixedLang: Libs build passed"
      "MixedLang: All build passed"
      "MixedLang_RayTracerTests [.]+ +Passed"
      "WithSubpackages: Configure passed"
      "WithSubpackages: Libs build passed"
      "WithSubpackages: All build passed"
      "WithSubpackagesA_test_of_a [.]+ +Passed"
      "WithSubpackagesB_test_of_b [.]+ +Passed"
      "WithSubpackagesC_test_of_c_util [.]+ +Passed"
      "WithSubpackagesC_test_of_c_b_mixed_lang [.]+ +Passed"
      "WrapExternal: Configure passed"
      "WrapExternal: Libs build passed"
      "WrapExternal: All build passed"
      "WrapExternal_run_external_func [.]+ +Passed"
      "TRIBITS_CTEST_DRIVER: OVERALL: ALL PASSSED"
    ALWAYS_FAIL_ON_NONZERO_RETURN
  )
  # NOTE: The above test is the basic mode of testing everything and making
  # sure that the configure, build, and tests all run correctly.  The names of
  # passing tests are grepped for to make sure they run and pass.  And a
  # non-zero return code is mandated.


TRIBITS_ADD_ADVANCED_TEST( CTestDriver_PBP_GlobalConfigureFail
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  TEST_0
    MESSAGE "Copy the project dir so I can break it!"
    CMND cp
    ARGS -r ${TribitsExProj_DIR} .
  TEST_1
    MESSAGE "Break the outer configure"
    CMND ${CMAKE_CURRENT_SOURCE_DIR}/append_file_with_line.sh
    ARGS TribitsExampleProject/CMakeLists.txt "The outer configure is broken!"
  TEST_2
    MESSAGE "Run ctest driver which should show a failed configure for every package!"
    CMND env
    ARGS
      CTEST_DASHBOARD_ROOT=PWD
      ${PBP_COMMON_ENV_ARGS}
      ${CTEST_DROP_SITE_ENV_ARGS}
      CTEST_BUILD_NAME=${PACKAGE_NAME}_CTestDriver_PBP_GlobalConfigureFail
      ${CTEST_S_SCRIPT_ARGS}
    PASS_REGULAR_EXPRESSION_ALL
      "SimpleCxx FAILED to configure"
      "MixedLang FAILED to configure"
      "WithSubpackages FAILED to configure"
      "TRIBITS_CTEST_DRIVER: OVERALL: ALL FAILED"
      "Final set packages that failed to configure or have the libraries build: 'SimpleCxx[;]MixedLang[;]WithSubpackages'"
    ALWAYS_FAIL_ON_ZERO_RETURN
  )
  # NOTE: The above test ensures that a global configure failures breaks the
  # configure for all of the packages that are tried.


TRIBITS_ADD_ADVANCED_TEST( CTestDriver_PBP_ST_BreakConfigureOptionalPkg
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  TEST_0
    MESSAGE "Copy the project dir so I can break it!"
    CMND cp
    ARGS -r ${TribitsExProj_DIR} .
  TEST_1
    MESSAGE "Break the confgiure for just the optional MixLang package"
    CMND ${CMAKE_CURRENT_SOURCE_DIR}/append_file_with_line.sh
    ARGS TribitsExampleProject/packages/mixed_lang/CMakeLists.txt
      "Configure of mixed_lang is broken!"
  TEST_2
    MESSAGE "Run ctest driver which should show a failed configure for just the MixedLang package!"
    CMND env
    ARGS
      CTEST_DASHBOARD_ROOT=PWD
      ${PBP_COMMON_ENV_ARGS}
      TribitsExProj_ENABLE_SECONDARY_TESTED_CODE=TRUE
      ${CTEST_DROP_SITE_ENV_ARGS}
      CTEST_BUILD_NAME=${PACKAGE_NAME}_CTestDriver_PBP_ST_BreakConfigureOptionalPkg
      ${CTEST_S_SCRIPT_ARGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Final set of enabled SE packages:  SimpleCxx MixedLang WithSubpackagesA WithSubpackagesB WithSubpackagesC WithSubpackages WrapExternal 7"
      "SimpleCxx: Configure passed"
      "SimpleCxx_HelloWorldProg [.]+ +Passed"
      "MixedLang FAILED to configure"
      "CONFIGURE_OPTIONS = '.*[;]-DTribitsExProj_ENABLE_MixedLang:BOOL=OFF[;].*[;]-DTribitsExProj_ENABLE_WithSubpackages:BOOL=ON'"
      "WithSubpackages: Configure passed"
      "WithSubpackagesA_test_of_a [.]+ +Passed"
      "CONFIGURE_OPTIONS = '.*[;]-DTribitsExProj_ENABLE_MixedLang:BOOL=OFF[;].*[;]-DTribitsExProj_ENABLE_WrapExternal:BOOL=ON'"
      "WrapExternal: Configure passed"
      "Final set packages that failed to configure or have the libraries build: 'MixedLang'"
      "Final set packages that had any failures: 'MixedLang'"
      "TRIBITS_CTEST_DRIVER: OVERALL: ALL FAILED"
    ALWAYS_FAIL_ON_ZERO_RETURN
  )
  # NOTE: The above test ensures that the configure failure of an upstream
  # optional package does not break the configure, build, or tests of
  # downstream packages.  It only disables the broken upstream package in
  # downstream packages.


TRIBITS_ADD_ADVANCED_TEST( CTestDriver_PBP_ST_BreakBuildLibOptionalPkg
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  TEST_0
    MESSAGE "Copy the project dir so I can break it!"
    CMND cp
    ARGS -r ${TribitsExProj_DIR} .
  TEST_1
    MESSAGE "Break the library build for optional MixLang package"
    CMND ${CMAKE_CURRENT_SOURCE_DIR}/append_file_with_line.sh
    ARGS TribitsExampleProject/packages/mixed_lang/src/MixedLang.cpp
      "Build mixed_lang lib is broken!"
  TEST_2
    MESSAGE "Run ctest driver which should show a failed libray build for just the MixedLang package!"
    CMND env
    ARGS
      CTEST_DASHBOARD_ROOT=PWD
      ${PBP_COMMON_ENV_ARGS}
      TribitsExProj_ENABLE_SECONDARY_TESTED_CODE=TRUE
      ${CTEST_DROP_SITE_ENV_ARGS}
      CTEST_BUILD_NAME=${PACKAGE_NAME}_CTestDriver_PBP_ST_BreakBuildLibOptionalPkg
      ${CTEST_S_SCRIPT_ARGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Final set of enabled SE packages:  SimpleCxx MixedLang WithSubpackagesA WithSubpackagesB WithSubpackagesC WithSubpackages WrapExternal 7"
      "SimpleCxx: Configure passed"
      "SimpleCxx_HelloWorldProg [.]+ +Passed"
      "MixedLang: Configure passed"
      "FAILED library build for package 'MixedLang'"
      "CONFIGURE_OPTIONS = '.*[;]-DTribitsExProj_ENABLE_MixedLang:BOOL=OFF[;].*[;]-DTribitsExProj_ENABLE_WithSubpackages:BOOL=ON'"
      "WithSubpackages: Configure passed"
      "WithSubpackagesA_test_of_a [.]+ +Passed"
      "CONFIGURE_OPTIONS = '.*[;]-DTribitsExProj_ENABLE_MixedLang:BOOL=OFF[;].*[;]-DTribitsExProj_ENABLE_WrapExternal:BOOL=ON'"
      "WrapExternal: Configure passed"
      "Final set packages that failed to configure or have the libraries build: 'MixedLang'"
      "Final set packages that had any failures: 'MixedLang'"
      "CMake Error at .*/TribitsCTestDriverCore.cmake"
      "TRIBITS_CTEST_DRIVER: OVERALL: ALL FAILED"
    ALWAYS_FAIL_ON_ZERO_RETURN
  )
  # NOTE: The above test ensures that the library build failure of an optional
  # upstream package does not break downstream packages.  It only disables the
  # optional upstream package in downstream packages.


TRIBITS_ADD_ADVANCED_TEST( CTestDriver_PBP_ST_BreakBuildAllOptionalPkg
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  TEST_0
    MESSAGE "Copy the project dir so I can break it!"
    CMND cp
    ARGS -r ${TribitsExProj_DIR} .
  TEST_1
    MESSAGE "Break a test build file only (not the library build)"
    CMND ${CMAKE_CURRENT_SOURCE_DIR}/append_file_with_line.sh
    ARGS TribitsExampleProject/packages/mixed_lang/test/tstRay_Tracer.cc
      "Build mixed_lang test is broken!"
  TEST_2
    MESSAGE "Run ctest driver which should show a failed ALL build (but not a failed lib build) for just the MixedLang package!"
    CMND env
    ARGS
      CTEST_DASHBOARD_ROOT=PWD
      ${PBP_COMMON_ENV_ARGS}
      TribitsExProj_ENABLE_SECONDARY_TESTED_CODE=TRUE
      ${CTEST_DROP_SITE_ENV_ARGS}
      CTEST_BUILD_NAME=${PACKAGE_NAME}_CTestDriver_PBP_ST_BreakBuildAllOptionalPkg
      ${CTEST_S_SCRIPT_ARGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Final set of enabled SE packages:  SimpleCxx MixedLang WithSubpackagesA WithSubpackagesB WithSubpackagesC WithSubpackages WrapExternal 7"
      "SimpleCxx: Configure passed"
      "SimpleCxx_HelloWorldProg [.]+ +Passed"
      "MixedLang: Configure passed"
      "MixedLang: Libs build passed"
      "MixedLang: All build FAILED"
      "MixedLang_RayTracerTests .*[*][*][*]Not Run"
      "WithSubpackages: Configure passed"
      "WithSubpackagesA_test_of_a [.]+ +Passed"
      "WithSubpackagesC_test_of_c_b_mixed_lang [.]+ +Passed"
      "WrapExternal: Configure passed"
      "Final set packages that had any failures: 'MixedLang'"
      "CMake Error at .*/TribitsCTestDriverCore.cmake"
      "TRIBITS_CTEST_DRIVER: OVERALL: ALL FAILED"
    FAIL_REGULAR_EXPRESSION
      "CONFIGURE_OPTIONS = '.*[;]-DTribitsExProj_ENABLE_MixedLang:BOOL=OFF[;]"
    ALWAYS_FAIL_ON_ZERO_RETURN
  )
  # NOTE: The above test ensures that the ALL build failure (but not the
  # library build failure) of an optional upstream package does not break
  # downstream packages in any way and does not disable the upstream package.


TRIBITS_ADD_ADVANCED_TEST( CTestDriver_PBP_ST_BreakBuildTestPkg
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  TEST_0
    MESSAGE "Copy the project dir so I can break it!"
    CMND cp
    ARGS -r ${TribitsExProj_DIR} .
  TEST_1
    MESSAGE "Break a test only (no build failure)"
    CMND ${CMAKE_CURRENT_SOURCE_DIR}/replace_string_in_file.sh
    ARGS TribitsExampleProject/packages/simple_cxx/test/CMakeLists.txt
      "Hello World" "Hellos World"
  TEST_2
    MESSAGE "Run ctest driver which should show a test for the package SimpleCxx!"
    CMND env
    ARGS
      CTEST_DASHBOARD_ROOT=PWD
      ${PBP_COMMON_ENV_ARGS}
      TribitsExProj_ENABLE_SECONDARY_TESTED_CODE=TRUE
      ${CTEST_DROP_SITE_ENV_ARGS}
      CTEST_BUILD_NAME=${PACKAGE_NAME}_CTestDriver_PBP_ST_BreakBuildTestPkg
      ${CTEST_S_SCRIPT_ARGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Final set of enabled SE packages:  SimpleCxx MixedLang WithSubpackagesA WithSubpackagesB WithSubpackagesC WithSubpackages WrapExternal 7"
      "SimpleCxx: Configure passed"
      "SimpleCxx_HelloWorldTests [.]+ +Passed"
      "SimpleCxx_HelloWorldProg [.]+[*][*][*]Failed  Required regular expression not found.Regex=.Hellos World"
      "SimpleCxx: File '.*/TriBITS_CTestDriver_PBP_ST_BreakBuildTestPkg/.*/LastTestsFailed_.*.log' exists so there were failed tests"
      "MixedLang: All build passed"
      "MixedLang_RayTracerTests [.]+ +Passed"
      "WithSubpackages: All build passed"
      "WithSubpackages: Configure passed"
      "WithSubpackagesA_test_of_a [.]+ +Passed"
      "WithSubpackagesC_test_of_c_b_mixed_lang [.]+ +Passed"
      "WrapExternal: All build passed"
      "WrapExternal_run_external_func [.]+ +Passed"
      "Final set packages that had any failures: 'SimpleCxx'"
      "CMake Error at .*/TribitsCTestDriverCore.cmake"
      "TRIBITS_CTEST_DRIVER: OVERALL: ALL FAILED"
    FAIL_REGULAR_EXPRESSION
      "CONFIGURE_OPTIONS = '.*[;]-DTribitsExProj_ENABLE_SimpleCxx:BOOL=OFF[;]"
    ALWAYS_FAIL_ON_ZERO_RETURN
  )
  # NOTE: The above test ensures that a test failure in a package is caught
  # and reported correctly.


TRIBITS_ADD_ADVANCED_TEST( CTestDriver_PBP_ST_BreakConfigureRequiredPkg
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  TEST_0
    MESSAGE "Copy the project dir so I can break it!"
    CMND cp
    ARGS -r ${TribitsExProj_DIR} .
  TEST_1
    MESSAGE "Break the confgiure for just the required SimpleCxx package"
    CMND ${CMAKE_CURRENT_SOURCE_DIR}/append_file_with_line.sh
    ARGS TribitsExampleProject/packages/simple_cxx/CMakeLists.txt
      "Configure of SimpleCxx is broken!"
  TEST_2
    MESSAGE "Run ctest driver which should show a failed configure for just the SimpleCxx package!"
    CMND env
    ARGS
      CTEST_DASHBOARD_ROOT=PWD
      ${PBP_COMMON_ENV_ARGS}
      TribitsExProj_ENABLE_SECONDARY_TESTED_CODE=TRUE
      ${CTEST_DROP_SITE_ENV_ARGS}
      CTEST_BUILD_NAME=${PACKAGE_NAME}_CTestDriver_PBP_ST_BreakConfigureRequiredPkg
      ${CTEST_S_SCRIPT_ARGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Final set of enabled SE packages:  SimpleCxx MixedLang WithSubpackagesA WithSubpackagesB WithSubpackagesC WithSubpackages WrapExternal 7"
      "SimpleCxx FAILED to configure"
      "CONFIGURE_OPTIONS = '.*[;]-DTribitsExProj_ENABLE_SimpleCxx:BOOL=OFF[;].*[;]-DTribitsExProj_ENABLE_MixedLang:BOOL=ON'"
      "MixedLang: Configure passed"
      "MixedLang: Libs build passed"
      "MixedLang_RayTracerTests [.]+ +Passed"
      "CONFIGURE_OPTIONS = '.*[;]-DTribitsExProj_ENABLE_SimpleCxx:BOOL=OFF[;].*[;]-DTribitsExProj_ENABLE_WithSubpackages:BOOL=ON'"
      "WithSubpackages: Configure passed"
      "WithSubpackages: Libs build passed"
      "WithSubpackages: All build passed"
      "No tests were found"  # Can't tell which package :-(
      "CONFIGURE_OPTIONS = '.*[;]-DTribitsExProj_ENABLE_SimpleCxx:BOOL=OFF[;].*[;]-DTribitsExProj_ENABLE_WrapExternal:BOOL=ON'"
      "WrapExternal: Configure passed"
      "WrapExternal: All build passed"
      "Final set packages that failed to configure or have the libraries build: 'SimpleCxx'"
      "Final set packages that had any failures: 'SimpleCxx'"
      "TRIBITS_CTEST_DRIVER: OVERALL: ALL FAILED"
    ALWAYS_FAIL_ON_ZERO_RETURN
  )
  # NOTE: The above test ensures that the configure failure of an upstream
  # optional package does not break the configure, build, or tests of
  # downstream packages.  It only disables the broken upstream package in
  # downstream packages.


TRIBITS_ADD_ADVANCED_TEST( CTestDriver_PBP_ST_ALL_COVERAGE
  OVERALL_WORKING_DIRECTORY TEST_NAME
  EXCLUDE_IF_NOT_TRUE  ${PACKAGE_NAME}_CTEST_DRIVER_COVERAGE_TESTS
  OVERALL_NUM_MPI_PROCS 1
  TEST_0
    MESSAGE "Symlink TribitsExampleProject so no need to clone (which would not work)."
    CMND ln
    ARGS -s ${TribitsExProj_DIR} .
  TEST_1
    MESSAGE "Run ctest driver testing everyting but no push."
    CMND env
    ARGS
      CTEST_DASHBOARD_ROOT=PWD
      ${PBP_COMMON_ENV_ARGS}
      TribitsExProj_ENABLE_SECONDARY_TESTED_CODE=TRUE
	CTEST_DO_COVERAGE_TESTING=TRUE
      ${CTEST_DROP_SITE_ENV_ARGS}
      CTEST_BUILD_NAME=${PACKAGE_NAME}_CTestDriver_PBP_ST_ALL_COVERAGE
      ${CTEST_S_SCRIPT_ARGS}
    PASS_REGULAR_EXPRESSION_ALL
      "CTEST_DO_COVERAGE_TESTING='TRUE'"
      "Loop through TribitsExProj packages to configure, build, and test"
      "Final set of packages to be explicitly processed by CTest/CDash:  SimpleCxx MixedLang WithSubpackages WrapExternal 4"
      "Running coverage for package 'SimpleCxx'"
      "Running coverage for package 'MixedLang'"
      "Running coverage for package 'WithSubpackages'"
      "Running coverage for package 'WrapExternal'"
      "TRIBITS_CTEST_DRIVER: OVERALL: ALL PASSSED"
    ALWAYS_FAIL_ON_NONZERO_RETURN
  )
  # NOTE: The above test is the only coverage test for PBP.


TRIBITS_ADD_ADVANCED_TEST( CTestDriver_PBP_ST_ALL_MEMORY
  OVERALL_WORKING_DIRECTORY TEST_NAME
  EXCLUDE_IF_NOT_TRUE  ${PACKAGE_NAME}_CTEST_DRIVER_MEMORY_TESTS
  OVERALL_NUM_MPI_PROCS 1
  TEST_0
    MESSAGE "Symlink TribitsExampleProject so no need to clone (which would not work)."
    CMND ln
    ARGS -s ${TribitsExProj_DIR} .
  TEST_1
    MESSAGE "Run ctest driver testing everyting but no push."
    CMND env
    ARGS
      CTEST_DASHBOARD_ROOT=PWD
      ${PBP_COMMON_ENV_ARGS}
      TribitsExProj_ENABLE_SECONDARY_TESTED_CODE=TRUE
        CTEST_DO_MEMORY_TESTING=TRUE
      ${CTEST_DROP_SITE_ENV_ARGS}
      CTEST_BUILD_NAME=${PACKAGE_NAME}_CTestDriver_PBP_ST_ALL_MEMORY
      ${CTEST_S_SCRIPT_ARGS}
    PASS_REGULAR_EXPRESSION_ALL
      "CTEST_DO_MEMORY_TESTING='TRUE'"
      "Loop through TribitsExProj packages to configure, build, and test"
      "Final set of packages to be explicitly processed by CTest/CDash:  SimpleCxx MixedLang WithSubpackages WrapExternal 4"
      "Running memory testing for package 'SimpleCxx'"
      "MemCheck .+: SimpleCxx_HelloWorldTests [.]+ +Passed"
      "Running memory testing for package 'MixedLang'"
      "MemCheck .+: MixedLang_RayTracerTests [.]+ +Passed"
      "Running memory testing for package 'WithSubpackages'"
      "MemCheck .+: WithSubpackagesA_test_of_a [.]+ +Passed"
      "Running memory testing for package 'WrapExternal'"
      "MemCheck .+: WrapExternal_run_external_func [.]+ +Passed"
      "TRIBITS_CTEST_DRIVER: OVERALL: ALL PASSSED"
    ALWAYS_FAIL_ON_NONZERO_RETURN
  )
  # NOTE: The above test is the only memory test for PBP.


TRIBITS_ADD_ADVANCED_TEST( CTestDriver_PBP_Dashboard_ST_ALL_PASS
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  EXCLUDE_IF_NOT_TRUE ${PROJECT_NAME}_ENABLE_Fortran
  TEST_0 CMND ${CMAKE_COMMAND}
    MESSAGE "Do the initial configure"
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=ON
      -DTribitsExProj_ENABLE_ALL_PACKAGES=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      -DTribitsExProj_ENABLE_SECONDARY_TESTED_CODE=ON
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Final set of enabled SE packages:  SimpleCxx MixedLang WithSubpackagesA WithSubpackagesB WithSubpackagesC WithSubpackages WrapExternal 7"
      "Finished configuring TribitsExProj"
      "Generating done"
    ALWAYS_FAIL_ON_NONZERO_RETURN
  TEST_1
    MESSAGE "Run the dashboard target"
    CMND env
    ARGS
      CTEST_BUILD_NAME=${PROJECT_NAME}_CTestDriver_PBP_Dashboard_ST_ALL_PASS
      make dashboard
    PASS_REGULAR_EXPRESSION_ALL
      "Running package-by-package experimental dashboard"
      "A[)] Clean out the list of packages"
      "B[)] Run the dashboard command setting the list of packages"
      "Final set of packages to be explicitly processed by CTest/CDash:  SimpleCxx MixedLang WithSubpackages WrapExternal 4"
      "Loop through TribitsExProj packages to configure, build, and test"
      "0. Processing current package SimpleCxx: libs='ON', tests='ON'"
      "1. Processing current package MixedLang: libs='ON', tests='ON'"
      "2. Processing current package WithSubpackages: libs='ON', tests='ON'"
      "3. Processing current package WrapExternal: libs='ON', tests='ON'"
      "Done with the incremental building and testing of TribitsExProj packages"
      "TRIBITS_CTEST_DRIVER_ERROR_QUEUE is empty. All is well."
      "TRIBITS_CTEST_DRIVER: OVERALL: ALL PASSSED"
      "C[)] Clean out the list of packages again to clean the cache file"
      "D[)] Reconfigure with the original package list"
    ALWAYS_FAIL_ON_NONZERO_RETURN
  TEST_2
    MESSAGE "Verify that the right set of packages are set"
    CMND ${CMAKE_COMMAND} ARGS .
    PASS_REGULAR_EXPRESSION_ALL
      "Enabling all required .and optional since TribitsExProj_ENABLE_ALL_OPTIONAL_PACKAGES=ON. upstream SE packages for current set of enabled packages .TribitsExProj_ENABLE_SECONDARY_TESTED_CODE=ON."
      "Final set of enabled packages:  SimpleCxx MixedLang WithSubpackages WrapExternal 4"
      "Generating done"
    ALWAYS_FAIL_ON_NONZERO_RETURN
  )
  # The above test does a lot of checking to really pin down the behavior of
  # the TRIBITS_CTEST_DRIVER() function run from the basic 'dashboard' target.
  # Follow-on tests will not check so much output.


TRIBITS_ADD_ADVANCED_TEST( CTestDriver_PBP_Dashboard_ST_PackagesSubset_PASS
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  EXCLUDE_IF_NOT_TRUE ${PROJECT_NAME}_ENABLE_Fortran
  TEST_0 CMND ${CMAKE_COMMAND}
    MESSAGE "Do the initial configure"
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=ON
      -DTribitsExProj_ENABLE_SimpleCxx=ON
      -DTribitsExProj_ENABLE_WrapExternal=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      -DTribitsExProj_ENABLE_SECONDARY_TESTED_CODE=ON
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Setting SimpleCxx_ENABLE_TESTS=ON"
      "Setting WrapExternal_ENABLE_TESTS=ON"
      "Final set of enabled SE packages:  SimpleCxx MixedLang WithSubpackagesA WithSubpackages WrapExternal 5"
      "Processing enabled package: SimpleCxx [(]Libs, Tests, Examples[)]"
      "Processing enabled package: MixedLang [(]Libs[)]"
      "Processing enabled package: WithSubpackages [(]A[)]"
      "Processing enabled package: WrapExternal [(]Libs, Tests, Examples[)]"
      "Generating done"
    ALWAYS_FAIL_ON_NONZERO_RETURN
  TEST_1
    MESSAGE "Run the dashboard target"
    CMND env
    ARGS
      CTEST_BUILD_NAME=${PROJECT_NAME}_CTestDriver_PBP_Dashboard_ST_PackagesSubset_PASS
      make dashboard
    PASS_REGULAR_EXPRESSION_ALL
      "Final set of packages to be explicitly processed by CTest/CDash:  SimpleCxx WrapExternal 2"
      "Loop through TribitsExProj packages to configure, build, and test"
      "0. Processing current package SimpleCxx: libs='ON', tests='ON'"
      "1. Processing current package WrapExternal: libs='ON', tests='ON'"
      "Done with the incremental building and testing of TribitsExProj packages"
      "TRIBITS_CTEST_DRIVER_ERROR_QUEUE is empty. All is well."
      "TRIBITS_CTEST_DRIVER: OVERALL: ALL PASSSED"
    ALWAYS_FAIL_ON_NONZERO_RETURN
  TEST_2
    MESSAGE "Verify that the right set of packages are set"
    CMND ${CMAKE_COMMAND} ARGS .
    PASS_REGULAR_EXPRESSION_ALL
      "Final set of enabled SE packages:  SimpleCxx MixedLang WithSubpackagesA WithSubpackages WrapExternal 5"
      "Processing enabled package: SimpleCxx [(]Libs, Tests, Examples[)]"
      "Processing enabled package: MixedLang [(]Libs[)]"
      "Processing enabled package: WithSubpackages [(]A[)]"
      "Processing enabled package: WrapExternal [(]Libs, Tests, Examples[)]"
      "Generating done"
      "Generating done"
    ALWAYS_FAIL_ON_NONZERO_RETURN
  )
  # The above test makes sure that TRIBITS_CTEST_DRIVER() function run from
  # the basic 'dashboard' target only tests the explicitly enabled and tested
  # packages.  It also makes sure that when the project is reconfigured at the
  # end, that it gives the same set of package enables.


######################################################################
#
# Test all-at-once mode for TribitsCTestDriverCore.cmake
#
######################################################################


FUNCTION(GENERATE_AAO_TESTS  USE_NEW_AAO_CTEST_CDASH_FEATURES)

  SET(TribitsExampleProject_AAO_COMMON_CONFIG_ARGS
    ${TribitsExampleProject_COMMON_CONFIG_ARGS}
    -DTribitsExProj_CTEST_DO_ALL_AT_ONCE=TRUE
    )

  SET( AAO_COMMON_ENV_ARGS
    ${PBP_COMMON_ENV_ARGS}
    TribitsExProj_CTEST_DO_ALL_AT_ONCE=TRUE
    )

  IF (USE_NEW_AAO_CTEST_CDASH_FEATURES)
    SET(AAO_POSTFIX "P")
    LIST(APPEND AAO_COMMON_ENV_ARGS
      TribitsExProj_CTEST_USE_NEW_AAO_FEATURES=TRUE )
    LIST(APPEND TribitsExampleProject_AAO_COMMON_CONFIG_ARGS
      -DTribitsExProj_CTEST_USE_NEW_AAO_FEATURES=TRUE )
    SET(CONFIGURE_OPTIONS_MATCH_CTEST_USE_NEW_AAO_FEATURES
      "-DTribitsExProj_CTEST_USE_NEW_AAO_FEATURES:BOOL=TRUE[;]" )
  ELSE()
    SET(AAO_POSTFIX "")
  ENDIF()

  TRIBITS_ADD_ADVANCED_TEST( CTestDriver_AAO${AAO_POSTFIX}_ST_ALL_PASS
    OVERALL_WORKING_DIRECTORY TEST_NAME
    OVERALL_NUM_MPI_PROCS 1
    TEST_0
      MESSAGE "Symlink TribitsExampleProject so no need to clone (which would not work)."
      CMND ln
      ARGS -s ${TribitsExProj_DIR} .
    TEST_1
      MESSAGE "Run ctest driver testing everyting but no push."
      CMND env
      ARGS
        CTEST_DASHBOARD_ROOT=PWD
        ${AAO_COMMON_ENV_ARGS}
        TribitsExProj_ENABLE_SECONDARY_TESTED_CODE=TRUE
        ${CTEST_DROP_SITE_ENV_ARGS}
        CTEST_BUILD_NAME=${PACKAGE_NAME}_CTestDriver_AAO${AAO_POSTFIX}_ST_ALL_PASS
        ${CTEST_S_SCRIPT_ARGS}
      PASS_REGULAR_EXPRESSION_ALL
        "NONE does not exist, skipping extra repositories"
        "Setting TribitsExProj_ENABLE_ALL_PACKAGES=ON since TribitsExProj_PACKAGES_USER_SELECTED=''"
        "Final set of enabled packages:  SimpleCxx MixedLang WithSubpackages WrapExternal 4"
        "Final set of enabled SE packages:  SimpleCxx MixedLang WithSubpackagesA WithSubpackagesB WithSubpackagesC WithSubpackages WrapExternal"
        "Final set of packages to be explicitly processed by CTest/CDash:  SimpleCxx MixedLang WithSubpackages WrapExternal 4"
        "Configure, build, test and submit results all-at-once for all enabled packages"
        "Configuring [.][.][.]"
        "CONFIGURE_OPTIONS = '-DTribitsExProj_TRIBITS_DIR=.*/tribits[;]-DCTEST_USE_LAUNCHERS:BOOL=1[;]-DTribitsExProj_ENABLE_ALL_OPTIONAL_PACKAGES:BOOL=ON[;]-DTribitsExProj_WARNINGS_AS_ERRORS_FLAGS:STRING=[;]-DTribitsExProj_ALLOW_NO_PACKAGES:BOOL=ON[;]-DTribitsExProj_DISABLE_ENABLED_FORWARD_DEP_PACKAGES=ON[;]-DTribitsExProj_DEPS_XML_OUTPUT_FILE:FILEPATH=[;]-DTribitsExProj_ENABLE_SECONDARY_TESTED_CODE:BOOL=TRUE[;]-DTribitsExProj_EXTRAREPOS_FILE:STRING=[;]-DTribitsExProj_IGNORE_MISSING_EXTRA_REPOSITORIES:BOOL=ON[;]-DTribitsExProj_ENABLE_KNOWN_EXTERNAL_REPOS_TYPE:STRING=Continuous[;]${CONFIGURE_OPTIONS_MATCH_CTEST_USE_NEW_AAO_FEATURES}-DTribitsExProj_ENABLE_ALL_PACKAGES=ON[;]-DTribitsExProj_ENABLE_TESTS:BOOL=ON[;]-DBUILD_SHARED_LIBS:BOOL=ON[;]-DCMAKE_BUILD_TYPE=DEBUG[;]-DCMAKE_C_COMPILER=gcc[;]-DCMAKE_CXX_COMPILER=g[+][+][;]-DCMAKE_Fortran_COMPILER=gfortran[;]-DTribitsExProj_ENABLE_Fortran=ON[;]-DTribitsExProj_TRACE_ADD_TEST=ON'"
        "Configure PASSED"
        "Building all targets [.][.][.]"
        "Build output: BUILD_ALL_NUM_ERRORS='0',BUILD_ALL_RETURN_VAL='0'"
        "Build PASSED"
        "Running tests .parallel level 1."
        "SimpleCxx_HelloWorldTests [.]+ +Passed"
        "SimpleCxx_HelloWorldProg [.]+ +Passed"
        "WithSubpackagesA_test_of_a [.]+ +Passed"
        "WithSubpackagesB_test_of_b [.]+ +Passed"
        "WithSubpackagesC_test_of_c_util [.]+ +Passed"
        "WithSubpackagesC_test_of_c_b_mixed_lang [.]+ +Passed"
        "WrapExternal_run_external_func [.]+ +Passed"
	"Skipping converage tests because CTEST_DO_COVERAGE_TESTING='FALSE'"
	"Skipping memory testing because CTEST_DO_MEMORY_TESTING='FALSE'"
        "File '' does NOT exist so all tests passed"
        "TRIBITS_CTEST_DRIVER: OVERALL: ALL PASSSED"
      ALWAYS_FAIL_ON_NONZERO_RETURN
    )
    # NOTE: The above test is the basic mode of testing all packages and making
    # sure that the configure, build, and tests all run correctly for
    # everything.  The names of passing tests are grepped for to make sure they
    # run and pass.  And a non-zero return code is mandated.  Also, the full
    # CONFIGURE_OPTIONS list is checked to make sure that it does not change
    # without being noticed.  Follow-on tests will not check all of that.

  TRIBITS_ADD_ADVANCED_TEST( CTestDriver_AAO${AAO_POSTFIX}_ST_PackagesSubset_PASS
    OVERALL_WORKING_DIRECTORY TEST_NAME
    OVERALL_NUM_MPI_PROCS 1
    TEST_0
      MESSAGE "Symlink TribitsExampleProject so no need to clone (which would not work)."
      CMND ln
      ARGS -s ${TribitsExProj_DIR} .
    TEST_1
      MESSAGE "Run ctest driver testing everyting but no push."
      CMND env
      ARGS
        CTEST_DASHBOARD_ROOT=PWD
        ${AAO_COMMON_ENV_ARGS}
        TribitsExProj_ENABLE_SECONDARY_TESTED_CODE=TRUE
        TribitsExProj_PACKAGES=SimpleCxx,WrapExternal
        CTEST_EXPLICITLY_ENABLE_IMPLICITLY_ENABLED_PACKAGES=FALSE
        ${CTEST_DROP_SITE_ENV_ARGS}
        CTEST_BUILD_NAME=${PACKAGE_NAME}_CTestDriver_AAO${AAO_POSTFIX}_ST_PackagesSubset_PASS
        ${CTEST_S_SCRIPT_ARGS}
      PASS_REGULAR_EXPRESSION_ALL
        "NONE does not exist, skipping extra repositories"
        "Setting SimpleCxx_ENABLE_TESTS=ON"
        "Setting WrapExternal_ENABLE_TESTS=ON"
        "Final set of enabled packages:  SimpleCxx MixedLang WithSubpackages WrapExternal 4"
        "Final set of enabled SE packages:  SimpleCxx MixedLang WithSubpackagesA WithSubpackages WrapExternal 5"
        "Final set of non-enabled SE packages:  WithSubpackagesB WithSubpackagesC 2"
        "Final set of packages to be explicitly processed by CTest/CDash:  SimpleCxx WrapExternal 2"
        "Configure, build, test and submit results all-at-once for all enabled packages"
        "Configuring [.][.][.]"
        "CONFIGURE_OPTIONS = '-DTribitsExProj_TRIBITS_DIR=.*/tribits[;].+[;]${CONFIGURE_OPTIONS_MATCH_CTEST_USE_NEW_AAO_FEATURES}-DTribitsExProj_ENABLE_SimpleCxx=ON[;]-DTribitsExProj_ENABLE_WrapExternal=ON[;]-DTribitsExProj_ENABLE_TESTS:BOOL=ON[;]-DBUILD_SHARED_LIBS:BOOL=ON[;].+'"
        "Configure PASSED"
        "Building all targets [.][.][.]"
        "Build output: BUILD_ALL_NUM_ERRORS='0',BUILD_ALL_RETURN_VAL='0'"
        "Build PASSED"
        "Running tests .parallel level 1."
        "SimpleCxx_HelloWorldTests [.]+ +Passed"
        "SimpleCxx_HelloWorldProg [.]+ +Passed"
        "WrapExternal_run_external_func [.]+ +Passed"
        "File '' does NOT exist so all tests passed"
        "TRIBITS_CTEST_DRIVER: OVERALL: ALL PASSSED"
      ALWAYS_FAIL_ON_NONZERO_RETURN
    )
    # NOTE: The above test makes sure that requesting a subset of packages build
    # will only enable and test that subset of packages.  Any extra dependency
    # enable/disable type of testing should be done with the much cheaper
    # dependency testing in the file ../MockCTestDriver/CMakeLists.txt.

  TRIBITS_ADD_ADVANCED_TEST( CTestDriver_AAO${AAO_POSTFIX}_GlobalConfigureFail
    OVERALL_WORKING_DIRECTORY TEST_NAME
    OVERALL_NUM_MPI_PROCS 1
    TEST_0
      MESSAGE "Copy the project dir so I can break it!"
      CMND cp
      ARGS -r ${TribitsExProj_DIR} .
    TEST_1
      MESSAGE "Break the outer configure"
      CMND ${CMAKE_CURRENT_SOURCE_DIR}/append_file_with_line.sh
      ARGS TribitsExampleProject/CMakeLists.txt "The outer configure is broken!"
    TEST_2
      MESSAGE "Run ctest driver which should show a failed configure!"
      CMND env
      ARGS
        CTEST_DASHBOARD_ROOT=PWD
        ${AAO_COMMON_ENV_ARGS}
        ${CTEST_DROP_SITE_ENV_ARGS}
        CTEST_BUILD_NAME=${PACKAGE_NAME}_CTestDriver_AAO${AAO_POSTFIX}_GlobalConfigureFail
        ${CTEST_S_SCRIPT_ARGS}
      PASS_REGULAR_EXPRESSION_ALL
        "Configure FAILED"
	"Skipping build because configure failed"
	"Skipping tests because configure failed"
	"Done with the all-at-once configure, build, test, ans submit of TribitsExProj packages"
	"Final set packages that had any failures: 'ALL_PACKAGES'"
        "TRIBITS_CTEST_DRIVER: OVERALL: ALL FAILED"
      ALWAYS_FAIL_ON_ZERO_RETURN
    TEST_3
      MESSAGE "Make sure the failedPackages.txt file has the right contects!"
      CMND cat
      ARGS
        BUILD/failedPackages.txt
      PASS_REGULAR_EXPRESSION_ALL
        "ALL_PACKAGES"
      ALWAYS_FAIL_ON_NONZERO_RETURN
    )
    # NOTE: The above test ensures that a configure failure is correctly
    # interpreted and processed.

  TRIBITS_ADD_ADVANCED_TEST( CTestDriver_AAO${AAO_POSTFIX}_ST_PackagesSubset_GlobalConfigureFail
    OVERALL_WORKING_DIRECTORY TEST_NAME
    OVERALL_NUM_MPI_PROCS 1
    TEST_0
      MESSAGE "Copy the project dir so I can break it!"
      CMND cp
      ARGS -r ${TribitsExProj_DIR} .
    TEST_1
      MESSAGE "Break the outer configure"
      CMND ${CMAKE_CURRENT_SOURCE_DIR}/append_file_with_line.sh
      ARGS TribitsExampleProject/CMakeLists.txt "The outer configure is broken!"
    TEST_2
      MESSAGE "Run ctest driver which should show a failed configure!"
      CMND env
      ARGS
        CTEST_DASHBOARD_ROOT=PWD
        ${AAO_COMMON_ENV_ARGS}
        TribitsExProj_ENABLE_SECONDARY_TESTED_CODE=TRUE
        TribitsExProj_PACKAGES=SimpleCxx,WrapExternal
        CTEST_EXPLICITLY_ENABLE_IMPLICITLY_ENABLED_PACKAGES=FALSE
        ${CTEST_DROP_SITE_ENV_ARGS}
        CTEST_BUILD_NAME=${PACKAGE_NAME}_CTestDriver_AAO${AAO_POSTFIX}_ST_PackagesSubset_GlobalConfigureFail
        ${CTEST_S_SCRIPT_ARGS}
      PASS_REGULAR_EXPRESSION_ALL
        "Configure FAILED"
	"Skipping build because configure failed"
	"Skipping tests because configure failed"
	"Done with the all-at-once configure, build, test, ans submit of TribitsExProj packages"
	"Final set packages that had any failures: 'SimpleCxx[;]WrapExternal'"
        "TRIBITS_CTEST_DRIVER: OVERALL: ALL FAILED"
      ALWAYS_FAIL_ON_ZERO_RETURN
    )
    # NOTE: The above test ensures that a configure failure is correctly
    # interpreted and processed.

  TRIBITS_ADD_ADVANCED_TEST( CTestDriver_AAO${AAO_POSTFIX}_ST_ALL_BreakWithSubpackagesALib
    OVERALL_WORKING_DIRECTORY TEST_NAME
    OVERALL_NUM_MPI_PROCS 1
    TEST_0
      MESSAGE "Copy the project dir so I can break it!"
      CMND cp
      ARGS -r ${TribitsExProj_DIR} .
    TEST_1
      MESSAGE "Break the library build WithSubpackageA"
      CMND ${CMAKE_CURRENT_SOURCE_DIR}/append_file_with_line.sh
      ARGS TribitsExampleProject/packages/with_subpackages/a/A.cpp
        "Build of A.cpp lib is broken!"
    TEST_2
      MESSAGE "Run ctest driver which should show a failed libray build for just the MixedLang package!"
      CMND env
      ARGS
        CTEST_DASHBOARD_ROOT=PWD
        ${AAO_COMMON_ENV_ARGS}
        TribitsExProj_ENABLE_SECONDARY_TESTED_CODE=TRUE
        ${CTEST_DROP_SITE_ENV_ARGS}
        CTEST_BUILD_NAME=${PACKAGE_NAME}_CTestDriver_AAO${AAO_POSTFIX}_ST_ALL_BreakWithSubpackagesALib
        ${CTEST_S_SCRIPT_ARGS}
      PASS_REGULAR_EXPRESSION_ALL
        "Final set of enabled SE packages:  SimpleCxx MixedLang WithSubpackagesA WithSubpackagesB WithSubpackagesC WithSubpackages WrapExternal 7"
        "Final set of packages to be explicitly processed by CTest/CDash:  SimpleCxx MixedLang WithSubpackages WrapExternal 4"
        "Configure PASSED"
	"Build output: BUILD_ALL_NUM_ERRORS='2',BUILD_ALL_RETURN_VAL='0'"
	"Build FAILED"
        "SimpleCxx_HelloWorldTests [.]+ +Passed"
        "SimpleCxx_HelloWorldProg [.]+ +Passed"
	"MixedLang_RayTracerTests [.]+ +Passed"
	"WithSubpackagesA_test_of_a [.]+[*][*][*]Not Run"
	"WithSubpackagesB_test_of_b [.]+[*][*][*]Not Run"
	"WithSubpackagesB_test_of_b_mixed_lang [.]+[*][*][*]Not Run"
	"WithSubpackagesC_test_of_c_util [.]+[*][*][*]Not Run"
	"WithSubpackagesC_test_of_c [.]+[*][*][*]Not Run"
	"WithSubpackagesC_test_of_c_b_mixed_lang [.]+[*][*][*]Not Run"
        "WrapExternal_run_external_func [.]+[*][*][*]Not Run"
        "File '.+/${PACKAGE_NAME}_CTestDriver_AAO${AAO_POSTFIX}_ST_ALL_BreakWithSubpackagesALib/BUILD/Testing/Temporary/LastTestsFailed_.+.log' exists so there were non-passing tests"
        "Final set packages that had any failures: 'WithSubpackages[;]WrapExternal'"
        "TRIBITS_CTEST_DRIVER: OVERALL: ALL FAILED"
      ALWAYS_FAIL_ON_ZERO_RETURN
    TEST_3
      MESSAGE "Make sure the failedPackages.txt file has the right contects!"
      CMND cat
      ARGS
        BUILD/failedPackages.txt
      PASS_REGULAR_EXPRESSION_ALL
        "WithSubpackages[;]WrapExternal"
      ALWAYS_FAIL_ON_NONZERO_RETURN
    )
    # NOTE: The above test ensures that the library build failure of an
    # upstream package is detected in that package and in all all downstream
    # packages.  For CI testing it is fine if downstream package enables are
    # triggered.  Also note that the contents of the failedPackages.txt file
    # is checked to make sure that it is getting written correctly.  That is
    # important for CI servers.

  TRIBITS_ADD_ADVANCED_TEST( CTestDriver_AAO${AAO_POSTFIX}_ST_PackagesSubset_BreakWithSubpackagesALib
    OVERALL_WORKING_DIRECTORY TEST_NAME
    OVERALL_NUM_MPI_PROCS 1
    TEST_0
      MESSAGE "Copy the project dir so I can break it!"
      CMND cp
      ARGS -r ${TribitsExProj_DIR} .
    TEST_1
      MESSAGE "Break the library build WithSubpackageA"
      CMND ${CMAKE_CURRENT_SOURCE_DIR}/append_file_with_line.sh
      ARGS TribitsExampleProject/packages/with_subpackages/a/A.cpp
        "Build of A.cpp lib is broken!"
    TEST_2
      MESSAGE "Run ctest driver which should show a failed libray build for just the MixedLang package!"
      CMND env
      ARGS
        CTEST_DASHBOARD_ROOT=PWD
        ${AAO_COMMON_ENV_ARGS}
        TribitsExProj_ENABLE_SECONDARY_TESTED_CODE=TRUE
        TribitsExProj_PACKAGES=SimpleCxx,WrapExternal
        CTEST_EXPLICITLY_ENABLE_IMPLICITLY_ENABLED_PACKAGES=FALSE
        ${CTEST_DROP_SITE_ENV_ARGS}
        CTEST_BUILD_NAME=${PACKAGE_NAME}_CTestDriver_AAO${AAO_POSTFIX}_ST_PackagesSubset_BreakWithSubpackagesALib
        ${CTEST_S_SCRIPT_ARGS}
      PASS_REGULAR_EXPRESSION_ALL
        "Final set of enabled SE packages:  SimpleCxx MixedLang WithSubpackagesA WithSubpackages WrapExternal 5"
        "Final set of packages to be explicitly processed by CTest/CDash:  SimpleCxx WrapExternal 2"
        "Configure PASSED"
	"Build output: BUILD_ALL_NUM_ERRORS='2',BUILD_ALL_RETURN_VAL='0'"
	"Build FAILED"
        "SimpleCxx_HelloWorldTests [.]+ +Passed"
        "SimpleCxx_HelloWorldProg [.]+ +Passed"
        "WrapExternal_run_external_func [.]+[*][*][*]Not Run"
        "File '.+/${PACKAGE_NAME}_CTestDriver_AAO${AAO_POSTFIX}_ST_PackagesSubset_BreakWithSubpackagesALib/BUILD/Testing/Temporary/LastTestsFailed_.+.log' exists so there were non-passing tests"
        "Final set packages that had any failures: 'WrapExternal'"
        "TRIBITS_CTEST_DRIVER: OVERALL: ALL FAILED"
      ALWAYS_FAIL_ON_ZERO_RETURN
    )
    # NOTE: The above test ensures that the library build failure of an
    # upstream package is detected as a break in all downstream packages even
    # though that upstream package is not directly shown on CDash.

  TRIBITS_ADD_ADVANCED_TEST( CTestDriver_AAO${AAO_POSTFIX}_ST_ALL_BreakSimpleCxxTestBuild
    OVERALL_WORKING_DIRECTORY TEST_NAME
    OVERALL_NUM_MPI_PROCS 1
    TEST_0
      MESSAGE "Copy the project dir so I can break it!"
      CMND cp
      ARGS -r ${TribitsExProj_DIR} .
    TEST_1
      MESSAGE "Break the build of a test only (no lib build failure)"
      CMND ${CMAKE_CURRENT_SOURCE_DIR}/append_file_with_line.sh
      ARGS TribitsExampleProject/packages/simple_cxx/test/SimpleCxx_HelloWorld_Tests.cpp
        "Build of SimpleCxx_HelloWorld_Tests.cpp lib is broken!"
    TEST_2
      MESSAGE "Run ctest driver which should show build failure and failing test"
      CMND env
      ARGS
        CTEST_DASHBOARD_ROOT=PWD
        ${AAO_COMMON_ENV_ARGS}
        TribitsExProj_ENABLE_SECONDARY_TESTED_CODE=TRUE
        ${CTEST_DROP_SITE_ENV_ARGS}
        CTEST_BUILD_NAME=${PACKAGE_NAME}_CTestDriver_AAO${AAO_POSTFIX}_ST_ALL_BreakSimpleCxxTestBuild
        ${CTEST_S_SCRIPT_ARGS}
      PASS_REGULAR_EXPRESSION_ALL
        "Final set of packages to be explicitly processed by CTest/CDash:  SimpleCxx MixedLang WithSubpackages WrapExternal 4"
        "Configure PASSED"
	"Build output: BUILD_ALL_NUM_ERRORS='2',BUILD_ALL_RETURN_VAL='0'"
	"Build FAILED"
        "SimpleCxx_HelloWorldTests [.]+[*][*][*]Not Run"
        "SimpleCxx_HelloWorldProg [.]+ +Passed"
        "WithSubpackagesA_test_of_a [.]+ +Passed"
        "WithSubpackagesB_test_of_b [.]+ +Passed"
        "WithSubpackagesC_test_of_c_util [.]+ +Passed"
        "WithSubpackagesC_test_of_c_b_mixed_lang [.]+ +Passed"
        "WrapExternal_run_external_func [.]+ +Passed"
        "Final set packages that had any failures: 'SimpleCxx'"
        "TRIBITS_CTEST_DRIVER: OVERALL: ALL FAILED"
      ALWAYS_FAIL_ON_ZERO_RETURN
    )
    # NOTE: The above test ensures that a build failure in the test of an
    # upstream package will be caught but will not impact break downstream
    # packages and tests.

  TRIBITS_ADD_ADVANCED_TEST( CTestDriver_AAO${AAO_POSTFIX}_ST_ALL_BreakSimpleCxxTestRun
    OVERALL_WORKING_DIRECTORY TEST_NAME
    OVERALL_NUM_MPI_PROCS 1
    TEST_0
      MESSAGE "Copy the project dir so I can break it!"
      CMND cp
      ARGS -r ${TribitsExProj_DIR} .
    TEST_1
      MESSAGE "Break a test only (no build failure)"
      CMND ${CMAKE_CURRENT_SOURCE_DIR}/replace_string_in_file.sh
      ARGS TribitsExampleProject/packages/simple_cxx/test/CMakeLists.txt
        "Hello World" "Hellos World"
    TEST_2
      MESSAGE "Run ctest driver which should show a failed libray build for just the MixedLang package!"
      CMND env
      ARGS
        CTEST_DASHBOARD_ROOT=PWD
        ${AAO_COMMON_ENV_ARGS}
        TribitsExProj_ENABLE_SECONDARY_TESTED_CODE=TRUE
        ${CTEST_DROP_SITE_ENV_ARGS}
        CTEST_BUILD_NAME=${PACKAGE_NAME}_CTestDriver_AAO${AAO_POSTFIX}_ST_ALL_BreakSimpleCxxTestRun
        ${CTEST_S_SCRIPT_ARGS}
      PASS_REGULAR_EXPRESSION_ALL
        "Final set of packages to be explicitly processed by CTest/CDash:  SimpleCxx MixedLang WithSubpackages WrapExternal 4"
        "Configure PASSED"
	"Build PASSED"
        "SimpleCxx_HelloWorldTests [.]+ +Passed"
        "SimpleCxx_HelloWorldProg [.]+[*][*][*]Failed"
        "WithSubpackagesA_test_of_a [.]+ +Passed"
        "WithSubpackagesB_test_of_b [.]+ +Passed"
        "WithSubpackagesC_test_of_c_util [.]+ +Passed"
        "WithSubpackagesC_test_of_c_b_mixed_lang [.]+ +Passed"
        "WrapExternal_run_external_func [.]+ +Passed"
        "Final set packages that had any failures: 'SimpleCxx'"
        "TRIBITS_CTEST_DRIVER: OVERALL: ALL FAILED"
      ALWAYS_FAIL_ON_ZERO_RETURN
    )
    # NOTE: The above test ensures that a runt failure in the test of an
    # upstream package will be caught but will not impact break downstream
    # packages and tests.

  TRIBITS_ADD_ADVANCED_TEST( CTestDriver_AAO${AAO_POSTFIX}_ST_ALL_COVERAGE
    OVERALL_WORKING_DIRECTORY TEST_NAME
    EXCLUDE_IF_NOT_TRUE  ${PACKAGE_NAME}_CTEST_DRIVER_COVERAGE_TESTS
    OVERALL_NUM_MPI_PROCS 1
    TEST_0
      MESSAGE "Symlink TribitsExampleProject so no need to clone (which would not work)."
      CMND ln
      ARGS -s ${TribitsExProj_DIR} .
    TEST_1
      MESSAGE "Run ctest driver testing"
      CMND env
      ARGS
        CTEST_DASHBOARD_ROOT=PWD
        ${AAO_COMMON_ENV_ARGS}
        TribitsExProj_ENABLE_SECONDARY_TESTED_CODE=TRUE
        CTEST_DO_COVERAGE_TESTING=TRUE
        ${CTEST_DROP_SITE_ENV_ARGS}
        CTEST_BUILD_NAME=${PACKAGE_NAME}_CTestDriver_AAO${AAO_POSTFIX}_ST_ALL_COVERAGE
        ${CTEST_S_SCRIPT_ARGS}
      PASS_REGULAR_EXPRESSION_ALL
        "CTEST_DO_COVERAGE_TESTING='TRUE'"
	"Final set of packages to be explicitly processed by CTest/CDash:  SimpleCxx MixedLang WithSubpackages WrapExternal 4"
	"Configure, build, test and submit results all-at-once for all enabled packages"
	"Gathering coverage results [.][.][.]"
	"Performing coverage"   # printed by ctest_coverage()
	"Percentage Coverage:"  # printed by ctest_coverage()
	"Done with the all-at-once configure, build, test, ans submit of TribitsExProj packages"
	"TRIBITS_CTEST_DRIVER_ERROR_QUEUE is empty. All is well."
        "TRIBITS_CTEST_DRIVER: OVERALL: ALL PASSSED"
      ALWAYS_FAIL_ON_NONZERO_RETURN
    )
    # NOTE: The above test is the only coverage test for AAO mode!

  TRIBITS_ADD_ADVANCED_TEST( CTestDriver_AAO${AAO_POSTFIX}_ST_ALL_MEMORY
    OVERALL_WORKING_DIRECTORY TEST_NAME
    EXCLUDE_IF_NOT_TRUE  ${PACKAGE_NAME}_CTEST_DRIVER_MEMORY_TESTS
    OVERALL_NUM_MPI_PROCS 1
    TEST_0
      MESSAGE "Symlink TribitsExampleProject so no need to clone (which would not work)."
      CMND ln
      ARGS -s ${TribitsExProj_DIR} .
    TEST_1
      MESSAGE "Run ctest driver testing"
      CMND env
      ARGS
        CTEST_DASHBOARD_ROOT=PWD
        ${AAO_COMMON_ENV_ARGS}
        TribitsExProj_ENABLE_SECONDARY_TESTED_CODE=TRUE
        CTEST_DO_MEMORY_TESTING=TRUE
        ${CTEST_DROP_SITE_ENV_ARGS}
        CTEST_BUILD_NAME=${PACKAGE_NAME}_CTestDriver_AAO${AAO_POSTFIX}_ST_ALL_MEMORY
        ${CTEST_S_SCRIPT_ARGS}
      PASS_REGULAR_EXPRESSION_ALL
        "CTEST_DO_MEMORY_TESTING='TRUE'"
	"Final set of packages to be explicitly processed by CTest/CDash:  SimpleCxx MixedLang WithSubpackages WrapExternal 4"
	"Configure, build, test and submit results all-at-once for all enabled packages"
	"Running memory tests [.][.][.]"
	"Memory check project"  # Printed by ctest_memcheck()
        "MemCheck .+: SimpleCxx_HelloWorldTests [.]+ +Passed"
        "MemCheck .+: MixedLang_RayTracerTests [.]+ +Passed"
        "MemCheck .+: WithSubpackagesA_test_of_a [.]+ +Passed"
        "MemCheck .+: WrapExternal_run_external_func [.]+ +Passed"
	"Done with the all-at-once configure, build, test, ans submit of TribitsExProj packages"
	"TRIBITS_CTEST_DRIVER_ERROR_QUEUE is empty. All is well."
        "TRIBITS_CTEST_DRIVER: OVERALL: ALL PASSSED"
      ALWAYS_FAIL_ON_NONZERO_RETURN
    )
    # NOTE: The above test is the only memory test for AAO mode!

  TRIBITS_ADD_ADVANCED_TEST( CTestDriver_AAO${AAO_POSTFIX}_Dashboard_ST_ALL_PASS
    OVERALL_WORKING_DIRECTORY TEST_NAME
    OVERALL_NUM_MPI_PROCS 1
    EXCLUDE_IF_NOT_TRUE ${PROJECT_NAME}_ENABLE_Fortran
    TEST_0 CMND ${CMAKE_COMMAND}
      MESSAGE "Do the initial configure"
      ARGS
        ${TribitsExampleProject_AAO_COMMON_CONFIG_ARGS}
        -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
        -DTribitsExProj_ENABLE_Fortran=ON
        -DTribitsExProj_ENABLE_ALL_PACKAGES=ON
        -DTribitsExProj_ENABLE_TESTS=ON
        -DTribitsExProj_ENABLE_SECONDARY_TESTED_CODE=ON
        ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
      PASS_REGULAR_EXPRESSION_ALL
        "Enabling all required .and optional since TribitsExProj_ENABLE_ALL_OPTIONAL_PACKAGES=ON. upstream SE packages for current set of enabled packages .TribitsExProj_ENABLE_SECONDARY_TESTED_CODE=ON."
        "Final set of enabled SE packages:  SimpleCxx MixedLang WithSubpackagesA WithSubpackagesB WithSubpackagesC WithSubpackages WrapExternal 7"
        "Finished configuring TribitsExProj"
        "Generating done"
      ALWAYS_FAIL_ON_NONZERO_RETURN
    TEST_1
      MESSAGE "Run the dashboard target"
      CMND env
      ARGS
        CTEST_BUILD_NAME=${PROJECT_NAME}_CTestDriver_AAO${AAO_POSTFIX}_Dashboard_ST_ALL_PASS
        make dashboard
      PASS_REGULAR_EXPRESSION_ALL
        "Running all-at-once experimental dashboard"
	"Final set of packages to be explicitly processed by CTest/CDash:  SimpleCxx MixedLang WithSubpackages WrapExternal 4"
	"Configure, build, test and submit results all-at-once for all enabled packages"
        "TRIBITS_CTEST_DRIVER: OVERALL: ALL PASSSED"
      ALWAYS_FAIL_ON_NONZERO_RETURN
    TEST_2
      MESSAGE "Verify that the right set of packages are set"
      CMND ${CMAKE_COMMAND} ARGS .
      PASS_REGULAR_EXPRESSION_ALL
        "Enabling all required .and optional since TribitsExProj_ENABLE_ALL_OPTIONAL_PACKAGES=ON. upstream SE packages for current set of enabled packages .TribitsExProj_ENABLE_SECONDARY_TESTED_CODE=ON."
        "Final set of enabled packages:  SimpleCxx MixedLang WithSubpackages WrapExternal 4"
        "Generating done"
      ALWAYS_FAIL_ON_NONZERO_RETURN
    )

  TRIBITS_ADD_ADVANCED_TEST( CTestDriver_AAO${AAO_POSTFIX}_Dashboard_ST_PackagesSubset_PASS
    OVERALL_WORKING_DIRECTORY TEST_NAME
    OVERALL_NUM_MPI_PROCS 1
    EXCLUDE_IF_NOT_TRUE ${PROJECT_NAME}_ENABLE_Fortran
    TEST_0 CMND ${CMAKE_COMMAND}
      MESSAGE "Do the initial configure"
      ARGS
        ${TribitsExampleProject_AAO_COMMON_CONFIG_ARGS}
        -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
        -DTribitsExProj_ENABLE_Fortran=ON
        -DTribitsExProj_ENABLE_SimpleCxx=ON
        -DTribitsExProj_ENABLE_WrapExternal=ON
        -DTribitsExProj_ENABLE_TESTS=ON
        -DTribitsExProj_ENABLE_SECONDARY_TESTED_CODE=ON
        ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
      PASS_REGULAR_EXPRESSION_ALL
        "Setting SimpleCxx_ENABLE_TESTS=ON"
        "Setting WrapExternal_ENABLE_TESTS=ON"
        "Final set of enabled SE packages:  SimpleCxx MixedLang WithSubpackagesA WithSubpackages WrapExternal 5"
        "Processing enabled package: SimpleCxx [(]Libs, Tests, Examples[)]"
        "Processing enabled package: MixedLang [(]Libs[)]"
        "Processing enabled package: WithSubpackages [(]A[)]"
        "Processing enabled package: WrapExternal [(]Libs, Tests, Examples[)]"
        "Generating done"
      ALWAYS_FAIL_ON_NONZERO_RETURN
    TEST_1
      MESSAGE "Run the dashboard target"
      CMND env
      ARGS
        CTEST_BUILD_NAME=${PROJECT_NAME}_CTestDriver_AAO${AAO_POSTFIX}_Dashboard_ST_PackagesSubset_PASS
        make dashboard
      PASS_REGULAR_EXPRESSION_ALL
	"Configure, build, test and submit results all-at-once for all enabled packages"
        "Final set of packages to be explicitly processed by CTest/CDash:  SimpleCxx WrapExternal 2"
        "TRIBITS_CTEST_DRIVER_ERROR_QUEUE is empty. All is well."
        "TRIBITS_CTEST_DRIVER: OVERALL: ALL PASSSED"
      ALWAYS_FAIL_ON_NONZERO_RETURN
    TEST_2
      MESSAGE "Verify that the right set of packages are set"
      CMND ${CMAKE_COMMAND} ARGS .
      PASS_REGULAR_EXPRESSION_ALL
        "Final set of enabled SE packages:  SimpleCxx MixedLang WithSubpackagesA WithSubpackages WrapExternal 5"
        "Processing enabled package: SimpleCxx [(]Libs, Tests, Examples[)]"
        "Processing enabled package: MixedLang [(]Libs[)]"
        "Processing enabled package: WithSubpackages [(]A[)]"
        "Processing enabled package: WrapExternal [(]Libs, Tests, Examples[)]"
        "Generating done"
        "Generating done"
      ALWAYS_FAIL_ON_NONZERO_RETURN
    )
  
ENDFUNCTION()


# Run all-at-once-tests *WITHOUT* using new CMake/CTest/CDash features (so
# packages will *NOT* get split out on CDash)
GENERATE_AAO_TESTS(FALSE)


# Run all-at-once-tests *WITH* using new CMake/CTest/CDash features (so
# packages will get split out on CDash)
IF (TribitsExProj_CTEST_USE_NEW_AAO_FEATURES)
  GENERATE_AAO_TESTS(TRUE)
ENDIF()
