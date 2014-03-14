# @HEADER
# ************************************************************************
#
#            TriBITS: Tribial Build, Integrate, and Test System
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

INCLUDE(TribitsAddTestHelpers)


#
#
# @FUNCTION: TRIBITS_ADD_TEST()
#
# Add a test or a set of tests for a single executable or command.
#
# Usage::
#
#   TRIBITS_ADD_TEST(
#     <exeRootName>  [NOEXEPREFIX]  [NOEXESUFFIX]
#     [NAME <testName> | NAME_POSTFIX <testNamePostfix>]
#     [DIRECTORY <directory>]
#     [ADD_DIR_TO_NAME]
#     [ARGS "<arg0> <arg1> ..." "<arg2> <arg3> ..." ...
#       | POSTFIX_AND_ARGS_0 <postfix> <arg0> <arg1> ...
#         POSTFIX_AND_ARGS_1 ... ]
#     [COMM [serial] [mpi]]
#     [NUM_MPI_PROCS <numProcs>]
#     [CATEGORIES <category0>  <category1> ...]
#     [HOST <host0> <host1> ...]
#     [XHOST <host0> <host1> ...]
#     [HOSTTYPE <hosttype0> <hosttype1> ...]
#     [XHOSTTYPE <hosttype0> <hosttype1> ...]
#     [STANDARD_PASS_OUTPUT
#       | PASS_REGULAR_EXPRESSION "<regex0>;<regex1>;..."]
#     [FAIL_REGULAR_EXPRESSION "<regex0>;<regex1>;..."]
#     [WILL_FAIL]
#     [ENVIRONMENT <var0>=<value0> <var1>=<value1> ...]
#     [TIMEOUT <maxSeconds>]
#     )
#
# *Sections:*
#
# * `Formal Arguments (TRIBITS_ADD_TEST())`_
# * `Determining the Exectuable or Command to Run (TRIBITS_ADD_TEST())`_
# * `Determining the Full Test Name (TRIBITS_ADD_TEST())`_
# * `Adding Multiple Tests  (TRIBITS_ADD_TEST())`_
# * `Determining Pass/Fail (TRIBITS_ADD_TEST())`_
# * `Setting additional test properties (TRIBITS_ADD_TEST())`_
# * `Debugging and Examining Test Generation (TRIBITS_ADD_TEST())`_
# * `Disabling Tests Externally (TRIBITS_ADD_TEST())`_
#
# .. _Formal Arguments (TRIBITS_ADD_TEST()):
#
# **Formal Arguments (TRIBITS_ADD_TEST())**
#
#   ``<exeRootName>``
#
#     The name of the exectuble or path to the exectuable to run for the test
#     (see `Determining the Exectuable or Command to Run
#     (TRIBITS_ADD_TEST())`_).  This name is also the default root name for
#     the test (see `Determining the Full Test Name (TRIBITS_ADD_TEST())`_).
#
#   ``NOEXEPREFIX``
#
#    If specified, then the prefix ``${PACKAGE_NAME}_`` is not assumed to be
#    prepended to ``<exeRootName>``.
#
#   ``NOEXESUFFIX``
#
#      If specified, then the postfix
#      ``${${PROJECT_NAME}_CMAKE_EXECUTABLE_SUFFIX}`` is not assumed to be
#      post-pended to ``<exeRootName>``.
#
#   ``NAME <testRootName>``
#
#     If specified, gives the root name of the test.
#     If not specified, then ``<testRootName>`` is taken to be
#     ``<exeRootName>``.  The actual test name will always prefixed as
#     ``${PACKAGE_NAME}_<testRootName>`` passed into the call to the built-in
#     CMake command ``ADD_TEST(...)``.  The main purpose of this argument is to
#     allow multiple tests to be defined for the same executable.  CTest
#     requires all test names to be globally unique in a single project.
#  
#   ``NAME_POSTFIX <testNamePostfix>``
#
#     If specified, gives a postfix that will be added to the standard test
#     name based on ``<exeRootName>`` (appended as ``_<NAME_POSTFIX>``).  If
#     the ``NAME <testRootName>`` argument is given, this argument is ignored.
#  
#   ``DIRECTORY <dir>``
#
#     If specified, then the executable is assumed to be in the directory
#     given by by ``<dir>``.  The directory ``<dir>`` can either be a relative
#     or absolute path.  If not specified, the executable is assumed to be in
#     the current bindary directory.
#   
#   ``ADD_DIR_TO_NAME``
#
#     If specified, then the directory name that this test resides in will be
#     added into the name of the test after the package name is added and
#     before the root test name (see below).  The directory will have the
#     package's base directory stripped off so only the unique part of the
#     test directory will be used.  All directory seperators will be changed
#     into underscores.
#  
#   ``RUN_SERIAL``
#
#     If specified then no other tests will be allowed to run while this test
#     is running. This is useful for devices(like cuda cards) that require
#     exclusive access for processes/threads.  This just sets the CTest test
#     property ``RUN_SERIAL`` using the built-in CMake function
#     ``SET_TESTS_PROPERTIES()``.
#  
#   ``ARGS "<arg0> <arg1> ..." "<arg2> <arg3> ..." ...``
#
#     If specified, then a set of arguments can be passed in quotes.  If
#     multiple groups of arguments are passed in different quoted clusters of
#     arguments then a different test will be added for each set of arguments.
#     In this way, many different tests can be added for a single executable
#     in a single call to this function.  Each of these separate tests will be
#     named ``${TEST_NAME}_xy`` where ``xy`` = ``00``, ``01``, ``02``, and so
#     on.
#  
#   ``POSTFIX_AND_ARGS_<IDX> <postfix> <arg0> <arg1> ...``
#
#     If specified, gives a sequence of sets of test postfix names and arguments
#     lists for different tests.  For example, a set of three different tests
#     with argument lists can be specified as::
#       
#       POSTIFX_AND_ARGS_0 postfix0 --arg1 --arg2="dummy"
#       POSTIFX_AND_ARGS_1 postfix1  --arg2="fly"
#       POSTIFX_AND_ARGS_2 postfix2  --arg2="bags"
#  
#     This will create three different test cases with the postfix names
#     ``postfix0``, ``postfix1``, and ``postfix2``.  The indexes must be
#     consecutive starting a ``0`` and going up to (currently) ``19``.  The main
#     advantages of using these arguments instead of just 'ARGS' are that you
#     can give meaningful name to each test case and you can specify multiple
#     arguments without having to quote them and you can allow long argument
#     lists to span multiple lines.
#  
#   ``COMM [serial] [mpi]``
#
#     If specified, selects if the test will be added in serial and/or MPI
#     mode.  If the ``COMM`` argument is missing, the test will be added in
#     both serial and MPI builds of the code.
#  
#   ``NUM_MPI_PROCS <numProcs>``
#
#     If specified, gives the number of processes that the test will be
#     defined to run.  If ``<numProcs>`` is greater than
#     ``${MPI_EXEC_MAX_NUMPROCS}`` then the test will be excluded.  If not
#     specified, then the default number of processes for an MPI build will be
#     ``${MPI_EXEC_DEFAULT_NUMPROCS}``.  For serial builds, this argument is
#     ignored.
#  
#   ``HOST <host0> <host1> ...``
#
#     If specified, gives a list of hostnames where the test will be included.
#     The current hostname is determined by the built-in CMake command
#     ``SITE_NAME(${PROJECT_NAME}_HOSTNAME)``.  On Linux/Unix systems, this is
#     typically the value returned by 'uname -n'.  If this list is given, the
#     value of ``${${PROJECT_NAME}_HOSTNAME}`` must equal one of the listed
#     host names ``<hosti>`` or test will not be added.  The value of
#     ``${PROJECT_NAME}_HOSTNAME`` gets printed out in the TriBITS cmake
#     output under the section ``Probing the environment``.
#  
#   ``XHOST <host0> <host1> ...``
#
#     If specified, gives a list of hostnames (see ``HOST`` argument) where
#     the test will *not* be added.  This check is performed after the check
#     for the hostnames in the ``HOST`` list if it should exist.  Therefore,
#     this list exclusion list overrides the 'HOST' inclusion list.
#
#   ``CATEGORIES <category0> <category1> ...``
#
#     If specified, gives the specific categories of the test.  Valid test
#     categories include ``BASIC``, ``CONTINUOUS``, ``NIGHTLY``, ``WEEKLY``
#     and ``PERFORMANCE``.  By default, the category is ``BASIC``.  When the
#     test category does not match ``${PROJECT_NAME}_TEST_CATEGORIES``, then
#     the test is not added.  When the ``CATEGORIES`` is ``BASIC`` it will
#     match ``${PROJECT_NAME}_TEST_CATEGORIES`` eqaual to ``CONTINUOUS``,
#     ``NIGHTLY``, and ``WEEKLY``.  When the ``CATEGORIES`` contains
#     ``CONTINUOUS`` it will match ``${PROJECT_NAME}_TEST_CATEGORIES`` equal
#     to ``CONTINUOUS``, ``NIGHTLY``, and ``WEEKLY``.  When the ``CATEGORIES``
#     is ``NIGHTLY`` it will match ``${PROJECT_NAME}_TEST_CATEGORIES`` equal
#     to ``NIGHTLY`` and ``WEEKLY``.  When the ``CATEGORIES`` is
#     ``PERFORMANCE`` it will match
#     ``${PROJECT_NAME}_TEST_CATEGORIES=PERFORMANCE`` only.
#
#   ``HOSTTYPE <hosttype0> <hosttype1> ...``
#
#     If specified, gives the names of the host system type (given by
#     ``CMAKE_HOST_SYSTEM_NAME`` which is printed in the TriBITS cmake
#     confgiure output in the section ``Probing the environment``) to include
#     the test.  Typical host system type names include ``Linux``, ``Darwain``
#     etc.
#
#   ``XHOSTTYPE <hosttype0> <hosttype1> ...``
#
#     If specified, gives the names of the host system type to *not* include
#     the test.  This check is performed after the check for the host system
#     names in the ``HOSTTYPE`` list if it should exist.  Therefore, this list
#     exclusion list overrides the ``HOSTTYPE`` inclusion list.
#
#   ``STANDARD_PASS_OUTPUT``
#
#     If specified, then the standard test output ``End Result: TEST PASSED``
#     is greped for to determine success.  This is needed for MPI tests on
#     some platforms since the return value is unreliable.  This is set using
#     the built-in ctest property ``PASS_REGULAR_EXPRESSION``.
#
#   ``PASS_REGULAR_EXPRESSION "<regex0>;<regex1>;..."``
#
#     If specified, then a test will be assumed to pass only if one of the
#     regular expressions ``<regex0>``, ``<regex1>`` etc. match the output.
#     Otherwise, the test will fail.  This is set using the built-in test
#     property ``PASS_REGULAR_EXPRESSION``.  Consult standard CMake
#     documentation.
#
#   ``FAIL_REGULAR_EXPRESSION "<regex0>;<regex1>;..."``
#
#     If specified, then a test will be assumed to fail if one of the regular
#     expressions ``<regex0>``, ``<regex1>`` etc. match the output.
#     Otherwise, the test will pass.  This is set using the built-in test
#     property ``FAIL_REGULAR_EXPRESSION``.
#
#   ``WILL_FAIL``
#
#     If passed in, then the pass/fail criteria will be inverted.  This is set
#     using the built-in test property ``WILL_FAIL``.
#
#   ``ENVIRONMENT <var0>=<value0> <var1>=<value1> ...``
#
#     If passed in, the listed environment varaibles will be set before
#     calling the test.  This is set using the built-in test property
#     ``ENVIRONMENT``.
#
#   ``TIMEOUT <maxSeconds>``
#
#     If passed in, gives maximum number of seconds the test will be allowed
#     to run beforebeing timed-out.  This sets the test property ``TIMEOUT``.
#     **WARNING:** Rather than just increasing the timeout for an expensive
#     test, please try to either make the test run faster or relegate the test
#     to being run less often (i.e. set ``CATEGORIES NIGHTLY`` or even
#     ``WEEKLY`` for extremently expensive tests).  Expensive tests are one of
#     the worse forms of technical debt that a project can have!
#
# In the end, this function just calls the built-in CMake commands
# ``ADD_TEST(${TEST_NAME} ...)`` and ``SET_TESTS_PROPERTIES(${TEST_NAME}
# ...)`` to set up a executable process for ``ctest`` to run, determine
# pass/fail criteria, and set some other test properties.  Therefore, this
# wrapper funtion does not provide any fundamentally new features that are
# already avaiable in the basic usage if CMake/CTest.  However, this wrapper
# function takes care of many of the details and boiler-plate CMake code that
# it takes to add such a test (or tests) and enforces consistency across a
# large project for how tests are defined, run, and named (to avoid test name
# clashes).
#
# If more flexibility or control is needed when defining tests, then the
# function ``TRIBITS_ADD_ADVANCED_TEST()`` should be used instead.
#
# In the following subsections, more details on how tests are defined and run
# is given.
#
# .. _Determining the Exectuable or Command to Run (TRIBITS_ADD_TEST()):
#
# **Determining the Exectuable or Command to Run (TRIBITS_ADD_TEST())**
#
# This funtion is primarily designed to make it easy to run tests for
# exectaubles built using the function `TRIBITS_ADD_EXECUTABLE()`_.  To set up
# tests to run arbitrary executables, see below.
#
# By default, the command to run for the executable is determined by first
# getting the exectuable name which by default is assumed to be
# ``<fullExeName``> =::
#
#   ${PACKAGE_NAME}_<exeRootName>${${PROJECT_NAME}_CMAKE_EXECUTABLE_SUFFIX}
#
# which is (by no coincidence) idential to how it is selected in
# `TRIBITS_ADD_EXECUTABLE()`_.  This name can be alterned by passing in
# ``NOEXEPREFIX``, ``NOEXESUFFIX``, and ``ADD_DIR_TO_NAME`` as described in
# `Executable and Target Name (TRIBITS_ADD_EXECUTABLE())`_.
#
# By default, this executable is assumed to be in the current CMake binary
# directory ``${CMAKE_CURRENT_BINARY_DIR}`` but the directory location can be
# changed using the ``DIRECTORY <dir>`` argument.  
#
# If an arbitrary exectuable is to be run for the test, then pass in
# ``NOEXEPREFIX`` and ``NOEXESUFFIX`` and set ``<exeRootName>`` to the
# relative or absolute path of the exeutable to be run.  If ``<exeRootName>``
# is not an absolute path, then ``${CMAKE_CURRENT_BINARY_DIR}/<exeRootName>``
# is set as the executable to run.
#
# Whatever executable path is specified using this logic, if the executable is
# not found, then when ``ctest`` goes to run the test, it will mark it as
# ``NOT RUN``.
#
# .. _Determining the Full Test Name (TRIBITS_ADD_TEST()):
#
# **Determining the Full Test Name (TRIBITS_ADD_TEST())**
#
# By default, the base test name is selected to be::
#
#   ${PACKAGE_NAME}_<exeRootName>
#
# If ``NAME <testRootName>`` is passed in, then ``<testRootName>`` is used
# instead of ``<exeRootName>``.
#
# If ``NAME_POSTFIX <testNamePostfix>`` is passed in, then the base test name
# is selected to be::
#
#   ${PACKAGE_NAME}_<exeRootName>_<testNamePostfix>
#
# If ``ADD_DIR_TO_NAME`` is passed in, then the directory name realtive to the
# package directory name is added to the name as well to help disambiguate the
# test name (see the above).
#
# Let the test name determined by this process be ``TEST_NAME``.  If no
# arguments or one set of arguments are passed in through ``ARGS``, then this
# is the test name actaully passed in to ``ADD_TEST()``.  If multiple tests
# are defined, then this name becomes the base test name for each of the
# tests. See below.
#
# Finally, for any test that gets defined, if MPI is enabled
# (i.e. ``TPL_ENABLE_MPI=ON``), then the terminal suffix
# `_MPI_${NUM_MPI_PROCS}` will be added to the end of the test name (even for
# multiple tests).  No such prefix is added for the serial case
# (i.e. ``TPL_ENABLE_MPI=OFF``).
#
# .. _Adding Multiple Tests  (TRIBITS_ADD_TEST()):
#
# **Adding Multiple Tests  (TRIBITS_ADD_TEST())**
#
# ToDo: Explain how multiple tests can be added with different sets of
#  arguments in one of two ways.
#
# .. _Determining Pass/Fail (TRIBITS_ADD_TEST()):
#
# **Determining Pass/Fail (TRIBITS_ADD_TEST())**
#
# ToDo: Fill in!
#
# .. _Setting additional test properties (TRIBITS_ADD_TEST()):
#
# **Setting additional test properties (TRIBITS_ADD_TEST())**
#
# ToDo: Fill in!
#
# .. _Debugging and Examining Test Generation (TRIBITS_ADD_TEST()):
#
# **Debugging and Examining Test Generation (TRIBITS_ADD_TEST())**
#
# ToDo: Describe setting ${PROJECT_NAME}_VERBOSE_CONFIGURE=ON and seeing what
# info it prints out.
#
# ToDo: Describe how to examine the generated CTest files to see what test(s)
# actually got added (or not added) and what the pass/fail criteria is.
#
# .. _Disabling Tests Externally (TRIBITS_ADD_TEST()):
#
# **Disabling Tests Externally (TRIBITS_ADD_TEST())**
#
# The test can be disabled externally by setting the CMake cache variable
# ``${FULL_TEST_NAME}_DISABLE=TRUE``.  This allows tests to be disable on a
# case-by-case basis.  This is the *exact* name that shows up in 'ctest -N'
# when running the test.  If multiple tests are added in this funtion through
# multiple argument sets to ``ARGS`` or through multiple
# ``POSTFIX_AND_ARGS_<IDX>`` arguments, then
# ``${FULL_TEST_NAME}_DISABLE=TRUE`` must be set for each test individually.
#
FUNCTION(TRIBITS_ADD_TEST EXE_NAME)

  IF(${PROJECT_NAME}_VERBOSE_CONFIGURE)
    MESSAGE("")
    MESSAGE("TRIBITS_ADD_TEST: ${EXE_NAME} ${ARGN}")
  ENDIF()

  GLOBAL_SET(PACKAGE_ADD_TEST_ADD_TEST_INPUT "")
   
  #
  # A) Parse the input arguments
  #

  # Allow for a maximum of 20 (0 through 19) postfix and argument blocks
  SET(MAX_NUM_POSTFIX_AND_ARGS_IDX 19)

  SET(POSTFIX_AND_ARGS_LIST "")
  FOREACH( POSTFIX_AND_ARGS_IDX RANGE ${MAX_NUM_POSTFIX_AND_ARGS_IDX})
    LIST( APPEND POSTFIX_AND_ARGS_LIST POSTFIX_AND_ARGS_${POSTFIX_AND_ARGS_IDX} )
  ENDFOREACH()
  #PRINT_VAR(POSTFIX_AND_ARGS_LIST)

  PARSE_ARGUMENTS(
     #prefix
     PARSE
     #lists
     "DIRECTORY;KEYWORDS;COMM;NUM_MPI_PROCS;ARGS;${POSTFIX_AND_ARGS_LIST};NAME;NAME_POSTFIX;CATEGORIES;HOST;XHOST;HOSTTYPE;XHOSTTYPE;PASS_REGULAR_EXPRESSION;FAIL_REGULAR_EXPRESSION;TIMEOUT;ENVIRONMENT"
     #options
     "NOEXEPREFIX;NOEXESUFFIX;STANDARD_PASS_OUTPUT;WILL_FAIL;ADD_DIR_TO_NAME;RUN_SERIAL"
     ${ARGN}
     )

  IF (PARSE_ARGS)
    LIST(LENGTH PARSE_ARGS NUM_PARSE_ARGS)
  ELSEIF (PARSE_POSTFIX_AND_ARGS_0)
    # We will use this list instead
  ELSE()
    # Niether 'ARGS' nor 'POSTFIX_AND_ARGS' was selected so just assume one
    # empty arg
    SET(PARSE_ARGS " ")
    SET(NUM_PARSE_ARGS 1)
  ENDIF()

  IF (${PROJECT_NAME}_VERBOSE_CONFIGURE)
    MESSAGE("")
    MESSAGE("TRIBITS_ADD_TEST: EXE_NAME = ${EXE_NAME}")
  ENDIF()
  
  #
  # B) Add or don't add tests based on a number of criteria
  #

  SET(ADD_THE_TEST FALSE)
  TRIBITS_ADD_TEST_PROCESS_CATEGORIES(ADD_THE_TEST)
  IF (NOT ADD_THE_TEST)
    RETURN()
  ENDIF()

  SET(ADD_THE_TEST FALSE)
  TRIBITS_ADD_TEST_PROCESS_HOST_HOSTTYPE(ADD_THE_TEST)
  IF (NOT ADD_THE_TEST)
    RETURN()
  ENDIF()

  #
  # C) Set the name and path of the binary that will be run
  #

  TRIBITS_ADD_TEST_GET_EXE_BINARY_NAME( "${EXE_NAME}"
    ${PARSE_NOEXEPREFIX} ${PARSE_NOEXESUFFIX} ${PARSE_ADD_DIR_TO_NAME} EXE_BINARY_NAME )
  
  #If requested create a modifier for the name that will be inserted between the package name 
  #and the given name or exe_name for the test
  SET(DIRECTORY_NAME "")
  IF(PARSE_ADD_DIR_TO_NAME)
    TRIBITS_CREATE_NAME_FROM_CURRENT_SOURCE_DIRECTORY(DIRECTORY_NAME)
    SET(DIRECTORY_NAME "${DIRECTORY_NAME}_")
  ENDIF()

  #MESSAGE("TRIBITS_ADD_TEST: ${EXE_NAME}: EXE_BINARY_NAME = ${EXE_BINARY_NAME}")
  
  IF (PARSE_NAME)
    SET(TEST_NAME "${DIRECTORY_NAME}${PARSE_NAME}")
  ELSEIF (PARSE_NAME_POSTFIX)
    SET(TEST_NAME "${DIRECTORY_NAME}${EXE_NAME}_${PARSE_NAME_POSTFIX}")  
  ELSE()
    SET(TEST_NAME "${DIRECTORY_NAME}${EXE_NAME}")  
  ENDIF()

  TRIBITS_ADD_TEST_ADJUST_DIRECTORY( ${EXE_BINARY_NAME} "${PARSE_DIRECTORY}"
    EXECUTABLE_PATH)

  #MESSAGE("TRIBITS_ADD_TEST: ${EXE_NAME}: EXECUTABLE_PATH = ${EXECUTABLE_PATH}")

  #
  # D) Determine if we will add the serial or MPI tests based on input COMM
  # and TPL_ENABLE_MPI
  #

  TRIBITS_PROCESS_COMM_ARGS(ADD_SERIAL_TEST  ADD_MPI_TEST  ${PARSE_COMM})

  #
  # E) Get the MPI options
  #
    
  TRIBITS_ADD_TEST_GET_NUM_PROCS_USED("${PARSE_NUM_MPI_PROCS}" NUM_PROCS_USED)
  IF (NUM_PROCS_USED LESS 0)
    SET(ADD_MPI_TEST FALSE)
  ENDIF()

  #
  # F) Add the tests
  #

  IF (NOT ADD_SERIAL_TEST AND NOT ADD_MPI_TEST)
    RETURN()
  ENDIF()

  IF (TPL_ENABLE_MPI)
    SET(MPI_NAME_POSTFIX "_MPI_${NUM_PROCS_USED}")
  ELSE()
    SET(MPI_NAME_POSTFIX "")
  ENDIF()

  IF (PARSE_ARGS)

    # F.1) Add tests with simple lists of arguments
  
    SET(COUNTER 0)
  
    FOREACH(PARSE_ARG ${PARSE_ARGS})
  
      IF(${NUM_PARSE_ARGS} EQUAL 1)
        SET(TEST_NAME_INSTANCE "${TEST_NAME}${MPI_NAME_POSTFIX}")
      ELSE()
        SET(TEST_NAME_INSTANCE "${TEST_NAME}_${COUNTER}${MPI_NAME_POSTFIX}")
      ENDIF()
      IF(${PROJECT_NAME}_VERBOSE_CONFIGURE)
        MESSAGE(STATUS "TEST_NAME = ${TEST_NAME_INSTANCE}")
      ENDIF()
  
      TRIBITS_CONVERT_CMND_ARG_STRING_TO_ADD_TEST_ARG_ARRAY(${PARSE_ARG} INARGS)
      IF (${PROJECT_NAME}_VERBOSE_CONFIGURE)
        PRINT_VAR(INARGS)
      ENDIF()

      TRIBITS_ADD_TEST_ADD_TEST_ALL( ${TEST_NAME_INSTANCE}
        "${EXECUTABLE_PATH}"  "${NUM_PROCS_USED}"
        ${PARSE_RUN_SERIAL} ${INARGS} )
  
      MATH(EXPR COUNTER ${COUNTER}+1 )
  
    ENDFOREACH()

  ELSEIF (PARSE_POSTFIX_AND_ARGS_0)

    # F.2) Add tests with different postfixes for each set of arguments

    FOREACH( POSTFIX_AND_ARGS_IDX RANGE ${MAX_NUM_POSTFIX_AND_ARGS_IDX})

      IF(${PROJECT_NAME}_VERBOSE_CONFIGURE)
        PRINT_VAR(PARSE_POSTFIX_AND_ARGS_${POSTFIX_AND_ARGS_IDX})
      ENDIF()

      IF (NOT PARSE_POSTFIX_AND_ARGS_${POSTFIX_AND_ARGS_IDX})
        BREAK()
      ENDIF()

      SET( POSTFIX_AND_ARGS ${PARSE_POSTFIX_AND_ARGS_${POSTFIX_AND_ARGS_IDX}} )

      LIST( GET  POSTFIX_AND_ARGS  0  POSTFIX )
      SET( INARGS  ${POSTFIX_AND_ARGS} ) # Initially contains postfix as ele 0
      LIST( REMOVE_AT  INARGS  0 ) # Strip off the postfix name

      SET(TEST_NAME_INSTANCE "${TEST_NAME}_${POSTFIX}${MPI_NAME_POSTFIX}")

      TRIBITS_ADD_TEST_ADD_TEST_ALL( ${TEST_NAME_INSTANCE}
        "${EXECUTABLE_PATH}"  "${NUM_PROCS_USED}" ${PARSE_CREATE_WORKING_DIR}
        ${PARSE_RUN_SERIAL} ${INARGS} )

    ENDFOREACH()

  ENDIF()
  
ENDFUNCTION()
