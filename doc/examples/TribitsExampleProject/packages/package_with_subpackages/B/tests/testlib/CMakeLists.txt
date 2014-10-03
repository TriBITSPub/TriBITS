ASSERT_DEFINED(${PACKAGE_NAME}_ENABLE_MixedLanguage)
IF (${PACKAGE_NAME}_ENABLE_MixedLanguage)

  # This is a test only library that can be reused anywhere
  
  INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR})
  
  TRIBITS_ADD_LIBRARY( b_mixed_lang
     TESTONLY
     HEADERS b_mixed_lang.hpp
     SOURCES b_mixed_lang.cpp
     )

ENDIF()
