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
  set(LD_LIBRARY_PATH_HACK_FOR_SIMPLETPL_${sharedOrStatic}_ENVIRONMENT_ARG_ON
    ENVIRONMENT LD_LIBRARY_PATH=${SimpleTpl_install_${sharedOrStatic}_DIR}/install/lib)
  if (TRIBITS_ADD_LD_LIBRARY_PATH_HACK_FOR_SIMPLETPL)
    set(LD_LIBRARY_PATH_HACK_FOR_SIMPLETPL_${sharedOrStatic}_ENVIRONMENT_ARG
      ${LD_LIBRARY_PATH_HACK_FOR_SIMPLETPL_${sharedOrStatic}_ENVIRONMENT_ARG_ON})
  else()
    set(LD_LIBRARY_PATH_HACK_FOR_SIMPLETPL_${sharedOrStatic}_ENVIRONMENT_ARG "")
  endif()
  set(LD_LIBRARY_PATH_HACK_FOR_SIMPLETPL_${sharedOrStatic}_ENVIRONMENT_ARG_ON
    ${LD_LIBRARY_PATH_HACK_FOR_SIMPLETPL_${sharedOrStatic}_ENVIRONMENT_ARG_ON}
    PARENT_SCOPE)
  set(LD_LIBRARY_PATH_HACK_FOR_SIMPLETPL_${sharedOrStatic}_ENVIRONMENT_ARG
    ${LD_LIBRARY_PATH_HACK_FOR_SIMPLETPL_${sharedOrStatic}_ENVIRONMENT_ARG}
    PARENT_SCOPE)
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


function(TribitsExampleApp_ALL_ST_NoFortran_test sharedOrStatic fullOrComponents)

  if (sharedOrStatic STREQUAL "SHARED")
    set(buildSharedLibsArg -DBUILD_SHARED_LIBS=ON)
  elseif (sharedOrStatic STREQUAL "STATIC")
    set(buildSharedLibsArg -DBUILD_SHARED_LIBS=OFF)
  else()
    message(FATAL_ERROR "Invalid value of buildSharedLibsArg='${buildSharedLibsArg}'!")
  endif()

  if (fullOrComponents STREQUAL "FULL")
    set(tribitsExProjUseComponentsArg "")
  elseif (fullOrComponents STREQUAL "COMPONENTS")
    set(tribitsExProjUseComponentsArg
      -DTribitsExApp_USE_COMPONENTS=SimpleCxx,WithSubpackages)
  else()
    message(FATAL_ERROR "Invalid value of fullOrComponents='${fullOrComponents}'!")
  endif()

  set(testBaseName
    TribitsExampleApp_ALL_ST_NoFortran_${sharedOrStatic}_${fullOrComponents})
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
        ${tribitsExProjUseComponentsArg}
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


TribitsExampleApp_ALL_ST_NoFortran_test(STATIC FULL)
TribitsExampleApp_ALL_ST_NoFortran_test(STATIC COMPONENTS)
TribitsExampleApp_ALL_ST_NoFortran_test(SHARED COMPONENTS)
# NOTE: We don't need to test the permutation SHARED FULL as well.  That does
# not really test anything new.


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


function(TribitsExampleApp_ALL_ST_tpl_link_options_test byProjectOrPackage sharedOrStatic)

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

  set(testBaseName
    TribitsExampleApp_ALL_ST_tpl_link_options_${byProjectOrPackage}_${sharedOrStatic})
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
      MESSAGE "Write configuration fragment file to deal with semi-colon problem"
      CMND ${CMAKE_COMMAND}
      ARGS
        -DSIMPLE_TPL_INSTALL_BASE=${SimpleTpl_install_${sharedOrStatic}_DIR}/install
        -DLIBDIR_NAME=lib
        -DOUTPUT_CMAKE_FRAG_FILE="${testDir}/SimpleTplOpts.cmake"
        -P "${CMAKE_CURRENT_SOURCE_DIR}/write_simple_tpl_link_options_spec.cmake"

    TEST_2
      MESSAGE "Do the configure of TribitsExampleProject"
      WORKING_DIRECTORY BUILD
      CMND ${CMAKE_COMMAND}
      ARGS
        -C "${testDir}/SimpleTplOpts.cmake"
        ${TribitsExampleProject_COMMON_CONFIG_ARGS}
        -DTribitsExProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
        -DTribitsExProj_ENABLE_Fortran=ON
        -DTribitsExProj_ENABLE_ALL_PACKAGES=ON
        -DTribitsExProj_ENABLE_SECONDARY_TESTED_CODE=ON
        -DTribitsExProj_ENABLE_INSTALL_CMAKE_CONFIG_FILES=ON
        ${buildSharedLibsArg}
        -DCMAKE_INSTALL_PREFIX=${testDir}/install
        ${testDir}/TribitsExampleProject

    TEST_3
      MESSAGE "Build and install TribitsExampleProject locally"
      WORKING_DIRECTORY BUILD
      SKIP_CLEAN_WORKING_DIRECTORY
      CMND make ARGS ${CTEST_BUILD_FLAGS} install

    TEST_4
      MESSAGE "Delete source and build directory for TribitsExampleProject"
      CMND ${CMAKE_COMMAND} ARGS -E rm -rf TribitsExampleProject BUILD

    TEST_5
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

    TEST_6
      MESSAGE "Build TribitsExampleApp"
      WORKING_DIRECTORY app_build
      SKIP_CLEAN_WORKING_DIRECTORY
      CMND make ARGS ${CTEST_BUILD_FLAGS}
      PASS_REGULAR_EXPRESSION_ALL
        "Built target app"
      ALWAYS_FAIL_ON_NONZERO_RETURN

    TEST_7
      MESSAGE "Test TribitsExampleApp"
      WORKING_DIRECTORY app_build
      SKIP_CLEAN_WORKING_DIRECTORY
      CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
      PASS_REGULAR_EXPRESSION_ALL
        "Full Deps: WithSubpackages:B A simpletpl headeronlytpl simpletpl headeronlytpl[;] MixedLang:Mixed Language[;] SimpleCxx:simpletpl headeronlytpl"
        "app_test [.]+   Passed"
        "100% tests passed, 0 tests failed out of 1"
      ALWAYS_FAIL_ON_NONZERO_RETURN

    ${LD_LIBRARY_PATH_HACK_FOR_SIMPLETPL_${sharedOrStatic}_ENVIRONMENT_ARG_ON}

    ADDED_TEST_NAME_OUT ${testNameBase}_NAME
    )

  if (${testNameBase}_NAME)
    set_tests_properties(${${testNameBase}_NAME}
      PROPERTIES DEPENDS ${SimpleTpl_install_${sharedOrStatic}_NAME} )
  endif()

endfunction()
# NOTE: Above, it seems you always have to set LD_LIBRARY_PATH because CMake
# does not put in RPATH if you only specifiy the TPL directory using -L<dir>.
# If you use the entire library file, CMake will put in RPATH correctly.


TribitsExampleApp_ALL_ST_tpl_link_options_test(ByProject STATIC)
TribitsExampleApp_ALL_ST_tpl_link_options_test(ByProject SHARED)
TribitsExampleApp_ALL_ST_tpl_link_options_test(ByPackage STATIC)
TribitsExampleApp_ALL_ST_tpl_link_options_test(ByPackage SHARED)


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
        -DCMAKE_PREFIX_PATH=${testDir}/cmake_packages
        -DTribitsExApp_FIND_INDIVIDUAL_PACKAGES=TRUE
        -DTribitsExApp_USE_COMPONENTS=SimpleCxx,MixedLang,WithSubpackages
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
        "Full Deps: WithSubpackages:B A headeronlytpl headeronlytpl[;] MixedLang:Mixed Language[;] SimpleCxx:headeronlytpl"
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
