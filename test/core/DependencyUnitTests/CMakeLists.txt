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
# These tests test the basic dependency adjustment logic in TriBITS for
# enabling and disabling packages, subpackages, tests/examples, TPLs, etc.
# These run very fast because they don't need to actually configure any code.
#

set(TRIBITS_REDUCED_MOCK_TRILINOS_DIR "examples/ReducedMockTrilinos")
set(TRIBITS_MOCK_TRILINOS_DIR "examples/MockTrilinos")


# MockTrilinos project
set(MOCK_PROJECT_NAME Trilinos)
set(MOCK_TRILINOS_DIR
  ${${PROJECT_NAME}_TRIBITS_DIR}/${TRIBITS_MOCK_TRILINOS_DIR})


#####################################################################
#
# Unit tests for dependency handling for reduced set of packages
#
#####################################################################

# Reduced MockTrilinos project
set(REDUCED_MOCK_PROJECT_NAME Trilinos)
set(REDUCED_MOCK_TRILINOS_DIR
  ${${PROJECT_NAME}_TRIBITS_DIR}/${TRIBITS_REDUCED_MOCK_TRILINOS_DIR})

# Expected output files directory
set(REDUCED_MOCK_TRILINOS_OUTPUT_DIR
  "${${PROJECT_NAME}_TRIBITS_DIR}/doc/guides/ReducedMockTrilinosOutput")


#
# NOTE: These tests compare against expected output stored in files under the
# in the guides/ReducedMockTrilinosOuptut/ directory and are used in the
# TribitsUsersGuide.rst document.  Therefore, if the behavior of TriBITS
# changes in such a way as to break these tests, then if any of the contents
# of the files under this directory need to change, then one must also look at
# the TribitsUsersGuilde.rst document and update it for the new behavior of
# TriBITS!
#


function(create_reduced_dependency_handling_test_case TEST_NAME)

  cmake_parse_arguments(
     #prefix
     PARSE
     #options
     ""
     #one_value_keywords
     ""
     #multi_value_keywords
     "ARGS;PASS_REGULAR_EXPRESSION_ALL"
     ${ARGN}
     )

  tribits_add_advanced_test( DepTestReduced_${TEST_NAME}
    OVERALL_WORKING_DIRECTORY TEST_NAME
    OVERALL_NUM_MPI_PROCS 1
    TEST_0 CMND "${CMAKE_COMMAND}"
      ARGS
        ${PARSE_ARGS}
        ${REDUCED_MOCK_TRILINOS_DIR}
      PASS_REGULAR_EXPRESSION_ALL ${PARSE_PASS_REGULAR_EXPRESSION_ALL}
    )

endfunction()


# Read in an expected output file and create a REGEX array to be used in
# checking test results (and replace all problematic chars as appropriate
# regex).
#
function(read_expected_output_file_into_regex_array  EXPECTED_OUTPUT_FILE
  EXPECTED_OUTPUT_REGEX_ARRAY_OUT
  )
  file(READ ${EXPECTED_OUTPUT_FILE} EXPECTED_RAW_STR_ALL)
  #print_var(EXPECTED_RAW_STR_ALL)
  split("${EXPECTED_RAW_STR_ALL}" "\n" EXPECTED_RAW_STR_ARRAY)
  #print_var(EXPECTED_RAW_STR_ARRAY)
  set(EXPECTED_REGEX_ARRAY)
  foreach(EXPECTED_RAW_STR ${EXPECTED_RAW_STR_ARRAY})
    #print_var(EXPECTED_RAW_STR)
    if (NOT "${EXPECTED_RAW_STR}" STREQUAL "")
      set(EXPECTED_REGEX_STR "${EXPECTED_RAW_STR}")
      string(REPLACE "[" "." EXPECTED_REGEX_STR "${EXPECTED_REGEX_STR}")
      string(REPLACE "]" "." EXPECTED_REGEX_STR "${EXPECTED_REGEX_STR}")
      string(REPLACE "(" "[(]" EXPECTED_REGEX_STR "${EXPECTED_REGEX_STR}")
      string(REPLACE ")" "[)]" EXPECTED_REGEX_STR "${EXPECTED_REGEX_STR}")
      string(REPLACE "*" "." EXPECTED_REGEX_STR "${EXPECTED_REGEX_STR}")
      list(APPEND EXPECTED_REGEX_ARRAY "${EXPECTED_REGEX_STR}")
      #print_var(EXPECTED_REGEX_ARRAY)
    endif()
  endforeach()
  set_property(DIRECTORY APPEND
    PROPERTY CMAKE_CONFIGURE_DEPENDS "${EXPECTED_OUTPUT_FILE}")
  set(${EXPECTED_OUTPUT_REGEX_ARRAY_OUT} ${EXPECTED_REGEX_ARRAY} PARENT_SCOPE)
endfunction()



#
# NoEnables
#

read_expected_output_file_into_regex_array(
  "${REDUCED_MOCK_TRILINOS_OUTPUT_DIR}/NoEnables.txt"
  RMT_NoEnables_REGEX_ARRAY
  )
#print_var(REDUCED_EXPECTED_DEPENDENCIES_REGEX_ARRAY)


create_reduced_dependency_handling_test_case(
  NoEnables
  ARGS
  PASS_REGULAR_EXPRESSION_ALL
    ${RMT_NoEnables_REGEX_ARRAY}
  )


#
# EnableThyra_EnableTests
#

read_expected_output_file_into_regex_array(
  "${REDUCED_MOCK_TRILINOS_OUTPUT_DIR}/EnableThyra_EnableTests.txt"
  EnableThyra_EnableTests_REGEX_ARRAY
  )

create_reduced_dependency_handling_test_case(
  EnableThyra_EnableTests
  ARGS
    -DTrilinos_ENABLE_Thyra:BOOL=ON
    -DTrilinos_ENABLE_TESTS:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    ${EnableThyra_EnableTests_REGEX_ARRAY}
  )


#
# EnableThyra_EnableTests_EnableBoost_ST
#

read_expected_output_file_into_regex_array(
  "${REDUCED_MOCK_TRILINOS_OUTPUT_DIR}/EnableThyra_EnableTests_EnableBoost_ST.txt"
  EnableThyra_EnableTests_EnableBoost_ST_REGEX_ARRAY
  )

create_reduced_dependency_handling_test_case(
  EnableThyra_EnableTests_EnableBoost_ST
  ARGS
    -DTPL_ENABLE_Boost:BOOL=ON
    -DTrilinos_ENABLE_Thyra:BOOL=ON
    -DTrilinos_ENABLE_TESTS:BOOL=ON
    -DTrilinos_ENABLE_SECONDARY_TESTED_CODE:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    ${EnableThyra_EnableTests_EnableBoost_ST_REGEX_ARRAY}
  )


#
# EnableThyra_EnableTests_EnableBoost_ST_RequiredOnly
#

read_expected_output_file_into_regex_array(
  "${REDUCED_MOCK_TRILINOS_OUTPUT_DIR}/EnableThyra_EnableTests_EnableBoost_ST_RequiredOnly.txt"
  EnableThyra_EnableTests_EnableBoost_ST_RequiredOnly_REGEX_ARRAY
  )

create_reduced_dependency_handling_test_case(
  EnableThyra_EnableTests_EnableBoost_ST_RequiredOnly
  ARGS
    -DTPL_ENABLE_Boost:BOOL=ON
    -DTrilinos_ENABLE_Thyra:BOOL=ON
    -DTrilinos_ENABLE_TESTS:BOOL=ON
    -DTrilinos_ENABLE_SECONDARY_TESTED_CODE:BOOL=ON
    -DTrilinos_ENABLE_ALL_OPTIONAL_PACKAGES:BOOL=OFF
  PASS_REGULAR_EXPRESSION_ALL
    ${EnableThyra_EnableTests_EnableBoost_ST_RequiredOnly_REGEX_ARRAY}
  )


#
# EnableThyra_DisableEpetra_EnableTests
#

read_expected_output_file_into_regex_array(
  "${REDUCED_MOCK_TRILINOS_OUTPUT_DIR}/EnableThyra_DisableEpetra_EnableTests.txt"
  EnableThyra_DisableEpetra_EnableTests_REGEX_ARRAY
  )

create_reduced_dependency_handling_test_case(
  EnableThyra_DisableEpetra_EnableTests
  ARGS
    -DTrilinos_ENABLE_Thyra:BOOL=ON
    -DTrilinos_ENABLE_Epetra:BOOL=OFF
    -DTrilinos_ENABLE_TESTS:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    ${EnableThyra_DisableEpetra_EnableTests_REGEX_ARRAY}
  )

#
# EnableEpetra_EnableRTOp_DisableTeuchos
#

set(TEST_NAME "EnableEpetra_EnableRTOp_DisableTeuchos")

read_expected_output_file_into_regex_array(
  "${REDUCED_MOCK_TRILINOS_OUTPUT_DIR}/${TEST_NAME}.txt"
  ${TEST_NAME}_REGEX_ARRAY
  )

create_reduced_dependency_handling_test_case(
  ${TEST_NAME}
  ARGS
    -DTrilinos_ENABLE_Epetra:BOOL=ON
    -DTrilinos_ENABLE_RTOp:BOOL=ON
    -DTrilinos_ENABLE_Teuchos:BOOL=OFF
   PASS_REGULAR_EXPRESSION_ALL
    ${${TEST_NAME}_REGEX_ARRAY}
  )


#
# EnableEpetra_EnableRTOp_DisableTeuchos_DisableEnabledFwdDepPackages
#

set(TEST_NAME "EnableEpetra_EnableRTOp_DisableTeuchos_DisableEnabledFwdDepPackages")

read_expected_output_file_into_regex_array(
  "${REDUCED_MOCK_TRILINOS_OUTPUT_DIR}/${TEST_NAME}.txt"
  ${TEST_NAME}_REGEX_ARRAY
  )

create_reduced_dependency_handling_test_case(
  ${TEST_NAME}
  ARGS
    -DTrilinos_ENABLE_Epetra:BOOL=ON
    -DTrilinos_ENABLE_RTOp:BOOL=ON
    -DTrilinos_ENABLE_Teuchos:BOOL=OFF
    -DTrilinos_DISABLE_ENABLED_FORWARD_DEP_PACKAGES=ON
   PASS_REGULAR_EXPRESSION_ALL
    ${${TEST_NAME}_REGEX_ARRAY}
  )


#
# EnableThyraCoreLibs_EnableTests
#

set(TEST_NAME "EnableThyraCoreLibs_EnableTests")

read_expected_output_file_into_regex_array(
  "${REDUCED_MOCK_TRILINOS_OUTPUT_DIR}/${TEST_NAME}.txt"
  ${TEST_NAME}_REGEX_ARRAY
  )

create_reduced_dependency_handling_test_case(
  ${TEST_NAME}
  ARGS
    -DTrilinos_ENABLE_ThyraCoreLibs:BOOL=ON
    -DTrilinos_ENABLE_TESTS:BOOL=ON
   PASS_REGULAR_EXPRESSION_ALL
    ${${TEST_NAME}_REGEX_ARRAY}
    "-- Setting Trilinos_ENABLE_Thyra=ON because Trilinos_ENABLE_ThyraCoreLibs=ON"
    "-- Setting Thyra_ENABLE_TESTS=ON because ThyraCoreLibs_ENABLE_TESTS=ON"
    "-- Setting Thyra_ENABLE_EXAMPLES=ON because ThyraCoreLibs_ENABLE_EXAMPLES=ON"
    # NOTE: These greps are repeated because they are the major purpose of
    # this test!
  )
# NOTE: The above test verifies that enabling just a subpackage and tests will
# enable both the parent package (Thyra in this case) and the parent package's
# tests and examples.


#
# EnableThyraEpetra_EnableTests
#

set(TEST_NAME "EnableThyraEpetra_EnableTests")

read_expected_output_file_into_regex_array(
  "${REDUCED_MOCK_TRILINOS_OUTPUT_DIR}/${TEST_NAME}.txt"
  ${TEST_NAME}_REGEX_ARRAY
  )

create_reduced_dependency_handling_test_case(
  ${TEST_NAME}
  ARGS
    -DTrilinos_ENABLE_ThyraEpetra:BOOL=ON
    -DTrilinos_ENABLE_TESTS:BOOL=ON
   PASS_REGULAR_EXPRESSION_ALL
    ${${TEST_NAME}_REGEX_ARRAY}
    "-- Setting Trilinos_ENABLE_Thyra=ON because Trilinos_ENABLE_ThyraCoreLibs=ON"
    "-- Setting Thyra_ENABLE_TESTS=ON because ThyraEpetra_ENABLE_TESTS=ON"
    "-- Setting Thyra_ENABLE_EXAMPLES=ON because ThyraEpetra_ENABLE_EXAMPLES=ON"
    # NOTE: These greps are repeated because they are the major purpose of
    # this test!
  )
# NOTE: The above test verifies that enabling a mid-level subpackage that
# triggers the enable of an upstream subpackage in the same parent package
# (but not that upstream subpackage's tests) will trigger the enable both the
# parent package (Thyra in this case) and the parent package's tests and
# examples.


#
# EnableAllPackages_DumpDependencies
#

read_expected_output_file_into_regex_array(
  "${REDUCED_MOCK_TRILINOS_OUTPUT_DIR}/ExpectedDependencies.txt"
  REDUCED_EXPECTED_DEPENDENCIES_REGEX_ARRAY
  )
#print_var(REDUCED_EXPECTED_DEPENDENCIES_REGEX_ARRAY)

read_expected_output_file_into_regex_array(
  "${REDUCED_MOCK_TRILINOS_OUTPUT_DIR}/EnableAllPackages.txt"
  REDUCED_EnableAllPackages_REGEX_ARRAY
  )
#print_var(REDUCED_EnableAllPackages_REGEX_ARRAY)

create_reduced_dependency_handling_test_case(
  EnableAllPackages_DumpDependencies
  ARGS
    -DTrilinos_ENABLE_ALL_PACKAGES:BOOL=ON
    -DTrilinos_DUMP_PACKAGE_DEPENDENCIES:BOOL=ON
    -DTrilinos_DUMP_FORWARD_PACKAGE_DEPENDENCIES:BOOL=ON
    -DTrilinos_GENERATE_EXPORT_FILE_DEPENDENCIES:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    ${REDUCED_EXPECTED_DEPENDENCIES_REGEX_ARRAY}
    ${REDUCED_EnableAllPackages_REGEX_ARRAY}
    "Final set of enabled top-level packages:  Teuchos RTOp Epetra Thyra 4"
    "Final set of enabled packages:  Teuchos RTOp Epetra ThyraCoreLibs ThyraEpetra Thyra 6"
    "Final set of non-enabled top-level packages:  Triutils EpetraExt 2"
    "Final set of non-enabled packages:  Triutils EpetraExt ThyraGoodStuff ThyraCrazyStuff ThyraEpetraExt 5"
  )
# NOTE: Above test may be the only test that generates and checks the full
# list of upstream internal package dependencies
# <Package>_FULL_ENABLED_DEP_PACKAGES.

create_reduced_dependency_handling_test_case(
  EnableAllPackages_VerboseConfigure
  ARGS
    -DTrilinos_ENABLE_ALL_PACKAGES:BOOL=ON
    -DTrilinos_VERBOSE_CONFIGURE:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    "MPI_FINDMOD='.*/ReducedMockTrilinos/../../core/std_tpls/FindTPLMPI.cmake'"
    "MPI_TESTGROUP='PT'"
    "MPI_TPLS_LIST_FILE='.*/ReducedMockTrilinos/TPLsList.cmake'"
    "MPI_PACKAGE_BUILD_STATUS='EXTERNAL'"
    "AMD_FINDMOD='cmake/TPLs/FindTPLAMD.cmake'"
    "AMD_TESTGROUP='EX'"
    "AMD_TPLS_LIST_FILE='.*/ReducedMockTrilinos/TPLsList.cmake'"
    "AMD_PACKAGE_BUILD_STATUS='EXTERNAL'"
    "PETSC_FINDMOD='.*/ReducedMockTrilinos/../../common_tpls/FindTPLPETSC.cmake'"
    "PETSC_TESTGROUP='ST'"
    "PETSC_TPLS_LIST_FILE='.*/ReducedMockTrilinos/TPLsList.cmake'"
    "PETSC_PACKAGE_BUILD_STATUS='EXTERNAL'"
    "-- Teuchos_SOURCE_DIR='.*/ReducedMockTrilinos/packages/teuchos'"
    "-- Teuchos_REL_SOURCE_DIR='packages/teuchos'"
    "-- Teuchos_PARENT_PACKAGE=''"
    "-- Teuchos_PARENT_REPOSITORY='Trilinos'"
    "-- Teuchos_PACKAGE_BUILD_STATUS='INTERNAL'"
    "-- RTOp_SOURCE_DIR='.*/ReducedMockTrilinos/packages/rtop'"
    "-- RTOp_REL_SOURCE_DIR='packages/rtop'"
    "-- RTOp_PARENT_PACKAGE=''"
    "-- RTOp_PARENT_REPOSITORY='Trilinos'"
    "-- RTOp_PACKAGE_BUILD_STATUS='INTERNAL'"
    "-- Epetra_SOURCE_DIR='.*/ReducedMockTrilinos/packages/epetra'"
    "-- Epetra_REL_SOURCE_DIR='packages/epetra'"
    "-- Epetra_PARENT_PACKAGE=''"
    "-- Epetra_PARENT_REPOSITORY='Trilinos'"
    "-- Epetra_PACKAGE_BUILD_STATUS='INTERNAL'"
    "-- Triutils_SOURCE_DIR='.*/ReducedMockTrilinos/packages/triutils'"
    "-- Triutils_REL_SOURCE_DIR='packages/triutils'"
    "-- Triutils_PARENT_PACKAGE=''"
    "-- Triutils_PARENT_REPOSITORY='Trilinos'"
    "-- Triutils_PACKAGE_BUILD_STATUS='INTERNAL'"
    "-- EpetraExt_SOURCE_DIR='.*/ReducedMockTrilinos/packages/epetraext'"
    "-- EpetraExt_REL_SOURCE_DIR='packages/epetraext'"
    "-- EpetraExt_PARENT_PACKAGE=''"
    "-- EpetraExt_PARENT_REPOSITORY='Trilinos'"
    "-- EpetraExt_PACKAGE_BUILD_STATUS='INTERNAL'"
    "-- Thyra_SOURCE_DIR='.*/ReducedMockTrilinos/packages/thyra'"
    "-- Thyra_REL_SOURCE_DIR='packages/thyra'"
    "-- Thyra_PARENT_PACKAGE=''"
    "-- Thyra_PARENT_REPOSITORY='Trilinos'"
    "-- Thyra_PACKAGE_BUILD_STATUS='INTERNAL'"
  )
  # NOTE: The above test directly checks some low-level variables that are not
  # checked in other unit tests.


#
# Other ReducedMockTrilinos tests
#


create_reduced_dependency_handling_test_case(
  EnableThyraCoreLibs_UnenabledEnabledPackages
  ARGS
    -DTrilinos_ENABLE_ThyraCoreLibs=ON
    -DTrilinos_UNENABLE_ENABLED_PACKAGES=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Explicitly enabled top-level packages on input [(]by user[)]:  0"
    "Explicitly enabled packages on input [(]by user[)]:  ThyraCoreLibs 1"
    "Explicitly disabled packages on input [(]by user or by default[)]:  ThyraCrazyStuff 1"
    "Setting to empty '' all enabled packages because Trilinos_UNENABLE_ENABLED_PACKAGES='ON'"
    "-- Setting Trilinos_ENABLE_ThyraCoreLibs=''"
    "Final set of enabled top-level packages:  0"
    "Final set of enabled packages:  0"
  )


create_reduced_dependency_handling_test_case(
  EnableAllPackages_RequiredOnly
  ARGS
    -DTrilinos_ENABLE_ALL_PACKAGES:BOOL=ON
    -DTrilinos_ENABLE_ALL_OPTIONAL_PACKAGES:BOOL=OFF
  PASS_REGULAR_EXPRESSION_ALL
    "Final set of enabled top-level packages:  Teuchos RTOp Epetra Thyra 4"
    "Final set of enabled packages:  Teuchos RTOp Epetra ThyraCoreLibs ThyraEpetra Thyra 6"
    "Final set of non-enabled top-level packages:  Triutils EpetraExt 2"
    "Final set of non-enabled packages:  Triutils EpetraExt ThyraGoodStuff ThyraCrazyStuff ThyraEpetraExt "
  )


create_reduced_dependency_handling_test_case(
  EnableAllPackages_ST_TestRequiredTpl_DisableAMD
  ARGS
    -DSHOW_TEST_REQUIRED_TPL_DEP=ON
    -DTrilinos_ENABLE_ALL_PACKAGES=ON
    -DTrilinos_ENABLE_SECONDARY_TESTED_CODE=ON
    -DTrilinos_ENABLE_TESTS=ON
    -DTPL_ENABLE_AMD=OFF
  PASS_REGULAR_EXPRESSION_ALL
    "-- Setting EpetraExt_ENABLE_TESTS=OFF because EpetraExt has a required test/example dependence on disabled package AMD"
    "-- Setting EpetraExt_ENABLE_EXAMPLES=OFF because EpetraExt has a required test/example dependence on disabled package AMD"
    "-- Setting Trilinos_ENABLE_ThyraEpetraExt=ON"
    "Processing enabled top-level package: Triutils [(]Libs, Tests, Examples[)]"
    "Processing enabled top-level package: EpetraExt [(]Libs[)]"
    "Finished configuring Trilinos!"
    "Configuring done"
  )


create_reduced_dependency_handling_test_case(
  EnableAllPackages_ST_TestRequiredPackage_DisableTriutils
  ARGS
    -DSHOW_TEST_REQUIRED_PACKAGE_DEP=ON
    -DTrilinos_ENABLE_ALL_PACKAGES=ON
    -DTrilinos_ENABLE_SECONDARY_TESTED_CODE=ON
    -DTrilinos_ENABLE_TESTS=ON
    -DTrilinos_ENABLE_Triutils=OFF
  PASS_REGULAR_EXPRESSION_ALL
    "-- Setting EpetraExt_ENABLE_TESTS=OFF because EpetraExt has a required test/example dependence on disabled package Triutils"
    "-- Setting EpetraExt_ENABLE_EXAMPLES=OFF because EpetraExt has a required test/example dependence on disabled package Triutils"
    "-- Setting Trilinos_ENABLE_ThyraEpetraExt=ON"
    "Final set of non-enabled top-level packages:  Triutils 1"
    "Processing enabled top-level package: Epetra [(]Libs, Tests, Examples[)]"
    "Processing enabled top-level package: EpetraExt [(]Libs[)]"
    "Finished configuring Trilinos!"
    "Configuring done"
  )


create_reduced_dependency_handling_test_case(
  EnableAllPackages_ST_EpetraExtEnableTriutilsOff
  ARGS
    -DTrilinos_ENABLE_ALL_PACKAGES=ON
    -DTrilinos_ENABLE_SECONDARY_TESTED_CODE=ON
    -DTrilinos_ENABLE_TESTS=ON
    -DEpetraExt_ENABLE_Triutils=OFF
  PASS_REGULAR_EXPRESSION_ALL
    "-- NOTE: EpetraExt_ENABLE_Triutils=OFF is already set so not enabling even though Trilinos_ENABLE_Triutils=ON is set!"
  )


create_reduced_dependency_handling_test_case(
  EnableAllPackages_ST_EpetraExtEnableTriutilsOn_EnableTriutilsOff
  ARGS
    -DTrilinos_ENABLE_ALL_PACKAGES=ON
    -DTrilinos_ENABLE_SECONDARY_TESTED_CODE=ON
    -DTrilinos_ENABLE_TESTS=ON
    -DEpetraExt_ENABLE_Triutils=ON
    -DTrilinos_ENABLE_Triutils=OFF
  PASS_REGULAR_EXPRESSION_ALL
    "-- NOTE: EpetraExt_ENABLE_Triutils=ON but Trilinos_ENABLE_Triutils=OFF is set[.]  Setting EpetraExt_ENABLE_Triutils=OFF"
  )


create_reduced_dependency_handling_test_case(
  EnableAllPackages_ST_EpetraExtEnableTriutilsOn
  ARGS
    -DTrilinos_ENABLE_ALL_PACKAGES=ON
    -DTrilinos_ENABLE_SECONDARY_TESTED_CODE=ON
    -DTrilinos_ENABLE_TESTS=ON
    -DEpetraExt_ENABLE_Triutils=ON
  PASS_REGULAR_EXPRESSION_ALL
    "-- NOTE: EpetraExt_ENABLE_Triutils=ON is already set!"
  )


create_reduced_dependency_handling_test_case(
 ST_EnableEpetraExt_DisableTriutils_EpetraExtEnableTriutilsOn
  ARGS
    -DTrilinos_ENABLE_SECONDARY_TESTED_CODE=ON
    -DTrilinos_ENABLE_TESTS=ON
    -DTrilinos_ENABLE_EpetraExt=ON
    -DTrilinos_ENABLE_Triutils=OFF
    -DEpetraExt_ENABLE_Triutils=ON
  PASS_REGULAR_EXPRESSION_ALL
    "-- NOTE: Setting EpetraExt_ENABLE_Triutils=OFF which was ON because EpetraExt has an optional library dependence on disabled package Triutils"
  )


#
# Test implicit TPL dependencies
#


create_reduced_dependency_handling_test_case(
  IndirectTplDependency_NoImplicitEnableBLAS
  ARGS
    -DTrilinos_EXTRA_REPOSITORIES=extraRepos/DependsOnLAPACK
    -DTrilinos_ENABLE_DependsOnLAPACK=ON
    -DTrilinos_DUMP_PACKAGE_DEPENDENCIES:BOOL=ON
    -DTrilinos_DUMP_FORWARD_PACKAGE_DEPENDENCIES:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    "-- BLAS_FORWARD_LIB_DEFINED_DEPENDENCIES: LAPACK.O."
    "-- LAPACK_LIB_DEFINED_DEPENDENCIES: BLAS.O."
    "Explicitly enabled external packages/TPLs on input [(]by user[)]:  0"
    "Explicitly disabled external packages/TPLs on input [(]by user or by default[)]:  0"
    "-- Setting TPL_ENABLE_LAPACK=ON because DependsOnLAPACK has a required dependence on LAPACK"
    "-- Setting DependsOnLAPACK_ENABLE_LAPACK=ON since Trilinos_ENABLE_DependsOnLAPACK=ON AND TPL_ENABLE_LAPACK=ON"
    "Final set of enabled packages:  DependsOnLAPACK 1"
    "Final set of enabled external packages/TPLs:  LAPACK 1"
    "Final set of non-enabled external packages/TPLs:  .* BLAS .*"
    "-- LAPACK: No enabled dependencies"
    "-- DependsOnLAPACK_LIB_ENABLED_DEPENDENCIES: LAPACK.R."
  )


create_reduced_dependency_handling_test_case(
  IndirectTplDependency_ExplicitEnableBLAS
  ARGS
    -DTrilinos_EXTRA_REPOSITORIES=extraRepos/DependsOnLAPACK
    -DTrilinos_ENABLE_DependsOnLAPACK=ON
    -DTPL_ENABLE_BLAS=ON
    -DTrilinos_DUMP_PACKAGE_DEPENDENCIES:BOOL=ON
    -DTrilinos_DUMP_FORWARD_PACKAGE_DEPENDENCIES:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Explicitly enabled external packages/TPLs on input [(]by user[)]:  BLAS 1"
    "Explicitly disabled external packages/TPLs on input [(]by user or by default[)]:  0"
    "-- Setting TPL_ENABLE_LAPACK=ON because DependsOnLAPACK has a required dependence on LAPACK"
    "-- Setting DependsOnLAPACK_ENABLE_LAPACK=ON since Trilinos_ENABLE_DependsOnLAPACK=ON AND TPL_ENABLE_LAPACK=ON"
    "Final set of enabled packages:  DependsOnLAPACK 1"
    "Final set of enabled external packages/TPLs:  BLAS LAPACK 2"
    "Processing enabled external package/TPL: BLAS [(]enabled explicitly, disable with -DTPL_ENABLE_BLAS=OFF[)]"
    "Processing enabled external package/TPL: LAPACK [(]enabled by DependsOnLAPACK, disable with -DTPL_ENABLE_LAPACK=OFF[)]"
    "-- LAPACK_LIB_ENABLED_DEPENDENCIES: BLAS.O."
    "-- DependsOnLAPACK_LIB_ENABLED_DEPENDENCIES: LAPACK.R."
  )


create_reduced_dependency_handling_test_case(
  IndirectTplDependency_ExplicitDisableBLAS
  ARGS
    -DTrilinos_EXTRA_REPOSITORIES=extraRepos/DependsOnLAPACK
    -DTPL_ENABLE_BLAS=OFF
    -DTrilinos_ENABLE_DependsOnLAPACK=ON
    -DTrilinos_DUMP_PACKAGE_DEPENDENCIES:BOOL=ON
    -DTrilinos_DUMP_FORWARD_PACKAGE_DEPENDENCIES:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    "-- BLAS_FORWARD_LIB_DEFINED_DEPENDENCIES: LAPACK.O."
    "-- LAPACK_LIB_DEFINED_DEPENDENCIES: BLAS.O."
    "Explicitly enabled external packages/TPLs on input [(]by user[)]:  0"
    "Explicitly disabled external packages/TPLs on input [(]by user or by default[)]:  BLAS 1"
    "-- Setting TPL_ENABLE_LAPACK=ON because DependsOnLAPACK has a required dependence on LAPACK"
    "-- Setting DependsOnLAPACK_ENABLE_LAPACK=ON since Trilinos_ENABLE_DependsOnLAPACK=ON AND TPL_ENABLE_LAPACK=ON"
    "Final set of enabled packages:  DependsOnLAPACK 1"
    "Final set of enabled external packages/TPLs:  LAPACK 1"
    "Final set of non-enabled external packages/TPLs:  .* BLAS .*"
    "-- LAPACK: No enabled dependencies"
    "-- DependsOnLAPACK_LIB_ENABLED_DEPENDENCIES: LAPACK.R."
  )
# NOTE: The above test ensures that the explicit disable of an upstream TPL
# does not implicitly disable a downstream TPL (see TriBITSPub/TriBITS#557).
# This was breaking use cases where people were enabling Netcdf but disabling
# HDF5 (and that is a valid configuration when Netcdf is built without HDF5).


#
# Test treating internal packages as TPLs with ReducedMockTrilinos
#


create_reduced_dependency_handling_test_case(
  ST_TplEnableRTOpOn_EnableAllPackages_EnableTests
  ARGS
    -DTPL_ENABLE_RTOp=ON
    -DTrilinos_ENABLE_ALL_PACKAGES=ON
    -DTrilinos_ENABLE_SECONDARY_TESTED_CODE=ON
    -DTrilinos_ENABLE_TESTS=ON
    -DTrilinos_DUMP_PACKAGE_BUILD_STATUS=ON
  PASS_REGULAR_EXPRESSION_ALL

    "Initial package build status:"
    "-- Initial: MPI_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Initial: BLAS_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Initial: LAPACK_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Initial: Boost_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Initial: UMFPACK_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Initial: AMD_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Initial: PETSC_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Initial: Teuchos_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Initial: RTOp_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Initial: Epetra_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Initial: Triutils_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Initial: EpetraExt_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Initial: ThyraCoreLibs_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Initial: ThyraGoodStuff_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Initial: ThyraCrazyStuff_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Initial: ThyraEpetra_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Initial: ThyraEpetraExt_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Initial: Thyra_PACKAGE_BUILD_STATUS=INTERNAL"

    "Adjust the set of internal and external packages:"
    "-- Treating internal package RTOp as EXTERNAL because TPL_ENABLE_RTOp=ON"
    "-- Treating internal package Teuchos as EXTERNAL because downstream package RTOp being treated as EXTERNAL"

    "Final package build status [(]enabled only[)]:"
    "-- Final: BLAS_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: LAPACK_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: Teuchos_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: RTOp_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: Epetra_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Final: Triutils_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Final: EpetraExt_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Final: ThyraCoreLibs_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Final: ThyraGoodStuff_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Final: ThyraEpetra_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Final: ThyraEpetraExt_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Final: Thyra_PACKAGE_BUILD_STATUS=INTERNAL"

    "Getting information for all enabled external packages/TPLs ..."
    "Processing enabled external package/TPL: BLAS [(]enabled by Epetra, disable with -DTPL_ENABLE_BLAS=OFF[)]"
    "Processing enabled external package/TPL: LAPACK [(]enabled by Epetra, disable with -DTPL_ENABLE_LAPACK=OFF[)]"
#    "Processing enabled external package/TPL: Teuchos [(]enabled by RTOp, disable with -DTPL_ENABLE_Teuchos=OFF[)]"
#    "Processing enabled external package/TPL: RTOp [(]enabled by TPL_ENABLE_RTOp=ON[)]"
# ToDo: Get above to be printed out!

    "Configuring individual enabled Trilinos packages ..."
    "Processing enabled top-level package: Epetra [(]Libs, Tests, Examples[)]"
    "Processing enabled top-level package: Triutils [(]Libs, Tests, Examples[)]"
    "Processing enabled top-level package: EpetraExt [(]Libs, Tests, Examples[)]"
    "Processing enabled top-level package: Thyra [(]CoreLibs, GoodStuff, Epetra, EpetraExt, Tests, Examples[)]"

  )


create_reduced_dependency_handling_test_case(
  ST_TplEnableThyraCoreLibsOn_EnableAllPackages_EnableTests
  ARGS
    -DTPL_ENABLE_ThyraCoreLibs=ON
    -DTrilinos_ENABLE_ALL_PACKAGES=ON
    -DTrilinos_ENABLE_SECONDARY_TESTED_CODE=ON
    -DTrilinos_ENABLE_TESTS=ON
    -DTrilinos_DUMP_PACKAGE_BUILD_STATUS=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Adjust the set of internal and external packages:"
    "-- Treating internal package Thyra as EXTERNAL because subpackage ThyraCoreLibs being treated as EXTERNAL [(]TPL_ENABLE_ThyraCoreLibs=ON[)]"
    "-- Treating internal package ThyraCoreLibs as EXTERNAL because downstream package Thyra being treated as EXTERNAL"
    "-- Treating internal package ThyraGoodStuff as EXTERNAL because downstream package Thyra being treated as EXTERNAL"
    "-- Treating internal package ThyraEpetra as EXTERNAL because downstream package Thyra being treated as EXTERNAL"
    "-- Treating internal package ThyraEpetraExt as EXTERNAL because downstream package Thyra being treated as EXTERNAL"
    "-- Treating internal package EpetraExt as EXTERNAL because downstream package ThyraEpetraExt being treated as EXTERNAL"
    "-- Treating internal package Epetra as EXTERNAL because downstream package ThyraEpetra being treated as EXTERNAL"
    "-- Treating internal package Teuchos as EXTERNAL because downstream package ThyraCoreLibs being treated as EXTERNAL"
    "-- Treating internal package RTOp as EXTERNAL because downstream package ThyraCoreLibs being treated as EXTERNAL"
    "-- Treating internal package Triutils as EXTERNAL because downstream package EpetraExt being treated as EXTERNAL"

    "Final package build status [(]enabled only[)]:"
    "-- Final: BLAS_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: LAPACK_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: Teuchos_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: RTOp_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: Epetra_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: Triutils_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: EpetraExt_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: ThyraCoreLibs_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: ThyraGoodStuff_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: ThyraEpetra_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: ThyraEpetraExt_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: Thyra_PACKAGE_BUILD_STATUS=EXTERNAL"

    "Final set of enabled top-level packages:  0"
    "Final set of enabled packages:  0"
    "Final set of non-enabled top-level packages:  0"
    "Final set of non-enabled packages:  0"
    "Final set of enabled top-level external packages/TPLs:  BLAS LAPACK Teuchos RTOp Epetra Triutils EpetraExt Thyra 8"
    "Final set of enabled external packages/TPLs:  BLAS LAPACK Teuchos RTOp Epetra Triutils EpetraExt ThyraCoreLibs ThyraGoodStuff ThyraEpetra ThyraEpetraExt Thyra 12"
    "Final set of non-enabled top-level external packages/TPLs:  MPI Boost UMFPACK AMD PETSC 5"
    "Final set of non-enabled external packages/TPLs:  MPI Boost UMFPACK AMD PETSC ThyraCrazyStuff 6"

  )


create_reduced_dependency_handling_test_case(
  TplEnableThyraCoreLibsOn
  ARGS
    -DTPL_ENABLE_ThyraCoreLibs=ON
    -DTrilinos_DUMP_PACKAGE_BUILD_STATUS=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Enabling all required [(]and optional since Trilinos_ENABLE_ALL_OPTIONAL_PACKAGES=ON[)] upstream packages for current set of enabled packages [(]Trilinos_ENABLE_SECONDARY_TESTED_CODE=OFF[)] ..."
    "-- Setting Trilinos_ENABLE_Teuchos=ON because ThyraCoreLibs has a required dependence on Teuchos"
    "-- Setting Trilinos_ENABLE_RTOp=ON because ThyraCoreLibs has a required dependence on RTOp"
    "-- Setting TPL_ENABLE_BLAS=ON because Teuchos has a required dependence on BLAS"
    "-- Setting TPL_ENABLE_LAPACK=ON because Teuchos has a required dependence on LAPACK"

    "Enabling the shell of non-enabled parent packages [(]mostly for show[)] that have at least one subpackage enabled ..."
    "-- Setting Trilinos_ENABLE_Thyra=ON because TPL_ENABLE_ThyraCoreLibs=ON"

    "Adjust the set of internal and external packages:"
    "-- Treating internal package Thyra as EXTERNAL because subpackage ThyraCoreLibs being treated as EXTERNAL [(]TPL_ENABLE_ThyraCoreLibs=ON[)]"
    "-- Treating internal package ThyraCoreLibs as EXTERNAL because downstream package Thyra being treated as EXTERNAL"
    "-- Treating internal package Teuchos as EXTERNAL because downstream package ThyraCoreLibs being treated as EXTERNAL"
    "-- Treating internal package RTOp as EXTERNAL because downstream package ThyraCoreLibs being treated as EXTERNAL"

    "Final package build status [(]enabled only[)]:"
    "-- Final: BLAS_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: LAPACK_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: Teuchos_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: RTOp_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: ThyraCoreLibs_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: Thyra_PACKAGE_BUILD_STATUS=EXTERNAL"

    "Final set of enabled top-level packages:  0"
    "Final set of enabled packages:  0"
    "Final set of non-enabled top-level packages:  Epetra Triutils EpetraExt 3"
    "Final set of non-enabled packages:  Epetra Triutils EpetraExt 3"
    "Final set of enabled external packages/TPLs:  BLAS LAPACK Teuchos RTOp ThyraCoreLibs Thyra 6"
    "Final set of non-enabled external packages/TPLs:  MPI Boost UMFPACK AMD PETSC ThyraGoodStuff ThyraCrazyStuff ThyraEpetra ThyraEpetraExt 9"

  )


# ???


#####################################################################
#
# Unit tests for dependency handling for full set of packages
#
#####################################################################


function(create_dependency_handling_test_case TEST_NAME)

  cmake_parse_arguments(
     #prefix
     PARSE
     #options
     ""
     #one_value_keywords
     ""
     #multi_value_keywords
     "ARGS;PASS_REGULAR_EXPRESSION_ALL"
     ${ARGN}
     )

  tribits_add_advanced_test( DepTests_${TEST_NAME}
    OVERALL_WORKING_DIRECTORY TEST_NAME
    OVERALL_NUM_MPI_PROCS 1
    TEST_0 CMND "${CMAKE_COMMAND}"
      ARGS
        -D${MOCK_PROJECT_NAME}_TRIBITS_DIR:FILEPATH=${${PROJECT_NAME}_TRIBITS_DIR}
        -D${MOCK_PROJECT_NAME}_DEPS_XML_OUTPUT_FILE:STRING=
        -D${MOCK_PROJECT_NAME}_DEPS_HTML_OUTPUT_FILE:STRING=
        -D${MOCK_PROJECT_NAME}_ENABLE_C:BOOL=OFF
        -D${MOCK_PROJECT_NAME}_ENABLE_CXX:BOOL=OFF
        -D${MOCK_PROJECT_NAME}_ENABLE_Fortran:BOOL=OFF
        ${PARSE_ARGS}
        ${MOCK_TRILINOS_DIR}
      PASS_REGULAR_EXPRESSION_ALL ${PARSE_PASS_REGULAR_EXPRESSION_ALL}
    )

endfunction()


create_dependency_handling_test_case(
  EnableAllPackages
  ARGS -DTrilinos_ENABLE_ALL_PACKAGES:BOOL=ON
    -DTrilinos_WARN_ABOUT_MISSING_EXTERNAL_PACKAGES:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Final set of enabled top-level packages:  TrilinosFramework Teuchos RTOp Epetra Zoltan Shards Triutils Tpetra EpetraExt Thyra Isorropia AztecOO Galeri Amesos Intrepid Ifpack ML Stratimikos RBGen 19"
    "NOTE: MissingPackage is being ignored since its directory is missing and MissingPackage_ALLOW_MISSING_EXTERNAL_PACKAGE = TRUE"
  )


read_expected_output_file_into_regex_array(
  "${CMAKE_CURRENT_LIST_DIR}/DepTests_EnableAllPackages_DumpDependencies.txt"
  EnableAllPackages_DumpDependencies_REGEX_ARRAY
  )
#print_var(EnableAllPackages_DumpDependencies_REGEX_ARRAY)

create_dependency_handling_test_case(
  EnableAllPackages_DumpDependencies
  ARGS
    -DTrilinos_ENABLE_ALL_PACKAGES:BOOL=ON
    -DTrilinos_DUMP_PACKAGE_DEPENDENCIES:BOOL=ON
    -DTrilinos_DUMP_FORWARD_PACKAGE_DEPENDENCIES:BOOL=ON
    -DTrilinos_WARN_ABOUT_MISSING_EXTERNAL_PACKAGES:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    "${EnableAllPackages_DumpDependencies_REGEX_ARRAY}"
    "Final set of enabled top-level packages:  TrilinosFramework Teuchos RTOp Epetra Zoltan Shards Triutils Tpetra EpetraExt Thyra Isorropia AztecOO Galeri Amesos Intrepid Ifpack ML Stratimikos RBGen 19"
    "NOTE: MissingPackage is being ignored since its directory is missing and MissingPackage_ALLOW_MISSING_EXTERNAL_PACKAGE = TRUE"
  )


create_dependency_handling_test_case(
  EnableAllPackages_EnableTests
  ARGS
    -DTrilinos_ENABLE_ALL_PACKAGES:BOOL=ON
     -DTrilinos_ENABLE_TESTS:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Final set of enabled top-level packages:  TrilinosFramework Teuchos RTOp Epetra Zoltan Shards Triutils Tpetra EpetraExt Thyra Isorropia AztecOO Galeri Amesos Intrepid Ifpack ML Stratimikos RBGen 19"
    "Setting Teuchos_ENABLE_TESTS=ON"
    "Setting RTOp_ENABLE_TESTS=ON"
    "Setting Epetra_ENABLE_TESTS=ON"
    "Setting ML_ENABLE_TESTS=ON"
    "Setting Stratimikos_ENABLE_TESTS=ON"
    "Setting RBGen_ENABLE_TESTS=ON"
  )


create_dependency_handling_test_case(
  EnableAllPackages_EnableTests_DumpDependencies
  ARGS
    -DTrilinos_ENABLE_ALL_PACKAGES:BOOL=ON
    -DTrilinos_ENABLE_TESTS:BOOL=ON
    -DTrilinos_DUMP_PACKAGE_DEPENDENCIES:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Final set of enabled top-level packages:  TrilinosFramework Teuchos RTOp Epetra Zoltan Shards Triutils Tpetra EpetraExt Thyra Isorropia AztecOO Galeri Amesos Intrepid Ifpack ML Stratimikos RBGen 19"
    "Setting Teuchos_ENABLE_TESTS=ON"
    "Setting RTOp_ENABLE_TESTS=ON"
    "Setting Epetra_ENABLE_TESTS=ON"
    "Setting ML_ENABLE_TESTS=ON"
    "Setting Stratimikos_ENABLE_TESTS=ON"
    "Setting RBGen_ENABLE_TESTS=ON"
  )


create_dependency_handling_test_case(
  DisableEpetra_EnableAllPackages
  ARGS -DTrilinos_ENABLE_Epetra:BOOL=OFF -DTrilinos_ENABLE_ALL_PACKAGES:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Final set of enabled top-level packages:  TrilinosFramework Teuchos RTOp Zoltan Shards Tpetra Thyra Intrepid ML RBGen 10"
  )


create_dependency_handling_test_case(
  EnableEpetra_EnableThyraTpetra_EnableTests_DisableThyraTests
  ARGS -DTrilinos_ENABLE_Epetra=ON -DTrilinos_ENABLE_ThyraTpetra=ON    
    -DTrilinos_ENABLE_TESTS=ON -DThyra_ENABLE_TESTS=OFF
  PASS_REGULAR_EXPRESSION_ALL
    "Disabling subpackage tests/examples based on parent package tests/examples disables ..."
    "-- Setting Thyra_ENABLE_EXAMPLES=OFF because Thyra_ENABLE_TESTS=OFF"
    "-- Setting ThyraTpetra_ENABLE_TESTS=OFF because parent package Thyra_ENABLE_TESTS=OFF"
    "-- Setting ThyraTpetra_ENABLE_EXAMPLES=OFF because parent package Thyra_ENABLE_EXAMPLES=OFF"
    "Enabling all tests and/or examples that have not been explicitly disabled because Trilinos_ENABLE_.TESTS,EXAMPLES.=ON ..."
    "-- Setting Epetra_ENABLE_TESTS=ON"
    "-- Setting Epetra_ENABLE_EXAMPLES=ON"
    "Final set of enabled top-level packages:  Teuchos RTOp Epetra Triutils Tpetra Thyra 6"
    "Final set of enabled packages:  Teuchos RTOp Epetra Triutils Tpetra ThyraCoreLibs ThyraTpetra Thyra 8"
  )


create_dependency_handling_test_case(
  EnableEpetra_EnableThyraTpetra_EnableTests_DisableThyraExamples
  ARGS -DTrilinos_ENABLE_Epetra=ON -DTrilinos_ENABLE_ThyraTpetra=ON    
    -DTrilinos_ENABLE_TESTS=ON -DThyra_ENABLE_EXAMPLES=OFF
  PASS_REGULAR_EXPRESSION_ALL
    "Disabling subpackage tests/examples based on parent package tests/examples disables ..."
    "-- Setting ThyraTpetra_ENABLE_EXAMPLES=OFF because parent package Thyra_ENABLE_EXAMPLES=OFF"
    "Enabling all tests and/or examples that have not been explicitly disabled because Trilinos_ENABLE_.TESTS,EXAMPLES.=ON ..."
    "-- Setting Epetra_ENABLE_TESTS=ON"
    "-- Setting Epetra_ENABLE_EXAMPLES=ON"
    "-- Setting ThyraTpetra_ENABLE_TESTS=ON"
  )


create_dependency_handling_test_case(
  EnableEpetra_EnableThyraTpetra_EnableThyraTests_DisableThyraExamples
  ARGS -DTrilinos_ENABLE_Epetra=ON -DTrilinos_ENABLE_ThyraTpetra=ON    
    -DThyra_ENABLE_TESTS=ON -DThyra_ENABLE_EXAMPLES=OFF
  PASS_REGULAR_EXPRESSION_ALL
    "Disabling subpackage tests/examples based on parent package tests/examples disables ..."
    "-- Setting ThyraTpetra_ENABLE_EXAMPLES=OFF because parent package Thyra_ENABLE_EXAMPLES=OFF"
    "Enabling subpackage tests/examples based on parent package tests/examples enables ..."
    "-- Setting ThyraTpetra_ENABLE_TESTS=ON because parent package Thyra_ENABLE_TESTS=ON"
  )


create_dependency_handling_test_case(
  EnableEpetra_EnableThyraTpetra_EnableTests_DisableThyraTests_DisableThyraExamples
  ARGS -DTrilinos_ENABLE_Epetra=ON -DTrilinos_ENABLE_ThyraTpetra=ON    
    -DTrilinos_ENABLE_TESTS=ON -DThyra_ENABLE_TESTS=OFF -DThyra_ENABLE_EXAMPLES=OFF
  PASS_REGULAR_EXPRESSION_ALL
    "Disabling subpackage tests/examples based on parent package tests/examples disables ..."
    "-- Setting ThyraTpetra_ENABLE_TESTS=OFF because parent package Thyra_ENABLE_TESTS=OFF"
    "-- Setting ThyraTpetra_ENABLE_EXAMPLES=OFF because parent package Thyra_ENABLE_EXAMPLES=OFF"
    "Enabling all tests and/or examples that have not been explicitly disabled because Trilinos_ENABLE_.TESTS,EXAMPLES.=ON ..."
    ""
    "-- Setting Epetra_ENABLE_TESTS=ON"
    "-- Setting Epetra_ENABLE_EXAMPLES=ON"
  FAIL_REGULAR_EXPRESSION
    "-- Setting Thyra_ENABLE_EXAMPLES=OFF because Thyra_ENABLE_TESTS=OFF"
  )


create_dependency_handling_test_case(
  EnableEpetra_EnableThyra_EnableTests_DisableThyraTests_EnableThyraTpetraTests_EnableThyraTpetraExamples
  ARGS -DTrilinos_ENABLE_Epetra=ON -DTrilinos_ENABLE_Thyra=ON    
    -DTrilinos_ENABLE_TESTS=ON -DThyra_ENABLE_TESTS=OFF -DThyraTpetra_ENABLE_TESTS=ON -DThyraTpetra_ENABLE_EXAMPLES=ON 
  PASS_REGULAR_EXPRESSION_ALL
    "Disabling subpackage tests/examples based on parent package tests/examples disables ..."
    "-- Setting Thyra_ENABLE_EXAMPLES=OFF because Thyra_ENABLE_TESTS=OFF"
    "-- Setting ThyraCoreLibs_ENABLE_TESTS=OFF because parent package Thyra_ENABLE_TESTS=OFF"
    "-- Setting ThyraEpetra_ENABLE_TESTS=OFF because parent package Thyra_ENABLE_TESTS=OFF"
    "-- Setting ThyraEpetraExt_ENABLE_TESTS=OFF because parent package Thyra_ENABLE_TESTS=OFF"
    "-- Setting ThyraCoreLibs_ENABLE_EXAMPLES=OFF because parent package Thyra_ENABLE_EXAMPLES=OFF"
    "-- Setting ThyraEpetra_ENABLE_EXAMPLES=OFF because parent package Thyra_ENABLE_EXAMPLES=OFF"
    "-- Setting ThyraEpetraExt_ENABLE_EXAMPLES=OFF because parent package Thyra_ENABLE_EXAMPLES=OFF"
    "Enabling all tests and/or examples that have not been explicitly disabled because Trilinos_ENABLE_.TESTS,EXAMPLES.=ON ..."
    "-- Setting Epetra_ENABLE_TESTS=ON"
    "-- Setting Epetra_ENABLE_EXAMPLES=ON"
  FAIL_REGULAR_EXPRESSION
    "-- Setting ThyraTpetra_ENABLE_TESTS=OFF because parent package Thyra_ENABLE_TESTS=OFF"
    "-- Setting ThyraTpetra_ENABLE_EXAMPLES=OFF because parent package Thyra_ENABLE_EXAMPLES=OFF"
  )


create_dependency_handling_test_case(
  EnableThyra_EnableExamples_EnableTestsEmpty_DisableThyraExamples_EnableThyraTests
  ARGS -DTrilinos_ENABLE_Thyra=ON
    -DTrilinos_ENABLE_EXAMPLES=ON -DTrilinos_ENABLE_TESTS= -DThyra_ENABLE_EXAMPLES=OFF -DThyra_ENABLE_TESTS=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Disabling subpackage tests/examples based on parent package tests/examples disables ..."
    "-- Setting ThyraCoreLibs_ENABLE_EXAMPLES=OFF because parent package Thyra_ENABLE_EXAMPLES=OFF"
    "-- Setting ThyraEpetra_ENABLE_EXAMPLES=OFF because parent package Thyra_ENABLE_EXAMPLES=OFF"
    "-- Setting ThyraEpetraExt_ENABLE_EXAMPLES=OFF because parent package Thyra_ENABLE_EXAMPLES=OFF"
    "-- Setting ThyraTpetra_ENABLE_EXAMPLES=OFF because parent package Thyra_ENABLE_EXAMPLES=OFF"
    "Enabling subpackage tests/examples based on parent package tests/examples enables ..."
    "-- Setting ThyraCoreLibs_ENABLE_TESTS=ON because parent package Thyra_ENABLE_TESTS=ON"
    "-- Setting ThyraEpetra_ENABLE_TESTS=ON because parent package Thyra_ENABLE_TESTS=ON"
    "-- Setting ThyraEpetraExt_ENABLE_TESTS=ON because parent package Thyra_ENABLE_TESTS=ON"
    "-- Setting ThyraTpetra_ENABLE_TESTS=ON because parent package Thyra_ENABLE_TESTS=ON"
  )


create_dependency_handling_test_case(
  TestTrueFalse
  ARGS -DTrilinos_ENABLE_ALL_PACKAGES=TRUE -DTrilinos_ENABLE_Zoltan=TRUE
    -DTrilinos_ENABLE_TEST=TRUE -DTPL_ENABLE_BLAS=FALSE
    #-DTrilinos_DUMP_PACKAGE_DEPENDENCIES:BOOL=ON
    #-DTrilinos_DUMP_FORWARD_PACKAGE_DEPENDENCIES:BOOL=ON
    #-DTrilinos_VERBOSE_CONFIGURE=TRUE
  PASS_REGULAR_EXPRESSION_ALL
    "Explicitly enabled top-level packages on input .by user.:  Zoltan 1"
    "Explicitly disabled top-level packages on input .by user or by default.:  Stokhos 1"
    "Explicitly disabled external packages/TPLs on input .by user or by default.:  MPI BLAS 2"
    "-- Setting Trilinos_ENABLE_Teuchos=OFF because Teuchos has a required library dependence on disabled package BLAS"
    "-- Setting Trilinos_ENABLE_Epetra=OFF because Epetra has a required library dependence on disabled package BLAS"
    "-- Setting Trilinos_ENABLE_TrilinosFramework=ON"
    "Final set of enabled top-level packages:  TrilinosFramework Zoltan Shards 3"
    "Final set of enabled packages:  TrilinosFramework Zoltan Shards 3"
    "Final set of non-enabled top-level packages:  Teuchos RTOp Epetra Triutils Tpetra EpetraExt Stokhos Sacado Thyra Isorropia AztecOO Galeri Amesos Intrepid Ifpack ML Belos Stratimikos RBGen Phalanx Panzer 21"
    "Final set of non-enabled packages:  Teuchos RTOp Epetra Triutils Tpetra EpetraExt Stokhos Sacado ThyraCoreLibs ThyraGoodStuff ThyraCrazyStuff ThyraEpetra ThyraEpetraExt ThyraTpetra Thyra Isorropia AztecOO Galeri Amesos Intrepid Ifpack ML Belos Stratimikos RBGen Phalanx Panzer 27"
    "Final set of enabled external packages/TPLs:  0"
  )
# Above test makes sure that TRUE/FALSE also processed correctly for enable
# vars.


create_dependency_handling_test_case(
  EnableEpetra_DisableTeuchos_EnableAllForwardPackages
  ARGS -DTrilinos_ENABLE_Epetra:BOOL=ON -DTrilinos_ENABLE_Teuchos:BOOL=OFF
    -DTrilinos_ENABLE_ALL_FORWARD_DEP_PACKAGES:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Setting Trilinos_ENABLE_RTOp=OFF because RTOp has a required library dependence on disabled package Teuchos"
    "Final set of enabled top-level packages:  Epetra Zoltan Triutils AztecOO ML 5"
  )


create_dependency_handling_test_case(
  EnableEpetra_DisableTriutils_EnableAllForwardPackages
  ARGS -DTrilinos_ENABLE_Epetra:BOOL=ON -DTrilinos_ENABLE_Triutils:BOOL=OFF
    -DTrilinos_ENABLE_ALL_FORWARD_DEP_PACKAGES:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Disabling forward required packages and optional intra-package support that have a dependency on disabled packages Trilinos_ENABLE_<TRIBITS_PACKAGE>=OFF [(]or TPL_ENABLE_<TRIBITS_EXTERNAL_PACKAGE>=OFF[)] ..."
    "-- Setting Trilinos_ENABLE_AztecOO=OFF because AztecOO has a required library dependence on disabled package Triutils"
    "Sweep backward enabling all forward test dependent packages because Trilinos_ENABLE_ALL_FORWARD_DEP_PACKAGES=ON"
    "-- Setting Trilinos_ENABLE_Intrepid=ON because Trilinos_ENABLE_Amesos=ON"
  FAIL_REGULAR_EXPRESSION
    "-- Setting Trilinos_ENABLE_Tpetra=ON because Trilinos_ENABLE_Triutils=ON"
  )
  # NOTE: The above test checks that a loop runs to enable needed test
  # dependencies that was not being tested in any other test in TriBITS (as
  # part of the refactoring for #63).


create_dependency_handling_test_case(
  DisableEpetra_DisableTeuchos_EnableAllPackages
  ARGS -DTrilinos_ENABLE_Epetra:BOOL=OFF -DTrilinos_ENABLE_Teuchos:BOOL=OFF -DTrilinos_ENABLE_ALL_PACKAGES:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Final set of enabled top-level packages:  TrilinosFramework Zoltan Shards ML 4"
  )


create_dependency_handling_test_case(
  EnableTeuchos_EnableAllForwardPackages
  ARGS -DTrilinos_ENABLE_Teuchos:BOOL=ON -DTrilinos_ENABLE_ALL_FORWARD_DEP_PACKAGES:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Final set of enabled top-level packages:  Teuchos RTOp Epetra Zoltan Shards Triutils Tpetra EpetraExt Thyra Isorropia AztecOO Galeri Amesos Intrepid Ifpack ML Stratimikos RBGen 18"
  )


create_dependency_handling_test_case(
  EnableEpetraExt_EnableAllForwardPackages
  ARGS -DTrilinos_ENABLE_EpetraExt:BOOL=ON -DTrilinos_ENABLE_ALL_FORWARD_DEP_PACKAGES:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Final set of enabled top-level packages:  Teuchos RTOp Epetra Zoltan Shards Triutils Tpetra EpetraExt Thyra Isorropia AztecOO Galeri Amesos Intrepid Ifpack ML Stratimikos RBGen 18"
  )


create_dependency_handling_test_case(
  EnableEpetraExt
  ARGS -DTrilinos_ENABLE_EpetraExt:BOOL=ON -DTrilinos_ENABLE_ALL_OPTIONAL_PACKAGES:BOOL=OFF
  PASS_REGULAR_EXPRESSION_ALL
    "Final set of enabled top-level packages:  Teuchos Epetra EpetraExt 3"
  )


create_dependency_handling_test_case(
  EnableEpetraExt_EnableAllOptionalPackages
  ARGS -DTrilinos_ENABLE_EpetraExt:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Final set of enabled top-level packages:  Teuchos Epetra Zoltan Triutils EpetraExt 5"
  )


create_dependency_handling_test_case(
  EnableEpetraExt_DisableAztecOO_EnableAllForwardPackages
  ARGS -DTrilinos_ENABLE_EpetraExt:BOOL=ON -DTrilinos_ENABLE_AztecOO:BOOL=OFF
    -DTrilinos_ENABLE_ALL_FORWARD_DEP_PACKAGES:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    "NOTE: Not Setting Trilinos_ENABLE_Belos=ON even though Stratimikos has an optional dependence on Belos because Trilinos_ENABLE_SECONDARY_TESTED_CODE=OFF"
    "NOTE: Not Setting Trilinos_ENABLE_Sacado=ON even though Intrepid has an optional dependence on Sacado because Trilinos_ENABLE_SECONDARY_TESTED_CODE=OFF"
    "Final set of enabled top-level packages:  Teuchos RTOp Epetra Zoltan Shards Triutils Tpetra EpetraExt Thyra Isorropia Galeri Amesos Intrepid Ifpack ML Stratimikos RBGen 17"
  )


create_dependency_handling_test_case(
  EnableAmesos_DisableZoltan_EnableAllForwardPackages
  ARGS -DTrilinos_ENABLE_Amesos:BOOL=ON -DTrilinos_ENABLE_Zoltan:BOOL=OFF
    -DTrilinos_ENABLE_ALL_FORWARD_DEP_PACKAGES:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Final set of enabled top-level packages:  Teuchos RTOp Epetra Shards Triutils EpetraExt Thyra AztecOO Galeri Amesos Intrepid Ifpack ML Stratimikos 14"
  )


create_dependency_handling_test_case(
  EnableThyraCoreLibs_EnableTests
  ARGS -DTrilinos_ENABLE_ThyraCoreLibs:BOOL=ON -DTrilinos_ENABLE_TESTS:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Setting Trilinos_ENABLE_Thyra=ON because Trilinos_ENABLE_ThyraCoreLibs=ON"
    "Setting Thyra_ENABLE_TESTS=ON because ThyraCoreLibs_ENABLE_TESTS=ON"
    "Setting Thyra_ENABLE_EXAMPLES=ON because ThyraCoreLibs_ENABLE_EXAMPLES=ON"
    "Final set of enabled top-level packages:  Teuchos RTOp Thyra 3"
    "Final set of enabled packages:  Teuchos RTOp ThyraCoreLibs Thyra 4"
  )


create_dependency_handling_test_case(
  EnableThyra_EnableAllForwardPackages
  ARGS -DTrilinos_ENABLE_Thyra:BOOL=ON -DTrilinos_ENABLE_ALL_FORWARD_DEP_PACKAGES:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Explicitly enabled top-level packages on input .by user.:  Thyra 1"
    "Enabling subpackages for hard enables of parent packages due to Trilinos_ENABLE_<PARENT_PACKAGE>=ON ..."
    "Setting subpackage enable Trilinos_ENABLE_ThyraCoreLibs=ON because parent package Trilinos_ENABLE_Thyra=ON"
    "Setting subpackage enable Trilinos_ENABLE_ThyraEpetra=ON because parent package Trilinos_ENABLE_Thyra=ON"
    "Setting subpackage enable Trilinos_ENABLE_ThyraEpetraExt=ON because parent package Trilinos_ENABLE_Thyra=ON"
    "Setting subpackage enable Trilinos_ENABLE_ThyraTpetra=ON because parent package Trilinos_ENABLE_Thyra=ON"
    "Sweep forward enabling all forward library dependent packages because Trilinos_ENABLE_ALL_FORWARD_DEP_PACKAGES=ON ..."
    "Setting Trilinos_ENABLE_Stratimikos=ON because Trilinos_ENABLE_ThyraCoreLibs=ON"
    "Final set of enabled top-level packages:  .+ Thyra .+ Stratimikos"
    "Final set of non-enabled packages:  .+ ThyraGoodStuff ThyraCrazyStuff"
  )


create_dependency_handling_test_case(
  EnableThyra_DisableThyraEpetraExt
  ARGS -DTrilinos_ENABLE_Thyra:BOOL=ON -DTrilinos_ENABLE_ThyraEpetraExt:BOOL=OFF
  PASS_REGULAR_EXPRESSION_ALL
    "Setting subpackage enable Trilinos_ENABLE_ThyraCoreLibs=ON because parent package Trilinos_ENABLE_Thyra=ON"
    "Setting subpackage enable Trilinos_ENABLE_ThyraEpetra=ON because parent package Trilinos_ENABLE_Thyra=ON"
    "Setting subpackage enable Trilinos_ENABLE_ThyraTpetra=ON because parent package Trilinos_ENABLE_Thyra=ON"
    "Setting Thyra_ENABLE_ThyraCrazyStuff=OFF because Thyra has an optional library dependence on disabled package ThyraCrazyStuff"
    "Setting Trilinos_ENABLE_Stratimikos=OFF because Stratimikos has a required library dependence on disabled package ThyraEpetraExt"
    "Setting Thyra_ENABLE_ThyraEpetraExt=OFF because Thyra has an optional library dependence on disabled package ThyraEpetraExt"
    "Final set of enabled top-level packages:  Teuchos RTOp Epetra Triutils Tpetra Thyra 6"
    "Final set of enabled packages:  Teuchos RTOp Epetra Triutils Tpetra ThyraCoreLibs ThyraEpetra ThyraTpetra Thyra 9"
    "Final set of non-enabled top-level packages:  TrilinosFramework Zoltan Shards EpetraExt Stokhos Sacado Isorropia AztecOO Galeri Amesos Intrepid Ifpack ML Belos Stratimikos RBGen Phalanx Panzer 18"
    "Final set of non-enabled packages:  TrilinosFramework Zoltan Shards EpetraExt Stokhos Sacado ThyraGoodStuff ThyraCrazyStuff ThyraEpetraExt Isorropia AztecOO Galeri Amesos Intrepid Ifpack ML Belos Stratimikos RBGen Phalanx Panzer 21"
  )


create_dependency_handling_test_case(
  EnableThyraEpetraExt
  ARGS -DTrilinos_ENABLE_ThyraEpetraExt:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Explicitly enabled top-level packages on input .by user.:  0"
    "Explicitly enabled packages on input .by user.:  ThyraEpetraExt 1"
    "Setting Trilinos_ENABLE_ThyraEpetra=ON because ThyraEpetraExt has a required dependence on ThyraEpetra"
    "Setting Trilinos_ENABLE_ThyraCoreLibs=ON because ThyraEpetra has a required dependence on ThyraCoreLibs"
    "Setting Trilinos_ENABLE_Teuchos=ON because ThyraCoreLibs has a required dependence on Teuchos"
    "Setting Trilinos_ENABLE_Thyra=ON because Trilinos_ENABLE_ThyraCoreLibs=ON"
    "Final set of enabled top-level packages:  Teuchos RTOp Epetra Zoltan Triutils EpetraExt Thyra 7"
    "Final set of non-enabled packages:  .+ ThyraGoodStuff ThyraCrazyStuff ThyraTpetra .+"
  )


create_dependency_handling_test_case(
  DisableThyra_EnableThyraEpetraExt
  ARGS -DTrilinos_ENABLE_Thyra:BOOL=OFF -DTrilinos_ENABLE_ThyraEpetraExt:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Setting subpackage enable Trilinos_ENABLE_ThyraEpetraExt=OFF because parent package Trilinos_ENABLE_Thyra=OFF"
    "Final set of enabled top-level packages:  0"
    "Final set of enabled packages:  0"
  )


create_dependency_handling_test_case(
  EnableThyra_DisableThyraEpetra_EnableThyraEpetraExt_DisableEnabledDownstreamPackages
  ARGS -DTrilinos_ENABLE_Thyra:BOOL=ON -DTrilinos_ENABLE_ThyraEpetra:BOOL=OFF
    -DTrilinos_ENABLE_ThyraEpetraExt:BOOL=ON
    -DTrilinos_DISABLE_ENABLED_FORWARD_DEP_PACKAGES=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Explicitly enabled top-level packages on input .by user.:  Thyra 1"
    "Explicitly enabled packages on input .by user.:  ThyraEpetraExt Thyra 2"
    "Explicitly disabled packages on input .by user or by default.:  .+ ThyraEpetra"
    "NOTE: Setting Trilinos_ENABLE_ThyraEpetraExt=OFF which was 'ON' because ThyraEpetraExt has a required library dependence on disabled package ThyraEpetra but Trilinos_DISABLE_ENABLED_FORWARD_DEP_PACKAGES=ON!"
    "Setting Thyra_ENABLE_ThyraEpetra=OFF because Thyra has an optional library dependence on disabled package ThyraEpetra"
    "Final set of enabled top-level packages:  Teuchos RTOp Epetra Triutils Tpetra Thyra 6"
    "Final set of enabled packages:  Teuchos RTOp Epetra Triutils Tpetra ThyraCoreLibs ThyraTpetra Thyra 8"
  )


create_dependency_handling_test_case(
  EnableThyra_DisableEpetra_EnableThyraEpetraExt_DisableEnabledDownstreamPackages
  ARGS -DTrilinos_ENABLE_Thyra:BOOL=ON -DTrilinos_ENABLE_Epetra:BOOL=OFF
    -DTrilinos_ENABLE_ThyraEpetraExt:BOOL=ON
    -DTrilinos_DISABLE_ENABLED_FORWARD_DEP_PACKAGES=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Explicitly enabled top-level packages on input .by user.:  Thyra 1"
    "Explicitly enabled packages on input .by user.:  ThyraEpetraExt Thyra 2"
    "Explicitly disabled top-level packages on input .by user or by default.:  Epetra"
    "Setting Trilinos_ENABLE_ThyraEpetra=OFF because ThyraEpetra has a required library dependence on disabled package Epetra"
    "NOTE: Setting Trilinos_ENABLE_ThyraEpetraExt=OFF which was 'ON' because ThyraEpetraExt has a required library dependence on disabled package EpetraExt but Trilinos_DISABLE_ENABLED_FORWARD_DEP_PACKAGES=ON!"
    "Final set of enabled top-level packages:  Teuchos RTOp Tpetra Thyra 4"
    "Final set of enabled packages:  Teuchos RTOp Tpetra ThyraCoreLibs ThyraTpetra Thyra 6"
  )


create_dependency_handling_test_case(
  EnableStratimikos_DisableThyra
  ARGS -DTrilinos_ENABLE_Stratimikos=ON -DTrilinos_ENABLE_Thyra=OFF
  PASS_REGULAR_EXPRESSION_ALL
    "Setting subpackage enable Trilinos_ENABLE_ThyraCoreLibs=OFF because parent package Trilinos_ENABLE_Thyra=OFF"
    "Setting subpackage enable Trilinos_ENABLE_ThyraGoodStuff=OFF because parent package Trilinos_ENABLE_Thyra=OFF"
    "Setting subpackage enable Trilinos_ENABLE_ThyraEpetra=OFF because parent package Trilinos_ENABLE_Thyra=OFF"
    "Setting subpackage enable Trilinos_ENABLE_ThyraEpetraExt=OFF because parent package Trilinos_ENABLE_Thyra=OFF"
    "Setting subpackage enable Trilinos_ENABLE_ThyraTpetra=OFF because parent package Trilinos_ENABLE_Thyra=OFF"
    "ERROR: Setting Trilinos_ENABLE_Stratimikos=OFF which was 'ON' because Stratimikos has a required library dependence on disabled package ThyraCoreLibs"
  )


create_dependency_handling_test_case(
  EnableStratimikos_DisableThyra_DisableEnabledDownstreamPackages
  ARGS -DTrilinos_ENABLE_Stratimikos=ON -DTrilinos_ENABLE_Thyra=OFF
    -DTrilinos_DISABLE_ENABLED_FORWARD_DEP_PACKAGES=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Setting subpackage enable Trilinos_ENABLE_ThyraCoreLibs=OFF because parent package Trilinos_ENABLE_Thyra=OFF"
    "Setting subpackage enable Trilinos_ENABLE_ThyraGoodStuff=OFF because parent package Trilinos_ENABLE_Thyra=OFF"
    "Setting subpackage enable Trilinos_ENABLE_ThyraEpetra=OFF because parent package Trilinos_ENABLE_Thyra=OFF"
    "Setting subpackage enable Trilinos_ENABLE_ThyraEpetraExt=OFF because parent package Trilinos_ENABLE_Thyra=OFF"
    "Setting subpackage enable Trilinos_ENABLE_ThyraTpetra=OFF because parent package Trilinos_ENABLE_Thyra=OFF"
    "NOTE: Setting Trilinos_ENABLE_Stratimikos=OFF which was 'ON' because Stratimikos has a required library dependence on disabled package ThyraCoreLibs but Trilinos_DISABLE_ENABLED_FORWARD_DEP_PACKAGES=ON"
    "Final set of enabled top-level packages:  0"
    "Final set of non-enabled top-level packages:  .+ Teuchos .+ Thyra .+ Stratimikos .+"
  )


create_dependency_handling_test_case(
  EnableEpetra_DisableThyraCoreLibs_EnableAllForwardPackages
  ARGS -DTrilinos_ENABLE_Epetra:BOOL=ON -DTrilinos_ENABLE_ThyraCoreLibs:BOOL=OFF
    -DTrilinos_ENABLE_ALL_FORWARD_DEP_PACKAGES:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Final set of enabled top-level packages:  Teuchos Epetra Zoltan Shards Triutils Tpetra EpetraExt Isorropia AztecOO Galeri Amesos Intrepid Ifpack ML RBGen 15"
  )


create_dependency_handling_test_case(
  EnableAllPackages_DefaultTPLs
  ARGS -DTrilinos_ENABLE_ALL_PACKAGES:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Final set of enabled external packages/TPLs:  BLAS LAPACK DUMMY 3"
    "Final set of non-enabled external packages/TPLs:  MPI Boost Scotch METIS ParMETIS CppUnit ADOLC ADIC TVMET y12m SuperLUDist SuperLU UMFPACK AMD PETSC MUMPS 16"
  )


create_dependency_handling_test_case(
  EnableAllPackages_EnableBoost
  ARGS -DTrilinos_ENABLE_ALL_PACKAGES:BOOL=ON -DTPL_ENABLE_Boost:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Final set of enabled external packages/TPLs:  BLAS LAPACK Boost DUMMY 4"
  )


create_dependency_handling_test_case(
  EnableAllPackages_EnableBoostParMETIS
  ARGS -DTrilinos_ENABLE_ALL_PACKAGES:BOOL=ON -DTPL_ENABLE_Boost:BOOL=ON
    -DTPL_ENABLE_ParMETIS:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Final set of enabled external packages/TPLs:  BLAS LAPACK Boost ParMETIS DUMMY 5"
  )


create_dependency_handling_test_case(
  EnableAllPackages_EnableBoost_TeuchosEnableBoostOff
  ARGS -DTrilinos_ENABLE_ALL_PACKAGES:BOOL=ON -DTPL_ENABLE_Boost:BOOL=ON
    -DTeuchos_ENABLE_Boost=OFF
  PASS_REGULAR_EXPRESSION_ALL
    "-- NOTE: Teuchos_ENABLE_Boost=OFF is already set so not enabling even though TPL_ENABLE_Boost=ON is set!"
  )


create_dependency_handling_test_case(
  EnableAllPackages_EnableBoost_TeuchosEnableBoostOn
  ARGS -DTrilinos_ENABLE_ALL_PACKAGES:BOOL=ON -DTPL_ENABLE_Boost:BOOL=ON
    -DTeuchos_ENABLE_Boost=ON
  PASS_REGULAR_EXPRESSION_ALL
    "-- NOTE: Teuchos_ENABLE_Boost=ON is already set!"
  )


create_dependency_handling_test_case(
  EnableZoltan_ZoltanEnableParMETIS
  ARGS  -DTrilinos_ENABLE_Zoltan=ON -DZoltan_ENABLE_ParMETIS=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Setting TPL_ENABLE_ParMETIS=ON because Zoltan_ENABLE_ParMETIS=ON"
    "Final set of enabled external packages/TPLs:  ParMETIS 1"
  )


create_dependency_handling_test_case(
  EnableZoltan_ZoltanEnableParMETIS_TplDisableParMETIS
  ARGS -DTrilinos_ENABLE_Zoltan=ON -DZoltan_ENABLE_ParMETIS=ON -DTPL_ENABLE_ParMETIS=OFF
  PASS_REGULAR_EXPRESSION_ALL
    "-- NOTE: Setting Zoltan_ENABLE_ParMETIS=OFF which was ON because Zoltan has an optional library dependence on disabled package ParMETIS"
    "Final set of enabled external packages/TPLs:  0"
  )


create_dependency_handling_test_case(
  EnablePanzer_DefaultMPI
  ARGS  -DTrilinos_ENABLE_Panzer=ON
    -DTrilinos_ENABLE_ALL_OPTIONAL_PACKAGES:BOOL=OFF
  PASS_REGULAR_EXPRESSION_ALL
    "Setting Trilinos_ENABLE_Panzer=OFF which was 'ON' because Panzer has a required library dependence on disabled package MPI!"
  )


create_dependency_handling_test_case(
  EnablePanzer_EnableMPI
  ARGS  -DTrilinos_ENABLE_Panzer=ON
    -DTPL_ENABLE_MPI:BOOL=ON
    -DTrilinos_ENABLE_ALL_OPTIONAL_PACKAGES:BOOL=OFF
  PASS_REGULAR_EXPRESSION_ALL
    "Final set of enabled top-level packages:  .*Panzer"
  )


create_dependency_handling_test_case(
  EnablePanzer_DisableMPI
  ARGS  -DTrilinos_ENABLE_Panzer=ON
    -DTPL_ENABLE_MPI:BOOL=OFF
    -DTrilinos_ENABLE_ALL_OPTIONAL_PACKAGES:BOOL=OFF
  PASS_REGULAR_EXPRESSION_ALL
    "ERROR: Setting Trilinos_ENABLE_Panzer=OFF which was 'ON' because Panzer has a required library dependence on disabled package MPI!"
    "Configuring incomplete, errors occurred!"
  )


create_dependency_handling_test_case(
  EnablePanzer_DisableMPI_DisableEnabledDownstreamPackages
  ARGS  -DTrilinos_ENABLE_Panzer=ON
    -DTPL_ENABLE_MPI:BOOL=OFF
    -DTrilinos_ENABLE_ALL_OPTIONAL_PACKAGES:BOOL=OFF
    -DTrilinos_DISABLE_ENABLED_FORWARD_DEP_PACKAGES=ON
  PASS_REGULAR_EXPRESSION_ALL
    "NOTE: Setting Trilinos_ENABLE_Panzer=OFF which was 'ON' because Panzer has a required library dependence on disabled package MPI but Trilinos_DISABLE_ENABLED_FORWARD_DEP_PACKAGES=ON"
    "Final set of enabled top-level packages:  0"
    "Final set of non-enabled top-level packages:  .+ Panzer .+"
  )


create_dependency_handling_test_case(
  NoOptionalPackages_EnableSubpackagesOnly
  ARGS
    -DTrilinos_ENABLE_ALL_OPTIONAL_PACKAGES:BOOL=OFF
    -DTrilinos_ENABLE_ThyraEpetra=ON
    -DTrilinos_ENABLE_ThyraGoodStuff=ON
  PASS_REGULAR_EXPRESSION_ALL
    "-- Setting Trilinos_ENABLE_Thyra=ON because Trilinos_ENABLE_ThyraCoreLibs=ON"
    "-- Setting Thyra_ENABLE_ThyraCoreLibs=ON because Trilinos_ENABLE_ThyraCoreLibs=ON"
    "-- Setting Thyra_ENABLE_ThyraGoodStuff=ON because Trilinos_ENABLE_ThyraGoodStuff=ON"
    "-- Setting Thyra_ENABLE_ThyraEpetra=ON because Trilinos_ENABLE_ThyraEpetra=ON"
    "Final set of enabled top-level packages:  Teuchos RTOp Epetra Thyra 4"
    "Final set of enabled packages:  Teuchos RTOp Epetra ThyraCoreLibs ThyraGoodStuff ThyraEpetra Thyra 7"
  )


create_dependency_handling_test_case(
  EnableTpetra_EnableAllForwardPackages
  ARGS  -DTrilinos_ENABLE_Tpetra=ON
    -DTrilinos_ENABLE_ALL_FORWARD_DEP_PACKAGES:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Final set of enabled top-level packages:  Teuchos RTOp Epetra Zoltan Triutils Tpetra EpetraExt Thyra 8"
    "Final set of enabled packages:  Teuchos RTOp Epetra Zoltan Triutils Tpetra EpetraExt ThyraCoreLibs ThyraEpetra ThyraEpetraExt ThyraTpetra Thyra 12"
  )


create_dependency_handling_test_case(
  EnableAllPackages_EnableSecondaryTestedCode_EnableAllOptionalPackges
  ARGS  -DTrilinos_ENABLE_ALL_PACKAGES=ON -DTrilinos_ENABLE_SECONDARY_TESTED_CODE=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Final set of enabled top-level packages:  TrilinosFramework Teuchos RTOp Epetra Zoltan Shards Triutils Tpetra EpetraExt Sacado Thyra Isorropia AztecOO Galeri Amesos Intrepid Ifpack ML Belos Stratimikos RBGen Phalanx 22"
    "Final set of enabled external packages/TPLs:  BLAS LAPACK Boost DUMMY 4"
  )


create_dependency_handling_test_case(
  EnableStratimikos_EnableAllOptionalPackages_BadSystem1
  ARGS  -DTrilinos_ENABLE_Stratimikos=ON
    -DTrilinos_HOSTTYPE:STRING=BadSystem1
  PASS_REGULAR_EXPRESSION_ALL
    "Explicitly disabled top-level packages on input .+:  Stokhos Ifpack ML 3"
    "Setting Stratimikos_ENABLE_Ifpack=OFF because Stratimikos has an optional library dependence on disabled package Ifpack"
    "Setting Stratimikos_ENABLE_ML=OFF because Stratimikos has an optional library dependence on disabled package ML"
    "Final set of enabled top-level packages:  Teuchos RTOp Epetra Zoltan Triutils EpetraExt Thyra AztecOO Galeri Amesos Stratimikos 11"
    "Final set of non-enabled top-level packages:  TrilinosFramework Shards Tpetra Stokhos Sacado Isorropia Intrepid Ifpack ML Belos RBGen Phalanx Panzer 13"
  )


create_dependency_handling_test_case(
  EnableStratimikos_EnableAllOptionalPackages_BadSystem2
  ARGS  -DTrilinos_ENABLE_Stratimikos=ON
    -DTrilinos_HOSTTYPE:STRING=BadSystem2
  PASS_REGULAR_EXPRESSION_ALL
    "Explicitly disabled top-level packages on input .+:  Stokhos Ifpack 2"
    "Setting Stratimikos_ENABLE_Ifpack=OFF because Stratimikos has an optional library dependence on disabled package Ifpack"
    "Final set of enabled top-level packages:  Teuchos RTOp Epetra Zoltan Triutils EpetraExt Thyra Isorropia AztecOO Galeri Amesos ML Stratimikos 13"
    "Final set of enabled packages:  Teuchos RTOp Epetra Zoltan Triutils EpetraExt ThyraCoreLibs ThyraEpetra ThyraEpetraExt Thyra Isorropia AztecOO Galeri Amesos ML Stratimikos 16"
    "Final set of non-enabled top-level packages:  TrilinosFramework Shards Tpetra Stokhos Sacado Intrepid Ifpack Belos RBGen Phalanx Panzer 11"
    "Final set of non-enabled packages:  TrilinosFramework Shards Tpetra Stokhos Sacado ThyraGoodStuff ThyraCrazyStuff ThyraTpetra Intrepid Ifpack Belos RBGen Phalanx Panzer 14"
  )


create_dependency_handling_test_case(
  EnableStratimikos_EnableIfpack_EnableAllOptionalPackages_BadSystem2
  ARGS  -DTrilinos_ENABLE_Stratimikos=ON -DTrilinos_ENABLE_Ifpack=ON
    -DTrilinos_HOSTTYPE:STRING=BadSystem2
  PASS_REGULAR_EXPRESSION_ALL
    "NOTE: User has set Trilinos_ENABLE_Ifpack=ON but the"
    "package Ifpack is not supported on this platform type 'BadSystem2'"
    "Final set of enabled top-level packages:  Teuchos RTOp Epetra Zoltan Triutils EpetraExt Thyra Isorropia AztecOO Galeri Amesos Ifpack ML Stratimikos 14"
    "Final set of enabled packages:  Teuchos RTOp Epetra Zoltan Triutils EpetraExt ThyraCoreLibs ThyraEpetra ThyraEpetraExt Thyra Isorropia AztecOO Galeri Amesos Ifpack ML Stratimikos 17"
  )


create_dependency_handling_test_case(
  preCopyrightTrilinos_EnableTeko
  ARGS -DTrilinos_EXTRA_REPOSITORIES=preCopyrightTrilinos
    -DTrilinos_ENABLE_Teko=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Trilinos_NUM_DEFINED_INTERNAL_TOPLEVEL_PACKAGES='26'"
    "Trilinos_NUM_DEFINED_TPLS='20'"
    "Explicitly enabled top-level packages on input .* Teko 1"
    "Explicitly disabled top-level packages on input .* Stokhos Stalix 2"
    "Setting Trilinos_ENABLE_Teuchos=ON because Teko has a required dependence on Teuchos"
    "Setting Trilinos_ENABLE_Epetra=ON because Teko has a required dependence on Epetra"
    "Setting Trilinos_ENABLE_Thyra=ON because Teko has a required dependence on Thyra"
    "Final set of enabled top-level packages:  Teuchos RTOp Epetra Zoltan Triutils Tpetra EpetraExt Thyra Isorropia AztecOO Galeri Amesos Ifpack ML Stratimikos Teko 16"
    "Final set of non-enabled top-level packages:  TrilinosFramework Shards Stokhos Sacado Intrepid Belos RBGen Phalanx Panzer Stalix 10"
    "Final set of enabled external packages/TPLs:  BLAS LAPACK TekoDepTPL 3"
  )


create_dependency_handling_test_case(
  preCopyrightTrilinos_EnableTeko_InconsistentExtraReposFile
  ARGS -DTrilinos_EXTRA_REPOSITORIES=preCopyrightTrilinos
    -DTrilinos_EXTRAREPOS_FILE=${CMAKE_CURRENT_SOURCE_DIR}/NoPackagesExtraReposFile.cmake
    -DTrilinos_ENABLE_KNOWN_EXTERNAL_REPOS_TYPE=Nightly
    -DTrilinos_IGNORE_MISSING_EXTRA_REPOSITORIES=ON
    #-DTrilinos_VERBOSE_CONFIGURE=ON
    #-DTRIBITS_PROCESS_EXTRAREPOS_LISTS_DEBUG=ON
    -DTrilinos_ENABLE_Teko=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Trilinos_NUM_DEFINED_INTERNAL_TOPLEVEL_PACKAGES='26'"
    "Trilinos_NUM_DEFINED_TPLS='20'"
    "Explicitly enabled top-level packages on input .* Teko 1"
  )


create_dependency_handling_test_case(
  DefaultExtraReposFile_EnableAllPackages_TraceFileProcessing
  ARGS
    -DTrilinos_EXTRAREPOS_FILE=${MOCK_TRILINOS_DIR}/cmake/ExtraRepositoriesList.cmake
    -DTrilinos_ENABLE_KNOWN_EXTERNAL_REPOS_TYPE=Nightly
    -DTrilinos_IGNORE_MISSING_EXTRA_REPOSITORIES=TRUE
    -DTrilinos_TRACE_FILE_PROCESSING=ON
    -DTrilinos_ENABLE_ALL_PACKAGES=ON
  PASS_REGULAR_EXPRESSION_ALL
    "-- File Trace: PROJECT    INCLUDE    .*/MockTrilinos/Version.cmake"
    "-- File Trace: REPOSITORY INCLUDE    .*/MockTrilinos/cmake/CallbackSetupExtraOptions.cmake"
    "-- File Trace: REPOSITORY INCLUDE    .*/MockTrilinos/PackagesList.cmake"
    "-- File Trace: REPOSITORY INCLUDE    .*/MockTrilinos/TPLsList.cmake"
    "-- File Trace: REPOSITORY INCLUDE    .*/MockTrilinos/preCopyrightTrilinos/PackagesList.cmake"
    "-- File Trace: REPOSITORY INCLUDE    .*/MockTrilinos/preCopyrightTrilinos/TPLsList.cmake"
    "-- File Trace: REPOSITORY INCLUDE    .*/MockTrilinos/extraTrilinosRepo/PackagesList.cmake"
    "-- File Trace: REPOSITORY INCLUDE    .*/MockTrilinos/extraTrilinosRepo/TPLsList.cmake"
    "-- File Trace: REPOSITORY INCLUDE    .*/MockTrilinos/cmake/RepositoryDependenciesSetup.cmake"
    "-- File Trace: PROJECT    INCLUDE    .*/MockTrilinos/cmake/ProjectDependenciesSetup.cmake"
    "-- File Trace: PACKAGE    INCLUDE    .*/MockTrilinos/cmake/cmake/Dependencies.cmake"
    "-- File Trace: PACKAGE    INCLUDE    .*/MockTrilinos/packages/teuchos/cmake/Dependencies.cmake"
    "-- File Trace: PACKAGE    INCLUDE    .*/MockTrilinos/packages/thyra/cmake/Dependencies.cmake"
    "-- File Trace: PACKAGE    INCLUDE    .*/MockTrilinos/packages/thyra/src/cmake/Dependencies.cmake"
    "-- File Trace: PACKAGE    INCLUDE    .*/MockTrilinos/packages/thyra/src/good_stuff/cmake/Dependencies.cmake"
    "-- File Trace: PACKAGE    INCLUDE    .*/MockTrilinos/packages/thyra/src/crazy_stuff/cmake/Dependencies.cmake"
    "-- File Trace: PACKAGE    INCLUDE    .*/MockTrilinos/packages/thyra/adapters/epetra/cmake/Dependencies.cmake"
    "-- File Trace: PACKAGE    INCLUDE    .*/MockTrilinos/packages/thyra/adapters/epetraext/cmake/Dependencies.cmake"
    "-- File Trace: PACKAGE    INCLUDE    .*/MockTrilinos/packages/thyra/adapters/tpetra/cmake/Dependencies.cmake"
    "-- File Trace: PACKAGE    INCLUDE    .*/MockTrilinos/preCopyrightTrilinos/teko/cmake/Dependencies.cmake"
    "-- File Trace: PACKAGE    INCLUDE    .*/MockTrilinos/preCopyrightTrilinos/stalix/cmake/Dependencies.cmake"
    "-- File Trace: PACKAGE    INCLUDE    .*/MockTrilinos/extraTrilinosRepo/extrapack/cmake/Dependencies.cmake"
  )


create_dependency_handling_test_case(
  PreAndExtraReposFile_Nightly_EnableAllPackages
  ARGS
    -DTrilinos_EXTRAREPOS_FILE=${CMAKE_CURRENT_SOURCE_DIR}/PreAndExtraRepositoriesList.cmake
    -DTrilinos_ENABLE_KNOWN_EXTERNAL_REPOS_TYPE=Nightly
    -DTrilinos_ENABLE_SECONDARY_TESTED_CODE:BOOL=ON
    -DTrilinos_IGNORE_MISSING_EXTRA_REPOSITORIES=TRUE
    -DTrilinos_ENABLE_ALL_PACKAGES=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Selecting the set of .Nightly. extra repos .ignoring missing repos. [.][.][.]"
    "-- Adding PRE extra Continuous repository preRepoOnePackage"
    "-- Adding POST extra Continuous repository preCopyrightTrilinos"
    "-- Adding POST extra Nightly repository extraTrilinosRepo"
    "NOTE: Ignoring missing extra repo 'Dakota' as requested since .*/examples/MockTrilinos/packages/TriKota/Dakota does not exist"
    "Reading list of PRE extra packages from .*/MockTrilinos/preRepoOnePackage/PackagesList.cmake"
    "Reading list of PRE extra TPLs from .*/MockTrilinos/preRepoOnePackage/TPLsList.cmake"
    "Final set of enabled packages:  preRepoOnePackage TrilinosFramework Teuchos .* Stratimikos RBGen Phalanx Teko ExtraPack [0-9][0-9]"
  )
# NOTE: The above test shows that PRE extra repos are processed correctly and
# their packages are listed before packages in the native project.


create_dependency_handling_test_case(
  PreAndExtraReposFile_Continuous_EnableAllPackages
  ARGS
    -DTrilinos_EXTRAREPOS_FILE=${CMAKE_CURRENT_SOURCE_DIR}/PreAndExtraRepositoriesList.cmake
    -DTrilinos_ENABLE_KNOWN_EXTERNAL_REPOS_TYPE=Continuous
    -DTrilinos_ENABLE_SECONDARY_TESTED_CODE:BOOL=ON
    -DTrilinos_IGNORE_MISSING_EXTRA_REPOSITORIES=TRUE
    -DTrilinos_ENABLE_ALL_PACKAGES=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Selecting the set of .Continuous. extra repos .ignoring missing repos. [.][.][.]"
    "-- Adding PRE extra Continuous repository preRepoOnePackage"
    "-- Adding POST extra Continuous repository preCopyrightTrilinos"
    "-- .NOT. adding POST extra Nightly repository extraTrilinosRepo"
    "NOTE: Ignoring missing extra repo 'Dakota' as requested since .*/examples/MockTrilinos/packages/TriKota/Dakota does not exist"
    "Reading list of PRE extra packages from .*/MockTrilinos/preRepoOnePackage/PackagesList.cmake"
    "Reading list of PRE extra TPLs from .*/MockTrilinos/preRepoOnePackage/TPLsList.cmake"
    "Final set of enabled packages:  preRepoOnePackage TrilinosFramework Teuchos .* Stratimikos RBGen Phalanx Teko [0-9][0-9]"
  )
# NOTE: The above test shows that Nightly repos are not processed but are
# printed out as not being processed!


create_dependency_handling_test_case(
  PreAndExtraReposFile_Continuous_AssertMissing_EnableAllPackages
  ARGS
    -DTrilinos_EXTRAREPOS_FILE=${CMAKE_CURRENT_SOURCE_DIR}/PreAndExtraRepositoriesList.cmake
    -DTrilinos_ENABLE_KNOWN_EXTERNAL_REPOS_TYPE=Continuous
    -DTrilinos_ENABLE_SECONDARY_TESTED_CODE:BOOL=ON
    -DTrilinos_IGNORE_MISSING_EXTRA_REPOSITORIES=FALSE
    -DTrilinos_ENABLE_ALL_PACKAGES=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Selecting the set of .Continuous. extra repos .asserting all selected repos exist. [.][.][.]"
    "-- Adding PRE extra Continuous repository preRepoOnePackage"
    "-- Adding POST extra Continuous repository preCopyrightTrilinos"
    "-- .NOT. adding POST extra Nightly repository extraTrilinosRepo"
    "CMake Error at .*/TribitsProcessExtraRepositoriesList.cmake"
    "ERROR. Skipping missing extra repo .Dakota. since"
    "Configuring incomplete, errors occurred"
  )
# NOTE: The above test shows that a missing repo is flagged and aborts
# configuration and that it prints the right header message!


create_dependency_handling_test_case(
  preCopyrightTrilinos_EnableStalix
  ARGS -DTrilinos_EXTRA_REPOSITORIES=preCopyrightTrilinos
    -DTrilinos_ENABLE_Stalix=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Explicitly enabled top-level packages on input .* Stalix 1"
    "Explicitly disabled top-level packages on input .* Stokhos 1"
    "NOTE: Not Setting Trilinos_ENABLE_ThyraGoodStuff=ON even though Thyra has an optional dependence on ThyraGoodStuff because Trilinos_ENABLE_SECONDARY_TESTED_CODE=OFF"
    "Setting Trilinos_ENABLE_Tpetra=ON because Stalix has a required dependence on Tpetra"
    "Setting Trilinos_ENABLE_Thyra=ON because Stalix has a required dependence on Thyra"
    "Final set of enabled top-level packages:  Teuchos RTOp Epetra Zoltan Triutils Tpetra EpetraExt Sacado Thyra Stalix 10"
    "Final set of non-enabled top-level packages:  TrilinosFramework Shards Stokhos Isorropia AztecOO Galeri Amesos Intrepid Ifpack ML Belos Stratimikos RBGen Phalanx Panzer Teko 16"
  )


create_dependency_handling_test_case(
  preCopyrightTrilinos_ShowInvalidPackageNameError
  ARGS -DTrilinos_EXTRA_REPOSITORIES=preCopyrightTrilinos
    -DSHOW_INVALID_PACKAGE_NAME_ERROR=ON
    -DTrilinos_ASSERT_DEFINED_DEPENDENDCIES=FATAL_ERROR
  PASS_REGULAR_EXPRESSION_ALL
    "CMake Error at .*/TribitsReadDepsFilesCreateDepsGraph.cmake:.+ [(]message[)]:"
    "Error, the package 'Anasazi' is listed as a dependency of the package"
    "'Teko' but the package 'Anasazi' is either not defined or is listed later"
    "in the package order[.]  This may also be an attempt to create a circular"
    "dependency between the packages 'Anasazi' and 'Teko' [(]which is not"
    "allowed[)][.]  Check the spelling of 'Anasazi' or see how it is listed in a"
    "call to tribits_repository_define_packages[(][)] in relation to 'Teko'[.]  To"
    "ignore/disable the undefined package 'Anasazi', set the cache variable"
    "Trilinos_ASSERT_DEFINED_DEPENDENCIES=IGNORE[.]"
  )


create_dependency_handling_test_case(
  ShowInvalidTplNameError
  ARGS -DTrilinos_ASSERT_DEFINED_DEPENDENCIES=FATAL_ERROR
    -DSHOW_INVALID_TPL_NAME_ERROR=ON
  PASS_REGULAR_EXPRESSION_ALL
    "CMake Error at .*/TribitsReadDepsFilesCreateDepsGraph.cmake:.+ [(]message[)]:"
    "Error, the package 'Zlib' is listed as a dependency of the package 'Zoltan'"
    "but the package 'Zlib' is either not defined or is listed later in the"
    "package order."
  )
  # NOTE: The reset of the error message is checked in the test
  # preCopyrightTrilinos_ShowInvalidPackageNameError above.


create_dependency_handling_test_case(
  AssertDefinedDependenciesBadValue
  ARGS -DTrilinos_ASSERT_DEFINED_DEPENDENCIES=BadValue
  PASS_REGULAR_EXPRESSION_ALL
    "CMake Error at .*/tribits/core/utils/TribitsAddEnumCacheVar.cmake:[0-9]+ [(]message[)]:"
    "  Error, the cache var Trilinos_ASSERT_DEFINED_DEPENDENCIES with value"
    "  'BadValue' is not in the list of allowed values: 'FATAL_ERROR',"
    "  'SEND_ERROR', 'WARNING', 'NOTICE', 'IGNORE', 'OFF' [(]default 'FATAL_ERROR'[)]"
  )


create_dependency_handling_test_case(
  preCopyrightTrilinos_ShowInvalidPackageNameAndTplNameError
  ARGS -DTrilinos_EXTRA_REPOSITORIES=preCopyrightTrilinos
    -DSHOW_INVALID_PACKAGE_NAME_ERROR=ON
    -DSHOW_INVALID_TPL_NAME_ERROR=ON
    -DTrilinos_ASSERT_DEFINED_DEPENDENCIES=SEND_ERROR
  PASS_REGULAR_EXPRESSION_ALL
    "CMake Error at .*/TribitsReadDepsFilesCreateDepsGraph.cmake:.+ [(]message[)]:"
    "Error, the package 'Anasazi' is listed as a dependency of the package"
    "Error, the package 'Zlib' is listed as a dependency of the package 'Zoltan'"
  )


create_dependency_handling_test_case(
  preCopyrightTrilinos_ShowInvalidPackageNameAndTplNameError_AssertMissingPackagesOn
  ARGS
    -DSHOW_INVALID_PACKAGE_NAME_ERROR=ON
    -DSHOW_INVALID_TPL_NAME_ERROR=ON
    -DTrilinos_ASSERT_MISSING_PACKAGES=ON
  PASS_REGULAR_EXPRESSION_ALL
    "CMake Deprecation Warning at .*/MessageWrapper.cmake:.+ [(]message[)]:"
    "  Warning, Trilinos_ASSERT_MISSING_PACKAGES='ON' is set and is no longer"
    "  supported! Please set Trilinos_ASSERT_DEFINED_DEPENDENCIES instead [(]see"
    "  build ref[)]!"
    "CMake Error at .*/TribitsReadDepsFilesCreateDepsGraph.cmake:.+ [(]message[)]:"
    "Error, the package 'Zlib' is listed as a dependency of the package 'Zoltan'"
    "ignore/disable the undefined package 'Zlib', set the cache variable"
    "Trilinos_ASSERT_DEFINED_DEPENDENCIES=IGNORE[.]"
  )


create_dependency_handling_test_case(
  preCopyrightTrilinos_ShowInvalidPackageSelfDependency
  ARGS -DTrilinos_EXTRA_REPOSITORIES=preCopyrightTrilinos
    -DSHOW_SELF_PACKAGE_DEPENDENCY_ERROR=ON
    -DTrilinos_ASSERT_DEFINED_DEPENDENDCIES=FATAL_ERROR
  PASS_REGULAR_EXPRESSION_ALL
    "Error, the package 'Teko' is listed as a dependency of itself in the list"
    " 'LIB_REQUIRED_DEP_PACKAGES'!"
  )


create_dependency_handling_test_case(
  preCopyrightTrilinos_ShowInvalidSubpackageSelfDependency
  ARGS
    -DSHOW_SELF_SUBPACKAGE_DEPENDENCY_ERROR=ON
    -DTrilinos_ASSERT_DEFINED_DEPENDENDCIES=FATAL_ERROR
  PASS_REGULAR_EXPRESSION_ALL
    "Error, the package 'ThyraTpetra' is listed as a dependency of itself in the"
     " list 'LIB_REQUIRED_DEP_PACKAGES'!"
  )


create_dependency_handling_test_case(
  MissingExtraRepositoryFail
  ARGS -DTrilinos_EXTRA_REPOSITORIES=MissingExtraRepo
    -DTrilinos_IGNORE_MISSING_EXTRA_REPOSITORIES=OFF
  PASS_REGULAR_EXPRESSION_ALL
    "ERROR: Skipping missing POST extra repo 'MissingExtraRepo' packages list"
    "ERROR: Skipping missing POST extra repo 'MissingExtraRepo' TPLs list"
    "Configuring incomplete, errors occurred"
  )


create_dependency_handling_test_case(
  MissingExtraRepositoryIgnore
  ARGS -DTrilinos_EXTRA_REPOSITORIES=MissingExtraRepo
    -DTrilinos_IGNORE_MISSING_EXTRA_REPOSITORIES=ON
    -DTrilinos_ENABLE_KNOWN_EXTERNAL_REPOS_TYPE=
    -DTRIBITS_PROCESS_EXTRAREPOS_LISTS_DEBUG=TRUE
  PASS_REGULAR_EXPRESSION_ALL
    "NOTE: Ignoring missing POST extra repo 'MissingExtraRepo' packages list file ..+/examples/MockTrilinos/MissingExtraRepo/PackagesList.cmake. on request!"
    "NOTE: Ignoring missing POST extra repo 'MissingExtraRepo' TPLs list file ..+/examples/MockTrilinos/MissingExtraRepo/TPLsList.cmake. on request!"
    "Configuring done"
    "Generating done"
  )


create_dependency_handling_test_case(
  NativeRepositoriesList1_EnableAllPackages_ST
  ARGS -DTrilinos_NATIVE_REPO_FILE_OVERRRIDE=cmake/NativeRepositoriesList1.cmake
    -DTrilinos_ENABLE_SECONDARY_TESTED_CODE:BOOL=ON
    -DTrilinos_ENABLE_ALL_PACKAGES:BOOL=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Reading list of native packages from .*/MockTrilinos/PackagesList.cmake"
    "Reading list of native packages from .*/MockTrilinos/preCopyrightTrilinos/PackagesList.cmake"
    "Reading list of native packages from .*/MockTrilinos/extraTrilinosRepo/PackagesList.cmake"
    "Final set of enabled top-level packages:  TrilinosFramework Teuchos RTOp Epetra Zoltan Shards Triutils Tpetra EpetraExt Sacado Thyra Isorropia AztecOO Galeri Amesos Intrepid Ifpack ML Belos Stratimikos RBGen Phalanx Teko ExtraPack 24"
    "Configuring done"
    "Generating done"
  )


create_dependency_handling_test_case(
  extraTrilinosRepo_EnableExtraPack
  ARGS "-DTrilinos_EXTRA_REPOSITORIES=preCopyrightTrilinos,extraTrilinosRepo"
    -DTrilinos_ENABLE_ExtraPack=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Trilinos_NUM_DEFINED_TPLS='22'"
    "Explicitly enabled top-level packages on input .* ExtraPack 1"
    "Explicitly disabled top-level packages on input .* Stokhos Stalix 2"
    "Setting Trilinos_ENABLE_Teuchos=ON because ExtraPack has a required dependence on Teuchos"
    "Setting Trilinos_ENABLE_Teko=ON because ExtraPack has a required dependence on Teko"
    "NOTE: Not Setting Trilinos_ENABLE_Sacado=ON even though ExtraPack has an optional dependence on Sacado because Trilinos_ENABLE_SECONDARY_TESTED_CODE=OFF"
    "Final set of enabled top-level packages:  Teuchos RTOp Epetra Zoltan Triutils Tpetra EpetraExt Thyra Isorropia AztecOO Galeri Amesos Ifpack ML Stratimikos Teko ExtraPack 17"
    "Final set of non-enabled top-level packages:  TrilinosFramework Shards Stokhos Sacado Intrepid Belos RBGen Phalanx Panzer Stalix 10"
    "Final set of enabled external packages/TPLs:  BLAS LAPACK TekoDepTPL ExtraTPL2 4"
  )


create_dependency_handling_test_case(
  extraTrilinosRepo_EnableExtraPack_EnableExtraTPL1
  ARGS "-DTrilinos_EXTRA_REPOSITORIES=preCopyrightTrilinos,extraTrilinosRepo"
    -DTrilinos_ENABLE_ExtraPack=ON -DTPL_ENABLE_ExtraTPL1=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Trilinos_NUM_DEFINED_TPLS='22'"
    "Explicitly enabled top-level packages on input .* ExtraPack 1"
    "Final set of enabled external packages/TPLs:  BLAS LAPACK TekoDepTPL ExtraTPL1 ExtraTPL2 5"
  )


create_dependency_handling_test_case(
  extraTrilinosRepo_ReplacePackagesList
  ARGS -DTrilinos_EXTRA_REPOSITORIES=preCopyrightTrilinos
    -DpreCopyrightTrilinos_PACKAGES_LIST_FILE=cmake/Reduced_preCopyrightTrilinos_PackagesList.cmake
  PASS_REGULAR_EXPRESSION_ALL
    "Reading list of POST extra packages from .*/MockTrilinos/cmake/Reduced_preCopyrightTrilinos_PackagesList.cmake"
    "Trilinos_NUM_DEFINED_INTERNAL_TOPLEVEL_PACKAGES='24'"
    "Final set of non-enabled packages:  .* Phalanx Panzer Stalix 31"
  )


create_dependency_handling_test_case(
  ENABLE_KNOWN_EXTERNAL_REPOS_TYPE_CI_EnableTeko
  ARGS -DTrilinos_ENABLE_KNOWN_EXTERNAL_REPOS_TYPE:STRING=Continuous
   -DTrilinos_IGNORE_MISSING_EXTRA_REPOSITORIES=ON
   -DTrilinos_ENABLE_Teko=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Explicitly enabled top-level packages on input .* Teko 1"
    "Explicitly disabled top-level packages on input .* Stokhos Stalix 2"
    "Setting Trilinos_ENABLE_Teuchos=ON because Teko has a required dependence on Teuchos"
    "Setting Trilinos_ENABLE_Epetra=ON because Teko has a required dependence on Epetra"
    "Setting Trilinos_ENABLE_Thyra=ON because Teko has a required dependence on Thyra"
    "Final set of enabled top-level packages:  Teuchos RTOp Epetra Zoltan Triutils Tpetra EpetraExt Thyra Isorropia AztecOO Galeri Amesos Ifpack ML Stratimikos Teko 16"
    "Final set of non-enabled top-level packages:  TrilinosFramework Shards Stokhos Sacado Intrepid Belos RBGen Phalanx Panzer Stalix 10"
  )


create_dependency_handling_test_case(
  ENABLE_KNOWN_EXTERNAL_REPOS_TYPE_Nightly_EnableExtraPack
  ARGS  -DTrilinos_ENABLE_KNOWN_EXTERNAL_REPOS_TYPE:STRING=Nightly
    -DTrilinos_IGNORE_MISSING_EXTRA_REPOSITORIES=ON
    -DTrilinos_ENABLE_ExtraPack=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Explicitly enabled top-level packages on input .* ExtraPack 1"
    "Explicitly disabled top-level packages on input .* Stokhos Stalix 2"
    "Setting Trilinos_ENABLE_Teuchos=ON because ExtraPack has a required dependence on Teuchos"
    "Setting Trilinos_ENABLE_Teko=ON because ExtraPack has a required dependence on Teko"
    "Final set of enabled top-level packages:  Teuchos RTOp Epetra Zoltan Triutils Tpetra EpetraExt Thyra Isorropia AztecOO Galeri Amesos Ifpack ML Stratimikos Teko ExtraPack 17"
    "Final set of non-enabled top-level packages:  TrilinosFramework Shards Stokhos Sacado Intrepid Belos RBGen Phalanx Panzer Stalix 10"
  )


#
# Test treating internal packages as TPLs with MockTrilinos
#

create_dependency_handling_test_case(
  ST_TplEnableThyraCoreLibsOn_EnableAllPackages_EnableTests
  ARGS
    -DTPL_ENABLE_ThyraCoreLibs=ON
    -DTrilinos_ENABLE_ALL_PACKAGES=ON
    -DTrilinos_ENABLE_SECONDARY_TESTED_CODE=ON
    -DTrilinos_ENABLE_TESTS=ON
    -DTrilinos_DUMP_PACKAGE_BUILD_STATUS=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Adjust the set of internal and external packages:"
    "-- Treating internal package Thyra as EXTERNAL because subpackage ThyraCoreLibs being treated as EXTERNAL [(]TPL_ENABLE_ThyraCoreLibs=ON[)]"
    "-- Treating internal package ThyraCoreLibs as EXTERNAL because downstream package Thyra being treated as EXTERNAL"
    "-- Treating internal package ThyraGoodStuff as EXTERNAL because downstream package Thyra being treated as EXTERNAL"
    "-- Treating internal package ThyraEpetra as EXTERNAL because downstream package Thyra being treated as EXTERNAL"
    "-- Treating internal package ThyraEpetraExt as EXTERNAL because downstream package Thyra being treated as EXTERNAL"
    "-- Treating internal package ThyraTpetra as EXTERNAL because downstream package Thyra being treated as EXTERNAL"
    "-- Treating internal package Tpetra as EXTERNAL because downstream package ThyraTpetra being treated as EXTERNAL"
    "-- Treating internal package EpetraExt as EXTERNAL because downstream package ThyraEpetraExt being treated as EXTERNAL"
    "-- Treating internal package Epetra as EXTERNAL because downstream package ThyraEpetra being treated as EXTERNAL"
    "-- Treating internal package Teuchos as EXTERNAL because downstream package ThyraCoreLibs being treated as EXTERNAL"
    "-- Treating internal package RTOp as EXTERNAL because downstream package ThyraCoreLibs being treated as EXTERNAL"
    "-- Treating internal package Triutils as EXTERNAL because downstream package EpetraExt being treated as EXTERNAL"
    "-- Treating internal package Zoltan as EXTERNAL because downstream package EpetraExt being treated as EXTERNAL"

    "Final package build status [(]enabled only[)]:"
    "-- Final: BLAS_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: LAPACK_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: Boost_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: DUMMY_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: TrilinosFramework_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Final: Teuchos_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: RTOp_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: Epetra_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: Zoltan_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: Shards_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Final: Triutils_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: Tpetra_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: EpetraExt_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: Sacado_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Final: ThyraCoreLibs_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: ThyraGoodStuff_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: ThyraEpetra_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: ThyraEpetraExt_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: ThyraTpetra_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: Thyra_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: Isorropia_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Final: AztecOO_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Final: Galeri_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Final: Amesos_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Final: Intrepid_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Final: Ifpack_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Final: ML_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Final: Belos_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Final: Stratimikos_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Final: RBGen_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Final: Phalanx_PACKAGE_BUILD_STATUS=INTERNAL"

    "Final set of enabled top-level packages:  TrilinosFramework Shards Sacado Isorropia AztecOO Galeri Amesos Intrepid Ifpack ML Belos Stratimikos RBGen Phalanx 14"
    "Final set of enabled packages:  TrilinosFramework Shards Sacado Isorropia AztecOO Galeri Amesos Intrepid Ifpack ML Belos Stratimikos RBGen Phalanx 14"
    "Final set of non-enabled top-level packages:  Stokhos Panzer 2"
    "Final set of non-enabled packages:  Stokhos Panzer 2"
    "Final set of enabled external packages/TPLs:  BLAS LAPACK Boost DUMMY Teuchos RTOp Epetra Zoltan Triutils Tpetra EpetraExt ThyraCoreLibs ThyraGoodStuff ThyraEpetra ThyraEpetraExt ThyraTpetra Thyra 17"
    "Final set of non-enabled external packages/TPLs:  MPI Scotch METIS ParMETIS CppUnit ADOLC ADIC TVMET y12m SuperLUDist SuperLU UMFPACK AMD PETSC MUMPS ThyraCrazyStuff 16"

  )


create_dependency_handling_test_case(
  ST_TplEnableStratimikosOn_EnableMLOff_EnableAllPackages_EnableTests
  ARGS
    -DTPL_ENABLE_Stratimikos=ON
    -DTrilinos_ENABLE_ML=OFF
    -DTrilinos_ENABLE_ALL_PACKAGES=ON
    -DTrilinos_ENABLE_SECONDARY_TESTED_CODE=ON
    -DTrilinos_ENABLE_TESTS=ON
    -DTrilinos_DUMP_PACKAGE_BUILD_STATUS=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Adjust the set of internal and external packages:"
    "-- Treating internal package Stratimikos as EXTERNAL because TPL_ENABLE_Stratimikos=ON"
    "-- Treating internal package ThyraEpetraExt as EXTERNAL because downstream package Stratimikos being treated as EXTERNAL"
    "-- Treating internal package ThyraCoreLibs as EXTERNAL because downstream package Stratimikos being treated as EXTERNAL"
    "-- Treating internal package Amesos as EXTERNAL because downstream package Stratimikos being treated as EXTERNAL"
    "-- Treating internal package AztecOO as EXTERNAL because downstream package Stratimikos being treated as EXTERNAL"
    "-- Treating internal package Belos as EXTERNAL because downstream package Stratimikos being treated as EXTERNAL"
    "-- Treating internal package Ifpack as EXTERNAL because downstream package Stratimikos being treated as EXTERNAL"
    "-- Treating internal package Teuchos as EXTERNAL because downstream package Belos being treated as EXTERNAL"
    "-- Treating internal package Epetra as EXTERNAL because downstream package Belos being treated as EXTERNAL"
    "-- Treating internal package Tpetra as EXTERNAL because downstream package Belos being treated as EXTERNAL"
    "-- Treating internal package EpetraExt as EXTERNAL because downstream package Amesos being treated as EXTERNAL"
    "-- Treating internal package Triutils as EXTERNAL because downstream package AztecOO being treated as EXTERNAL"
    "-- Treating internal package Thyra as EXTERNAL because subpackage ThyraCoreLibs being treated as EXTERNAL"
    "-- Treating internal package ThyraGoodStuff as EXTERNAL because downstream package Thyra being treated as EXTERNAL"
    "-- Treating internal package ThyraEpetra as EXTERNAL because downstream package Thyra being treated as EXTERNAL"
    "-- Treating internal package ThyraTpetra as EXTERNAL because downstream package Thyra being treated as EXTERNAL"
    "-- Treating internal package RTOp as EXTERNAL because downstream package ThyraCoreLibs being treated as EXTERNAL"
    "-- Treating internal package Zoltan as EXTERNAL because downstream package EpetraExt being treated as EXTERNAL"

    "Final package build status [(]enabled only[)]:"
    "-- Final: BLAS_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: LAPACK_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: Boost_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: DUMMY_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: TrilinosFramework_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Final: Teuchos_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: RTOp_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: Epetra_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: Zoltan_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: Shards_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Final: Triutils_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: Tpetra_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: EpetraExt_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: Sacado_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Final: ThyraCoreLibs_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: ThyraGoodStuff_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: ThyraEpetra_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: ThyraEpetraExt_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: ThyraTpetra_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: Thyra_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: Isorropia_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Final: AztecOO_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: Galeri_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Final: Amesos_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: Intrepid_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Final: Ifpack_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: Belos_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: Stratimikos_PACKAGE_BUILD_STATUS=EXTERNAL"
    "-- Final: RBGen_PACKAGE_BUILD_STATUS=INTERNAL"
    "-- Final: Phalanx_PACKAGE_BUILD_STATUS=INTERNAL"

    "Final set of enabled top-level packages:  TrilinosFramework Shards Sacado Isorropia Galeri Intrepid RBGen Phalanx 8"
    "Final set of enabled packages:  TrilinosFramework Shards Sacado Isorropia Galeri Intrepid RBGen Phalanx 8"
    "Final set of non-enabled top-level packages:  Stokhos Panzer 2"
    "Final set of non-enabled packages:  Stokhos Panzer 2"
    "Final set of enabled external packages/TPLs:  BLAS LAPACK Boost DUMMY Teuchos RTOp Epetra Zoltan Triutils Tpetra EpetraExt ThyraCoreLibs ThyraGoodStuff ThyraEpetra ThyraEpetraExt ThyraTpetra Thyra AztecOO Amesos Ifpack Belos Stratimikos 22"
    "Final set of non-enabled external packages/TPLs:  MPI Scotch METIS ParMETIS CppUnit ADOLC ADIC TVMET y12m SuperLUDist SuperLU UMFPACK AMD PETSC MUMPS ThyraCrazyStuff ML 17"

  )
# NOTE: The above test implicitly makes ThyraCoreLibs and ThyraEpetraExt
# EXTERNAL due to Stratimikos being EXTERNAL and makes sure that all of the
# Thyra subpackages get changed to EXTERNAL.  This above test also disables ML
# to turn off the dependency between Stratimikos and Isorropia so that the
# Isorropia package stays INTERNAL.  That is, we don't want to make more
# packages EXTERNAL that we need to based on the final set of enables and
# disables and the enabled optional dependencies between packages.
