########################################################################
# TribitsExampleProject2
########################################################################


set(TribitsExampleProject2_COMMON_CONFIG_ARGS
  ${SERIAL_PASSTHROUGH_CONFIGURE_ARGS}
  -DTribitsExProj2_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
  -DTribitsExProj2_ENABLE_Fortran=${${PROJECT_NAME}_ENABLE_Fortran}
  )


########################################################################

set(testBaseName TribitsExampleProject2_install_config_again)
set(testName ${PACKAGE_NAME}_${testBaseName})
set(testDir "${CMAKE_CURRENT_BINARY_DIR}/${testName}")

tribits_add_advanced_test( ${testBaseName}

  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  ENVIRONMENT
    "CMAKE_PREFIX_PATH=${testDir}/install_tpl1"

  TEST_0
    MESSAGE "Configure Tpl1 to install"
    CMND ${CMAKE_COMMAND}
    WORKING_DIRECTORY build_tpl1
    ARGS
      ${SERIAL_PASSTHROUGH_CONFIGURE_ARGS}
      -DCMAKE_BUILD_TYPE=Release
      -DCMAKE_INSTALL_PREFIX=../install_tpl1
      -DCMAKE_INSTALL_LIBDIR=lib
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/tpls/Tpl1

  TEST_1
    MESSAGE "Make and install Tpl1"
    WORKING_DIRECTORY build_tpl1
    SKIP_CLEAN_WORKING_DIRECTORY
    CMND make ARGS install

  TEST_2
    MESSAGE "Configure TribitsExampleProject2 against Tpl1"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject2_COMMON_CONFIG_ARGS}
      -DCMAKE_BUILD_TYPE=DEBUG
      -DTribitsExProj2_ENABLE_TESTS=ON
      -DCMAKE_INSTALL_PREFIX=install
      -DTribitsExProj2_ENABLE_Package1=ON
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject2
    ALWAYS_FAIL_ON_NONZERO_RETURN
    PASS_REGULAR_EXPRESSION_ALL
      "Using find_package[(]Tpl1 [.][.][.][)] [.][.][.]"
      "Found Tpl1_DIR='.*/${testName}/install_tpl1/lib/cmake/Tpl1'"
      "-- Configuring done"
      "-- Generating done"

  TEST_3
    MESSAGE "Build Package2 and tests"
    CMND make
    ALWAYS_FAIL_ON_NONZERO_RETURN
    PASS_REGULAR_EXPRESSION_ALL
      "package1-helloworld"

  TEST_4
    MESSAGE "Run tests for Package2"
    CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    ALWAYS_FAIL_ON_NONZERO_RETURN
    PASS_REGULAR_EXPRESSION_ALL
      "Test.*Package1_HelloWorldProg.*Passed"
      "100% tests passed, 0 tests failed"

  TEST_5
    MESSAGE "Install Package 2"
    CMND make ARGS install
    ALWAYS_FAIL_ON_NONZERO_RETURN
    PASS_REGULAR_EXPRESSION_ALL
      "Tpl1Config.cmake"

  TEST_6
    MESSAGE "Remove configuration files for TribitsExampleProject2"
    CMND rm ARGS -r CMakeCache.txt CMakeFiles

  TEST_7
    MESSAGE "Configure  TribitsExampleProject2 against from scratch with install dir first in path"
    CMND ${CMAKE_COMMAND}
    ARGS
      #-C "${${testName}_CMAKE_PREFIX_PATH_file}"
      ${TribitsExampleProject2_COMMON_CONFIG_ARGS}
      -DCMAKE_BUILD_TYPE=DEBUG
      -DTribitsExProj2_ENABLE_TESTS=ON
      -DCMAKE_PREFIX_PATH="${testDir}/install"
      -DCMAKE_INSTALL_PREFIX=install
      -DTribitsExProj2_ENABLE_Package1=ON
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject2
    ALWAYS_FAIL_ON_NONZERO_RETURN
    PASS_REGULAR_EXPRESSION_ALL
      "Using find_package[(]Tpl1 [.][.][.][)] [.][.][.]"
      "Found Tpl1_DIR='.*/${testName}/install_tpl1/lib/cmake/Tpl1'"
      "-- Configuring done"
      "-- Generating done"

  )
  # Above, we set the cache var CMAKE_PREFIX_PATH=install and the env var
  # CMAKE_PREFIX_PATH=install_tpl1 so that find_package(Tpl1) will look in
  # install/ first for Tpl1Config.cmake before looking in install_tpl1/.
  # (Note that we have to set the cache var CMAKE_PREFIX_PATH=install to put
  # install/ in the search path ahead of install_tpl1/ for this simulation
  # since CMAKE_INSTALL_PREFIX, which initializes CMAKE_SYSTEM_PREFIX_PATH, is
  # searched after the env var CMAKE_PREFIX_PATH.)
  #
  # This test simulates the situation in bug #427 where CMAKE_INSTALL_PREFIX
  # (which initializes CMAKE_SYSTEM_PREFIX_PATH) is searched before PATH and
  # HDF5Config.cmake was getting found in CMAKE_INSTALL_PREFIX from a prior
  # install of Trilinos.  But since I don't want to mess with PATH for this
  # test, I just want to have find_package() search install/ before in
  # searches install_tpl1/ to simulate that scenario.  This test ensures that
  # find_package(Tpl1) will not does not find Tpl1Config.cmake just because
  # CMAKE_PREFIX_PATH is in the search path.
