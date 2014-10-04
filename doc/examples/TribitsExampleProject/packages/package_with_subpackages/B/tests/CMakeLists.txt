# Create a test-only lib
ADD_SUBDIRECTORY(testlib)

# Create a test executable
TRIBITS_ADD_EXECUTABLE( b_test SOURCES b_test.cpp )

#
# Test b_test
#

SET(EXPECTED_B_DEPS)
ASSERT_DEFINED(${PACKAGE_NAME}_ENABLE_PackageWithSubpackagesSubpackageA)
IF(${PACKAGE_NAME}_ENABLE_PackageWithSubpackagesSubpackageA)
  SET(EXPECTED_B_DEPS "${EXPECTED_B_DEPS} A no_deps")
ENDIF()
SET(EXPECTED_B_DEPS "${EXPECTED_B_DEPS} no_deps")

TRIBITS_ADD_ADVANCED_TEST( test_of_b
  OVERALL_NUM_MPI_PROCS 1
  TEST_0 EXEC b_test
    PASS_REGULAR_EXPRESSION_ALL 
      "B label is: B"
      "B deps are:${EXPECTED_B_DEPS}"
  )

#
# Define an test involving the optional dependent MixedLang package
# 

ASSERT_DEFINED(${PACKAGE_NAME}_ENABLE_MixedLanguage)
IF (${PACKAGE_NAME}_ENABLE_MixedLanguage)

  # Define these vars (one at a time) in your input cach to see invalid usage
  # checking and the errors and warnings printed!
  IF (SPKB_SHOW_TESTONLY_INSTALLABLE_ERROR)
    SET(TAEAT_EXTRALIB_ARGS INSTALLABLE)
  ENDIF()
  IF (SPKB_SHOW_NON_TESTONLY_LIB_ERROR)
    SET(TAEAT_EXTRALIB_ARGS simplecxx)
  ENDIF()
  IF (SPKB_SHOW_IMPORTED_LIBS_THIS_PKG_ERROR)
    SET(TAEAT_EXTRALIB_ARGS IMPORTEDLIBS pws_b)
  ENDIF()
  IF (SPKB_SHOW_TESTONLY_DEBLIBS_WARNING) # Deprecated
    SET(TAEAT_EXTRALIB_ARGS  DEPLIBS b_mixed_lang)
  ENDIF()
  IF (SPKB_SHOW_NONTESTONLY_DEBLIBS_WARNING) # Deprecated
    SET(TAEAT_EXTRALIB_ARGS  DEPLIBS pws_b)
  ENDIF()
  PRINT_VAR(TAEAT_EXTRALIB_ARGS)

  TRIBITS_ADD_EXECUTABLE_AND_TEST( test_of_b_mixed_lang
    SOURCES b_mixed_lang_test.cpp
    NUM_MPI_PROCS 1
    PASS_REGULAR_EXPRESSION 
      "B Mixed Language"
    TESTONLYLIBS b_mixed_lang
    ${TAEAT_EXTRALIB_ARGS} # Used for testing and to demonstrate errors
    )

ENDIF()
