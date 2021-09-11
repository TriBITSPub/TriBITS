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


########################################################################
# Helper functions and macros
########################################################################


function(get_regex_correct_string  INPUT_STR  OUTPUT_STR_VAR_OUT)
  set(OUTPUT_STR "${INPUT_STR}")
  string(REPLACE "+" "[+]" OUTPUT_STR "${OUTPUT_STR}")
  string(REPLACE "." "[.]" OUTPUT_STR "${OUTPUT_STR}")
  set(${OUTPUT_STR_VAR_OUT} "${OUTPUT_STR}" PARENT_SCOPE)
endfunction()


macro(get_regex_correct_cmake_lang_compiler  LANG)
  get_regex_correct_string("${CMAKE_${LANG}_COMPILER}" CMAKE_${LANG}_COMPILER_FOR_REGEX)
endmacro()

########################################################################
# Common arguments for all inner CMake and TriBITS projects
########################################################################

include(${CMAKE_CURRENT_LIST_DIR}/GetCompilerPassthroughArgs.cmake)

if (CMAKE_HOST_SYSTEM_NAME STREQUAL "Linux")
  set(IS_REAL_LINUX_SYSTEM ON)
else()
  set(IS_REAL_LINUX_SYSTEM OFF)
endif()

get_regex_correct_cmake_lang_compiler(CXX)
get_regex_correct_cmake_lang_compiler(C)
get_regex_correct_cmake_lang_compiler(Fortran)


########################################################################
# RawHelloWorld
########################################################################


tribits_add_advanced_test( RawHelloWorld
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  TEST_0 CMND ${CMAKE_COMMAND}
    ARGS
      ${SERIAL_PASSTHROUGH_CONFIGURE_ARGS}
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/RawHelloWorld
    PASS_REGULAR_EXPRESSION_ALL
      "Configuring done"
      "Generating done"
      "Build files have been written to: .*ExamplesUnitTests/TriBITS_RawHelloWorld"
  TEST_1 CMND make
    ARGS ${CTEST_BUILD_FLAGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Built target hello_world_lib"
      "Built target hello_world"
      "Built target unit_tests"
  TEST_2 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    PASS_REGULAR_EXPRESSION_ALL
      ": test .*  Passed"
      ": unit_test .*  Passed"
      "100% tests passed, 0 tests failed out of 2"
  )


########################################################################
# TribitsHelloWorld
########################################################################


set(TribitsHelloWorld_COMMON_CONFIG_ARGS
  ${SERIAL_PASSTHROUGH_CONFIGURE_ARGS}
  )

tribits_add_advanced_test( TribitsHelloWorld
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  TEST_0 CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsHelloWorld_COMMON_CONFIG_ARGS}
      -DTribitsHelloWorld_ENABLE_TESTS=ON
      -DHelloWorld_ENABLE_CPACK_PACKAGING=ON
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsHelloWorld
    PASS_REGULAR_EXPRESSION_ALL
      "Configuring done"
      "Generating done"
      "Build files have been written to: .*ExamplesUnitTests/TriBITS_TribitsHelloWorld"
    FAIL_REGULAR_EXPRESSION
      "Check for working Fortran compiler" # Should not be looking for Fortran!
  TEST_1 CMND make
    ARGS ${CTEST_BUILD_FLAGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Built target hello_world_lib"
      "Built target hello_world"
      "Built target HelloWorld_unit_tests"
  TEST_2 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    PASS_REGULAR_EXPRESSION_ALL
      ": HelloWorld_hello_world .*  Passed"
      ": HelloWorld_unit_tests .*  Passed"
      "100% tests passed, 0 tests failed out of 2"
  )


tribits_add_advanced_test( TribitsHelloWorld_EXE_DISABLE
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  TEST_0 CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsHelloWorld_COMMON_CONFIG_ARGS}
      -DTribitsHelloWorld_ENABLE_TESTS=ON
      -DHelloWorld_unit_tests_EXE_DISABLE=ON
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsHelloWorld
    PASS_REGULAR_EXPRESSION_ALL
      "-- HelloWorld_unit_tests EXE NOT being built due to HelloWorld_unit_tests_EXE_DISABLE=[']ON[']"
      "Configuring done"
      "Generating done"
      "Build files have been written to: .*ExamplesUnitTests/TriBITS_TribitsHelloWorld"
  TEST_1 CMND make
    ARGS ${CTEST_BUILD_FLAGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Built target hello_world_lib"
      "Built target hello_world"
  TEST_2 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    PASS_REGULAR_EXPRESSION_ALL
      "Test [#]2: HelloWorld_unit_tests [.]+[*][*][*]Not Run"
      ": HelloWorld_hello_world .*  Passed"
      "2 - HelloWorld_unit_tests [(]Not Run[)]"
      "50% tests passed, 1 tests failed out of 2"
  )
  # NOTE: Above we are testing the <exec_name>_EXE_DISABLE option in a full
  # configure and build case because the tribits_add_executable() command is
  # not set up for unit-testing mode.


tribits_add_advanced_test( TribitsHelloWorld_InSourceBuildErrors
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    CMND ${CMAKE_COMMAND}
    ARGS -E copy_directory
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsHelloWorld
      TribitsHelloWorld

  TEST_1
    MESSAGE "Try an in-source configure and check error message"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsHelloWorld_COMMON_CONFIG_ARGS}
      -DTribitsHelloWorld_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      .
    WORKING_DIRECTORY TribitsHelloWorld
    SKIP_CLEAN_WORKING_DIRECTORY
    PASS_REGULAR_EXPRESSION_ALL
      "CMAKE_CURRENT_SOURCE_DIR=.*/TriBITS_TribitsHelloWorld_InSourceBuildErrors/TribitsHelloWorld"
      "CMAKE_CURRENT_BINARY_DIR=.*/TriBITS_TribitsHelloWorld_InSourceBuildErrors/TribitsHelloWorld"
      "TribitsHelloWorld does not support in source builds"
      "NOTE: You must now delete the CMakeCache.txt file and the CMakeFiles/"
      "Please create a different directory and configure"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_2
    MESSAGE "Try configure in build subdir and check for bad CMakeCache.txt file"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsHelloWorld_COMMON_CONFIG_ARGS}
      -DTribitsHelloWorld_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      ..
    WORKING_DIRECTORY TribitsHelloWorld/BUILD
    PASS_REGULAR_EXPRESSION_ALL
      "TriBITS_TribitsHelloWorld_InSourceBuildErrors/TribitsHelloWorld/CMakeCache.txt"
      "exists from a likely prior attempt to do an in-source build"
      ""
    ALWAYS_FAIL_ON_ZERO_RETURN

  )


tribits_add_advanced_test( TribitsHelloWorld_DefaultGlobalTimeout
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Configure first time not setting any default timeout."
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsHelloWorld_COMMON_CONFIG_ARGS}
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsHelloWorld
    ALWAYS_FAIL_ON_NONZERO_RETURN
  TEST_1
    MESSAGE "Make sure that 'TimeOut' is set to the CMake default of 1500"
    CMND grep ARGS "^TimeOut: " DartConfiguration.tcl
    PASS_REGULAR_EXPRESSION "TimeOut: 1500"
  TEST_2
    MESSAGE "Make sure DART_TESTING_TIMEOUT in cache is the CMake default 1500!"
    CMND grep ARGS "^DART_TESTING_TIMEOUT:" CMakeCache.txt
    PASS_REGULAR_EXPRESSION "DART_TESTING_TIMEOUT:STRING=1500"

  TEST_3
    MESSAGE "Reconfigure and make sure the timeout is still set correctly"
    CMND ${CMAKE_COMMAND} ARGS .
    PASS_REGULAR_EXPRESSION_ALL "Generating done"
  TEST_4
    MESSAGE "Make sure that 'TimeOut' is set correctly on reconfigure"
    CMND grep ARGS "^TimeOut: " DartConfiguration.tcl
    PASS_REGULAR_EXPRESSION "TimeOut: 1500"
  TEST_5
    MESSAGE "Make sure DART_TESTING_TIMEOUT in cache is still the default"
    CMND grep ARGS "^DART_TESTING_TIMEOUT:" CMakeCache.txt
    PASS_REGULAR_EXPRESSION "DART_TESTING_TIMEOUT:STRING=1500"

  )


tribits_add_advanced_test( TribitsHelloWorld_DefaultGlobalTimeout_ScaleTimeout
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Configure first time not setting any default timeout but scale it."
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsHelloWorld_COMMON_CONFIG_ARGS}
      -DTribitsHelloWorld_SCALE_TEST_TIMEOUT=2.0
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsHelloWorld
    ALWAYS_FAIL_ON_NONZERO_RETURN
  TEST_1
    MESSAGE "Make sure that default 'TimeOut' is scaled correctly by 2.0"
    CMND grep ARGS "^TimeOut: " DartConfiguration.tcl
    PASS_REGULAR_EXPRESSION "TimeOut: 3000"
  TEST_2
    MESSAGE "Make sure DART_TESTING_TIMEOUT in cache is CMake default 1500"
    CMND grep ARGS "^DART_TESTING_TIMEOUT:" CMakeCache.txt
    PASS_REGULAR_EXPRESSION "DART_TESTING_TIMEOUT:STRING=1500"

  TEST_3
    MESSAGE "Reconfigure and make sure the timeout is still set correctly"
    CMND ${CMAKE_COMMAND} ARGS .
    PASS_REGULAR_EXPRESSION_ALL "Generating done"
  TEST_4
    MESSAGE "Make sure that 'TimeOut' is set correctly on reconfigure"
    CMND grep ARGS "^TimeOut: " DartConfiguration.tcl
    PASS_REGULAR_EXPRESSION "TimeOut: 3000"
  TEST_5
    MESSAGE "Make sure DART_TESTING_TIMEOUT in cache is still the default"
    CMND grep ARGS "^DART_TESTING_TIMEOUT:" CMakeCache.txt
    PASS_REGULAR_EXPRESSION "DART_TESTING_TIMEOUT:STRING=1500"

  )


tribits_add_advanced_test( TribitsHelloWorld_ScaleTimeout_FirstConfig
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Configure first time out scaling the timeout."
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsHelloWorld_COMMON_CONFIG_ARGS}
      -DDART_TESTING_TIMEOUT=200.0
      -DTribitsHelloWorld_SCALE_TEST_TIMEOUT=1.5
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsHelloWorld
    PASS_REGULAR_EXPRESSION_ALL "Generating done"
  TEST_1
    MESSAGE "Make sure that 'TimeOut' is set correctly on the first try"
    CMND grep ARGS "^TimeOut: " DartConfiguration.tcl
    PASS_REGULAR_EXPRESSION "TimeOut: 300"
  TEST_2
    MESSAGE "Make sure DART_TESTING_TIMEOUT in cache is what the user passed in!"
    CMND grep ARGS "^DART_TESTING_TIMEOUT:" CMakeCache.txt
    PASS_REGULAR_EXPRESSION "DART_TESTING_TIMEOUT:STRING=200.0"

  TEST_3
    MESSAGE "Reconfigure and make sure the timeout is still set correctly"
    CMND ${CMAKE_COMMAND} ARGS .
    PASS_REGULAR_EXPRESSION_ALL "Generating done"
  TEST_4
    MESSAGE "Make sure that 'TimeOut' is set correctly on reconfigure"
    CMND grep ARGS "^TimeOut: " DartConfiguration.tcl
    PASS_REGULAR_EXPRESSION "TimeOut: 300"
  TEST_5
    MESSAGE "Make sure DART_TESTING_TIMEOUT in cache is still what the user passed in!"
    CMND grep ARGS "^DART_TESTING_TIMEOUT:" CMakeCache.txt
    PASS_REGULAR_EXPRESSION "DART_TESTING_TIMEOUT:STRING=200.0"

  )


tribits_add_advanced_test( TribitsHelloWorld_ScaleTimeout_Reconfig
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0 CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsHelloWorld_COMMON_CONFIG_ARGS}
      -DDART_TESTING_TIMEOUT=200.0
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsHelloWorld
    PASS_REGULAR_EXPRESSION_ALL "Generating done"
    MESSAGE "Configure with default 1.0 scaling"
  TEST_1 CMND grep ARGS "^TimeOut: " DartConfiguration.tcl
    PASS_REGULAR_EXPRESSION "TimeOut: 200.0"
  TEST_2 CMND grep ARGS "^DART_TESTING_TIMEOUT:" CMakeCache.txt
    MESSAGE "DART_TESTING_TIMEOUT in cache does not change!"
    PASS_REGULAR_EXPRESSION "DART_TESTING_TIMEOUT:STRING=200.0"

  TEST_3 CMND ${CMAKE_COMMAND}
    ARGS
      -DTribitsHelloWorld_SCALE_TEST_TIMEOUT=1.5
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsHelloWorld
    MESSAGE "Configure with 1.5 scaling"
    PASS_REGULAR_EXPRESSION_ALL
      "DART_TESTING_TIMEOUT=200.0 being scaled by TribitsHelloWorld_SCALE_TEST_TIMEOUT=1.5 to 300"
      "Generating done"

  TEST_4 CMND grep ARGS "^TimeOut: " DartConfiguration.tcl
    PASS_REGULAR_EXPRESSION "TimeOut: 300"
  TEST_5 CMND grep ARGS "^DART_TESTING_TIMEOUT:" CMakeCache.txt
    MESSAGE "DART_TESTING_TIMEOUT in cache does not change!"
    PASS_REGULAR_EXPRESSION "DART_TESTING_TIMEOUT:STRING=200.0"

  TEST_6 CMND ${CMAKE_COMMAND}
    ARGS
      -DTribitsHelloWorld_SCALE_TEST_TIMEOUT=2.0
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsHelloWorld
    MESSAGE "Configure with 2.0 scaling"
    PASS_REGULAR_EXPRESSION_ALL
      "DART_TESTING_TIMEOUT=200.0 being scaled by TribitsHelloWorld_SCALE_TEST_TIMEOUT=2.0 to 400"
      "Generating done"
  TEST_7 CMND grep ARGS "^TimeOut: " DartConfiguration.tcl
    PASS_REGULAR_EXPRESSION "TimeOut: 400"
  TEST_8 CMND grep ARGS "^DART_TESTING_TIMEOUT:" CMakeCache.txt
    MESSAGE "DART_TESTING_TIMEOUT in cache does not change!"
    PASS_REGULAR_EXPRESSION "DART_TESTING_TIMEOUT:STRING=200.0"

  )


if (TriBITS_EANBLE_Fortran)
 set(TribitsHelloWorld_XSDK_DEFAULTS_Fortran_REGEX
    "-- XSDK: Setting CMAKE_Fortran_COMPILER from env var FC=")
else()
 set(TribitsHelloWorld_XSDK_DEFAULTS_Fortran_REGEX)
endif()


tribits_add_advanced_test( TribitsHelloWorld_XSDK_DEFAULTS
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0 CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsHelloWorld_COMMON_CONFIG_ARGS}
      -DUSE_XSDK_DEFAULTS=TRUE
      -DCMAKE_C_COMPILER=
      -DCMAKE_CXX_COMPILER=
      -DCMAKE_Fortran_COMPILER=
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsHelloWorld
    PASS_REGULAR_EXPRESSION_ALL
      "-- XSDK: Setting default BUILD_SHARED_LIBS=TRUE"
      "USE_XSDK_DEFAULTS=.TRUE."
      "-- XSDK: Setting CMAKE_C_COMPILER from env var CC="
      "-- XSDK: Setting CMAKE_CXX_COMPILER from env var CXX="
      "${TribitsHelloWorld_XSDK_DEFAULTS_Fortran_REGEX}"
      "-- XSDK: Setting default CMAKE_BUILD_TYPE=DEBUG"
      "-- CMAKE_BUILD_TYPE='DEBUG'"
      "-- BUILD_SHARED_LIBS='TRUE'"
      "Generating done"
 
  ENVIRONMENT
    CC=${CMAKE_C_COMPILER}
    CXX=${CMAKE_CXX_COMPILER}
    FC=${CMAKE_Fortran_COMPILER}
  )


tribits_add_advanced_test( TribitsHelloWorld_CONFIGURE_OPTIONS_FILE
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Copy TribitsHelloWorld so that we can copy things into it."
    CMND ${CMAKE_COMMAND}
    ARGS -E copy_directory ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsHelloWorld TribitsHelloWorld

  TEST_1
    MESSAGE "Get the initial configure out of the way"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsHelloWorld_COMMON_CONFIG_ARGS}
      -DTribitsHelloWorld_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      TribitsHelloWorld
    PASS_REGULAR_EXPRESSION_ALL
      "Generating done"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_2
    MESSAGE "Copy ConfigOptions1.cmake to source dir"
    CMND cp
    ARGS ${CMAKE_CURRENT_SOURCE_DIR}/ConfigOptions1.cmake TribitsHelloWorld/

  TEST_3
    MESSAGE "Configure using default FILEPATH pointing to ConfigOptions1.cmake (should fail)"
    CMND ${CMAKE_COMMAND}
    ARGS -DTribitsHelloWorld_CONFIGURE_OPTIONS_FILE=ConfigOptions1.cmake
      .
    PASS_REGULAR_EXPRESSION_ALL
      "(include|INCLUDE) could not find (load|requested) file"
      "TriBITS_TribitsHelloWorld_CONFIGURE_OPTIONS_FILE/ConfigOptions1.cmake"
    # NOTE: Above shows that FILEPATH type causes relative paths to be
    # evaluated w.r.t. the current working directory.

  TEST_4
    MESSAGE "Configure using STRING pointing to ConfigOptions1.cmake (should pass)"
    CMND ${CMAKE_COMMAND}
    ARGS -DTribitsHelloWorld_CONFIGURE_OPTIONS_FILE:STRING=ConfigOptions1.cmake
      .
    PASS_REGULAR_EXPRESSION_ALL
      "Reading in configuration options from ConfigOptions1.cmake"
      "Included ConfigOptions1.cmake"
    ALWAYS_FAIL_ON_NONZERO_RETURN
    # NOTE: Above shows that STRING type causes relative paths to be evaluated
    # w.r.t. the current working directory.

  TEST_5
    MESSAGE "Configure using FILEPATH pointing to ConfigOptions2.cmake (should pass)"
    CMND ${CMAKE_COMMAND}
    ARGS -DTribitsHelloWorld_CONFIGURE_OPTIONS_FILE:FILEPATH=${CMAKE_CURRENT_SOURCE_DIR}/ConfigOptions2.cmake
      .
    PASS_REGULAR_EXPRESSION_ALL
      "Reading in configuration options from .*/test/core/ExamplesUnitTests/ConfigOptions2.cmake"
      "Included ConfigOptions2.cmake"
    ALWAYS_FAIL_ON_NONZERO_RETURN
    # NOTE: Above shows that STRING type causes relative paths to be evaluated
    # w.r.t. the current working directory.

  )


tribits_add_advanced_test( TribitsHelloWorld_Shared_NoVersion
  OVERALL_WORKING_DIRECTORY TEST_NAME
  EXCLUDE_IF_NOT_TRUE IS_REAL_LINUX_SYSTEM
  OVERALL_NUM_MPI_PROCS 1
  TEST_0 CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsHelloWorld_COMMON_CONFIG_ARGS}
      -DBUILD_SHARED_LIBS=ON
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsHelloWorld
    PASS_REGULAR_EXPRESSION_ALL
      "Configuring done"
      "Generating done"
    ALWAYS_FAIL_ON_NONZERO_RETURN
  TEST_1 CMND make
    ARGS ${CTEST_BUILD_FLAGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Built target hello_world_lib"
    ALWAYS_FAIL_ON_NONZERO_RETURN
  TEST_2 CMND ls ARGS hello_world
    PASS_REGULAR_EXPRESSION_ALL
      "libhello_world_lib[.]so"
    FAIL_REGULAR_EXPRESSION
      "libhello_world_lib[.]so[.]SOVERSION"
    ALWAYS_FAIL_ON_NONZERO_RETURN
  )


tribits_add_advanced_test( TribitsHelloWorld_install_perms
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Do initial configure with just libs not tests with default install settings"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsHelloWorld_COMMON_CONFIG_ARGS}
      -DCMAKE_INSTALL_PREFIX=install
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsHelloWorld
    PASS_REGULAR_EXPRESSION_ALL
      "Configuring done"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_1
    MESSAGE "Verify that set_installed_group_and_permissions.cmake is *not* in build dir"
    CMND ls ARGS set_installed_group_and_permissions.cmake
    PASS_REGULAR_EXPRESSION
      "No such file or directory"
    ALWAYS_FAIL_ON_ZERO_RETURN
  # NOTE: We don't want running any extra code if we are just using the stock
  # built-in CMake permissions scheme.  (See trilinos/Trilinos#7881)

  TEST_2
    MESSAGE "Do make to build everything"
    CMND make ARGS ${CTEST_BUILD_FLAGS}
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_3
    MESSAGE "Make install with default directory settings"
    CMND make ARGS ${CTEST_BUILD_FLAGS} install
    PASS_REGULAR_EXPRESSION_ALL
      "Installing: .*/TriBITS_TribitsHelloWorld_install_perms/install/lib/libhello_world_lib.a"
      "Installing: .*/TriBITS_TribitsHelloWorld_install_perms/install/include/hello_world_lib.hpp"
      "Installing: .*/TriBITS_TribitsHelloWorld_install_perms/install/bin/hello_world.exe"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_4
    MESSAGE "Check some default install directory permissions"
    CMND ls ARGS -ld
      install install/include install/lib install/bin
    PASS_REGULAR_EXPRESSION_ALL
      "drwx.* .* install"
      "drwx.* .* install/bin"
      "drwx.* .* install/include"
      "drwx.* .* install/lib"
    ALWAYS_FAIL_ON_NONZERO_RETURN
    # NOTE: Above we can't change the default group or other permissions
    # because that depends on the user's umask when the run these tests.  But
    # the owner should have read/write/execute on the directories or it could
    # not possibly install anything.

  TEST_5
    MESSAGE "Check some default install file permissions"
    CMND ls ARGS -l
      install install/include install/lib install/bin
    PASS_REGULAR_EXPRESSION_ALL
      "[-]rwxr-xr-x.* .* hello_world.exe"
      "[-]rw-r--r--.* .* Makefile.export.HelloWorld"
      "[-]rw-r--r--.* .* .* libhello_world_lib.a"
    ALWAYS_FAIL_ON_NONZERO_RETURN
    # NOTE: The above permissions are the default install permissions of CMake
    # for files that it installs.

  TEST_6
    MESSAGE "Reconfigure with <Project>_MAKE_INSTALL_WORLD_READABLE=ON"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsHelloWorld_COMMON_CONFIG_ARGS}
      -DTribitsHelloWorld_MAKE_INSTALL_WORLD_READABLE=ON
      -DCMAKE_INSTALL_PREFIX=install
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsHelloWorld
    PASS_REGULAR_EXPRESSION_ALL
      "-- TribitsHelloWorld_MAKE_INSTALL_WORLD_READABLE='ON'"
      "-- TribitsHelloWorld_MAKE_INSTALL_GROUP_READABLE=''"
      "-- CMAKE_INSTALL_DEFAULT_DIRECTORY_PERMISSIONS = [(]OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE[)]"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_7
    MESSAGE "Verify that set_installed_group_and_permissions.cmake *is* in build dir"
    CMND ls ARGS set_installed_group_and_permissions.cmake
    PASS_REGULAR_EXPRESSION
      "set_installed_group_and_permissions.cmake"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_8
    MESSAGE "Remove the install directory"
    CMND rm ARGS -r install
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_9
    MESSAGE "Re-install"
    CMND make ARGS ${CTEST_BUILD_FLAGS} install
    PASS_REGULAR_EXPRESSION_ALL
      "Installing: .*/TriBITS_TribitsHelloWorld_install_perms/install/bin/hello_world.exe"
      "0: Running: chmod -R g[+]rX,o[+]rX /.*/TriBITS_TribitsHelloWorld_install_perms/install"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_10
    MESSAGE "Check updated permissions for <Project>_MAKE_INSTALL_WORLD_READABLE=ON"
    CMND ls ARGS -ld
      install install/include install/lib install/bin
    PASS_REGULAR_EXPRESSION_ALL
      "drwxr-xr-x.* .* install"
      "drwxr-xr-x.* .* install/bin"
      "drwxr-xr-x.* .* install/include"
      "drwxr-xr-x.* .* install/lib"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_11
    MESSAGE "Reconfigure with <Project>_MAKE_INSTALL_GROUP_READABLE=ON and <Project>_MAKE_INSTALL_WORLD_READABLE=OFF"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsHelloWorld_COMMON_CONFIG_ARGS}
      -DTribitsHelloWorld_MAKE_INSTALL_GROUP_READABLE=ON
      -DTribitsHelloWorld_MAKE_INSTALL_WORLD_READABLE=OFF
      -DCMAKE_INSTALL_PREFIX=install
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsHelloWorld
    PASS_REGULAR_EXPRESSION_ALL
      "-- TribitsHelloWorld_MAKE_INSTALL_GROUP_READABLE='ON'"
      "-- TribitsHelloWorld_MAKE_INSTALL_WORLD_READABLE='OFF'"
      "-- CMAKE_INSTALL_DEFAULT_DIRECTORY_PERMISSIONS = [(]OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE[)]"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_12
    MESSAGE "Remove the install directory"
    CMND rm ARGS -r install
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_13
    MESSAGE "Re-install"
    CMND make ARGS ${CTEST_BUILD_FLAGS} install
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_14
    MESSAGE "Check updated permissions for <Project>_MAKE_INSTALL_GROUP_READABLE=ON and <Project>_MAKE_INSTALL_WORLD_READABLE=OFF"
    CMND ls ARGS -ld
      install install/include install/lib install/bin
    PASS_REGULAR_EXPRESSION_ALL
      "drwxr-x---.* .* install"
      "drwxr-x---.* .* install/bin"
      "drwxr-x---.* .* install/include"
      "drwxr-x---.* .* install/lib"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_15
    MESSAGE "Reconfigure with <Project>_MAKE_INSTALL_GROUP_READABLE=OFF and <Project>_MAKE_INSTALL_WORLD_READABLE=OFF"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsHelloWorld_COMMON_CONFIG_ARGS}
      -DTribitsHelloWorld_MAKE_INSTALL_GROUP_READABLE=OFF
      -DTribitsHelloWorld_MAKE_INSTALL_WORLD_READABLE=OFF
      -DCMAKE_INSTALL_PREFIX=install
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsHelloWorld
    PASS_REGULAR_EXPRESSION_ALL
      "-- TribitsHelloWorld_MAKE_INSTALL_GROUP_READABLE='OFF'"
      "-- TribitsHelloWorld_MAKE_INSTALL_WORLD_READABLE='OFF'"
      "-- CMAKE_INSTALL_DEFAULT_DIRECTORY_PERMISSIONS = [(]OWNER_READ OWNER_WRITE OWNER_EXECUTE[)]"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_16
    MESSAGE "Remove the install directory"
    CMND rm ARGS -r install
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_17
    MESSAGE "Re-install"
    CMND make ARGS ${CTEST_BUILD_FLAGS} install
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_18
    MESSAGE "Check updated permissions for <Project>_MAKE_INSTALL_GROUP_READABLE=OFF and <Project>_MAKE_INSTALL_WORLD_READABLE=OFF"
    CMND ls ARGS -ld
      install install/include install/lib install/bin
    PASS_REGULAR_EXPRESSION_ALL
      "drwx------.* .* install"
      "drwx------.* .* install/bin"
      "drwx------.* .* install/include"
      "drwx------.* .* install/lib"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  )
  # NOTE: Above we are testing different directory install options.


tribits_add_advanced_test( TribitsHelloWorld_install_package_by_package
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Do initial configure with just libs"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsHelloWorld_COMMON_CONFIG_ARGS}
      -DCMAKE_INSTALL_PREFIX=install
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsHelloWorld
    PASS_REGULAR_EXPRESSION_ALL
      "Configuring done"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_1
    MESSAGE "Do make to build everything"
    CMND make ARGS ${CTEST_BUILD_FLAGS}
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_2
    MESSAGE "Make install_package_by_package without a runner"
    CMND make ARGS ${CTEST_BUILD_FLAGS} install_package_by_package
    PASS_REGULAR_EXPRESSION_ALL
      "Installing: .*/TriBITS_TribitsHelloWorld_install_package_by_package/install/lib/libhello_world_lib[.]a"
      "Installing: .*/TriBITS_TribitsHelloWorld_install_package_by_package/install/include/hello_world_lib[.]hpp"
      "Installing: .*/TriBITS_TribitsHelloWorld_install_package_by_package/install/bin/hello_world[.]exe"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_3
    MESSAGE "Check for some installed files"
    CMND ls ARGS
      install/include/hello_world_lib.hpp
      install/lib/libhello_world_lib.a
      install/bin/hello_world.exe
    PASS_REGULAR_EXPRESSION_ALL
      "install/include/hello_world_lib[.]hpp"
      "install/lib/libhello_world_lib[.]a"
      "install/bin/hello_world[.]exe"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  )
  # NOTE: Above we are testing the 'install_package_by_package' target and
  # without using an install runner.


tribits_add_advanced_test( TribitsHelloWorld_install_package_by_package_with_runner
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Do initial configure with an install_package_by_package runner"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsHelloWorld_COMMON_CONFIG_ARGS}
      -DTribitsHelloWorld_INSTALL_PBP_RUNNER=${CMAKE_CURRENT_SOURCE_DIR}/run-program.sh
      -DCMAKE_INSTALL_PREFIX=install
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsHelloWorld
    PASS_REGULAR_EXPRESSION_ALL
      "Configuring done"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_1
    MESSAGE "Do make to build everything"
    CMND make ARGS ${CTEST_BUILD_FLAGS}
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_2
    MESSAGE "Make install_package_by_package with a runner"
    CMND make ARGS ${CTEST_BUILD_FLAGS} install_package_by_package
    PASS_REGULAR_EXPRESSION_ALL
      "Running: .*/cmake.* -P cmake_pbp_install[.]cmake"
      "Installing: .*/TriBITS_TribitsHelloWorld_install_package_by_package_with_runner/install/lib/libhello_world_lib[.]a"
      "Installing: .*/TriBITS_TribitsHelloWorld_install_package_by_package_with_runner/install/include/hello_world_lib[.]hpp"
      "Installing: .*/TriBITS_TribitsHelloWorld_install_package_by_package_with_runner/install/bin/hello_world[.]exe"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_3
    MESSAGE "Check for some installed files"
    CMND ls ARGS
      install/include/hello_world_lib.hpp
      install/lib/libhello_world_lib.a
      install/bin/hello_world.exe
    PASS_REGULAR_EXPRESSION_ALL
      "install/include/hello_world_lib[.]hpp"
      "install/lib/libhello_world_lib[.]a"
      "install/bin/hello_world[.]exe"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  )
  # NOTE: Above we are testing the 'install_package_by_package' with an
  # install runner for that target set with <Project>_INSTALL_PBP_RUNNER.


tribits_add_advanced_test( TribitsHelloWorld_install_perms_windows_error
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Cconfigure with <Project>_MAKE_INSTALL_WORLD_READABLE=ON and Windows"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsHelloWorld_COMMON_CONFIG_ARGS}
      -DTribitsHelloWorld_MAKE_INSTALL_GROUP_WRITABLE=on
      -DTribitsHelloWorld_MAKE_INSTALL_GROUP_READABLE=true
      -DTribitsHelloWorld_MAKE_INSTALL_WORLD_READABLE=TRUE
      -DTribitsHelloWorld_MAKE_INSTALL_GROUP=dummy-group
      -DTribitsHelloWorld_HOSTTYPE=Windows
      -DCMAKE_INSTALL_PREFIX=install
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsHelloWorld
    PASS_REGULAR_EXPRESSION_ALL
      "ERROR: The options"
      "    TribitsHelloWorld_MAKE_INSTALL_GROUP_WRITABLE='on'"
      "    TribitsHelloWorld_MAKE_INSTALL_GROUP_READABLE='true'"
      "    TribitsHelloWorld_MAKE_INSTALL_WORLD_READABLE='TRUE'"
      "    TribitsHelloWorld_MAKE_INSTALL_GROUP='dummy-group'"
      "are not supported on Windows!"
      "Please remove these options and configure from scratch!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  )


tribits_add_advanced_test( TribitsHelloWorld_install_config_dummy_proj
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Do initial configure with just libs"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsHelloWorld_COMMON_CONFIG_ARGS}
      -DCMAKE_INSTALL_PREFIX=install
      -DMPI_EXEC=mympiexec
      -DMPI_EXEC_PRE_NUMPROCS_FLAGS="--pre-flags"    # Can't use ';'
      -DMPI_EXEC_NUMPROCS_FLAG="-mynp"
      -DMPI_EXEC_POST_NUMPROCS_FLAGS="--post-flags"  # Can't use ';'
      -DTribitsHelloWorld_ENABLE_INSTALL_CMAKE_CONFIG_FILES=ON
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsHelloWorld
    PASS_REGULAR_EXPRESSION_ALL
      "Configuring done"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_1
    MESSAGE "Do make install to build and everything"
    CMND make ARGS ${CTEST_BUILD_FLAGS} install
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_2
    MESSAGE "Create and configure a dummy project that includes"
      " TribitsHelloWorkdConfig.cmake from the install tree"
    CMND ${CMAKE_COMMAND}
    ARGS
      -DDUMMY_PROJECT_NAME=DummyProject
      -DDUMMY_PROJECT_DIR=dummy_client_of_TribitsHelloWorld
      -DEXPORT_VAR_PREFIX=TribitsHelloWorld
      -DEXPORT_CONFIG_FILE=../install/lib/cmake/TribitsHelloWorld/TribitsHelloWorldConfig.cmake
      -DCMAKE_COMMAND=${CMAKE_COMMAND}
      -P ${CMAKE_CURRENT_SOURCE_DIR}/RunDummyPackageClientBulid.cmake
    PASS_REGULAR_EXPRESSION_ALL
      "DUMMY_PROJECT_NAME = 'DummyProject'"
      "DUMMY_PROJECT_DIR = 'dummy_client_of_TribitsHelloWorld'"
      "EXPORT_CONFIG_FILE = '../install/lib/cmake/TribitsHelloWorld/TribitsHelloWorldConfig.cmake'"
      "EXPORT_VAR_PREFIX = 'TribitsHelloWorld'"
      "Configure the dummy project to print the variables in .*/TriBITS_TribitsHelloWorld_install_config_dummy_proj/dummy_client_of_TribitsHelloWorld ..."
      "DUMMY_PROJECT_NAME = 'DummyProject'"
      "EXPORT_CONFIG_FILE = '../install/lib/cmake/TribitsHelloWorld/TribitsHelloWorldConfig.cmake'"
      "EXPORT_VAR_PREFIX = 'TribitsHelloWorld'"
      "TribitsHelloWorld_CMAKE_BUILD_TYPE = 'RELEASE'"
      "TribitsHelloWorld_CXX_COMPILER = '${CMAKE_CXX_COMPILER_FOR_REGEX}'"
      "TribitsHelloWorld_C_COMPILER = '${CMAKE_C_COMPILER_FOR_REGEX}'"
      "TribitsHelloWorld_Fortran_COMPILER = ''"
      "TribitsHelloWorld_FORTRAN_COMPILER = ''"
      "TribitsHelloWorld_CXX_FLAGS = ''"
      "TribitsHelloWorld_C_FLAGS = ''"
      "TribitsHelloWorld_Fortran_FLAGS = ''"
      "TribitsHelloWorld_FORTRAN_FLAGS = ''"
      "TribitsHelloWorld_EXTRA_LD_FLAGS = ''"
      "TribitsHelloWorld_SHARED_LIB_RPATH_COMMAND = ''"
      "TribitsHelloWorld_BUILD_SHARED_LIBS = 'FALSE'"
      "TribitsHelloWorld_LINKER = '.*'"
      "TribitsHelloWorld_AR = '.*'"
      "TribitsHelloWorld_INSTALL_DIR = '.*/TriBITS_TribitsHelloWorld_install_config_dummy_proj/install'"
      "TribitsHelloWorld_INCLUDE_DIRS = '.*/TriBITS_TribitsHelloWorld_install_config_dummy_proj/install/include'"
      "TribitsHelloWorld_LIBRARY_DIRS = '.*/TriBITS_TribitsHelloWorld_install_config_dummy_proj/install/lib'"
      "TribitsHelloWorld_LIBRARIES = 'hello_world_lib'"
      "TribitsHelloWorld_TPL_INCLUDE_DIRS = '"
      "TribitsHelloWorld_TPL_LIBRARY_DIRS = ''"
      "TribitsHelloWorld_TPL_LIBRARIES = ''"
      "TribitsHelloWorld_MPI_LIBRARIES = ''"
      "TribitsHelloWorld_MPI_LIBRARY_DIRS = ''"
      "TribitsHelloWorld_MPI_INCLUDE_DIRS = ''"
      "TribitsHelloWorld_MPI_EXEC = 'mympiexec"
      "TribitsHelloWorld_MPI_EXEC_MAX_NUMPROCS = '[1-9]*'"  # Is null for an MPI build
      "TribitsHelloWorld_MPI_EXEC_PRE_NUMPROCS_FLAGS = '--pre-flags'"
      "TribitsHelloWorld_MPI_EXEC_NUMPROCS_FLAG = '-mynp"
      "TribitsHelloWorld_MPI_EXEC_POST_NUMPROCS_FLAGS = '--post-flags'"
      "TribitsHelloWorld_PACKAGE_LIST = 'HelloWorld'"
      "TribitsHelloWorld_TPL_LIST = ''"  # Must work for no MPI too
      "-- Configuring done"
      "-- Generating done"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  )
  # NOTE: Above we are testing:
  #
  # * 'install' target builds and installs by default
  #
  # * The <Project>Config.cmake file works if there are no TPLs enabled
  #   (defect trilinos/trilinos#5213)
  #


# NOTE: In the below tests, we are only testing TriBITS support for generating
# the ctest_resources.json file, setting the RESOURCES_GROUP and ENVIRONMENT
# test properties, and testing CMake support for recognizing the
# RESOURCES_GROUP test property and putting it in the CTestTestfile.cmake
# file.  We are not actually running ctest or looking for the var
# CTEST_RESOURCE_SPEC_FILE set in the CTestTestfile.cmake file.  (Support for
# CTEST_RESOURCE_SPEC_FILE was not added proper until 3.18 so we can't rely on
# it in these tests that work with CMake 3.17.)


tribits_add_advanced_test( TribitsHelloWorld_ctest_resources_file_autogen_2_3
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Configure and generate the ctest_resources.json file"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsHelloWorld_COMMON_CONFIG_ARGS}
      -DTribitsHelloWorld_ENABLE_TESTS=ON
      -DTribitsHelloWorld_AUTOGENERATE_TEST_RESOURCE_FILE=ON
      -DTribitsHelloWorld_CUDA_NUM_GPUS=2
      -DTribitsHelloWorld_CUDA_SLOTS_PER_GPU=3
      -DTPL_ENABLE_CUDA=ON
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsHelloWorld
    PASS_REGULAR_EXPRESSION_ALL
      "Configuring done"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_1
    MESSAGE "Determine that ctest_resources.json was generated correctly"
    CMND diff
    ARGS ctest_resources.json
      "${CMAKE_CURRENT_SOURCE_DIR}/ctest_resources/ctest_resources.autogen_2_3_.json"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_2
    MESSAGE "Check that the CTestTestfile.cmake file has the right entries"
    CMND cat
    ARGS hello_world/CTestTestfile.cmake
    PASS_REGULAR_EXPRESSION_ALL
      "ENVIRONMENT .CTEST_KOKKOS_DEVICE_TYPE=gpus."
      "PROCESSORS .1."
      "RESOURCE_GROUPS .1,gpus:1."
    ALWAYS_FAIL_ON_NONZERO_RETURN

  )
  # NOTE: The above test ensures that the ctest_resources.json file gets
  # auto-generated correctly and ensures that the RESOURCE_GROUPS test
  # property gets set correctly in a CUDA build of a project.  (What is
  # interesting about the above case is that bare bones TriBITS does not
  # really do anything special when setting TPL_ENABLE_CUDA=ON.  All of the
  # special logic for CUDA is handled in Kokkos and Trilinos with the usage of
  # nvcc_wrapper.)


tribits_add_advanced_test( TribitsHelloWorld_no_ctest_resources_file
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Configure without any ctest resources file, just enable CUDA"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsHelloWorld_COMMON_CONFIG_ARGS}
      -DTribitsHelloWorld_ENABLE_TESTS=ON
      -DTPL_ENABLE_CUDA=ON
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsHelloWorld
    PASS_REGULAR_EXPRESSION_ALL
      "Configuring done"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_1
    MESSAGE "Check that the CTestTestfile.cmake file has the right entries"
    CMND cat
    ARGS hello_world/CTestTestfile.cmake
    PASS_REGULAR_EXPRESSION_ALL
      "ENVIRONMENT .CTEST_KOKKOS_DEVICE_TYPE=gpus."
      "PROCESSORS .1."
      "RESOURCE_GROUPS .1,gpus:1."
    ALWAYS_FAIL_ON_NONZERO_RETURN

  )
  # NOTE: The above test ensures that the RESOURCE_GROUPS test property gets
  # set correctly in a CUDA build of a project, regardless if a ctest
  # resources file gets set or not.  (The user can always explicitly pass in a
  # ctest resources file later directly to ctest.)


tribits_add_advanced_test( TribitsHelloWorld_set_other_ctest_resources_file_autogen_on
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Copy in pre-created ctest resource file to make sure it is not overwritten"
    CMND cp
    ARGS "${CMAKE_CURRENT_SOURCE_DIR}/ctest_resources/other_ctest_resources.json" .

  TEST_1
    MESSAGE "Configure pointing to non-default ctest resource file with autogenerate turned on "
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsHelloWorld_COMMON_CONFIG_ARGS}
      -DTribitsHelloWorld_ENABLE_TESTS=ON
      -DTribitsHelloWorld_AUTOGENERATE_TEST_RESOURCE_FILE=ON
      -DTribitsHelloWorld_CUDA_NUM_GPUS=2        # Will not get used!
      -DTribitsHelloWorld_CUDA_SLOTS_PER_GPU=3   # Will not get used!
      -DTPL_ENABLE_CUDA=ON
      -DCTEST_RESOURCE_SPEC_FILE=other_ctest_resources.json
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsHelloWorld
    PASS_REGULAR_EXPRESSION_ALL
      "NOTE: The test resource file CTEST_RESOURCE_SPEC_FILE='.*/TriBITS_TribitsHelloWorld_set_other_ctest_resources_file_autogen_on/other_ctest_resources[.]json' will not be auto-generated even through TribitsHelloWorld_AUTOGENERATE_TEST_RESOURCE_FILE=ON because its location does not match the default location '.*/TriBITS_TribitsHelloWorld_set_other_ctest_resources_file_autogen_on/ctest_resources[.]json'[.]  If you want to auto-generate this file, please clear CTEST_RESOURCE_SPEC_FILE and reconfigure or create that file on your own and clear TribitsHelloWorld_AUTOGENERATE_TEST_RESOURCE_FILE[.]"
      "Configuring done"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_2
    MESSAGE "Check that the pre-existing other_ctest_resources.json file was not overwritten"
    CMND diff
    ARGS "${CMAKE_CURRENT_SOURCE_DIR}/ctest_resources/other_ctest_resources.json"
      other_ctest_resources.json

  TEST_3
    MESSAGE "Check that default ctest_resources.json file is not generated"
    CMND ls
    ARGS ctest_resources.json
    WILL_FAIL

  )
  # NOTE: The above test ensures that when CTEST_RESOURCE_SPEC_FILE is set to
  # the non-default location then the autogenerate feature will not overwrite
  # the file and will not generate the default ctest_resources.json file.


tribits_add_advanced_test( TribitsHelloWorld_set_default_ctest_resources_file_autogen_on
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Copy in pre-created ctest resource file into the default autogen name and location"
    CMND cp
    ARGS "${CMAKE_CURRENT_SOURCE_DIR}/ctest_resources/other_ctest_resources.json"
      ctest_resources.json

  TEST_1
    MESSAGE "Configure pointing to default ctest resource file with autogenerate turned on"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsHelloWorld_COMMON_CONFIG_ARGS}
      -DTribitsHelloWorld_ENABLE_TESTS=ON
      -DTribitsHelloWorld_AUTOGENERATE_TEST_RESOURCE_FILE=ON
      -DTribitsHelloWorld_CUDA_NUM_GPUS=2
      -DTribitsHelloWorld_CUDA_SLOTS_PER_GPU=3
      -DTPL_ENABLE_CUDA=ON
      -DCTEST_RESOURCE_SPEC_FILE=ctest_resources.json
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsHelloWorld
    PASS_REGULAR_EXPRESSION_ALL
      "Configuring done"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_2
    MESSAGE "Check that the pre-existing ctest_resources.json file **was** overwritten"
    CMND diff
    ARGS "${CMAKE_CURRENT_SOURCE_DIR}/ctest_resources/ctest_resources.autogen_2_3_.json"
      ctest_resources.json

  )
  # NOTE: The above test shows that if the user happens to provide a ctest
  # resources file of the same name and the same location as the default
  # generated file, then TriBITS will actually overwrite it if the
  # autogenerate option is enabled!


tribits_add_advanced_test( TribitsHelloWorld_set_default_ctest_resources_file_autogen_off
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Copy in pre-created ctest resource file into the default autogen name and location"
    CMND cp
    ARGS "${CMAKE_CURRENT_SOURCE_DIR}/ctest_resources/other_ctest_resources.json"
      ctest_resources.json

  TEST_1
    MESSAGE "Configure pointing to default ctest resource file with autogenerate turned off"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsHelloWorld_COMMON_CONFIG_ARGS}
      -DTribitsHelloWorld_ENABLE_TESTS=ON
      -DTribitsHelloWorld_CUDA_NUM_GPUS=2
      -DTribitsHelloWorld_CUDA_SLOTS_PER_GPU=3
      -DTPL_ENABLE_CUDA=ON
      -DCTEST_RESOURCE_SPEC_FILE=ctest_resources.json
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsHelloWorld
    PASS_REGULAR_EXPRESSION_ALL
      "Configuring done"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_2
    MESSAGE "Check that the pre-existing ctest_resources.json file was **not** overwritten"
    CMND diff
    ARGS "${CMAKE_CURRENT_SOURCE_DIR}/ctest_resources/other_ctest_resources.json"
      ctest_resources.json

  )
  # NOTE: The above test shows that if the user happens to provide a ctest
  # resources file of the same name and the same location as the default
  # generated file, then TriBITS will not overwrite that file if the
  # autgenerate option is disabled.


########################################################################
# RawAndTribitsHelloWorld
########################################################################


tribits_add_advanced_test( RawAndTribitsHelloWorld_Raw
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  TEST_0 CMND ${CMAKE_COMMAND}
    ARGS
      ${SERIAL_PASSTHROUGH_CONFIGURE_ARGS}
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/RawAndTribitsHelloWorld
    PASS_REGULAR_EXPRESSION_ALL
      "Configuring done"
      "Generating done"
      "Build files have been written to: .*ExamplesUnitTests/TriBITS_RawAndTribitsHelloWorld"
  TEST_1 CMND make
    ARGS ${CTEST_BUILD_FLAGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Built target hello_world_lib"
      "Built target hello_world"
      "Built target unit_tests"
  TEST_2 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    PASS_REGULAR_EXPRESSION_ALL
      ": test .*  Passed"
      ": unit_test .*  Passed"
      "100% tests passed, 0 tests failed out of 2"
  )


tribits_add_advanced_test( RawAndTribitsHelloWorld_Tribits
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  TEST_0 CMND ${CMAKE_COMMAND}
    ARGS
      -DRawAndTribitsHelloWorld_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      ${SERIAL_PASSTHROUGH_CONFIGURE_ARGS}
      ${RawAndTribitsHelloWorld_COMMON_CONFIG_ARGS}
      -DRawAndTribitsHelloWorld_ENABLE_TESTS=ON
      -DHelloWorld_ENABLE_CPACK_PACKAGING=ON
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/RawAndTribitsHelloWorld
    PASS_REGULAR_EXPRESSION_ALL
      "Configuring done"
      "Generating done"
      "Build files have been written to: .*ExamplesUnitTests/TriBITS_RawAndTribitsHelloWorld"
    FAIL_REGULAR_EXPRESSION
      "Check for working Fortran compiler" # Should not be looking for Fortran!
  TEST_1 CMND make
    ARGS ${CTEST_BUILD_FLAGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Built target hello_world_lib"
      "Built target hello_world"
      "Built target HelloWorld_unit_tests"
  TEST_2 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    PASS_REGULAR_EXPRESSION_ALL
      ": HelloWorld_hello_world .*  Passed"
      ": HelloWorld_unit_tests .*  Passed"
      "100% tests passed, 0 tests failed out of 2"
  )


########################################################################
# TribitsExampleProject
########################################################################


set(TribitsExampleProject_COMMON_CONFIG_ARGS
  ${COMMON_ENV_ARGS_PASSTHROUGH}
  -DTribitsExProj_ENABLE_Fortran=${${PROJECT_NAME}_ENABLE_Fortran}
  )


assert_defined(TPL_ENABLE_MPI)
if (TPL_ENABLE_MPI)
  set(TPL_MPI_FILE_TRACE
    "-- File Trace: TPL        INCLUDE    .*/core/std_tpls/FindTPLMPI.cmake")
  set(FINAL_ENABLED_TPLS "MPI HeaderOnlyTpl 2")
else()
  set(TPL_MPI_FILE_TRACE "")
  set(FINAL_ENABLED_TPLS "HeaderOnlyTpl 1")
endif()


if (EXISTS "${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject/.gitignore")
  set(REGEX_FOR_GITIGNORE "Only in .*/TribitsExampleProject: .gitignore")
else()
  set(REGEX_FOR_GITIGNORE)
endif()


if (CMAKE_CXX_COMPILER_VERSION VERSION_LESS 5.0)
  set(DEPRECATED_WARNING_1_STR
    "‘int SimpleCxx::HelloWorld::someOldFunc.. const’ is deprecated .declared at .*/TribitsExampleProject/packages/simple_cxx/src/SimpleCxx_HelloWorld.hpp:"
    )
  if (NOT CMAKE_CXX_COMPILER_VERSION VERSION_LESS 4.5)
    # Only versions 4.5+ support this feature
    set(DEPRECATED_MSG_STR ".* .Just don't call this function at all please!")
  else()
    set(DEPRECATED_MSG_STR)
  endif()
  set(DEPRECATED_WARNING_2_STR
    "‘int SimpleCxx::HelloWorld::someOldFunc2.. const’ is deprecated .declared at .*/TribitsExampleProject/packages/simple_cxx/src/SimpleCxx_HelloWorld.hpp:${DEPRECATED_MSG_STR}"
    )
else()
  set(DEPRECATED_WARNING_1_STR
    ".*/TribitsExampleProject/packages/simple_cxx/src/SimpleCxx_HelloWorld.cpp:.*: warning: .*int SimpleCxx::HelloWorld::someOldFunc.. const.* is deprecated"
    )
  set(DEPRECATED_WARNING_2_STR
    ".*/TribitsExampleProject/packages/simple_cxx/src/SimpleCxx_HelloWorld.cpp:.*: warning: .*int SimpleCxx::HelloWorld::someOldFunc2.. const.* is deprecated: .Just don.t call this function at all please."
    )
endif()


set(LabelsForSubprojects_CMND_AND_ARGS
  grep ARGS "^LabelsForSubprojects:" DartConfiguration.tcl)
set(LabelsForSubprojects_REGEX
  "LabelsForSubprojects: SimpleCxx[;]MixedLang[;]WithSubpackages[;]WrapExternal")


tribits_add_advanced_test( TribitsExampleProject_ALL_ST_NoFortran
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  XHOSTTYPE Darwin

  TEST_0
    MESSAGE "Do the initial configure (and test a lot of things at once)"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_ENABLE_ALL_PACKAGES=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      -DTribitsExProj_ENABLE_SECONDARY_TESTED_CODE=ON
      -DTribitsExProj_TRACE_FILE_PROCESSING=ON
      -DTribitsExProj_ENABLE_CPACK_PACKAGING=ON
      -DTribitsExProj_DUMP_CPACK_SOURCE_IGNORE_FILES=ON
      -DTribitsExProj_DUMP_PACKAGE_DEPENDENCIES=ON
      -DTribitsExProj_ENABLE_EXPORT_MAKEFILES=ON
      -DTribitsExProj_ENABLE_INSTALL_CMAKE_CONFIG_FILES=ON
      -DCMAKE_CXX_FLAGS=-DSIMPLECXX_SHOW_DEPRECATED_WARNINGS=1
      -DCMAKE_INSTALL_PREFIX=install
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Configuring TribitsExProj build directory"
      "-- PROJECT_SOURCE_DIR="
      "-- PROJECT_BINARY_DIR="
      "-- TribitsExProj_TRIBITS_DIR="
      "-- TriBITS_VERSION_STRING="
      "-- CMAKE_VERSION="
      "-- CMAKE_HOST_SYSTEM_NAME="
      "-- TribitsExProj_HOSTNAME="

      "NOTE: Setting TribitsExProj_ENABLE_WrapExternal=OFF because TribitsExProj_ENABLE_EXPORT_MAKEFILES"
      "NOTE: Setting TribitsExProj_ENABLE_MixedLang=OFF because TribitsExProj_ENABLE_Fortran"
      "Printing package dependencies ..."
      "-- TribitsExProj_PACKAGES: SimpleCxx MixedLang WithSubpackages WrapExternal"
      "-- TribitsExProj_SE_PACKAGES: SimpleCxx MixedLang WithSubpackagesA WithSubpackagesB WithSubpackagesC WithSubpackages WrapExternal"

      "-- SimpleCxx_LIB_REQUIRED_DEP_TPLS: HeaderOnlyTpl"
      "-- MixedLang: No dependencies!"
      "-- WithSubpackagesA_LIB_REQUIRED_DEP_PACKAGES: SimpleCxx"
      "-- WithSubpackagesB_LIB_REQUIRED_DEP_PACKAGES: SimpleCxx"
      "-- WithSubpackagesB_LIB_OPTIONAL_DEP_PACKAGES: WithSubpackagesA"
      "-- WithSubpackagesB_TEST_OPTIONAL_DEP_PACKAGES: MixedLang"
      "-- WithSubpackagesC_LIB_REQUIRED_DEP_PACKAGES: WithSubpackagesA WithSubpackagesB"
      "-- WithSubpackages_LIB_REQUIRED_DEP_PACKAGES: WithSubpackagesA"
      "-- WithSubpackages_LIB_OPTIONAL_DEP_PACKAGES: WithSubpackagesB WithSubpackagesC"
      "-- WrapExternal_LIB_REQUIRED_DEP_PACKAGES: WithSubpackagesA"
      "-- WrapExternal_LIB_OPTIONAL_DEP_PACKAGES: MixedLang"
      "-- SimpleCxx: No library dependencies!"
      "-- WithSubpackagesA_FULL_ENABLED_DEP_PACKAGES: SimpleCxx"
      "-- WithSubpackagesB_FULL_ENABLED_DEP_PACKAGES: WithSubpackagesA SimpleCxx"
      "-- WithSubpackagesC_FULL_ENABLED_DEP_PACKAGES: WithSubpackagesB WithSubpackagesA SimpleCxx"
      "-- WithSubpackages_FULL_ENABLED_DEP_PACKAGES: WithSubpackagesC WithSubpackagesB WithSubpackagesA SimpleCxx"
      "Explicitly enabled packages on input .by user.:  0"
      "Explicitly disabled packages on input .by user or by default.:  MixedLang WrapExternal 2"
      "Enabling all SE packages that are not currently disabled because of TribitsExProj_ENABLE_ALL_PACKAGES=ON "
      "Setting TribitsExProj_ENABLE_SimpleCxx=ON"
      "Setting TribitsExProj_ENABLE_WithSubpackages=ON"
      "Setting TPL_ENABLE_HeaderOnlyTpl=ON because it is required by the enabled package SimpleCxx"
      "Final set of enabled packages:  SimpleCxx WithSubpackages 2"
      "Final set of enabled SE packages:  SimpleCxx WithSubpackagesA WithSubpackagesB WithSubpackagesC WithSubpackages 5"
      "Final set of enabled TPLs:  ${FINAL_ENABLED_TPLS}"
      "Final set of non-enabled packages:  MixedLang WrapExternal 2"
      "Processing enabled TPL: HeaderOnlyTpl"
      "-- File Trace: TPL        INCLUDE    .+/TribitsExampleProject/cmake/tpls/FindTPLHeaderOnlyTpl.cmake"
      "-- TPL_HeaderOnlyTpl_INCLUDE_DIRS='.+/examples/tpls/HeaderOnlyTpl'"
      "Performing Test HAVE_SIMPLECXX___INT64"
      "Configuring done"
      "Generating done"
      "Build files have been written to: .*ExamplesUnitTests/TriBITS_TribitsExampleProject_ALL_ST_NoFortran"
      "-- File Trace: PROJECT    INCLUDE    .*/TribitsExampleProject/Version.cmake"
      "-- File Trace: REPOSITORY INCLUDE    .*/TribitsExampleProject/cmake/CallbackSetupExtraOptions.cmake"
      "-- File Trace: REPOSITORY INCLUDE    .*/TribitsExampleProject/PackagesList.cmake"
      "-- File Trace: REPOSITORY INCLUDE    .*/TribitsExampleProject/TPLsList.cmake"
      "-- File Trace: PACKAGE    INCLUDE    .*/TribitsExampleProject/packages/simple_cxx/cmake/Dependencies.cmake"
      "-- File Trace: PACKAGE    INCLUDE    .*/TribitsExampleProject/packages/mixed_lang/cmake/Dependencies.cmake"
      "-- File Trace: PACKAGE    INCLUDE    .*/TribitsExampleProject/packages/with_subpackages/cmake/Dependencies.cmake"
      "-- File Trace: PACKAGE    INCLUDE    .*/TribitsExampleProject/packages/with_subpackages/a/cmake/Dependencies.cmake"
      "-- File Trace: PACKAGE    INCLUDE    .*/TribitsExampleProject/packages/with_subpackages/b/cmake/Dependencies.cmake"
      "-- File Trace: PACKAGE    INCLUDE    .*/TribitsExampleProject/packages/with_subpackages/c/cmake/Dependencies.cmake"
      "-- File Trace: PACKAGE    INCLUDE    .*/TribitsExampleProject/packages/wrap_external/cmake/Dependencies.cmake"
      "-- File Trace: PROJECT    CONFIGURE  .*/TribitsExampleProject/cmake/ctest/CTestCustom.cmake.in"
      "-- File Trace: REPOSITORY READ       .*/TribitsExampleProject/Copyright.txt"
      "-- File Trace: REPOSITORY INCLUDE    .*/TribitsExampleProject/Version.cmake"
      "${TPL_MPI_FILE_TRACE}"
      "-- File Trace: PACKAGE    ADD_SUBDIR .*/TribitsExampleProject/packages/simple_cxx/CMakeLists.txt"
      "-- File Trace: PACKAGE    ADD_SUBDIR .*/TribitsExampleProject/packages/simple_cxx/test/CMakeLists.txt"
      "-- File Trace: PACKAGE    ADD_SUBDIR .*/TribitsExampleProject/packages/with_subpackages/CMakeLists.txt"
      "-- File Trace: PACKAGE    ADD_SUBDIR .*/TribitsExampleProject/packages/with_subpackages/a/CMakeLists.txt"
      "-- File Trace: PACKAGE    ADD_SUBDIR .*/TribitsExampleProject/packages/with_subpackages/a/tests/CMakeLists.txt"
      "-- File Trace: PACKAGE    ADD_SUBDIR .*/TribitsExampleProject/packages/with_subpackages/b/CMakeLists.txt"
      "-- File Trace: PACKAGE    ADD_SUBDIR .*/TribitsExampleProject/packages/with_subpackages/b/tests/CMakeLists.txt"
      "-- File Trace: PACKAGE    ADD_SUBDIR .*/TribitsExampleProject/packages/with_subpackages/c/CMakeLists.txt"
      "-- File Trace: PACKAGE    ADD_SUBDIR .*/TribitsExampleProject/packages/with_subpackages/c/tests/CMakeLists.txt"
      "-- File Trace: REPOSITORY INCLUDE    .*/TribitsExampleProject/cmake/CallbackDefineRepositoryPackaging.cmake"
      "-- File Trace: PROJECT    INCLUDE    .*/TribitsExampleProject/cmake/CallbackDefineProjectPackaging.cmake"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_1
    MESSAGE "Make sure that 'LabelsForSubprojects' is set to list of packages"
    CMND ${LabelsForSubprojects_CMND_AND_ARGS}
    PASS_REGULAR_EXPRESSION "${LabelsForSubprojects_REGEX}"

  TEST_2
    MESSAGE "Build the default 'all' target using raw 'make'"
    CMND make ARGS ${CTEST_BUILD_FLAGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Built target simplecxx"
      "${DEPRECATED_WARNING_1_STR}"
      "${DEPRECATED_WARNING_2_STR}"
      "Built target pws_a"
      "Built target pws_b"
      "Built target pws_c"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_3
    MESSAGE "Run all the tests with raw 'ctest'"
    CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    PASS_REGULAR_EXPRESSION_ALL
      "SimpleCxx_HelloWorldTests${TEST_MPI_1_SUFFIX} .* Passed"
      "WithSubpackagesA_test_of_a .* Passed"
      "WithSubpackagesB_test_of_b .* Passed"
      "WithSubpackagesC_test_of_c .* Passed"
      "WithSubpackagesC_test_of_c_util.* Passed"
      "100% tests passed, 0 tests failed out of 6"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_4
    MESSAGE "Create and configure a dummy project that includes"
      " WithSubpackagesConfig.cmake from the build tree"
    CMND ${CMAKE_COMMAND}
    ARGS
      -DDUMMY_PROJECT_NAME=DummyProject
      -DDUMMY_PROJECT_DIR=dummy_client_of_build_WithSubpackages
      -DEXPORT_VAR_PREFIX=WithSubpackages
      -DEXPORT_CONFIG_FILE=../packages/with_subpackages/WithSubpackagesConfig.cmake
      -DCMAKE_COMMAND=${CMAKE_COMMAND}
      -P ${CMAKE_CURRENT_SOURCE_DIR}/RunDummyPackageClientBulid.cmake
    PASS_REGULAR_EXPRESSION_ALL
      "WithSubpackages_CMAKE_BUILD_TYPE = 'RELEASE'"
      "WithSubpackages_CXX_COMPILER = '${CMAKE_CXX_COMPILER_FOR_REGEX}'"
      "WithSubpackages_C_COMPILER = '${CMAKE_C_COMPILER_FOR_REGEX}'"
      "WithSubpackages_Fortran_COMPILER = ''"
      "WithSubpackages_FORTRAN_COMPILER = ''"
      "WithSubpackages_CXX_FLAGS = '.*'"
      "WithSubpackages_C_FLAGS = '.*'"
      "WithSubpackages_Fortran_FLAGS = '.*'"
      "WithSubpackages_EXTRA_LD_FLAGS = '.*'"
      "WithSubpackages_SHARED_LIB_RPATH_COMMAND = '.*'"
      "WithSubpackages_BUILD_SHARED_LIBS = '.*'"
      "WithSubpackages_LINKER = '.+'"
      "WithSubpackages_AR = '.+'"
      "WithSubpackages_INSTALL_DIR = .*/TriBITS_TribitsExampleProject_ALL_ST_NoFortran/install"
      "WithSubpackages_INCLUDE_DIRS = .+/TriBITS_TribitsExampleProject_ALL_ST_NoFortran;.+/TriBITS_TribitsExampleProject_ALL_ST_NoFortran/packages/with_subpackages/b/src;.+/TribitsExampleProject/packages/with_subpackages/b/src;.+/TribitsExampleProject/packages/with_subpackages/a;.+/TriBITS_TribitsExampleProject_ALL_ST_NoFortran/packages/simple_cxx/src;.+/TribitsExampleProject/packages/simple_cxx/src;.+/tpls/HeaderOnlyTpl;.+/TribitsExampleProject/packages/with_subpackages/c"
      "WithSubpackages_LIBRARY_DIRS = '.+/TriBITS_TribitsExampleProject_ALL_ST_NoFortran/packages/with_subpackages/b/src;.+/TriBITS_TribitsExampleProject_ALL_ST_NoFortran/packages/with_subpackages/a;.+/TriBITS_TribitsExampleProject_ALL_ST_NoFortran/packages/simple_cxx/src;.+/TriBITS_TribitsExampleProject_ALL_ST_NoFortran/packages/with_subpackages/c'"
      "WithSubpackages_LIBRARIES = 'pws_c.pws_b.pws_a.simplecxx'"
      "WithSubpackages_TPL_INCLUDE_DIRS = '.+/tribits/examples/tpls/HeaderOnlyTpl'"
      "WithSubpackages_TPL_LIBRARY_DIRS = ''"
      "WithSubpackages_TPL_LIBRARIES = ''"
      "WithSubpackages_MPI_LIBRARIES = ''"
      "WithSubpackages_MPI_LIBRARY_DIRS = ''"
      "WithSubpackages_MPI_INCLUDE_DIRS = ''"
      "WithSubpackages_MPI_EXEC = '${MPI_EXEC}'"
      "WithSubpackages_MPI_EXEC_MAX_NUMPROCS = '${MPI_EXEC_MAX_NUMPROCS}'"
      "WithSubpackages_MPI_EXEC_NUMPROCS_FLAG = '${MPI_EXEC_NUMPROCS_FLAG}'"
      "WithSubpackages_PACKAGE_LIST = 'WithSubpackagesC.WithSubpackagesB.WithSubpackagesA.SimpleCxx'"
      "WithSubpackages_TPL_LIST = 'HeaderOnlyTpl'"
      "-- Configuring done"
      "-- Generating done"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_5
    MESSAGE "Build 'install' target using raw 'make'"
    CMND make ARGS install ${CTEST_BUILD_FLAGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Installing: .+/install/include/TribitsExProj_version.h"
      "Installing: .+/install/lib/cmake/TribitsExProj/TribitsExProjConfig.cmake"
      "Installing: .+/install/include/Makefile.export.TribitsExProj"
      "Installing: .+/install/lib/cmake/TribitsExProj/TribitsExProjConfigVersion.cmake"
      "Installing: .+/install/include/TribitsExProjConfig.cmake"
      "Installing: .+/install/lib/cmake/SimpleCxx/SimpleCxxConfig.cmake"
      "Installing: .+/install/lib/cmake/SimpleCxx/SimpleCxxTargets.cmake"
      "Installing: .+/install/lib/cmake/SimpleCxx/SimpleCxxTargets-release.cmake"
      "Installing: .+/install/include/Makefile.export.SimpleCxx"
      "Installing: .+/install/lib/libsimplecxx.a"
      "Installing: .+/install/include/SimpleCxx_HelloWorld.hpp"
      "Installing: .+/install/lib/cmake/WithSubpackages/WithSubpackagesConfig.cmake"
      "Installing: .+/install/include/Makefile.export.WithSubpackages"
      "Installing: .+/install/lib/libpws_a.a"
      "Installing: .+/install/include/A.hpp"
      "Installing: .+/install/lib/cmake/WithSubpackagesA/WithSubpackagesAConfig.cmake"
      "Installing: .+/install/lib/cmake/WithSubpackagesA/WithSubpackagesATargets.cmake"
      "Installing: .+/install/lib/cmake/WithSubpackagesA/WithSubpackagesATargets-release.cmake"
      "Installing: .+/install/include/Makefile.export.WithSubpackagesA"
      "Installing: .+/install/lib/libpws_b.a"
      "Installing: .+/install/include/B.hpp"
      "Installing: .+/install/lib/cmake/WithSubpackagesB/WithSubpackagesBConfig.cmake"
      "Installing: .+/install/lib/cmake/WithSubpackagesB/WithSubpackagesBTargets.cmake"
      "Installing: .+/install/lib/cmake/WithSubpackagesB/WithSubpackagesBTargets-release.cmake"
      "Installing: .+/install/include/Makefile.export.WithSubpackagesB"
      "Installing: .+/install/lib/libpws_c.a"
      "Installing: .+/install/include/wsp_c/C.hpp"
      "Installing: .+/install/lib/cmake/WithSubpackagesC/WithSubpackagesCConfig.cmake"
      "Installing: .+/install/lib/cmake/WithSubpackagesC/WithSubpackagesCTargets.cmake"
      "Installing: .+/install/lib/cmake/WithSubpackagesC/WithSubpackagesCTargets-release.cmake"
      "Installing: .+/install/include/Makefile.export.WithSubpackagesC"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_6
    MESSAGE "Create and configure a dummy project that includes"
      " WithSubpackagesConfig.cmake from the install tree"
    CMND ${CMAKE_COMMAND}
    ARGS
      -DDUMMY_PROJECT_NAME=DummyProject
      -DDUMMY_PROJECT_DIR=dummy_client_of_WithSubpackages
      -DEXPORT_VAR_PREFIX=WithSubpackages
      -DEXPORT_CONFIG_FILE=../install/lib/cmake/WithSubpackages/WithSubpackagesConfig.cmake
      -DCMAKE_COMMAND=${CMAKE_COMMAND}
      -P ${CMAKE_CURRENT_SOURCE_DIR}/RunDummyPackageClientBulid.cmake
    PASS_REGULAR_EXPRESSION_ALL
      "WithSubpackages_CMAKE_BUILD_TYPE = 'RELEASE'"
      "WithSubpackages_CXX_COMPILER = '${CMAKE_CXX_COMPILER_FOR_REGEX}'"
      "WithSubpackages_C_COMPILER = '${CMAKE_C_COMPILER_FOR_REGEX}'"
      "WithSubpackages_Fortran_COMPILER = ''"
      "WithSubpackages_FORTRAN_COMPILER = ''"
      "WithSubpackages_CXX_FLAGS = '.*'"
      "WithSubpackages_C_FLAGS = '.*'"
      "WithSubpackages_Fortran_FLAGS = '.*'"
      "WithSubpackages_EXTRA_LD_FLAGS = '.*'"
      "WithSubpackages_SHARED_LIB_RPATH_COMMAND = '.*'"
      "WithSubpackages_BUILD_SHARED_LIBS = '.*'"
      "WithSubpackages_LINKER = '.+'"
      "WithSubpackages_AR = '.+'"
      "WithSubpackages_INSTALL_DIR = '.+/install'"
      "WithSubpackages_INCLUDE_DIRS = '.+/install/lib/cmake/WithSubpackages/../../../include'"
      "WithSubpackages_LIBRARY_DIRS = '.+/install/lib/cmake/WithSubpackages/../../../lib'"
      "WithSubpackages_LIBRARIES = 'pws_c.pws_b.pws_a.simplecxx'"
      "WithSubpackages_TPL_INCLUDE_DIRS = '.+/examples/tpls/HeaderOnlyTpl'"
      "WithSubpackages_TPL_LIBRARY_DIRS = ''"
      "WithSubpackages_TPL_LIBRARIES = ''"
      "WithSubpackages_MPI_LIBRARIES = ''"
      "WithSubpackages_MPI_LIBRARY_DIRS = ''"
      "WithSubpackages_MPI_INCLUDE_DIRS = ''"
      "WithSubpackages_MPI_EXEC = '${MPI_EXEC}'"
      "WithSubpackages_MPI_EXEC_MAX_NUMPROCS = '${MPI_EXEC_MAX_NUMPROCS}'"
      "WithSubpackages_MPI_EXEC_NUMPROCS_FLAG = '${MPI_EXEC_NUMPROCS_FLAG}'"
      "WithSubpackages_PACKAGE_LIST = 'WithSubpackagesC.WithSubpackagesB.WithSubpackagesA.SimpleCxx'"
      "WithSubpackages_TPL_LIST = 'HeaderOnlyTpl'"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_7
    MESSAGE "Create and configure a dummy project that includes"
      " TribitsExProjConfig.cmake from the install tree"
    CMND ${CMAKE_COMMAND}
    ARGS
      -DDUMMY_PROJECT_NAME=DummyProject
      -DDUMMY_PROJECT_DIR=dummy_client_of_TribitsExProj
      -DEXPORT_VAR_PREFIX=TribitsExProj
      -DEXPORT_CONFIG_FILE=../install/lib/cmake/TribitsExProj/TribitsExProjConfig.cmake
      -DCMAKE_COMMAND=${CMAKE_COMMAND}
      -P ${CMAKE_CURRENT_SOURCE_DIR}/RunDummyPackageClientBulid.cmake
    PASS_REGULAR_EXPRESSION_ALL
      "DUMMY_PROJECT_NAME = 'DummyProject'"
      "DUMMY_PROJECT_DIR = 'dummy_client_of_TribitsExProj'"
      "EXPORT_CONFIG_FILE = '../install/lib/cmake/TribitsExProj/TribitsExProjConfig.cmake'"
      "EXPORT_VAR_PREFIX = 'TribitsExProj'"
      "CMAKE_COMMAND = '${CMAKE_COMMAND}"
      "Create the dummy client directory ..."
      "Create dummy dummy_client_of_TribitsExProj/CMakeLists.txt file ..."
      "Configure the dummy project to print the variables in .*/TriBITS_TribitsExampleProject_ALL_ST_NoFortran/dummy_client_of_TribitsExProj ..."
      "DUMMY_PROJECT_NAME = 'DummyProject'"
      "EXPORT_CONFIG_FILE = '../install/lib/cmake/TribitsExProj/TribitsExProjConfig.cmake'"
      "EXPORT_VAR_PREFIX = 'TribitsExProj'"
      "Including file '.*/TriBITS_TribitsExampleProject_ALL_ST_NoFortran/dummy_client_of_TribitsExProj/../install/lib/cmake/TribitsExProj/TribitsExProjConfig.cmake'"
      "TribitsExProj_CMAKE_BUILD_TYPE = 'RELEASE'"
      "TribitsExProj_CXX_COMPILER = '${CMAKE_CXX_COMPILER_FOR_REGEX}'"
      "TribitsExProj_C_COMPILER = '${CMAKE_C_COMPILER_FOR_REGEX}'"
      "TribitsExProj_Fortran_COMPILER = ''"
      "TribitsExProj_FORTRAN_COMPILER = ''"
      "TribitsExProj_CXX_FLAGS = ''"
      "TribitsExProj_C_FLAGS = ''"
      "TribitsExProj_Fortran_FLAGS = ''"
      "TribitsExProj_EXTRA_LD_FLAGS = ''"
      "TribitsExProj_SHARED_LIB_RPATH_COMMAND = ''"
      "TribitsExProj_BUILD_SHARED_LIBS = 'FALSE'"
      "TribitsExProj_LINKER = '.*'"
      "TribitsExProj_AR = '.*'"
      "TribitsExProj_INSTALL_DIR = '.*/TriBITS_TribitsExampleProject_ALL_ST_NoFortran/install'"
      "TribitsExProj_INCLUDE_DIRS = '.*/TriBITS_TribitsExampleProject_ALL_ST_NoFortran/install/include'"
      "TribitsExProj_LIBRARY_DIRS = '.*/TriBITS_TribitsExampleProject_ALL_ST_NoFortran/install/lib'"
      "TribitsExProj_LIBRARIES = 'pws_c[;]pws_b[;]pws_a[;]simplecxx'"
      "TribitsExProj_TPL_INCLUDE_DIRS = '.*/examples/tpls/HeaderOnlyTpl"
      "TribitsExProj_TPL_LIBRARY_DIRS = ''"
      "TribitsExProj_TPL_LIBRARIES = ''"
      "TribitsExProj_MPI_LIBRARIES = ''"
      "TribitsExProj_MPI_LIBRARY_DIRS = ''"
      "TribitsExProj_MPI_INCLUDE_DIRS = ''"
      "TribitsExProj_MPI_EXEC = '.*'"
      "TribitsExProj_MPI_EXEC_MAX_NUMPROCS = '[1-9]*'"  # Is null for an MPI build
      "TribitsExProj_MPI_EXEC_NUMPROCS_FLAG = '.*'"
      "TribitsExProj_PACKAGE_LIST = 'WithSubpackages[;]WithSubpackagesC[;]WithSubpackagesB[;]WithSubpackagesA[;]SimpleCxx'"
      "TribitsExProj_TPL_LIST = 'HeaderOnlyTpl"  # Must work for no MPI too
      "-- Configuring done"
      "-- Generating done"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  # ToDo: Add test for the components parts of <Project>Config.cmake ...

  # ToDo: Add test that actually builds a C++ project and links to these libs
  # to make sure this works!

  TEST_8
    MESSAGE "Create the tarball"
    CMND make ARGS package_source
    PASS_REGULAR_EXPRESSION_ALL
      "Run CPack packaging tool for source..."
      "CPack: Create package using TGZ"
      "CPack: Install projects"
      "CPack: - Install directory: .*/examples/TribitsExampleProject"
      "CPack: Create package"
      "CPack: - package: .*/ExamplesUnitTests/TriBITS_TribitsExampleProject_ALL_ST_NoFortran/tribitsexproj-1.1-Source.tar.gz generated."
      "CPack: Create package using TBZ2"
      "CPack: Install projects"
      "CPack: - Install directory: .*/examples/TribitsExampleProject"
      "CPack: Create package"
      "CPack: - package: .*/ExamplesUnitTests/TriBITS_TribitsExampleProject_ALL_ST_NoFortran/tribitsexproj-1.1-Source.tar.bz2 generated."
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_9
    MESSAGE "Untar the tarball"
    CMND tar ARGS -xzf tribitsexproj-1.1-Source.tar.gz
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_10
    MESSAGE "Make sure right directoires are excluced"
    CMND diff
    ARGS -qr
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
      tribitsexproj-1.1-Source
    PASS_REGULAR_EXPRESSION_ALL
      "Only in .*/TribitsExampleProject/cmake: ctest"
      ${REGEX_FOR_GITIGNORE}
      "Only in .*/TribitsExampleProject/packages: mixed_lang"
      "Only in .*/TribitsExampleProject/packages: wrap_external"
      "Only in .*/TribitsExampleProject/packages/with_subpackages/b: ExcludeFromRelease.txt"
      "Only in .*/TribitsExampleProject/packages/with_subpackages/b/src: AlsoExcludeFromTarball.txt"
    # NOTE: We don't check return code because diff returns nonzero

  )


if (NOT CMAKE_SYSTEM_NAME STREQUAL "Windows")

  execute_process(COMMAND whoami
    OUTPUT_STRIP_TRAILING_WHITESPACE
    OUTPUT_VARIABLE  TribitsExProj_INSTALL_OWNING_USER)

  if ("${TribitsExProj_INSTALL_OWNING_GROUP}" STREQUAL "")
    execute_process(COMMAND id -gn
      OUTPUT_STRIP_TRAILING_WHITESPACE
      OUTPUT_VARIABLE  TribitsExProj_INSTALL_OWNING_GROUP)
  endif()

endif()


if ( ${PROJECT_NAME}_ENABLE_Fortran )
  set(mixedLangHeaderRegex
    "[-]rw-rw-r--.* .* ${TribitsExProj_INSTALL_OWNING_USER} *${TribitsExProj_INSTALL_OWNING_GROUP} .* MixedLang.hpp")
else()
  set(mixedLangHeaderRegex "")
endif()

tribits_add_advanced_test( TribitsExampleProject_install_perms
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  XHOSTTYPE Windows

  TEST_0
    MESSAGE "Copy TribitsExampleProject so we can change the source permissions"
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject .

  TEST_1
    MESSAGE "Make TribitsExampleProject source dir user rwX only!"
    CMND chmod
    ARGS -R g-rwx,o-rwx TribitsExampleProject

  TEST_2
    MESSAGE "Do initial configure with just libs not tests with default install settings"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_SECONDARY_TESTED_CODE=ON
      -DTribitsExProj_ENABLE_WithSubpackages=ON
      -DCMAKE_INSTALL_PREFIX=install_base/install
      -DTribitsExProj_SET_GROUP_AND_PERMISSIONS_ON_INSTALL_BASE_DIR=install_base
      -DTribitsExProj_MAKE_INSTALL_WORLD_READABLE=TRUE
      -DTribitsExProj_MAKE_INSTALL_GROUP_WRITABLE=TRUE
      -DTribitsExProj_MAKE_INSTALL_GROUP=${TribitsExProj_INSTALL_OWNING_GROUP}
      TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Configuring done"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_3
    MESSAGE "Do make to build everything"
    CMND make ARGS ${CTEST_BUILD_FLAGS}
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_4
    MESSAGE "Make install with fixup of permissions"
    CMND make ARGS ${CTEST_BUILD_FLAGS} install
    PASS_REGULAR_EXPRESSION_ALL
      ".*/install_base/install/include/wsp_c/C.hpp"
      ".*/install_base/install/lib/libpws_c.a"
      "0: Running: chgrp ${TribitsExProj_INSTALL_OWNING_GROUP} /.*/TriBITS_TribitsExampleProject_install_perms/install_base"
      "0: Running: chmod g[+]rwX,o[+]rX /.*/TriBITS_TribitsExampleProject_install_perms/install_base"
      "1: Running: chgrp -R ${TribitsExProj_INSTALL_OWNING_GROUP} /.*/TriBITS_TribitsExampleProject_install_perms/install_base/install"
      "1: Running: chmod -R g[+]rwX,o[+]rX /.*/TriBITS_TribitsExampleProject_install_perms/install_base/install"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_5
    MESSAGE "Check some installed directory permissions and the owning group"
    CMND ls ARGS -ld
      install_base
      install_base/install
      install_base/install/bin
      install_base/install/include
      install_base/install/lib
      install_base/install/share/WithSubpackagesB/stuff
    PASS_REGULAR_EXPRESSION_ALL
      "drwxrwxr-x.* .* ${TribitsExProj_INSTALL_OWNING_USER} *${TribitsExProj_INSTALL_OWNING_GROUP} .* install_base"
      "drwxrwxr-x.* .* ${TribitsExProj_INSTALL_OWNING_USER} *${TribitsExProj_INSTALL_OWNING_GROUP} .* install_base/install"
      "drwxrwxr-x.* .* ${TribitsExProj_INSTALL_OWNING_USER} *${TribitsExProj_INSTALL_OWNING_GROUP} .* install_base/install/bin"
      "drwxrwxr-x.* .* ${TribitsExProj_INSTALL_OWNING_USER} *${TribitsExProj_INSTALL_OWNING_GROUP} .* install_base/install/include"
      "drwxrwxr-x.* .* ${TribitsExProj_INSTALL_OWNING_USER} *${TribitsExProj_INSTALL_OWNING_GROUP} .* install_base/install/lib"
      "drwxrwxr-x.* .* ${TribitsExProj_INSTALL_OWNING_USER} *${TribitsExProj_INSTALL_OWNING_GROUP} .* install_base/install/share/WithSubpackagesB/stuff"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_6
    MESSAGE "Check some installed file permissions"
    CMND ls ARGS -l
      install_base/install
      install_base/install/include
      install_base/install/include/wsp_c
      install_base/install/lib
      install_base/install/bin
      install_base/install/share/WithSubpackagesB/stuff
    PASS_REGULAR_EXPRESSION_ALL
      "${mixedLangHeaderRegex}"
      "[d]rwxrwxr-x.* .* ${TribitsExProj_INSTALL_OWNING_USER} *${TribitsExProj_INSTALL_OWNING_GROUP} .* wsp_c"
      "[-]rw-rw-r--.* .* ${TribitsExProj_INSTALL_OWNING_USER} *${TribitsExProj_INSTALL_OWNING_GROUP} .* C.hpp"
      "[-]rw-rw-r--.* .* ${TribitsExProj_INSTALL_OWNING_USER} *${TribitsExProj_INSTALL_OWNING_GROUP} .* Makefile.export.WithSubpackagesC"
      "[-]rw-rw-r--.* .* ${TribitsExProj_INSTALL_OWNING_USER} *${TribitsExProj_INSTALL_OWNING_GROUP} .* libpws_c.a"
      "[-]rwxrwxr-x.* .* ${TribitsExProj_INSTALL_OWNING_USER} *${TribitsExProj_INSTALL_OWNING_GROUP} .* exec_script.sh"
      "[-]rw-rw-r--.* .* ${TribitsExProj_INSTALL_OWNING_USER} *${TribitsExProj_INSTALL_OWNING_GROUP} .* regular_file.txt"
    ALWAYS_FAIL_ON_NONZERO_RETURN
    # NOTE: Above, the file Makefile.export.WithSubpackagesC seems to be the
    # last file installed and therefore if it has the right permissions, then
    # this final script set_installed_group_and_permissions.cmake must be
    # getting called at the very end.

  TEST_7
    MESSAGE "Make sure that exec_script.sh is executable"
    CMND ./install_base/install/share/WithSubpackagesB/stuff/exec_script.sh
    PASS_REGULAR_EXPRESSION
      "exec_script.sh executed and returned this string"

  )
  # NOTE: The above test checks a few important things:
  #
  # * The CMake install machinery will actually create multiple base dirs
  #   under ${CMAKE_INSTALL_PREFIX} in case they don't already exist.
  #
  # * The group ownership actually will be set correctly starting with
  #   ${<Project>_SET_GROUP_AND_PERMISSIONS_ON_INSTALL_BASE_DIR} which is
  #   above ${CMAKE_INSTALL_PREFIX}.  This is needed to address systems where
  #   the group sticky bit is disabled (like we see on some SNL systems, see
  #   ATDV-241).
  #
  # * Even with the source directory permissions being 'rwx------' (i.e. 700),
  #   the files isntalled under share/WithSubpackagesB/stuff using
  #   install(DIRECTORY ... USE_SOURCE_PERMISSIONS) will actually have the
  #   correct group and other permissions set.

if ( ${PROJECT_NAME}_ENABLE_Fortran )
  set(mixedLangHeaderRegex
    "[-]rw-rw-r--.* .* ${TribitsExProj_INSTALL_OWNING_USER} *${TribitsExProj_INSTALL_OWNING_GROUP} .* MixedLang.hpp")

else()
  set(mixedLangHeaderRegex "")
endif()

tribits_add_advanced_test( TribitsExampleProject_install_package_by_package_perms
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  XHOSTTYPE Windows

  TEST_0
    MESSAGE "Copy TribitsExampleProject so we can change the source permissions"
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject .

  TEST_1
    MESSAGE "Break the WithSubpackagesB so that it will not install"
    CMND ${CMAKE_CURRENT_SOURCE_DIR}/append_file_with_line.sh
    ARGS TribitsExampleProject/packages/with_subpackages/c/C.cpp
      "C.cpp is broken!"

  TEST_2
    MESSAGE "Make TribitsExampleProject source dir user rwX only!"
    CMND chmod
    ARGS -R g-rwx,o-rwx TribitsExampleProject

  TEST_3
    MESSAGE "Do initial configure with just libs not tests with default install settings"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_SECONDARY_TESTED_CODE=ON
      -DTribitsExProj_ENABLE_WithSubpackages=ON
      -DCMAKE_INSTALL_PREFIX=install_base/subdir/install
      -DTribitsExProj_SET_GROUP_AND_PERMISSIONS_ON_INSTALL_BASE_DIR=install_base
      -DTribitsExProj_MAKE_INSTALL_WORLD_READABLE=TRUE
      -DTribitsExProj_MAKE_INSTALL_GROUP_WRITABLE=TRUE
      -DTribitsExProj_MAKE_INSTALL_GROUP=${TribitsExProj_INSTALL_OWNING_GROUP}
      TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Configuring done"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_4
    MESSAGE "Do make -k to build everything that will build"
    CMND make ARGS ${CTEST_BUILD_FLAGS}
    PASS_REGULAR_EXPRESSION_ALL
      "C.cpp is broken"
      "packages/with_subpackages/c/CMakeFiles/pws_c.dir/C.cpp.o.*Error"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_5
    MESSAGE "Make install_pakage_by_package with fixup of permissions"
    CMND make ARGS ${CTEST_BUILD_FLAGS} install_package_by_package
    PASS_REGULAR_EXPRESSION_ALL
      "The global install failed so resorting to package-by-package installs"
      ".*/install_base/subdir/install/include/B.hpp"
      ".*/install_base/subdir/install/lib/libpws_b.a"
      "0: Running: chgrp ${TribitsExProj_INSTALL_OWNING_GROUP} /.*/TriBITS_TribitsExampleProject_install_package_by_package_perms/install_base"
      "0: Running: chmod g[+]rwX,o[+]rX /.*/TriBITS_TribitsExampleProject_install_package_by_package_perms/install_base"
      "1: Running: chgrp ${TribitsExProj_INSTALL_OWNING_GROUP} /.*/TriBITS_TribitsExampleProject_install_package_by_package_perms/install_base/subdir"
      "1: Running: chmod g[+]rwX,o[+]rX /.*/TriBITS_TribitsExampleProject_install_package_by_package_perms/install_base/subdir"
      "2: Running: chgrp -R ${TribitsExProj_INSTALL_OWNING_GROUP} /.*/TriBITS_TribitsExampleProject_install_package_by_package_perms/install_base/subdir/install"
      "2: Running: chmod -R g[+]rwX,o[+]rX /.*/TriBITS_TribitsExampleProject_install_package_by_package_perms/install_base/subdir/install"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_6
    MESSAGE "Check some installed directory permissions and the owning group"
    CMND ls ARGS -ld
      install_base
      install_base/subdir
      install_base/subdir/install
      install_base/subdir/install/bin
      install_base/subdir/install/include
      install_base/subdir/install/lib
      install_base/subdir/install/share/WithSubpackagesB/stuff
    PASS_REGULAR_EXPRESSION_ALL
      "drwxrwxr-x.* .* ${TribitsExProj_INSTALL_OWNING_USER} *${TribitsExProj_INSTALL_OWNING_GROUP} .* install_base"
      "drwxrwxr-x.* .* ${TribitsExProj_INSTALL_OWNING_USER} *${TribitsExProj_INSTALL_OWNING_GROUP} .* install_base/subdir"
      "drwxrwxr-x.* .* ${TribitsExProj_INSTALL_OWNING_USER} *${TribitsExProj_INSTALL_OWNING_GROUP} .* install_base/subdir/install"
      "drwxrwxr-x.* .* ${TribitsExProj_INSTALL_OWNING_USER} *${TribitsExProj_INSTALL_OWNING_GROUP} .* install_base/subdir/install/bin"
      "drwxrwxr-x.* .* ${TribitsExProj_INSTALL_OWNING_USER} *${TribitsExProj_INSTALL_OWNING_GROUP} .* install_base/subdir/install/include"
      "drwxrwxr-x.* .* ${TribitsExProj_INSTALL_OWNING_USER} *${TribitsExProj_INSTALL_OWNING_GROUP} .* install_base/subdir/install/lib"
      "drwxrwxr-x.* .* ${TribitsExProj_INSTALL_OWNING_USER} *${TribitsExProj_INSTALL_OWNING_GROUP} .* install_base/subdir/install/share/WithSubpackagesB/stuff"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_7
    MESSAGE "Check some installed file permissions"
    CMND ls ARGS -l
      install_base/subdir/install
      install_base/subdir/install/include
      install_base/subdir/install/lib
      install_base/subdir/install/bin
      install_base/subdir/install/share/WithSubpackagesB/stuff
    PASS_REGULAR_EXPRESSION_ALL
      "${mixedLangHeaderRegex}"
      "[-]rw-rw-r--.* .* ${TribitsExProj_INSTALL_OWNING_USER} *${TribitsExProj_INSTALL_OWNING_GROUP} .* B.hpp"
      "[-]rw-rw-r--.* .* ${TribitsExProj_INSTALL_OWNING_USER} *${TribitsExProj_INSTALL_OWNING_GROUP} .* Makefile.export.WithSubpackagesB"
      "[-]rw-rw-r--.* .* ${TribitsExProj_INSTALL_OWNING_USER} *${TribitsExProj_INSTALL_OWNING_GROUP} .* libpws_b.a"
      "[-]rwxrwxr-x.* .* ${TribitsExProj_INSTALL_OWNING_USER} *${TribitsExProj_INSTALL_OWNING_GROUP} .* exec_script.sh"
      "[-]rw-rw-r--.* .* ${TribitsExProj_INSTALL_OWNING_USER} *${TribitsExProj_INSTALL_OWNING_GROUP} .* regular_file.txt"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_8
    MESSAGE "Make sure that exec_script.sh is executable"
    CMND ./install_base/subdir/install/share/WithSubpackagesB/stuff/exec_script.sh
    PASS_REGULAR_EXPRESSION
      "exec_script.sh executed and returned this string"

  )
  # NOTE: In addition to the same checks performed by the test
  # TribitsExampleProject_install_perms described above, this above test also:
  #
  # * Ensures that the non-recursive group and permissions gets set on
  # * base-dirs.
  #
  # * Ensures that owning group and directory permissions get set even if
  #   there is a package install failure.  The other packages that did build
  #   correctly will get installed and all of the files and directories that
  #   did install will have the correct group and permissions.


if (NOT CMAKE_SYSTEM_NAME STREQUAL "Windows")
  set(TribitsExProj_INSTALL_BASE_DIR "" CACHE FILEPATH
    "Path to a base directory that installs will be made into that is not owned by the current user but is in the same owning group and has group write access"
    )
  if (TribitsExProj_INSTALL_BASE_DIR)
    execute_process(COMMAND stat -c %U "${TribitsExProj_INSTALL_BASE_DIR}"
      OUTPUT_STRIP_TRAILING_WHITESPACE
      OUTPUT_VARIABLE  TribitsExProj_INSTALL_BASE_OWNING_USER)
  endif()
  set(installBaseDir "${TribitsExProj_INSTALL_BASE_DIR}")
  set(installPrefixBaseDir
    "${installBaseDir}/TribitsExampleProject_install_perms_nonowning_base_dir")
  set(installPrefix
    "${installPrefixBaseDir}/install")
  if ("${TribitsExProj_INSTALL_BASE_OWNING_USER}"
    STREQUAL "${TribitsExProj_INSTALL_OWNING_USER}"
    )
    set(CHGRP_CHMOD_BASE_TEXT
      "0: Running: chgrp wg-sems-users-son /tmp/tribits_install_tests"
      "0: Running: chmod g[+]rwX,o[+]rX /tmp/tribits_install_tests")
  else()
    set(CHGRP_CHMOD_BASE_TEXT
      "0: NOTE: Not calling chgrp and chmod on ${installBaseDir} since owner '${TribitsExProj_INSTALL_BASE_OWNING_USER}' != current owner '${TribitsExProj_INSTALL_OWNING_USER}'!")
  endif()
endif()

tribits_add_advanced_test( TribitsExampleProject_install_perms_nonowning_base_dir
  OVERALL_WORKING_DIRECTORY TEST_NAME
  EXCLUDE_IF_NOT_TRUE TribitsExProj_INSTALL_BASE_DIR
  OVERALL_NUM_MPI_PROCS 1
  XHOSTTYPE Windows

  TEST_0
    MESSAGE "Copy TribitsExampleProject so we can change the source permissions"
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject .

  TEST_1
    MESSAGE "Make TribitsExampleProject source dir user rwX only!"
    CMND chmod
    ARGS -R g-rwx,o-rwx TribitsExampleProject

  TEST_2
    MESSAGE "Remove existing intermediate base install if exists"
    CMND ${CMAKE_CURRENT_SOURCE_DIR}/remove-dir-if-exists.sh
    ARGS ${installPrefixBaseDir}

  TEST_3
    MESSAGE "Do initial configure with just libs not tests with default install settings"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_SECONDARY_TESTED_CODE=ON
      -DTribitsExProj_ENABLE_WithSubpackages=ON
      -DCMAKE_INSTALL_PREFIX=${installPrefix}
      -DTribitsExProj_SET_GROUP_AND_PERMISSIONS_ON_INSTALL_BASE_DIR=${installBaseDir}
      -DTribitsExProj_MAKE_INSTALL_WORLD_READABLE=TRUE
      -DTribitsExProj_MAKE_INSTALL_GROUP_WRITABLE=TRUE
      -DTribitsExProj_MAKE_INSTALL_GROUP=${TribitsExProj_INSTALL_OWNING_GROUP}
      TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Configuring done"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_4
    MESSAGE "Do make to build everything"
    CMND make ARGS ${CTEST_BUILD_FLAGS}
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_5
    MESSAGE "Make install with fixup of permissions"
    CMND make ARGS ${CTEST_BUILD_FLAGS} install
    PASS_REGULAR_EXPRESSION_ALL
      "${installPrefix}/include/wsp_c/C.hpp"
      "${installPrefix}/lib/libpws_c.a"
      "${CHGRP_CHMOD_BASE_TEXT}"
      "1: Running: chgrp ${TribitsExProj_INSTALL_OWNING_GROUP} ${installPrefixBaseDir}"
      "1: Running: chmod g[+]rwX,o[+]rX ${installPrefixBaseDir}"
      "2: Running: chgrp -R ${TribitsExProj_INSTALL_OWNING_GROUP} ${installPrefix}"
      "2: Running: chmod -R g[+]rwX,o[+]rX ${installPrefix}"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_6
    MESSAGE "Check some installed directory permissions and the owning group"
    CMND ls ARGS -ld
      ${installBaseDir}
      ${installPrefixBaseDir}
      ${installPrefix}
      ${installPrefix}/bin
      ${installPrefix}/include
      ${installPrefix}/lib
      ${installPrefix}/share/WithSubpackagesB/stuff
    PASS_REGULAR_EXPRESSION_ALL
      "drwxrwxr-x.* .* ${TribitsExProj_INSTALL_BASE_OWNING_USER} *${TribitsExProj_INSTALL_OWNING_GROUP} .* ${installBaseDir}"
      "drwxrwxr-x.* .* ${TribitsExProj_INSTALL_OWNING_USER} +${TribitsExProj_INSTALL_OWNING_GROUP} .* ${installPrefixBaseDir}"
      "drwxrwxr-x.* .* ${TribitsExProj_INSTALL_OWNING_USER} +${TribitsExProj_INSTALL_OWNING_GROUP} .* ${installPrefix}"
      "drwxrwxr-x.* .* ${TribitsExProj_INSTALL_OWNING_USER} +${TribitsExProj_INSTALL_OWNING_GROUP} .* ${installPrefix}/bin"
      "drwxrwxr-x.* .* ${TribitsExProj_INSTALL_OWNING_USER} +${TribitsExProj_INSTALL_OWNING_GROUP} .* ${installPrefix}/include"
      "drwxrwxr-x.* .* ${TribitsExProj_INSTALL_OWNING_USER} +${TribitsExProj_INSTALL_OWNING_GROUP} .* ${installPrefix}/lib"
      "drwxrwxr-x.* .* ${TribitsExProj_INSTALL_OWNING_USER} +${TribitsExProj_INSTALL_OWNING_GROUP} .* ${installPrefix}/share/WithSubpackagesB/stuff"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  )
  # NOTE: The above test ensures that if a base dir under
  # ${TribitsExProj_SET_GROUP_AND_PERMISSIONS_ON_INSTALL_BASE_DIR} is not
  # owned by the current user then chgrp will not be run on it and will avoid
  # an error.


tribits_add_advanced_test( TribitsExampleProject_SET_GROUP_AND_PERMISSIONS_ON_INSTALL_BASE_DIR_not_base_dir
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  XHOSTTYPE Windows

  TEST_0
    MESSAGE "Configure with TribitsExProj_SET_GROUP_AND_PERMISSIONS_ON_INSTALL_BASE_DIR not a base dir of CMAKE_INSTALL_PREFIX "
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DCMAKE_INSTALL_PREFIX=install_base/install
      -DTribitsExProj_SET_GROUP_AND_PERMISSIONS_ON_INSTALL_BASE_DIR=non_base_dir
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "ERROR in TribitsExProj_SET_GROUP_AND_PERMISSIONS_ON_INSTALL_BASE_DIR"
      "TribitsExProj_SET_GROUP_AND_PERMISSIONS_ON_INSTALL_BASE_DIR=.*/TriBITS_TribitsExampleProject_SET_GROUP_AND_PERMISSIONS_ON_INSTALL_BASE_DIR_not_base_dir/non_base_dir"
      "is not a strict base dir of"
      "CMAKE_INSTALL_PREFIX=.*/TriBITS_TribitsExampleProject_SET_GROUP_AND_PERMISSIONS_ON_INSTALL_BASE_DIR_not_base_dir/install_base/install"
    ALWAYS_FAIL_ON_ZERO_RETURN

  )


tribits_add_advanced_test( TribitsExampleProject_ALL_ST_NoFortran_enable_installation_testing
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  XHOSTTYPE Darwin

  TEST_0
    MESSAGE "Copy the TribitsExampleProject locally so we can move it after install"
    WORKING_DIRECTORY BUILD_LIBS
    CMND ${CMAKE_COMMAND}
    ARGS -E copy_directory
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
      TribitsExampleProject
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_1
    MESSAGE "Do the initial configure of just the libraries"
    WORKING_DIRECTORY BUILD_LIBS
    SKIP_CLEAN_WORKING_DIRECTORY
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_ENABLE_ALL_PACKAGES=ON
      -DTribitsExProj_ENABLE_SECONDARY_TESTED_CODE=ON
      -DTribitsExProj_ENABLE_EXPORT_MAKEFILES=ON
      -DTribitsExProj_ENABLE_INSTALL_CMAKE_CONFIG_FILES=ON
      -DCMAKE_INSTALL_PREFIX=${CMAKE_CURRENT_BINARY_DIR}/${PACKAGE_NAME}_TribitsExampleProject_ALL_ST_NoFortran_enable_installation_testing/install
      TribitsExampleProject
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_2
    MESSAGE "Do Make install "
    WORKING_DIRECTORY BUILD_LIBS
    SKIP_CLEAN_WORKING_DIRECTORY
    CMND make ARGS ${CTEST_BUILD_FLAGS} install
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_3
    MESSAGE "BUILD_LIBS dir to a subdir to make sure install is independent of build and source tree"
    WORKING_DIRECTORY BUILD_LIBS_MOVED_BASE
    SKIP_CLEAN_WORKING_DIRECTORY
    CMND mv ARGS ../BUILD_LIBS .

  TEST_4
    MESSAGE "Copy the TribitsExampleProject locally so we can remove some libs source and header files"
    WORKING_DIRECTORY BUILD_TESTS
    CMND ${CMAKE_COMMAND}
    ARGS -E copy_directory
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
      TribitsExampleProject
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_5
    MESSAGE "Remove some lib header and source files from local TribitsExampleProject source tree!"
    CMND rm ARGS
      BUILD_TESTS/TribitsExampleProject/packages/simple_cxx/src/SimpleCxx_HelloWorld.hpp
      BUILD_TESTS/TribitsExampleProject/packages/simple_cxx/src/SimpleCxx_HelloWorld.cpp
      BUILD_TESTS/TribitsExampleProject/packages/with_subpackages/a/A.hpp
      BUILD_TESTS/TribitsExampleProject/packages/with_subpackages/a/A.cpp
      BUILD_TESTS/TribitsExampleProject/packages/with_subpackages/b/src/B.hpp
      BUILD_TESTS/TribitsExampleProject/packages/with_subpackages/b/src/B.cpp
      BUILD_TESTS/TribitsExampleProject/packages/with_subpackages/c/C.cpp
      BUILD_TESTS/TribitsExampleProject/packages/with_subpackages/c/wsp_c/C.hpp

  TEST_6
    MESSAGE "Do the configure of just the tests/examples pointing to existing install"
    WORKING_DIRECTORY BUILD_TESTS
    SKIP_CLEAN_WORKING_DIRECTORY
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_TESTS=ON
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_ENABLE_ALL_PACKAGES=ON
      -DTribitsExProj_ENABLE_SECONDARY_TESTED_CODE=ON
      -DTribitsExProj_ENABLE_EXPORT_MAKEFILES=ON
      -DTribitsExProj_ENABLE_INSTALL_CMAKE_CONFIG_FILES=ON
      -DTribitsExProj_ENABLE_INSTALLATION_TESTING=ON
      -DTribitsExProj_INSTALLATION_DIR=${CMAKE_CURRENT_BINARY_DIR}/${PACKAGE_NAME}_TribitsExampleProject_ALL_ST_NoFortran_enable_installation_testing/install
      TribitsExampleProject
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_7
    MESSAGE "Build 'all' target"
    WORKING_DIRECTORY BUILD_TESTS
    SKIP_CLEAN_WORKING_DIRECTORY
    CMND make ARGS ${CTEST_BUILD_FLAGS}
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_8
    MESSAGE "Run all the tests with ctest"
    WORKING_DIRECTORY BUILD_TESTS
    SKIP_CLEAN_WORKING_DIRECTORY
    CMND ${CMAKE_CTEST_COMMAND}
    PASS_REGULAR_EXPRESSION_ALL
      "SimpleCxx_HelloWorldTests${TEST_MPI_1_SUFFIX} .* Passed"
      "WithSubpackagesA_test_of_a .* Passed"
      "WithSubpackagesB_test_of_b .* Passed"
      "WithSubpackagesC_test_of_c .* Passed"
      "WithSubpackagesC_test_of_c_util.* Passed"
      "100% tests passed, 0 tests failed out of 6"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  )
# NOTE: Above is a very strong test that ensures that the
# <Project>_ENABLE_INSTALLATION_TESTING option works as it should.  This above
# test also shows the the installation of the non-Fortran packages in
# TribitsExampleProject works and is independent from the source and build
# trees.  If you comment out the cmake options
# TribitsExProj_ENABLE_INSTALLATION_TESTING and TribitsExProj_INSTALLATION_DIR
# you will see that build of the project fails because we removed some source
# files that are needed.  This proves that they are being used from the
# install tree!


# Find ninja so we can test TriBITS using ninja as well
find_program(NINJA_EXE ninja)

if ( CMAKE_VERSION VERSION_LESS 3.18.0 )
  set(rulesNinjaFilePath "rules.ninja")
else()
  set(rulesNinjaFilePath "CMakeFiles/rules.ninja")
endif()

tribits_add_advanced_test( TribitsExampleProject_ALL_ST_NoFortran_Ninja
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  EXCLUDE_IF_NOT_TRUE  NINJA_EXE
  XHOSTTYPE Darwin

  TEST_0 CMND ${CMAKE_COMMAND}
    MESSAGE "Do the initial configure with ninja"
    ARGS
      -GNinja
      -DTribitsExProj_WRITE_NINJA_MAKEFILES=OFF
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_ENABLE_ALL_PACKAGES=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      -DTribitsExProj_ENABLE_SECONDARY_TESTED_CODE=ON
      -DTribitsExProj_ENABLE_CPACK_PACKAGING=ON
      -DTribitsExProj_DUMP_CPACK_SOURCE_IGNORE_FILES=ON
      -DTribitsExProj_ENABLE_EXPORT_MAKEFILES=ON
      -DTribitsExProj_ENABLE_INSTALL_CMAKE_CONFIG_FILES=ON
      -DTribitsExProj_PARALLEL_COMPILE_JOBS_LIMIT=3
      -DTribitsExProj_PARALLEL_LINK_JOBS_LIMIT=2
      -DCMAKE_INSTALL_PREFIX=install
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Configuring done"
      "Generating done"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_1
    MESSAGE "Verify TribitsExProj_PARALLEL_COMPILE_JOBS_LIMIT=3 has correct effect"
    CMND grep ARGS -A 1 compile_job_pool ${rulesNinjaFilePath}
    PASS_REGULAR_EXPRESSION
      "depth *= *3"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_2
    MESSAGE "Verify TribitsExProj_PARALLEL_LINK_JOBS_LIMIT=2 has correct effect"
    CMND grep ARGS -A 1 link_job_pool ${rulesNinjaFilePath}
    PASS_REGULAR_EXPRESSION
      "depth *= *2"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_3 CMND ninja ARGS -j1 ${CTEST_BUILD_FLAGS}
    MESSAGE "Build the default 'all' target using raw 'ninja'"
    PASS_REGULAR_EXPRESSION_ALL
      "Linking CXX .* library .*simplecxx"
      "Linking CXX executable .*simplecxx-helloworld"
      "Linking CXX .* library .*pws_a"
      "Linking CXX .* library .*pws_b"
      "Linking CXX .* library .*pws_c"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  # ToDo: Add check of 'ninja" returns "ninja: no work to do"

  TEST_4 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    MESSAGE "Run all the tests with raw 'ctest'"
    PASS_REGULAR_EXPRESSION_ALL
      "SimpleCxx_HelloWorldTests${TEST_MPI_1_SUFFIX} .* Passed"
      "WithSubpackagesA_test_of_a .* Passed"
      "WithSubpackagesB_test_of_b .* Passed"
      "WithSubpackagesC_test_of_c .* Passed"
      "WithSubpackagesC_test_of_c_util.* Passed"
      "100% tests passed, 0 tests failed out of 6"

  TEST_5
    MESSAGE "Create and configure a dummy project that includes WithSubpackagesConfig.cmake"
      " from the build tree"
    CMND ${CMAKE_COMMAND}
    ARGS
      -DDUMMY_PROJECT_NAME=DummyProject
      -DDUMMY_PROJECT_DIR=dummy_client_of_build_WithSubpackages
      -DEXPORT_VAR_PREFIX=WithSubpackages
      -DEXPORT_CONFIG_FILE=../packages/with_subpackages/WithSubpackagesConfig.cmake
      -DCMAKE_COMMAND=${CMAKE_COMMAND}
      -P ${CMAKE_CURRENT_SOURCE_DIR}/RunDummyPackageClientBulid.cmake
    PASS_REGULAR_EXPRESSION_ALL
      "WithSubpackages_INSTALL_DIR = '.*/TriBITS_TribitsExampleProject_ALL_ST_NoFortran_Ninja/install'"
      "WithSubpackages_LIBRARIES = 'pws_c.pws_b.pws_a.simplecxx'"
      "WithSubpackages_TPL_INCLUDE_DIRS = '.+/tribits/examples/tpls/HeaderOnlyTpl'"
      "WithSubpackages_PACKAGE_LIST = 'WithSubpackagesC.WithSubpackagesB.WithSubpackagesA.SimpleCxx'"
      "WithSubpackages_TPL_LIST = 'HeaderOnlyTpl'"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_6 CMND ninja ARGS -j1 install ${CTEST_BUILD_FLAGS}
    MESSAGE "Build 'install' target using raw 'ninja'"
    PASS_REGULAR_EXPRESSION_ALL
      "Installing: .+/install/include/TribitsExProj_version.h"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_7
    MESSAGE "Configure dummy project pointing to install tree"
    CMND ${CMAKE_COMMAND}
    ARGS
      -DDUMMY_PROJECT_NAME=DummyProject
      -DDUMMY_PROJECT_DIR=dummy_client_of_WithSubpackages
      -DEXPORT_VAR_PREFIX=WithSubpackages
      -DEXPORT_CONFIG_FILE=../install/lib/cmake/WithSubpackages/WithSubpackagesConfig.cmake
      -DCMAKE_COMMAND=${CMAKE_COMMAND}
      -P ${CMAKE_CURRENT_SOURCE_DIR}/RunDummyPackageClientBulid.cmake
    MESSAGE "Create and configure a dummy project that includes WithSubpackagesConfig.cmake"
    PASS_REGULAR_EXPRESSION_ALL
      "WithSubpackages_INSTALL_DIR = '.*/TriBITS_TribitsExampleProject_ALL_ST_NoFortran_Ninja/install'"
      "WithSubpackages_LIBRARY_DIRS = '.+/install/lib/cmake/WithSubpackages/../../../lib'"
      "WithSubpackages_LIBRARIES = 'pws_c.pws_b.pws_a.simplecxx'"
      "WithSubpackages_TPL_INCLUDE_DIRS = '.+/examples/tpls/HeaderOnlyTpl'"
      "WithSubpackages_PACKAGE_LIST = 'WithSubpackagesC.WithSubpackagesB.WithSubpackagesA.SimpleCxx'"
      "WithSubpackages_TPL_LIST = 'HeaderOnlyTpl'"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_8 CMND ninja ARGS -j1 package_source
    MESSAGE "Create the tarball"
    PASS_REGULAR_EXPRESSION_ALL
      "Run CPack packaging tool for source..."
      "CPack: - package: .*/ExamplesUnitTests/TriBITS_TribitsExampleProject_ALL_ST_NoFortran_Ninja/tribitsexproj-1.1-Source.tar.gz generated."
    ALWAYS_FAIL_ON_NONZERO_RETURN
    # Above should be 'make package_soruce' but the dummy makefiles don't
    # support that yet!

  TEST_9 CMND tar ARGS -xzf tribitsexproj-1.1-Source.tar.gz
    MESSAGE "Untar the tarball"

  TEST_10 CMND diff
     ARGS -qr
       ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
       tribitsexproj-1.1-Source
    MESSAGE "Make sure right directoires are excluced"
    PASS_REGULAR_EXPRESSION_ALL
      "Only in .*/TribitsExampleProject/cmake: ctest"
      ${REGEX_FOR_GITIGNORE}
      "Only in .*/TribitsExampleProject/packages: mixed_lang"
      "Only in .*/TribitsExampleProject/packages: wrap_external"
    # NOTE: We don't check the the return code form diff because it will
    # return nonzero if there are any differences

  )


tribits_add_advanced_test( TribitsExampleProject_ALL_ST_NoFortran_Ninja_Makefiles
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  EXCLUDE_IF_NOT_TRUE  NINJA_EXE
  XHOSTTYPE Darwin

  TEST_0 CMND ${CMAKE_COMMAND}
    MESSAGE "Do the initial configure with ninja"
    ARGS
      -GNinja
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_ENABLE_ALL_PACKAGES=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      -DTribitsExProj_ENABLE_SECONDARY_TESTED_CODE=ON
      -DTribitsExProj_ENABLE_CPACK_PACKAGING=ON
      -DTribitsExProj_DUMP_CPACK_SOURCE_IGNORE_FILES=ON
      -DTribitsExProj_ENABLE_EXPORT_MAKEFILES=ON
      -DTribitsExProj_ENABLE_INSTALL_CMAKE_CONFIG_FILES=ON
      -DCMAKE_INSTALL_PREFIX=install
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Configuring done"
      "Generating done"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_1 CMND make ARGS ${MAKE_PARALLEL_ARG} ${CTEST_BUILD_FLAGS}
    MESSAGE "Build the default 'all' target using raw 'make'"
    PASS_REGULAR_EXPRESSION_ALL
      "Linking CXX .* library .*simplecxx"
      "Linking CXX executable .*simplecxx-helloworld"
      "Linking CXX .* library .*pws_a"
      "Linking CXX .* library .*pws_b"
      "Linking CXX .* library .*pws_c"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  # ToDo: Add check of 'make" returns "ninja: no work to do"

  TEST_2 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    MESSAGE "Run all the tests with raw 'ctest'"
    PASS_REGULAR_EXPRESSION_ALL
      "SimpleCxx_HelloWorldTests${TEST_MPI_1_SUFFIX} .* Passed"
      "WithSubpackagesA_test_of_a .* Passed"
      "WithSubpackagesB_test_of_b .* Passed"
      "WithSubpackagesC_test_of_c .* Passed"
      "WithSubpackagesC_test_of_c_util.* Passed"
      "100% tests passed, 0 tests failed out of 6"

  TEST_3
    MESSAGE "Create and configure a dummy project that includes WithSubpackagesConfig.cmake"
      " from the build tree"
    CMND ${CMAKE_COMMAND}
    ARGS
      -DDUMMY_PROJECT_NAME=DummyProject
      -DDUMMY_PROJECT_DIR=dummy_client_of_build_WithSubpackages
      -DEXPORT_VAR_PREFIX=WithSubpackages
      -DEXPORT_CONFIG_FILE=../packages/with_subpackages/WithSubpackagesConfig.cmake
      -DCMAKE_COMMAND=${CMAKE_COMMAND}
      -P ${CMAKE_CURRENT_SOURCE_DIR}/RunDummyPackageClientBulid.cmake
    PASS_REGULAR_EXPRESSION_ALL
      "WithSubpackages_INSTALL_DIR = '.*/TriBITS_TribitsExampleProject_ALL_ST_NoFortran_Ninja_Makefiles/install'"
      "WithSubpackages_LIBRARIES = 'pws_c.pws_b.pws_a.simplecxx'"
      "WithSubpackages_TPL_INCLUDE_DIRS = '.+/tribits/examples/tpls/HeaderOnlyTpl'"
      "WithSubpackages_PACKAGE_LIST = 'WithSubpackagesC.WithSubpackagesB.WithSubpackagesA.SimpleCxx'"
      "WithSubpackages_TPL_LIST = 'HeaderOnlyTpl'"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_4 CMND make ARGS ${MAKE_PARALLEL_ARG} install ${CTEST_BUILD_FLAGS}
    MESSAGE "Build 'install' target using raw 'make'"
    PASS_REGULAR_EXPRESSION_ALL
      "Installing: .+/install/include/TribitsExProj_version.h"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_5
    MESSAGE "Configure dummy project pointing to install tree"
    CMND ${CMAKE_COMMAND}
    ARGS
      -DDUMMY_PROJECT_NAME=DummyProject
      -DDUMMY_PROJECT_DIR=dummy_client_of_WithSubpackages
      -DEXPORT_VAR_PREFIX=WithSubpackages
      -DEXPORT_CONFIG_FILE=../install/lib/cmake/WithSubpackages/WithSubpackagesConfig.cmake
      -DCMAKE_COMMAND=${CMAKE_COMMAND}
      -P ${CMAKE_CURRENT_SOURCE_DIR}/RunDummyPackageClientBulid.cmake
    MESSAGE "Create and configure a dummy project that includes WithSubpackagesConfig.cmake"
    PASS_REGULAR_EXPRESSION_ALL
      "WithSubpackages_INSTALL_DIR = '.*/TriBITS_TribitsExampleProject_ALL_ST_NoFortran_Ninja_Makefiles/install'"
      "WithSubpackages_LIBRARY_DIRS = '.+/install/lib/cmake/WithSubpackages/../../../lib'"
      "WithSubpackages_LIBRARIES = 'pws_c.pws_b.pws_a.simplecxx'"
      "WithSubpackages_TPL_INCLUDE_DIRS = '.+/examples/tpls/HeaderOnlyTpl'"
      "WithSubpackages_PACKAGE_LIST = 'WithSubpackagesC.WithSubpackagesB.WithSubpackagesA.SimpleCxx'"
      "WithSubpackages_TPL_LIST = 'HeaderOnlyTpl'"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_6 CMND make ARGS ${MAKE_PARALLEL_ARG} package_source
    MESSAGE "Create the tarball"
    PASS_REGULAR_EXPRESSION_ALL
      "Run CPack packaging tool for source..."
      "CPack: - package: .*/ExamplesUnitTests/TriBITS_TribitsExampleProject_ALL_ST_NoFortran_Ninja_Makefiles/tribitsexproj-1.1-Source.tar.gz generated."
    ALWAYS_FAIL_ON_NONZERO_RETURN
    # Above should be 'make package_soruce' but the dummy makefiles don't
    # support that yet!

  TEST_7 CMND tar ARGS -xzf tribitsexproj-1.1-Source.tar.gz
    MESSAGE "Untar the tarball"

  TEST_8 CMND diff
     ARGS -qr
       ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
       tribitsexproj-1.1-Source
    MESSAGE "Make sure right directoires are excluced"
    PASS_REGULAR_EXPRESSION_ALL
      "Only in .*/TribitsExampleProject/cmake: ctest"
      ${REGEX_FOR_GITIGNORE}
      "Only in .*/TribitsExampleProject/packages: mixed_lang"
      "Only in .*/TribitsExampleProject/packages: wrap_external"
    # NOTE: We don't check the the return code form diff because it will
    # return nonzero if there are any differences

  )


if (NOT ${PROJECT_NAME}_HOSTTYPE STREQUAL "Windows")

  tribits_add_advanced_test( TribitsExampleProject_ALL_PT_NoFortran_ConfigTiming
    OVERALL_WORKING_DIRECTORY TEST_NAME
    OVERALL_NUM_MPI_PROCS 1
    XHOSTTYPE Darwin

    TEST_0 CMND ${CMAKE_COMMAND}
      MESSAGE "Do the initial configure with basic configure timing"
      ARGS
        ${TribitsExampleProject_COMMON_CONFIG_ARGS}
        -DTribitsExProj_ENABLE_Fortran=OFF
        -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
        -DTribitsExProj_ENABLE_ALL_PACKAGES=ON
        -DTribitsExProj_ENABLE_TESTS=ON
        -DTribitsExProj_ENABLE_CPACK_PACKAGING=ON
        -DTribitsExProj_ENABLE_EXPORT_MAKEFILES=ON
        -DTribitsExProj_ENABLE_CONFIGURE_TIMING=ON
        ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
      PASS_REGULAR_EXPRESSION_ALL
        "Total time to read in all dependencies files and build dependencies graph: "
        "Total time to adjust package and TPL enables: "
        "Total time to probe and setup the environment: "
        "Total time to configure enabled TPLs: "
        "Total time to configure enabled packages: "
        "Total time to set up for CPack packaging: "
        "Total time to configure TribitsExProj: "
        "Final set of enabled packages:  SimpleCxx WithSubpackages 2"
        "Final set of enabled SE packages:  SimpleCxx WithSubpackagesA WithSubpackages 3"

    TEST_1 CMND ${CMAKE_COMMAND}
      MESSAGE "Reconfigure to test out timing of all packages"
      ARGS
        -DTribitsExProj_ENABLE_PACKAGE_CONFIGURE_TIMING=ON
        .
      PASS_REGULAR_EXPRESSION_ALL
        "Total time to read in all dependencies files and build dependencies graph: "
        "Total time to adjust package and TPL enables: "
        "Total time to probe and setup the environment: "
        "Total time to configure enabled TPLs: "
        "-- Total time to configure package SimpleCxx: "
        "-- Total time to configure package WithSubpackages: "
        "Total time to configure enabled packages: "
        "Total time to set up for CPack packaging: "
        "Total time to configure TribitsExProj: "

    TEST_2 CMND ${CMAKE_COMMAND}
      MESSAGE "Reconfigure to test out timing of just one package"
      ARGS
        -DTribitsExProj_ENABLE_PACKAGE_CONFIGURE_TIMING=OFF
        -DSimpleCxx_PACKAGE_CONFIGURE_TIMING=ON
        .
      PASS_REGULAR_EXPRESSION_ALL
        "Total time to read in all dependencies files and build dependencies graph: "
        "Total time to adjust package and TPL enables: "
        "Total time to probe and setup the environment: "
        "Total time to configure enabled TPLs: "
        "-- Total time to configure package SimpleCxx: "
        "Total time to configure enabled packages: "
        "Total time to set up for CPack packaging: "
        "Total time to configure TribitsExProj: "

    )

endif()


tribits_add_advanced_test( TribitsExampleProject_ALL_PT_NoFortran
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0 CMND ${CMAKE_COMMAND}
    MESSAGE "Do the initial configure (and test a lot of things at once)"
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_ALL_PACKAGES=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      -DTribitsExProj_DUMP_PACKAGE_DEPENDENCIES=ON
      -DTribitsExProj_ENABLE_EXPORT_MAKEFILES=ON
      -DTribitsExProj_ENABLE_INSTALL_CMAKE_CONFIG_FILES=ON
      -DCMAKE_CXX_FLAGS=-DSIMPLECXX_SHOW_DEPRECATED_WARNINGS=1
      -DTribitsExProj_SHOW_DEPRECATED_WARNINGS=OFF
      -DCMAKE_INSTALL_PREFIX=install
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "-- SimpleCxx: No library dependencies!"
      "-- WithSubpackagesA_FULL_ENABLED_DEP_PACKAGES: SimpleCxx"
      "-- WithSubpackages_FULL_ENABLED_DEP_PACKAGES: WithSubpackagesA SimpleCxx"
      "Explicitly enabled packages on input .by user.:  0"
      "Explicitly disabled packages on input .by user or by default.:  MixedLang WrapExternal 2"
      "Final set of enabled packages:  SimpleCxx WithSubpackages 2"
      "Final set of enabled SE packages:  SimpleCxx WithSubpackagesA WithSubpackages 3"
      "Final set of non-enabled packages:  MixedLang WrapExternal 2"
      "Final set of non-enabled SE packages:  MixedLang WithSubpackagesB WithSubpackagesC WrapExternal 4"
  # NOTES: In the above test, we do a configure with
  # SIMPLECXX_SHOW_DEPRECATED_WARNINGS=1 and
  # TribitsExProj_SHOW_DEPRECATED_WARNINGS=OFF so that deprecated functions
  # are called but deprecated warnings for these functions are turned off.
  # This makes sure the macros XXX_DEPRECATED and XXX_DEPRECATED_MSG are
  # defined as tempy.

  TEST_1 CMND make ARGS ${CTEST_BUILD_FLAGS}
    MESSAGE "Build the default 'all' target using raw 'make'"
    PASS_REGULAR_EXPRESSION_ALL
      "Built target simplecxx"
      "Built target pws_a"

  TEST_2 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    MESSAGE "Run all the tests with raw 'ctest'"
    PASS_REGULAR_EXPRESSION_ALL
      "SimpleCxx_HelloWorldTests${TEST_MPI_1_SUFFIX} .* Passed"
      "WithSubpackagesA_test_of_a .* Passed"
      "100% tests passed, 0 tests failed out of 3"

  TEST_3 CMND make ARGS install ${CTEST_BUILD_FLAGS}
    MESSAGE "Build 'install' target using raw 'make'"
    PASS_REGULAR_EXPRESSION_ALL
      "Installing: .+/install/lib/cmake/WithSubpackages/WithSubpackagesConfig.cmake"
      "Installing: .+/install/include/Makefile.export.WithSubpackages"

  TEST_4 CMND ${CMAKE_COMMAND}
    ARGS
      -DDUMMY_PROJECT_NAME=DummyProject
      -DDUMMY_PROJECT_DIR=dummy_client_of_WithSubpackages
      -DEXPORT_VAR_PREFIX=WithSubpackages
      -DEXPORT_CONFIG_FILE=../install/lib/cmake/WithSubpackages/WithSubpackagesConfig.cmake
      -DCMAKE_COMMAND=${CMAKE_COMMAND}
      -P ${CMAKE_CURRENT_SOURCE_DIR}/RunDummyPackageClientBulid.cmake
    MESSAGE "Create and configure a dummy project that includes WithSubpackagesConfig.cmake"
    PASS_REGULAR_EXPRESSION_ALL
      "WithSubpackages_INSTALL_DIR = '.+/install'"
      "WithSubpackages_INCLUDE_DIRS = '.+/install/lib/cmake/WithSubpackages/../../../include'"
      "WithSubpackages_LIBRARY_DIRS = '.+/install/lib/cmake/WithSubpackages/../../../lib'"
      "WithSubpackages_LIBRARIES = 'pws_a.simplecxx'"
      "WithSubpackages_PACKAGE_LIST = 'WithSubpackagesA.SimpleCxx'"
  )


tribits_add_advanced_test( TribitsExampleProject_ALL_ST
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
      -DTribitsExProj_ENABLE_EXPORT_MAKEFILES=ON
      -DTribitsExProj_ENABLE_INSTALL_CMAKE_CONFIG_FILES=ON
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "NOTE: Setting TribitsExProj_ENABLE_WrapExternal=OFF because "
      "Explicitly enabled packages on input .by user.:  0"
      "Explicitly disabled packages on input .by user or by default.:  WrapExternal 1"
      "Enabling all SE packages that are not currently disabled because of TribitsExProj_ENABLE_ALL_PACKAGES=ON "
      "Setting TribitsExProj_ENABLE_SimpleCxx=ON"
      "Setting TribitsExProj_ENABLE_MixedLang=ON"
      "Setting TribitsExProj_ENABLE_WithSubpackages=ON"
      "Final set of enabled packages:  SimpleCxx MixedLang WithSubpackages 3"
      "Final set of enabled SE packages:  SimpleCxx MixedLang WithSubpackagesA WithSubpackagesB WithSubpackagesC WithSubpackages 6"
      "Final set of non-enabled packages:  WrapExternal 1"
      "Configuring done"
      "Generating done"
      "Build files have been written to: .*ExamplesUnitTests/TriBITS_TribitsExampleProject_ALL_ST"
  TEST_1 CMND make
    MESSAGE "Build the default 'all' target using raw 'make'"
    ARGS ${CTEST_BUILD_FLAGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Built target simplecxx"
      "Built target mixedlang"
      "Built target pws_a"
      "Built target pws_b"
      "Built target pws_c"
  TEST_2 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    MESSAGE "Run all the tests with raw 'ctest'"
    PASS_REGULAR_EXPRESSION_ALL
      "SimpleCxx_HelloWorldTests${TEST_MPI_1_SUFFIX} .* Passed"
      "MixedLang_RayTracerTests${TEST_MPI_1_SUFFIX} .* Passed"
      "WithSubpackagesA_test_of_a .* Passed"
      "WithSubpackagesB_test_of_b .* Passed"
      "WithSubpackagesB_test_of_b_mixed_lang.* Passed"
      "WithSubpackagesC_test_of_c_util.* Passed"
      "WithSubpackagesC_test_of_c .* Passed"
      "WithSubpackagesC_test_of_c_b_mixed_lang.* Passed"
      "100% tests passed, 0 tests failed out of 9"
  )


tribits_add_advanced_test( TribitsExampleProject_ALL_ST_LibPrefix
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
      -DTribitsExProj_ENABLE_EXPORT_MAKEFILES=ON
      -DTribitsExProj_ENABLE_INSTALL_CMAKE_CONFIG_FILES=ON
      -DTribitsExProj_LIBRARY_NAME_PREFIX=tep_
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "NOTE: Setting TribitsExProj_ENABLE_WrapExternal=OFF because "
      "Explicitly enabled packages on input .by user.:  0"
      "Explicitly disabled packages on input .by user or by default.:  WrapExternal 1"
      "Enabling all SE packages that are not currently disabled because of TribitsExProj_ENABLE_ALL_PACKAGES=ON "
      "Setting TribitsExProj_ENABLE_SimpleCxx=ON"
      "Setting TribitsExProj_ENABLE_MixedLang=ON"
      "Setting TribitsExProj_ENABLE_WithSubpackages=ON"
      "Final set of enabled packages:  SimpleCxx MixedLang WithSubpackages 3"
      "Final set of enabled SE packages:  SimpleCxx MixedLang WithSubpackagesA WithSubpackagesB WithSubpackagesC WithSubpackages 6"
      "Final set of non-enabled packages:  WrapExternal 1"
      "Configuring done"
      "Generating done"
      "Build files have been written to: .*ExamplesUnitTests/TriBITS_TribitsExampleProject_ALL_ST_LibPrefix"
  TEST_1 CMND make
    MESSAGE "Build the default 'all' target using raw 'make'"
    ARGS ${CTEST_BUILD_FLAGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Built target tep_simplecxx"
      "Built target tep_mixedlang"
      "Built target tep_pws_a"
      "Built target tep_pws_b"
      "Built target tep_pws_c"
  TEST_2 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    MESSAGE "Run all the tests with raw 'ctest'"
    PASS_REGULAR_EXPRESSION_ALL
      "SimpleCxx_HelloWorldTests${TEST_MPI_1_SUFFIX} .* Passed"
      "MixedLang_RayTracerTests${TEST_MPI_1_SUFFIX} .* Passed"
      "WithSubpackagesA_test_of_a .* Passed"
      "WithSubpackagesB_test_of_b .* Passed"
      "WithSubpackagesB_test_of_b_mixed_lang.* Passed"
      "WithSubpackagesC_test_of_c_util.* Passed"
      "WithSubpackagesC_test_of_c .* Passed"
      "WithSubpackagesC_test_of_c_b_mixed_lang.* Passed"
      "100% tests passed, 0 tests failed out of 9"
  )


tribits_add_advanced_test( TribitsExampleProject_ALL_ST_LibUsage
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  EXCLUDE_IF_NOT_TRUE ${PROJECT_NAME}_ENABLE_Fortran

  TEST_0
    MESSAGE "Do the initial configure to get the package enables"
      " and the  env probe in place."
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=ON
      -DPYTHON_EXECUTABLE=
      -DTribitsExProj_ENABLE_ALL_PACKAGES=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      -DTribitsExProj_ENABLE_SECONDARY_TESTED_CODE=ON
      -DTribitsExProj_ENABLE_EXPORT_MAKEFILES=OFF
      -DTribitsExProj_ENABLE_INSTALL_CMAKE_CONFIG_FILES=OFF
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "NOTE: Setting TribitsExProj_ENABLE_WrapExternal=OFF because PYTHON_EXECUTABLE=''"
      "Final set of enabled packages:  SimpleCxx MixedLang WithSubpackages 3"
      "Final set of enabled SE packages:  SimpleCxx MixedLang WithSubpackagesA WithSubpackagesB WithSubpackagesC WithSubpackages 6"
      "Configuring done"
      "Generating done"
      "Build files have been written to: .*/TriBITS_TribitsExampleProject_ALL_ST_LibUsage"

  #
  # Testing passing libs to tribits_add_library()
  #

  TEST_1
    MESSAGE "Show deprecated warning when trying to link lib from upstream SE package."
    CMND ${CMAKE_COMMAND}
    ARGS -DSPKB_SHOW_UPSTREAM_DEPLIBS_ERROR=ON
      .
    PASS_REGULAR_EXPRESSION_ALL
      "WARNING: 'simplecxx' in DEPLIBS is not a lib in this SE package"
      "packages/with_subpackages/b/src/CMakeLists.txt:.* [(]tribits_add_library[)]"
      "Generating done"
      "Build files have been written to: .*/TriBITS_TribitsExampleProject_ALL_ST_LibUsage"

  TEST_2
    MESSAGE "Show deprecated warning when passing a lib from this SE package through IMPORTEDLIBS."
    CMND ${CMAKE_COMMAND}
    ARGS -DSPKB_SHOW_SE_PKG_LIB_IMPORTEDLIBS_ERROR=ON
      -DSPKB_SHOW_UPSTREAM_DEPLIBS_ERROR=
      .
    PASS_REGULAR_EXPRESSION_ALL
      "WARNING: Lib 'pws_b' in IMPORTEDLIBS is in this SE package "
      "packages/with_subpackages/b/tests/testlib/CMakeLists.txt:.* [(]tribits_add_library[)]"
      "Generating done"
      "Build files have been written to: .*/TriBITS_TribitsExampleProject_ALL_ST_LibUsage"

  TEST_3
    MESSAGE "Show deprecated warning when passing a lib from upstream"
      " SE package through IMPORTEDLIBS."
    CMND ${CMAKE_COMMAND}
    ARGS -DSPKB_SHOW_UPSTREAM_SE_PKG_LIB_IMPORTEDLIBS_ERROR=ON
      -DSPKB_SHOW_SE_PKG_LIB_IMPORTEDLIBS_ERROR=
      .
    PASS_REGULAR_EXPRESSION_ALL
      "WARNING: Lib 'simplecxx' being passed through IMPORTEDLIBS"
      "TribitsExampleProject/packages/with_subpackages/b/cmake/Dependencies.cmake"
      "packages/with_subpackages/b/tests/testlib/CMakeLists.txt:.* [(]tribits_add_library[)]"
      "Generating done"
      "Build files have been written to: .*/TriBITS_TribitsExampleProject_ALL_ST_LibUsage"

  TEST_4
    MESSAGE "Show deprecated warning when passing a TESTONLY lib through DEPLBIS."
    CMND ${CMAKE_COMMAND}
    ARGS -DSPKC_SHOW_TESTONLY_DEPLBIS_ERROR=ON
      -DSPKB_SHOW_UPSTREAM_SE_PKG_LIB_IMPORTEDLIBS_ERROR=
      .
    PASS_REGULAR_EXPRESSION_ALL
      "WARNING: 'b_mixed_lang' in DEPLIBS is a TESTONLY lib "
      "TribitsExampleProject/packages/with_subpackages/c/cmake/Dependencies.cmake"
      "packages/with_subpackages/c/CMakeLists.txt:.* [(]tribits_add_library[)]"
      "Generating done"
      "Build files have been written to: .*/TriBITS_TribitsExampleProject_ALL_ST_LibUsage"

  TEST_5
    MESSAGE "Show deprecated warning when passing a TESTONLY lib through IMPORTEDLIBS."
    CMND ${CMAKE_COMMAND}
    ARGS -DSPKC_SHOW_TESTONLY_IMPORTEDLIBS_ERROR=ON
      -DSPKC_SHOW_TESTONLY_DEPLBIS_ERROR=
      .
    PASS_REGULAR_EXPRESSION_ALL
      "WARNING: 'b_mixed_lang' in IMPORTEDLIBS is a TESTONLY lib"
      "packages/with_subpackages/c/CMakeLists.txt:.* [(]tribits_add_library[)]"
      "Generating done"
      "Build files have been written to: .*/TriBITS_TribitsExampleProject_ALL_ST_LibUsage"

  TEST_6
    MESSAGE "Show deprecated warning when passing m through DEPLIBS."
    CMND ${CMAKE_COMMAND}
    ARGS -DSPKB_SHOW_M_DEPLIBS_ERROR=ON
      -DSPKC_SHOW_TESTONLY_IMPORTEDLIBS_ERROR=
      .
    PASS_REGULAR_EXPRESSION_ALL
      "WARNING: 'm' in DEPLIBS is not a lib defined in the current cmake "
      "packages/with_subpackages/b/src/CMakeLists.txt:.* [(]tribits_add_library[)]"
      "Generating done"
      "Build files have been written to: .*/TriBITS_TribitsExampleProject_ALL_ST_LibUsage"

  #
  # Testing passing libs to tribits_add_executable()
  #

  TEST_7
    MESSAGE "Show error when trying to link an INSTALLABLE exec against a TESTONLY lib."
    CMND ${CMAKE_COMMAND}
    ARGS -DSPKB_SHOW_TESTONLY_INSTALLABLE_ERROR=ON
      -DSPKB_SHOW_M_DEPLIBS_ERROR=
      .
    PASS_REGULAR_EXPRESSION_ALL
      "ERROR: TESTONLY lib 'b_test_utils' not allowed with INSTALLABLE executable"
      "packages/with_subpackages/b/tests/CMakeLists.txt:.* [(]tribits_add_executable_and_test[)]"
      "Configuring incomplete, errors occurred!"

  TEST_8
    MESSAGE "Show error when trying to link against non-TESTONLY lib."
    CMND ${CMAKE_COMMAND}
    ARGS -DSPKB_SHOW_NON_TESTONLY_LIB_ERROR=ON
      -DSPKB_SHOW_TESTONLY_INSTALLABLE_ERROR=
      .
    PASS_REGULAR_EXPRESSION_ALL
      " ERROR: 'simplecxx' in TESTONLYLIBS not a TESTONLY lib"
      "packages/with_subpackages/b/tests/CMakeLists.txt:.* [(]tribits_add_executable_and_test[)]"
      "Configuring incomplete, errors occurred!"

  TEST_9
    MESSAGE "Show error when trying to link SE package lib using TESTONLYLIBS"
    CMND ${CMAKE_COMMAND}
    ARGS -DSPKB_SHOW_IMPORTED_LIBS_THIS_PKG_ERROR=ON
      -DSPKB_SHOW_NON_TESTONLY_LIB_ERROR=
      .
    PASS_REGULAR_EXPRESSION_ALL
      "ERROR: Lib 'pws_b' in IMPORTEDLIBS is in this SE package"
      "packages/with_subpackages/b/tests/CMakeLists.txt:.* [(]tribits_add_executable_and_test[)]"
      "Configuring incomplete, errors occurred!"

  TEST_10
    MESSAGE "Show deprecated warning when trying to link TESTONLY lib using DEBLIBS."
    CMND ${CMAKE_COMMAND}
    ARGS -DSPKB_SHOW_TESTONLY_DEBLIBS_WARNING=ON
      -DSPKB_SHOW_IMPORTED_LIBS_THIS_PKG_ERROR=
      .
    PASS_REGULAR_EXPRESSION_ALL
      "WARNING: Passing TESTONLY lib 'b_mixed_lang' through DEPLIBS is deprecated"
      "packages/with_subpackages/b/tests/CMakeLists.txt:.* [(]tribits_add_executable_and_test[)]"
      "Generating done"
      "Build files have been written to: .*/TriBITS_TribitsExampleProject_ALL_ST_LibUsage"

  TEST_11
    MESSAGE "Show deprecated warning when trying to link non-TESTONLY lib using DEBLIBS."
    CMND ${CMAKE_COMMAND}
    ARGS -DSPKB_SHOW_NONTESTONLY_DEBLIBS_WARNING=ON
      -DSPKB_SHOW_TESTONLY_DEBLIBS_WARNING=
      .
    PASS_REGULAR_EXPRESSION_ALL
      "WARNING: Passing non-TESTONLY lib 'pws_b' through DEPLIBS is deprecated"
      "packages/with_subpackages/b/tests/CMakeLists.txt:.* [(]tribits_add_executable_and_test[)]"
      "Generating done"
      "Build files have been written to: .*/TriBITS_TribitsExampleProject_ALL_ST_LibUsage"

  TEST_12
    MESSAGE "Show deprecated warning when trying to link external lib using DEBLIBS."
    CMND ${CMAKE_COMMAND}
    ARGS -DSPKB_SHOW_EXTERNAL_DEBLIBS_WARNING=ON
      -DSPKB_SHOW_NONTESTONLY_DEBLIBS_WARNING=
      .
    PASS_REGULAR_EXPRESSION_ALL
      "WARNING: Passing external lib 'm' through DEPLIBS is deprecated"
      "packages/with_subpackages/b/tests/CMakeLists.txt:.* [(]tribits_add_executable_and_test[)]"
      "Generating done"
      "Build files have been written to: .*/TriBITS_TribitsExampleProject_ALL_ST_LibUsage"

  )


tribits_add_advanced_test( TribitsExampleProject_ALL_ST_LibUsage_LibPrefix
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  EXCLUDE_IF_NOT_TRUE ${PROJECT_NAME}_ENABLE_Fortran

  TEST_0
    MESSAGE "Do the initial configure to get the package enables"
      " and the  env probe in place."
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=ON
      -DTribitsExProj_ENABLE_WrapExternal=OFF
      -DTribitsExProj_ENABLE_ALL_PACKAGES=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      -DTribitsExProj_ENABLE_SECONDARY_TESTED_CODE=ON
      -DTribitsExProj_ENABLE_EXPORT_MAKEFILES=OFF
      -DTribitsExProj_ENABLE_INSTALL_CMAKE_CONFIG_FILES=OFF
      -DTribitsExProj_LIBRARY_NAME_PREFIX=tep_
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Final set of enabled packages:  SimpleCxx MixedLang WithSubpackages 3"
      "Final set of enabled SE packages:  SimpleCxx MixedLang WithSubpackagesA WithSubpackagesB WithSubpackagesC WithSubpackages 6"
      "Configuring done"
      "Generating done"
      "Build files have been written to: .*/TriBITS_TribitsExampleProject_ALL_ST_LibUsage_LibPrefix"

  #
  # Testing passing libs to tribits_add_library()
  #

  TEST_1
    MESSAGE "Show deprecated warning when trying to link lib from upstream SE package."
    CMND ${CMAKE_COMMAND}
    ARGS -DSPKB_SHOW_UPSTREAM_DEPLIBS_ERROR=ON
      .
    PASS_REGULAR_EXPRESSION_ALL
      "WARNING: 'simplecxx' in DEPLIBS is not a lib in this SE package"
      "packages/with_subpackages/b/src/CMakeLists.txt:.* [(]tribits_add_library[)]"
      "Generating done"
      "Build files have been written to: .*/TriBITS_TribitsExampleProject_ALL_ST_LibUsage_LibPrefix"

  TEST_2
    MESSAGE "Show deprecated warning when passing a lib from this SE package through IMPORTEDLIBS."
    CMND ${CMAKE_COMMAND}
    ARGS -DSPKB_SHOW_SE_PKG_LIB_IMPORTEDLIBS_ERROR=ON
      -DSPKB_SHOW_UPSTREAM_DEPLIBS_ERROR=
      .
    PASS_REGULAR_EXPRESSION_ALL
      "WARNING: Lib 'pws_b' in IMPORTEDLIBS is in this SE package "
      "packages/with_subpackages/b/tests/testlib/CMakeLists.txt:.* [(]tribits_add_library[)]"
      "Generating done"
      "Build files have been written to: .*/TriBITS_TribitsExampleProject_ALL_ST_LibUsage_LibPrefix"

  TEST_3
    MESSAGE "Show deprecated warning when passing a lib from upstream"
      " SE package through IMPORTEDLIBS."
    CMND ${CMAKE_COMMAND}
    ARGS -DSPKB_SHOW_UPSTREAM_SE_PKG_LIB_IMPORTEDLIBS_ERROR=ON
      -DSPKB_SHOW_SE_PKG_LIB_IMPORTEDLIBS_ERROR=
      .
    PASS_REGULAR_EXPRESSION_ALL
      "WARNING: Lib 'simplecxx' being passed through IMPORTEDLIBS"
      "TribitsExampleProject/packages/with_subpackages/b/cmake/Dependencies.cmake"
      "packages/with_subpackages/b/tests/testlib/CMakeLists.txt:.* [(]tribits_add_library[)]"
      "Generating done"
      "Build files have been written to: .*/TriBITS_TribitsExampleProject_ALL_ST_LibUsage_LibPrefix"

  TEST_4
    MESSAGE "Show deprecated warning when passing a TESTONLY lib through DEPLBIS."
    CMND ${CMAKE_COMMAND}
    ARGS -DSPKC_SHOW_TESTONLY_DEPLBIS_ERROR=ON
      -DSPKB_SHOW_UPSTREAM_SE_PKG_LIB_IMPORTEDLIBS_ERROR=
      .
    PASS_REGULAR_EXPRESSION_ALL
      "WARNING: 'b_mixed_lang' in DEPLIBS is a TESTONLY lib "
      "TribitsExampleProject/packages/with_subpackages/c/cmake/Dependencies.cmake"
      "packages/with_subpackages/c/CMakeLists.txt:.* [(]tribits_add_library[)]"
      "Generating done"
      "Build files have been written to: .*/TriBITS_TribitsExampleProject_ALL_ST_LibUsage_LibPrefix"

  TEST_5
    MESSAGE "Show deprecated warning when passing a TESTONLY lib through IMPORTEDLIBS."
    CMND ${CMAKE_COMMAND}
    ARGS -DSPKC_SHOW_TESTONLY_IMPORTEDLIBS_ERROR=ON
      -DSPKC_SHOW_TESTONLY_DEPLBIS_ERROR=
      .
    PASS_REGULAR_EXPRESSION_ALL
      "WARNING: 'b_mixed_lang' in IMPORTEDLIBS is a TESTONLY lib"
      "packages/with_subpackages/c/CMakeLists.txt:.* [(]tribits_add_library[)]"
      "Generating done"
      "Build files have been written to: .*/TriBITS_TribitsExampleProject_ALL_ST_LibUsage_LibPrefix"

  TEST_6
    MESSAGE "Show deprecated warning when passing m through DEPLIBS."
    CMND ${CMAKE_COMMAND}
    ARGS -DSPKB_SHOW_M_DEPLIBS_ERROR=ON
      -DSPKC_SHOW_TESTONLY_IMPORTEDLIBS_ERROR=
      .
    PASS_REGULAR_EXPRESSION_ALL
      "WARNING: 'm' in DEPLIBS is not a lib defined in the current cmake "
      "packages/with_subpackages/b/src/CMakeLists.txt:.* [(]tribits_add_library[)]"
      "Generating done"
      "Build files have been written to: .*/TriBITS_TribitsExampleProject_ALL_ST_LibUsage_LibPrefix"

  #
  # Testing passing libs to tribits_add_executable()
  #

  TEST_7
    MESSAGE "Show error when trying to link an INSTALLABLE exec against a TESTONLY lib."
    CMND ${CMAKE_COMMAND}
    ARGS -DSPKB_SHOW_TESTONLY_INSTALLABLE_ERROR=ON
      -DSPKB_SHOW_M_DEPLIBS_ERROR=
      .
    PASS_REGULAR_EXPRESSION_ALL
      "ERROR: TESTONLY lib 'b_test_utils' not allowed with INSTALLABLE executable"
      "packages/with_subpackages/b/tests/CMakeLists.txt:.* [(]tribits_add_executable_and_test[)]"
      "Configuring incomplete, errors occurred!"

  TEST_8
    MESSAGE "Show error when trying to link against non-TESTONLY lib."
    CMND ${CMAKE_COMMAND}
    ARGS -DSPKB_SHOW_NON_TESTONLY_LIB_ERROR=ON
      -DSPKB_SHOW_TESTONLY_INSTALLABLE_ERROR=
      .
    PASS_REGULAR_EXPRESSION_ALL
      " ERROR: 'simplecxx' in TESTONLYLIBS not a TESTONLY lib"
      "packages/with_subpackages/b/tests/CMakeLists.txt:.* [(]tribits_add_executable_and_test[)]"
      "Configuring incomplete, errors occurred!"

  TEST_9
    MESSAGE "Show error when trying to link SE package lib using TESTONLYLIBS"
    CMND ${CMAKE_COMMAND}
    ARGS -DSPKB_SHOW_IMPORTED_LIBS_THIS_PKG_ERROR=ON
      -DSPKB_SHOW_NON_TESTONLY_LIB_ERROR=
      .
    PASS_REGULAR_EXPRESSION_ALL
      "ERROR: Lib 'pws_b' in IMPORTEDLIBS is in this SE package"
      "packages/with_subpackages/b/tests/CMakeLists.txt:.* [(]tribits_add_executable_and_test[)]"
      "Configuring incomplete, errors occurred!"

  TEST_10
    MESSAGE "Show deprecated warning when trying to link TESTONLY lib using DEBLIBS."
    CMND ${CMAKE_COMMAND}
    ARGS -DSPKB_SHOW_TESTONLY_DEBLIBS_WARNING=ON
      -DSPKB_SHOW_IMPORTED_LIBS_THIS_PKG_ERROR=
      .
    PASS_REGULAR_EXPRESSION_ALL
      "WARNING: Passing TESTONLY lib 'b_mixed_lang' through DEPLIBS is deprecated"
      "packages/with_subpackages/b/tests/CMakeLists.txt:.* [(]tribits_add_executable_and_test[)]"
      "Generating done"
      "Build files have been written to: .*/TriBITS_TribitsExampleProject_ALL_ST_LibUsage_LibPrefix"

  TEST_11
    MESSAGE "Show deprecated warning when trying to link non-TESTONLY lib using DEBLIBS."
    CMND ${CMAKE_COMMAND}
    ARGS -DSPKB_SHOW_NONTESTONLY_DEBLIBS_WARNING=ON
      -DSPKB_SHOW_TESTONLY_DEBLIBS_WARNING=
      .
    PASS_REGULAR_EXPRESSION_ALL
      "WARNING: Passing non-TESTONLY lib 'pws_b' through DEPLIBS is deprecated"
      "packages/with_subpackages/b/tests/CMakeLists.txt:.* [(]tribits_add_executable_and_test[)]"
      "Generating done"
      "Build files have been written to: .*/TriBITS_TribitsExampleProject_ALL_ST_LibUsage_LibPrefix"

  )


tribits_add_advanced_test( TribitsExampleProject_SimpleCxx_DEBUG_int64
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  TEST_0 CMND ${CMAKE_COMMAND}
    MESSAGE "Do the initial configure"
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_DEBUG=ON
      -DTribitsExProj_ENABLE_SimpleCxx=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      -DHAVE_SIMPLECXX___INT64=ON
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Final set of enabled packages:  SimpleCxx 1"
      "Configuring done"
      "Generating done"
  TEST_1 CMND make
    MESSAGE "Build the default 'all' target using raw 'make'"
    ARGS ${CTEST_BUILD_FLAGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Built target simplecxx"
  TEST_2 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    MESSAGE "Run all the tests with raw 'ctest'"
    PASS_REGULAR_EXPRESSION_ALL
      "SimpleCxx_HelloWorldTests${TEST_MPI_1_SUFFIX} .* Passed"
      "100% tests passed, 0 tests failed out of 2"
  )


tribits_add_advanced_test( TribitsExampleProject_CONFIGURE_OPTIONS_FILE
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  TEST_0 CMND ${CMAKE_COMMAND}
    MESSAGE "Do the initial configure with no options file"
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Configuring done"
      "Generating done"
  TEST_1 CMND ${CMAKE_COMMAND}
    MESSAGE "Do the re-configure with user-defined configure options file"
    ARGS
      -DTribitsExProj_CONFIGURE_OPTIONS_FILE=${CMAKE_CURRENT_LIST_DIR}/ConfigOptions1.cmake
      .
    PASS_REGULAR_EXPRESSION_ALL
      "Reading in configuration options from .*/ConfigOptions1.cmake"
      "Included ConfigOptions1.cmake"
      "Generating done"
  TEST_2 CMND ${CMAKE_COMMAND}
    MESSAGE "Do the re-configure with configure options file append"
    ARGS
      -DTribitsExProj_CONFIGURE_OPTIONS_FILE=
      -DTribitsExProj_CONFIGURE_OPTIONS_FILE_APPEND=${CMAKE_CURRENT_LIST_DIR}/ConfigOptions2.cmake
      .
    PASS_REGULAR_EXPRESSION_ALL
      "Reading in configuration options from .*/ConfigOptions2.cmake"
      "Included ConfigOptions2.cmake"
      "Generating done"
  TEST_3 CMND ${CMAKE_COMMAND}
    MESSAGE "Do the re-configure with configure options file and append"
    ARGS
      -DTribitsExProj_CONFIGURE_OPTIONS_FILE=${CMAKE_CURRENT_LIST_DIR}/ConfigOptions1.cmake
      -DTribitsExProj_CONFIGURE_OPTIONS_FILE_APPEND=${CMAKE_CURRENT_LIST_DIR}/ConfigOptions2.cmake
      .
    PASS_REGULAR_EXPRESSION_ALL
      "Reading in configuration options from .*/ConfigOptions1.cmake"
      "Reading in configuration options from .*/ConfigOptions2.cmake"
      "Included ConfigOptions1.cmake"
      "Included ConfigOptions2.cmake"
      "Generating done"
  TEST_4 CMND ${CMAKE_COMMAND}
    MESSAGE "Do the re-configure with two user configure options files"
    ARGS
      -DTribitsExProj_CONFIGURE_OPTIONS_FILE=${CMAKE_CURRENT_LIST_DIR}/ConfigOptions1.cmake,${CMAKE_CURRENT_LIST_DIR}/ConfigOptions2.cmake
      -DTribitsExProj_CONFIGURE_OPTIONS_FILE_APPEND=
      .
    PASS_REGULAR_EXPRESSION_ALL
      "Reading in configuration options from .*/ConfigOptions1.cmake"
      "Reading in configuration options from .*/ConfigOptions2.cmake"
      "Included ConfigOptions1.cmake"
      "Included ConfigOptions2.cmake"
      "Generating done"
  )


tribits_add_advanced_test( TribitsExampleProject_SKIP_CTEST_ADD_TEST_Project
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0 CMND ${CMAKE_COMMAND}
    MESSAGE "Do the initial configure with TribitsExProj_SKIP_CTEST_ADD_TEST=ON"
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_ALL_PACKAGES=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      -DTribitsExProj_TRACE_ADD_TEST=ON
      -DTribitsExProj_SKIP_CTEST_ADD_TEST=ON
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Final set of enabled packages:  SimpleCxx WithSubpackages 2"
      "Final set of enabled SE packages:  SimpleCxx WithSubpackagesA WithSubpackages 3"
      "SimpleCxx_HelloWorldTests: NOT added test because SimpleCxx_SKIP_CTEST_ADD_TEST='ON'[!]"
      "SimpleCxx_HelloWorldProg: NOT added test because SimpleCxx_SKIP_CTEST_ADD_TEST='ON'[!]"
      "WithSubpackagesA_test_of_a: NOT added test because WithSubpackages_SKIP_CTEST_ADD_TEST='ON'[!]"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_1 CMND make ARGS ${CTEST_BUILD_FLAGS}
    MESSAGE "Build the default 'all' target using raw 'make'"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_2 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    MESSAGE "Run all the tests with raw 'ctest'"
    PASS_REGULAR_EXPRESSION_ALL
      "No tests were found"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  )


tribits_add_advanced_test( TribitsExampleProject_SKIP_CTEST_ADD_TEST_Package_Whitelist
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0 CMND ${CMAKE_COMMAND}
    MESSAGE "Do the initial configure with TribitsExProj_SKIP_CTEST_ADD_TEST=ON"
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_ALL_PACKAGES=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      -DTribitsExProj_TRACE_ADD_TEST=ON
      -DSimpleCxx_SKIP_CTEST_ADD_TEST=ON
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Final set of enabled packages:  SimpleCxx WithSubpackages 2"
      "Final set of enabled SE packages:  SimpleCxx WithSubpackagesA WithSubpackages 3"
      "SimpleCxx_HelloWorldTests: NOT added test because SimpleCxx_SKIP_CTEST_ADD_TEST='ON'[!]"
      "SimpleCxx_HelloWorldProg: NOT added test because SimpleCxx_SKIP_CTEST_ADD_TEST='ON'[!]"
      "WithSubpackagesA_test_of_a: Added test [(]BASIC, .*PROCESSORS=1[)][!]"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_1 CMND make ARGS ${CTEST_BUILD_FLAGS}
    MESSAGE "Build the default 'all' target using raw 'make'"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_2 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    MESSAGE "Run all the tests with raw 'ctest'"
    PASS_REGULAR_EXPRESSION_ALL
      "1/1 Test #1: WithSubpackagesA_test_of_a .* Passed"
      "100% tests passed, 0 tests failed out of 1"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  )


tribits_add_advanced_test( TribitsExampleProject_SKIP_CTEST_ADD_TEST_Package_Blacklist
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0 CMND ${CMAKE_COMMAND}
    MESSAGE "Do the initial configure with TribitsExProj_SKIP_CTEST_ADD_TEST=ON"
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_ALL_PACKAGES=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      -DTribitsExProj_TRACE_ADD_TEST=ON
      -DTribitsExProj_SKIP_CTEST_ADD_TEST=ON
      -DSimpleCxx_SKIP_CTEST_ADD_TEST=OFF
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Final set of enabled packages:  SimpleCxx WithSubpackages 2"
      "Final set of enabled SE packages:  SimpleCxx WithSubpackagesA WithSubpackages 3"
      "SimpleCxx_HelloWorldTests.*: Added test [(]BASIC, .*PROCESSORS=1[)][!]"
      "SimpleCxx_HelloWorldProg.*: Added test [(]BASIC, .*PROCESSORS=1[)][!]"
      "WithSubpackagesA_test_of_a: NOT added test because WithSubpackages_SKIP_CTEST_ADD_TEST='ON'[!]"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_1 CMND make ARGS ${CTEST_BUILD_FLAGS}
    MESSAGE "Build the default 'all' target using raw 'make'"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_2 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    MESSAGE "Run all the tests with raw 'ctest'"
    PASS_REGULAR_EXPRESSION_ALL
      "1/2 Test #1: SimpleCxx_HelloWorldTests.* .* Passed"
      "2/2 Test #2: SimpleCxx_HelloWorldProg.* .* Passed"
      "100% tests passed, 0 tests failed out of 2"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  )


tribits_add_advanced_test( TribitsExampleProject_WrapExternal
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  EXCLUDE_IF_NOT_TRUE ${PROJECT_NAME}_ENABLE_Fortran
  XHOSTTYPE "Darwin"

  TEST_0
    MESSAGE "Copy TribitsExampleProject so that we can modify it."
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject .

  TEST_1 CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_DEBUG=OFF
      -DTribitsExProj_ENABLE_EXPORT_MAKEFILES=OFF
      -DTribitsExProj_ENABLE_INSTALL_CMAKE_CONFIG_FILES=OFF
      -DTribitsExProj_ENABLE_WrapExternal=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Explicitly enabled packages on input .by user.:  WrapExternal 1"
      "Explicitly disabled packages on input .by user or by default.:  0"
      "Setting TribitsExProj_ENABLE_WithSubpackagesA=ON because WrapExternal has a required dependence on WithSubpackagesA"
      "Setting TribitsExProj_ENABLE_MixedLang=ON because WrapExternal has an optional dependence on MixedLang"
      "Setting TribitsExProj_ENABLE_SimpleCxx=ON because WithSubpackagesA has a required dependence on SimpleCxx"
      "Final set of enabled packages:  SimpleCxx MixedLang WithSubpackages WrapExternal 4"
      "Final set of enabled SE packages:  SimpleCxx MixedLang WithSubpackagesA WithSubpackages WrapExternal 5"
      "Final set of non-enabled packages:  0"
      "Final set of non-enabled SE packages:  WithSubpackagesB WithSubpackagesC 2"
      "This package has no unfiltered binary files so consider out of date"
      "Configuring done"
      "Generating done"
      "Build files have been written to: .*ExamplesUnitTests/TriBITS_TribitsExampleProject_WrapExternal"
  TEST_2 CMND make ARGS ${CTEST_BUILD_FLAGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Built target WrapExternal_run_external_func"
  TEST_3 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    PASS_REGULAR_EXPRESSION_ALL
      "WrapExternal_run_external_func${TEST_MPI_1_SUFFIX} .* Passed"
      "100% tests passed, 0 tests failed out of 1"

  TEST_4 CMND sleep ARGS 1s
     MESSAGE "Sleep for 1 sec for systems were time stamps are only accurate to 1 sec"
  TEST_5 CMND touch
     ARGS TribitsExampleProject/packages/with_subpackages/a/A.cpp
     MESSAGE "Test that changing upstream source will trigger rebuild"
  TEST_6 CMND ${CMAKE_COMMAND} ARGS TribitsExampleProject
      -DWrapExternal_SHOW_MOST_RECENT_FILES=TRUE
     MESSAGE "Recofigure with changed upstream source"
    PASS_REGULAR_EXPRESSION_ALL
      "Most recent file in ./packages/with_subpackages/ is ./a/A.cpp"
      "Overall most recent modified file is in ./packages/with_subpackages/ and is ./a/A.cpp"
      "The upstream SE package source file ./a/A.cpp is more recent than this package's binary file ./WrapExternal_run_external_func.exe"
      "Blowing away WrapExternal build dir external_func/ so it will build from scratch"
  TEST_7 CMND make ARGS ${CTEST_BUILD_FLAGS}
    MESSAGE "Rebuild only exteranl_func"
    PASS_REGULAR_EXPRESSION_ALL
      "Built target simplecxx"
      "Built target mixedlang"
      "Built target pws_a"
      "Generating external_func/libexternal_func.a"
      "Linking CXX executable WrapExternal_run_external_func.exe"

  TEST_8 CMND sleep ARGS 1s
     MESSAGE "Sleep for 1 sec for systems were time stamps are only accurate to 1 sec"
  TEST_9 CMND ${CMAKE_COMMAND}
     ARGS  -DSimpleCxx_ENABLE_DEBUG=ON  -DWrapExternal_SHOW_MOST_RECENT_FILES=FALSE
       TribitsExampleProject
     MESSAGE "Recofigure changing the debug mode to trigger rebuild"
    PASS_REGULAR_EXPRESSION_ALL
      "The upstream SE package binary file ./src/SimpleCxx_config.h is more recent than this package's binary file ./WrapExternal_run_external_func.exe"
      "Blowing away WrapExternal build dir external_func/ so it will build from scratch"
  TEST_10 CMND make ARGS ${CTEST_BUILD_FLAGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Generating external_func/libexternal_func.a"
      "Linking CXX executable WrapExternal_run_external_func.exe"

  TEST_11 CMND sleep ARGS 1s
     MESSAGE "Sleep for 1 sec for systems were time stamps are only accurate to 1 sec"
  TEST_12 CMND touch
     ARGS TribitsExampleProject/packages/wrap_external/external_func/configure.py
     MESSAGE "Test that changing the external file will trigger rebuild"
  TEST_13 CMND ${CMAKE_COMMAND} ARGS TribitsExampleProject
     MESSAGE "Recofigure with changes external file"
    PASS_REGULAR_EXPRESSION_ALL
      "The this package's source file ./external_func/configure.py is more recent than this package's binary file ./WrapExternal_run_external_func.exe"
      "Blowing away WrapExternal build dir external_func/ so it will build from scratch"
  TEST_14 CMND make ARGS ${CTEST_BUILD_FLAGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Generating external_func/libexternal_func.a"
      "Linking CXX executable WrapExternal_run_external_func.exe"

  TEST_15 CMND ${CMAKE_COMMAND} ARGS TribitsExampleProject
     MESSAGE "Recofigure with no changes that will not do anything"
    PASS_REGULAR_EXPRESSION_ALL
      "This package's most recent binary file ./WrapExternal_run_external_func.exe is more recent than its upstream SE package source or binary files or this package's source files"
  TEST_16 CMND make ARGS ${CTEST_BUILD_FLAGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Built target build_external_func"
      "Built target WrapExternal_run_external_func"

  )


tribits_add_advanced_test( TribitsExampleProject_ALL_NoFortran_WrapExternal_VerboseConfigure
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Do a verbose configure and check that the packages coupling variables are correct."
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_ENABLE_DEBUG=OFF
      -DTribitsExProj_ENABLE_EXPORT_MAKEFILES=OFF
      -DTribitsExProj_ENABLE_INSTALL_CMAKE_CONFIG_FILES=OFF
      -DTribitsExProj_ENABLE_ALL_PACKAGES=ON
      -DTribitsExProj_ENABLE_SECONDARY_TESTED_CODE=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      -DTribitsExProj_VERBOSE_CONFIGURE=ON
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Final set of enabled packages:  SimpleCxx WithSubpackages WrapExternal 3"
      "Final set of enabled SE packages:  SimpleCxx WithSubpackagesA WithSubpackagesB WithSubpackagesC WithSubpackages WrapExternal 6"

      "HeaderOnlyTpl_INCLUDE_DIRS='.+/examples/tpls/HeaderOnlyTpl'"
      "-- TPL_HeaderOnlyTpl_INCLUDE_DIRS='.+/examples/tpls/HeaderOnlyTpl'"

      "SimpleCxx_INCLUDE_DIRS='.+/TriBITS_TribitsExampleProject_ALL_NoFortran_WrapExternal_VerboseConfigure[;].+/TriBITS_TribitsExampleProject_ALL_NoFortran_WrapExternal_VerboseConfigure/packages/simple_cxx/src[;].+/TribitsExampleProject/packages/simple_cxx/src[;].+/examples/tpls/HeaderOnlyTpl'"
      "SimpleCxx_LIBRARY_DIRS='.+/packages/simple_cxx/src'"
      "SimpleCxx_LIBRARIES='simplecxx'"

      "WithSubpackagesA_INCLUDE_DIRS='.+/TriBITS_TribitsExampleProject_ALL_NoFortran_WrapExternal_VerboseConfigure[;].+/TribitsExampleProject/packages/with_subpackages/a[;].+/TriBITS_TribitsExampleProject_ALL_NoFortran_WrapExternal_VerboseConfigure/packages/simple_cxx/src[;].+/TribitsExampleProject/packages/simple_cxx/src[;].+/examples/tpls/HeaderOnlyTpl'"
      "WithSubpackagesA_LIBRARY_DIRS='.+/packages/with_subpackages/a[;].+/packages/simple_cxx/src'"
      "WithSubpackagesA_LIBRARIES='pws_a'"

      "b_test_utils_INCLUDE_DIRS='.+/TriBITS_TribitsExampleProject_ALL_NoFortran_WrapExternal_VerboseConfigure[;].+/TriBITS_TribitsExampleProject_ALL_NoFortran_WrapExternal_VerboseConfigure/packages/with_subpackages/b/src[;].+/TribitsExampleProject/packages/with_subpackages/b/src[;].+/TribitsExampleProject/packages/with_subpackages/a[;].+/TriBITS_TribitsExampleProject_ALL_NoFortran_WrapExternal_VerboseConfigure/packages/simple_cxx/src[;].+/TribitsExampleProject/packages/simple_cxx/src[;].+/examples/tpls/HeaderOnlyTpl[;].+/TribitsExampleProject/packages/with_subpackages/b/tests/testlib'"

      "WithSubpackagesB_INCLUDE_DIRS='.+/TriBITS_TribitsExampleProject_ALL_NoFortran_WrapExternal_VerboseConfigure[;].+/TriBITS_TribitsExampleProject_ALL_NoFortran_WrapExternal_VerboseConfigure/packages/with_subpackages/b/src[;].+/TribitsExampleProject/packages/with_subpackages/b/src[;].+/TribitsExampleProject/packages/with_subpackages/a[;].+/TriBITS_TribitsExampleProject_ALL_NoFortran_WrapExternal_VerboseConfigure/packages/simple_cxx/src[;].+/TribitsExampleProject/packages/simple_cxx/src[;].+/examples/tpls/HeaderOnlyTpl'"
      "WithSubpackagesB_LIBRARY_DIRS='.+/TriBITS_TribitsExampleProject_ALL_NoFortran_WrapExternal_VerboseConfigure/packages/with_subpackages/b/src;.+/TriBITS_TribitsExampleProject_ALL_NoFortran_WrapExternal_VerboseConfigure/packages/with_subpackages/a;.+/TriBITS_TribitsExampleProject_ALL_NoFortran_WrapExternal_VerboseConfigure/packages/simple_cxx/src'"
      "WithSubpackagesB_LIBRARIES='pws_b'"

      "WithSubpackagesC_INCLUDE_DIRS='.+/TriBITS_TribitsExampleProject_ALL_NoFortran_WrapExternal_VerboseConfigure[;].+/TriBITS_TribitsExampleProject_ALL_NoFortran_WrapExternal_VerboseConfigure/packages/with_subpackages/b/src[;].+/TribitsExampleProject/packages/with_subpackages/b/src[;].+/TribitsExampleProject/packages/with_subpackages/a[;].+/TriBITS_TribitsExampleProject_ALL_NoFortran_WrapExternal_VerboseConfigure/packages/simple_cxx/src[;].+/TribitsExampleProject/packages/simple_cxx/src[;].+/examples/tpls/HeaderOnlyTpl[;].+/TribitsExampleProject/packages/with_subpackages/c'"
      "WithSubpackagesC_LIBRARY_DIRS='.+/TriBITS_TribitsExampleProject_ALL_NoFortran_WrapExternal_VerboseConfigure/packages/with_subpackages/b/src[;].+/TriBITS_TribitsExampleProject_ALL_NoFortran_WrapExternal_VerboseConfigure/packages/with_subpackages/a[;].+/TriBITS_TribitsExampleProject_ALL_NoFortran_WrapExternal_VerboseConfigure/packages/simple_cxx/src[;].+/TriBITS_TribitsExampleProject_ALL_NoFortran_WrapExternal_VerboseConfigure/packages/with_subpackages/c'"
      "WithSubpackagesC_LIBRARIES='pws_c'"

      "WithSubpackages_INCLUDE_DIRS='.+/TriBITS_TribitsExampleProject_ALL_NoFortran_WrapExternal_VerboseConfigure[;].+/TriBITS_TribitsExampleProject_ALL_NoFortran_WrapExternal_VerboseConfigure/packages/with_subpackages/b/src[;].+/TribitsExampleProject/packages/with_subpackages/b/src[;].+/TribitsExampleProject/packages/with_subpackages/a[;].+/TriBITS_TribitsExampleProject_ALL_NoFortran_WrapExternal_VerboseConfigure/packages/simple_cxx/src[;].+/TribitsExampleProject/packages/simple_cxx/src[;].+/examples/tpls/HeaderOnlyTpl[;].+/TribitsExampleProject/packages/with_subpackages/c'"
      "WithSubpackages_LIBRARY_DIRS='.+/TriBITS_TribitsExampleProject_ALL_NoFortran_WrapExternal_VerboseConfigure/packages/with_subpackages/b/src[;].+/TriBITS_TribitsExampleProject_ALL_NoFortran_WrapExternal_VerboseConfigure/packages/with_subpackages/a[;].+/TriBITS_TribitsExampleProject_ALL_NoFortran_WrapExternal_VerboseConfigure/packages/simple_cxx/src[;].+/TriBITS_TribitsExampleProject_ALL_NoFortran_WrapExternal_VerboseConfigure/packages/with_subpackages/c'"
      "WithSubpackages_LIBRARIES='pws_c.pws_b.pws_a'"

      "WrapExternal_INCLUDE_DIRS='.+/packages/wrap_external/external_func'"
      "WrapExternal_LIBRARY_DIRS=''"
      "WrapExternal_LIBRARIES='external_func.pws_a'"

      "pws_b_TARGET_NAME='pws_b'"
      "b_test_TARGET_NAME='WithSubpackagesB_b_test'"
      "test_of_b_TEST_NAME='WithSubpackagesB_test_of_b'"
      "c_util_TEST_NAME='WithSubpackagesC_test_of_c_util${TEST_MPI_1_SUFFIX}'"

      "-- simplecxx:LINK_LIBS=''"
      "-- HelloWorldTests:LINK_LIBS='simplecxx'"
      "-- pws_a:LINK_LIBS='simplecxx'"
      "-- a_test:LINK_LIBS='pws_a'"
      "-- pws_b:LINK_LIBS='pws_a[;]simplecxx'"
      "-- b_test:LINK_LIBS='pws_b'"
      "-- c_util:LINK_LIBS='pws_b[;]pws_a'"
      "-- pws_c:LINK_LIBS='pws_b[;]pws_a'"
      "-- c_test:LINK_LIBS='pws_c'"
      "-- run_external_func:LINK_LIBS='external_func[;]pws_a'"

  )


tribits_add_advanced_test( TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  XHOSTTYPE Darwin

  TEST_0
    MESSAGE "Copy TribitsExampleProject so that we can modify it."
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject .

  TEST_1
    MESSAGE "Copy the with_subpackages package dir to base dir."
    CMND cp
    ARGS -r TribitsExampleProject/packages/with_subpackages/
      TribitsExampleProject/.

  TEST_2
    MESSAGE "Remove the packages/with_subpackages package dir."
    CMND rm
    ARGS -r TribitsExampleProject/packages/with_subpackages/

  TEST_3
    MESSAGE "Override with_packages/ source dir and configure"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_ENABLE_DEBUG=OFF
      -DTribitsExProj_ENABLE_EXPORT_MAKEFILES=OFF
      -DTribitsExProj_ENABLE_INSTALL_CMAKE_CONFIG_FILES=OFF
      -DTribitsExProj_ENABLE_ALL_PACKAGES=ON
      -DTribitsExProj_ENABLE_SECONDARY_TESTED_CODE=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      -DTribitsExProj_VERBOSE_CONFIGURE=ON
      -DWithSubpackages_SOURCE_DIR_OVERRIDE=with_subpackages
      TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Final set of enabled packages:  SimpleCxx WithSubpackages WrapExternal 3"
      "Final set of enabled SE packages:  SimpleCxx WithSubpackagesA WithSubpackagesB WithSubpackagesC WithSubpackages WrapExternal 6"
      "-- NOTE: WithSubpackages_SOURCE_DIR_OVERRIDE='with_subpackages' is overriding default path 'packages/with_subpackages'"
      "-- File Trace: PACKAGE    INCLUDE    .*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/TribitsExampleProject/with_subpackages/cmake/Dependencies[.]cmake"
      "-- File Trace: PACKAGE    INCLUDE    .*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/TribitsExampleProject/with_subpackages/a/cmake/Dependencies[.]cmake"
      "-- File Trace: PACKAGE    INCLUDE    .*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/TribitsExampleProject/with_subpackages/b/cmake/Dependencies[.]cmake"
      "-- File Trace: PACKAGE    INCLUDE    .*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/TribitsExampleProject/with_subpackages/c/cmake/Dependencies[.]cmake"
      "-- WithSubpackages_BINARY_DIR='.*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/with_subpackages'"
      "-- WithSubpackages_SOURCE_DIR='.*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/TribitsExampleProject/with_subpackages'"
      "-- WithSubpackages_BINARY_DIR='.*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/with_subpackages'"
      "-- File Trace: PACKAGE    ADD_SUBDIR .*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/TribitsExampleProject/with_subpackages/CMakeLists[.]txt"
      "-- File Trace: PACKAGE    ADD_SUBDIR .*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/TribitsExampleProject/with_subpackages/a/CMakeLists[.]txt"
      "-- File Trace: PACKAGE    ADD_SUBDIR .*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/TribitsExampleProject/with_subpackages/a/tests/CMakeLists[.]txt"

      "-- WithSubpackagesA_INCLUDE_DIRS='.+/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir[;].+/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/TribitsExampleProject/with_subpackages/a[;].+/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/packages/simple_cxx/src[;].+/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/TribitsExampleProject/packages/simple_cxx/src[;].+/examples/tpls/HeaderOnlyTpl'"

      "-- File Trace: PACKAGE    ADD_SUBDIR .*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/TribitsExampleProject/with_subpackages/b/CMakeLists[.]txt"
      "-- File Trace: PACKAGE    ADD_SUBDIR .*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/TribitsExampleProject/with_subpackages/b/tests/CMakeLists[.]txt"

      "-- WithSubpackagesB_INCLUDE_DIRS='.+/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir[;].+/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/with_subpackages/b/src[;].+/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/TribitsExampleProject/with_subpackages/b/src[;].+/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/TribitsExampleProject/with_subpackages/a[;].+/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/packages/simple_cxx/src[;].+/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/TribitsExampleProject/packages/simple_cxx/src[;].+/examples/tpls/HeaderOnlyTpl'"
      "-- WithSubpackagesB_LIBRARY_DIRS='.*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/with_subpackages/b/src[;].*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/with_subpackages/a[;].*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/packages/simple_cxx/src'"

      "-- File Trace: PACKAGE    ADD_SUBDIR .*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/TribitsExampleProject/with_subpackages/c/CMakeLists[.]txt"
      "-- File Trace: PACKAGE    ADD_SUBDIR .*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/TribitsExampleProject/with_subpackages/c/tests/CMakeLists[.]txt"

      "-- WithSubpackagesC_INCLUDE_DIRS='.*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir[;].*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/with_subpackages/b/src[;].*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/TribitsExampleProject/with_subpackages/b/src[;].*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/TribitsExampleProject/with_subpackages/a[;].*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/packages/simple_cxx/src[;].*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/TribitsExampleProject/packages/simple_cxx/src[;].*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/TribitsExampleProject/with_subpackages/c'"
      "-- WithSubpackagesC_LIBRARY_DIRS='.*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/with_subpackages/b/src[;].*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/with_subpackages/a[;].*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/packages/simple_cxx/src[;].*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/with_subpackages/c'"

     "-- WithSubpackages_INCLUDE_DIRS='.+/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir;.+/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/with_subpackages/b/src;.+/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/TribitsExampleProject/with_subpackages/b/src;.+/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/TribitsExampleProject/with_subpackages/a;.+/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/packages/simple_cxx/src;.+/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/TribitsExampleProject/packages/simple_cxx/src;.+/examples/tpls/HeaderOnlyTpl;.+/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/TribitsExampleProject/with_subpackages/c'"
      "-- WithSubpackages_LIBRARY_DIRS='.*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/with_subpackages/b/src[;].*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/with_subpackages/a[;].*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/packages/simple_cxx/src[;].*/TriBITS_TribitsExampleProject_ALL_NoFortran_OverridePackageSourceDir/with_subpackages/c'"

  TEST_4 CMND make
    ARGS ${CTEST_BUILD_FLAGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Built target WithSubpackagesC_c_test"

  TEST_5 CMND ${CMAKE_CTEST_COMMAND}
    PASS_REGULAR_EXPRESSION_ALL
      "100% tests passed, 0 tests failed out of 7"

  )


tribits_add_advanced_test( TribitsExampleProject_HeaderOnlyTpl_FailThenPass
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Do the initial configure with a bad TPL find path"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_ENABLE_SimpleCxx=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      #-DTribitsExProj_VERBOSE_CONFIGURE=ON
      -DHeaderOnlyTpl_INCLUDE_DIRS=/path_does_not_exist
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Processing enabled TPL: HeaderOnlyTpl .enabled by SimpleCxx, disable with -DTPL_ENABLE_HeaderOnlyTpl=OFF."
      "-- Searching for headers in HeaderOnlyTpl_INCLUDE_DIRS='/path_does_not_exist'"
      "-- TIP: If the TPL 'HeaderOnlyTpl' is on your system then you can set:"
      "-DHeaderOnlyTpl_INCLUDE_DIRS='<dir0>[;]<dir1>[;]...'"
      "-DTPL_HeaderOnlyTpl_INCLUDE_DIRS='<dir0>[;]<dir1>[;]...'"
      "-- ERROR: Failed finding all of the parts of TPL 'HeaderOnlyTpl' .see above., Aborting!"
      "-- NOTE: The find module file for this failed TPL 'HeaderOnlyTpl' is:"
      "     .*/TribitsExampleProject/cmake/tpls/FindTPLHeaderOnlyTpl.cmake"
      "   which is pointed to in the file:"
      "     .*/TribitsExampleProject/TPLsList.cmake"
      "TIP: One way to get past the configure failure for the"
      "TPL 'HeaderOnlyTpl' is to simply disable it with:"
      "  -DTPL_ENABLE_HeaderOnlyTpl=OFF"
      "which will disable it and will recursively disable all of the"
      "downstream packages that have required dependencies on it, including"
      "the package 'SimpleCxx' which triggered its enable."
      "When you reconfigure, just grep the cmake stdout for 'HeaderOnlyTpl'"
      "and then follow the disables that occur as a result to see what impact"
      "this TPL disable has on the configuration of TribitsExProj."
      "CMake Error at .+/TribitsProcessEnabledTpl[.]cmake:[0-9]+ [(]message[)]:"
      "  ERROR: TPL_HeaderOnlyTpl_NOT_FOUND=TRUE, aborting!"
      "Call Stack .most recent call first.:"
      "-- Configuring incomplete, errors occurred!"

  TEST_1
    MESSAGE "Reconfigure now fining the TPL correctly"
    CMND ${CMAKE_COMMAND}
    ARGS
      -DHeaderOnlyTpl_INCLUDE_DIRS=${${PROJECT_NAME}_TRIBITS_DIR}/examples/tpls/HeaderOnlyTpl
      #-DTribitsExProj_VERBOSE_CONFIGURE=ON
      .
    PASS_REGULAR_EXPRESSION_ALL
      "Processing enabled TPL: HeaderOnlyTpl .enabled by SimpleCxx, disable with -DTPL_ENABLE_HeaderOnlyTpl=OFF."
      "-- Searching for headers in HeaderOnlyTpl_INCLUDE_DIRS='.*/tribits/examples/tpls/HeaderOnlyTpl'"
      "Found header '.*/tribits/examples/tpls/HeaderOnlyTpl/HeaderOnlyTpl_stuff.hpp'"
      "Found TPL 'HeaderOnlyTpl' include dirs '.*/tribits/examples/tpls/HeaderOnlyTpl'"
      "TPL_HeaderOnlyTpl_INCLUDE_DIRS='.*/tribits/examples/tpls/HeaderOnlyTpl'"
      "Configuring done"
      "Generating done"

  )


tribits_add_advanced_test( TribitsExampleProject_HeaderOnlyTpl_HardEnable_Fail
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Do the initial configure with a bad TPL find path"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_ENABLE_SimpleCxx=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      #-DTribitsExProj_VERBOSE_CONFIGURE=ON
      -DTPL_ENABLE_HeaderOnlyTpl=ON
      -DHeaderOnlyTpl_INCLUDE_DIRS=/path_does_not_exist
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Processing enabled TPL: HeaderOnlyTpl .enabled explicitly, disable with -DTPL_ENABLE_HeaderOnlyTpl=OFF."
      "TIP: Even though the TPL 'HeaderOnlyTpl' was explicitly enabled in input,"
      "it can be disabled with:"
      "  -DTPL_ENABLE_HeaderOnlyTpl=OFF"
      "which will disable it and will recursively disable all of the"
      "downstream packages that have required dependencies on it."
      "When you reconfigure, just grep the cmake stdout for 'HeaderOnlyTpl'"
      "and then follow the disables that occur as a result to see what impact"
      "this TPL disable has on the configuration of TribitsExProj."
      "-- ERROR: Failed finding all of the parts of TPL 'HeaderOnlyTpl' .see above., Aborting!"
      "CMake Error at .+/TribitsProcessEnabledTpl[.]cmake:[0-9]+ [(]message[)]:"
      "  ERROR: TPL_HeaderOnlyTpl_NOT_FOUND=TRUE, aborting!"
      "Call Stack .most recent call first.:"
      "-- Configuring incomplete, errors occurred!"
  )


tribits_add_advanced_test( TribitsExampleProject_InsertedPkg
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  XHOSTTYPE Darwin

  TEST_0
    MESSAGE "Copy TribitsExampleProject so that we can copy in ExteranlPkg."
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject .

  TEST_1
    MESSAGE "Configure to get the compiler options"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_ENABLE_DEBUG=OFF
      TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Configuring done"
      "Generating done"

  TEST_2
    MESSAGE "Configure asserting existence of missing InsertedPkg"
    CMND ${CMAKE_COMMAND}
    ARGS
      -DInsertedPkg_ALLOW_MISSING_EXTERNAL_PACKAGE=FALSE
      .
    PASS_REGULAR_EXPRESSION_ALL
      "Error, the package InsertedPkg directory .+/TribitsExampleProject/InsertedPkg does not exist!"
      "CMake Error at .+/TribitsProcessPackagesAndDirsLists.cmake:[0-9]+ [(]message[)]:"
      "Configuring incomplete, errors occurred!"

  TEST_3
    MESSAGE "Copy TargetDefinesPkg to base dir."
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/InsertedPkg
      TribitsExampleProject/.


  TEST_4
    MESSAGE "Configure all packages"
    CMND ${CMAKE_COMMAND}
    ARGS
      -DTribitsExProj_ENABLE_ALL_PACKAGES=ON
      -DTribitsExProj_ENABLE_SECONDARY_TESTED_CODE=ON
      -DTribitsExProj_ENABLE_TESTS=ON
     .
    PASS_REGULAR_EXPRESSION_ALL
      "Setting TribitsExProj_ENABLE_InsertedPkg=ON"
      "Final set of enabled packages:  SimpleCxx InsertedPkg .+"
      "Final set of enabled SE packages:  SimpleCxx InsertedPkg .+"
      "Configuring done"
      "Generating done"

  TEST_5 CMND make
    ARGS ${CTEST_BUILD_FLAGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Built target externalpkg"
      "Linking CXX executable InsertedPkg_test.exe"

  TEST_6 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    PASS_REGULAR_EXPRESSION_ALL
      "InsertedPkg_test${TEST_MPI_1_SUFFIX} [.]+   Passed"
      "100% tests passed, 0 tests failed out of"

  # ToDo: Add usage of InsertedPkg in downstream package.

  )


tribits_add_advanced_test( TribitsExampleProject_TargetDefinesPkg
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Copy TribitsExampleProject so that we can copy in TargetDefinesPkg."
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject .

  TEST_1
    MESSAGE "Configure to get the compiler options"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_ENABLE_DEBUG=OFF
      TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Configuring done"
      "Generating done"

  TEST_2
    MESSAGE "Copy TargetDefinesPkg to base dir."
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TargetDefinesPkg
      TribitsExampleProject/.

  TEST_3
    MESSAGE "Configure just TargetDefinesPkg"
    CMND ${CMAKE_COMMAND}
    ARGS
      -DTribitsExProj_EXTRA_REPOSITORIES=TargetDefinesPkg
      -DTribitsExProj_ENABLE_TargetDefinesPkg=ON
      -DTribitsExProj_ENABLE_TESTS=ON
     .
    PASS_REGULAR_EXPRESSION_ALL
      "WARNING: Passing extra defines through 'DEFINES'"
      "Final set of enabled packages:  TargetDefinesPkg 1"
      "Final set of enabled SE packages:  TargetDefinesPkg 1"
      "Configuring done"
      "Generating done"

  TEST_4 CMND make
    ARGS ${CTEST_BUILD_FLAGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Built target targetdefinespkg"
      "Linking CXX executable TargetDefinesPkg_testcasedefault1"
      "Linking CXX executable TargetDefinesPkg_testcase_deprecated_default2"

  TEST_5 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    PASS_REGULAR_EXPRESSION_ALL
      "TargetDefinesPkg_testcasedefault1.* Passed"
      "TargetDefinesPkg_testcase_deprecated_default2.* Passed"
      "100% tests passed, 0 tests failed out of 8"

  )


tribits_add_advanced_test( TribitsExampleProject_MixedSharedStaticLibs_shared
  OVERALL_WORKING_DIRECTORY TEST_NAME
  EXCLUDE_IF_NOT_TRUE IS_REAL_LINUX_SYSTEM
  OVERALL_NUM_MPI_PROCS 1
  XHOSTTYPE Darwin

  TEST_0
    MESSAGE "Copy TribitsExampleProject so that we can copy in MixedSharedStaticLibs."
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject .

  TEST_1
    MESSAGE "Configure to get the compiler options"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DBUILD_SHARED_LIBS=ON
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_ENABLE_DEBUG=OFF
      TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "BUILD_SHARED_LIBS=.ON."
      "Configuring done"
      "Generating done"

  TEST_2
    MESSAGE "Copy MixedSharedStaticLibs to base dir."
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/MixedSharedStaticLibs
      TribitsExampleProject/.

  TEST_3
    MESSAGE "Configure SimpleCxx and MixedSharedStaticLibs"
    CMND ${CMAKE_COMMAND}
    ARGS
      -DTribitsExProj_EXTRA_REPOSITORIES=MixedSharedStaticLibs
      -DTribitsExProj_ENABLE_SimpleCxx=ON
      -DTribitsExProj_ENABLE_MixedSharedStaticLibs=ON
      -DTribitsExProj_ENABLE_TESTS=ON
     .
    PASS_REGULAR_EXPRESSION_ALL
      "Final set of enabled packages:  SimpleCxx MixedSharedStaticLibs 2"
      "Final set of enabled SE packages:  SimpleCxx MixedSharedStaticLibsSharedOnly MixedSharedStaticLibsStaticOnly MixedSharedStaticLibsStaticExec MixedSharedStaticLibs 5"
      "Configuring done"
      "Generating done"

  TEST_4 CMND make
    ARGS ${CTEST_BUILD_FLAGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Built target static_only_lib"
      "Linking CXX shared library libsimplecxx.so"  # Shared because of BULID_SHARED_LIBS=ON
      "Linking CXX shared library libshared_only_lib.so" # Always shared
      "Built target shared_only_lib"
      "Linking CXX static library libstatic_only_lib.a" # Always static
      "Built target static_only_lib"
      "Linking CXX executable MixedSharedStaticLibsSharedOnly_test"
      "Linking CXX executable MixedSharedStaticLibsStaticExec_test"

  TEST_5 CMND ls ARGS packages/simple_cxx/src
    PASS_REGULAR_EXPRESSION_ALL
      "libsimplecxx[.]so"
      "libsimplecxx[.]so[.]01"
      "libsimplecxx[.]so[.]1[.]1"

  TEST_6 CMND ls ARGS MixedSharedStaticLibs/shared_only
    PASS_REGULAR_EXPRESSION_ALL
      "libshared_only_lib[.]so"
      "libshared_only_lib[.]so[.]01"
      "libshared_only_lib[.]so[.]1[.]1"

  TEST_7 CMND ls ARGS MixedSharedStaticLibs/static_only
    PASS_REGULAR_EXPRESSION_ALL
      "libstatic_only_lib[.]a"

  TEST_8 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    PASS_REGULAR_EXPRESSION_ALL
      "MixedSharedStaticLibsSharedOnly_test.* Passed"
      "MixedSharedStaticLibsStaticExec_test.* Passed"
      "100% tests passed, 0 tests failed out of 4"

  )
  # NOTE: The above test make sure that you can build a static library with
  # tribits_add_library( ... STATIC ...) in project that is defaulted to use
  # shared libs with BUILD_SHARED_LIBS=ON.  This also tests that the correct
  # soversion links are created as well.


tribits_add_advanced_test( TribitsExampleProject_MixedSharedStaticLibs_static
  OVERALL_WORKING_DIRECTORY TEST_NAME
  EXCLUDE_IF_NOT_TRUE IS_REAL_LINUX_SYSTEM
  OVERALL_NUM_MPI_PROCS 1
  XHOSTTYPE Darwin

  TEST_0
    MESSAGE "Copy TribitsExampleProject so that we can copy in MixedSharedStaticLibs."
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject .

  TEST_1
    MESSAGE "Configure to get the compiler options"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DBUILD_SHARED_LIBS=OFF
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_ENABLE_DEBUG=OFF
      TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "BUILD_SHARED_LIBS=.OFF."
      "Configuring done"
      "Generating done"

  TEST_2
    MESSAGE "Copy MixedSharedStaticLibs to base dir."
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/MixedSharedStaticLibs
      TribitsExampleProject/.

  TEST_3
    MESSAGE "Configure SimpleCxx and MixedSharedStaticLibs"
    CMND ${CMAKE_COMMAND}
    ARGS
      -DTribitsExProj_EXTRA_REPOSITORIES=MixedSharedStaticLibs
      -DTribitsExProj_ENABLE_SimpleCxx=ON
      -DTribitsExProj_ENABLE_MixedSharedStaticLibs=ON
      -DTribitsExProj_ENABLE_TESTS=ON
     .
    PASS_REGULAR_EXPRESSION_ALL
      "Final set of enabled packages:  SimpleCxx MixedSharedStaticLibs 2"
      "Final set of enabled SE packages:  SimpleCxx MixedSharedStaticLibsSharedOnly MixedSharedStaticLibsStaticOnly MixedSharedStaticLibsStaticExec MixedSharedStaticLibs 5"
      "Configuring done"
      "Generating done"

  TEST_4 CMND make
    ARGS ${CTEST_BUILD_FLAGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Linking CXX static library libsimplecxx.a"   # Shared because of BULID_SHARED_LIBS=OFF
      "Linking CXX shared library libshared_only_lib.so" # Always shared
      "Built target shared_only_lib"
      "Linking CXX static library libstatic_only_lib.a" # Always static
      "Built target static_only_lib"
      "Linking CXX executable MixedSharedStaticLibsSharedOnly_test"
      "Linking CXX executable MixedSharedStaticLibsStaticExec_test"
  TEST_5 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    PASS_REGULAR_EXPRESSION_ALL
      "MixedSharedStaticLibsSharedOnly_test.* Passed"
      "MixedSharedStaticLibsStaticExec_test.* Passed"
      "100% tests passed, 0 tests failed out of 4"

  )
  # NOTE: The above test make sure that you can build a shared library with
  # tribits_add_library( ... SHARED ...) in project that is defaulted to use
  # static libs with BUILD_SHARED_LIBS=OFF.


tribits_add_advanced_test( TribitsExampleProject_DisableWithSubpackagesB_EnableWithSubpackagesB
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Just do dependency analysis to test enabling of parent package"
     " with eanbled subpackages even if is disabled"
    CMND ${CMAKE_COMMAND}
    ARGS
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_ENABLE_INSTALL_CMAKE_CONFIG_FILES=OFF
      -DTribitsExProj_ENABLE_EXPORT_MAKEFILES_DEFAULT=OFF
      -DTribitsExProj_SHORTCIRCUIT_AFTER_DEPENDENCY_HANDLING=ON
      -DTribitsExProj_ENABLE_WithSubpackagesA=OFF
      -DTribitsExProj_ENABLE_WithSubpackagesB=ON
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Explicitly enabled SE packages on input .by user.:  WithSubpackagesB 1"
      "-- Setting TribitsExProj_ENABLE_WrapExternal=OFF because WrapExternal has a required library dependence on disabled package WithSubpackagesA"
      "Enabling all optional intra-package enables <TRIBITS_PACKAGE>_ENABLE_<DEPPACKAGE> that are not currently disabled if both sets of packages are enabled [.][.][.]"
      "-- NOT setting WithSubpackagesB_ENABLE_MixedLang=ON since MixedLang is NOT enabled at this point!"
      "Enabling the shell of non-enabled parent packages [(]mostly for show[)] that have at least one subpackage enabled [.][.][.]"
      "-- Setting TribitsExProj_ENABLE_WithSubpackages=ON because TribitsExProj_ENABLE_WithSubpackagesB=ON"
      "Final set of enabled packages:  SimpleCxx WithSubpackages 2"
      "Final set of enabled SE packages:  SimpleCxx WithSubpackagesB WithSubpackages 3"

  )
# NOTE: The above test is the *only* test that we have that checks that a
# parent package is enabled at the end if any of its subpackages are enabled!
# This is also the only test that looks for the output that an optional
# package enable is not set.


##################################
# RPATH handling
##################################


if (CMAKE_HOST_SYSTEM_NAME STREQUAL "Darwin")
  set(SHARED_LIB_EXT "dylib")
  set(RPATH_INSPECT_CMND "otool")
  set(RPATH_INSPECT_ARG "-L")
elseif (CMAKE_HOST_SYSTEM_NAME STREQUAL "Linux")
  set(SHARED_LIB_EXT "so")
  set(RPATH_INSPECT_CMND "objdump")
  set(RPATH_INSPECT_ARG "-x")
endif()


#
# SimpleTpl_install_shared
#

if (CMAKE_HOST_SYSTEM_NAME STREQUAL "Darwin")
  set(THIS_RPATH_INSPECT_CMND "${RPATH_INSPECT_CMND}")
  set(THIS_RPATH_INSPECT_ARG "${RPATH_INSPECT_ARG}")
  set(RPATH_GREP_STR "@rpath/libsimpletpl.dylib")
elseif (CMAKE_HOST_SYSTEM_NAME STREQUAL "Linux")
  set(THIS_RPATH_INSPECT_CMND "ls")
  set(THIS_RPATH_INSPECT_ARG "")
  set(RPATH_GREP_STR "libsimpletpl")
else()
  set(THIS_RPATH_INSPECT_CMND "")
  set(THIS_RPATH_INSPECT_ARG "")
  set(RPATH_GREP_STR "")
endif()

set(SimpleTpl_install_shared_DIR
  ${CMAKE_CURRENT_BINARY_DIR}/${PACKAGE_NAME}_SimpleTpl_install_shared)

tribits_add_advanced_test( SimpleTpl_install_shared
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  EXCLUDE_IF_NOT_TRUE THIS_RPATH_INSPECT_CMND

  TEST_0
    CMND ${CMAKE_COMMAND}
    ARGS
      ${SERIAL_PASSTHROUGH_CONFIGURE_ARGS}
      -DBUILD_SHARED_LIBS=ON
      -DCMAKE_INSTALL_RPATH_USE_LINK_PATH=TRUE
      -DCMAKE_MACOSX_RPATH=TRUE
      -DCMAKE_INSTALL_PREFIX=${SimpleTpl_install_shared_DIR}/install
      -DCMAKE_INSTALL_INCLUDEDIR=include
      -DCMAKE_INSTALL_LIBDIR=lib
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/tpls/SimpleTpl
    PASS_REGULAR_EXPRESSION_ALL
      "Configuring done"
      "Generating done"

  TEST_1 CMND make
    ARGS ${CTEST_BUILD_FLAGS} install
    PASS_REGULAR_EXPRESSION_ALL
      "Built target simpletpl"
      "Installing: ${SimpleTpl_install_shared_DIR}/install/lib/libsimpletpl[.]"
      "Installing: ${SimpleTpl_install_shared_DIR}/install/include/SimpleTpl.hpp"

  TEST_2 CMND ${THIS_RPATH_INSPECT_CMND}
    ARGS ${THIS_RPATH_INSPECT_ARG}  install/lib/libsimpletpl.${SHARED_LIB_EXT}
    PASS_REGULAR_EXPRESSION  "${THIS_RPATH_GREP_STR}"
    ALWAYS_FAIL_ON_NONZERO_RETURN

    ADDED_TEST_NAME_OUT SimpleTpl_install_shared_NAME

  )


#
# Common configure arguments for all for the
# TribitsExampleProject_SimpleTpl_RPATH_XXX tests.
#

set(TEST_RPATH_COMMON_CONFIG_ARGS
  ${TribitsExampleProject_COMMON_CONFIG_ARGS}
  -DBUILD_SHARED_LIBS=ON
  -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
  -DTribitsExProj_ENABLE_Fortran=OFF
  -DTribitsExProj_ENABLE_SimpleCxx=ON
  -DTribitsExProj_ENABLE_TESTS=ON
  -DTPL_ENABLE_SimpleTpl=ON
  -DSimpleTpl_INCLUDE_DIRS=${SimpleTpl_install_shared_DIR}/install/include
  -DSimpleTpl_LIBRARY_DIRS=${SimpleTpl_install_shared_DIR}/install/lib
  )

set(LD_LIBRARY_PATH_ORIG $ENV{LD_LIBRARY_PATH})


#
# Test default TriBITS RPATH setting
#

set(RPATH_CURRENT_TEST_DIR
  ${CMAKE_CURRENT_BINARY_DIR}/${PACKAGE_NAME}_TribitsExampleProject_SimpleTpl_RPATH_default)

if (CMAKE_HOST_SYSTEM_NAME STREQUAL "Darwin")
  set(RPATH_GREP_STR "@rpath/libsimplecxx[.].*[.]dylib;@rpath/libsimpletpl[.]dylib")
elseif (CMAKE_HOST_SYSTEM_NAME STREQUAL "Linux")
  set(RPATH_GREP_STR
    "R.*PATH *${RPATH_CURRENT_TEST_DIR}/install/lib:${SimpleTpl_install_shared_DIR}/install/lib")
  # NOTE: Above matches both RPATH and RUNPATH which are used on different
  # Linux systems.
endif()

tribits_add_advanced_test( TribitsExampleProject_SimpleTpl_RPATH_default
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  EXCLUDE_IF_NOT_TRUE RPATH_INSPECT_CMND

  TEST_0 CMND ${CMAKE_COMMAND}
    MESSAGE "Do default configure for auto RPATH to install dir"
    ARGS
      ${TEST_RPATH_COMMON_CONFIG_ARGS}
      -DCMAKE_INSTALL_PREFIX=${RPATH_CURRENT_TEST_DIR}/install
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Processing enabled package: SimpleCxx .Libs, Tests, Examples."
      "Configuring done"
      "Generating done"
  # Above tests the standard install lib location

  TEST_1 CMND make ARGS ${CTEST_BUILD_FLAGS}
    MESSAGE "Build the default 'all' target using raw 'make'"
    PASS_REGULAR_EXPRESSION_ALL
      "Built target simplecxx"
      "Built target simplecxx-helloworld"
      "Built target SimpleCxx_HelloWorldTests"

  TEST_2 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    MESSAGE "Run all the tests with raw 'ctest'"
    PASS_REGULAR_EXPRESSION_ALL
      "SimpleCxx_HelloWorldTests${TEST_MPI_1_SUFFIX} .* Passed"
      "SimpleCxx_HelloWorldProg${TEST_MPI_1_SUFFIX} .* Passed"
      "100% tests passed, 0 tests failed out of 2"

  TEST_3 CMND make ARGS ${CTEST_BUILD_FLAGS} install
    PASS_REGULAR_EXPRESSION_ALL
      "-- Installing: .*/install/bin/simplecxx-helloworld"
      "-- Installing: .*/install/lib/libsimplecxx[.].*${SHARED_LIB_EXT}"

  TEST_4 CMND ${RPATH_INSPECT_CMND}
    ARGS  ${RPATH_INSPECT_ARG}  install/lib/libsimplecxx.${SHARED_LIB_EXT}
    PASS_REGULAR_EXPRESSION_ALL  "${RPATH_GREP_STR}"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_5
    MESSAGE "Run installed executable without having to set env"
    CMND ${RPATH_CURRENT_TEST_DIR}/install/bin/simplecxx-helloworld
    PASS_REGULAR_EXPRESSION_ALL
      "Hello World"
      "Cube.3. = 27"  # This comes from the SimpleTpl TPL

  ADDED_TEST_NAME_OUT RPATH_CURRENT_TEST_NAME_NAME
  )
if (RPATH_CURRENT_TEST_NAME_NAME)
  set_tests_properties(${RPATH_CURRENT_TEST_NAME_NAME}
    PROPERTIES DEPENDS ${SimpleTpl_install_shared_NAME} )
endif()


# NOTE: The above test does some more detailed checking for this first test
# case.  Future test cases will not do as much checking but only change what
# is changing.


#
# Test setting <project>_SET_INSTALL_RPATH=FALSE
#

set(RPATH_CURRENT_TEST_DIR
  ${CMAKE_CURRENT_BINARY_DIR}/${PACKAGE_NAME}_TribitsExampleProject_SimpleTpl_RPATH_no_SET_INSTALL_RPATH)

if (CMAKE_HOST_SYSTEM_NAME STREQUAL "Darwin")
  set(RPATH_GREP_STR "@rpath/libsimplecxx[.].*[.]dylib;@rpath/libsimpletpl[.]dylib")
elseif (CMAKE_HOST_SYSTEM_NAME STREQUAL "Linux")
  set(RPATH_GREP_STR
    "R.*PATH *${SimpleTpl_install_shared_DIR}/install/lib")
endif()

tribits_add_advanced_test( TribitsExampleProject_SimpleTpl_RPATH_no_SET_INSTALL_RPATH
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  EXCLUDE_IF_NOT_TRUE RPATH_INSPECT_CMND

  TEST_0 CMND ${CMAKE_COMMAND}
    MESSAGE "Do configure with -DTribitsExProj_SET_INSTALL_RPATH=OFF"
    ARGS
      ${TEST_RPATH_COMMON_CONFIG_ARGS}
      -DCMAKE_INSTALL_PREFIX=${RPATH_CURRENT_TEST_DIR}/install2
      -DTribitsExProj_SET_INSTALL_RPATH=OFF
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject

  TEST_1 CMND make ARGS ${CTEST_BUILD_FLAGS} install

  TEST_2 CMND ${RPATH_INSPECT_CMND}
    ARGS  ${RPATH_INSPECT_ARG}  install2/lib/libsimplecxx.${SHARED_LIB_EXT}
    PASS_REGULAR_EXPRESSION_ALL  "${RPATH_GREP_STR}"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_3 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    MESSAGE "Run the executables from the build directory which shows that RPATH is set in build tree."
    PASS_REGULAR_EXPRESSION_ALL
      "100% tests passed, 0 tests failed out of 2"

  TEST_4
    MESSAGE "Run installed executable which should fail"
    CMND ${RPATH_CURRENT_TEST_DIR}/install/bin/simplecxx-helloworld
    WILL_FAIL

  ADDED_TEST_NAME_OUT RPATH_CURRENT_TEST_NAME_NAME
  )
if (RPATH_CURRENT_TEST_NAME_NAME)
  set_tests_properties(${RPATH_CURRENT_TEST_NAME_NAME}
    PROPERTIES DEPENDS ${SimpleTpl_install_shared_NAME} )
endif()


# Run the executable built and installed above setting LD_LIBRARY_PATH
tribits_add_test(
  simplecxx-helloworld  NOEXEPREFIX  NOEXESUFFIX
    DIRECTORY ${RPATH_CURRENT_TEST_DIR}/install2/bin
  NAME TribitsExampleProject_SimpleTpl_RPATH_no_SET_INSTALL_RPATH_run
  EXCLUDE_IF_NOT_TRUE IS_REAL_LINUX_SYSTEM
  ENVIRONMENT
    LD_LIBRARY_PATH=${RPATH_CURRENT_TEST_DIR}/install2/lib:${LD_LIBRARY_PATH_ORIG}
  ADDED_TESTS_NAMES_OUT TribitsExampleProject_SimpleTpl_RPATH_no_SET_INSTALL_RPATH_run_NAMES
  )
if (TribitsExampleProject_SimpleTpl_RPATH_no_SET_INSTALL_RPATH_run_NAMES
  AND RPATH_CURRENT_TEST_NAME_NAME
  )
  set_tests_properties(
    ${TribitsExampleProject_SimpleTpl_RPATH_no_SET_INSTALL_RPATH_run_NAMES}
    PROPERTIES DEPENDS ${RPATH_CURRENT_TEST_NAME_NAME} )
endif()


#
# Test setting CMAKE_INSTALL_RPATH="<path0>:<path1>:..."
#

set(RPATH_CURRENT_TEST_DIR
  ${CMAKE_CURRENT_BINARY_DIR}/${PACKAGE_NAME}_TribitsExampleProject_SimpleTpl_RPATH_CMAKE_INSTALL_RPATH)

if (CMAKE_HOST_SYSTEM_NAME STREQUAL "Darwin")
  set(RPATH_GREP_STR "@rpath/libsimplecxx[.].*[.]dylib;@rpath/libsimpletpl[.]dylib")
elseif (CMAKE_HOST_SYSTEM_NAME STREQUAL "Linux")
  set(RPATH_GREP_STR
    "R.*PATH *${RPATH_CURRENT_TEST_DIR}/install2/nonstd_lib_location:${SimpleTpl_install_shared_DIR}/install/lib")
endif()

tribits_add_advanced_test( TribitsExampleProject_SimpleTpl_RPATH_CMAKE_INSTALL_RPATH
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  EXCLUDE_IF_NOT_TRUE RPATH_INSPECT_CMND

  TEST_0 CMND ${CMAKE_COMMAND}
    MESSAGE "Do configure with CMAKE_INSTALL_RPATH set to moved install dir install2/"
    ARGS
      ${TEST_RPATH_COMMON_CONFIG_ARGS}
      -DCMAKE_INSTALL_PREFIX=${RPATH_CURRENT_TEST_DIR}/install
      -DTribitsExProj_INSTALL_LIB_DIR:STRING=nonstd_lib_location
      -DCMAKE_INSTALL_RPATH_USE_LINK_PATH=FALSE
      -DCMAKE_INSTALL_RPATH="${RPATH_CURRENT_TEST_DIR}/install2/nonstd_lib_location:${SimpleTpl_install_shared_DIR}/install/lib"
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
  # Above tests with a non-standard lib location to see that TriBITS has the
  # right logic in this case.

  TEST_1 CMND make ARGS ${CTEST_BUILD_FLAGS} install
    PASS_REGULAR_EXPRESSION_ALL
      "-- Installing: .*/install/bin/simplecxx-helloworld"
      "-- Installing: .*/install/nonstd_lib_location/libsimplecxx[.].*${SHARED_LIB_EXT}"

  TEST_2 CMND ${RPATH_INSPECT_CMND}
    ARGS  ${RPATH_INSPECT_ARG}  install/nonstd_lib_location/libsimplecxx.${SHARED_LIB_EXT}
    PASS_REGULAR_EXPRESSION_ALL  "${RPATH_GREP_STR}"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_3 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    MESSAGE "Run the executables from the build directory which shows that RPATH is set in build tree."
    PASS_REGULAR_EXPRESSION_ALL
      "100% tests passed, 0 tests failed out of 2"

  TEST_4
    MESSAGE "Run installed executable which should fail"
    CMND ${RPATH_CURRENT_TEST_DIR}/install/bin/simplecxx-helloworld
    WILL_FAIL

  TEST_5
    MESSAGE "Move from install/ to install2/ which should match CMAKE_INSTALL_RPATH"
    CMND mv ARGS install/ install2/

  TEST_6
    MESSAGE "Run from the moved install2/ dir which should pass"
    CMND ${RPATH_CURRENT_TEST_DIR}/install2/bin/simplecxx-helloworld
    PASS_REGULAR_EXPRESSION_ALL
      "Hello World"
      "Cube.3. = 27"  # This comes from the SimpleTpl TPL

  ADDED_TEST_NAME_OUT RPATH_CURRENT_TEST_NAME_NAME
  )
if (RPATH_CURRENT_TEST_NAME_NAME)
  set_tests_properties(${RPATH_CURRENT_TEST_NAME_NAME}
    PROPERTIES DEPENDS ${SimpleTpl_install_shared_NAME} )
endif()


#
# Test setting -DCMAKE_SKIP_INSTALL_RPATH=TRUE
#

set(RPATH_CURRENT_TEST_DIR
  ${CMAKE_CURRENT_BINARY_DIR}/${PACKAGE_NAME}_TribitsExampleProject_SimpleTpl_RPATH_CMAKE_SKIP_INSTALL_RPATH)

if (CMAKE_HOST_SYSTEM_NAME STREQUAL "Darwin")
  set(RPATH_GREP_STR "@rpath/libsimplecxx[.].*[.]dylib;@rpath/libsimpletpl[.]dylib")
elseif (CMAKE_HOST_SYSTEM_NAME STREQUAL "Linux")
  set(RPATH_GREP_STR "") # Can't look for RPATH at all
endif()

tribits_add_advanced_test( TribitsExampleProject_SimpleTpl_RPATH_CMAKE_SKIP_INSTALL_RPATH
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  EXCLUDE_IF_NOT_TRUE RPATH_INSPECT_CMND

  TEST_0 CMND ${CMAKE_COMMAND}
    MESSAGE "Do configure with -DTribitsExProj_SET_INSTALL_RPATH=OFF"
    ARGS
      ${TEST_RPATH_COMMON_CONFIG_ARGS}
      -DCMAKE_INSTALL_PREFIX=${RPATH_CURRENT_TEST_DIR}/install3
      -DCMAKE_SKIP_INSTALL_RPATH=TRUE
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject

  TEST_1 CMND make ARGS ${CTEST_BUILD_FLAGS} install
    MESSAGE "Install and grep to check for expected RPATH"
    PASS_REGULAR_EXPRESSION_ALL
      "-- Installing: .*/install3/bin/simplecxx-helloworld"
      "-- Installing: .*/install3/lib/libsimplecxx[.].*${SHARED_LIB_EXT}"

  TEST_2 CMND ${RPATH_INSPECT_CMND}
    ARGS  ${RPATH_INSPECT_ARG}  install3/lib/libsimplecxx.${SHARED_LIB_EXT}
    PASS_REGULAR_EXPRESSION_ALL  "${RPATH_GREP_STR}"
    FAIL_REGULAR_EXPRESSION  "RPATH.*${SimpleTpl_install_shared_DIR}/install/lib"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_3 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    MESSAGE "Run the executables from the build directory which shows that RPATH is set in build tree."
    PASS_REGULAR_EXPRESSION_ALL
      "100% tests passed, 0 tests failed out of 2"

  TEST_4
    MESSAGE "Run installed executable which should fail"
    CMND ${RPATH_CURRENT_TEST_DIR}/install3/bin/simplecxx-helloworld
    WILL_FAIL

  ADDED_TEST_NAME_OUT RPATH_CURRENT_TEST_NAME_NAME
  )
if (RPATH_CURRENT_TEST_NAME_NAME)
  set_tests_properties(${RPATH_CURRENT_TEST_NAME_NAME}
    PROPERTIES DEPENDS ${SimpleTpl_install_shared_NAME} )
endif()


# Run the executable built and installed above setting LD_LIBRARY_PATH
tribits_add_test(
  simplecxx-helloworld  NOEXEPREFIX  NOEXESUFFIX
    DIRECTORY ${RPATH_CURRENT_TEST_DIR}/install3/bin
  NAME TribitsExampleProject_SimpleTpl_RPATH_CMAKE_SKIP_INSTALL_RPATH_run
  EXCLUDE_IF_NOT_TRUE IS_REAL_LINUX_SYSTEM
  PASS_REGULAR_EXPRESSION
    "Hello World"
  ENVIRONMENT
    LD_LIBRARY_PATH=${RPATH_CURRENT_TEST_DIR}/install3/lib:${SimpleTpl_install_shared_DIR}/install/lib:${LD_LIBRARY_PATH_ORIG}
  ADDED_TESTS_NAMES_OUT TribitsExampleProject_SimpleTpl_RPATH_CMAKE_SKIP_INSTALL_RPATH_run_NAMES
  )
if (TribitsExampleProject_SimpleTpl_RPATH_CMAKE_SKIP_INSTALL_RPATH_run_NAMES
  AND RPATH_CURRENT_TEST_NAME_NAME
  )
  set_tests_properties(
    ${TribitsExampleProject_SimpleTpl_RPATH_CMAKE_SKIP_INSTALL_RPATH_run_NAMES}
    PROPERTIES DEPENDS ${RPATH_CURRENT_TEST_NAME_NAME} )
endif()


#
# Test cmake/ProjectCompilerPostConfig.cmake
#

tribits_add_advanced_test( TribitsExampleProject_ProjectCompilerPostConfig
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  XHOSTTYPE Darwin

  TEST_0
    MESSAGE "Copy TribitsExampleProject so that we can copy in cmake/ProjectCompilerPostConfig.cmake."
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject .

  TEST_1
    MESSAGE "Copy in dummy cmake/ProjectCompilerPostConfig.cmake."
    CMND cp
    ARGS ${CMAKE_CURRENT_SOURCE_DIR}/DummyProjectCompilerPostConfig.cmake
      TribitsExampleProject/cmake/ProjectCompilerPostConfig.cmake

  TEST_2
    MESSAGE "Configure SimpleCxx and trace includes"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_ENABLE_DEBUG=OFF
      -DTribitsExProj_TRACE_FILE_PROCESSING=ON
      -DTribitsExProj_ENABLE_SimpleCxx=ON
      -DCMAKE_VERBOSE_MAKEFILE=ON
      TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "-- File Trace: PROJECT    INCLUDE    .*/cmake/ProjectCompilerPostConfig[.]cmake"
      "Configuring done"
      "Generating done"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_3
    MESSAGE "VERBOSE Build the simplecxx lib and verify that the new compiler flags is added "
    CMND make
    PASS_REGULAR_EXPRESSION_ALL
      "DDUMMY_DEFINE_JUST_TO_TEST_COMILER_POST_CONFIG"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  )


########################################################################
# TribitsExampleProject + TribitsExampleProjectAddons
########################################################################


tribits_add_advanced_test( TribitsExampleProject_TribitsExampleProjectAddons
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Copy TribitsExampleProject so that we can copy in TribitsExampleProjectAddons."
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject .

  TEST_1
    MESSAGE "Copy TribitsExampleProjectAddons to base dir."
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProjectAddons
      TribitsExampleProject/.

  TEST_2
    MESSAGE "Configure with cmake/ExtraRepositoriesList.cmake file enabling all packages"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_ENABLE_DEBUG=OFF
      -DTribitsExProj_ENABLE_ALL_PACKAGES=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      -DTribitsExProj_EXTRAREPOS_FILE=cmake/ExtraRepositoriesList.cmake
      -DTribitsExProj_ENABLE_KNOWN_EXTERNAL_REPOS_TYPE=Continuous
      TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "-- Adding POST extra Continuous repository TribitsExampleProjectAddons "
      "Reading list of native packages from .*/TribitsExampleProject/PackagesList.cmake"
      "Reading list of native TPLs from .*/TribitsExampleProject/TPLsList.cmake"
      "Reading list of POST extra packages from .*/TribitsExampleProject/TribitsExampleProjectAddons/PackagesList.cmake"
      "Reading list of POST extra TPLs from .*/TribitsExampleProject/TribitsExampleProjectAddons/TPLsList.cmake"
      "Final set of enabled SE packages:  SimpleCxx .* Addon1"
      "Processing enabled package: SimpleCxx [(]Libs, Tests, Examples[)]"
      "Processing enabled package: Addon1 [(]Libs, Tests, Examples[)]"
      "Configuring done"
      "Generating done"

  TEST_3 CMND make
    ARGS ${CTEST_BUILD_FLAGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Linking CXX executable Addon1_test.exe"
      "Built target Addon1_test"

  TEST_4 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    PASS_REGULAR_EXPRESSION_ALL
      "Test .*: Addon1_test .* Passed"
      "100% tests passed, 0 tests failed out of"

  TEST_5 CMND make
    ARGS ${CTEST_BUILD_FLAGS} clean

  TEST_6
    MESSAGE "Configure again enabling all packages using TribitsExProj_EXTRA_REPOSITORIES only"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_EXTRAREPOS_FILE=
      -DTribitsExProj_EXTRA_REPOSITORIES=TribitsExampleProjectAddons
      .
    PASS_REGULAR_EXPRESSION_ALL
      "Processing list of POST extra repos from TribitsExProj_EXTRA_REPOSITORIES='TribitsExampleProjectAddons'"
      "Reading list of native packages from .*/TribitsExampleProject/PackagesList.cmake"
      "Reading list of native TPLs from .*/TribitsExampleProject/TPLsList.cmake"
      "Reading list of POST extra packages from .*/TribitsExampleProject/TribitsExampleProjectAddons/PackagesList.cmake"
      "Reading list of POST extra TPLs from .*/TribitsExampleProject/TribitsExampleProjectAddons/TPLsList.cmake"
      "Final set of enabled SE packages:  SimpleCxx .* Addon1"
      "Processing enabled package: SimpleCxx [(]Libs, Tests, Examples[)]"
      "Processing enabled package: Addon1 [(]Libs, Tests, Examples[)]"
      "Configuring done"
      "Generating done"

  TEST_7 CMND make
    ARGS ${CTEST_BUILD_FLAGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Linking CXX executable Addon1_test.exe"
      "Built target Addon1_test"

  TEST_8 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    PASS_REGULAR_EXPRESSION_ALL
      "Test .*: Addon1_test .* Passed"
      "100% tests passed, 0 tests failed out of"

  )


########################################################################
# TribitsExampleApp
########################################################################


function(TribitsExampleApp_ALL_ST_NoFortran_test sharedOrStatic)

  if (sharedOrStatic STREQUAL "SHARED")
    set(buildSharedLibsArg -DBUILD_SHARED_LIBS=ON)
  else()
    set(buildSharedLibsArg -DBUILD_SHARED_LIBS=OFF)
  endif()

  set(testBaseName TribitsExampleApp_ALL_ST_NoFortran_${sharedOrStatic})
  set(testName ${PACKAGE_NAME}_${testBaseName})
  set(buildDir ${CMAKE_CURRENT_BINARY_DIR}/${testName})

  tribits_add_advanced_test( ${testBaseName}
    OVERALL_WORKING_DIRECTORY TEST_NAME
    OVERALL_NUM_MPI_PROCS 1
    XHOSTTYPE Darwin

    TEST_0
      MESSAGE "Configure SimpleTpl to be installed for TribitsExampleProject"
      WORKING_DIRECTORY simpletpl_build
      CMND ${CMAKE_COMMAND}
      ARGS
        ${SERIAL_PASSTHROUGH_CONFIGURE_ARGS}
        -DCMAKE_BUILD_TYPE=RelWithDepInfo
        ${buildSharedLibsArg}
        -DCMAKE_INSTALL_PREFIX=install
        ${${PROJECT_NAME}_TRIBITS_DIR}/examples/tpls/SimpleTpl

    TEST_1
      MESSAGE "Build and install SimpleTpl locally"
      WORKING_DIRECTORY simpletpl_build
      SKIP_CLEAN_WORKING_DIRECTORY
      CMND make ARGS ${CTEST_BUILD_FLAGS} install

    TEST_2
      MESSAGE "Do the configure of TribitsExampleProject"
      CMND ${CMAKE_COMMAND}
      ARGS
        ${TribitsExampleProject_COMMON_CONFIG_ARGS}
        -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
        -DTribitsExProj_ENABLE_Fortran=OFF
        -DTribitsExProj_ENABLE_ALL_PACKAGES=ON
        -DTribitsExProj_ENABLE_SECONDARY_TESTED_CODE=ON
        -DTribitsExProj_ENABLE_INSTALL_CMAKE_CONFIG_FILES=ON
        -DTPL_ENABLE_SimpleTpl=ON
        -DSimpleTpl_INCLUDE_DIRS=${buildDir}/simpletpl_build/install/include
        -DSimpleTpl_LIBRARY_DIRS=${buildDir}/simpletpl_build/install/lib
        ${buildSharedLibsArg}
        -DCMAKE_INSTALL_PREFIX=install
        ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject

    TEST_3
      MESSAGE "Build and install TribitsExampleProject locally"
      CMND make ARGS ${CTEST_BUILD_FLAGS} install

    TEST_4
      MESSAGE "Configure TribitsExampleApp locally"
      WORKING_DIRECTORY app_build
      CMND ${CMAKE_COMMAND} ARGS
        -DCMAKE_PREFIX_PATH=${buildDir}/install
        -DTribitsExApp_USE_COMPONENTS=SimpleCxx,WithSubpackages
        ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleApp
      PASS_REGULAR_EXPRESSION_ALL
        "-- Configuring done"
        "-- Generating done"
        "-- Build files have been written to: .*/${testName}/app_build"
      ALWAYS_FAIL_ON_NONZERO_RETURN

    TEST_5
      MESSAGE "Build TribitsExampleApp"
      WORKING_DIRECTORY app_build
      SKIP_CLEAN_WORKING_DIRECTORY
      CMND make ARGS ${CTEST_BUILD_FLAGS}
      PASS_REGULAR_EXPRESSION_ALL
        "Built target app"
      ALWAYS_FAIL_ON_NONZERO_RETURN

    TEST_6
      MESSAGE "Test TribitsExampleApp"
      WORKING_DIRECTORY app_build
      SKIP_CLEAN_WORKING_DIRECTORY
      CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
      PASS_REGULAR_EXPRESSION_ALL
        "Full Deps: WithSubpackages:B A simpletpl headeronlytpl simpletpl headeronlytpl[;] SimpleCxx:simpletpl headeronlytpl"
        "app_test [.]+   Passed"
        "100% tests passed, 0 tests failed out of 1"
      ALWAYS_FAIL_ON_NONZERO_RETURN

    )

endfunction()


TribitsExampleApp_ALL_ST_NoFortran_test(STATIC)
TribitsExampleApp_ALL_ST_NoFortran_test(SHARED)


function(TribitsExampleApp_ALL_ST_test byProjectOrPackage sharedOrStatic)

  if (byProjectOrPackage STREQUAL "ByProject")
    set(findByProjectOrPackageArg -DTribitsExApp_FIND_INDIVIDUAL_PACKAGES=OFF)
    set(foundProjectOrPackageStr "Found TribitsExProj")
  elseif (byProjectOrPackage STREQUAL "ByPackage")
    set(findByProjectOrPackageArg -DTribitsExApp_FIND_INDIVIDUAL_PACKAGES=ON)
    set(foundProjectOrPackageStr "Found SimpleCxx")
  else()
    message(FATAL_ERROR "Invaid value for findByProjectOrPackageArg='${findByProjectOrPackageArg}'!")
  endif()

  if (sharedOrStatic STREQUAL "SHARED")
    set(buildSharedLibsArg -DBUILD_SHARED_LIBS=ON)
  elseif (sharedOrStatic STREQUAL "STATIC")
    set(buildSharedLibsArg -DBUILD_SHARED_LIBS=OFF)
  else()
    message(FATAL_ERROR "Invaid value for sharedOrStatic='${sharedOrStatic}'!")
  endif()

  set(testBaseName TribitsExampleApp_ALL_ST_${byProjectOrPackage}_${sharedOrStatic})
  set(testName ${PACKAGE_NAME}_${testBaseName})
  set(buildDir ${CMAKE_CURRENT_BINARY_DIR}/${testName})

  tribits_add_advanced_test( ${testBaseName}
    OVERALL_WORKING_DIRECTORY TEST_NAME
    OVERALL_NUM_MPI_PROCS 1
    EXCLUDE_IF_NOT_TRUE ${PROJECT_NAME}_ENABLE_Fortran
    XHOSTTYPE Darwin

    TEST_0
      MESSAGE "Configure SimpleTpl to be installed for TribitsExampleProject"
      WORKING_DIRECTORY simpletpl_build
      CMND ${CMAKE_COMMAND}
      ARGS
        ${SERIAL_PASSTHROUGH_CONFIGURE_ARGS}
        -DCMAKE_BUILD_TYPE=RelWithDepInfo
        ${buildSharedLibsArg}
        -DCMAKE_INSTALL_PREFIX=install
        ${${PROJECT_NAME}_TRIBITS_DIR}/examples/tpls/SimpleTpl

    TEST_1
      MESSAGE "Build and install SimpleTpl locally"
      WORKING_DIRECTORY simpletpl_build
      SKIP_CLEAN_WORKING_DIRECTORY
      CMND make ARGS ${CTEST_BUILD_FLAGS} install

    TEST_2
      MESSAGE "Do the configure of TribitsExampleProject"
      CMND ${CMAKE_COMMAND}
      ARGS
        ${TribitsExampleProject_COMMON_CONFIG_ARGS}
        -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
        -DTribitsExProj_ENABLE_Fortran=ON
        -DTribitsExProj_ENABLE_ALL_PACKAGES=ON
        -DTribitsExProj_ENABLE_SECONDARY_TESTED_CODE=ON
        -DTribitsExProj_ENABLE_INSTALL_CMAKE_CONFIG_FILES=ON
        -DTPL_ENABLE_SimpleTpl=ON
        -DSimpleTpl_INCLUDE_DIRS=${buildDir}/simpletpl_build/install/include
        -DSimpleTpl_LIBRARY_DIRS=${buildDir}/simpletpl_build/install/lib
        ${buildSharedLibsArg}
        -DCMAKE_INSTALL_PREFIX=install
        ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject

    TEST_3
      MESSAGE "Build and install TribitsExampleProject locally"
      CMND make ARGS ${CTEST_BUILD_FLAGS} install

    TEST_4
      MESSAGE "Configure TribitsExampleApp locally"
      WORKING_DIRECTORY app_build
      CMND ${CMAKE_COMMAND} ARGS
        -DCMAKE_PREFIX_PATH=${buildDir}/install
        -DTribitsExApp_USE_COMPONENTS=SimpleCxx,MixedLang,WithSubpackages
        ${findByProjectOrPackageArg}
        ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleApp
      PASS_REGULAR_EXPRESSION_ALL
        "${foundProjectOrPackageStr}"
        "-- Configuring done"
        "-- Generating done"
        "-- Build files have been written to: .*/${testName}/app_build"
      ALWAYS_FAIL_ON_NONZERO_RETURN

    TEST_5
      MESSAGE "Build TribitsExampleApp"
      WORKING_DIRECTORY app_build
      SKIP_CLEAN_WORKING_DIRECTORY
      CMND make ARGS ${CTEST_BUILD_FLAGS}
      PASS_REGULAR_EXPRESSION_ALL
        "Built target app"
      ALWAYS_FAIL_ON_NONZERO_RETURN

    TEST_6
      MESSAGE "Test TribitsExampleApp"
      WORKING_DIRECTORY app_build
      SKIP_CLEAN_WORKING_DIRECTORY
      CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
      PASS_REGULAR_EXPRESSION_ALL
        "Full Deps: WithSubpackages:B A simpletpl headeronlytpl simpletpl headeronlytpl[;] MixedLang:Mixed Language[;] SimpleCxx:simpletpl headeronlytpl"
        "app_test [.]+   Passed"
        "100% tests passed, 0 tests failed out of 1"
      ALWAYS_FAIL_ON_NONZERO_RETURN
    )

endfunction()


TribitsExampleApp_ALL_ST_test(ByProject STATIC)
TribitsExampleApp_ALL_ST_test(ByProject SHARED)
TribitsExampleApp_ALL_ST_test(ByPackage STATIC)
TribitsExampleApp_ALL_ST_test(ByPackage SHARED)


function(TribitsExampleApp_ALL_ST_buildtree_test sharedOrStatic)

  if (sharedOrStatic STREQUAL "SHARED")
    set(buildSharedLibsArg -DBUILD_SHARED_LIBS=ON)
  elseif (sharedOrStatic STREQUAL "STATIC")
    set(buildSharedLibsArg -DBUILD_SHARED_LIBS=OFF)
  else()
    message(FATAL_ERROR "Invaid value for sharedOrStatic='${sharedOrStatic}'!")
  endif()

  set(testBaseName TribitsExampleApp_ALL_ST_buildtree_${sharedOrStatic})
  set(testName ${PACKAGE_NAME}_${testBaseName})
  set(buildDir ${CMAKE_CURRENT_BINARY_DIR}/${testName})

  tribits_add_advanced_test( ${testBaseName}
    OVERALL_WORKING_DIRECTORY TEST_NAME
    OVERALL_NUM_MPI_PROCS 1
    EXCLUDE_IF_NOT_TRUE ${PROJECT_NAME}_ENABLE_Fortran
    XHOSTTYPE Darwin

    TEST_0
      MESSAGE "Do the configure of TribitsExampleProject"
      CMND ${CMAKE_COMMAND}
      ARGS
        ${TribitsExampleProject_COMMON_CONFIG_ARGS}
        -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
        -DTribitsExProj_ENABLE_Fortran=ON
        -DTribitsExProj_ENABLE_ALL_PACKAGES=ON
        -DTribitsExProj_ENABLE_SECONDARY_TESTED_CODE=ON
        -DTribitsExProj_ENABLE_INSTALL_CMAKE_CONFIG_FILES=ON
        ${buildSharedLibsArg}
        ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject

    TEST_1
      MESSAGE "Build TribitsExampleProject only (no install)"
      CMND make ARGS ${CTEST_BUILD_FLAGS}

    TEST_2
      MESSAGE "Configure TribitsExampleApp locally"
      WORKING_DIRECTORY app_build
      CMND ${CMAKE_COMMAND} ARGS
        -DTribitsExApp_FIND_INDIVIDUAL_PACKAGES=TRUE
        -DTribitsExApp_FIND_UNDER_BUILD_DIR=${buildDir}
        -DTribitsExApp_USE_COMPONENTS=SimpleCxx,MixedLang
        ${findByProjectOrPackageArg}
        ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleApp
      PASS_REGULAR_EXPRESSION_ALL
        "Found SimpleCxx"
        "Found MixedLang"
        "-- Configuring done"
        "-- Generating done"
        "-- Build files have been written to: .*/${testName}/app_build"
      ALWAYS_FAIL_ON_NONZERO_RETURN

    TEST_3
      MESSAGE "Build TribitsExampleApp"
      WORKING_DIRECTORY app_build
      SKIP_CLEAN_WORKING_DIRECTORY
      CMND make ARGS ${CTEST_BUILD_FLAGS}
      PASS_REGULAR_EXPRESSION_ALL
        "Built target app"
      ALWAYS_FAIL_ON_NONZERO_RETURN

    TEST_4
      MESSAGE "Test TribitsExampleApp"
      WORKING_DIRECTORY app_build
      SKIP_CLEAN_WORKING_DIRECTORY
      CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
      PASS_REGULAR_EXPRESSION_ALL
        "Full Deps: MixedLang:Mixed Language[;] SimpleCxx:headeronlytpl"
        "app_test [.]+   Passed"
        "100% tests passed, 0 tests failed out of 1"
      ALWAYS_FAIL_ON_NONZERO_RETURN
    )

endfunction()
#
# NOTE: The test above only pulls in top-level packages that don't have any
# subpackages SimpleCxx and MixedLang.  It seems that whoever implemented the
# <Package>Config.cmake files in the build dir only got this working for
# top-level packages that don't have any subpackages.  This test above at
# least (partially) pins down what already works.  (Later, these
# <Package>Config.cmake files in the build dir will need to be fixed up so
# that they work for top-level packages with subpackages as well and then this
# test can be expanded for that case too.)


TribitsExampleApp_ALL_ST_buildtree_test(STATIC)
TribitsExampleApp_ALL_ST_buildtree_test(SHARED)


########################################################################
# TribitsExampleProjectAddons
########################################################################


tribits_add_advanced_test( TribitsExampleProjectAddons
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Copy TribitsExampleProjectAddons"
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProjectAddons .

  TEST_1
    MESSAGE "Copy TribitsExampleProject to base dir"
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
      TribitsExampleProjectAddons/.

  TEST_2
    MESSAGE "Configure enabling all packages using cmake/ExtraRepositoriesList.cmake"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${COMMON_ENV_ARGS_PASSTHROUGH}
      -DTribitsExProjAddons_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProjAddons_ENABLE_Fortran=OFF
      -DTribitsExProjAddons_ENABLE_DEBUG=OFF
      -DTribitsExProjAddons_ENABLE_ALL_PACKAGES=ON
      -DTribitsExProjAddons_ENABLE_TESTS=ON
      TribitsExampleProjectAddons
    PASS_REGULAR_EXPRESSION_ALL
      "Reading the list of extra repositories from cmake/ExtraRepositoriesList.cmake"
      "-- Adding PRE extra Continuous repository TribitsExampleProject "
      "Reading list of PRE extra packages from .*/TribitsExampleProjectAddons/TribitsExampleProject/PackagesList.cmake"
      "Reading list of PRE extra TPLs from .*/TribitsExampleProjectAddons/TribitsExampleProject/TPLsList.cmake"
      "Reading list of native packages from .*/TribitsExampleProjectAddons/PackagesList.cmake"
      "Reading list of native TPLs from .*/TribitsExampleProjectAddons/TPLsList.cmake"
      "Final set of enabled SE packages:  SimpleCxx .* Addon1"
      "Processing enabled package: SimpleCxx [(]Libs, Tests, Examples[)]"
      "Processing enabled package: Addon1 [(]Libs, Tests, Examples[)]"
      "Configuring done"
      "Generating done"

  TEST_3 CMND make
    ARGS ${CTEST_BUILD_FLAGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Linking CXX executable Addon1_test.exe"
      "Built target Addon1_test"

  TEST_4 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    PASS_REGULAR_EXPRESSION_ALL
      "Test .*: Addon1_test .* Passed"
      "100% tests passed, 0 tests failed out of"

  TEST_5 CMND make
    ARGS ${CTEST_BUILD_FLAGS} clean

  TEST_6
    MESSAGE "Configure again enabling all packages using TribitsExProjAddons_PRE_REPOSITORIES only"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${COMMON_ENV_ARGS_PASSTHROUGH}
      -DTribitsExProjAddons_EXTRAREPOS_FILE=
      -DTribitsExProjAddons_PRE_REPOSITORIES=TribitsExampleProject
      .
    PASS_REGULAR_EXPRESSION_ALL
      "Processing list of PRE extra repos from TribitsExProjAddons_PRE_REPOSITORIES='TribitsExampleProject'"
      "Reading list of PRE extra packages from .*/TribitsExampleProjectAddons/TribitsExampleProject/PackagesList.cmake"
      "Reading list of PRE extra TPLs from .*/TribitsExampleProjectAddons/TribitsExampleProject/TPLsList.cmake"
      "Reading list of native packages from .*/TribitsExampleProjectAddons/PackagesList.cmake"
      "Reading list of native TPLs from .*/TribitsExampleProjectAddons/TPLsList.cmake"
      "Final set of enabled SE packages:  SimpleCxx .* Addon1"
      "Processing enabled package: SimpleCxx [(]Libs, Tests, Examples[)]"
      "Processing enabled package: Addon1 [(]Libs, Tests, Examples[)]"
      "Configuring done"
      "Generating done"

  TEST_7 CMND make
    ARGS ${CTEST_BUILD_FLAGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Linking CXX executable Addon1_test.exe"
      "Built target Addon1_test"

  TEST_8 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    PASS_REGULAR_EXPRESSION_ALL
      "Test .*: Addon1_test .* Passed"
      "100% tests passed, 0 tests failed out of"

  )


########################################################################
# TribitsExampleMetaProject
########################################################################


tribits_add_advanced_test( TribitsExampleMetaProject_Empty
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Configure TribitsExampleMetaProject with nothing in it"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${COMMON_ENV_ARGS_PASSTHROUGH}
      -DTribitsExMetaProj_ENABLE_Fortran=OFF
      -DTribitsExMetaProj_IGNORE_MISSING_EXTRA_REPOSITORIES=TRUE
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleMetaProject
    PASS_REGULAR_EXPRESSION_ALL
      "NOTE: Ignoring missing extra repo 'TribitsExampleProject' as requested since .*/TribitsExampleMetaProject/TribitsExampleProject does not exist"
      "NOTE: Ignoring missing extra repo 'TribitsExampleProjectAddons' as requested since .*/TribitsExampleMetaProject/TribitsExampleProjectAddons does not exist"
      "Final set of enabled SE packages:  0"
      "Final set of non-enabled SE packages:  0"
      "WARNING:  There were no packages configured so no libraries or tests/examples will be built"
      "Configuring done"
      "Generating done"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  )
# NOTE: That above test is the only test that triggers an empty list that
# tries to get reversed.  This is a TriBITS project with no packages and no
# TPLs.  While not common, it is a starter sitiation that users will have so
# it should be handled smoothly.


tribits_add_advanced_test( TribitsExampleMetaProject
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Copy TribitsExampleMetaProject"
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleMetaProject .

  TEST_1
    MESSAGE "Copy TribitsExampleProject to base dir"
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
      TribitsExampleMetaProject/.

  TEST_2
    MESSAGE "Copy TribitsExampleProjectAddons to base dir"
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProjectAddons
      TribitsExampleMetaProject/.

  TEST_3
    MESSAGE "Configure enabling all packages using cmake/ExtraRepositoriesList.cmake"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${COMMON_ENV_ARGS_PASSTHROUGH}
      -DTribitsExMetaProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExMetaProj_ENABLE_Fortran=OFF
      -DTribitsExMetaProj_ENABLE_DEBUG=OFF
      -DTribitsExMetaProj_ENABLE_ALL_PACKAGES=ON
      -DTribitsExMetaProj_ENABLE_TESTS=ON
      TribitsExampleMetaProject
    PASS_REGULAR_EXPRESSION_ALL
      "Reading the list of extra repositories from .*cmake/ExtraRepositoriesList.cmake"
      "-- Adding POST extra Continuous repository TribitsExampleProject "
      "-- Adding POST extra Continuous repository TribitsExampleProject "
      "Reading list of native packages from .*/TribitsExampleMetaProject/PackagesList.cmake"
      "Reading list of native TPLs from .*/TribitsExampleMetaProject/TPLsList.cmake"
      "Reading list of POST extra packages from .*/TribitsExampleMetaProject/TribitsExampleProject/PackagesList.cmake"
      "Reading list of POST extra TPLs from .*/TribitsExampleMetaProject/TribitsExampleProject/TPLsList.cmake"
      "Reading list of POST extra packages from .*/TribitsExampleMetaProject/TribitsExampleProjectAddons/PackagesList.cmake"
      "Reading list of POST extra TPLs from .*/TribitsExampleMetaProject/TribitsExampleProjectAddons/TPLsList.cmake"
      "Final set of enabled SE packages:  SimpleCxx .* Addon1"
      "Processing enabled package: SimpleCxx [(]Libs, Tests, Examples[)]"
      "Processing enabled package: Addon1 [(]Libs, Tests, Examples[)]"
      "Configuring done"
      "Generating done"

  TEST_4 CMND make
    ARGS ${CTEST_BUILD_FLAGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Linking CXX executable Addon1_test.exe"
      "Built target Addon1_test"

  TEST_5 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    PASS_REGULAR_EXPRESSION_ALL
      "Test .*: Addon1_test .* Passed"
      "100% tests passed, 0 tests failed out of"

  TEST_6 CMND make
    ARGS ${CTEST_BUILD_FLAGS} clean

  TEST_7
    MESSAGE "Configure again enabling all packages using TribitsExMetaProj_PRE_REPOSITORIES and TribitsExMetaProj_EXTRA_REPOSITORIES only"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${COMMON_ENV_ARGS_PASSTHROUGH}
      -DTribitsExMetaProj_EXTRAREPOS_FILE=
      -DTribitsExMetaProj_PRE_REPOSITORIES=TribitsExampleProject
      -DTribitsExMetaProj_EXTRA_REPOSITORIES=TribitsExampleProjectAddons
      .
    PASS_REGULAR_EXPRESSION_ALL
      "Processing list of PRE extra repos from TribitsExMetaProj_PRE_REPOSITORIES='TribitsExampleProject'"
      "Reading list of PRE extra packages from .*/TribitsExampleMetaProject/TribitsExampleProject/PackagesList.cmake"
      "Reading list of PRE extra TPLs from .*/TribitsExampleMetaProject/TribitsExampleProject/TPLsList.cmake"
      "Reading list of native packages from .*/TribitsExampleMetaProject/PackagesList.cmake"
      "Reading list of native TPLs from .*/TribitsExampleMetaProject/TPLsList.cmake"
      "Reading list of POST extra packages from .*/TribitsExampleMetaProject/TribitsExampleProjectAddons/PackagesList.cmake"
      "Reading list of POST extra TPLs from .*/TribitsExampleMetaProject/TribitsExampleProjectAddons/TPLsList.cmake"
      "Final set of enabled SE packages:  SimpleCxx .* Addon1"
      "Processing enabled package: SimpleCxx [(]Libs, Tests, Examples[)]"
      "Processing enabled package: Addon1 [(]Libs, Tests, Examples[)]"
      "Configuring done"
      "Generating done"

  TEST_8 CMND make
    ARGS ${CTEST_BUILD_FLAGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Linking CXX executable Addon1_test.exe"
      "Built target Addon1_test"

  TEST_9 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    PASS_REGULAR_EXPRESSION_ALL
      "Test .*: Addon1_test .* Passed"
      "100% tests passed, 0 tests failed out of"

  )


tribits_add_advanced_test( TribitsExampleMetaProject_version_date_undef
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Copy TribitsExampleMetaProject"
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleMetaProject .

  TEST_1
    MESSAGE "Copy TribitsExampleProject to base dir"
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
      TribitsExampleMetaProject/.

  TEST_2
    MESSAGE "Copy TribitsExampleProjectAddons to base dir"
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProjectAddons
      TribitsExampleMetaProject/.

  TEST_3
    MESSAGE "Configure enabling all packages and generate version files"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${COMMON_ENV_ARGS_PASSTHROUGH}
      -DTribitsExMetaProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExMetaProj_ENABLE_Fortran=OFF
      -DTribitsExMetaProj_ENABLE_DEBUG=OFF
      -DTribitsExMetaProj_ENABLE_ALL_PACKAGES=ON
      -DTribitsExMetaProj_ENABLE_TESTS=ON
      -DTribitsExMetaProj_GENERATE_VERSION_DATE_FILES=TRUE
      -DTribitsExMetaProj_TRACE_FILE_PROCESSING=ON
      TribitsExampleMetaProject
    PASS_REGULAR_EXPRESSION_ALL
      "-- NOTE: Can't fill in version date files for TribitsExMetaProj since .*/TribitsExampleMetaProject/.git/ does not exist!"
      "-- File Trace: REPOSITORY CONFIGURE  .*/TribitsExMetaProj_version_date.h"
      "-- NOTE: Can't fill in version date files for TribitsExampleProject since .*/TribitsExampleMetaProject/TribitsExampleProject/.git/ does not exist!"
      "-- File Trace: REPOSITORY CONFIGURE  .*/TribitsExampleProject/TribitsExampleProject_version_date.h"
      "-- NOTE: Can't fill in version date files for TribitsExampleProjectAddons since .*/TribitsExampleMetaProject/TribitsExampleProjectAddons/.git/ does not exist!"
      "-- File Trace: REPOSITORY CONFIGURE  .*/TribitsExampleProjectAddons/TribitsExampleProjectAddons_version_date.h"

  TEST_4
    MESSAGE "Check that the TribitsExMetaProjec_version_date.h for undef macro"
    CMND cat
    ARGS TribitsExMetaProj_version_date.h
    PASS_REGULAR_EXPRESSION
      "#undef TRIBITSEXMETAPROJ_VERSION_DATE"

  TEST_5
    MESSAGE "Check TribitsExampleProject_version_date.h for undef macro"
    CMND cat
    ARGS TribitsExampleProject/TribitsExampleProject_version_date.h
    PASS_REGULAR_EXPRESSION
      "#undef TRIBITSEXAMPLEPROJECT_VERSION_DATE"

  TEST_6
    MESSAGE "Check TribitsExampleProjectAddons_version_date.h for undef macro"
    CMND cat
    ARGS TribitsExampleProjectAddons/TribitsExampleProjectAddons_version_date.h
    PASS_REGULAR_EXPRESSION
      "#undef TRIBITSEXAMPLEPROJECTADDONS_VERSION_DATE"

  )


########################################################################
# User error checking tests
########################################################################


tribits_add_advanced_test( TribitsExampleProject_PkgWithUserErrors_PASS
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Copy TribitsExampleProject so that we can copy in PkgWithUserErrors."
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject .

  TEST_1
    MESSAGE "Copy PkgWithUserErrors to base dir."
    CMND cp
    ARGS -r ${CMAKE_CURRENT_SOURCE_DIR}/PkgWithUserErrors
      TribitsExampleProject/.

  TEST_2
    MESSAGE "Configure PkgWithUserErrors"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_EXTRA_REPOSITORIES=PkgWithUserErrors
      -DTribitsExProj_ENABLE_PkgWithUserErrors=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Explicitly enabled packages on input [(]by user[)]:  PkgWithUserErrors 1"
      "Final set of enabled packages:  PkgWithUserErrors 1"
      "Processing enabled package: PkgWithUserErrors [(]Libs, Tests, Examples[)]"
      "Configuring done"
      "Generating done"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_3 CMND make
    ARGS ${CTEST_BUILD_FLAGS}
    PASS_REGULAR_EXPRESSION_ALL
      "Built target PkgWithUserErrors_PkgWithUserErrorsTest"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_4 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    PASS_REGULAR_EXPRESSION_ALL
      "Test [#]1: PkgWithUserErrors_PkgWithUserErrorsTest[_MPI1]* [.]+ +Passed"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  )


tribits_add_advanced_test( TribitsExampleProject_PkgWithUserErrors_PACKAGE_POST_PROCESS
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Copy TribitsExampleProject so that we can copy in PkgWithUserErrors."
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject .

  TEST_1
    MESSAGE "Copy PkgWithUserErrors to base dir."
    CMND cp
    ARGS -r ${CMAKE_CURRENT_SOURCE_DIR}/PkgWithUserErrors
      TribitsExampleProject/.

  TEST_2
    MESSAGE "Configure PkgWithUserErrors"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_EXTRA_REPOSITORIES=PkgWithUserErrors
      -DTribitsExProj_ENABLE_PkgWithUserErrors=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      -DPkgWithUserErrors_turn_off_passing_call_order=TRUE
      -DPkgWithUserErrors_no_POSTPROCESS_call=TRUE
      TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Processing enabled package: PkgWithUserErrors [(]Libs, Tests, Examples[)]"
      "ERROR: Forgot to call tribits_package_postprocess[(][)] .*/TribitsExampleProject/PkgWithUserErrors/CMakeLists.txt"
    ALWAYS_FAIL_ON_ZERO_RETURN
  )

tribits_add_advanced_test( TribitsExampleProject_PkgWithUserErrors_PACKAGE_INIT
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Copy TribitsExampleProject so that we can copy in PkgWithUserErrors."
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject .

  TEST_1
    MESSAGE "Copy PkgWithUserErrors to base dir."
    CMND cp
    ARGS -r ${CMAKE_CURRENT_SOURCE_DIR}/PkgWithUserErrors
      TribitsExampleProject/.

  TEST_2
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_EXTRA_REPOSITORIES=PkgWithUserErrors
      -DTribitsExProj_ENABLE_PkgWithUserErrors=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      -DPkgWithUserErrors_turn_off_passing_call_order=TRUE
      -DPkgWithUserErrors_ADD_LIBRARY_with_no_package_init=TRUE
      TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Must call tribits_package[(][)] or tribits_package_decl[(][)] before\n  tribits_add_library[(][)] in"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_3
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_EXTRA_REPOSITORIES=PkgWithUserErrors
      -DTribitsExProj_ENABLE_PkgWithUserErrors=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      -DPkgWithUserErrors_turn_off_passing_call_order=TRUE
      -DPkgWithUserErrors_ADD_LIBRARY_with_no_package_init=FALSE
      -DPkgWithUserErrors_ADD_EXECUTABLE_with_no_package_init=TRUE
      TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Must call tribits_package[(][)] or tribits_package_decl[(][)] before\n  tribits_add_executable[(][)] in"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_4
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_EXTRA_REPOSITORIES=PkgWithUserErrors
      -DTribitsExProj_ENABLE_PkgWithUserErrors=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      -DPkgWithUserErrors_turn_off_passing_call_order=TRUE
      -DPkgWithUserErrors_ADD_LIBRARY_with_no_package_init=FALSE
      -DPkgWithUserErrors_ADD_EXECUTABLE_with_no_package_init=FALSE
      -DPkgWithUserErrors_POSTPROCESS_with_no_package_init=TRUE
      TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Must call tribits_package[(][)] or tribits_package_def[(][)]"
      "tribits_package_postprocess[(][)]"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_5
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_EXTRA_REPOSITORIES=PkgWithUserErrors
      -DTribitsExProj_ENABLE_PkgWithUserErrors=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      -DPkgWithUserErrors_turn_off_passing_call_order=TRUE
      -DPkgWithUserErrors_ADD_LIBRARY_with_no_package_init=FALSE
      -DPkgWithUserErrors_ADD_EXECUTABLE_with_no_package_init=FALSE
      -DPkgWithUserErrors_POSTPROCESS_with_no_package_init=FALSE
      -DPkgWithUserErrors_multiple_calls_to_PACKAGE=TRUE
      TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Package .* declared more than once!"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_6
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_EXTRA_REPOSITORIES=PkgWithUserErrors
      -DTribitsExProj_ENABLE_PkgWithUserErrors=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      -DPkgWithUserErrors_multiple_calls_to_PACKAGE=FALSE
      -DPkgWithUserErrors_using_package_with_subpackage_commands=TRUE
      TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "The TriBITS Package 'PkgWithUserErrors' does not have any subpackages[.]"
      "Therefore, you are not allowed to call tribits_process_subpackages[(][)]!"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  )

tribits_add_advanced_test( TribitsExampleProject_PkgWithUserErrors_AFTER_POSTPROCESS
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Copy TribitsExampleProject so that we can copy in PkgWithUserErrors."
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject .

  TEST_1
    MESSAGE "Copy PkgWithUserErrors to base dir."
    CMND cp
    ARGS -r ${CMAKE_CURRENT_SOURCE_DIR}/PkgWithUserErrors
      TribitsExampleProject/.

  TEST_2
    MESSAGE "Configure PkgWithUserErrors"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_EXTRA_REPOSITORIES=PkgWithUserErrors
      -DTribitsExProj_ENABLE_PkgWithUserErrors=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      -DPkgWithUserErrors_turn_off_passing_call_order=TRUE
      -DPkgWithUserErrors_ADD_LIBRARY_after_POSTPROCESS=TRUE
      TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Must call tribits_add_library[(][)] before tribits_package_postprocess[(][)] in"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_3
    MESSAGE "Configure PkgWithUserErrors"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_EXTRA_REPOSITORIES=PkgWithUserErrors
      -DTribitsExProj_ENABLE_PkgWithUserErrors=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      -DPkgWithUserErrors_turn_off_passing_call_order=TRUE
      -DPkgWithUserErrors_ADD_LIBRARY_after_POSTPROCESS=FALSE
      -DPkgWithUserErrors_ADD_EXECUTABLE_after_POSTPROCESS=TRUE
      TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Must call tribits_add_executable[(][)] before tribits_package_postprocess[(][)] in"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_4
    MESSAGE "Configure PkgWithUserErrors"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_EXTRA_REPOSITORIES=PkgWithUserErrors
      -DTribitsExProj_ENABLE_PkgWithUserErrors=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      -DPkgWithUserErrors_turn_off_passing_call_order=TRUE
      -DPkgWithUserErrors_ADD_LIBRARY_after_POSTPROCESS=FALSE
      -DPkgWithUserErrors_ADD_EXECUTABLE_after_POSTPROCESS=FALSE
      -DPkgWithUserErrors_multiple_calls_to_POSTPROCESS=TRUE
      TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "tribits_package_postprocess[(][)] has been called more than once in"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  )

tribits_add_advanced_test( TribitsExampleProject_PkgWithUserErrors_UNPARSED_ARGS
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Copy TribitsExampleProject so that we can copy in PkgWithUserErrors."
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject .

  TEST_1
    MESSAGE "Copy PkgWithUserErrors to base dir."
    CMND cp
    ARGS -r ${CMAKE_CURRENT_SOURCE_DIR}/PkgWithUserErrors
      TribitsExampleProject/.

  TEST_2
    MESSAGE "Configure PkgWithUserErrors"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_CHECK_FOR_UNPARSED_ARGUMENTS=FATAL_ERROR
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_EXTRA_REPOSITORIES=PkgWithUserErrors
      -DTribitsExProj_ENABLE_PkgWithUserErrors=ON
      -DPkgWithUserErrors_UNPARSED_ARGS_DEFINE_DEPENDENCIES=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "CMake Error at.*TribitsGeneralMacros.cmake:"
      "Arguments are being passed in but not used.  UNPARSED_ARGUMENTS ="
      "nonsense_jdslkfhlskd"
      "tribits_read_toplevel_package_deps_files_add_to_graph"
      "-- Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_3
    MESSAGE "Configure PkgWithUserErrors"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_EXTRA_REPOSITORIES=PkgWithUserErrors
      -DTribitsExProj_ENABLE_PkgWithUserErrors=ON
      -DPkgWithUserErrors_UNPARSED_ARGS_DEFINE_DEPENDENCIES=OFF
      -DPkgWithUserErrors_turn_off_passing_call_order=TRUE
      -DPkgWithUserErrors_UNPARSED_ARGS_ADD_LIBRARY=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "CMake Error at.*TribitsGeneralMacros.cmake:"
      "Arguments are being passed in but not used.  UNPARSED_ARGUMENTS ="
      "this_shouldnt_be_here"
      "PkgWithUserErrors/CMakeLists.txt.*tribits_add_library"
      "-- Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_4
    MESSAGE "Configure PkgWithUserErrors"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_EXTRA_REPOSITORIES=PkgWithUserErrors
      -DTribitsExProj_ENABLE_PkgWithUserErrors=ON
      -DPkgWithUserErrors_UNPARSED_ARGS_DEFINE_DEPENDENCIES=OFF
      -DPkgWithUserErrors_turn_off_passing_call_order=TRUE
      -DPkgWithUserErrors_UNPARSED_ARGS_ADD_LIBRARY=OFF
      -DPkgWithUserErrors_UNPARSED_ARGS_ADD_EXECUTABLE=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "CMake Error at.*TribitsGeneralMacros.cmake:"
      "Arguments are being passed in but not used.  UNPARSED_ARGUMENTS ="
      "misspelled_argument"
      "PkgWithUserErrors/CMakeLists.txt.*tribits_add_executable"
      "-- Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN
  )


tribits_add_advanced_test( TribitsExampleProject_PkgWithSubpkgsWithUserErrors_PASS
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Copy TribitsExampleProject so that we can copy in PkgWithSubpkgsWithUserErrors."
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject .

  TEST_1
    MESSAGE "Copy PkgWithSubpkgsWithUserErrors to base dir."
    CMND cp
    ARGS -r ${CMAKE_CURRENT_SOURCE_DIR}/PkgWithSubpkgsWithUserErrors
      TribitsExampleProject/.

  TEST_2
    MESSAGE "Configure PkgWithSubpkgsWithUserErrors"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_EXTRA_REPOSITORIES=PkgWithSubpkgsWithUserErrors
      -DTribitsExProj_ENABLE_PkgWithSubpkgsWithUserErrors=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Explicitly enabled packages on input [(]by user[)]:  PkgWithSubpkgsWithUserErrors 1"
      "Final set of enabled packages:  PkgWithSubpkgsWithUserErrors 1"
      "Processing enabled package: PkgWithSubpkgsWithUserErrors [(]A, B, Tests, Examples[)]"
      "Configuring done"
      "Generating done"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_3 CMND make
    ARGS ${CTEST_BUILD_FLAGS}
    PASS_REGULAR_EXPRESSION_ALL
      "libpwswue_a"
      "libpwswue_b"
      "PkgWithSubpkgsWithUserErrorsA_a_test"
      "PkgWithSubpkgsWithUserErrorsB_b_test"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_4 CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    PASS_REGULAR_EXPRESSION_ALL
      "Test [#]1: PkgWithSubpkgsWithUserErrorsA_test_of_a [.]+ +Passed"
      "Test [#]2: PkgWithSubpkgsWithUserErrorsB_test_of_b [.]+ +Passed"
    ALWAYS_FAIL_ON_NONZERO_RETURN
  )

tribits_add_advanced_test( TribitsExampleProject_PkgWithSubpkgsWithUserErrors_PACKAGE_USER_ERRORS
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Copy TribitsExampleProject so that we can copy in PkgWithSubpkgsWithUserErrors."
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject .

  TEST_1
    MESSAGE "Copy PkgWithSubpkgsWithUserErrors to base dir."
    CMND cp
    ARGS -r ${CMAKE_CURRENT_SOURCE_DIR}/PkgWithSubpkgsWithUserErrors
      TribitsExampleProject/.

  TEST_2
    MESSAGE "Configure PkgWithSubpkgsWithUserErrors"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_EXTRA_REPOSITORIES=PkgWithSubpkgsWithUserErrors
      -DTribitsExProj_ENABLE_PkgWithSubpkgsWithUserErrors=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      -DPkgWithSubpkgsWithUserErrors_TURN_OFF_PASSING_CALL_ORDER=TRUE
      -DPkgWithSubpkgsWithUserErrors_no_PACKAGE_DECL_before_PROCESS_SUBPACKAGES=TRUE
      TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Must call tribits_package_decl[(][)] before tribits_process_subpackages[(][)]"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_3
    CMND ${CMAKE_COMMAND}
    ARGS
      -DPkgWithSubpkgsWithUserErrors_no_PACKAGE_DECL_before_PROCESS_SUBPACKAGES=FALSE
      -DPkgWithSubpkgsWithUserErrors_POSTPROCESS_before_SUBPACKAGES=TRUE
      .
    PASS_REGULAR_EXPRESSION_ALL
      " Must call tribits_package_decl[(][)], tribits_process_subpackages[(][)] and"
      " tribits_package_def[(][)] before tribits_package_postprocess[(][)].  Because this"
      " package has subpackages you cannot use tribits_package[(][)] you must call"
      " these in the following order: tribits_package_decl[(][)]"
      " tribits_process_subpackages[(][)] tribits_package_def[(][)]"
      " tribits_package_postprocess[(][)] in:"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_4
    CMND ${CMAKE_COMMAND}
    ARGS
      -DPkgWithSubpkgsWithUserErrors_POSTPROCESS_before_SUBPACKAGES=FALSE
      -DPkgWithSubpkgsWithUserErrors_PACKAGE_DEF_before_SUBPACKAGES=TRUE
      .
    PASS_REGULAR_EXPRESSION_ALL
      "Must call tribits_package_def[(][)] after tribits_process_subpackages[(][)]"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_5
    CMND ${CMAKE_COMMAND}
    ARGS
      -DPkgWithSubpkgsWithUserErrors_PACKAGE_DEF_before_SUBPACKAGES=FALSE
      -DPkgWithSubpkgsWithUserErrors_multiple_calls_to_PACKAGE_DECL=TRUE
      .
    PASS_REGULAR_EXPRESSION_ALL
      "tribits_package_decl[(][)] called more than once"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_6
    CMND ${CMAKE_COMMAND}
    ARGS
      -DPkgWithSubpkgsWithUserErrors_multiple_calls_to_PACKAGE_DECL=FALSE
      -DPkgWithSubpkgsWithUserErrors_multiple_calls_to_PACKAGE_DEF=TRUE
      .
    PASS_REGULAR_EXPRESSION_ALL
      "tribits_package_def[(][)] was called more than once"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_7
    CMND ${CMAKE_COMMAND}
    ARGS
      -DPkgWithSubpkgsWithUserErrors_multiple_calls_to_PACKAGE_DEF=FALSE
      -DPkgWithSubpkgsWithUserErrors_call_PACKAGE_from_package_with_subpackages=TRUE
      .
    PASS_REGULAR_EXPRESSION_ALL
      "This package has subpackages so you cannot use tribits_package[(][)]"
      "Instead use the following call order:"
      "tribits_project_decl[(]PkgWithSubpkgsWithUserErrors[)]"
      "tribits_process_subpackages[(][)]"
      "tribits_package_def[(][)]"
      "tribits_package_postprocess[(][)]"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_8
    CMND ${CMAKE_COMMAND}
    ARGS
      -DPkgWithSubpkgsWithUserErrors_call_PACKAGE_from_package_with_subpackages=FALSE
      -DPkgWithSubpkgsWithUserErrors_call_PACKAGE_after_PROCESS_SUBPACKAGES=TRUE
      .
    PASS_REGULAR_EXPRESSION_ALL
      "This package has subpackages so you cannot use tribits_package[(][)]"
      "Instead use the following call order"
      "tribits_project_decl[(]PkgWithSubpkgsWithUserErrors[)]"
      "tribits_process_subpackages[(][)]"
      "tribits_package_def[(][)]"
      "tribits_package_postprocess[(][)]"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_9
    CMND ${CMAKE_COMMAND}
    ARGS
      -DPkgWithSubpkgsWithUserErrors_call_PACKAGE_after_PROCESS_SUBPACKAGES=FALSE
      -DPkgWithSubpkgsWithUserErrors_call_everthing_except_PROCESS_SUBPACKAGES=TRUE
      .
    PASS_REGULAR_EXPRESSION_ALL
      " Must call tribits_package_decl[(][)], tribits_process_subpackages[(][)] and"
      " tribits_package_def[(][)] before tribits_package_postprocess[(][)].  Because this"
      " package has subpackages you cannot use tribits_package[(][)] you must call"
      " these in the following order: tribits_package_decl[(][)]"
      " tribits_process_subpackages[(][)] tribits_package_def[(][)]"
      " tribits_package_postprocess[(][)] in:"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_10
    CMND ${CMAKE_COMMAND}
    ARGS
      -DPkgWithSubpkgsWithUserErrors_call_everthing_except_PROCESS_SUBPACKAGES=FALSE
      -DPkgWithSubpkgsWithUserErrors_call_PACKAGE_DECL_only=TRUE
      .
    PASS_REGULAR_EXPRESSION_ALL
      " Must call tribits_package_decl[(][)], tribits_process_subpackages[(][)] and"
      " tribits_package_def[(][)] before tribits_package_postprocess[(][)].  Because this"
      " package has subpackages you cannot use tribits_package[(][)] you must call"
      " these in the following order: tribits_package_decl[(][)]"
      " tribits_process_subpackages[(][)] tribits_package_def[(][)]"
      " tribits_package_postprocess[(][)] in:"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_11
    CMND ${CMAKE_COMMAND}
    ARGS
      -DPkgWithSubpkgsWithUserErrors_call_PACKAGE_DECL_only=FALSE
      -DPkgWithSubpkgsWithUserErrors_call_SUBPACKAGE_from_package_with_subpackages=TRUE
      .
    PASS_REGULAR_EXPRESSION_ALL
      "Cannot call tribits_subpackage[(][)] from a package.  Use tribits_package[(][)]"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_12
    CMND ${CMAKE_COMMAND}
    ARGS
      -DPkgWithSubpkgsWithUserErrors_call_SUBPACKAGE_from_package_with_subpackages=FALSE
      -DPkgWithSubpkgsWithUserErrors_call_SUBPACKAGE_POSTPROCESS=TRUE
      .
    PASS_REGULAR_EXPRESSION_ALL
      "Cannot call tribits_subpackage_postprocess[(][)] from a package.  Use"
      " tribits_package_postprocess[(][)] instead"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  )


tribits_add_advanced_test( TribitsExampleProject_PkgWithSubpkgsWithUserErrors_SUBPACKAGE_USER_ERRORS
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Copy TribitsExampleProject so that we can copy in PkgWithSubpkgsWithUserErrors."
    CMND cp
    ARGS -r ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject .

  TEST_1
    MESSAGE "Copy PkgWithSubpkgsWithUserErrors to base dir."
    CMND cp
    ARGS -r ${CMAKE_CURRENT_SOURCE_DIR}/PkgWithSubpkgsWithUserErrors
      TribitsExampleProject/.

  TEST_2
    MESSAGE "Configure PkgWithSubpkgsWithUserErrors"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
      -DTribitsExProj_ENABLE_Fortran=OFF
      -DTribitsExProj_EXTRA_REPOSITORIES=PkgWithSubpkgsWithUserErrors
      -DTribitsExProj_ENABLE_PkgWithSubpkgsWithUserErrors=ON
      -DTribitsExProj_ENABLE_TESTS=ON
      -DsubpackageA_turn_off_passing_call_order=TRUE
      -DsubPackageA_call_PACKAGE=TRUE
      TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Cannot call tribits_package[(][)] in a subpackage"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_3
    CMND ${CMAKE_COMMAND}
    ARGS
      -DsubPackageA_call_PACKAGE=FALSE
      -DsubPackageA_call_PACKAGE_DECL=TRUE
      .
    PASS_REGULAR_EXPRESSION_ALL
      "Cannot call tribits_package_decl[(][)] in a subpackage"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_4
    CMND ${CMAKE_COMMAND}
    ARGS
      -DsubPackageA_call_PACKAGE_DECL=FALSE
      -DsubPackageA_call_PACKAGE_DEF=TRUE
      .
    PASS_REGULAR_EXPRESSION_ALL
      "Cannot call tribits_package_def[(][)] in a subpackage"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_5
    CMND ${CMAKE_COMMAND}
    ARGS
      -DsubPackageA_call_PACKAGE_DEF=FALSE
      -DsubPackageA_call_PROCESS_SUBPACKAGES=TRUE
      .
    PASS_REGULAR_EXPRESSION_ALL
      "Cannot call tribits_process_subpackages[(][)] in a subpackage"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_6
    CMND ${CMAKE_COMMAND}
    ARGS
      -DsubPackageA_call_PACKAGE_POSTPROCESS=TRUE
      -DsubPackageA_call_PROCESS_SUBPACKAGES=FALSE
      .
    PASS_REGULAR_EXPRESSION_ALL
      "Cannot call tribits_package_postprocess[(][)] in a subpackage"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_7
    CMND ${CMAKE_COMMAND}
    ARGS
      -DsubPackageA_call_PACKAGE_POSTPROCESS=FALSE
      -DsubPackageA_DOUBLE_SUBPACKAGE_INIT=TRUE
      .
    PASS_REGULAR_EXPRESSION_ALL
      "Already called tribits_subpackge[(][)] for the PkgWithSubpkgsWithUserErrors"
      "subpackage A"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_8
    CMND ${CMAKE_COMMAND}
    ARGS
      -DsubPackageA_DOUBLE_SUBPACKAGE_INIT=FALSE
      -DsubPAckageA_DOUBLE_SUBPACKAGE_POSTPROCESS=TRUE
      .
    PASS_REGULAR_EXPRESSION_ALL
      "Already called tribits_subpackge_postprocess[(][)] for the"
      "PkgWithSubpkgsWithUserErrors subpackage A"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_9
    CMND ${CMAKE_COMMAND}
    ARGS
      -DsubPackageA_no_SUBPACKAGE_before_POSTPROCESS=TRUE
      -DsubPAckageA_DOUBLE_SUBPACKAGE_POSTPROCESS=FALSE
      .
    PASS_REGULAR_EXPRESSION_ALL
      "tribits_subpackage[(][)] must be called before tribits_subpackage_postprocess[(][)]"
      " for the PkgWithSubpkgsWithUserErrors"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_10
    MESSAGE "Configure PkgWithSubpkgsWithUserErrors library after postprocess"
    CMND ${CMAKE_COMMAND}
    ARGS
      -DsubPackageA_no_SUBPACKAGE_before_POSTPROCESS=FALSE
      -DsubPackageA_ADD_LIBRARY_AFTER_POST_PROCESS=TRUE
      .
    PASS_REGULAR_EXPRESSION_ALL
      "Adding library in subpackage after post process"
      "Must call tribits_add_library[(][)] before tribits_subpackage_postprocess[(][)]"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_11
    MESSAGE "Configure PkgWithSubpkgsWithUserErrors exec after postprocess"
    CMND ${CMAKE_COMMAND}
    ARGS
      -DsubPackageA_ADD_LIBRARY_AFTER_POST_PROCESS=FALSE
      -DsubPackageA_ADD_EXECUTABLE_AFTER_POST_PROCESS=TRUE
      .
    PASS_REGULAR_EXPRESSION_ALL
      "Adding executable in subpackage after post process"
      "Must call tribits_add_executable[(][)] before tribits_subpackage_postprocess[(][)]"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_12
    MESSAGE "Configure PkgWithSubpkgsWithUserErrors lib with no preprocess"
    CMND ${CMAKE_COMMAND}
    ARGS
      -DsubPackageA_ADD_EXECUTABLE_AFTER_POST_PROCESS=FALSE
      -DsubPackageA_add_lib_no_PREPROCESS=TRUE
      .
    PASS_REGULAR_EXPRESSION_ALL
      "Must call tribits_subpackage[(][)] before tribits_add_library[(][)]"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_13
    MESSAGE "Configure PkgWithSubpkgsWithUserErrors exec with no preprocess"
    CMND ${CMAKE_COMMAND}
    ARGS
      -DsubPackageA_add_lib_no_PREPROCESS=FALSE
      -DsubPackageA_add_exe_no_PREPROCESS=TRUE
      .
    PASS_REGULAR_EXPRESSION_ALL
      "Must call tribits_subpackage[(][)] before tribits_add_executable[(][)]"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_14
    MESSAGE "Configure PkgWithSubpkgsWithUserErrors exec with no preprocess"
    CMND ${CMAKE_COMMAND}
    ARGS
      -DsubPackageA_add_exe_no_PREPROCESS=FALSE
      -DsubPackageA_call_ADD_TEST_DIRECTORY_without_SUBPACKAGE=TRUE
      .
    PASS_REGULAR_EXPRESSION_ALL
      "Must call tribits_subpackage[(][)] before tribits_add_test_directories[(][)]"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_15
    MESSAGE "Configure PkgWithSubpkgsWithUserErrors exec with no preprocess"
    CMND ${CMAKE_COMMAND}
    ARGS
      -DsubPackageA_call_ADD_TEST_DIRECTORY_without_SUBPACKAGE=FALSE
      -DsubPackageA_call_ADD_TEST_DIRECTORY_after_POSTPROCESS=TRUE
      .
    PASS_REGULAR_EXPRESSION_ALL
      "Must call tribits_add_test_directories[(][)] before"
      "tribits_subpackage_postprocess[(][)]"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_16
    MESSAGE "Configure PkgWithSubpkgsWithUserErrors exec with no preprocess"
    CMND ${CMAKE_COMMAND}
    ARGS
      -DsubPackageA_call_ADD_TEST_DIRECTORY_after_POSTPROCESS=FALSE
      -DsubPackageA_call_ADD_EXAMPLE_DIRECTORY_without_SUBPACKAGE=TRUE
      .
    PASS_REGULAR_EXPRESSION_ALL
      "Must call tribits_subpackage[(][)] before tribits_add_example_directories[(][)]"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  TEST_17
    MESSAGE "Configure PkgWithSubpkgsWithUserErrors exec with no preprocess"
    CMND ${CMAKE_COMMAND}
    ARGS
      -DsubPackageA_call_ADD_EXAMPLE_DIRECTORY_without_SUBPACKAGE=FALSE
      -DsubPackageA_call_ADD_EXAMPLE_DIRECTORY_after_POSTPROCESS=TRUE
      .
    PASS_REGULAR_EXPRESSION_ALL
      "Must call tribits_add_example_directories[(][)] before"
      "tribits_subpackage_postprocess[(][)]"
      "Configuring incomplete, errors occurred!"
    ALWAYS_FAIL_ON_ZERO_RETURN

  )


tribits_add_advanced_test( TribitsExampleProject_config_file_compiler_overrides
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0 CMND ${CMAKE_COMMAND}
    MESSAGE "Configure replacing the compilers listed in the generated Config.cmake files"
    ARGS
      ${TribitsExampleProject_COMMON_CONFIG_ARGS}
      -DCMAKE_CXX_COMPILER_FOR_CONFIG_FILE_BUILD_DIR=cxx_wrapper_build_dir
      -DCMAKE_C_COMPILER_FOR_CONFIG_FILE_BUILD_DIR=c_wrapper_build_dir
      -DCMAKE_Fortran_COMPILER_FOR_CONFIG_FILE_BUILD_DIR=fortran_wrapper_build_dir
      -DCMAKE_CXX_COMPILER_FOR_CONFIG_FILE_INSTALL_DIR=cxx_wrapper_install_dir
      -DCMAKE_C_COMPILER_FOR_CONFIG_FILE_INSTALL_DIR=c_wrapper_install_dir
      -DCMAKE_Fortran_COMPILER_FOR_CONFIG_FILE_INSTALL_DIR=fortran_wrapper_install_dir
      -DTribitsExProj_ENABLE_WithSubpackages=ON
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject
    PASS_REGULAR_EXPRESSION_ALL
      "Configuring done"
      "Generating done"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_1
    MESSAGE "Check complers set in TribitsExProjConfig_install.cmake"
    CMND grep
    ARGS _COMPILER TribitsExProjConfig_install.cmake
    PASS_REGULAR_EXPRESSION_ALL
      "set[(]TribitsExProj_CXX_COMPILER .cxx_wrapper_install_dir.[)]"
      "set[(]TribitsExProj_C_COMPILER .c_wrapper_install_dir.[)]"
      "set[(]TribitsExProj_Fortran_COMPILER .fortran_wrapper_install_dir.[)]"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_2
    MESSAGE "Check complers set in WithSubpackagesConfig_install.cmake"
    CMND grep
    ARGS _COMPILER packages/with_subpackages/CMakeFiles/WithSubpackagesConfig_install.cmake
    PASS_REGULAR_EXPRESSION_ALL
      "set[(]WithSubpackages_CXX_COMPILER .cxx_wrapper_install_dir.[)]"
      "set[(]WithSubpackages_C_COMPILER .c_wrapper_install_dir.[)]"
      "set[(]WithSubpackages_Fortran_COMPILER .fortran_wrapper_install_dir.[)]"
      "set[(]WithSubpackages_FORTRAN_COMPILER .fortran_wrapper_install_dir.[)]"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_3
    MESSAGE "Check complers set in WithSubpackagesConfig.cmake for build dir"
    CMND grep
    ARGS _COMPILER packages/with_subpackages/WithSubpackagesConfig.cmake
    PASS_REGULAR_EXPRESSION_ALL
      "set[(]WithSubpackages_CXX_COMPILER .cxx_wrapper_build_dir.[)]"
      "set[(]WithSubpackages_C_COMPILER .c_wrapper_build_dir.[)]"
      "set[(]WithSubpackages_Fortran_COMPILER .fortran_wrapper_build_dir.[)]"
      "set[(]WithSubpackages_FORTRAN_COMPILER .fortran_wrapper_build_dir.[)]"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  )
