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
# The tests defined here are used to test the dynamic behavior of the
# CMake/CTest functions TRIBITS_ADD_TEST(...) and
# TRIBITS_ADD_ADVANCED_TEST(...).
#


ASSERT_DEFINED(${PACKAGE_NAME}_ENABLE_MPI)
IF (${PACKAGE_NAME}_ENABLE_MPI)
  ADD_DEFINITIONS(-DHAVE_MPI)
ENDIF()

TRIBITS_ADD_EXECUTABLE(
  GenericDriver
  SOURCES GenericDriver.cpp
  )

TRIBITS_ADD_ADVANCED_TEST(
  CTestScripts_cmnd_1_args_0
  TEST_0 EXEC GenericDriver
  OVERALL_NUM_MPI_PROCS 1
  )

TRIBITS_ADD_TEST( GenericDriver
  NAME CTestScripts_simple_pass_regex
  ARGS "\"This is a crazy test!\" 1"
  PASS_REGULAR_EXPRESSION "[^=]This is a crazy test"
  NUM_MPI_PROCS 1
  )

TRIBITS_ADD_TEST( GenericDriver
  NAME CTestScripts_simple_posfix_and_args_1
  POSTFIX_AND_ARGS_0 test1 "This is a crazy test!" 1
  PASS_REGULAR_EXPRESSION "[^=]This is a crazy test"
  NUM_MPI_PROCS 1
  )

TRIBITS_ADD_TEST( GenericDriver
  NAME CTestScripts_simple_posfix_and_args_2
  POSTFIX_AND_ARGS_0 test1 "This is a crazy test!" 0
  POSTFIX_AND_ARGS_1 test2 "This is a silly test!" 0
  NUM_MPI_PROCS 1
  )

TRIBITS_ADD_TEST( GenericDriver
  NAME CTestScripts_will_fail
  POSTFIX_AND_ARGS_0 test1 "This test is supposed to fail!" 1
  WILL_FAIL
  NUM_MPI_PROCS 1
  )
  # If you comment out WILL_FAIL above, then the final test result is "failed"
  # due to the non-zero returncode being.

TRIBITS_ADD_TEST( GenericDriver
  NAME CTestScripts_will_fail_pass_regular_expression
  POSTFIX_AND_ARGS_0 test1 "This test is expected the regex!" 0
  PASS_REGULAR_EXPRESSION "Does not match string"
  WILL_FAIL
  NUM_MPI_PROCS 1
  )
  # The above test shows that the built-in WILL_FAIL just inverts the
  # pass/fail result of the other criteria, PASS_REGULAR_EXPRESSION in this
  # case.  If you comment out the WILL_FAIL, then this test final result is
  # "failed"!

TRIBITS_ADD_TEST( GenericDriver
  NAME CTestScripts_will_fail_fail_regular_exprssion
  POSTFIX_AND_ARGS_0 test1 "Printing a string that is matched with FAIL_REGULAR_EXPRESSION!" 0
  FAIL_REGULAR_EXPRESSION "matched with FAIL_REGULAR_EXPRESSION"
  WILL_FAIL
  NUM_MPI_PROCS 1
  )
  # The above test shows that the built-in WILL_FAIL just inverts the
  # pass/fail result of the other criteria, FAIL_REGULAR_EXPRESSION in this
  # case.  If you comment out WILL_FAIL, then this test final result is failed
  # (because the FAIL_REGULAR_EXPRESSION matched the STDOUT).

TRIBITS_ADD_TEST( GenericDriver
  NAME CTestScripts_pass_regular_expression_fail_regular_exprssion_will_fail
  POSTFIX_AND_ARGS_0 test1 "This says PASS!  This says FAIL!" 1
  PASS_REGULAR_EXPRESSION "This says PASS"
  FAIL_REGULAR_EXPRESSION "This says FAIL"
  WILL_FAIL
  NUM_MPI_PROCS 1
  )
  # The above test shows that FAIL_REGULAR_EXPRESSION takes precedence over
  # PASS_REGULAR_EXPRESSION.  The final WILL_FAIL inverts that and allows the
  # test to pass.  If you comment out WILL_FAIL, the final result will be
  # "failed".  If you comment out FAIL_REGULAR_EXPRESSION, the final result
  # will be "failed".


FUNCTION(CTestScripts_fail_regular_exprssion_w_circular_ref_detection_tests)

  # Create private namespace for setting var
  SET(${PACKAGE_NAME}_ENABLE_CIRCULAR_REF_DETECTION_FAILURE TRUE)

  TRIBITS_ADD_TEST( GenericDriver
    NAME CTestScripts_fail_regular_exprssion_w_circular_ref_detection_1
    POSTFIX_AND_ARGS_0 test1 "Printing a string that is matched with FAIL_REGULAR_EXPRESSION!" 0
    FAIL_REGULAR_EXPRESSION "matched with FAIL_REGULAR_EXPRESSION"
    WILL_FAIL
    NUM_MPI_PROCS 1
    )
    # The above tests makes sure that the passed-in regex is used to match and
    # fail the test.  If you comment out WILL_FAIL, you will see the test
    # fail.

  TRIBITS_ADD_TEST( GenericDriver
    NAME CTestScripts_fail_regular_exprssion_w_circular_ref_detection_2
    POSTFIX_AND_ARGS_0 test1 "Some stuff\n\nThe following Teuchos::RCPNode objects were created\n\nsome other stuff" 0
    FAIL_REGULAR_EXPRESSION "Some other bad outptut taht does not match"
    WILL_FAIL
    NUM_MPI_PROCS 1
    )
    # The above tests makes sure that the passed-in regex is used to match and
    # fail the test does not overwrite the circular detection regex.  If you
    # comment out WILL_FAIL, you will see the test fail.

  TRIBITS_ADD_TEST( GenericDriver
    NAME CTestScripts_fail_regular_exprssion_w_circular_ref_detection_3
    POSTFIX_AND_ARGS_0 test1 "Some stuff\n\nThe following Teuchos::RCPNode objects were created\n\nsome other stuff" 0
    WILL_FAIL
    NUM_MPI_PROCS 1
    )
    # The above tests makes sure that the default circular detection regex is
    # present.  If you comment out WILL_FAIL, you will see the test fail.

ENDFUNCTION()

CTestScripts_fail_regular_exprssion_w_circular_ref_detection_tests()

TRIBITS_ADD_ADVANCED_TEST(
  CTestScripts_cmnd_1_args_1_print_msg
  TEST_0 EXEC GenericDriver ARGS "This is a crazy test!" 1
  FINAL_PASS_REGULAR_EXPRESSION "\"This is a crazy test"
  )

TRIBITS_ADD_ADVANCED_TEST(
  CTestScripts_cmnd_1_args_1_print_msg_no_echo_output
  TEST_0 EXEC GenericDriver ARGS "This is a crazy test!" 0
    NO_ECHO_OUTPUT
  FINAL_FAIL_REGULAR_EXPRESSION "\"This is a crazy test\""
  OVERALL_NUM_MPI_PROCS 1
  )

TRIBITS_ADD_ADVANCED_TEST(
  CTestScripts_cmnd_1_args_1_return_code
  TEST_0 EXEC GenericDriver ARGS "Dummy msg" 1
  FINAL_PASS_REGULAR_EXPRESSION "TEST_0: Return code = 1"
  OVERALL_NUM_MPI_PROCS 1
  )

TRIBITS_ADD_ADVANCED_TEST(
  CTestScripts_cmnd_1_args_1_print_msg_out_file
  TEST_0 EXEC GenericDriver ARGS "This is a crazy test!" 5
    OUTPUT_FILE cmnd_1_args_1_print_msg_out_file_outputFile.out
    PASS_REGULAR_EXPRESSION "This is a crazy test"
  OVERALL_NUM_MPI_PROCS 1
  )

TRIBITS_ADD_ADVANCED_TEST(
  CTestScripts_cmnd_1_args_1_pass_any_test_0
  TEST_0 EXEC GenericDriver ARGS "Dummy msg" 7
    PASS_ANY
  FINAL_PASS_REGULAR_EXPRESSION "TEST_0: Pass criteria = Pass Any"
  OVERALL_NUM_MPI_PROCS 1
  )

TRIBITS_ADD_ADVANCED_TEST(
  CTestScripts_cmnd_1_args_1_pass_any_overall
  TEST_0 EXEC GenericDriver ARGS "Dummy msg" 7
    PASS_ANY
  OVERALL_NUM_MPI_PROCS 1
  )

TRIBITS_ADD_ADVANCED_TEST(
  CTestScripts_cmnd_1_args_1_standard_pass_output
  TEST_0 EXEC GenericDriver ARGS "Dummy msg" 7
    STANDARD_PASS_OUTPUT
  OVERALL_NUM_MPI_PROCS 1
  )

TRIBITS_ADD_ADVANCED_TEST(
  CTestScripts_cmnd_1_args_2_stderr_pass_regular_expression_all
  TEST_0 EXEC GenericDriver
    ARGS "This is a crazy test\n\nThis is not the best test" 5 "This goes to stderr"
    OUTPUT_FILE cmnd_1_args_1_pass_regular_expression_all_outputFile.out
    PASS_REGULAR_EXPRESSION_ALL "This is a crazy test" "This is not the best test" "This goes to stderr"
  OVERALL_NUM_MPI_PROCS 1
  )

TRIBITS_ADD_ADVANCED_TEST(
  CTestScripts_cmnd_1_args_1_pass_regular_expression_all_compare_1
  TEST_0 EXEC GenericDriver
    ARGS "This is a crazy test\n\nThis is not the best test" 5
    OUTPUT_FILE cmnd_1_args_1_pass_regular_expression_all_compare_1_outputFile.out
    PASS_REGULAR_EXPRESSION_ALL "This is a crazy test" "This is not the best test"
  FINAL_PASS_REGULAR_EXPRESSION "TEST_0: Pass criteria = Match REGEX {This is a crazy test} [^a]PASSED[^a]"
  OVERALL_NUM_MPI_PROCS 1
  )

TRIBITS_ADD_ADVANCED_TEST(
  CTestScripts_cmnd_1_args_1_pass_regular_expression_all_compare_2
  TEST_0 EXEC GenericDriver
    ARGS "This is a crazy test\n\nThis is not the best test" 5
    OUTPUT_FILE cmnd_1_args_1_pass_regular_expression_all_compare_2_outputFile.out
    PASS_REGULAR_EXPRESSION_ALL "This is a crazy test" "This is not the best test"
  FINAL_PASS_REGULAR_EXPRESSION "TEST_0: Pass criteria = Match REGEX {This is not the best test} [^a]PASSED[^a]"
  OVERALL_NUM_MPI_PROCS 1
  )

# 2009/04/06: rabartl: Above, I can't use '[' or ']' in the regular expression
# because it is interpreted as a char list.  Therefore, I leave it as not 'a'
# and that is good enough for me.

TRIBITS_ADD_ADVANCED_TEST(
  CTestScripts_cmnd_1_args_1_print_msg_out_file_no_echo_output
  TEST_0 EXEC GenericDriver
    ARGS "This is a crazy test!" 5
    OUTPUT_FILE cmnd_1_args_1_print_msg_out_file_no_echo_output_outputFile.out
    NO_ECHO_OUTPUT
  FINAL_FAIL_REGULAR_EXPRESSION "^This is a crazy test"
  OVERALL_NUM_MPI_PROCS 1
  )

TRIBITS_ADD_ADVANCED_TEST(
  CTestScripts_cmnd_1_args_1_message
  TEST_0 EXEC GenericDriver
    ARGS "Dummy msg" 1
    MESSAGE "This is a crazy test!"
  FINAL_PASS_REGULAR_EXPRESSION "This is a crazy test"
  OVERALL_NUM_MPI_PROCS 1
  )

TRIBITS_ADD_ADVANCED_TEST(
  CTestScripts_cmnd_1_args_1_working_directory
  TEST_0 EXEC GenericDriver
    ARGS "This is a crazy test!" 0
    WORKING_DIRECTORY TEST_NAME
    OUTPUT_FILE cmnd_1_args_1_working_directory_console.out
  OVERALL_NUM_MPI_PROCS 1
  )

TRIBITS_ADD_ADVANCED_TEST(
  CTestScripts_cmnd_2_args_1_basic
  TEST_0 EXEC GenericDriver
    ARGS "This is the first test" 3
    PASS_REGULAR_EXPRESSION "first test"
  TEST_1 EXEC GenericDriver
    ARGS "This is the second test" 4
    PASS_REGULAR_EXPRESSION "second test"
  OVERALL_NUM_MPI_PROCS 1
  )

TRIBITS_ADD_ADVANCED_TEST(
  CTestScripts_cmnd_2_args_1_check_second_print
  TEST_0 EXEC GenericDriver
    ARGS "This is the first test" 3
    PASS_REGULAR_EXPRESSION "first test"
  TEST_1 EXEC GenericDriver
    ARGS "This is the second test" 4
    PASS_REGULAR_EXPRESSION "second test"
  FINAL_PASS_REGULAR_EXPRESSION "second test"
  OVERALL_NUM_MPI_PROCS 1
  )

TRIBITS_ADD_ADVANCED_TEST(
  CTestScripts_cmnd_2_fail_fast
  TEST_0 EXEC GenericDriver
    ARGS "This first test will fail" 3
  TEST_1 EXEC GenericDriver
    ARGS "This is the second test will never be run" 0
  FAIL_FAST
  FINAL_PASS_REGULAR_EXPRESSION "TEST_0: FAIL FAST, SKIPPING REST OF TEST CASES!"
  OVERALL_NUM_MPI_PROCS 1
  )

TRIBITS_ADD_ADVANCED_TEST(
  CTestScripts_cmnd_2_no_fail_fast_print_msg
  TEST_0 EXEC GenericDriver
    ARGS "This first test will fail" 3
  TEST_1 EXEC GenericDriver
    ARGS "This is the second test should be run" 0
  FINAL_PASS_REGULAR_EXPRESSION "This is the second test should be run"
  OVERALL_NUM_MPI_PROCS 1
  )

TRIBITS_ADD_ADVANCED_TEST(
  CTestScripts_cmnd_2_no_fail_fast_final_fail
  TEST_0 EXEC GenericDriver
    ARGS "This first test will fail" 3
  TEST_1 EXEC GenericDriver
    ARGS "This is the second test should be run" 0
  FINAL_PASS_REGULAR_EXPRESSION "OVERALL FINAL RESULT: TEST FAILED"
  OVERALL_NUM_MPI_PROCS 1
  )

IF (CMAKE_HOST_SYSTEM_NAME STREQUAL "Windows")
  # cmake -E compare_files only gives return != 0 if the files don't compare.
  # It gives no diff output.
  SET(DIFF_COMMAND_STUFF "${CMAKE_COMMAND}" ARGS -E compare_files)
ELSE()
  # Diff gives output of the diff so it is better to use if we have it.
  # Otherwise, I need to write a portable diff (using a CMake -P script).
  SET(DIFF_COMMAND_STUFF diff ARGS)
ENDIF()

TRIBITS_ADD_ADVANCED_TEST(
  CTestScripts_cmnd_3_args_1_overall_working_directory
  MESSAGE "NOTE: This test does not check the order of STDOUT and STDERR, only that both exist in the output file.  It seems that EXECUTE_PROCESS() and MPI do not behave well together w.r.t. to STDOUT and STDERR outputting.  The fault may be with the MPI implementation.  Also, even in serial it would seem that the order of STDOUT and STDERR gets messed up when the machine is loaded."
  OVERALL_WORKING_DIRECTORY TEST_NAME
  TEST_0 EXEC GenericDriver
    ARGS "This is a crazy test!" 0 "This is a bad crazy test!"
    OUTPUT_FILE cmnd_3_args_1_overall_working_directory_console.out
  TEST_1 CMND cat
    ARGS cmnd_3_args_1_overall_working_directory_console.out
    PASS_REGULAR_EXPRESSION_ALL
       "This is a crazy test"
       "This is a bad crazy test"
  OVERALL_NUM_MPI_PROCS 1
  XHOSTTYPE Windows
  )
# NOTE: The above test does not run on Windows because it relies on the 'cat'
# command.  The form of this test is needed in order to check that both STDOUT
# and STDERR output are both in the output file but we can't rely on the
# order.  It seems that EXECUTE_PROCESS() and mpiexec don't work together to
# produce ordered STDOUT and STDERR very well.  Also, even in serial, it seems
# that when the machine is loaded that the order of STDOUT and STDERR can get
# messed up.  It is not clear if this is a problem with EXECUTE_PROCESS() or
# not.


#
# Test creation and optional preservation of working directories
#

TRIBITS_ADD_ADVANCED_TEST(
  CTestScripts_cmnd_3_args_1_overall_working_directory_working_directory
  OVERALL_WORKING_DIRECTORY
    CTestScripts_cmnd_3_args_1_overall_working_directory_working_directory
  TEST_0 EXEC GenericDriver
    ARGS "This is another crazy test!" 0
    OUTPUT_FILE cmnd_3_args_1_overall_working_directory_working_directory_console.out
    WORKING_DIRECTORY GenericDriver
    SKIP_CLEAN_WORKING_DIRECTORY
  TEST_1 CMND "${CMAKE_COMMAND}"
    ARGS -E copy
      ../GenericDriver/cmnd_3_args_1_overall_working_directory_working_directory_console.out
      cmnd_3_args_1_overall_working_directory_working_directory_console.gold.out
    WORKING_DIRECTORY Gold
  TEST_2 CMND ${DIFF_COMMAND_STUFF}  # Contains the ARGS part
    GenericDriver/cmnd_3_args_1_overall_working_directory_working_directory_console.out
    Gold/cmnd_3_args_1_overall_working_directory_working_directory_console.gold.out
  OVERALL_NUM_MPI_PROCS 1
  ADDED_TEST_NAME_OUT
    CTestScripts_cmnd_3_args_1_overall_working_directory_working_directory_TEST_NAME
  )

# This test uses the same working directory and relies on it not being deleted
# so it still contains the output file.
TRIBITS_ADD_ADVANCED_TEST(
  CTestScripts_cmnd_3_args_1_overall_working_directory_working_directory_skip_clean
  OVERALL_WORKING_DIRECTORY
    "${CMAKE_CURRENT_BINARY_DIR}/CTestScripts_cmnd_3_args_1_overall_working_directory_working_directory"
  SKIP_CLEAN_OVERALL_WORKING_DIRECTORY
  SKIP_CLEAN_OVERALL_WORKING_DIRECTORY
  TEST_0 CMND "${CMAKE_COMMAND}"
    ARGS -E copy
      cmnd_3_args_1_overall_working_directory_working_directory_console.out
      cmnd_3_args_1_overall_working_directory_working_directory_console.gold.out
    WORKING_DIRECTORY
      "${CMAKE_CURRENT_BINARY_DIR}/CTestScripts_cmnd_3_args_1_overall_working_directory_working_directory/GenericDriver"
    SKIP_CLEAN_WORKING_DIRECTORY
  TEST_1 CMND ${DIFF_COMMAND_STUFF}  # Contains the ARGS part
    GenericDriver/cmnd_3_args_1_overall_working_directory_working_directory_console.out
    GenericDriver/cmnd_3_args_1_overall_working_directory_working_directory_console.gold.out
  OVERALL_NUM_MPI_PROCS 1
  ADDED_TEST_NAME_OUT
    CTestScripts_cmnd_3_args_1_overall_working_directory_working_directory_skip_clean_TEST_NAME
  )

# You have to run the above two tests in sequence it the second test can't
# pass.
SET_PROPERTY(  TEST
  ${CTestScripts_cmnd_3_args_1_overall_working_directory_working_directory_skip_clean_TEST_NAME}
  PROPERTY DEPENDS
    ${CTestScripts_cmnd_3_args_1_overall_working_directory_working_directory_TEST_NAME}
  )

# Demonstrate processes never dying

IF (PERL_EXECUTABLE AND TriBITS_ENABLE_RUNS_FOREVER_TEST)
  
  TRIBITS_ADD_EXECUTABLE(
    RunsForever
    SOURCES RunsForever.cpp
    )
  
  TRIBITS_ADD_ADVANCED_TEST(
    CTestScripts_RunsForever
    TEST_0 CMND ${PERL_EXECUTABLE} ARGS ${CMAKE_CURRENT_SOURCE_DIR}/runs_forever.pl
    OVERALL_NUM_MPI_PROCS 1
    )

ENDIF()

# ENVIRONMENT

TRIBITS_ADD_TEST( "${CMAKE_COMMAND}" NOEXEPREFIX NOEXESUFFIX
  NAME CTestScripts_TAT_pass_env
  ARGS "-P ${CMAKE_CURRENT_SOURCE_DIR}/EchoEnvVarForTest.cmake"
  NUM_MPI_PROCS 1
  ENVIRONMENT PASS_IN_FROM_ENV_VAR=ThisWasPassedCorrectly
  PASS_REGULAR_EXPRESSION "PASS_IN_FROM_ENV_VAR: ThisWasPassedCorrectly"
  )

TRIBITS_ADD_ADVANCED_TEST( CTestScripts_TAAT_pass_env
  TEST_0 CMND ${CMAKE_COMMAND}
    ARGS -P ${CMAKE_CURRENT_SOURCE_DIR}/EchoEnvVarForTest.cmake
    NUM_MPI_PROCS 1
    PASS_REGULAR_EXPRESSION "PASS_IN_FROM_ENV_VAR: ThisWasPassedCorrectly"
  ENVIRONMENT PASS_IN_FROM_ENV_VAR=ThisWasPassedCorrectly
  )

# TAAT() WILL_FAIL and FAIL_REGULAR_EXPRESSION

TRIBITS_ADD_ADVANCED_TEST(
  CTestScripts_TAAT_will_fail_return_code
  TEST_0 EXEC GenericDriver
    ARGS "We expect this test to fail" 1
    WILL_FAIL
  OVERALL_NUM_MPI_PROCS 1
  )

TRIBITS_ADD_ADVANCED_TEST(
  CTestScripts_TAAT_will_fail_pass_regular_expression
  TEST_0 EXEC GenericDriver
    ARGS "This test passes?" 1
    PASS_REGULAR_EXPRESSION "This test PASSES" # will not match
    WILL_FAIL
  OVERALL_NUM_MPI_PROCS 1
  )

TRIBITS_ADD_ADVANCED_TEST(
  CTestScripts_TAAT_will_fail_fail_regular_expression
  TEST_0 EXEC GenericDriver
    ARGS "This test failed!" 0
    FAIL_REGULAR_EXPRESSION "This test failed"
    WILL_FAIL
  OVERALL_NUM_MPI_PROCS 1
  )

TRIBITS_ADD_ADVANCED_TEST(
  CTestScripts_TAAT_will_fail_pass_regular_expression_fail_regular_expression
  TEST_0 EXEC GenericDriver
    ARGS "This test passed!  This test failed" 1
    PASS_REGULAR_EXPRESSION "This test passed"
    FAIL_REGULAR_EXPRESSION "This test failed"
    WILL_FAIL
  OVERALL_NUM_MPI_PROCS 1
  )

# TAAT() ALWAYS_FAIL_ON_NONZERO_RETURN

TRIBITS_ADD_ADVANCED_TEST(
  CTestScripts_TAAT_pass_regular_expression_always_fail_on_nonzero_return
  TEST_0 EXEC GenericDriver
    ARGS "This test passed!" 1
    PASS_REGULAR_EXPRESSION "This test passed"
    ALWAYS_FAIL_ON_NONZERO_RETURN
    WILL_FAIL
  OVERALL_NUM_MPI_PROCS 1
  )
  # Comment out WILL_FAIL and you will see th test fails because
  # ALWAYS_FAIL_ON_NONZERO_RETURN is speicfied.

TRIBITS_ADD_ADVANCED_TEST(
  CTestScripts_TAAT_pass_regular_expression_all_always_fail_on_nonzero_return
  TEST_0 EXEC GenericDriver
    ARGS "This test passed!" 1
    PASS_REGULAR_EXPRESSION_ALL  "This test"  "This test passed"
    ALWAYS_FAIL_ON_NONZERO_RETURN
    WILL_FAIL
  OVERALL_NUM_MPI_PROCS 1
  )
  # Comment out WILL_FAIL and you will see th test fails because
  # ALWAYS_FAIL_ON_NONZERO_RETURN is speicfied.
