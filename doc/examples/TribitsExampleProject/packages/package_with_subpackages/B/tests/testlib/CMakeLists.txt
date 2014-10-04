ASSERT_DEFINED(${PACKAGE_NAME}_ENABLE_MixedLanguage)
IF (${PACKAGE_NAME}_ENABLE_MixedLanguage)

  # Define these vars to see invalid usage checking and errors!
  IF (SPKB_SHOW_SE_PKG_LIB_IMPORTEDLIBS_ERROR)
    SET(EXTRA_TAL_ARGS IMPORTEDLIBS pws_b)
  ENDIF()
  IF (SPKB_SHOW_UPSTREAM_SE_PKG_LIB_IMPORTEDLIBS_ERROR)
    SET(EXTRA_TAL_ARGS IMPORTEDLIBS simplecxx)
  ENDIF()
  PRINT_NONEMPTY_VAR(EXTRA_TAL_ARGS)

  # Define the include dirs for the TESTONLY lib.
  INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR})
  
  # Define the TESTONLY library
  TRIBITS_ADD_LIBRARY( b_mixed_lang
     TESTONLY
     HEADERS b_mixed_lang.hpp
     SOURCES b_mixed_lang.cpp
     DEPLIBS pws_b
     ${EXTRA_TAL_ARGS}
     )

ENDIF()
