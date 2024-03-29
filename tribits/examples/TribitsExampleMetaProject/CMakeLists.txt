################################################################################
#                                                                              #
#                        TribitsExampleProjectMeta                             #
#                                                                              #
################################################################################

# To be safe, define your minimum CMake version.  This may be newer than the
# min required by TriBITS.
cmake_minimum_required(VERSION 3.23.0 FATAL_ERROR)

# Make CMake set WIN32 with CYGWIN for older CMake versions.  CMake requires
# this to be in the top-level CMakeLists.txt file and not an include file :-(
set(CMAKE_LEGACY_CYGWIN_WIN32 1 CACHE BOOL "" FORCE)

#
# A) Define your project name and set up major project options
#
# NOTE: Don't set options that would impact what packages get defined or
# enabled/disabled in this file as that would not impact other tools that
# don't process this file.
#

# Get PROJECT_NAME (must be in a file for other parts of system to read)
include("${CMAKE_CURRENT_SOURCE_DIR}/ProjectName.cmake")

# CMake requires that you declare the CMake project in the top-level file and
# not in an include file :-(
project(${PROJECT_NAME} NONE)

#
# B) Pull in the TriBITS system and execute
#

set(${PROJECT_NAME}_TRIBITS_DIR
   "${CMAKE_CURRENT_LIST_DIR}/../.."  CACHE  STRING
  "TriBITS base directory (default assumes in TriBITS source tree)")
include("${${PROJECT_NAME}_TRIBITS_DIR}/TriBITS.cmake")

# Set default location for header-only TPL to make easy to configure out of
# the TriBITS source tree.
set(HeaderOnlyTpl_INCLUDE_DIRS
  "${${PROJECT_NAME}_TRIBITS_DIR}/examples/tpls/HeaderOnlyTpl" 
  CACHE PATH "Default set by TriBITS/CMakeLists.txt" )

# Do all of the processing for this Tribits project
tribits_project()
