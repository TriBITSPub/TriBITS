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

################################################################################
#
# Module containing functions for getting Git repo information
#
################################################################################


# Run the git log command to get the version info for a git repo
#
function(tribits_generate_single_repo_version_string  gitRepoDir
   repoVersionStringOut
  )

  tribits_assert_git_executable()

  # A) Get the basic version info.

  execute_process(
    COMMAND ${GIT_EXECUTABLE} log -1 --pretty=format:"%h [%ad] <%ae>"
    WORKING_DIRECTORY ${gitRepoDir}
    RESULT_VARIABLE gitCmndRtn
    OUTPUT_VARIABLE gitCmndOutput
    )
  # NOTE: Above we have to add quotes '"' or CMake will not accept the
  # command.  However, git will put those quotes in the output so we have to
  # strip them out later :-(

  if (NOT gitCmndRtn STREQUAL 0)
    message(FATAL_ERROR "ERROR, ${GIT_EXECUTABLE} command returned ${gitCmndRtn}!=0"
      " for repo ${gitRepoDir}!")
    set(gitVersionLine "Error, could not get version info!")
  else()
    # Strip the quotes off :-(
    string(LENGTH "${gitCmndOutput}" gitCmndOutputLen)
    math(EXPR outputNumCharsToKeep "${gitCmndOutputLen}-2")
    string(SUBSTRING "${gitCmndOutput}" 1 ${outputNumCharsToKeep}
      gitVersionLine)
  endif()

  # B) Get the first 80 chars of the summary message for more info

  execute_process(
    COMMAND ${GIT_EXECUTABLE} log -1 --pretty=format:"%s"
    WORKING_DIRECTORY ${gitRepoDir}
    RESULT_VARIABLE gitCmndRtn
    OUTPUT_VARIABLE gitCmndOutput
    )

  if (NOT gitCmndRtn STREQUAL 0)
    message(FATAL_ERROR "ERROR, ${GIT_EXECUTABLE} command returned ${gitCmndRtn}!=0"
      " for extra repo ${gitRepoDir}!")
    set(gitSummaryStr "Error, could not get version summary!")
  else()
    # Strip off quotes and quote the 80 char string
    set(maxSummaryLen 80)
    math(EXPR maxSummaryLen_PLUS_2 "${maxSummaryLen}+2")
    string(LENGTH "${gitCmndOutput}" gitCmndOutputLen)
    math(EXPR outputNumCharsToKeep "${gitCmndOutputLen}-2")
    string(SUBSTRING "${gitCmndOutput}" 1 ${outputNumCharsToKeep}
      gitCmndOutputStripped)
    if (gitCmndOutputLen GREATER ${maxSummaryLen_PLUS_2})
      string(SUBSTRING "${gitCmndOutputStripped}" 0 ${maxSummaryLen}
         gitSummaryStr)
    else()
      set(gitSummaryStr "${gitCmndOutputStripped}")
    endif()
  endif()

  set(${repoVersionStringOut}
    "${gitVersionLine}\n${gitSummaryStr}" PARENT_SCOPE)

endfunction()


function(tribits_assert_git_executable)
  if (NOT GIT_EXECUTABLE)
    message(SEND_ERROR "ERROR, the program '${GIT_NAME}' could not be found!"
      "  We can not generate the repo version file!")
  endif()
endfunction()
