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


include(TribitsProcessPackagesAndDirsLists)
include(TribitsAddOptionAndDefine)
include(TribitsGeneralMacros)
include(TribitsPrintEnabledPackagesLists)
include(TribitsPrintDependencyInfo)
include(TribitsPackageDependencies)
include(TribitsGetPackageEnableStatus)

include(AdvancedOption)
include(AdvancedSet)
include(AppendStringVar)
include(CMakeBuildTypesList)
include(FindListElement)
include(GlobalNullSet)
include(PrintNonemptyVar)
include(PrintVarWithSpaces)
include(PrintNonemptyVarWithSpaces)
include(PrintVar)
include(RemoveGlobalDuplicates)
include(SetDefault)
include(MessageWrapper)
include(DualScopeSet)
include(CMakeParseArguments)
include(TribitsCreateReverseList)


# NOTE: A nice way to view and navigate the contents of this file is to use
# the emacs 'occur' string:
#
#   "\(^##########\|^# .*-level\|^function\|^macro\)"


# @MACRO: tribits_adjust_package_enables()
#
# Usage:
#
#   tribits_adjust_package_enables()
#
# Macro that adjusts all of the package enables from what the user input to
# the final set that will be used to enable packages.
#
macro(tribits_adjust_package_enables)
  tribits_unenable_enabled_packages()
  tribits_sweep_forward_apply_disables()
  tribits_sweep_forward_apply_enables()
  tribits_disable_and_enable_tests_and_examples()
  tribits_sweep_backward_enable_upstream_packages()
  tribits_sweep_backward_enable_required_tpls()
  # ToDo #63: Merge behavior of the above macro into
  # tribits_sweep_backward_enable_upstream_packages() as part of #63.
  tribits_set_cache_vars_for_current_enabled_packages()
  tribits_enable_parent_package_for_subpackage_enable()
  tribits_set_up_enabled_lists_and_pkg_idx()
  tribits_setup_direct_packages_dependencies_lists_and_lib_required_enable_vars()
  tribits_print_direct_packages_dependencies_lists()
endmacro()


################################################################################
#
# First-level macros called directly from ``tribits_adjust_package_enables()``
#
# NOTE: In the below macros, local variables are prefixed by 'tap1_' in all of
# the macros() which will not clash because they are at the same level in the
# call stack (and are initialized in each macro).
# 
################################################################################


# @MACRO: tribits_unenable_enabled_packages()
#
# Macro to enable all unenabled packages if asked.
#
# See implementation for details.
#
macro(tribits_unenable_enabled_packages)
  if (${PROJECT_NAME}_UNENABLE_ENABLED_PACKAGES)
    message("\nSetting to empty '' all enabled packages because"
      " ${PROJECT_NAME}_UNENABLE_ENABLED_PACKAGES="
      "'${${PROJECT_NAME}_UNENABLE_ENABLED_PACKAGES}'\n")
    foreach(tap1_tribitsPkg  IN LISTS  ${PROJECT_NAME}_DEFINED_INTERNAL_PACKAGES)
      if (${PROJECT_NAME}_ENABLE_${tap1_tribitsPkg})
        message("-- " "Setting ${PROJECT_NAME}_ENABLE_${tap1_tribitsPkg}=''")
        set_cache_on_off_empty(${PROJECT_NAME}_ENABLE_${tap1_tribitsPkg} ""
          "Forced to empty '' by ${PROJECT_NAME}_UNENABLE_ENABLED_PACKAGES=ON" FORCE)
      endif()
      # NOTE: Above, we don't want to set to empty those packages that have hard
      # disables because this will mess up the logic in later invocations.
    endforeach()
    advanced_set(${PROJECT_NAME}_UNENABLE_ENABLED_PACKAGES OFF CACHE BOOL
      "Forced to FALSE after use" FORCE)
  endif()
endmacro()


# @MACRO: tribits_sweep_forward_apply_disables()
#
# Sweep forward and apply all disables in order first.
#
# See implementation for details.
#
macro(tribits_sweep_forward_apply_disables)

  message("\nDisabling all packages that have a required dependency"
    " on disabled TPLs and optional package TPL support based on TPL_ENABLE_<TPL>=OFF ...\n")

  message("\nDisabling subpackages for hard disables of parent packages"
    " due to ${PROJECT_NAME}_ENABLE_<PARENT_PACKAGE>=OFF ...\n")
  foreach(tad1_tribitsPkg  IN LISTS  ${PROJECT_NAME}_DEFINED_INTERNAL_PACKAGES)
    tribits_disable_parents_subpackages(${tad1_tribitsPkg})
  endforeach()

  message("\nDisabling forward required packages and optional intra-package"
    " support that have a dependency on disabled packages"
    " ${PROJECT_NAME}_ENABLE_<TRIBITS_PACKAGE>=OFF (or"
    " TPL_ENABLE_<TRIBITS_EXTERNAL_PACKAGE>=OFF) ...\n")
  foreach(tad1_tribitsPkg  IN LISTS  ${PROJECT_NAME}_DEFINED_PACKAGES)
    tribits_disable_forward_required_dep_packages(${tad1_tribitsPkg})
  endforeach()

endmacro()


# @MACRO: tribits_sweep_forward_apply_enables()
#
# Updates the following variables in the local scope:
#
#   * ``${PROJECT_NAME}_NOTDISABLED_INTERNAL_PACKAGES``
#   * `${PROJECT_NAME}_ENABLED_INTERNAL_PACKAGES`_
#
# See implementation for details.
#
macro(tribits_sweep_forward_apply_enables)

  tribits_get_sublist_nondisabled( ${PROJECT_NAME}_DEFINED_INTERNAL_PACKAGES
    ${PROJECT_NAME}_NOTDISABLED_INTERNAL_PACKAGES "")
  tribit_create_reverse_list(${PROJECT_NAME}_NOTDISABLED_INTERNAL_PACKAGES
    ${PROJECT_NAME}_REVERSE_NOTDISABLED_INTERNAL_PACKAGES)

  message("\nEnabling subpackages for hard enables of parent packages"
    " due to ${PROJECT_NAME}_ENABLE_<PARENT_PACKAGE>=ON ...\n")
  foreach(tad1_tribitsPkg  IN LISTS  ${PROJECT_NAME}_NOTDISABLED_INTERNAL_PACKAGES)
    tribits_enable_parents_subpackages(${tad1_tribitsPkg})
  endforeach()

  if (${PROJECT_NAME}_ENABLE_ALL_PACKAGES)
    message("\nEnabling all packages that are not currently disabled because of"
      " ${PROJECT_NAME}_ENABLE_ALL_PACKAGES=ON"
      " (${PROJECT_NAME}_ENABLE_SECONDARY_TESTED_CODE="
      "${${PROJECT_NAME}_ENABLE_SECONDARY_TESTED_CODE}) ...\n")
    foreach(tad1_tribitsPkg  IN LISTS  ${PROJECT_NAME}_NOTDISABLED_INTERNAL_PACKAGES)
      tribits_apply_all_package_enables(${tad1_tribitsPkg})
    endforeach()
  endif()

  if (${PROJECT_NAME}_ENABLE_ALL_FORWARD_DEP_PACKAGES)
    message("\nSweep forward enabling all forward library dependent packages because"
      " ${PROJECT_NAME}_ENABLE_ALL_FORWARD_DEP_PACKAGES=ON ...\n")
    foreach(tad1_tribitsPkg   IN LISTS  ${PROJECT_NAME}_NOTDISABLED_INTERNAL_PACKAGES)
      tribits_enable_forward_lib_package_enables(${tad1_tribitsPkg})
    endforeach()

    tribits_get_sublist_enabled( ${PROJECT_NAME}_DEFINED_INTERNAL_PACKAGES
      ${PROJECT_NAME}_ENABLED_INTERNAL_PACKAGES "")
    tribit_create_reverse_list(${PROJECT_NAME}_ENABLED_INTERNAL_PACKAGES
      ${PROJECT_NAME}_REVERSE_ENABLED_INTERNAL_PACKAGES)

    message("\nSweep backward enabling all forward test dependent packages because"
      " ${PROJECT_NAME}_ENABLE_ALL_FORWARD_DEP_PACKAGES=ON ...\n")
    foreach(tad1_tribitsPkg   IN LISTS
        ${PROJECT_NAME}_REVERSE_ENABLED_INTERNAL_PACKAGES
      )
      tribits_enable_forward_test_package_enables(${tad1_tribitsPkg})
    endforeach()
    # NOTE: Above, we want to sweep backward to enable test-dependent packages
    # because we don't want to enable package Z just because package Y was enabled
    # because it had a test-only dependency on package X.  Sweeping backwards through
    # the packages makes sure this does not happen.
    set(${PROJECT_NAME}_ENABLE_ALL_OPTIONAL_PACKAGES ON)
  endif()

  tribits_get_sublist_enabled( ${PROJECT_NAME}_NOTDISABLED_INTERNAL_PACKAGES
    ${PROJECT_NAME}_ENABLED_INTERNAL_PACKAGES  "")

endmacro()
# NOTE: Above, we are sweeping over *all* of the not-disabled packages listed
# in ${PROJECT_NAME}_DEFINED_INTERNAL_PACKAGES, including those package that
# might have <Package>_PACKAGE_BUILD_STATUS=EXTERNAL.  That makes sense
# because these are TriBITS (or TriBITS compatible) packages so we should
# assume that all of their downstream packages, whether internal or external,
# should be enabled as well.  If we find this is not the desirable behavior,
# then we can change this later.


# @MACRO: tribits_disable_and_enable_tests_and_examples()
#
# Adjust test and example enables based on different criteria.
#
# See implementation for details.
#
macro(tribits_disable_and_enable_tests_and_examples)

  message("\nDisabling subpackage tests/examples based on parent package"
    " tests/examples disables ...\n")
  foreach(tad1_tribitsPkg  IN LISTS
      ${PROJECT_NAME}_DEFINED_INTERNAL_TOPLEVEL_PACKAGES
    )
    tribits_apply_package_examples_disable(${tad1_tribitsPkg} TESTS)
    tribits_apply_subpackage_tests_or_examples_disables(${tad1_tribitsPkg} TESTS)
    tribits_apply_subpackage_tests_or_examples_disables(${tad1_tribitsPkg} EXAMPLES)
  endforeach()

  if (${PROJECT_NAME}_ENABLE_TESTS  OR  ${PROJECT_NAME}_ENABLE_EXAMPLES)
    message("\nEnabling all tests and/or examples that have not been"
      " explicitly disabled because ${PROJECT_NAME}_ENABLE_[TESTS,EXAMPLES]=ON ...\n")
    foreach(tad1_tribitsPkg  IN LISTS  ${PROJECT_NAME}_ENABLED_INTERNAL_PACKAGES)
      tribits_apply_test_example_enables(${tad1_tribitsPkg})
    endforeach()
  endif()
  # NOTE: Above, we enable tests and examples here, before the remaining required
  # packages so that we don't enable tests that don't need to be enabled based
  # on the use of the option ${PROJECT_NAME}_ENABLE_ALL_FORWARD_DEP_PACKAGES.

  message("\nEnabling subpackage tests/examples based on parent package tests/examples enables ...\n")
  foreach(tad1_tribitsPkg  IN LISTS
      ${PROJECT_NAME}_DEFINED_INTERNAL_TOPLEVEL_PACKAGES
    )
    tribits_apply_subpackage_tests_examples_enables(${tad1_tribitsPkg})
  endforeach()
  # NOTE: We want to apply this logic here instead of later after the backward
  # sweep of package enables because we don't want to enable the
  # tests/examples for a subpackage if it is not needed based on set of
  # requested subpackages and packages to be enabled and the optional forward
  # sweep of downstream packages.

endmacro()


# @MACRO: tribits_sweep_backward_enable_upstream_packages()
#
# Sweep backwards and enable required and (optionally) optional upstream
# packages.
#
# This sets the final value for:
#
# * `${PROJECT_NAME}_ENABLED_INTERNAL_PACKAGES`_
#
# See implementation for details.
#
macro(tribits_sweep_backward_enable_upstream_packages)

  set(tap1_extraMsgStr "")
  if (${PROJECT_NAME}_ENABLE_ALL_OPTIONAL_PACKAGES)
    set(tap1_extraMsgStr
       " (and optional since ${PROJECT_NAME}_ENABLE_ALL_OPTIONAL_PACKAGES=ON)")
  endif()

  message("\nEnabling all required${tap1_extraMsgStr} upstream packages for current"
    " set of enabled packages (${PROJECT_NAME}_ENABLE_SECONDARY_TESTED_CODE="
    "${${PROJECT_NAME}_ENABLE_SECONDARY_TESTED_CODE}) ...\n")
  foreach(tad1_tribitsPkg  IN LISTS  ${PROJECT_NAME}_REVERSE_NOTDISABLED_INTERNAL_PACKAGES)
    tribits_enable_upstream_packages(${tad1_tribitsPkg})
  endforeach()
  # NOTE: Above, we have to loop through the packages backward to enable all
  # the packages that feed into these packages.  This has to include *all*
  # upstream package enables including required packages, and optional
  # packages (when ${PROJECT_NAME}_ENABLE_ALL_OPTIONAL_PACKAGES).

  tribits_get_sublist_enabled( ${PROJECT_NAME}_NOTDISABLED_INTERNAL_PACKAGES
    ${PROJECT_NAME}_ENABLED_INTERNAL_PACKAGES  "")

  message("\nEnabling all optional intra-package enables"
    " <TRIBITS_PACKAGE>_ENABLE_<DEPPACKAGE> that are not currently disabled"
    " if both sets of packages are enabled ...\n")
  foreach(tad1_tribitsPkg  IN LISTS  ${PROJECT_NAME}_ENABLED_INTERNAL_PACKAGES)
    tribits_postprocess_optional_package_enables(${tad1_tribitsPkg})
  endforeach()

endmacro()


# @MACRO: tribits_sweep_backward_enable_required_tpls()
#
# Enable the TPLs required by the internal packages that are enabled
#
# See implementation for details.
#
macro(tribits_sweep_backward_enable_required_tpls)

  message("\nEnabling all remaining required TPLs for current set of"
    " enabled packages ...\n")
  foreach(tad1_tribitsPkg  IN LISTS  ${PROJECT_NAME}_ENABLED_INTERNAL_PACKAGES)
    tribits_enable_required_tpls(${tad1_tribitsPkg})
  endforeach()

  message("\nEnabling all optional package TPL support"
    " <TRIBITS_PACKAGE>_ENABLE_<DEPTPL> not currently disabled for"
    " enabled TPLs ...\n")
  foreach(tad1_tribitsPkg  IN LISTS  ${PROJECT_NAME}_ENABLED_INTERNAL_PACKAGES)
    tribits_postprocess_optional_tpl_enables(${tad1_tribitsPkg})
  endforeach()

  message("\nEnabling TPLs based on <TRIBITS_PACKAGE>_ENABLE_<TPL>=ON if TPL is not explicitly disabled ...\n")
  foreach(tad1_tribitsPkg  IN LISTS  ${PROJECT_NAME}_ENABLED_INTERNAL_PACKAGES)
    tribits_enable_optional_tpls(${tad1_tribitsPkg})
  endforeach()
  # NOTE: We need to do this after the above optional package TPL support
  # logic so that the TPL will be turned on for this package only as requested
  # in bug 4298.

endmacro()


# @MACRO: tribits_set_cache_vars_for_current_enabled_packages()
#
macro(tribits_set_cache_vars_for_current_enabled_packages)
  message("\nSet cache entries for optional packages/TPLs and tests/examples for packages actually enabled ...\n")
  foreach(tad1_tribitsPkg  IN LISTS  ${PROJECT_NAME}_ENABLED_INTERNAL_PACKAGES)
    tribits_set_up_optional_package_enables_and_cache_vars(${tad1_tribitsPkg})
  endforeach()
endmacro()


# @MACRO: tribits_enable_parent_package_for_subpackage_enable()
#
macro(tribits_enable_parent_package_for_subpackage_enable)

  message("\nEnabling the shell of non-enabled parent packages (mostly for show) that have at least one subpackage enabled ...\n")
  foreach(tad1_tribitsPkg  IN LISTS
      ${PROJECT_NAME}_DEFINED_INTERNAL_TOPLEVEL_PACKAGES
    )
    tribits_postprocess_package_with_subpackages_enables(${tad1_tribitsPkg})
  endforeach()
  # NOTE: The above ensures that loops involving the parent package will
  # process the parent package but doing this last ensures that no downstream
  # dependencies will be enabled.

endmacro()


# @MACRO: tribits_setup_direct_packages_dependencies_lists_and_lib_required_enable_vars()
#
# Set up flat list of direct external and inner package dependencies (even for
# non-enabled packages) and enabled package dependencies for enabled packages.
#
macro(tribits_setup_direct_packages_dependencies_lists_and_lib_required_enable_vars)

  foreach(tad1_externalPkgName  IN LISTS  ${PROJECT_NAME}_DEFINED_TPLS)
    tribits_extpkg_setup_enabled_dependencies(${tad1_externalPkgName})
    # ToDo: Assert that all of the listed dependencies in
    # ${tad1_externalPkgName}_LIB_ENABLED_DEPENDENCIES exist and are
    # upstream from ${tad1_externalPkgName}
  endforeach()

  foreach(tad1_internalPkgName   IN LISTS
      ${PROJECT_NAME}_DEFINED_INTERNAL_PACKAGES
    )
    tribits_setup_enabled_dependencies_lists_and_enable_vars(${tad1_internalPkgName})
  endforeach()

endmacro()


# @MACRO: tribits_print_direct_packages_dependencies_lists()
#
macro(tribits_print_direct_packages_dependencies_lists)
  if (${PROJECT_NAME}_DUMP_PACKAGE_DEPENDENCIES)
    message("\nDumping direct enabled dependencies for each package ...")
    foreach(tad1_tribitsPkg  IN  LISTS  ${PROJECT_NAME}_DEFINED_PACKAGES)
      tribits_print_direct_package_dependencies_lists(${tad1_tribitsPkg})
    endforeach()
  endif()
endmacro()



################################################################################
#
# Second-level macros called indirectly from ``tribits_adjust_package_enables()``
#
################################################################################


# Macro that disables all of the subpackages of a parent package.
#
macro(tribits_disable_parents_subpackages PARENT_PACKAGE_NAME)

  if(NOT ${PROJECT_NAME}_ENABLE_${PARENT_PACKAGE_NAME}
    AND NOT ${PROJECT_NAME}_ENABLE_${PARENT_PACKAGE_NAME} STREQUAL ""
    )

    set(SUBPACKAGE_IDX 0)
    foreach(tap2_subPkgName   IN LISTS  ${PARENT_PACKAGE_NAME}_SUBPACKAGES)

      set(subpkgFullName ${PARENT_PACKAGE_NAME}${tap2_subPkgName})

      if (NOT ${PROJECT_NAME}_ENABLE_${subpkgFullName} STREQUAL "OFF")
        set(ENABLE_BEING_DISABLED_VAR_NAME ${PROJECT_NAME}_ENABLE_${subpkgFullName})
        message("-- "
          "Setting subpackage enable ${ENABLE_BEING_DISABLED_VAR_NAME}=OFF"
          " because parent package ${PROJECT_NAME}_ENABLE_${PARENT_PACKAGE_NAME}=OFF")
        set(${ENABLE_BEING_DISABLED_VAR_NAME} OFF)
      endif()

      math(EXPR SUBPACKAGE_IDX "${SUBPACKAGE_IDX}+1")

    endforeach()

  endif()

endmacro()


# Macro that disables forward package that depends on the passed-in package
#
macro(tribits_disable_forward_required_dep_packages  packageName)
  tribits_get_package_enable_status(${packageName}  packageEnable  "")
  if ((NOT packageEnable) AND (NOT "${packageEnable}" STREQUAL ""))
    foreach(fwdDepPkg  IN LISTS  ${packageName}_FORWARD_LIB_DEFINED_DEPENDENCIES)
      if (${fwdDepPkg}_LIB_DEP_REQUIRED_${packageName})
        tribits_private_disable_required_package_enables(${fwdDepPkg}
          ${packageName} TRUE)
      else()
        tribits_private_disable_optional_package_enables(${fwdDepPkg}
          ${packageName} TRUE)
      endif()
    endforeach()
    foreach(fwdDepPkg  IN LISTS  ${packageName}_FORWARD_TEST_DEFINED_DEPENDENCIES)
      if (${fwdDepPkg}_TEST_DEP_REQUIRED_${packageName})
        tribits_private_disable_required_package_enables(${fwdDepPkg}
          ${packageName} FALSE)
      endif()
    endforeach()
  endif()
endmacro()


# Macro that enables all of the subpackages of a parent package.
#
macro(tribits_enable_parents_subpackages  parentPackageName)

  if(${PROJECT_NAME}_ENABLE_${parentPackageName})

    set(subpkgIdx 0)
    foreach(tap2_subPkgName  IN LISTS  ${parentPackageName}_SUBPACKAGES)

      set(subpkgFullName ${parentPackageName}${tap2_subPkgName})

      if (NOT ${PROJECT_NAME}_ENABLE_${subpkgFullName} AND
        NOT "${${PROJECT_NAME}_ENABLE_${subpkgFullName}}" STREQUAL ""
        )
        # The subpackage is already disabled and is not just empty!
      elseif (${PROJECT_NAME}_ENABLE_${subpkgFullName})
        # The subpackage is already enabled so there is no reason to enable it!
      else()
        # The subpackage is not hard off or on so turn it on by default
        tribits_implicit_package_enable_is_allowed( "" ${subpkgFullName}
          subpkgAllowImplicitEnable)
        if (subpkgAllowImplicitEnable)
          set(enableVarName ${PROJECT_NAME}_ENABLE_${subpkgFullName})
          message("-- "
            "Setting subpackage enable ${enableVarName}=ON"
            " because parent package ${PROJECT_NAME}_ENABLE_${parentPackageName}="
	    "${${PROJECT_NAME}_ENABLE_${parentPackageName}}")
          set(${enableVarName} ON)
        endif()
      endif()

      math(EXPR  subpkgIdx "${subpkgIdx}+1")

    endforeach()

  endif()

endmacro()


# Macro used to set ${PROJECT_NAME}_ENABLE_${PACKAGE_NAME} based on
# ${PROJECT_NAME}_ENABLE_ALL_PACKAGES
#
macro(tribits_apply_all_package_enables  packageName)
  tribits_is_primary_meta_project_package(${packageName}  packageIsPmpp)
  tribits_implicit_package_enable_is_allowed( "" ${packageName}
    processThisPackageEnable )
  if (packageIsPmpp  AND  processThisPackageEnable)
    tribits_set_package_enable_based_on_project_enable(
      ${PROJECT_NAME}_ENABLE_ALL_PACKAGES  ${PROJECT_NAME}_ENABLE_${packageName} )
  endif()
endmacro()


# Macro used to set ${PROJECT_NAME}_ENABLE_${FWD_PACKAGE_NAME}=ON for all
# forward required or optional LIB dependency on ${packageName}
#
macro(tribits_enable_forward_lib_package_enables  packageName)
  if (${PROJECT_NAME}_ENABLE_${packageName})
    foreach(fwdDepPkgName  IN LISTS  ${packageName}_FORWARD_LIB_DEFINED_DEPENDENCIES)
      tribits_private_enable_forward_package(${fwdDepPkgName} ${packageName})
    endforeach()
  endif()
endmacro()


# Macro used to set ${PROJECT_NAME}_ENABLE_${FWD_PACKAGE_NAME}=ON for all
# forward required or optional TEST dependency on ${packageName}
#
macro(tribits_enable_forward_test_package_enables  packageName)
  foreach(fwdDepPkgName  IN LISTS  ${packageName}_FORWARD_TEST_DEFINED_DEPENDENCIES)
    tribits_private_enable_forward_package(${fwdDepPkgName} ${packageName})
  endforeach()
endmacro()
# NOTE: The above macro does not need to check if ${packageName} is enabled
# because it will only be called for packages that are enabled already.  This
# not only improves performance but it also aids in testing.


# Macro that sets the required TPLs for given package
#
macro(tribits_enable_required_tpls PACKAGE_NAME)

  assert_defined(${PROJECT_NAME}_ENABLE_${PACKAGE_NAME})

  if (${PROJECT_NAME}_ENABLE_${PACKAGE_NAME})

    foreach(DEP_TPL  IN LISTS  ${PACKAGE_NAME}_LIB_REQUIRED_DEP_TPLS)
      tribits_private_enable_dep_tpl(${PACKAGE_NAME} ${DEP_TPL})
    endforeach()

    foreach(DEP_TPL  IN LISTS  ${PACKAGE_NAME}_TEST_REQUIRED_DEP_TPLS)
      tribits_private_enable_dep_tpl(${PACKAGE_NAME} ${DEP_TPL})
    endforeach()

  endif()

endmacro()


# Post-processes optional package TPL based on if the TPL
# has been enabled or not
#
macro(tribits_postprocess_optional_tpl_enables PACKAGE_NAME)

  if (${PROJECT_NAME}_ENABLE_${PACKAGE_NAME})

    foreach(OPTIONAL_DEP_TPL ${${PACKAGE_NAME}_LIB_OPTIONAL_DEP_TPLS})
      tribits_private_postprocess_optional_tpl_enable(
        ${PACKAGE_NAME} ${OPTIONAL_DEP_TPL} )
    endforeach()

    foreach(OPTIONAL_DEP_TPL ${${PACKAGE_NAME}_TEST_OPTIONAL_DEP_TPLS})
      tribits_private_postprocess_optional_tpl_enable(
        ${PACKAGE_NAME} ${OPTIONAL_DEP_TPL} )
    endforeach()

  endif()

endmacro()


# Macro that enables the optional TPLs for given package
#
macro(tribits_enable_optional_tpls PACKAGE_NAME)

  assert_defined(${PROJECT_NAME}_ENABLE_${PACKAGE_NAME})

  if (${PROJECT_NAME}_ENABLE_${PACKAGE_NAME})

    foreach(DEP_TPL ${${PACKAGE_NAME}_LIB_OPTIONAL_DEP_TPLS})
      tribits_private_enable_optional_dep_tpl(${PACKAGE_NAME} ${DEP_TPL})
    endforeach()

    foreach(DEP_TPL ${${PACKAGE_NAME}_TEST_OPTIONAL_DEP_TPLS})
      tribits_private_enable_optional_dep_tpl(${PACKAGE_NAME} ${DEP_TPL})
    endforeach()

  endif()

endmacro()


# Macro that sets cache vars for optional package interdependencies
#
# This also will set ${PACKAGE_NAME}_ENABLE_TESTS and
# ${PACKAGE_NAME}_ENABLE_EXAMPLES to empty non-cache vars
#
macro(tribits_set_up_optional_package_enables_and_cache_vars PACKAGE_NAME)

  assert_defined(${PROJECT_NAME}_ENABLE_${PACKAGE_NAME})
  set(SET_AS_CACHE ${${PROJECT_NAME}_ENABLE_${PACKAGE_NAME}})

  if (SET_AS_CACHE)

    multiline_set(DOCSTR
      "Build tests for the package ${PACKAGE_NAME}.  Set to 'ON', 'OFF', or leave empty ''"
       " to allow for other logic to decide."
       )
    set_cache_on_off_empty( ${PACKAGE_NAME}_ENABLE_TESTS "" ${DOCSTR} )

    multiline_set(DOCSTR
      "Build examples for the package ${PACKAGE_NAME}.  Set to 'ON', 'OFF', or leave empty ''"
       " to allow for other logic to decide."
       )
    set_cache_on_off_empty( ${PACKAGE_NAME}_ENABLE_EXAMPLES "" ${DOCSTR} )

    multiline_set(DOCSTR
      "Build examples for the package ${PACKAGE_NAME}.  Set to 'ON', 'OFF', or leave empty ''"
       " to allow for other logic to decide."
       )
    set( ${PACKAGE_NAME}_SKIP_CTEST_ADD_TEST
      "${${PROJECT_NAME}_SKIP_CTEST_ADD_TEST}" CACHE BOOL ${DOCSTR} )

  else()

    if (NOT DEFINED ${PACKAGE_NAME}_ENABLE_TESTS)
      set( ${PACKAGE_NAME}_ENABLE_TESTS "" )
    endif()
    if (NOT DEFINED ${PACKAGE_NAME}_ENABLE_EXAMPLES)
      set( ${PACKAGE_NAME}_ENABLE_EXAMPLES "" )
    endif()

  endif()

  foreach(OPTIONAL_DEP_PACKAGE ${${PACKAGE_NAME}_LIB_OPTIONAL_DEP_PACKAGES})
    tribits_private_add_optional_package_enable(
      ${PACKAGE_NAME} ${OPTIONAL_DEP_PACKAGE} "library" "${SET_AS_CACHE}" )
  endforeach()

  foreach(OPTIONAL_DEP_PACKAGE ${${PACKAGE_NAME}_TEST_OPTIONAL_DEP_PACKAGES})
    tribits_private_add_optional_package_enable(
      ${PACKAGE_NAME} ${OPTIONAL_DEP_PACKAGE} "test" "${SET_AS_CACHE}" )
  endforeach()

  foreach(OPTIONAL_DEP_TPL ${${PACKAGE_NAME}_LIB_OPTIONAL_DEP_TPLS})
    tribits_private_add_optional_tpl_enable(
      ${PACKAGE_NAME} ${OPTIONAL_DEP_TPL} "library" "${SET_AS_CACHE}" )
  endforeach()

  foreach(OPTIONAL_DEP_TPL ${${PACKAGE_NAME}_TEST_OPTIONAL_DEP_TPLS})
    tribits_private_add_optional_tpl_enable(
      ${PACKAGE_NAME} ${OPTIONAL_DEP_TPL} "test" "${SET_AS_CACHE}" )
  endforeach()

endmacro()


# Macro that post-processes final package enables for packages with subpackage
# enables.
#
macro(tribits_postprocess_package_with_subpackages_enables  PACKAGE_NAME)
  foreach(tap2_subPkgName  IN LISTS  ${PACKAGE_NAME}_SUBPACKAGES)
    set(subpkgFullName ${PACKAGE_NAME}${tap2_subPkgName})
    if (${PROJECT_NAME}_ENABLE_${subpkgFullName}
        AND NOT ${PROJECT_NAME}_ENABLE_${PACKAGE_NAME}
      )
      message("-- "
        "Setting ${PROJECT_NAME}_ENABLE_${PACKAGE_NAME}=ON"
        " because ${PROJECT_NAME}_ENABLE_${subpkgFullName}=ON")
      set(${PROJECT_NAME}_ENABLE_${PACKAGE_NAME} ON)
      tribits_postprocess_package_with_subpackages_optional_subpackage_enables(
        ${PACKAGE_NAME})
      tribits_postprocess_package_with_subpackages_test_example_enables(
        ${PACKAGE_NAME}  TESTS)
      tribits_postprocess_package_with_subpackages_test_example_enables(
        ${PACKAGE_NAME}  EXAMPLES)
      # NOTE: We need to enable the parent package even if it was disabled by
      # some means before this because a subpackage is enabled.  But other
      # logic should ensure that the parent package is never disabled and a
      # subpackage is allowed to be enabled.
    endif()
  endforeach()
endmacro()


# Macro that sets up the flat list of direct package dependencies and enabled
# package dependencies and sets ${packageName}_ENABLE_${depPkg} for LIB
# dependencies
#
# This makes it easy to just loop over all of the direct upstream dependencies
# for a package or just the enabled dependencies.
#
# NOTES:
#
#  * ${packageName}_LIB_ENABLED_DEPENDENCIES is only set if ${packageName} is
#    enabled and will only contain the names of direct library upstream
#    internal and external packages ${depPkg} that are required or are
#    optional and ${packageName}_ENABLE_${depPkg} is set to ON.
#
#  * ${packageName}_TEST_ENABLED_DEPENDENCIES is only set if ${packageName} is
#    enabled and will only contain the names of direct test/example upstream
#    internal and external packages ${depPkg} that are required or are
#    optional and ${packageName}_ENABLE_${depPkg} is set to ON.
#
#  * Sets ${packageName}_ENABLE_${depPkg}=ON for every required dep package
#    for LIB dependencies (but not TEST dependencies).  This allows looping
#    over just ${packageName}_LIB_DEFINED_DEPENDENCIES looking at
#    ${packageName}_ENABLE_${depPkg} to see if the package is enable or not.
#    This also includes special logic for required subpackages for parent
#    packages where only the shell of the parent package is enabled and not
#    all of its required subpackages are enabled.
#
macro(tribits_setup_enabled_dependencies_lists_and_enable_vars  packageName)

  # LIB dependencies

  set(${packageName}_LIB_ENABLED_DEPENDENCIES "")

  foreach(depPkg ${${packageName}_LIB_REQUIRED_DEP_PACKAGES})
    if (${PROJECT_NAME}_ENABLE_${packageName} AND ${PROJECT_NAME}_ENABLE_${depPkg})
      set(${packageName}_ENABLE_${depPkg} ON)
      list(APPEND ${packageName}_LIB_ENABLED_DEPENDENCIES ${depPkg})
    endif()
  endforeach()
  # See below NOTE about required subpackage dependencies not being enabled in
  # some cases!

  foreach(depPkg ${${packageName}_LIB_OPTIONAL_DEP_PACKAGES})
    if (${PROJECT_NAME}_ENABLE_${packageName} AND ${packageName}_ENABLE_${depPkg})
      list(APPEND ${packageName}_LIB_ENABLED_DEPENDENCIES ${depPkg})
    endif()
  endforeach()

  foreach(depPkg ${${packageName}_LIB_REQUIRED_DEP_TPLS})
    if (${PROJECT_NAME}_ENABLE_${packageName})
      set(${packageName}_ENABLE_${depPkg} ON)
      list(APPEND ${packageName}_LIB_ENABLED_DEPENDENCIES ${depPkg})
    endif()
  endforeach()

  foreach(depPkg ${${packageName}_LIB_OPTIONAL_DEP_TPLS})
    if (${PROJECT_NAME}_ENABLE_${packageName} AND ${packageName}_ENABLE_${depPkg})
      list(APPEND ${packageName}_LIB_ENABLED_DEPENDENCIES ${depPkg})
    endif()
  endforeach()

  # TEST dependencies

  set(${packageName}_TEST_ENABLED_DEPENDENCIES "")

  if (${PROJECT_NAME}_ENABLE_${packageName}
      AND
      (${packageName}_ENABLE_TESTS OR ${packageName}_ENABLE_EXAMPLES)
    )
    set(enablePkgAndTestsOrExamples ON)
  else()
    set(enablePkgAndTestsOrExamples OFF)
  endif()

  foreach(depPkg ${${packageName}_TEST_REQUIRED_DEP_PACKAGES})
    if (enablePkgAndTestsOrExamples)
      list(APPEND ${packageName}_TEST_ENABLED_DEPENDENCIES ${depPkg})
    endif()
  endforeach()

  foreach(depPkg ${${packageName}_TEST_OPTIONAL_DEP_PACKAGES})
    if (enablePkgAndTestsOrExamples AND ${packageName}_ENABLE_${depPkg})
      list(APPEND ${packageName}_TEST_ENABLED_DEPENDENCIES ${depPkg})
    endif()
  endforeach()

  foreach(depPkg ${${packageName}_TEST_REQUIRED_DEP_TPLS})
    if (enablePkgAndTestsOrExamples)
      list(APPEND ${packageName}_TEST_ENABLED_DEPENDENCIES ${depPkg})
    endif()
  endforeach()

  foreach(depPkg ${${packageName}_TEST_OPTIONAL_DEP_TPLS})
    if (enablePkgAndTestsOrExamples AND ${packageName}_ENABLE_${depPkg})
      list(APPEND ${packageName}_TEST_ENABLED_DEPENDENCIES ${depPkg})
    endif()
  endforeach()

endmacro()
# NOTE: Above, a required dependency of an enabled package may not actually be
# enabled if it is a required subpackage of a parent package and the parent
# package was not actually enabled due to a dependency but the shell of the
# parent package was only enabled at the very end.  This is one of the more
# confusing aspects of the TriBITS dependency system.


# Function to print the direct package dependency lists
#
function(tribits_print_direct_package_dependencies_lists  packageName)
  message("")
  set(printedVar "")
  tribits_print_nonempty_package_deps_list(${packageName}  LIB  ENABLED  printedVar)
  tribits_print_nonempty_package_deps_list(${packageName}  TEST  ENABLED  printedVar)
  if (NOT printedVar)
    message("-- ${packageName}: No enabled dependencies!")
  endif()
endfunction()



################################################################################
#
# Third and lower-level macros called indirectly from
# ``tribits_adjust_package_enables()``
#
################################################################################


function(tribits_private_print_disable
  ENABLE_BEING_DISABLED_VAR_NAME  PACKAGE_WITH_SOMETHING_BEING_DISABLED
  DEP_TYPE_STR  THING_DISALBED_TYPE  THING_DISABLED_NAME
  )
  if (${ENABLE_BEING_DISABLED_VAR_NAME})
    if (${PROJECT_NAME}_DISABLE_ENABLED_FORWARD_DEP_PACKAGES)
      message(
        " ***\n"
        " *** NOTE: Setting ${ENABLE_BEING_DISABLED_VAR_NAME}=OFF"
        " which was '${${ENABLE_BEING_DISABLED_VAR_NAME}}' because"
        " ${PACKAGE_WITH_SOMETHING_BEING_DISABLED} has"
        " a required ${DEP_TYPE_STR} dependence on disabled"
        " ${THING_DISALBED_TYPE} ${THING_DISABLED_NAME}"
        " but ${PROJECT_NAME}_DISABLE_ENABLED_FORWARD_DEP_PACKAGES=ON!\n"
        " ***\n"
        )
    else()
      message(FATAL_ERROR
        " ***\n"
        " *** ERROR: Setting ${ENABLE_BEING_DISABLED_VAR_NAME}=OFF"
        " which was '${${ENABLE_BEING_DISABLED_VAR_NAME}}' because"
        " ${PACKAGE_WITH_SOMETHING_BEING_DISABLED} has"
        " a required ${DEP_TYPE_STR} dependence on disabled"
        " ${THING_DISALBED_TYPE} ${THING_DISABLED_NAME}!\n"
        " ***\n"
        )
    endif()
  else()
    message("-- "
      "Setting ${ENABLE_BEING_DISABLED_VAR_NAME}=OFF"
      " because ${PACKAGE_WITH_SOMETHING_BEING_DISABLED} has a required ${DEP_TYPE_STR}"
      " dependence on disabled ${THING_DISALBED_TYPE} ${THING_DISABLED_NAME}")
  endif()
endfunction()


macro(tribits_private_disable_tpl_required_package_enable
  TPL_NAME  PACKAGE_NAME  LIBRARY_DEP
  )

  # Only turn off PACKAGE_NAME libraries and test/examples if it
  # is currently enabled or could be enabled.

  assert_defined(${PROJECT_NAME}_ENABLE_${PACKAGE_NAME})
  if (${PROJECT_NAME}_ENABLE_${PACKAGE_NAME}
     OR ${PROJECT_NAME}_ENABLE_${PACKAGE_NAME} STREQUAL ""
     )

    if ("${LIBRARY_DEP}" STREQUAL "TRUE")

      tribits_private_print_disable(
        ${PROJECT_NAME}_ENABLE_${PACKAGE_NAME} ${PACKAGE_NAME} "library"
        "TPL" ${TPL_NAME}
        )

      set(${PROJECT_NAME}_ENABLE_${PACKAGE_NAME} OFF)

    else()

      set(DEP_TYPE_STR "test/example")

      if (${PACKAGE_NAME}_ENABLE_TESTS
        OR "${${PACKAGE_NAME}_ENABLE_TESTS}" STREQUAL ""
        )
        tribits_private_print_disable(
          ${PACKAGE_NAME}_ENABLE_TESTS ${PACKAGE_NAME} "${DEP_TYPE_STR}"
          "TPL" ${TPL_NAME}
          )
        set(${PACKAGE_NAME}_ENABLE_TESTS OFF)
      endif()

      if (${PACKAGE_NAME}_ENABLE_EXAMPLES
        OR "${${PACKAGE_NAME}_ENABLE_EXAMPLES}" STREQUAL ""
        )
        tribits_private_print_disable(
          ${PACKAGE_NAME}_ENABLE_EXAMPLES ${PACKAGE_NAME} "${DEP_TYPE_STR}"
          "TPL" ${TPL_NAME}
          )
        set(${PACKAGE_NAME}_ENABLE_EXAMPLES OFF)
      endif()

      # NOTE: We can't assert that ${PACKAGE_NAME}_ENABLE_TESTS or
      # ${PACKAGE_NAME}_ENABLE_EXAMPLES exists yet because
      # tribits_set_up_optional_package_enables_and_cache_vars() which defines
      # them is not called until after the final package enables are set.

    endif()

  endif()

endmacro()


function(tribits_private_print_disable_required_package_enable
  PACKAGE_NAME  PACKAGE_ENABLE_SOMETHING_VAR_NAME  FORWARD_DEP_PACKAGE_NAME
  DEP_TYPE_STR
  )
  tribits_private_print_disable(
    ${PACKAGE_ENABLE_SOMETHING_VAR_NAME} ${FORWARD_DEP_PACKAGE_NAME}
    "${DEP_TYPE_STR}" "package" ${PACKAGE_NAME} )
endfunction()


# Only turn off ${fwdDepPkgName} libraries or test/examples if it is currently
# enabled or could be enabled
#
macro(tribits_private_disable_required_package_enables
    fwdDepPkgName  packageName  libraryDep
  )
  tribits_get_package_enable_status(${fwdDepPkgName}  ""  fwdDepPkgEnableVarName)
  if (${fwdDepPkgEnableVarName} OR ${fwdDepPkgEnableVarName} STREQUAL "")
    if ("${libraryDep}" STREQUAL "TRUE")
      tribits_private_print_disable_required_package_enable(
        ${packageName}  ${fwdDepPkgEnableVarName}
        ${fwdDepPkgName} "library" )
      set(${fwdDepPkgEnableVarName}  OFF)
    else()
      set(DEP_TYPE_STR "test/example")
      if (${fwdDepPkgName}_ENABLE_TESTS
        OR "${${fwdDepPkgName}_ENABLE_TESTS}" STREQUAL ""
        )
        tribits_private_print_disable_required_package_enable(
          ${packageName} ${fwdDepPkgName}_ENABLE_TESTS
          ${fwdDepPkgName} "${DEP_TYPE_STR}" )
        set(${fwdDepPkgName}_ENABLE_TESTS OFF)
      endif()

      if (${fwdDepPkgName}_ENABLE_EXAMPLES
        OR "${${fwdDepPkgName}_ENABLE_EXAMPLES}" STREQUAL ""
        )
        tribits_private_print_disable_required_package_enable(
          ${packageName} ${fwdDepPkgName}_ENABLE_EXAMPLES
          ${fwdDepPkgName} "${DEP_TYPE_STR}" )
        set(${fwdDepPkgName}_ENABLE_EXAMPLES OFF)
      endif()
    endif()
  endif()
endmacro()


macro(tribits_private_disable_optional_package_enables  fwdDepPkgName  packageName)

  if (${fwdDepPkgName}_ENABLE_${packageName}
      OR "${${fwdDepPkgName}_ENABLE_${packageName}}" STREQUAL ""
    )
    # Always disable the conditional enable but only print the message if the
    # package is enabled or if a disable overrides an enable
    if (${PROJECT_NAME}_ENABLE_${fwdDepPkgName})
      if (${fwdDepPkgName}_ENABLE_${packageName})  # is explicitly enabled already!
        message("-- "
          "NOTE: Setting ${fwdDepPkgName}_ENABLE_${packageName}=OFF"
          " which was ${${fwdDepPkgName}_ENABLE_${packageName}}"
          " because ${fwdDepPkgName} has an optional library dependence"
          " on disabled package ${packageName}")
      else()  # Not explicitly set
        message("-- "
          "Setting ${fwdDepPkgName}_ENABLE_${packageName}=OFF"
          " because ${fwdDepPkgName} has an optional library dependence"
          " on disabled package ${packageName}")
      endif()
    endif()
    if (${fwdDepPkgName}_ENABLE_${packageName}
        AND (NOT ${PROJECT_NAME}_ENABLE_${packageName})
        AND (NOT "${${PROJECT_NAME}_ENABLE_${packageName}}" STREQUAL "")
      )
      message("-- " "NOTE: ${fwdDepPkgName}_ENABLE_${packageName}="
        "${${fwdDepPkgName}_ENABLE_${packageName}} but"
        " ${PROJECT_NAME}_ENABLE_${packageName}="
        "${${PROJECT_NAME}_ENABLE_${packageName}} is set.  Setting"
        " ${fwdDepPkgName}_ENABLE_${packageName}=OFF!")
    endif()
    set(${fwdDepPkgName}_ENABLE_${packageName} OFF)
  endif()

endmacro()


macro(tribits_private_add_optional_package_enable PACKAGE_NAME  OPTIONAL_DEP_PACKAGE
  TYPE  SET_AS_CACHE_IN
  )

  if (SET_AS_CACHE_IN)

    multiline_set(DOCSTR
      "Enable optional ${TYPE} support in the package ${PACKAGE_NAME}"
      " for the package ${OPTIONAL_DEP_PACKAGE}."
      "  Set to 'ON', 'OFF', or leave empty"
      " to allow for other logic to decide."
      )

    set_cache_on_off_empty( ${PACKAGE_NAME}_ENABLE_${OPTIONAL_DEP_PACKAGE} ""
      ${DOCSTR} )

  else()

    if (NOT DEFINED ${PACKAGE_NAME}_ENABLE_${OPTIONAL_DEP_PACKAGE})
      set( ${PACKAGE_NAME}_ENABLE_${OPTIONAL_DEP_PACKAGE} "" )
    endif()

  endif()

endmacro()


macro(tribits_private_add_optional_tpl_enable PACKAGE_NAME OPTIONAL_DEP_TPL
  TYPE  SET_AS_CACHE_IN )

  if (SET_AS_CACHE_IN)

    multiline_set(DOCSTR
      "Enable optional ${TYPE} support in the package ${PACKAGE_NAME}"
      " for the TPL ${OPTIONAL_DEP_TPL}."
      "  Set to 'ON', 'OFF', or leave empty"
      " to allow for other logic to decide."
      )

    set_cache_on_off_empty( ${PACKAGE_NAME}_ENABLE_${OPTIONAL_DEP_TPL} ""
      ${DOCSTR} )

  else()

    if (NOT DEFINED ${PACKAGE_NAME}_ENABLE_${OPTIONAL_DEP_TPL})
      set( ${PACKAGE_NAME}_ENABLE_${OPTIONAL_DEP_TPL} "" )
    endif()

  endif()

endmacro()


# Enable optional intra-package support for enabled target package
# ${PACKAGE_NAME} (i.e. ${PROJECT_NAME}_ENABLE_${PACKAGE_NAME} is assumed to
# be TRUE before calling this macro.
#
macro(tribits_private_postprocess_optional_package_enable  packageName
    optDepPkg
  )

  if (${packageName}_ENABLE_${optDepPkg}  AND  ${PROJECT_NAME}_ENABLE_${optDepPkg})
    message("-- " "NOTE:"
      " ${packageName}_ENABLE_${optDepPkg}=${${packageName}_ENABLE_${optDepPkg}}"
      " is already set!")
  elseif ("${${packageName}_ENABLE_${optDepPkg}}" STREQUAL "")
    if (${PROJECT_NAME}_ENABLE_${optDepPkg})
      message("-- " "Setting ${packageName}_ENABLE_${optDepPkg}=ON"
       " since ${PROJECT_NAME}_ENABLE_${packageName}=ON AND"
       " ${PROJECT_NAME}_ENABLE_${optDepPkg}=ON")
      set(${packageName}_ENABLE_${optDepPkg}  ON)
    else()
      message("-- " "NOT setting ${packageName}_ENABLE_${optDepPkg}=ON"
       " since ${optDepPkg} is NOT enabled at this point!")
    endif()
  elseif ((NOT "${${packageName}_ENABLE_${optDepPkg}}" STREQUAL "")
      AND (NOT ${packageName}_ENABLE_${optDepPkg})
      AND ${PROJECT_NAME}_ENABLE_${optDepPkg}
    )
    message("-- " "NOTE: ${packageName}_ENABLE_${optDepPkg}="
      "${${packageName}_ENABLE_${optDepPkg}} is already set so not enabling even"
      " though ${PROJECT_NAME}_ENABLE_${optDepPkg}="
      "${${PROJECT_NAME}_ENABLE_${optDepPkg}} is set!")
  endif()

  string(TOUPPER  ${packageName}  packageName_UPPER)
  string(TOUPPER  ${optDepPkg}  optDepPkg_UPPER)
  set(MACRO_DEFINE_NAME  HAVE_${packageName_UPPER}_${optDepPkg_UPPER})

  if(${packageName}_ENABLE_${optDepPkg})
    set(${MACRO_DEFINE_NAME}  ON)
  else()
    set(${MACRO_DEFINE_NAME}  OFF)
  endif()

endmacro()


# Enable optional intra-package support for enabled target package
# ${PACKAGE_NAME} (i.e. ${PROJECT_NAME}_ENABLE_${PACKAGE_NAME} is assumed to
# be TRUE before calling this macro.
#
macro(tribits_private_postprocess_optional_tpl_enable  PACKAGE_NAME  OPTIONAL_DEP_TPL)

  if (${PACKAGE_NAME}_ENABLE_${OPTIONAL_DEP_TPL} AND TPL_ENABLE_${OPTIONAL_DEP_TPL})
    message("-- " "NOTE:"
      " ${PACKAGE_NAME}_ENABLE_${OPTIONAL_DEP_TPL}=${${PACKAGE_NAME}_ENABLE_${OPTIONAL_DEP_TPL}}"
      " is already set!")
  elseif (
    (NOT TPL_ENABLE_${OPTIONAL_DEP_TPL})
    AND
    (NOT "${TPL_ENABLE_${OPTIONAL_DEP_TPL}}" STREQUAL "")
    AND
    ${PACKAGE_NAME}_ENABLE_${OPTIONAL_DEP_TPL}
    )
    message(
      "\n***"
      "\n*** NOTE: Setting ${PACKAGE_NAME}_ENABLE_${OPTIONAL_DEP_TPL}=OFF"
      " which was ON since TPL_ENABLE_${OPTIONAL_DEP_TPL}=OFF"
      "\n***\n"
      )
    set(${PACKAGE_NAME}_ENABLE_${OPTIONAL_DEP_TPL} OFF)
  elseif ("${${PACKAGE_NAME}_ENABLE_${OPTIONAL_DEP_TPL}}" STREQUAL ""
    AND TPL_ENABLE_${OPTIONAL_DEP_TPL}
    )
    message("-- " "Setting ${PACKAGE_NAME}_ENABLE_${OPTIONAL_DEP_TPL}=ON"
      " since TPL_ENABLE_${OPTIONAL_DEP_TPL}=ON")
    set(${PACKAGE_NAME}_ENABLE_${OPTIONAL_DEP_TPL} ON)
  elseif (NOT "${${PACKAGE_NAME}_ENABLE_${OPTIONAL_DEP_TPL}}" STREQUAL ""
    AND NOT ${PACKAGE_NAME}_ENABLE_${OPTIONAL_DEP_TPL}
    AND TPL_ENABLE_${OPTIONAL_DEP_TPL}
    )
    message("-- " "NOTE: ${PACKAGE_NAME}_ENABLE_${OPTIONAL_DEP_TPL}=${${PACKAGE_NAME}_ENABLE_${OPTIONAL_DEP_TPL}}"
      " is already set so not enabling even though TPL_ENABLE_${OPTIONAL_DEP_TPL}=${TPL_ENABLE_${OPTIONAL_DEP_TPL}} is set!")
  endif()

  string(TOUPPER ${PACKAGE_NAME} PACKAGE_NAME_UPPER)
  string(TOUPPER ${OPTIONAL_DEP_TPL} OPTIONAL_DEP_TPL_UPPER)
  set(MACRO_DEFINE_NAME HAVE_${PACKAGE_NAME_UPPER}_${OPTIONAL_DEP_TPL_UPPER})

  if (${PACKAGE_NAME}_ENABLE_${OPTIONAL_DEP_TPL})
    set(${MACRO_DEFINE_NAME} ON)
  else()
    set(${MACRO_DEFINE_NAME} OFF)
  endif()

endmacro()


# Macro that post-processes optional dependencies after all other
# dependencies have been worked out
#
macro(tribits_postprocess_optional_package_enables packageName)

  if (${PROJECT_NAME}_ENABLE_${packageName})

    foreach(depPkg ${${packageName}_LIB_DEFINED_DEPENDENCIES})
      tribits_private_postprocess_optional_package_enable(
        ${packageName} ${depPkg} )
    endforeach()

    foreach(depPkg ${${packageName}_TEST_DEFINED_DEPENDENCIES})
      tribits_private_postprocess_optional_package_enable(
        ${packageName} ${depPkg} )
    endforeach()

  endif()

endmacro()
# NOTE: Above, it is harmless to process required dependencies as well so we
# leave of the if () statement based on
# ${packageName}_[LIB|TEST]_DEP_REQUIRED_${depPkg}.


# Set <ParentPackage>_ENABLE_<SubPackage>=ON if not already enabled for all
# subpackages of a parent package.
#
macro(tribits_postprocess_package_with_subpackages_optional_subpackage_enables
    PACKAGE_NAME
  )
  foreach(tap3_subPkg   IN LISTS  ${PACKAGE_NAME}_SUBPACKAGES)
    set(subpkgFullName ${PACKAGE_NAME}${tap3_subPkg})
    if (${PROJECT_NAME}_ENABLE_${subpkgFullName}
      AND "${${PACKAGE_NAME}_ENABLE_${subpkgFullName}}" STREQUAL ""
      )
      message("-- "
        "Setting ${PACKAGE_NAME}_ENABLE_${subpkgFullName}=ON"
        " because ${PROJECT_NAME}_ENABLE_${subpkgFullName}=ON")
      set(${PACKAGE_NAME}_ENABLE_${subpkgFullName} ON)
    endif()
  endforeach()
endmacro()


# Set the parent package tests/examples enables if one subpackage is enabled
# and has its tests/examples
#
macro(tribits_postprocess_package_with_subpackages_test_example_enables
    PACKAGE_NAME  TESTS_OR_EXAMPLES
  )
  foreach(tap3_subPkg  IN LISTS  ${PACKAGE_NAME}_SUBPACKAGES)
    set(subpkgFullName ${PACKAGE_NAME}${tap3_subPkg})
    if (${subpkgFullName}_ENABLE_${TESTS_OR_EXAMPLES}
      AND "${${PACKAGE_NAME}_ENABLE_${TESTS_OR_EXAMPLES}}" STREQUAL ""
      )
      message("-- "
        "Setting ${PACKAGE_NAME}_ENABLE_${TESTS_OR_EXAMPLES}=ON"
        " because ${subpkgFullName}_ENABLE_${TESTS_OR_EXAMPLES}=ON")
      set(${PACKAGE_NAME}_ENABLE_${TESTS_OR_EXAMPLES} ON)
    endif()
  endforeach()
endmacro()


# Set an individual package variable enable variable (to on or off) based on a
# global enable value
#
macro(tribits_set_package_enable_based_on_project_enable  projectEnableVar
    packageEnableVar
  )

  if ("${${packageEnableVar}}" STREQUAL "")
    if (${projectEnableVar})
      message("-- " "Setting ${packageEnableVar}=ON")
      set(${packageEnableVar} ON)
    elseif ( (NOT ${projectEnableVar})
        AND (NOT "${projectEnableVar}" STREQUAL "")
      )
      message("-- " "Setting ${packageEnableVar}=OFF")
      set(${packageEnableVar} OFF)
    else()
      # Otherwise, we will leave it up the the individual package
      # to decide?
    endif()
  else()
    # "${packageEnableVar} not at the default empty ''
  endif()

endmacro()


# Set an individual package test or examples enable to on only if global
# enable var is on
#
macro(tribits_set_package_enable_based_on_project_enable_on  projectEnableVar
    packageEnableVar
  )
  if (("${${packageEnableVar}}" STREQUAL "") AND ${projectEnableVar})
    message("-- " "Setting ${packageEnableVar}=ON")
    set(${packageEnableVar} ON)
  endif()
endmacro()


# Macro used to set ${TRIBITS_PACKAGE)_ENABLE_TESTS and ${TRIBITS_PACKAGE)_ENABLE_EXAMPLES
# based on ${PROJECT_NAME}_ENABLE_TESTS and ${PROJECT_NAME}_ENABLE_EXAMPLES 
#
macro(tribits_apply_test_example_enables  packageName)
  if (${PROJECT_NAME}_ENABLE_${packageName})
    tribits_is_primary_meta_project_package(${packageName}  packageIsPmmp)
    if (packageIsPmmp)
      tribits_set_package_enable_based_on_project_enable_on(
        ${PROJECT_NAME}_ENABLE_TESTS  ${packageName}_ENABLE_TESTS )
      tribits_set_package_enable_based_on_project_enable_on(
        ${PROJECT_NAME}_ENABLE_EXAMPLES  ${packageName}_ENABLE_EXAMPLES )
    endif()
  endif()
endmacro()


# Macro to disable ${parentPackageName)_ENABLE_ENABLES by default if
# ${parentPackageName)_ENABLE_TESTS is explicitly disabled.
#
macro(tribits_apply_package_examples_disable  parentPackageName)
  if ( (NOT ${parentPackageName}_ENABLE_TESTS)
      AND (NOT "${${parentPackageName}_ENABLE_TESTS}" STREQUAL "")
      AND ("${${parentPackageName}_ENABLE_EXAMPLES}" STREQUAL "")
    )
    message("-- " "Setting"
      " ${parentPackageName}_ENABLE_EXAMPLES"
      "=${${parentPackageName}_ENABLE_TESTS}"
      " because"
      " ${parentPackageName}_ENABLE_TESTS"
      "=${${parentPackageName}_ENABLE_TESTS}" )
     set(${parentPackageName}_ENABLE_EXAMPLES ${${parentPackageName}_ENABLE_TESTS})
  endif()
endmacro()
# NOTE: Above, the top-level package ${parentPackageName} may not even be
# enabled yet when this gets called but its subpackages might and we need to
# process this default disable in case their are any enabled subpackages.


# Macro to disable ${TRIBITS_SUBPACKAGE)_ENABLE_TESTS and
# ${TRIBITS_SUBPACKAGE)_ENABLE_EXAMPLES based on
# ${TRIBITS_PARENTPACKAGE)_ENABLE_TESTS or
# ${TRIBITS_PARENTPACKAGE)_ENABLE_EXAMPLES
#
macro(tribits_apply_subpackage_tests_or_examples_disables  parentPackageName
    testsOrExamples
  )
  set(parentPkgEnableVar ${parentPackageName}_ENABLE_${testsOrExamples})
  if ((NOT ${parentPkgEnableVar}) AND (NOT "${${parentPkgEnableVar}}" STREQUAL ""))
    foreach(subpkgName  IN LISTS  ${parentPackageName}_SUBPACKAGES)
      set(fullSpkgName ${parentPackageName}${subpkgName})
      if (${PROJECT_NAME}_ENABLE_${fullSpkgName})
        if ("${${fullSpkgName}_ENABLE_${testsOrExamples}}" STREQUAL "")
          message("-- " "Setting"
            " ${fullSpkgName}_ENABLE_${testsOrExamples}=${${parentPkgEnableVar}}"
            " because parent package"
            " ${parentPkgEnableVar}=${${parentPkgEnableVar}}")
          set(${fullSpkgName}_ENABLE_${testsOrExamples} ${${parentPkgEnableVar}})
        endif()
      endif()
    endforeach()
  endif()
endmacro()


# Macro to enable subpackage tests and examples based on parent package tests
# and examples enables
#
macro(tribits_apply_subpackage_tests_examples_enables  parentPackageName)
  # Set default for ${parentPackageName}_ENABLE_EXAMPLES=OFF if tests disabled
  if ( ("${${parentPackageName}_ENABLE_EXAMPLES}" STREQUAL "")
      AND ${parentPackageName}_ENABLE_TESTS
    )
    message("-- " "Setting"
      " ${parentPackageName}_ENABLE_EXAMPLES=${${parentPackageName}_ENABLE_TESTS}"
      " because"
      " ${parentPackageName}_ENABLE_TESTS=${${parentPackageName}_ENABLE_TESTS}")
    set(${parentPackageName}_ENABLE_EXAMPLES ${${parentPackageName}_ENABLE_TESTS})
  endif()
  # Set defaults for <fullSubpackageName>_ENABLE_[TESTS|EXAMPLES]
  set(parentEnableExamples ${${parentPackageName}_ENABLE_EXAMPLES})
  set(parentEnableTests ${${parentPackageName}_ENABLE_TESTS})
  foreach(subpkgName  IN LISTS  ${parentPackageName}_SUBPACKAGES)
    set(fullSpkgName ${parentPackageName}${subpkgName})
    if (${PROJECT_NAME}_ENABLE_${fullSpkgName})
      if (parentEnableTests AND ("${${fullSpkgName}_ENABLE_TESTS}" STREQUAL ""))
        message("-- " "Setting"
          " ${fullSpkgName}_ENABLE_TESTS=${parentEnableTests}"
          " because parent package"
          " ${parentPackageName}_ENABLE_TESTS=${parentEnableTests}")
        set(${fullSpkgName}_ENABLE_TESTS ${parentEnableTests})
      endif()
      if (parentEnableExamples AND ("${${fullSpkgName}_ENABLE_EXAMPLES}" STREQUAL ""))
        message("-- " "Setting"
          " ${fullSpkgName}_ENABLE_EXAMPLES=${parentEnableExamples}"
          " because parent package"
          " ${parentPackageName}_ENABLE_EXAMPLES=${parentEnableExamples}")
        set(${fullSpkgName}_ENABLE_EXAMPLES ${parentEnableExamples})
      endif()
    endif()
  endforeach()
endmacro()
# NOTE: Above, the parent package may not actually be enabled yet
# (i.e. ${PROJECT_NAME}_ENABLE_${parentPackageName} my not be TRUE) if only
# subpackages needed to be enabled in the forward sweep but we want the tests
# and examples for a subpackage to be enabled if the tests and examples for
# the parent package, respectfully, are enabled.


macro(tribits_private_enable_forward_package  fwdDepPkgName  packageName)
  tribits_implicit_package_enable_is_allowed( "" ${fwdDepPkgName} allowFwdDepPkgEnable)
  if ("${${PROJECT_NAME}_ENABLE_${fwdDepPkgName}}" STREQUAL "" AND allowFwdDepPkgEnable)
    message("-- " "Setting ${PROJECT_NAME}_ENABLE_${fwdDepPkgName}=ON"
      " because ${PROJECT_NAME}_ENABLE_${packageName}=ON")
    set(${PROJECT_NAME}_ENABLE_${fwdDepPkgName}  ON)
  endif()
endmacro()


macro(tribits_private_enable_dep_package  packageName  depPkgName  libOrTest)
  if (${PROJECT_NAME}_ENABLE_${depPkgName})
    #message("The package is already enabled so there is nothing to enable!")
  elseif (${PROJECT_NAME}_ENABLE_${depPkgName}  STREQUAL  "")
    set(tpedp_enableDepPkg "")
    if (${packageName}_${libOrTest}_DEP_REQUIRED_${depPkgName})
      message("-- " "Setting ${PROJECT_NAME}_ENABLE_${depPkgName}=ON"
        " because ${packageName} has a required dependence on ${depPkgName}")
      set(tpedp_enableDepPkg  ON)
    elseif (${packageName}_ENABLE_${depPkgName})
      # Enable the upstream package if the user directly specified the
      # optional package enable regardless if it is PT or ST or even EX.
      message("-- " "Setting ${PROJECT_NAME}_ENABLE_${depPkgName}=ON"
        " because ${packageName}_ENABLE_${depPkgName}=ON")
      set(tpedp_enableDepPkg  ON)
    elseif (${PROJECT_NAME}_ENABLE_ALL_OPTIONAL_PACKAGES)
      # Enable the package if there is an optional dependence and we are asked
      # to enabled optional dependencies.
      tribits_implicit_package_enable_is_allowed(${packageName}  ${depPkgName}
        allowImplicitEnable)
      if (allowImplicitEnable)
        message("-- " "Setting ${PROJECT_NAME}_ENABLE_${depPkgName}=ON"
          " because ${packageName} has an optional dependence on ${depPkgName}")
        set(tpedp_enableDepPkg  ON)
      endif()
    endif()
    # Enable the upstream package
    if (tpedp_enableDepPkg)
      set(${PROJECT_NAME}_ENABLE_${depPkgName}  ON)
    endif()
  endif()
endmacro()


macro(tribits_private_enable_dep_tpl  PACKAGE_NAME  DEP_TPL_NAME)
  assert_defined(TPL_ENABLE_${DEP_TPL_NAME})
  if(TPL_ENABLE_${DEP_TPL_NAME} STREQUAL "")
    message("-- " "Setting TPL_ENABLE_${DEP_TPL_NAME}=ON because"
      " it is required by the enabled package ${PACKAGE_NAME}")
    assert_defined(TPL_ENABLE_${DEP_TPL_NAME})
    set(TPL_ENABLE_${DEP_TPL_NAME} ON)
    set(TPL_${DEP_TPL_NAME}_ENABLING_PKG  ${PACKAGE_NAME})
  endif()
endmacro()


macro(tribits_private_enable_optional_dep_tpl PACKAGE_NAME DEP_TPL_NAME)
  #assert_defined(${PACKAGE_NAME}_ENABLE_${DEP_TPL_NAME})
  if (${PROJECT_NAME}_ENABLE_${PACKAGE_NAME}
    AND ${PACKAGE_NAME}_ENABLE_${DEP_TPL_NAME}
    AND TPL_ENABLE_${DEP_TPL_NAME} STREQUAL ""
    )
    message("-- " "Setting TPL_ENABLE_${DEP_TPL_NAME}=ON because"
      " ${PACKAGE_NAME}_ENABLE_${DEP_TPL_NAME}=ON")
    assert_defined(TPL_ENABLE_${DEP_TPL_NAME})
    set(TPL_ENABLE_${DEP_TPL_NAME} ON)
  endif()
endmacro()


# Macro that enables upstream (required and optional) packages for a given
# package
#
macro(tribits_enable_upstream_packages  packageName)

  if (${PROJECT_NAME}_ENABLE_${packageName})

    foreach(depPkg  IN LISTS  ${packageName}_LIB_DEFINED_DEPENDENCIES)
      tribits_private_enable_dep_package(${packageName}  ${depPkg}  LIB)
    endforeach()

    foreach(depPkg  IN LISTS  ${packageName}_TEST_DEFINED_DEPENDENCIES)
      tribits_private_enable_dep_package(${packageName}  ${depPkg}  TEST)
    endforeach()

  endif()

endmacro()
# NOTE: The above macro has a defect.  It is enabling upstream test dependent
# packages even if tests nor examples are not enabled (see
# TriBITSPub/TriBITS#56).  But fixing this will break backward compatibility
# and therefore require upgrading the packages that currently only work
# correctly because of this defect.


# LocalWords: tribits TriBITS foreach endmacro endfunction
