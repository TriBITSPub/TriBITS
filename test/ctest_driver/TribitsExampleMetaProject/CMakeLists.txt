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


###############################################################################
#
# Strong automated testing of TribitsCTestDriverCore.cmake and 'dashboard'
# target using real TribitsExampleMetaProject including cloning git repos
#
###############################################################################

#
# Set up common vars/args for all direct CTest Driver tests
#

SET(TribitsExMetaProj_DIR "${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleMetaProject")

SET(COMMON_ENV_ARGS
  # Set back to default in case set in env
  CTEST_TEST_TYPE=
  TribitsExMetaProj_PACKAGES=
  CTEST_EXPLICITLY_ENABLE_IMPLICITLY_ENABLED_PACKAGES=
  CTEST_ENABLE_MODIFIED_PACKAGES_ONLY=OFF
  TribitsExMetaProj_PRE_REPOSITORIES=
  TribitsExMetaProj_EXTRA_REPOSITORIES=
  CTEST_BUILD_FLAGS=-j2
  CTEST_PARALLEL_LEVEL=1
  # Other args
  TribitsExMetaProj_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
  CTEST_DO_SUBMIT=OFF
  )

SET(CTEST_S_SCRIPT_ARGS
  ${CMAKE_CTEST_COMMAND} -V -S
    ${TribitsExMetaProj_DIR}/cmake/ctest/general_gcc/ctest_serial_debug.cmake
  )

#
# Set up arguments for direct configures of TribitsExampleMetaProject to test
# the 'dashboard' target.
#

INCLUDE("${CMAKE_CURRENT_LIST_DIR}/../../core/ExamplesUnitTests/GetCompilerPassthroughArgs.cmake")

SET(TribitsExampleMetaProject_COMMON_CONFIG_ARGS
  ${COMMON_ENV_ARGS_PASSTHROUGH}
  -DTribitsExMetaProj_ENABLE_Fortran=${${PROJECT_NAME}_ENABLE_Fortran}
  ${CTEST_DROP_SITE_CONFIG_ARGS}
  )


TRIBITS_ADD_ADVANCED_TEST( CTestDriver_TribitsExMetaProj_clone_default_branch_remote
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Run ctest driver with intial clone of the repos on the default branch and remote"
    CMND env
    ARGS
      CTEST_DASHBOARD_ROOT=PWD
      ${COMMON_ENV_ARGS}
      TribitsExMetaProj_ENABLE_SECONDARY_TESTED_CODE=TRUE
      CTEST_BUILD_NAME=CTestDriver_TribitsExMetaProj_clone_default_branch_remote
      ${CTEST_S_SCRIPT_ARGS}
    PASS_REGULAR_EXPRESSION_ALL
      "First perform the initial checkout: .*/git. clone -o origin  https://github.com/tribits/TribitsExampleMetaProject.git"
      "Perform checkout in directory: .*/TriBITS_CTestDriver_TribitsExMetaProj_clone_default_branch_remote"
      "Calling CTEST_UPDATE[(][)] to update base source repo '.*/TriBITS_CTestDriver_TribitsExMetaProj_clone_default_branch_remote/TribitsExampleMetaProject"
      "Old revision of repository is: 0cd597ff42eb91fce59bbbe9a712a3cae5879ff5"
      "New revision of repository is: 0cd597ff42eb91fce59bbbe9a712a3cae5879ff5"
      "CTEST_UPDATE[(][.][.][.][)] returned '0'"
      "cmake -P tribits_ctest_update_commands[.]cmake"
      "Git Update PASSED!"
      "TribitsExampleProject: Doing initial GIT clone/checkout from URL 'git@github[.]com:tribits/TribitsExampleProject' to dir 'TribitsExampleProject' [.][.][.]"
      "Cloning into 'TribitsExampleProject'[.][.][.]"
      "TribitsExampleProjectAddons: Doing initial GIT clone/checkout from URL 'git@github[.]com:tribits/TribitsExampleProjectAddons' to dir 'TribitsExampleProjectAddons' [.][.][.]"
      "Cloning into 'TribitsExampleProjectAddons'[.][.][.]"
      "Configure PASSED!"
      "Build PASSED!"
      "100% tests passed, 0 tests failed out of 11"
      "Addon1 .*=.*.* sec[*]proc [(]1 test[)]"
      "MixedLang .* =.*.* sec[*]proc [(]1 test[)]"
      "SimpleCxx .*=*.* sec[*]proc [(]2 tests[)]"
      "WithSubpackages .*=*.* sec[*]proc [(]6 tests[)]"
      "WrapExternal .*=*.* sec[*]proc [(]1 test[)]"
      "File '' does NOT exist so all tests passed!"
      "TRIBITS_CTEST_DRIVER: OVERALL: ALL PASSSED"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  # ToDo: Check the remote name 'origin' and branch 'master' in the cloned
  # repos

  # ToDo: Do the update, configure, build, and test again, except change the
  # branch to 'for-testing' in each repo

  # ToDo: Check the remote name 'origin' and branch 'for-testing' in the
  # cloned repos

  # ToDo: Check the TribitsExMetaProjRepoVersion.txt file

  # ToDo: Delete one of the extra repos

  # ToDo: Reset back the other repos to an ealier version

  # ToDo: Do the update, configure, build, and test again checking the repo
  # commands and output

  # ToDo: Check out a non-tracking branch in the base repo and an extra repo

  # ToDo: Do the update, configure, build, and test again checking the repo
  # commands and output

  # ToDo: Check the TribitsExMetaProjRepoVersion.txt file

  # ToDo: Do the update, configure, build, and test again, except change the
  # git URLs for the base and extra repos and make sure that it renames the
  # remotes correctly.  (This functionality is not implemented yet but it
  # needs to be.)

  # ToDo: Check the remote name 'github' and branch name 'for-testing' in the
  # cloned repos

  # ToDo: Check the TribitsExMetaProjRepoVersion.txt file

  )


# ToDo: Do fresh clone but using the remote name 'github' and branch 'for-testing'






