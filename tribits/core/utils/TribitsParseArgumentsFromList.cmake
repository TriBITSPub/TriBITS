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


include(TribitsPrintList)
include(TribitsCopyListVars)


# @MACRO: tribits_parse_arguments_from_list()
#
# Parse the entires of an input list into different sublists based on a list of options argument names
#
# Usage::
#
#   tribits_parse_arguments_from_list(
#     <prefix>   <optionNamesList>  <argNamesList>
#     <inputListName>
#     )
#
# Arguments to this macro are:
#
#   ``<prefix>``
#
#     Prefix ``<prefix>_`` added the list and option variables created listed
#     in ``<argNamesList>`` and ``<optionNamesList>``.
#
#   ``<optionNamesList>``
#
#     Quoted array of list options (e.g. ``"<optName0>;<optName1>;..."``) For
#     each variable name ``<optNamei>``, a local variable will be created in
#     the current scope with the name ``<prefix>_<optNamei>`` that is either
#     set to ``TRUE`` or ``FALSE`` depending if ``<optNamei>`` appears in
#     ``<inputArgsList>`` or not.
#
#   ``<argNamesList>``
#
#     Quoted array of list arguments (e.g. ``"<argName0>;<argName1>;..."``).
#     For each variable name ``<argNamei>``, a local variable will be created
#     in the current scope with the name ``<prefix>_<argNamei>`` which gives
#     the list of variables parsed out of ``<inputArgsList>``.
#
#   ``<inputListName>``
#
#     Name of list var containing keyword-based arguments.
#
# This function performs about the same task as the built-in function
# cmake_parse_arguments() except it operates on an arbitarary list given as a
# list var and it maintains the arguments even if they contain semi-colons ';'
# but it has to replace the semi-colons ';' with '<semicolon>'.  However, it
# will not maintain quotes '"'.
#
# For example, consider the following user-defined macro that uses both
# positional and keyword-based arguments using
# ``tribits_parse_arguments_from_list()``::
#
#   macro(parse_special_vars  BASE_NAME  SOME_LIST_VAR)
#
#     tribits_parse_arguments_from_list(
#       #prefix
#       ${BASE_NAME}
#       #lists
#       "ARG0;ARG1;ARG2"
#       #options
#       "OPT0;OPT1"
#       # The list var name
#       "${SOME_LIST_VAR}"
#       )
#
#   endmacro()
#
# Calling this macro as::
#
#   parse_special_vars(MyVar ARG0 a "b=v1;v2" ARG2 c OPT1)
#
# sets the following variables in the current scope::
#
#   MyVar_ARG0: "a" "b=v1<semicolon>v2" 
#   MyVar_ARG1: ""
#   MyVar_ARG2: "c"
#   MyVar_OPT0: "FALSE"
#   MyVar_OPT1: "TRUE"
#
# Any initial arguments that are not recognized as ``<argNamesList>`` or
# ``<optionNamesList>`` keyword arguments will be put into the variable
# ``<prefix>_UNPARSED_ARGUMENTS``.  If no arguments in ``<inputListName>`` match any
# in ``<argNamesList>``, then all non-option arguments are put into
# ``<prefix>_UNPARSED_ARGUMENTS``.  For example, if one passes in::
#
#   parse_special_vars(MyVar ARG5 a b c)
#
# you will get::
#
#   MyVar_UNPARSED_ARGUMENTS: "ARG5" "a" "b" "c"
#   MyVar_ARG0: ""
#   MyVar_ARG1: ""
#   MyVar_ARG2: ""
#   MyVar_OPT0: "FALSE"
#   MyVar_OPT1: "FALSE"
#
# Multiple occurrences of keyword arguments in ``<inputListName>`` is allowed
# but only the last one listed will be recorded.  For example, if one calls::
#
#   parse_special_vars(MyVar ARG1 a b ARG1 c)
#
# then this will set::
#
#   MyVar_ARG0: ""
#   MyVar_ARG1: "c"
#   MyVar_ARG2: ""
#   MyVar_OPT0: "FALSE"
#   MyVar_OPT1: "FALSE"
#
# This is actually consistent with the way that most argument list parsers
# behave with respect to multiple instances of the same argument so hopefully
# this will not be a surprise to anyone.
#
# If one puts an option keyword in the middle of a keyword argument list, the
# option keyword will get pulled out of the list.  For example, if one calls::
#
#   parse_special_vars(MyVar ARG0 a OPT0 c)
#
# then this will set::
#
#   MyVar_ARG0: "a: "c"
#   MyVar_ARG1: ""
#   MyVar_ARG2: ""
#   MyVar_OPT0: "TRUE"
#   MyVar_OPT1: "FALSE"
#
# This is confusing behavior so users would be smart not to mix option
# arguments inside of list arguments.
#
# If ``TRIBITS_PARSE_ARGUMENTS_FROM_LIST_DUMP_OUTPUT_ENABLED`` is set to
# ``TRUE``, then a bunch of detailed debug info will be printed.  This should
# only be used in the most desperate of debug situations because it will print
# a *lot* of output!
#
# **PERFORMANCE:** This function will scale as::
#
#   o( (len(<argNamesList>) * len(<optionNamesList>)) * len(<inputListName>) )
#
# Therefore, this could scale very badly for large sets of argument and option
# names and input argument list names.
#
macro(tribits_parse_arguments_from_list  prefix  option_names  arg_names
    inputListName
  )
 
  tribits_parse_arguments_from_list_dump_output(
    "tribits_parse_arguments_from_list: prefix='${prefix}'")
  tribits_parse_arguments_from_list_dump_output(
    "tribits_parse_arguments_from_list: option_names='${option_names}'")
  tribits_parse_arguments_from_list_dump_output(
    "tribits_parse_arguments_from_list: arg_names='${arg_names}'")
  tribits_parse_arguments_from_list_dump_output(
    "tribits_parse_arguments_from_list: inputListName='${inputListName}'")

  foreach(option ${option_names})
    set(${prefix}_${option} FALSE)
  endforeach()

  foreach(arg_name ${arg_names})
    set(${prefix}_${arg_name} "")
  endforeach()

  set(${prefix}_UNPARSED_ARGUMENTS "")

  set(DEFAULT_ARGS "")
  set(current_arg_name UNPARSED_ARGUMENTS)
  set(current_arg_list "")

  foreach(arg IN LISTS ${inputListName})
    string(REPLACE ";" "<semicolon>" arg "${arg}")
    tribits_parse_arguments_from_list_print_list(arg)
    set(larg_names ${arg_names}) # ToDo: Replace 'larg_names' with 'arg_names'
    list(FIND larg_names "${arg}" is_arg_name)
    if (is_arg_name GREATER -1)
      tribits_copy_list_vars(current_arg_list ${prefix}_${current_arg_name})
      tribits_parse_arguments_from_list_print_list(${prefix}_${current_arg_name})
      set(current_arg_name "${arg}")
      set(current_arg_list "")
    else()
      set(loption_names "${option_names}")  # ToDo: Replace 'option_names' with 'option_names'
      list(FIND loption_names "${arg}" is_option)
      if (is_option GREATER -1)
        set(${prefix}_${arg} TRUE)
        tribits_parse_arguments_from_list_print_list(${prefix}_${arg})
      else()
        list(APPEND current_arg_list "${arg}")
        tribits_parse_arguments_from_list_print_list(current_arg_list)
      endif()
    endif()
  endforeach()

  tribits_copy_list_vars(current_arg_list ${prefix}_${current_arg_name})

endmacro()
# NOTE: If the above macro turns out to be a performance bottle neck, there
# are a few things that could be done to improve performance.  One thing you
# could do is repalce the o(len(arg_names)) and o(len(option_names)) lookups
# with o(1) lookups by creating CMake variables of the name
# ${OUTER_FUNC_NAME}_arg_<argNamei> and then just look of that variable exists
# or not.  That should use a hash function.  That might actually slow things
# down for short lists however so we would have to measure, measure,
# measure. I would have to pass in the function/macro name to disabiguate
# the variable names.  It would really be better if cmake would provide a
# sorted list find operation.  That would make this much faster for large
# numbers of argument and option names.


function(tribits_parse_arguments_from_list_print_list  listName)
  if (TRIBITS_PARSE_ARGUMENTS_FROM_LIST_DUMP_OUTPUT_ENABLED)
    tribits_print_list(${listName})
  endif()
endfunction()

function(tribits_parse_arguments_from_list_dump_output  OUTPUT_STR)
  if (TRIBITS_PARSE_ARGUMENTS_FROM_LIST_DUMP_OUTPUT_ENABLED)
    message("${OUTPUT_STR}")
  endif()
endfunction()
