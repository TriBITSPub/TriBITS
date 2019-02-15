#
# ctest -P script to do and update of the base git repo.
#
# ToDo: Finish documentation
#

message("cmake -P tribits_ctest_update_commands.cmake:")
message("-- GIT_EXE=${GIT_EXE}")
message("-- REMOTE_NAME=${REMOTE_NAME}")
message("-- BRANCH=${BRANCH}")
message("-- UNIT_TEST_MODE=${UNIT_TEST_MODE}")

set(OVERALL_SUCCESS TRUE)
set(ERROR_CODE 0)

macro(execute_process_wrapper)
  message("\nRunning: execute_process(${ARGN})")
  if (NOT UNIT_TEST_MODE)
    execute_process(${ARGN} RESULT_VARIABLE RTN_CODE)
    message("RESULT_VARIABLE=${RTN_CODE}")
    IF (NOT "${RTN_CODE}" STREQUAL "0")
      set(OVERALL_SUCCESS FALSE)
      set(ERROR_CODE ${RTN_CODE})
    endif()
  endif()
endmacro()

execute_process_wrapper(
  COMMAND "${GIT_EXE}" fetch ${REMOTE_NAME} )

execute_process_wrapper(
  COMMAND "${GIT_EXE}" clean -fdx )

execute_process_wrapper(
  COMMAND "${GIT_EXE}" reset --hard HEAD )

if (BRANCH)
  execute_process_wrapper(
    COMMAND "${GIT_EXE}" checkout -B ${BRANCH} --track ${REMOTE_NAME}/${BRANCH} )
else()
  execute_process_wrapper(
    COMMAND "${GIT_EXE}" reset --hard @{u} )
endif()

if (OVERALL_SUCCESS)
  message("\nGit Update PASSED!")
else()
  message(FATAL_ERROR "Git Update FAILED!")
endif()
