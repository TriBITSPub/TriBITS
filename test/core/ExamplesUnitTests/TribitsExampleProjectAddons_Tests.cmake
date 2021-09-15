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
