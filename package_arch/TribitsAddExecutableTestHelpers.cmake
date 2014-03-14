# @HEADER
# ************************************************************************
#
#            TriBITS: Tribial Build, Integrate, and Test System
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

INCLUDE(AdvancedSet)

ADVANCED_SET( ${PROJECT_NAME}_CMAKE_EXECUTABLE_SUFFIX ".exe"
  CACHE STRING
  "Default exec suffix on all platforms (can be overridden by each executable added)." )

#
# Process the COMM arguments
#
# NOTE: The COMM array arguments is passed as ${ARGN}
#

FUNCTION( TRIBITS_PROCESS_COMM_ARGS  ADD_SERIAL_FEATURE  ADD_MPI_FEATURE )

  SET(COMM_ARRAY ${ARGN})

  IF (COMM_ARRAY)
    SET(${ADD_SERIAL_FEATURE} OFF PARENT_SCOPE)
    SET(${ADD_MPI_FEATURE} OFF PARENT_SCOPE)
    FOREACH(COMM ${COMM_ARRAY})
      IF(${COMM} STREQUAL "serial")
        SET(${ADD_SERIAL_FEATURE} ON PARENT_SCOPE)
      ELSEIF (${COMM} STREQUAL "mpi")
        SET(${ADD_MPI_FEATURE} ON PARENT_SCOPE)
      ELSE()
        MESSAGE(SEND_ERROR "Error, the COMM value '${COMM}' is not valid."
          "  Only 'mpi' and 'serial' are allowed.")
      ENDIF()
    ENDFOREACH()
  ELSE()
    SET(${ADD_MPI_FEATURE} ON PARENT_SCOPE)
    SET(${ADD_SERIAL_FEATURE} ON PARENT_SCOPE)
  ENDIF()

  IF (TPL_ENABLE_MPI)
    SET(${ADD_SERIAL_FEATURE} OFF PARENT_SCOPE)
  ELSE()
    SET(${ADD_MPI_FEATURE} OFF PARENT_SCOPE)
  ENDIF()

ENDFUNCTION()


FUNCTION( TRIBITS_CREATE_NAME_FROM_CURRENT_SOURCE_DIRECTORY DIRECTORY_NAME )
    SET(DIRECTORY_NAME "")
    #Get the unique part of the path for this test directory
    STRING(REGEX REPLACE ${PACKAGE_SOURCE_DIR} "" unique_dir_path
      ${CMAKE_CURRENT_SOURCE_DIR})
    
    #strip off the preceeding "/"
    STRING(LENGTH ${unique_dir_path} udp_length)
    MATH(EXPR last_index "${udp_length}-1")
    STRING(SUBSTRING ${unique_dir_path} 1 ${last_index} unique_dir_path)

    # Make the name acceptable for filesystems. This may need to be made
    # compatible with windows since they use a "\" instead of a "/" for
    # directory delimiters. I'm not sure how this will react if we encounter a
    # directory name with a space in it.
    STRING(REGEX REPLACE "/" "_" DIRECTORY_NAME ${unique_dir_path})

    #PRINT_VAR(DIRECTORY_NAME)
    SET(DIRECTORY_NAME ${DIRECTORY_NAME} PARENT_SCOPE)
ENDFUNCTION()
