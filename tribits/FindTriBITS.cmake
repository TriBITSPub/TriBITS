# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

#.rst:
# FindTriBITS
# ------------
#
# Find the Tribal Build, Integration, and Test System (TriBITS) and set up
# TriBITS project to use it.
#
# Variables
# ^^^^^^^^^
#
# This module will set the following variables:
#
# ``TRIBITS_DIR``
#   The location of the found TriBITS base directory (i.e. location of TriBITS.cmake)
#
# ``${PROJECT_NAME}_TRIBITS_DIR``
#   The location of the found TriBITS base directory (i.e. locatioin of TriBITS.cmake)
#
# Usage
# ^^^^^
#
# To use this to find TriBITS by any CMake project call ``find_package(TriBITS)``.
#
# ToDo: Finish docuemnation!
#

IF ("${PROJECT_NAME}" STREQUAL "")
  MESSAGE(FATAL_ERROR "ERROR: Must set 'PROJECT_NAME'!" )
ENDIF()

IF ("${${PROJECT_NAME}_SOURCE_DIR}" STREQUAL "")
  MESSAGE(FATAL_ERROR "ERROR: ${PROJECT_NAME}_SOURCE_DIR not set!"
    "Must call PROJECT(${PROJECT_NAME} NONE) before!" )
ENDIF()

FIND_PACKAGE(TriBITS CONFIG
  PATHS "${PROJECT_NAME}_SOURCE_DIR}/cmake/tribits"
  )
