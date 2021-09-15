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


########################################################################
# TribitsExampleApp
########################################################################


if (NOT "$ENV{TRIBITS_ADD_LD_LIBRARY_PATH_HACK_FOR_SIMPLETPL}" STREQUAL "")
  set(TRIBITS_ADD_LD_LIBRARY_PATH_HACK_FOR_SIMPLETPL_DEFAULT
    $ENV{TRIBITS_ADD_LD_LIBRARY_PATH_HACK_FOR_SIMPLETPL})
else()
  set($ENV{TRIBITS_ADD_LD_LIBRARY_PATH_HACK_FOR_SIMPLETPL} OFF)
endif()
advanced_set(TRIBITS_ADD_LD_LIBRARY_PATH_HACK_FOR_SIMPLETPL
  ${TRIBITS_ADD_LD_LIBRARY_PATH_HACK_FOR_SIMPLETPL_DEFAULT} CACHE BOOL
  "Set to TRUE to add LD_LIBRARY_PATH to libsimpletpl.so for platforms where RPATH not working")

function(set_LD_LIBRARY_PATH_HACK_FOR_SIMPLETPL_ENVIRONMENT_ARG sharedOrStatic)
  if (TRIBITS_ADD_LD_LIBRARY_PATH_HACK_FOR_SIMPLETPL)
    set(LD_LIBRARY_PATH_HACK_FOR_SIMPLETPL_${sharedOrStatic}_ENVIRONMENT_ARG
      ENVIRONMENT LD_LIBRARY_PATH=${SimpleTpl_install_${sharedOrStatic}_DIR}/install/lib)
  else()
    set(LD_LIBRARY_PATH_HACK_FOR_SIMPLETPL_${sharedOrStatic}_ENVIRONMENT_ARG "")
  endif()
endfunction()
set_LD_LIBRARY_PATH_HACK_FOR_SIMPLETPL_ENVIRONMENT_ARG(STATIC)
set_LD_LIBRARY_PATH_HACK_FOR_SIMPLETPL_ENVIRONMENT_ARG(SHARED)
# NOTE: Above, we have to set LD_LIBRARY_PATH to pick up the
# libsimpletpl.so because CMake 3.17.5 and 3.21.2 with the GitHub Actions
# Umbuntu build is refusing to put in the RPATH for libsimpletpl.so into
# libsimplecxx.so even through CMAKE_INSTALL_RPATH_USE_LINK_PATH=ON is
# set.  This is not needed for the RHEL 7 builds that I have tried where
# CMake is behaving correctly and putting in RPATH correctly.  But because
# I can't log into this system, it is very hard and time consuming to
# debug this so I am just giving up at this point.


function(TribitsExampleApp_ALL_ST_NoFortran_test sharedOrStatic)

  if (sharedOrStatic STREQUAL "SHARED")
    set(buildSharedLibsArg -DBUILD_SHARED_LIBS=ON)
  else()
    set(buildSharedLibsArg -DBUILD_SHARED_LIBS=OFF)
  endif()

  set(testBaseName TribitsExampleApp_ALL_ST_NoFortran_${sharedOrStatic})
  set(testName ${PACKAGE_NAME}_${testBaseName})
  set(testDir ${CMAKE_CURRENT_BINARY_DIR}/${testName})

  tribits_add_advanced_test( ${testBaseName}
    OVERALL_WORKING_DIRECTORY TEST_NAME
    OVERALL_NUM_MPI_PROCS 1
    XHOSTTYPE Darwin

    TEST_0
      MESSAGE "Copy source for TribitsExampleProject"
      CMND ${CMAKE_COMMAND}
      ARGS -E copy_directory
        ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject .
      WORKING_DIRECTORY TribitsExampleProject

    TEST_1
      MESSAGE "Do the configure of TribitsExampleProject"
      WORKING_DIRECTORY BUILD
      CMND ${CMAKE_COMMAND}
      ARGS
        ${TribitsExampleProject_COMMON_CONFIG_ARGS}
        -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
        -DTribitsExProj_ENABLE_Fortran=OFF
        -DTribitsExProj_ENABLE_ALL_PACKAGES=ON
        -DTribitsExProj_ENABLE_SECONDARY_TESTED_CODE=ON
        -DTribitsExProj_ENABLE_INSTALL_CMAKE_CONFIG_FILES=ON
        -DTPL_ENABLE_SimpleTpl=ON
        -DSimpleTpl_INCLUDE_DIRS=${SimpleTpl_install_${sharedOrStatic}_DIR}/install/include
        -DSimpleTpl_LIBRARY_DIRS=${SimpleTpl_install_${sharedOrStatic}_DIR}/install/lib
        ${buildSharedLibsArg}
        -DCMAKE_INSTALL_PREFIX=${testDir}/install
        ${testDir}/TribitsExampleProject

    TEST_2
      MESSAGE "Build and install TribitsExampleProject locally"
      WORKING_DIRECTORY BUILD
      SKIP_CLEAN_WORKING_DIRECTORY
      CMND make ARGS ${CTEST_BUILD_FLAGS} install

    TEST_3
      MESSAGE "Delete source and build directory for TribitsExampleProject"
      CMND ${CMAKE_COMMAND} ARGS -E rm -rf TribitsExampleProject BUILD

    TEST_4
      MESSAGE "Configure TribitsExampleApp locally"
      WORKING_DIRECTORY app_build
      CMND ${CMAKE_COMMAND} ARGS
        -DCMAKE_PREFIX_PATH=${testDir}/install
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

    ${LD_LIBRARY_PATH_HACK_FOR_SIMPLETPL_${sharedOrStatic}_ENVIRONMENT_ARG}

    ADDED_TEST_NAME_OUT ${testNameBase}_NAME
    )
  # NOTE: Above test deletes the source and build dir for
  # TribitsExampleProject after the install to ensure that the install dir is
  # stand-alone.

  if (${testNameBase}_NAME)
    set_tests_properties(${${testNameBase}_NAME}
      PROPERTIES DEPENDS ${SimpleTpl_install_${sharedOrStatic}_NAME} )
  endif()

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
  set(testDir ${CMAKE_CURRENT_BINARY_DIR}/${testName})

  tribits_add_advanced_test( ${testBaseName}
    OVERALL_WORKING_DIRECTORY TEST_NAME
    OVERALL_NUM_MPI_PROCS 1
    EXCLUDE_IF_NOT_TRUE ${PROJECT_NAME}_ENABLE_Fortran
    XHOSTTYPE Darwin

    TEST_0
      MESSAGE "Copy source for TribitsExampleProject"
      CMND ${CMAKE_COMMAND}
      ARGS -E copy_directory
        ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject .
      WORKING_DIRECTORY TribitsExampleProject

    TEST_1
      MESSAGE "Do the configure of TribitsExampleProject"
      WORKING_DIRECTORY BUILD
      CMND ${CMAKE_COMMAND}
      ARGS
        ${TribitsExampleProject_COMMON_CONFIG_ARGS}
        -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
        -DTribitsExProj_ENABLE_Fortran=ON
        -DTribitsExProj_ENABLE_ALL_PACKAGES=ON
        -DTribitsExProj_ENABLE_SECONDARY_TESTED_CODE=ON
        -DTribitsExProj_ENABLE_INSTALL_CMAKE_CONFIG_FILES=ON
        -DTPL_ENABLE_SimpleTpl=ON
        -DSimpleTpl_INCLUDE_DIRS=${SimpleTpl_install_${sharedOrStatic}_DIR}/install/include
        -DSimpleTpl_LIBRARY_DIRS=${SimpleTpl_install_${sharedOrStatic}_DIR}/install/lib
        ${buildSharedLibsArg}
        -DCMAKE_INSTALL_PREFIX=${testDir}/install
        ${testDir}/TribitsExampleProject

    TEST_2
      MESSAGE "Build and install TribitsExampleProject locally"
      WORKING_DIRECTORY BUILD
      SKIP_CLEAN_WORKING_DIRECTORY
      CMND make ARGS ${CTEST_BUILD_FLAGS} install

    TEST_3
      MESSAGE "Delete source and build directory for TribitsExampleProject"
      CMND ${CMAKE_COMMAND} ARGS -E rm -rf TribitsExampleProject BUILD

    TEST_4
      MESSAGE "Configure TribitsExampleApp locally"
      WORKING_DIRECTORY app_build
      CMND ${CMAKE_COMMAND} ARGS
        -DCMAKE_PREFIX_PATH=${testDir}/install
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

    ${LD_LIBRARY_PATH_HACK_FOR_SIMPLETPL_${sharedOrStatic}_ENVIRONMENT_ARG}

    ADDED_TEST_NAME_OUT ${testNameBase}_NAME
    )

  if (${testNameBase}_NAME)
    set_tests_properties(${${testNameBase}_NAME}
      PROPERTIES DEPENDS ${SimpleTpl_install_${sharedOrStatic}_NAME} )
  endif()

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
  set(testDir ${CMAKE_CURRENT_BINARY_DIR}/${testName})

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
        -DTribitsExApp_FIND_UNDER_BUILD_DIR=${testDir}
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
# subpackages which are SimpleCxx and MixedLang.  It seems that whoever
# implemented the <Package>Config.cmake files in the build dir only got this
# working for top-level packages that don't have any subpackages.  This test
# above at least (partially) pins down what already works.  (Later, these
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
