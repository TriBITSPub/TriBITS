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


# Standard TriBITS system includes
INCLUDE(TribitsProcessExtraRepositoriesList)
INCLUDE(TribitsProcessPackagesAndDirsLists)
INCLUDE(TribitsProcessTplsLists)
INCLUDE(TribitsAdjustPackageEnables)

# Standard TriBITS utilities includes
INCLUDE(TimingUtils)


#
# @MACRO: TRIBITS_READ_PACKAGES_PROCESS_DEPENDENCIES_WRITE_XML()
#
# Usage::
#
#   TRIBITS_READ_PACKAGES_PROCESS_DEPENDENCIES_WRITE_XML()
#
# Macro run at the top project-level scope that reads in packages and TPLs,
# process dependencies, and (optimally) writes XML files of dependency
# information.
# 
#
MACRO(TRIBITS_READ_PACKAGES_PROCESS_DEPENDENCIES_WRITE_XML)

  #
  # A) Read in list of packages and package dependencies
  #

  IF (${PROJECT_NAME}_ENABLE_CONFIGURE_TIMING)
    TIMER_GET_RAW_SECONDS(SET_UP_DEPENDENCIES_TIME_START_SECONDS)
  ENDIF()

  TRIBITS_READ_DEFINED_EXTERNAL_AND_INTENRAL_TOPLEVEL_PACKAGES_LISTS()

  TRIBITS_READ_ALL_PACKAGE_DEPENDENCIES()

  IF (${PROJECT_NAME}_ENABLE_CONFIGURE_TIMING)
    TIMER_GET_RAW_SECONDS(SET_UP_DEPENDENCIES_TIME_STOP_SECONDS)
    TIMER_PRINT_REL_TIME(${SET_UP_DEPENDENCIES_TIME_START_SECONDS}
      ${SET_UP_DEPENDENCIES_TIME_STOP_SECONDS}
      "\nTotal time to read in and process all package dependencies")
  ENDIF()

  #
  # B) Dump dependnecy info as XML files if asked
  #

  TRIBITS_WRITE_XML_DEPENDENCY_FILES_IF_SUPPORTED()

ENDMACRO()


#
# @MACRO: TRIBITS_READ_DEFINED_EXTERNAL_AND_INTENRAL_TOPLEVEL_PACKAGES_LISTS()
#
# Usage::
#
#   TRIBITS_READ_DEFINED_EXTERNAL_AND_INTENRAL_TOPLEVEL_PACKAGES_LISTS()
#
# Macro run at the top project-level cope that reads in the contents of all of
# the `<repoDir>/TPLsList.cmake`_ and `<repoDir>/PackagesList.cmake`_ files to
# get the list of defined external packages (TPLs) and internal top-level
# packages.
#
# On output, this produces::
#
#   ${PROJECT_NAME}_PACKAGES
#   ${PROJECT_NAME}_TPLS
#
# and related varaibles.  Calls and sets variables from:
#
#  * `TRIBITS_PROCESS_TPLS_LISTS()`_
#  * `TRIBITS_PROCESS_PACKAGES_AND_DIRS_LISTS()`_
#
MACRO(TRIBITS_READ_DEFINED_EXTERNAL_AND_INTENRAL_TOPLEVEL_PACKAGES_LISTS)

  TRIBITS_SET_ALL_EXTRA_REPOSITORIES()

  # Set to empty
  SET(${PROJECT_NAME}_PACKAGES)
  SET(${PROJECT_NAME}_TPLS)

  #
  # A) Read list of packages and TPLs from 'PRE' extra repos
  #

  SET(READ_PRE_OR_POST_EXRAREPOS  PRE)
  TRIBITS_READ_EXTRA_REPOSITORIES_LISTS()

  #
  # B) Read list of packages and TPLs from native repos
  #

  FOREACH(NATIVE_REPO ${${PROJECT_NAME}_NATIVE_REPOSITORIES})

    TRIBITS_GET_REPO_NAME_DIR(${NATIVE_REPO}  NATIVE_REPO_NAME  NATIVE_REPO_DIR)
    #PRINT_VAR(NATIVE_REPO_NAME)
    #PRINT_VAR(NATIVE_REPO_DIR)

    # Need to make sure this gets set because logic in Dependencies.cmake files
    # looks for the presents of this variable.
    TRIBITS_SET_BASE_REPO_DIR(${PROJECT_SOURCE_DIR} ${NATIVE_REPO_DIR}
      ${NATIVE_REPO_NAME}_SOURCE_DIR)
    #PRINT_VAR(${NATIVE_REPO_NAME}_SOURCE_DIR)

    #
    # B.1) Define the lists of all ${NATIVE_REPO_NAME} native packages and TPLs
    #

    IF (${NATIVE_REPO_NAME}_PACKAGES_FILE_OVERRIDE)
      IF (IS_ABSOLUTE "${${NATIVE_REPO_NAME}_PACKAGES_FILE_OVERRIDE}")
        MESSAGE(FATAL_ERROR
          "ToDo: Implement abs path for ${NATIVE_REPO_NAME}_PACKAGES_FILE_OVERRIDE")
      ELSE()
        SET(${NATIVE_REPO_NAME}_PACKAGES_FILE
          "${${NATIVE_REPO_NAME}_SOURCE_DIR}/${${NATIVE_REPO_NAME}_PACKAGES_FILE_OVERRIDE}")
      ENDIF()
    ELSE()
      SET(${NATIVE_REPO_NAME}_PACKAGES_FILE
        "${${NATIVE_REPO_NAME}_SOURCE_DIR}/${${PROJECT_NAME}_PACKAGES_FILE_NAME}")
    ENDIF()

    IF (NATIVE_REPO STREQUAL ".")
      SET(REPOSITORY_NAME ${PROJECT_NAME})
    ELSE()
      SET(REPOSITORY_NAME ${NATIVE_REPO_NAME})
    ENDIF()

    # B.1.a) Read in the list of TPLs for this repo

    SET(${NATIVE_REPO_NAME}_TPLS_FILE
      "${${NATIVE_REPO_NAME}_SOURCE_DIR}/${${PROJECT_NAME}_TPLS_FILE_NAME}")

    MESSAGE("")
    MESSAGE("Reading list of native TPLs from ${${NATIVE_REPO_NAME}_TPLS_FILE}")
    MESSAGE("")

    TRIBITS_TRACE_FILE_PROCESSING(REPOSITORY  INCLUDE
      "${${NATIVE_REPO_NAME}_TPLS_FILE}")
    INCLUDE(${${NATIVE_REPO_NAME}_TPLS_FILE})
    TRIBITS_PROCESS_TPLS_LISTS(${NATIVE_REPO_NAME}  ${NATIVE_REPO_DIR})

    # B.1.b) Read in list of packages for this repo

    MESSAGE("")
    MESSAGE("Reading list of native packages from ${${NATIVE_REPO_NAME}_PACKAGES_FILE}")
    MESSAGE("")

    TRIBITS_TRACE_FILE_PROCESSING(REPOSITORY  INCLUDE
      "${${NATIVE_REPO_NAME}_PACKAGES_FILE}")
    INCLUDE(${${NATIVE_REPO_NAME}_PACKAGES_FILE})

    TRIBITS_PROCESS_PACKAGES_AND_DIRS_LISTS(${NATIVE_REPO_NAME} ${NATIVE_REPO_DIR})

  ENDFOREACH()

  #
  # C) Read list of packages and TPLs from 'POST' extra repos
  #

  SET(READ_PRE_OR_POST_EXRAREPOS  POST)
  TRIBITS_READ_EXTRA_REPOSITORIES_LISTS()

ENDMACRO()


#
# Function that will write XML dependnecy files if support for that exists in
# this installation of TriBITS.
#
FUNCTION(TRIBITS_WRITE_XML_DEPENDENCY_FILES_IF_SUPPORTED)
  SET(TRIBITS_PROJECT_CI_SUPPORT_DIR
     "${${PROJECT_NAME}_TRIBITS_DIR}/${TRIBITS_CI_SUPPORT_DIR}")
  SET(TRIBITS_DUMP_XML_DEPS_MODULE
   "${TRIBITS_PROJECT_CI_SUPPORT_DIR}/TribitsDumpXmlDependenciesFiles.cmake")
  IF (EXISTS "${TRIBITS_DUMP_XML_DEPS_MODULE}")
    INCLUDE(${TRIBITS_DUMP_XML_DEPS_MODULE})
    TRIBITS_WRITE_XML_DEPENDENCY_FILES()
  ENDIF()
ENDFUNCTION()