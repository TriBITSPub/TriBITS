###############################################################
# test a passing call order, will be run by default turn this 
# off when you turn on one of the other sections
###############################################################
IF (NOT ${PACKAGE_NAME}_TURN_OFF_PASSING_CALL_ORDER)
  
  PRINT_VAR(${PACKAGE_NAME}_SUBPACKAGES)

  #
  # A) Forward declare the package so that certain options are also defined for
  # subpackages
  #
  TRIBITS_PACKAGE_DECL(PkgWithSubpkgsWithUserErrors)

  #
  # B) Define the common options for the package first so they can be used by
  # subpackages as well.
  #
  TRIBITS_ADD_DEBUG_OPTION()

  #
  # C) Process the subpackages
  #
  TRIBITS_PROCESS_SUBPACKAGES()

  #
  # D) Define the package now and perform standard post processing
  #
  TRIBITS_PACKAGE_DEF()
  TRIBITS_PACKAGE_POSTPROCESS()
ENDIF()


###############################################################
# No PACKAGE_DECL before PROCESS_SUBPACKAGES
###############################################################
IF(${PACKAGE_NAME}_no_PACKAGE_DECL_before_PROCESS_SUBPACKAGES)
  MESSAGE( "Unit test ${PACKAGE_NAME}_no_PACKAGE_DECL_before_PROCESS_SUBPACKAGES")
  TRIBITS_PROCESS_SUBPACKAGES()
ENDIF()


###############################################################
# PACKAGE_POSTPROCESS before PROCESS_SUBPACKAGES
###############################################################
IF(${PACKAGE_NAME}_POSTPROCESS_before_SUBPACKAGES)
  MESSAGE( "Unit test ${PACKAGE_NAME}_POSTPROCESS_before_SUBPACKAGES")
  TRIBITS_PACKAGE_DECL(PkgWithSubpkgsWithUserErrors)
  TRIBITS_PACKAGE_DEF()
  TRIBITS_PACKAGE_POSTPROCESS()
  TRIBITS_PROCESS_SUBPACKAGES()
ENDIF()

###############################################################
# PACKAGE_DEF before PROCESS_SUBPACKAGES
###############################################################
IF(${PACKAGE_NAME}_PACKAGE_DEF_before_SUBPACKAGES)
  MESSAGE( "Unit test ${PACKAGE_NAME}_PACKAGE_DEF_before_SUBPACKAGES")
  TRIBITS_PACKAGE_DECL(PkgWithSubpkgsWithUserErrors)
  TRIBITS_PACKAGE_DEF()
  TRIBITS_PROCESS_SUBPACKAGES()
  TRIBITS_PACKAGE_POSTPROCESS()
ENDIF()

###############################################################
# multiple calls to PACKAGE_DECL
###############################################################
IF(${PACKAGE_NAME}_multiple_calls_to_PACKAGE_DECL)
  MESSAGE( "Unit test ${PACKAGE_NAME}_multiple_calls_to_PACKAGE_DECL")
  TRIBITS_PACKAGE_DECL(PkgWithSubpkgsWithUserErrors)
  TRIBITS_PACKAGE_DECL(PkgWithSubpkgsWithUserErrors)
  TRIBITS_ADD_DEBUG_OPTION()
  TRIBITS_PROCESS_SUBPACKAGES()
  TRIBITS_PACKAGE_DEF()
  TRIBITS_PACKAGE_POSTPROCESS()
ENDIF()

###############################################################
# multiple calls to PACKAGE_DEF
###############################################################
IF(${PACKAGE_NAME}_multiple_calls_to_PACKAGE_DEF)
  MESSAGE( "Unit test ${PACKAGE_NAME}_multiple_calls_to_PACKAGE_DEF")
  TRIBITS_PACKAGE_DECL(PkgWithSubpkgsWithUserErrors)
  TRIBITS_ADD_DEBUG_OPTION()
  TRIBITS_PROCESS_SUBPACKAGES()
  TRIBITS_PACKAGE_DEF()
  TRIBITS_PACKAGE_DEF()
  TRIBITS_PACKAGE_POSTPROCESS()
ENDIF()


###############################################################
# call PACKAGE() from package with subpackages
###############################################################
IF(${PACKAGE_NAME}_call_PACKAGE_from_package_with_subpackages)
  MESSAGE( "Unit test ${PACKAGE_NAME}_call_PACKAGE_from_package_with_subpackages")
  TRIBITS_PACKAGE(PkgWithSubpkgsWithUserErrors)
  TRIBITS_PROCESS_SUBPACKAGES()
  TRIBITS_PACKAGE_POSTPROCESS()
ENDIF()


###############################################################
#  Call PACKAGE_DECL without anything else
###############################################################
IF(${PACKAGE_NAME}_call_PACKAGE_DECL_only)
  MESSAGE( "Unit test ${PACKAGE_NAME}_call_PACKAGE_DECL_only")
  TRIBITS_PACKAGE_DECL(PkgWithSubpkgsWithUserErrors)
  TRIBITS_PACKAGE_POSTPROCESS()
ENDIF()


###############################################################
# call SUBPACKAGE() from a package
###############################################################
IF(${PACKAGE_NAME}_call_SUBPACKAGE_from_package_with_subpackages)
  MESSAGE( "Unit test ${PACKAGE_NAME}_call_SUBPACKAGE_from_package_with_subpackages")
  TRIBITS_SUBPACKAGE(PkgWithSubpkgsWithUserErrors)
  TRIBITS_PACKAGE_POSTPROCESS()
ENDIF()


# UNTESTED
###############################################################
# call SUBPACKAGE_POSTPROCESS from a package
###############################################################
IF(${PACKAGE_NAME}_call_SUBPACKAGE_POSTPROCESS)
  MESSAGE( "Unit test ${PACKAGE_NAME}_call_SUBPACKAGE_POSTPROCESS")
  TRIBITS_PACKAGE_DECL(PkgWithSubpkgsWithUserErrors)
  TRIBITS_PROCESS_SUBPACKAGES()
  TRIBITS_PACKAGE_DEF()
  TRIBITS_SUBPACKAGE_POSTPROCESS()
ENDIF()


###############################################################
# Calling PACKAGE after PROCESS_SUBPACKAGES
###############################################################
IF(${PACKAGE_NAME}_call_PACKAGE_after_PROCESS_SUBPACKAGES)
  MESSAGE( "Unit test ${PACKAGE_NAME}_call_PACKAGE_after_PROCESS_SUBPACKAGES")
  TRIBITS_PACKAGE_DECL(PkgWithSubpkgsWithUserErrors)
  TRIBITS_PROCESS_SUBPACKAGES()
  TRIBITS_PACKAGE(PkgWithSubpkgsWithUserErrors)
  TRIBITS_SUBPACKAGE_POSTPROCESS()
ENDIF()


###############################################################
# Not calling PROCESS_SUBPACKAGES when package has subpackages
###############################################################
IF(${PACKAGE_NAME}_call_everthing_except_PROCESS_SUBPACKAGES)
  MESSAGE( "Unit test ${PACKAGE_NAME}_call_everthing_except_PROCESS_SUBPACKAGES")
  TRIBITS_PACKAGE_DECL(PkgWithSubpkgsWithUserErrors)
  TRIBITS_PACKAGE_DEF()
  TRIBITS_PACKAGE_POSTPROCESS()
ENDIF()
