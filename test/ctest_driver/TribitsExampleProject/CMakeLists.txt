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


#
# Set up common vars/args for all tests
#

SET(TribitsExProj_DIR "${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject")

SET(COMMON_ENV_ARGS
  # Set back to default
  TribitsExProj_PACKAGES=
  CTEST_EXPLICITLY_ENABLE_IMPLICITLY_ENABLED_PACKAGES=
  CTEST_ENABLE_MODIFIED_PACKAGES_ONLY=OFF
  TribitsExProj_PRE_REPOSITORIES=
  TribitsExProj_EXTRA_REPOSITORIES=
  # Other args
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

IF ("${${PACKAGE_NAME}_TRIBITEXPROJ_SUBMIT_TO}" STREQUAL "") 
  SET(${PACKAGE_NAME}_TRIBITEXPROJ_SUBMIT_TO $ENV{${PACKAGE_NAME}_TRIBITEXPROJ_SUBMIT_TO})
ENDIF()

IF ("${${PACKAGE_NAME}_TRIBITEXPROJ_SUBMIT_TO}" STREQUAL "")
  SET(CDASH_SUBMIT_ARGS "")
ELSEIF (${PACKAGE_NAME}_TRIBITEXPROJ_SUBMIT_TO STREQUAL "MY_CDASH")
  SET(CDASH_SUBMIT_ARGS CTEST_DO_SUBMIT=TRUE)
ELSEIF (${PACKAGE_NAME}_TRIBITEXPROJ_SUBMIT_TO STREQUAL "TRILINOS_CDASH")
  SET(CDASH_SUBMIT_ARGS
    CTEST_DO_SUBMIT=TRUE
    CTEST_DROP_SITE=testing.sandia.gov/cdash
    CTEST_PROJECT_NAME=TribitsExProj
    CTEST_DROP_LOCATION="/submit.php?project=TribitsExProj"
    )
ELSE()
  MESSAGE(FATAL_ERROR "Error, the value"
    " ${PACKAGE_NAME}_TRIBITEXPROJ_SUBMIT_TO='${${PACKAGE_NAME}_TRIBITEXPROJ_SUBMIT_TO}'"
    " is invalid!  Valid choices are '', 'MY_CDASH' and 'TRILINOS_CDASH'"
   ) 
ENDIF()

IF (CDASH_SUBMIT_ARGS)
  MESSAGE(
    "NOTE: The tests ${PACKAGE_NAME}_CTestDriver_XXX are set up to submit CDash!"
    " (See the test details for what CDash site is being targeted!)"
    )
ENDIF()

#
# Run the tests
#


TRIBITS_ADD_ADVANCED_TEST( CTestDriver_ST_ALL_PASS
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
      ${COMMON_ENV_ARGS}
      TribitsExProj_ENABLE_SECONDARY_TESTED_CODE=TRUE
      ${CDASH_SUBMIT_ARGS}
      CTEST_BUILD_NAME=${PACKAGE_NAME}_CTestDriver_ST_ALL_PASS
      ${CTEST_S_SCRIPT_ARGS}
    PASS_REGULAR_EXPRESSION_ALL
      "NONE does not exist, skipping extra repositories"
      "Setting TribitsExProj_ENABLE_ALL_PACKAGES=ON since TribitsExProj_PACKAGES_USER_SELECTED=''"
      "Final set of enabled packages:  SimpleCxx MixedLang WithSubpackages WrapExternal 4"
      "Final set of enabled SE packages:  SimpleCxx MixedLang WithSubpackagesA WithSubpackagesB WithSubpackagesC WithSubpackages WrapExternal"
      "SimpleCxx: Configure passed"
      "SimpleCxx: Libs build passed"
      "SimpleCxx: All build passed"
      "SimpleCxx_HelloWorldProg .* Passed"
      "MixedLang: Configure passed"
      "MixedLang: Libs build passed"
      "MixedLang: All build passed"
      "MixedLang_RayTracerTests .* Passed"
      "WithSubpackages: Configure passed"
      "WithSubpackages: Libs build passed"
      "WithSubpackages: All build passed"
      "WithSubpackagesA_test_of_a .* Passed"
      "WithSubpackagesB_test_of_b .* Passed"
      "WithSubpackagesC_test_of_c_util .* Passed"
      "WithSubpackagesC_test_of_c_b_mixed_lang .* Passed"
      "WrapExternal: Configure passed"
      "WrapExternal: Libs build passed"
      "WrapExternal: All build passed"
      "WrapExternal_run_external_func .* Passed"
      "TRIBITS_CTEST_DRIVER: OVERALL: ALL PASSSED"
    ALWAYS_FAIL_ON_NONZERO_RETURN
  )
  # NOTE: The above test is the basic mode of testing everything and making
  # sure that the configure, build, and tests all run correctly.  The names of
  # passing tests are grepped for to make sure they run and pass.  And a
  # non-zero return code is mandated.


TRIBITS_ADD_ADVANCED_TEST( CTestDriver_GlobalConfigureFail
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
      ${COMMON_ENV_ARGS}
      ${CDASH_SUBMIT_ARGS}
      CTEST_BUILD_NAME=${PACKAGE_NAME}_CTestDriver_GlobalConfigureFail
      ${CTEST_S_SCRIPT_ARGS}
    PASS_REGULAR_EXPRESSION_ALL
      "SimpleCxx FAILED to configure"
      "MixedLang FAILED to configure"
      "WithSubpackages FAILED to configure"
      "TRIBITS_CTEST_DRIVER: OVERALL: ALL FAILED"
      "Final set packages that failed to configure or have the libraries build: 'SimpleCxx[;]MixedLang[;]WithSubpackages'"
    # ToDo: Add ALWAYS_FAIL_ON_ZERO_RETURN!
  )
  # NOTE: The above test ensures that a global configure failures breaks the
  # configure for all of the packages that are tried.


TRIBITS_ADD_ADVANCED_TEST( CTestDriver_ST_BreakConfigureOptionalPkg
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
      ${COMMON_ENV_ARGS}
      TribitsExProj_ENABLE_SECONDARY_TESTED_CODE=TRUE
      ${CDASH_SUBMIT_ARGS}
      CTEST_BUILD_NAME=${PACKAGE_NAME}_CTestDriver_ST_BreakConfigureOptionalPkg
      ${CTEST_S_SCRIPT_ARGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Final set of enabled SE packages:  SimpleCxx MixedLang WithSubpackagesA WithSubpackagesB WithSubpackagesC WithSubpackages WrapExternal 7"
      "SimpleCxx: Configure passed"
      "SimpleCxx_HelloWorldProg .* Passed"
      "MixedLang FAILED to configure"
      "CONFIGURE_OPTIONS = '.*[;]-DTribitsExProj_ENABLE_MixedLang:BOOL=OFF[;].*[;]-DTribitsExProj_ENABLE_WithSubpackages:BOOL=ON'"
      "WithSubpackages: Configure passed"
      "WithSubpackagesA_test_of_a .* Passed"
      "CONFIGURE_OPTIONS = '.*[;]-DTribitsExProj_ENABLE_MixedLang:BOOL=OFF[;].*[;]-DTribitsExProj_ENABLE_WrapExternal:BOOL=ON'"
      "WrapExternal: Configure passed"
      "Final set packages that failed to configure or have the libraries build: 'MixedLang'"
      "Final set packages that had any failures: 'MixedLang'"
      "TRIBITS_CTEST_DRIVER: OVERALL: ALL FAILED"
    # ToDo: Add ALWAYS_FAIL_ON_ZERO_RETURN!
  )
  # NOTE: The above test ensures that the configure failure of an upstream
  # optional package does not break the configure, build, or tests of
  # downstream packages.  It only disables the broken upstream package in
  # downstream packages.


TRIBITS_ADD_ADVANCED_TEST( CTestDriver_ST_BreakBuildLibOptionalPkg
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
      ${COMMON_ENV_ARGS}
      TribitsExProj_ENABLE_SECONDARY_TESTED_CODE=TRUE
      ${CDASH_SUBMIT_ARGS}
      CTEST_BUILD_NAME=${PACKAGE_NAME}_CTestDriver_ST_BreakBuildLibOptionalPkg
      ${CTEST_S_SCRIPT_ARGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Final set of enabled SE packages:  SimpleCxx MixedLang WithSubpackagesA WithSubpackagesB WithSubpackagesC WithSubpackages WrapExternal 7"
      "SimpleCxx: Configure passed"
      "SimpleCxx_HelloWorldProg .* Passed"
      "MixedLang: Configure passed"
      "FAILED library build for package 'MixedLang'"
      "CONFIGURE_OPTIONS = '.*[;]-DTribitsExProj_ENABLE_MixedLang:BOOL=OFF[;].*[;]-DTribitsExProj_ENABLE_WithSubpackages:BOOL=ON'"
      "WithSubpackages: Configure passed"
      "WithSubpackagesA_test_of_a .* Passed"
      "CONFIGURE_OPTIONS = '.*[;]-DTribitsExProj_ENABLE_MixedLang:BOOL=OFF[;].*[;]-DTribitsExProj_ENABLE_WrapExternal:BOOL=ON'"
      "WrapExternal: Configure passed"
      "Final set packages that failed to configure or have the libraries build: 'MixedLang'"
      "Final set packages that had any failures: 'MixedLang'"
      "CMake Error at .*/TribitsCTestDriverCore.cmake"
      "TRIBITS_CTEST_DRIVER: OVERALL: ALL FAILED"
    # ToDo: Add ALWAYS_FAIL_ON_ZERO_RETURN!
  )
  # NOTE: The above test ensures that the library build failure of an optional
  # upstream package does not break downstream packages.  It only disables the
  # optional upstream package in downstream packages.


TRIBITS_ADD_ADVANCED_TEST( CTestDriver_ST_BreakBuildAllOptionalPkg
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  TEST_0
    MESSAGE "Copy the project dir so I can break it!"
    CMND cp
    ARGS -r ${TribitsExProj_DIR} .
  TEST_1
    MESSAGE "Break a test file only (not the library build)"
    CMND ${CMAKE_CURRENT_SOURCE_DIR}/append_file_with_line.sh
    ARGS TribitsExampleProject/packages/mixed_lang/test/tstRay_Tracer.cc
      "Build mixed_lang test is broken!"
  TEST_2
    MESSAGE "Run ctest driver which should show a failed ALL build (but not a failed lib build) for just the MixedLang package!"
    CMND env
    ARGS
      CTEST_DASHBOARD_ROOT=PWD
      ${COMMON_ENV_ARGS}
      TribitsExProj_ENABLE_SECONDARY_TESTED_CODE=TRUE
      ${CDASH_SUBMIT_ARGS}
      CTEST_BUILD_NAME=${PACKAGE_NAME}_CTestDriver_ST_BreakBuildAllOptionalPkg
      ${CTEST_S_SCRIPT_ARGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Final set of enabled SE packages:  SimpleCxx MixedLang WithSubpackagesA WithSubpackagesB WithSubpackagesC WithSubpackages WrapExternal 7"
      "SimpleCxx: Configure passed"
      "SimpleCxx_HelloWorldProg .* Passed"
      "MixedLang: Configure passed"
      "MixedLang: Libs build passed"
      "MixedLang: All build FAILED"
      "MixedLang_RayTracerTests .*[*][*][*]Not Run"
      "WithSubpackages: Configure passed"
      "WithSubpackagesA_test_of_a .* Passed"
      "WithSubpackagesC_test_of_c_b_mixed_lang .* Passed"
      "WrapExternal: Configure passed"
      "Final set packages that had any failures: 'MixedLang'"
      "CMake Error at .*/TribitsCTestDriverCore.cmake"
      "TRIBITS_CTEST_DRIVER: OVERALL: ALL FAILED"
    FAIL_REGULAR_EXPRESSION
      "CONFIGURE_OPTIONS = '.*[;]-DTribitsExProj_ENABLE_MixedLang:BOOL=OFF[;]"
    # ToDo: Add ALWAYS_FAIL_ON_ZERO_RETURN!
  )
  # NOTE: The above test ensures that the ALL build failure (but not the
  # library build failure) of an optional upstream package does not break
  # downstream packages in any way and does not disable the upstream package.


TRIBITS_ADD_ADVANCED_TEST( CTestDriver_ST_BreakConfigureRequiredPkg
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
      ${COMMON_ENV_ARGS}
      TribitsExProj_ENABLE_SECONDARY_TESTED_CODE=TRUE
      ${CDASH_SUBMIT_ARGS}
      CTEST_BUILD_NAME=${PACKAGE_NAME}_CTestDriver_ST_BreakConfigureRequiredPkg
      ${CTEST_S_SCRIPT_ARGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Final set of enabled SE packages:  SimpleCxx MixedLang WithSubpackagesA WithSubpackagesB WithSubpackagesC WithSubpackages WrapExternal 7"
      "SimpleCxx FAILED to configure"
      "CONFIGURE_OPTIONS = '.*[;]-DTribitsExProj_ENABLE_SimpleCxx:BOOL=OFF[;].*[;]-DTribitsExProj_ENABLE_MixedLang:BOOL=ON'"
      "MixedLang: Configure passed"
      "MixedLang: Libs build passed"
      "MixedLang_RayTracerTests .* Passed"
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
    # ToDo: Add ALWAYS_FAIL_ON_ZERO_RETURN!
  )
  # NOTE: The above test ensures that the configure failure of an upstream
  # optional package does not break the configure, build, or tests of
  # downstream packages.  It only disables the broken upstream package in
  # downstream packages.
