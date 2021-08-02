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

message("PROJECT_NAME = ${PROJECT_NAME}")
message("${PROJECT_NAME}_TRIBITS_DIR = ${${PROJECT_NAME}_TRIBITS_DIR}")

set( CMAKE_MODULE_PATH
  "${${PROJECT_NAME}_TRIBITS_DIR}/core/utils"
  "${${PROJECT_NAME}_TRIBITS_DIR}/core/package_arch"
  "${${PROJECT_NAME}_TRIBITS_DIR}/ctest_driver"
  )

include(GlobalSet)
include(TribitsReadTagFile)
include(UnitTestHelpers)


function(unittest_read_ctest_tag_file)

  message("\n***")
  message("*** Testing tribits_read_ctest_tag_file()")
  message("***\n")

  set(TAG_FILE_IN "${CMAKE_CURRENT_LIST_DIR}/data/dummy_build_dir/Testing/TAG")

  tribits_read_ctest_tag_file(${TAG_FILE_IN} BUILD_START_TIME_OUT CDASH_TRACK_OUT)

  unittest_compare_const(BUILD_START_TIME_OUT
    "20101015-1112")

  unittest_compare_const(CDASH_TRACK_OUT
    "My CDash Track")  # NOTE: Spaces are important to test here!

endfunction()

#
# Execute the unit tests
#

# Assume that all unit tests will pass by default
global_set(UNITTEST_OVERALL_PASS TRUE)
global_set(UNITTEST_OVERALL_NUMPASSED 0)
global_set(UNITTEST_OVERALL_NUMRUN 0)

# Run the unit test functions
unittest_read_ctest_tag_file()

message("\n***")
message("*** Determine final result of all unit tests")
message("***\n")

# Pass in the number of expected tests that must pass!
unittest_final_result(2)
