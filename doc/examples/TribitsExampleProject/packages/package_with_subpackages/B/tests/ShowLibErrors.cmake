# Define these vars (one at a time) in your input cach to see invalid usage
# checking and the errors and warnings printed!
IF (SPKB_SHOW_TESTONLY_INSTALLABLE_ERROR)
  SET(TAEAT_EXTRALIB_ARGS INSTALLABLE)
ELSEIF (SPKB_SHOW_NON_TESTONLY_LIB_ERROR)
  SET(TAEAT_EXTRALIB_ARGS simplecxx)
ELSEIF (SPKB_SHOW_IMPORTED_LIBS_THIS_PKG_ERROR)
  SET(TAEAT_EXTRALIB_ARGS IMPORTEDLIBS pws_b)
ELSEIF (SPKB_SHOW_TESTONLY_DEBLIBS_WARNING) # Deprecated
  SET(TAEAT_EXTRALIB_ARGS  DEPLIBS b_mixed_lang)
ELSEIF (SPKB_SHOW_NONTESTONLY_DEBLIBS_WARNING) # Deprecated
  SET(TAEAT_EXTRALIB_ARGS  DEPLIBS pws_b)
ENDIF()
PRINT_NONEMPTY_VAR(TAEAT_EXTRALIB_ARGS)

