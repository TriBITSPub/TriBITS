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



INCLUDE(ParseVariableArguments)

SET(MOCK_PROJECT_NAME DummyProj)


#####################################################################
#
# Unit test TribitsProcessEnabledTpl.cmake and
# TribitsTplFindIncludeDirsAndLibraries.cmake
#
#####################################################################


FUNCTION(CREATE_PROCESS_ENABLED_TPLS_TEST_CASE  TEST_NAME)

  PARSE_ARGUMENTS(
     #prefix
     PARSE
     #lists
     "TPL_NAME;TPL_FINDMOD;INCLUDE_DIRS;LIBRARY_DIRS;PASS_REGULAR_EXPRESSION_ALL"
     #options
     "TPL_FIND_SHARED_LIBS;VERBOSE_DEBUG"
     ${ARGN}
     )

  SET(EXTENDED_TEST_NAME ProcessEnabledTpl_${TEST_NAME})
  SET(FULL_TEST_NAME ${PACKAGE_NAME}_${EXTENDED_TEST_NAME})

  SET(TEST_OUTPUT_REL_DIR ${FULL_TEST_NAME})
  SET(TEST_OUTPUT_DIR ${CMAKE_CURRENT_BINARY_DIR}/${TEST_OUTPUT_REL_DIR})

  TRIBITS_ADD_ADVANCED_TEST( ${EXTENDED_TEST_NAME}
    OVERALL_WORKING_DIRECTORY ${TEST_OUTPUT_REL_DIR}
    OVERALL_NUM_MPI_PROCS 1
    TEST_0 CMND "${CMAKE_COMMAND}"
      ARGS
        -DPROJECT_NAME=${MOCK_PROJECT_NAME}
        -D${MOCK_PROJECT_NAME}_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
        -DTPL_NAME=${PARSE_TPL_NAME}
        -D${PARSE_TPL_NAME}_FINDMOD=${PARSE_TPL_FINDMOD}
        -D${PARSE_TPL_NAME}_INCLUDE_DIRS=${PARSE_INCLUDE_DIRS}
        -D${PARSE_TPL_NAME}_LIBRARY_DIRS=${PARSE_LIBRARY_DIRS}
        -DTPL_FIND_SHARED_LIBS=${PARSE_TPL_FIND_SHARED_LIBS}
        -DTRIBITS_TPL_FIND_INCLUDE_DIRS_AND_LIBRARIES_VERBOSE=${PARSE_VERBOSE_DEBUG}
        -P ${CMAKE_CURRENT_SOURCE_DIR}/TribitsProcessEnabledTplTester.cmake
      PASS_REGULAR_EXPRESSION_ALL ${PARSE_PASS_REGULAR_EXPRESSION_ALL}
    XHOSTTYPE Windows
    )

ENDFUNCTION()

#
# Test with HeadersOnlyTpl
#

SET(HeaderOnlyTpl_BASE_DIR ${${PROJECT_NAME}_TRIBITS_DIR}/doc/examples/tpls/HeaderOnlyTpl)
SET(HeaderOnlyTpl_FINDMOD
  ${${PROJECT_NAME}_TRIBITS_DIR}/doc/examples/TribitsExampleProject/cmake/tpls/FindTPLHeaderOnlyTpl.cmake)

CREATE_PROCESS_ENABLED_TPLS_TEST_CASE(
  HeaderOnlyTpl_FindAll
  TPL_NAME  HeaderOnlyTpl
  TPL_FINDMOD  ${HeaderOnlyTpl_FINDMOD}
  INCLUDE_DIRS  ${HeaderOnlyTpl_BASE_DIR}
  PASS_REGULAR_EXPRESSION_ALL
    "Processing enabled TPL: HeaderOnlyTpl .enabled explicitly, disable with -DTPL_ENABLE_HeaderOnlyTpl=OFF."
    "-- Must find all headers in header sets .HeaderOnlyTpl_stuff.hpp."
    "-- Searching in HeaderOnlyTpl_INCLUDE_DIRS='/home/8vt/localhome/PROJECTS/Trilinos.base/Trilinos/TriBITS/doc/examples/tpls/HeaderOnlyTpl'"
    "-- Searching for headers in set .HeaderOnlyTpl_stuff.hpp."
    "--   Found TPL 'HeaderOnlyTpl' header file '/home/8vt/localhome/PROJECTS/Trilinos.base/Trilinos/TriBITS/doc/examples/tpls/HeaderOnlyTpl/HeaderOnlyTpl_stuff.hpp'"
    "-- Found TPL 'HeaderOnlyTpl' header path '/home/8vt/localhome/PROJECTS/Trilinos.base/Trilinos/TriBITS/doc/examples/tpls/HeaderOnlyTpl'"
    "-- TPL_HeaderOnlyTpl_INCLUDE_DIRS='/home/8vt/localhome/PROJECTS/Trilinos.base/Trilinos/TriBITS/doc/examples/tpls/HeaderOnlyTpl'"
  )

#
# Test with HeadersAndLibsTpl
#

SET(HeadersAndLibsTpl_BASE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/tpls/HeadersAndLibsTpl)
SET(HeadersAndLibsTpl_FINDMOD ${HeadersAndLibsTpl_BASE_DIR}/FindTPLHeadersAndLibsTpl.cmake)

CREATE_PROCESS_ENABLED_TPLS_TEST_CASE(
  HeadersAndLibsTpl_FindAll
  TPL_NAME  HeadersAndLibsTpl
  TPL_FINDMOD  ${HeadersAndLibsTpl_FINDMOD}
  INCLUDE_DIRS  ${HeadersAndLibsTpl_BASE_DIR}/include
  LIBRARY_DIRS  ${HeadersAndLibsTpl_BASE_DIR}/lib
  PASS_REGULAR_EXPRESSION_ALL
    "Processing enabled TPL: HeadersAndLibsTpl .enabled explicitly, disable with -DTPL_ENABLE_HeadersAndLibsTpl=OFF."
    "-- Must find all libraries in .haltpl1[;]haltpl2."
    "-- Searching in HeadersAndLibsTpl_LIBRARY_DIRS='.+/HeadersAndLibsTpl/lib'"
    "-- Searching for library 'haltpl1' ..."
    "--   Found HeadersAndLibsTpl TPL library: .+/HeadersAndLibsTpl/lib/libhaltpl1.a"
    "-- Searching for library 'haltpl2' ..."
    "--   Found HeadersAndLibsTpl TPL library: .+/HeadersAndLibsTpl/lib/libhaltpl2.a"
    "-- TPL_HeadersAndLibsTpl_LIBRARIES='.+/HeadersAndLibsTpl/lib/libhaltpl1.a[;].+/HeadersAndLibsTpl/lib/libhaltpl2.a'"
    "-- Must find all headers in header sets .HeadersAndLibsTpl_header1.hpp[;]HeadersAndLibsTpl_header2.hpp."
    "-- Searching in HeadersAndLibsTpl_INCLUDE_DIRS='.+/HeadersAndLibsTpl/include'"
    "-- Searching for headers in set .HeadersAndLibsTpl_header1.hpp."
    "--   Found TPL 'HeadersAndLibsTpl' header file '.+/HeadersAndLibsTpl/include/HeadersAndLibsTpl_header1.hpp'"
    "-- Searching for headers in set .HeadersAndLibsTpl_header2.hpp."
    "--   Found TPL 'HeadersAndLibsTpl' header file '.+/HeadersAndLibsTpl/include/HeadersAndLibsTpl_header2.hpp'"
    "-- Found TPL 'HeadersAndLibsTpl' header path '.+/HeadersAndLibsTpl/include'"
    "-- TPL_HeadersAndLibsTpl_INCLUDE_DIRS='.+/HeadersAndLibsTpl/include'"
  )
