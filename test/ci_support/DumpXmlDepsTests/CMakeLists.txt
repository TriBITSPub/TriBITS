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

SET(TRIBITS_MOCK_TRILINOS_DIR "examples/MockTrilinos")


# MockTrilinos project
SET(MOCK_PROJECT_NAME Trilinos)
SET(MOCK_TRILINOS_DIR
  ${${PROJECT_NAME}_TRIBITS_DIR}/${TRIBITS_MOCK_TRILINOS_DIR})


#####################################################################
#
# Unit tests for just creating the depencency XML files
#
#####################################################################


FUNCTION(CREATE_DEPENDENCY_XML_DUMP_TEST_CASE TEST_NAME)

  CMAKE_PARSE_ARGUMENTS(
     #prefix
     PARSE
     #options
     ""
     #one_value_keywords
     ""
     #mulit_value_keywords
     "ARGS;PASS_REGULAR_EXPRESSION_ALL;COMPARE_XML_FILE"
     ${ARGN}
     )

  SET(EXTENDED_TEST_NAME DepXmlDumpTests_${TEST_NAME})
  SET(FULL_TEST_NAME ${PACKAGE_NAME}_${EXTENDED_TEST_NAME})

  SET(TEST_OUTPUT_REL_DIR ${FULL_TEST_NAME})
  SET(TEST_OUTPUT_DIR ${CMAKE_CURRENT_BINARY_DIR}/${TEST_OUTPUT_REL_DIR})

  TRIBITS_ADD_ADVANCED_TEST( ${EXTENDED_TEST_NAME}
    OVERALL_WORKING_DIRECTORY ${TEST_OUTPUT_REL_DIR}
    OVERALL_NUM_MPI_PROCS 1
    TEST_0 CMND "${CMAKE_COMMAND}"
      ARGS
        -DPROJECT_SOURCE_DIR:PATH=${MOCK_TRILINOS_DIR}
        -D${MOCK_PROJECT_NAME}_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
        -D${MOCK_PROJECT_NAME}_NATIVE_REPOSITORIES=.
        -D${MOCK_PROJECT_NAME}_DEPS_XML_OUTPUT_FILE=${TEST_OUTPUT_DIR}/${MOCK_PROJECT_NAME}PackageDependencies.xml
        -D${MOCK_PROJECT_NAME}_CDASH_DEPS_XML_OUTPUT_FILE=CDashSubprojectDependencies.xml
        -D${MOCK_PROJECT_NAME}_DEPS_HTML_OUTPUT_FILE=${MOCK_PROJECT_NAME}PackageDependenciesTable.html
        ${PARSE_ARGS}
        -P ${${PROJECT_NAME}_TRIBITS_DIR}/ci_support/TribitsDumpDepsXmlScript.cmake
      PASS_REGULAR_EXPRESSION_ALL ${PARSE_PASS_REGULAR_EXPRESSION_ALL}
    TEST_1 CMND "${CMAKE_COMMAND}"
      ARGS
        -E compare_files
        ${TEST_OUTPUT_DIR}/${MOCK_PROJECT_NAME}PackageDependencies.xml
        ${${PACKAGE_NAME}_SOURCE_DIR}/test/ci_support/${PARSE_COMPARE_XML_FILE}
    XHOSTTYPE Windows
    )

ENDFUNCTION()


CREATE_DEPENDENCY_XML_DUMP_TEST_CASE(
  BasePackagesTpls
  PASS_REGULAR_EXPRESSION_ALL
    "Trilinos_NUM_PACKAGES='24'"
    "Trilinos_NUM_TPLS='19'"
  COMPARE_XML_FILE
    TrilinosPackageDependencies.gold.xml
  )


CREATE_DEPENDENCY_XML_DUMP_TEST_CASE(
  WithPreCopyrightTrilinos
  ARGS
    -DTrilinos_EXTRA_REPOSITORIES=preCopyrightTrilinos
    -DLIST_ALWAYS_MISSING_PACKAGE=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Trilinos_NUM_PACKAGES='26'"
    "Trilinos_NUM_TPLS='20'"
  COMPARE_XML_FILE
    TrilinosPackageDependencies.preCopyrightTrilinos.gold.xml
  )
# The above test also ensures that the TribitsDumpDepsXmlScript.cmake behaves
# correctly when missing packages are listed but are marked as such and
# therefore should be ignored.  I have another test for
# TriBITSExProj/TribitsExampleProject that verifies that such a package is
# processed correctly when it does exist.  It is just that this was not
# testing this dump script.


CREATE_DEPENDENCY_XML_DUMP_TEST_CASE(
  WithPreCopyrightTrilinosExtraTrilinosRepo
  ARGS
    -DTrilinos_EXTRA_REPOSITORIES=preCopyrightTrilinos,extraTrilinosRepo
  PASS_REGULAR_EXPRESSION_ALL
    "Trilinos_NUM_PACKAGES='26'"
    "Trilinos_NUM_TPLS='22'"
  COMPARE_XML_FILE
    TrilinosPackageDependencies.preCopyrightTrilinos.extraTrilinosRepo.gold.xml
  )


CREATE_DEPENDENCY_XML_DUMP_TEST_CASE(
  WithExtraRepoOnePackage
  ARGS
    -DTrilinos_EXTRA_REPOSITORIES=extraRepoOnePackage
  PASS_REGULAR_EXPRESSION_ALL
    "Trilinos_NUM_PACKAGES='24'"
    "Trilinos_NUM_TPLS='19'"
  COMPARE_XML_FILE
    TrilinosPackageDependencies.extraRepoOnePackage.gold.xml
  )


CREATE_DEPENDENCY_XML_DUMP_TEST_CASE(
  WithPreRepoOnePackagePreCopyrightTrilinos
  ARGS
    -DTrilinos_PRE_REPOSITORIES=preRepoOnePackage
    -DTrilinos_EXTRA_REPOSITORIES=preCopyrightTrilinos
    -DLIST_ALWAYS_MISSING_PACKAGE=ON
  PASS_REGULAR_EXPRESSION_ALL
    "Trilinos_NUM_PACKAGES='27'"
    "Trilinos_NUM_TPLS='20'"
  COMPARE_XML_FILE
    TrilinosPackageDependencies.preRepoOnePackage.preCopyrightTrilinos.gold.xml
  )
