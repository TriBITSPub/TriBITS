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


# Function that creates enable-only dependency data-structures
#
# For each enabled package `<Package>`, this function sets up the global list
# var::
#
#   <Package>_FULL_ENABLED_DEP_PACKAGES
#
# If ``${PROJECT_NAME}_GENERATE_EXPORT_FILES_FOR_ONLY_LISTED_PACKAGES`` is
# set, then ``<Package>_FULL_ENABLED_DEP_PACKAGES`` will only be sets for
# those packages.  Otherwise, ``<Package>_FULL_ENABLED_DEP_PACKAGES`` will be
# set for all packages listed in `${PROJECT_NAME}_ENABLED_INTERNAL_PACKAGES`_.
#
# NOTE: The modern TriBITS implementation does not need this full list of
# dependencies for each package.  Only the function
# `tribits_find_most_recent_file_timestamp()` needs this.  (Therefore, this
# could not be striped out of TriBITS because there are still some projects
# that use this function.)
#
function(tribits_set_up_enabled_only_dependencies)

  set(GENERATE_EXPORT_DEPENDENCIES ${${PROJECT_NAME}_GENERATE_EXPORT_FILE_DEPENDENCIES})
  if ("${${PROJECT_NAME}_GENERATE_EXPORT_FILES_FOR_ONLY_LISTED_PACKAGES}" STREQUAL ""
      AND NOT
      "${${PROJECT_NAME}_GENERATE_EXPORT_FILES_FOR_ONLY_LISTED_SE_PACKAGES}" STREQUAL ""
    )
    message(DEPRECATION
      "WARNING! The cache var"
      " ${PROJECT_NAME}_GENERATE_EXPORT_FILES_FOR_ONLY_LISTED_SE_PACKAGES"
      "='${${PROJECT_NAME}_GENERATE_EXPORT_FILES_FOR_ONLY_LISTED_SE_PACKAGES}'"
      " is deprecated!  Please instead set"
      " ${PROJECT_NAME}_GENERATE_EXPORT_FILES_FOR_ONLY_LISTED_PACKAGES"
      "='${${PROJECT_NAME}_GENERATE_EXPORT_FILES_FOR_ONLY_LISTED_SE_PACKAGES}'")
    set(${PROJECT_NAME}_GENERATE_EXPORT_FILES_FOR_ONLY_LISTED_PACKAGES
      ${${PROJECT_NAME}_GENERATE_EXPORT_FILES_FOR_ONLY_LISTED_SE_PACKAGES} )
  endif()

  # Determine lastExportTribitsPackage if not to generate any of these full
  # dependency lists
  set(lastExportTribitsPackage "")
  if (GENERATE_EXPORT_DEPENDENCIES
      AND ${PROJECT_NAME}_GENERATE_EXPORT_FILES_FOR_ONLY_LISTED_PACKAGES
    )
    # Find the last enabled package for which an export file is requested.
    set(LAST_PKG_IDX -1)
    set(LAST_PKG)
    foreach(tribitsPkg  IN LISTS
        ${PROJECT_NAME}_GENERATE_EXPORT_FILES_FOR_ONLY_LISTED_PACKAGES
      )
      #print_var(tribitsPkg)
      set(PKG_IDX ${${tribitsPkg}_PKG_IDX})
      #print_var(PKG_IDX)
      if (PKG_IDX)
        # The listed package is enabled so we will consider it
        if (PKG_IDX GREATER ${LAST_PKG_IDX})
          set(LAST_PKG_IDX ${PKG_IDX})
          set(LAST_PKG ${tribitsPkg})
         #print_var(LAST_PKG_IDX)
         #print_var(LAST_PKG)
        endif()
      endif()
    endforeach()
    if (LAST_PKG)
      # At least one listed package was enabled
      set(lastExportTribitsPackage ${LAST_PKG})
    else()
      # None of the listed packages were enabled so don't bother generating
      # any export dependencies
      set(GENERATE_EXPORT_DEPENDENCIES FALSE)
    endif()

  endif()


  if (GENERATE_EXPORT_DEPENDENCIES)

    if (lastExportTribitsPackage)
      message("\nSetting up export dependencies up through ${lastExportTribitsPackage} ...\n")
    else()
      message("\nSetting up export dependencies for all enabled packages ...\n")
    endif()

    foreach(tribitsPackage  IN LISTS  ${PROJECT_NAME}_ENABLED_INTERNAL_PACKAGES)
      tribits_package_set_full_enabled_dep_packages(${tribitsPackage})
      if (${PROJECT_NAME}_DUMP_PACKAGE_DEPENDENCIES)
        set(PRINTED_VAR FALSE)
        print_nonempty_var_with_spaces(${tribitsPackage}_FULL_ENABLED_DEP_PACKAGES
          PRINTED_VAR)
        if (NOT PRINTED_VAR)
          message("-- ${tribitsPackage}: No library dependencies!")
        endif()
      endif()
      if ("${lastExportTribitsPackage}" STREQUAL "${tribitsPackage}")
        break()
      endif()
    endforeach()

  endif()

endfunction()


# Function that sets up the full package dependencies for the given internal
# enabled package ``${PACKAGE_NAME}``, including all of its indirect upstream
# internal package dependencies.
#
function(tribits_package_set_full_enabled_dep_packages  PACKAGE_NAME)

  set(PACKAGE_FULL_DEPS_LIST "")

  foreach(DEP_PKG  IN LISTS  ${PACKAGE_NAME}_LIB_REQUIRED_DEP_PACKAGES)
    if (${PROJECT_NAME}_ENABLE_${DEP_PKG})
      list(APPEND  PACKAGE_FULL_DEPS_LIST  ${DEP_PKG})
    endif()
    # NOTE: This if() should not be needed but this is a safeguard
  endforeach()

  foreach(DEP_PKG  IN LISTS  ${PACKAGE_NAME}_LIB_OPTIONAL_DEP_PACKAGES)
    if (${PACKAGE_NAME}_ENABLE_${DEP_PKG})
      list(APPEND  PACKAGE_FULL_DEPS_LIST  ${DEP_PKG})
    endif()
  endforeach()

  if(PACKAGE_FULL_DEPS_LIST)
    list(REMOVE_DUPLICATES  PACKAGE_FULL_DEPS_LIST)

    foreach(DEP_PACKAGE  IN LISTS  PACKAGE_FULL_DEPS_LIST)
      list(APPEND PACKAGE_FULL_DEPS_LIST  ${${DEP_PACKAGE}_FULL_ENABLED_DEP_PACKAGES})
    endforeach()

    list(REMOVE_DUPLICATES PACKAGE_FULL_DEPS_LIST)
  endif()

  set(ORDERED_PACKAGE_FULL_DEPS_LIST "")

  foreach(DEP_PACKAGE  IN LISTS  PACKAGE_FULL_DEPS_LIST)

    #print_var(${DEP_PACKAGE}_PKG_IDX)
    set(DEP_PACKAGE_VALUE  ${${DEP_PACKAGE}_PKG_IDX})

    set(SORTED_INDEX 0)
    set(INSERTED_DEP_PACKAGE FALSE)

    foreach(SORTED_PACKAGE  IN LISTS  ORDERED_PACKAGE_FULL_DEPS_LIST)

      #print_var(${SORTED_PACKAGE}_PKG_IDX)
      set(SORTED_PACKAGE_VALUE  ${${SORTED_PACKAGE}_PKG_IDX})

      if (${DEP_PACKAGE_VALUE} GREATER ${SORTED_PACKAGE_VALUE})
        list(INSERT  ORDERED_PACKAGE_FULL_DEPS_LIST  ${SORTED_INDEX}  ${DEP_PACKAGE})
        set(INSERTED_DEP_PACKAGE TRUE)
        break()
      endif()

      math(EXPR SORTED_INDEX ${SORTED_INDEX}+1)

    endforeach()

    if(NOT INSERTED_DEP_PACKAGE)
      list(APPEND  ORDERED_PACKAGE_FULL_DEPS_LIST  ${DEP_PACKAGE})
    endif()

  endforeach()

  global_set(${PACKAGE_NAME}_FULL_ENABLED_DEP_PACKAGES
    ${ORDERED_PACKAGE_FULL_DEPS_LIST})

endfunction()
