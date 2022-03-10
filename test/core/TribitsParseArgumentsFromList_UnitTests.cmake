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
  )

include(TribitsParseArgumentsFromList)

include(MessageWrapper)
include(UnitTestHelpers)
include(GlobalSet)
include(GlobalNullSet)
include(AppendStringVar)


#####################################################################
#
# Unit tests for tribits_parse_arguments_from_list()
#
#####################################################################


function(tribits_parse_arguments_from_list_pass_through_all)

  message("tribits_parse_arguments_from_list(): All passthrough")

  set(theList "arg1[]" "arg2a\;arg2b" "--arg3 val3")

  tribits_parse_arguments_from_list(PREFIX "" "" theList)

  unittest_compare_const(PREFIX_UNPARSED_ARGUMENTS "arg1[];arg2a<semicolon>arg2b;--arg3 val3")

  unittest_compare_list_ele_const(PREFIX_UNPARSED_ARGUMENTS 0 "arg1[]" )
  unittest_compare_list_ele_const(PREFIX_UNPARSED_ARGUMENTS 1 "arg2a<semicolon>arg2b" )
  unittest_compare_list_ele_const(PREFIX_UNPARSED_ARGUMENTS 2 "--arg3 val3" )

endfunction()


function(tribits_parse_arguments_from_list_options_3_args_3_partial_unparsed_args)

  message("tribits_parse_arguments_from_list(): options 3, args 3, partial matching, with unparsed args")

  set(theList
     "unparsed1" "up2\;--up3 junk"
    ARG1 "arg1[]" ARG3 "arg2a\;arg2b" OPTION1 "--arg3 val3" OPTION3)
    # Note: above shows how options are pulled out of arguments!

  tribits_parse_arguments_from_list(PREFIX
    "OPTION1;OPTION2;OPTION3"
    "ARG1;ARG2;ARG3"
    theList)

  unittest_compare_const(PREFIX_OPTION1 "TRUE")
  unittest_compare_const(PREFIX_OPTION2 "FALSE")
  unittest_compare_const(PREFIX_OPTION3 "TRUE")

  unittest_compare_const(PREFIX_ARG1 "arg1[]")
  unittest_compare_list_ele_const(PREFIX_ARG1 0 "arg1[]" )

  unittest_compare_const(PREFIX_ARG2 "")

  unittest_compare_const(PREFIX_ARG3 "arg2a<semicolon>arg2b;--arg3 val3")
  unittest_compare_list_ele_const(PREFIX_ARG3 0 "arg2a<semicolon>arg2b")
  unittest_compare_list_ele_const(PREFIX_ARG3 1 "--arg3 val3")

  unittest_compare_const(PREFIX_UNPARSED_ARGUMENTS
     "unparsed1;up2<semicolon>--up3 junk")

  unittest_compare_list_ele_const(PREFIX_UNPARSED_ARGUMENTS 0 "unparsed1")
  unittest_compare_list_ele_const(PREFIX_UNPARSED_ARGUMENTS 1 "up2<semicolon>--up3 junk")

endfunction()


function(tribits_parse_arguments_from_list_options_3_args_3_partial_no_unparsed_args)

  message("tribits_parse_arguments_from_list(): options 3, args 3, partial matching, no unparsed args")

  set(theList
     OPTION2 ARG1 "arg1[]" ARG3 "arg2a\;arg2b" "--arg3 val3" OPTION3)

  tribits_parse_arguments_from_list(PREFIX
    "OPTION1;OPTION2;OPTION3"
    "ARG1;ARG2;ARG3"
    theList)

  unittest_compare_const(PREFIX_OPTION1 "FALSE")
  unittest_compare_const(PREFIX_OPTION2 "TRUE")
  unittest_compare_const(PREFIX_OPTION3 "TRUE")

  unittest_compare_const(PREFIX_ARG1 "arg1[]")
  unittest_compare_list_ele_const(PREFIX_ARG1 0 "arg1[]" )

  unittest_compare_const(PREFIX_ARG2 "")

  unittest_compare_const(PREFIX_ARG3 "arg2a<semicolon>arg2b;--arg3 val3")
  unittest_compare_list_ele_const(PREFIX_ARG3 0 "arg2a<semicolon>arg2b")
  unittest_compare_list_ele_const(PREFIX_ARG3 1 "--arg3 val3")

  unittest_compare_const(PREFIX_UNPARSED_ARGUMENTS "")

endfunction()


#
# Execute the unit tests
#

unittest_initialize_vars()

message("\n***")
message("*** Running the unit tests")
message("***\n")

tribits_parse_arguments_from_list_pass_through_all()
tribits_parse_arguments_from_list_options_3_args_3_partial_unparsed_args()
tribits_parse_arguments_from_list_options_3_args_3_partial_no_unparsed_args()

message("\n***")
message("*** Determine final result of all unit tests")
message("***\n")

# Pass in the number of expected tests that must pass!
unittest_final_result(26)
