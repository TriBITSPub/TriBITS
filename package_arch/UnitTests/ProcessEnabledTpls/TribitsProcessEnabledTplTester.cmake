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

#
# This file is run as a cmake -P script to test out the
# TribitsProcessEnabledTpl.cmake and
# TribitsTplFindIncludeDirsAndLibraries.cmake modules.
#

# Passed in on command-line
MESSAGE("${PROJECT_NAME} = ${PROJECT_NAME}")
MESSAGE("${PROJECT_NAME}_TRIBITS_DIR = ${${PROJECT_NAME}_TRIBITS_DIR}")

SET( CMAKE_MODULE_PATH
  "${${PROJECT_NAME}_TRIBITS_DIR}/utils"
  "${${PROJECT_NAME}_TRIBITS_DIR}/package_arch"
  )

INCLUDE(TribitsProcessEnabledTpl)

# Passed in on command-line
PRINT_VAR("TPL_NAME")
PRINT_VAR("TPL_${TPL_NAME}_ENABLING_PKG")
PRINT_VAR("${TPL_NAME}_FINDMOD")

# Set up other vars
SET(TPL_ENABLE_${TPL_NAME} ON  CACHE STRING  "The default for testing")
SET(CMAKE_FIND_LIBRARY_PREFIXES "lib")
IF (TPL_FIND_SHARED_LIBS)
  SET(CMAKE_FIND_LIBRARY_SUFFIXES .so )
ENDIF()

# Do the processing of the TPL
MESSAGE("")
TRIBITS_PROCESS_ENABLED_TPL(${TPL_NAME})
MESSAGE("")
MESSAGE("Exported TPL_ENABLE_${TPL_NAME}='${TPL_ENABLE_${TPL_NAME}}'")
MESSAGE("Exported TPL_${TPL_NAME}_NOT_FOUND='${TPL_${TPL_NAME}_NOT_FOUND}'")
MESSAGE("Exported TPL_${TPL_NAME}_LIBRARIES='${TPL_${TPL_NAME}_LIBRARIES}'")
MESSAGE("Exported TPL_${TPL_NAME}_INCLUDE_DIRS='${TPL_${TPL_NAME}_INCLUDE_DIRS}'")
