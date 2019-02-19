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

##########################################################################################
#
# Test TRIBITS_CTEST_DRIVER() using real git clones
#
# NOTE: To get these tests to work on some systems, one may need to switch
# away from 'https://github.com/' to using 'git@github.com:' using:
#
#   export TribitsExMetaProj_GIT_URL_REPO_BASE=git@github.com:tribits/
#
# before configuring.
#
##########################################################################################


TRIBITS_ADD_ADVANCED_TEST( CTestDriver_TribitsExMetaProj_clone_default_branch_remote
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Run ctest driver with intial clone of the repos on the default branch 'master' and remote 'origin'"
    CMND env
    ARGS
      CTEST_DASHBOARD_ROOT=PWD
      ${COMMON_ENV_ARGS}
      TribitsExMetaProj_ENABLE_SECONDARY_TESTED_CODE=TRUE
      CTEST_BUILD_NAME=CTestDriver_TribitsExMetaProj_clone_default_branch_remote
      ${CTEST_S_SCRIPT_ARGS}
    PASS_REGULAR_EXPRESSION_ALL
      "CTEST_NOTES_FILES=''"
      "First perform the initial checkout: .*/git. clone -o origin .*github.com.tribits/TribitsExampleMetaProject.git"
      "Perform checkout in directory: .*/TriBITS_CTestDriver_TribitsExMetaProj_clone_default_branch_remote"
      "Calling CTEST_UPDATE[(][)] to update base source repo '.*/TriBITS_CTestDriver_TribitsExMetaProj_clone_default_branch_remote/TribitsExampleMetaProject"
      "Old revision of repository is: [a-z0-9]+"
      "New revision of repository is: [a-z0-9]+"
      "CTEST_UPDATE[(][.][.][.][)] returned '0'"
      "cmake -P tribits_ctest_update_commands[.]cmake"
      "Git Update PASSED!"
      "TribitsExampleProject: Doing initial GIT clone/checkout from URL '.*github[.]com.tribits/TribitsExampleProject.git' to dir 'TribitsExampleProject' [.][.][.]"
      "Cloning into 'TribitsExampleProject'[.][.][.]"
      "TribitsExampleProjectAddons: Doing initial GIT clone/checkout from URL '.*github[.]com.tribits/TribitsExampleProjectAddons.git' to dir 'TribitsExampleProjectAddons' [.][.][.]"
      "Cloning into 'TribitsExampleProjectAddons'[.][.][.]"
      "CTEST_NOTES_FILES_WO_CACHE='.*/TriBITS_CTestDriver_TribitsExMetaProj_clone_default_branch_remote/BUILD/UpdateCommandsOutput.txt'"
      "Configure PASSED!"
       "CTEST_NOTES_FILES='.*/TriBITS_CTestDriver_TribitsExMetaProj_clone_default_branch_remote/BUILD/TribitsExMetaProjRepoVersion.txt[;].*/TriBITS_CTestDriver_TribitsExMetaProj_clone_default_branch_remote/BUILD/UpdateCommandsOutput.txt[;].*/TriBITS_CTestDriver_TribitsExMetaProj_clone_default_branch_remote/BUILD/CMakeCache.clean.txt'"
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

  TEST_1
    MESSAGE "Check that base repo has correct remote"
    CMND git ARGS remote -v
    WORKING_DIRECTORY TribitsExampleMetaProject
    SKIP_CLEAN_WORKING_DIRECTORY
    PASS_REGULAR_EXPRESSION_ALL
      "origin.*.*github[.]com.tribits/TribitsExampleMetaProject[.]git"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_2
    MESSAGE "Check that base repo is on the correct branch"
    CMND git ARGS branch
    WORKING_DIRECTORY TribitsExampleMetaProject
    SKIP_CLEAN_WORKING_DIRECTORY
    PASS_REGULAR_EXPRESSION_ALL
      "[*].*master"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_3
    MESSAGE "Check that one of the extra repos has correct remote"
    CMND git ARGS remote -v
    WORKING_DIRECTORY TribitsExampleMetaProject/TribitsExampleProject
    SKIP_CLEAN_WORKING_DIRECTORY
    PASS_REGULAR_EXPRESSION_ALL
      "origin.*.*github[.]com.tribits/TribitsExampleProject[.]git"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_4
    MESSAGE "Check that one of the extra repos in on the correct branch"
    CMND git ARGS branch
    WORKING_DIRECTORY TribitsExampleMetaProject/TribitsExampleProject
    SKIP_CLEAN_WORKING_DIRECTORY
    PASS_REGULAR_EXPRESSION_ALL
      "[*].*master"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_5
    MESSAGE "Run ctest driver with an update changing to the branch 'for-testing'"
    CMND env
    ARGS
      CTEST_DASHBOARD_ROOT=PWD
      ${COMMON_ENV_ARGS}
      CTEST_START_WITH_EMPTY_BINARY_DIRECTORY=FALSE
      CTEST_WIPE_CACHE=FALSE
      TribitsExMetaProj_ENABLE_SECONDARY_TESTED_CODE=TRUE
      TribitsExMetaProj_BRANCH=for-testing
      CTEST_NOTES_FILES=${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleMetaProject/README
      CTEST_BUILD_NAME=CTestDriver_TribitsExMetaProj_clone_default_branch_remote
      ${CTEST_S_SCRIPT_ARGS}
    PASS_REGULAR_EXPRESSION_ALL
      "-- ENV_CTEST_NOTES_FILES='.*/tribits/examples/TribitsExampleMetaProject/README'"
      "-- CTEST_NOTES_FILES='.*/tribits/examples/TribitsExampleMetaProject/README'"
      "-- ENV_TribitsExMetaProj_BRANCH='for-testing'"
      "-- TribitsExMetaProj_BRANCH='for-testing'"
      "Calling CTEST_UPDATE[(][)] to update base source repo '.*/TriBITS_CTestDriver_TribitsExMetaProj_clone_default_branch_remote/TribitsExampleMetaProject"
      "Old revision of repository is: [a-z0-9]+"
      "New revision of repository is: 56877b3b3dd06f41dfb27cedcedc2693aafaef03"
      "CTEST_UPDATE[(][.][.][.][)] returned '[0-9]+'"
      "cmake -P tribits_ctest_update_commands[.]cmake"
      "Running: .*/git checkout -B for-testing --track origin/for-testing"
      "Switched to a new branch 'for-testing'"
      "Branch for-testing set up to track remote branch for-testing from origin."
      "Git Update PASSED!"
      "For extra repos, doing switch to branch for-testing"
      "TribitsExampleProject: Doing GIT update from URL '.*github[.]com.tribits/TribitsExampleProject[.]git' to dir '.*/TribitsExampleProject' [.][.][.]"
      "TribitsExampleProjectAddons: Doing GIT update from URL '.*github[.]com.tribits/TribitsExampleProjectAddons[.]git' to dir '.*/TribitsExampleProjectAddons' [.][.][.]"
      "CTEST_NOTES_FILES_WO_CACHE='.*/BUILD/Updates.txt[;].*/BUILD/UpdateCommandsOutput.txt[;].*/tribits/examples/TribitsExampleMetaProject/README'"
      "Configure PASSED!"
      "CTEST_NOTES_FILES='.*/BUILD/TribitsExMetaProjRepoVersion.txt[;].*/BUILD/Updates.txt[;].*/BUILD/UpdateCommandsOutput.txt[;].*/tribits/examples/TribitsExampleMetaProject/README[;].*/BUILD/CMakeCache.clean.txt'"
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

  TEST_6
    MESSAGE "Check that base repo is on the correct branch"
    CMND git ARGS branch
    WORKING_DIRECTORY TribitsExampleMetaProject
    SKIP_CLEAN_WORKING_DIRECTORY
    PASS_REGULAR_EXPRESSION_ALL
      "[*].*for-testing"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_7
    MESSAGE "Check that one of the extra repos in on the correct branch"
    CMND git ARGS branch
    WORKING_DIRECTORY TribitsExampleMetaProject/TribitsExampleProject
    SKIP_CLEAN_WORKING_DIRECTORY
    PASS_REGULAR_EXPRESSION_ALL
      "[*].*for-testing"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_8
    MESSAGE "Make sure that the file TribitsExMetaProjRepoVersion.txt is correct"
    CMND diff ARGS 
      "${CMAKE_CURRENT_LIST_DIR}/data/TribitsExMetaProjRepoVersion.for-testing.txt"
      BUILD/TribitsExMetaProjRepoVersion.txt 
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_9
    MESSAGE "Remove one of the git repos to make sure that it clones again"
    CMND rm ARGS -rf TribitsExampleMetaProject/TribitsExampleProjectAddons
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_10
    MESSAGE "Reset other repos back to an earlier version so we can simulate and update"
    CMND "${${PROJECT_NAME}_TRIBITS_DIR}/python_utils/gitdist"
    ARGS --dist-no-color --dist-repos=.,TribitsExampleProject reset --hard HEAD^
    WORKING_DIRECTORY TribitsExampleMetaProject
    SKIP_CLEAN_WORKING_DIRECTORY
    PASS_REGULAR_EXPRESSION_ALL
      "[*][*][*] Base Git Repo: TribitsExampleMetaProject"
      "HEAD is now at a8f6f48 Update README file [(]tribitspub/tribits#278[)]"
      "[*][*][*] Git Repo: TribitsExampleProject"
      "HEAD is now at 8108b6a Automatic snapshot commit from TribitsExampleProject at f5ca5b7"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_11
    MESSAGE "Run ctest driver with an on branch 'for-testing'"
    CMND env
    ARGS
      CTEST_DASHBOARD_ROOT=PWD
      ${COMMON_ENV_ARGS}
      CTEST_START_WITH_EMPTY_BINARY_DIRECTORY=FALSE
      CTEST_WIPE_CACHE=FALSE
      TribitsExMetaProj_ENABLE_SECONDARY_TESTED_CODE=TRUE
      TribitsExMetaProj_BRANCH=for-testing
      CTEST_BUILD_NAME=CTestDriver_TribitsExMetaProj_clone_default_branch_remote
      ${CTEST_S_SCRIPT_ARGS}
    PASS_REGULAR_EXPRESSION_ALL
      "-- CTEST_NOTES_FILES=''"
      "-- ENV_TribitsExMetaProj_BRANCH='for-testing'"
      "-- TribitsExMetaProj_BRANCH='for-testing'"
      "Calling CTEST_UPDATE[(][)] to update base source repo '.*/TriBITS_CTestDriver_TribitsExMetaProj_clone_default_branch_remote/TribitsExampleMetaProject"
      "Old revision of repository is: a8f6f489088537176f0cab2fc189294038963ec4"
      "New revision of repository is: 56877b3b3dd06f41dfb27cedcedc2693aafaef03"
      "CTEST_UPDATE[(][.][.][.][)] returned '1'"
      "cmake -P tribits_ctest_update_commands[.]cmake"
      "HEAD is now at a8f6f48 Update README file [(]tribitspub/tribits#278[)]"
      "Git Update PASSED!"
      "For extra repos, doing switch to branch for-testing"
      "TribitsExampleProject: Doing GIT update from URL '.*github[.]com.tribits/TribitsExampleProject[.]git' to dir '.*/TribitsExampleProject' [.][.][.]"
      "TribitsExampleProjectAddons: Doing initial GIT clone/checkout from URL '.*github.com.tribits/TribitsExampleProjectAddons.git' to dir 'TribitsExampleProjectAddons' [.][.][.]"
      "CTEST_NOTES_FILES_WO_CACHE='.*/BUILD/Updates.txt[;].*/BUILD/UpdateCommandsOutput.txt'"
      "Configure PASSED!"
      "CTEST_NOTES_FILES='.*/BUILD/TribitsExMetaProjRepoVersion.txt[;].*/BUILD/Updates.txt[;].*/BUILD/UpdateCommandsOutput.txt[;].*/BUILD/CMakeCache.clean.txt'"
      "Build PASSED!"
      "100% tests passed, 0 tests failed out of 11"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_12
    MESSAGE "Make sure that the file TribitsExMetaProjRepoVersion.txt is correct"
    CMND diff ARGS 
      "${CMAKE_CURRENT_LIST_DIR}/data/TribitsExMetaProjRepoVersion.for-testing.txt"
      BUILD/TribitsExMetaProjRepoVersion.txt 
    ALWAYS_FAIL_ON_NONZERO_RETURN

  )
  # The above test checks several things:
  #
  # * Tests the initial clone of all the repos from scratch on the default
  #   branch and remote name work.
  #
  # * Tests that the Updates.txt file in *NOT* created or attached as a notes
  #   file on the initial clone.
  #
  # * Makes sure some git commit SHA1s are shown in 'Old/New revision of
  #   repository' printouts from ctest_update().
  #
  # * ???
  # 
  #
  # NOTE: The reason that so many tests are done in a single ctest test is the
  # cost of the initial configure which is very expensive.  The other runs use
  # CTEST_START_WITH_EMPTY_BINARY_DIRECTORY=FALSE and CTEST_WIPE_CACHE=FALSE
  # to avoid this cost.


TRIBITS_ADD_ADVANCED_TEST( CTestDriver_TribitsExMetaProj_clone_custom_branch_remote
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  TEST_0
    MESSAGE "Run ctest driver with intial clone of the repos on the default branch 'master' and remote 'origin'"
    CMND env
    ARGS
      CTEST_DASHBOARD_ROOT=PWD
      ${COMMON_ENV_ARGS}
      TribitsExMetaProj_GIT_REPOSITORY_REMOTE=github
      TribitsExMetaProj_BRANCH=for-testing
      TribitsExMetaProj_ENABLE_SECONDARY_TESTED_CODE=TRUE
      CTEST_BUILD_NAME=CTestDriver_TribitsExMetaProj_clone_custom_branch_remote
      ${CTEST_S_SCRIPT_ARGS}
    PASS_REGULAR_EXPRESSION_ALL
      "CTEST_NOTES_FILES=''"
      "First perform the initial checkout: .*/git. clone -b for-testing -o github .*github.com.tribits/TribitsExampleMetaProject.git"
      "Perform checkout in directory: .*/TriBITS_CTestDriver_TribitsExMetaProj_clone_custom_branch_remote"
      "Calling CTEST_UPDATE[(][)] to update base source repo '.*/TriBITS_CTestDriver_TribitsExMetaProj_clone_custom_branch_remote/TribitsExampleMetaProject"
      "Old revision of repository is: 56877b3b3dd06f41dfb27cedcedc2693aafaef03"
      "New revision of repository is: 56877b3b3dd06f41dfb27cedcedc2693aafaef03"
      "CTEST_UPDATE[(][.][.][.][)] returned '0'"
      "cmake -P tribits_ctest_update_commands[.]cmake"
      "Git Update PASSED!"
      "TribitsExampleProject: Doing initial GIT clone/checkout from URL '.*github[.]com.tribits/TribitsExampleProject.git' to dir 'TribitsExampleProject' [.][.][.]"
      "Cloning into 'TribitsExampleProject'[.][.][.]"
      "TribitsExampleProjectAddons: Doing initial GIT clone/checkout from URL '.*github[.]com.tribits/TribitsExampleProjectAddons.git' to dir 'TribitsExampleProjectAddons' [.][.][.]"
      "Cloning into 'TribitsExampleProjectAddons'[.][.][.]"
      "CTEST_NOTES_FILES_WO_CACHE='.*/TriBITS_CTestDriver_TribitsExMetaProj_clone_custom_branch_remote/BUILD/UpdateCommandsOutput.txt'"
      "Configure PASSED!"
       "CTEST_NOTES_FILES='.*/TriBITS_CTestDriver_TribitsExMetaProj_clone_custom_branch_remote/BUILD/TribitsExMetaProjRepoVersion.txt[;].*/TriBITS_CTestDriver_TribitsExMetaProj_clone_custom_branch_remote/BUILD/UpdateCommandsOutput.txt[;].*/TriBITS_CTestDriver_TribitsExMetaProj_clone_custom_branch_remote/BUILD/CMakeCache.clean.txt'"
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

  TEST_1
    MESSAGE "Check that base repo has correct remote"
    CMND git ARGS remote -v
    WORKING_DIRECTORY TribitsExampleMetaProject
    SKIP_CLEAN_WORKING_DIRECTORY
    PASS_REGULAR_EXPRESSION_ALL
      "github.*.*github[.]com.tribits/TribitsExampleMetaProject[.]git"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_2
    MESSAGE "Check that base repo is on the correct branch"
    CMND git ARGS branch
    WORKING_DIRECTORY TribitsExampleMetaProject
    SKIP_CLEAN_WORKING_DIRECTORY
    PASS_REGULAR_EXPRESSION_ALL
      "[*].*for-testing"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_3
    MESSAGE "Check that one of the extra repos has correct remote"
    CMND git ARGS remote -v
    WORKING_DIRECTORY TribitsExampleMetaProject/TribitsExampleProject
    SKIP_CLEAN_WORKING_DIRECTORY
    PASS_REGULAR_EXPRESSION_ALL
      "github.*.*github[.]com.tribits/TribitsExampleProject[.]git"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_4
    MESSAGE "Check that one of the extra repos in on the correct branch"
    CMND git ARGS branch
    WORKING_DIRECTORY TribitsExampleMetaProject/TribitsExampleProject
    SKIP_CLEAN_WORKING_DIRECTORY
    PASS_REGULAR_EXPRESSION_ALL
      "[*].*for-testing"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_5
    MESSAGE "Check out a retarded non-tracking branch"
    CMND "${${PROJECT_NAME}_TRIBITS_DIR}/python_utils/gitdist"
    ARGS --dist-no-color
      --dist-repos=.,TribitsExampleProject,TribitsExampleProjectAddons
      checkout -b non-tracking HEAD^
    WORKING_DIRECTORY TribitsExampleMetaProject
    SKIP_CLEAN_WORKING_DIRECTORY
    PASS_REGULAR_EXPRESSION_ALL
      "[*][*][*] Base Git Repo: TribitsExampleMetaProject"
      "Switched to a new branch 'non-tracking'"
      "[*][*][*] Git Repo: TribitsExampleProject"
      "[*][*][*] Git Repo: TribitsExampleProjectAddons"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_6
    MESSAGE "Check that base repo is on the correct branch"
    CMND git ARGS branch
    WORKING_DIRECTORY TribitsExampleMetaProject
    SKIP_CLEAN_WORKING_DIRECTORY
    PASS_REGULAR_EXPRESSION_ALL
      "[*].*non-tracking"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_7
    MESSAGE "Check that one of the extra repos in on the correct branch"
    CMND git ARGS branch
    WORKING_DIRECTORY TribitsExampleMetaProject/TribitsExampleProject
    SKIP_CLEAN_WORKING_DIRECTORY
    PASS_REGULAR_EXPRESSION_ALL
      "[*].*non-tracking"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_8
    MESSAGE "Remote the generated <project>RepoVersion.txt file"
    CMND rm ARGS BUILD/TribitsExMetaProjRepoVersion.txt
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_9
    MESSAGE "Run ctest driver to get back on the 'for-testing' branch"
    CMND env
    ARGS
      CTEST_DASHBOARD_ROOT=PWD
      ${COMMON_ENV_ARGS}
      CTEST_START_WITH_EMPTY_BINARY_DIRECTORY=FALSE
      CTEST_WIPE_CACHE=FALSE
      TribitsExMetaProj_ENABLE_SECONDARY_TESTED_CODE=TRUE
      TribitsExMetaProj_GIT_REPOSITORY_REMOTE=github
      TribitsExMetaProj_BRANCH=for-testing
      CTEST_BUILD_NAME=CTestDriver_TribitsExMetaProj_clone_default_branch_remote
      ${CTEST_S_SCRIPT_ARGS}
    PASS_REGULAR_EXPRESSION_ALL
      "-- ENV_TribitsExMetaProj_BRANCH='for-testing'"
      "-- TribitsExMetaProj_BRANCH='for-testing'"
      "Calling CTEST_UPDATE[(][)] to update base source repo '.*/TriBITS_CTestDriver_TribitsExMetaProj_clone_custom_branch_remote/TribitsExampleMetaProject"
      "Old revision of repository is: a8f6f489088537176f0cab2fc189294038963ec4"
      "New revision of repository is: 56877b3b3dd06f41dfb27cedcedc2693aafaef03"
      "CTEST_UPDATE[(][.][.][.][)] returned '1'"
      "cmake -P tribits_ctest_update_commands[.]cmake"
      "HEAD is now at a8f6f48 Update README file [(]tribitspub/tribits#278[)]"
      "Git Update PASSED!"
      "For extra repos, doing switch to branch for-testing"
      "TribitsExampleProject: Doing GIT update from URL '.*github[.]com.tribits/TribitsExampleProject[.]git' to dir '.*/TribitsExampleProject' [.][.][.]"
      "TribitsExampleProjectAddons: Doing GIT update from URL '.*github.com.tribits/TribitsExampleProjectAddons.git' to dir '.*/TribitsExampleProjectAddons' [.][.][.]"
      "CTEST_NOTES_FILES_WO_CACHE='.*/BUILD/Updates.txt[;].*/BUILD/UpdateCommandsOutput.txt'"
      "Configure PASSED!"
      "CTEST_NOTES_FILES='.*/BUILD/TribitsExMetaProjRepoVersion.txt[;].*/BUILD/Updates.txt[;].*/BUILD/UpdateCommandsOutput.txt[;].*/BUILD/CMakeCache.clean.txt'"
      "Build PASSED!"
      "100% tests passed, 0 tests failed out of 11"
    ALWAYS_FAIL_ON_NONZERO_RETURN
  # NOTE: The above use case requires the custom git commands used by
  # ctest_update().  The default git commits used inside of ctest_update()
  # fail in that use case (see #TRIL-260 for an example).

  TEST_10
    MESSAGE "Check that base repo is on the correct branch"
    CMND git ARGS branch
    WORKING_DIRECTORY TribitsExampleMetaProject
    SKIP_CLEAN_WORKING_DIRECTORY
    PASS_REGULAR_EXPRESSION_ALL
      "[*].*for-testing"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_11
    MESSAGE "Check that one of the extra repos in on the correct branch"
    CMND git ARGS branch
    WORKING_DIRECTORY TribitsExampleMetaProject/TribitsExampleProject
    SKIP_CLEAN_WORKING_DIRECTORY
    PASS_REGULAR_EXPRESSION_ALL
      "[*].*for-testing"
    ALWAYS_FAIL_ON_NONZERO_RETURN

  TEST_12
    MESSAGE "Make sure that the file TribitsExMetaProjRepoVersion.txt is correct"
    CMND diff ARGS 
      "${CMAKE_CURRENT_LIST_DIR}/data/TribitsExMetaProjRepoVersion.for-testing.txt"
      BUILD/TribitsExMetaProjRepoVersion.txt 
    ALWAYS_FAIL_ON_NONZERO_RETURN

  # ToDo: Do the update except change the git URLs for the base and extra
  # repos and make sure that it resets the git remote URL correctly.  (This
  # functionality is not implemented yet but it needs to be.)  But this will
  # fail the update because those remotes don't actually exist (but that is
  # okay for the purpose of this test).

  # ToDo: Check the remote name 'github' and git remote URLs and branch name
  # 'for-testing' in the cloned repos

  # ToDo: Check the TribitsExMetaProjRepoVersion.txt file

  )
  # The above test checks a few other use cases:
  #
  # * Initial clone on non-default branch and remote name
  #
  # * 
  #
  # ???
  #



# ToDo: Add a test that does a bad clone using a bad repo URL for the base repo



# ToDo: Add a test that does a bad clone using a bad bad extra repo branch
# (but an okay base repo branch)







# ToDo: Define the proper behavior for doing and update where the name
# ${TribitsExMetaProj_GIT_REPOSITORY_REMOTE} does not exist but the git repos
# already exist.  What should be the behavior?  NOTE: This should likely just
# error out as this should be an invalid use case.  If you want to use
# different remote, add it external to the ctest -S script invocation.
