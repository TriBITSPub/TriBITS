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
# TribitsExampleApp2
########################################################################


if (NOT "$ENV{TRIBITS_ADD_LD_LIBRARY_PATH_HACK_FOR_TPL1}" STREQUAL "")
  set(TRIBITS_ADD_LD_LIBRARY_PATH_HACK_FOR_TPL1_DEFAULT
    $ENV{TRIBITS_ADD_LD_LIBRARY_PATH_HACK_FOR_TPL1})
else()
  set($ENV{TRIBITS_ADD_LD_LIBRARY_PATH_HACK_FOR_TPL1} OFF)
endif()
advanced_set(TRIBITS_ADD_LD_LIBRARY_PATH_HACK_FOR_TPL1
  ${TRIBITS_ADD_LD_LIBRARY_PATH_HACK_FOR_TPL1_DEFAULT} CACHE BOOL
  "Set to TRUE to add LD_LIBRARY_PATH to libtpl1.so for platforms where RPATH not working")

function(set_LD_LIBRARY_PATH_HACK_FOR_TPL1_ENVIRONMENT_ARG sharedOrStatic)
  set(LD_LIBRARY_PATH_HACK_FOR_TPL1_${sharedOrStatic}_ENVIRONMENT_ARG_ON
    ENVIRONMENT LD_LIBRARY_PATH=${Tpl1_install_${sharedOrStatic}_DIR}/install/lib)
  if (TRIBITS_ADD_LD_LIBRARY_PATH_HACK_FOR_TPL1)
    set(LD_LIBRARY_PATH_HACK_FOR_TPL1_${sharedOrStatic}_ENVIRONMENT_ARG
      ${LD_LIBRARY_PATH_HACK_FOR_TPL1_${sharedOrStatic}_ENVIRONMENT_ARG_ON})
  else()
    set(LD_LIBRARY_PATH_HACK_FOR_TPL1_${sharedOrStatic}_ENVIRONMENT_ARG "")
  endif()
  set(LD_LIBRARY_PATH_HACK_FOR_TPL1_${sharedOrStatic}_ENVIRONMENT_ARG_ON
    ${LD_LIBRARY_PATH_HACK_FOR_TPL1_${sharedOrStatic}_ENVIRONMENT_ARG_ON}
    PARENT_SCOPE)
  set(LD_LIBRARY_PATH_HACK_FOR_TPL1_${sharedOrStatic}_ENVIRONMENT_ARG
    ${LD_LIBRARY_PATH_HACK_FOR_TPL1_${sharedOrStatic}_ENVIRONMENT_ARG}
    PARENT_SCOPE)
endfunction()
set_LD_LIBRARY_PATH_HACK_FOR_TPL1_ENVIRONMENT_ARG(STATIC)
set_LD_LIBRARY_PATH_HACK_FOR_TPL1_ENVIRONMENT_ARG(SHARED)
# NOTE: Above, we have to set LD_LIBRARY_PATH to pick up the
# libtpl1.so because CMake 3.17.5 and 3.21.2 with the GitHub Actions
# Umbuntu build is refusing to put in the RPATH for libtpl1.so into
# libsimplecxx.so even through CMAKE_INSTALL_RPATH_USE_LINK_PATH=ON is
# set.  This is not needed for the RHEL 7 builds that I have tried where
# CMake is behaving correctly and putting in RPATH correctly.  But because
# I can't log into this system, it is very hard and time consuming to
# debug this so I am just giving up at this point.


################################################################################


set(tribitsExProj2TestNameBaseBase TribitsExampleProject2_find_tpl_parts)
set(sharedOrStatic STATIC)
set(fullOrComponents COMPONENTS)

set(testBaseName
  TribitsExampleApp2_find_package_missing_component_error_msg)
set(testName ${PACKAGE_NAME}_${testBaseName})
set(testDir ${CMAKE_CURRENT_BINARY_DIR}/${testName})

tribits_add_advanced_test( ${testBaseName}
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1
  XHOSTTYPE Darwin

  TEST_0
    MESSAGE "Configure TribitsExampleApp2 locally against already installed TribitsExProject2"
    WORKING_DIRECTORY app_build
    CMND ${CMAKE_COMMAND} ARGS
      -DCMAKE_PREFIX_PATH=${${tribitsExProj2TestNameBaseBase}_${sharedOrStatic}_INSTALL_DIR}
      -DTribitsExApp2_USE_COMPONENTS=PackageDoesNotExist
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleApp2
    PASS_REGULAR_EXPRESSION_ALL
      "ERROR: Could not find component 'PackageDoesNotExist'"
      "-- Configuring incomplete, errors occurred"
    ALWAYS_FAIL_ON_ZERO_RETURN

  ${LD_LIBRARY_PATH_HACK_FOR_TPL1_${sharedOrStatic}_ENVIRONMENT_ARG}

  ADDED_TEST_NAME_OUT ${testNameBase}_NAME
  )
# NOTE: Above test checks that searched-for required components that are not
# founds emit the correct error message from CMake

if (${testNameBase}_NAME)
  set_tests_properties(${${testNameBase}_NAME}
    PROPERTIES DEPENDS ${${tribitsExProj2TestNameBaseBase}_${sharedOrStatic}_NAME} )
endif()


################################################################################


function(TribitsExampleApp2_test  tribitsExProj2TestNameBaseBase
    sharedOrStatic  fullOrComponents
  )

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
      -DTribitsExApp2_USE_COMPONENTS=Package1)
  else()
    message(FATAL_ERROR "Invalid value of fullOrComponents='${fullOrComponents}'!")
  endif()

  set(testBaseName
    TribitsExampleApp2_${tribitsExProj2TestNameBaseBase}_${sharedOrStatic}_${fullOrComponents})
  set(testName ${PACKAGE_NAME}_${testBaseName})
  set(testDir ${CMAKE_CURRENT_BINARY_DIR}/${testName})

  tribits_add_advanced_test( ${testBaseName}
    OVERALL_WORKING_DIRECTORY TEST_NAME
    OVERALL_NUM_MPI_PROCS 1
    XHOSTTYPE Darwin

    TEST_0
      MESSAGE "Configure TribitsExampleApp2 locally against already installed TribitsExProject2"
      WORKING_DIRECTORY app_build
      CMND ${CMAKE_COMMAND} ARGS
        -DCMAKE_PREFIX_PATH=${${tribitsExProj2TestNameBaseBase}_${sharedOrStatic}_INSTALL_DIR}
        ${tribitsExProjUseComponentsArg}
        ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleApp2
      PASS_REGULAR_EXPRESSION_ALL
        "-- Configuring done"
        "-- Generating done"
        "-- Build files have been written to: .*/${testName}/app_build"
      ALWAYS_FAIL_ON_NONZERO_RETURN

    TEST_1
      MESSAGE "Build TribitsExampleApp2"
      WORKING_DIRECTORY app_build
      SKIP_CLEAN_WORKING_DIRECTORY
      CMND make ARGS ${CTEST_BUILD_FLAGS}
      PASS_REGULAR_EXPRESSION_ALL
        "Built target app"
      ALWAYS_FAIL_ON_NONZERO_RETURN

    TEST_2
      MESSAGE "Test TribitsExampleApp2"
      WORKING_DIRECTORY app_build
      SKIP_CLEAN_WORKING_DIRECTORY
      CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
      PASS_REGULAR_EXPRESSION_ALL
        "Full Deps: Package1: tpl1"
        "app_test [.]+   Passed"
        "100% tests passed, 0 tests failed out of 1"
      ALWAYS_FAIL_ON_NONZERO_RETURN

    ${LD_LIBRARY_PATH_HACK_FOR_TPL1_${sharedOrStatic}_ENVIRONMENT_ARG}

    ADDED_TEST_NAME_OUT ${testNameBase}_NAME
    )
  # NOTE: Above test deletes the source and build dir for
  # TribitsExampleProject after the install to ensure that the install dir is
  # stand-alone.

  if (${testNameBase}_NAME)
    set_tests_properties(${${testNameBase}_NAME}
      PROPERTIES DEPENDS ${${tribitsExProj2TestNameBaseBase}_${sharedOrStatic}_NAME} )
  endif()

endfunction()


TribitsExampleApp2_test(TribitsExampleProject2_find_tpl_parts STATIC FULL)
# NOTE: We don't need to test the permutation SHARED FULL as well.  That does
# not really test anything new given that shared is tested with COMPONENTS.
TribitsExampleApp2_test(TribitsExampleProject2_find_tpl_parts STATIC COMPONENTS)
TribitsExampleApp2_test(TribitsExampleProject2_find_tpl_parts SHARED COMPONENTS)
TribitsExampleApp2_test(TribitsExampleProject2_explicit_tpl_vars STATIC COMPONENTS)
TribitsExampleApp2_test(TribitsExampleProject2_find_package SHARED COMPONENTS)
TribitsExampleApp2_test(TribitsExampleProject2_find_package STATIC COMPONENTS)
