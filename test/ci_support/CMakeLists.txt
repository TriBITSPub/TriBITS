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
# Test generation of package dependency and related XML and related files
#


# The mock test project 
SET(MOCK_PROJECT_NAME Trilinos)

SET(TRIBITS_MOCK_TRILINOS_DIR "examples/MockTrilinos")

SET(MOCK_TRILINOS_DIR ${${PROJECT_NAME}_TRIBITS_DIR}/${TRIBITS_MOCK_TRILINOS_DIR})


IF (WIN23 AND NOT CYGWIN)
  SET(DIFF_COMMAND_STUFF "${CMAKE_COMMAND}" ARGS -E compare_files)
ELSE()
  SET(DIFF_COMMAND_STUFF diff ARGS)
ENDIF()


TRIBITS_ADD_ADVANCED_TEST( XmlHtmlCDashOutputTest
  OVERALL_WORKING_DIRECTORY TEST_NAME
  TEST_0 CMND ${CMAKE_COMMAND}
    ARGS
      -D${MOCK_PROJECT_NAME}_TRIBITS_DIR:FILEPATH=${${PROJECT_NAME}_TRIBITS_DIR}
      -D ${MOCK_PROJECT_NAME}_SHORTCIRCUIT_AFTER_DEPENDENCY_HANDLING:BOOL=ON
      -D ${MOCK_PROJECT_NAME}_ENABLE_ALL_PACKAGES:BOOL=ON
      -D ${MOCK_PROJECT_NAME}_DEPS_XML_OUTPUT_FILE:STRING=TrilinosPackageDependencies.xml
      -D ${MOCK_PROJECT_NAME}_DEPS_HTML_OUTPUT_FILE:STRING=TrilinosPackageDependenciesTable.html
      -D ${MOCK_PROJECT_NAME}_CDASH_DEPS_XML_OUTPUT_FILE:STRING=CDashSubprojectDependencies.xml
      -D ${MOCK_PROJECT_NAME}_ENABLE_C:BOOL=OFF
      -D ${MOCK_PROJECT_NAME}_ENABLE_CXX:BOOL=OFF
      -D ${MOCK_PROJECT_NAME}_ENABLE_Fortran:BOOL=OFF
      ${MOCK_TRILINOS_DIR}
    PASS_REGULAR_EXPRESSION "Shortcircuiting after dependency tracking ..."
  TEST_1 CMND ${DIFF_COMMAND_STUFF}
    ${CMAKE_CURRENT_SOURCE_DIR}/TrilinosPackageDependencies.gold.xml
    TrilinosPackageDependencies.xml
  TEST_2 CMND ${DIFF_COMMAND_STUFF}
    ${CMAKE_CURRENT_SOURCE_DIR}/TrilinosPackageDependenciesTable.gold.html
     TrilinosPackageDependenciesTable.html
  TEST_3 CMND ${DIFF_COMMAND_STUFF}
    ${CMAKE_CURRENT_SOURCE_DIR}/CDashSubprojectDependencies.gold.xml
    CDashSubprojectDependencies.xml
  )


#
# Test checkin-test.py script
#


ASSERT_DEFINED(${PROJECT_NAME}_ENABLE_DEVELOPMENT_MODE)
IF (${PROJECT_NAME}_ENABLE_DEVELOPMENT_MODE)
  TRIBITS_ADD_ADVANCED_TEST( TribitsPackageFilePathUtils_UnitTests
    OVERALL_WORKING_DIRECTORY TEST_NAME
    OVERALL_NUM_MPI_PROCS 1
    TEST_0 CMND ${PYTHON_EXECUTABLE} 
      ARGS ${CMAKE_CURRENT_SOURCE_DIR}/TribitsPackageFilePathUtils_UnitTests.py -v
      PASS_REGULAR_EXPRESSION "OK"
    )
ENDIF()

TRIBITS_ADD_ADVANCED_TEST( clone_extra_repos_UnitTests
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  TEST_0 CMND ${PYTHON_EXECUTABLE} 
    ARGS ${CMAKE_CURRENT_SOURCE_DIR}/clone_extra_repos_UnitTests.py
      --with-cmake="${CMAKE_COMMAND}"
      -v
    PASS_REGULAR_EXPRESSION "OK"
  )

TRIBITS_ADD_ADVANCED_TEST( CheckinTest_UnitTests
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  TEST_0 CMND ${PYTHON_EXECUTABLE} 
    ARGS ${CMAKE_CURRENT_SOURCE_DIR}/CheckinTest_UnitTests.py
      --with-cmake="${CMAKE_COMMAND}"
      -v
    PASS_REGULAR_EXPRESSION "OK"
  )


#
# TRIBITS_STRIP_COMMENTS_FROM_CMAKE_CACHE_FILE()
#

TRIBITS_ADD_ADVANCED_TEST( TribitsStripCommentsFromCMakeCacheFile_small
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  TEST_0 CMND ${CMAKE_COMMAND} 
    ARGS
      -DPROJECT_NAME=DummyProject
      -DTRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DCMAKE_CACHE_FILE_IN=${CMAKE_CURRENT_SOURCE_DIR}/CMakeCache.small.txt
      -DCMAKE_CACHE_FILE_CLEAN_OUT=CMakeCache.small.clean.txt
      -P ${CMAKE_CURRENT_SOURCE_DIR}/TribitsStripCommentsFromCMakeCacheFile_TestDriver.cmake
  TEST_1 CMND diff
    ARGS ${CMAKE_CURRENT_SOURCE_DIR}/CMakeCache.small.clean.txt.expected
      CMakeCache.small.clean.txt
  )

TRIBITS_ADD_ADVANCED_TEST( TribitsStripCommentsFromCMakeCacheFile_large
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  TEST_0 CMND ${CMAKE_COMMAND} 
    ARGS
      -DPROJECT_NAME=DummyProject
      -DTRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DCMAKE_CACHE_FILE_IN=${CMAKE_CURRENT_SOURCE_DIR}/CMakeCache.large.txt
      -DCMAKE_CACHE_FILE_CLEAN_OUT=CMakeCache.large.clean.txt
      -P ${CMAKE_CURRENT_SOURCE_DIR}/TribitsStripCommentsFromCMakeCacheFile_TestDriver.cmake
  TEST_1 CMND diff
    ARGS ${CMAKE_CURRENT_SOURCE_DIR}/CMakeCache.large.clean.txt.expected
      CMakeCache.large.clean.txt
  )

TRIBITS_ADD_ADVANCED_TEST( CDashQueryPassFail_UnitTests
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  TEST_0 CMND ${PYTHON_EXECUTABLE} 
    ARGS ${CMAKE_CURRENT_SOURCE_DIR}/CDashQueryPassFail_UnitTests.py -v
    PASS_REGULAR_EXPRESSION "OK"
  )

#
# TribitsExampleProject checkin-test.py tests
#


TRIBITS_ADD_ADVANCED_TEST( TribitsExampleProject_checkin_test
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Copy TribitsExampleProject so we can snapshot TriBITS into it"
    CMND ${CMAKE_COMMAND}
    ARGS -E copy_directory ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
      TribitsExampleProject

  TEST_1
    MESSAGE "Copy tribits dir into TribitsExampleProject/cmake/"
    CMND ${CMAKE_COMMAND}
    ARGS -E copy_directory ${${PROJECT_NAME}_TRIBITS_DIR}
      TribitsExampleProject/cmake/tribits

  TEST_2
    MESSAGE "Run checkin-test.py script to make sure it finds base dir"
    CMND ${PYTHON_EXECUTABLE}
    ARGS -E TribitsExampleProject/cmake/tribits/ci_support/checkin-test.py
      --enable-all-packages=on --send-email-to= --send-email-to-on-push= --allow-no-pull
    PASS_REGULAR_EXPRESSION_ALL
      "src-dir=.*/TriBITS_TribitsExampleProject_checkin_test/TribitsExampleProject/cmake/tribits/ci_support/[.][.]/[.][.]/[.][.]"
      "0[)] MPI_DEBUG => No configure, build, or test for MPI_DEBUG was requested! => Not ready to push! [(]-1.00 min[)]"
      "1[)] SERIAL_RELEASE => No configure, build, or test for SERIAL_RELEASE was requested! => Not ready to push! [(]-1.00 min[)]"
    # NOTE: That above test proves that the checkin-test.py script can find
    # the base directory when run as
    # <projectDir>/cmake/tribis/ci_support/checkin-test.py

  )


# NOTE: The fact that all testing and pushing for the checkin-test.py script
# is using the symlinked TriBITS/checkin-test.py tests and protects that use
# case.
