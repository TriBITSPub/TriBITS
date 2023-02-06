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
# Module TribitsExternalPackageFindTplHelpers.cmake
#
# Contains functions for implementing FindTPL<tplName>.cmake files for
# external packages using find_package(<externalPkg>) that producing modern
# IMPORTED targets.
#
# NOTE: The acronym 'extpkgwit' stands for "External Package With Imported
# Targets".
# 
################################################################################


include(TribitsExternalPackageWriteConfigFile)



# @FUNCTION: tribits_extpkg_create_imported_all_libs_target_and_config_file()
#
# Called from a `FindTPL<tplName>.cmake`_ module which first calls
# ``find_package(<externalPkg>)``and the calls this function to get and
# external package that uses modern CMake IMPORTED targets. This function
# creates the ``<tplName>::all_libs`` target and creates a TriBITS-compliant
# external package wrapper file `<tplName>Config.cmake`.
#
# Usage::
#
#   tribits_extpkg_create_imported_all_libs_target_and_config_file(
#     <tplName>
#     INNER_FIND_PACKAGE_NAME <externalPkg>
#     IMPORTED_TARGETS_FOR_ALL_LIBS <importedTarget0> <importedTarget1> ... )
#
# This function is called from a TriBITS ``FindTPL<tplName>.cmake`` wrapper
# module after it calls ``find_package(<externalPkg>)`` and then this function
# creates the IMPORTED target ``<tplName>::all_libs`` from the list of
# IMPORTED targets ``<importedTarget0> <importedTarget1> ...`` which are
# defined from the call ``find_package(<externalPkg>)``.  This function also
# takes care of generating the correct ``<tplName>Config.cmake`` file under
# the directory::
#
#   ${${PROJECT_NAME}_BINARY_DIR}/${${PROJECT_NAME}_BUILD_DIR_EXTERNAL_PKGS_DIR}
#
# The generated ``<tplName>Config.cmake`` file pulls in the upstream
# TriBITS-compliant ``<UpstreamPkg>Config.cmake` files, calls
# ``find_dependency(<externalPkg>)`` (with no other arguments), defines the
# `<tplName>::all_libs`` target, and then sets up the correct dependencies
# between these targets.
#
# For more details, see `Creating FindTPL<tplName>.cmake using find_package()
# with IMPORTED targets`_.
#
function(tribits_extpkg_create_imported_all_libs_target_and_config_file
    tplName
  )

  # Parse arguments
  cmake_parse_arguments(
     PARSE_ARGV 1
     PARSE "" "" # prefix, options, one_value_keywords
     "INNER_FIND_PACKAGE_NAME;IMPORTED_TARGETS_FOR_ALL_LIBS"  #multi_value_keywords
     )
  tribits_check_for_unparsed_arguments(PARSE)
  tribits_assert_parse_arg_one_value(PARSE  INNER_FIND_PACKAGE_NAME)
  tribits_assert_parse_arg_one_or_more_values(PARSE IMPORTED_TARGETS_FOR_ALL_LIBS)

  # Create imported target <tplName>::all_libs
  add_library(${tplName}::all_libs  INTERFACE  IMPORTED  GLOBAL)
  foreach (importedTarget  IN LISTS  PARSE_IMPORTED_TARGETS_FOR_ALL_LIBS)
    target_link_libraries(${tplName}::all_libs  INTERFACE  ${importedTarget})
  endforeach()

  # Create the TriBITS-compliant <tplName>Config.cmake wrapper file
  tribits_extpkgwit_create_package_config_file(
    ${tplName}
    INNER_FIND_PACKAGE_NAME ${PARSE_INNER_FIND_PACKAGE_NAME}
    IMPORTED_TARGETS_FOR_ALL_LIBS ${PARSE_IMPORTED_TARGETS_FOR_ALL_LIBS} )

endfunction()


# @FUNCTION: tribits_extpkgwit_create_package_config_file()
#
# Create the ``<tplName>Config.cmake`` file for a TriBITS external package/TPL
# that is defined by a set of IMPORTED targets by call to
# ``find_package(<externalPkg>)``
#
# Usage::
#
#   tribits_extpkgwit_create_package_config_file( <tplName>
#     INNER_FIND_PACKAGE_NAME <externalPkg>
#     IMPORTED_TARGETS_FOR_ALL_LIBS <importedTarget0> <importedTarget1> ... )
#
function(tribits_extpkgwit_create_package_config_file  tplName)
  # Parse arguments
  cmake_parse_arguments(
     PARSE_ARGV 1
     PARSE "" "" # prefix, options, one_value_keywords
     "INNER_FIND_PACKAGE_NAME;IMPORTED_TARGETS_FOR_ALL_LIBS"  #multi_value_keywords
     )
  tribits_check_for_unparsed_arguments(PARSE)
  tribits_assert_parse_arg_one_value(PARSE  INNER_FIND_PACKAGE_NAME)
  tribits_assert_parse_arg_one_or_more_values(PARSE  IMPORTED_TARGETS_FOR_ALL_LIBS)
  set(externalPkg ${PARSE_INNER_FIND_PACKAGE_NAME})

  # Create header for <tplName>Config.cmake file
  set(configFileStr "")
  tribits_extpkgwit_append_package_config_file_header_str(
    ${tplName}  ${externalPkg}  configFileStr)

  # Get ${externalPkg} from where you found it before (see note below)
  tribits_extpkgwit_append_find_dependency_external_package_str(
    ${tplName}  ${externalPkg}  configFileStr)

  # Pull in upstream <UpstreamPkg>Config.cmake files
  tribits_extpkg_append_find_upstream_dependencies_str(${tplName} configFileStr)

  # Add the ${tplName}::all_libs target and link to this ${externalPkg}
  # package's native IMPORTED targets
  tribits_extpkg_append_create_all_libs_target_str( ${tplName}
    LIB_TARGETS_LIST  ${PARSE_IMPORTED_TARGETS_FOR_ALL_LIBS}
    CONFIG_FILE_STR_INOUT  configFileStr )

  # Also link against upstream package's `<UpstreamPkg>::all_libs` targets
  tribits_extpkg_append_target_link_libraries_to_upstream_all_libs_targets_str(${tplName}
    ${tplName}::all_libs  configFileStr)

  tribits_extpkg_append_tribits_compliant_package_config_vars_str(${tplName}
    configFileStr)

  tribits_extpkg_write_package_config_file_from_str(${tplName}  "${configFileStr}")
endfunction()


function(tribits_extpkgwit_append_find_dependency_external_package_str
    tplName  externalPkg  configFileStrVarInOut
  )
  set(configFileStr "${${configFileStrVarInOut}}")
  if (${externalPkg}_DIR)
    string(APPEND configFileStr
      "set(${externalPkg}_DIR \"${${externalPkg}_DIR}\")\n" )
  endif()
  string(APPEND configFileStr
    "find_dependency(${externalPkg})\n\n")
  set(${configFileStrVarInOut} "${configFileStr}" PARENT_SCOPE)
endfunction()
#
# NOTE: Above, ${externalPkg}_DIR is only set when
# find_package(${externalPkg}) finds a package configure file
# ${externalPkg}Config.cmake and **not** when it uses a
# Find${externalPkg}.cmake module.  Therefore, there is no reason to set
# ${externalPkg}_DIR in this file if it will not be used.


function(tribits_extpkgwit_append_package_config_file_header_str
    tplName  externalPkg  configFileStrVarInOut
  )
  set(configFileStr "${${configFileStrVarInOut}}")
  string(APPEND configFileStr
    "# TriBITS-compliant Package config file for external package/TPL '${tplName}'\n"
    "# based on non fully TriBITS-compliant external package '${externalPkg}' that uses\n"
    "# modern IMPORTED targets\n"
    "#\n"
    "# Generated by CMake, do not edit!\n"
    "\n"
    "# Guard against multiple inclusion\n"
    "if (TARGET ${tplName}::all_libs)\n"
    "  return()\n"
    "endif()\n"
    "\n"
    "include(CMakeFindDependencyMacro)\n\n"
    )
  set(${configFileStrVarInOut} "${configFileStr}" PARENT_SCOPE)
endfunction()
