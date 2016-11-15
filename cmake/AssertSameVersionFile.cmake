# Make sure the base Version.cmake file is the same as the copy in
# tribits/Version.cmake We can't use a symlink because this breaks TriBITS on
# Windows (See TriBITSPub/TriBITS#129).  Later, this will be replaced with a
# configured Version.cmake file so this will not be an issue.
SET(BASE_VERSION_CMAKE_FILE "${CMAKE_CURRENT_SOURCE_DIR}/Version.cmake")
SET(TRIBITS_VERSION_CMAKE_FILE "${CMAKE_CURRENT_SOURCE_DIR}/tribits/Version.cmake")
FILE(READ "${BASE_VERSION_CMAKE_FILE}" BASE_VERSION_CMAKE_STR)
FILE(READ "${TRIBITS_VERSION_CMAKE_FILE}" TRIBITS_VERSION_CMAKE_STR)
IF (NOT BASE_VERSION_CMAKE_STR STREQUAL TRIBITS_VERSION_CMAKE_STR)
  MESSAGE(FATAL_ERROR
    "ERROR: '${BASE_VERSION_CMAKE_FILE}' and '${TRIBITS_VERSION_CMAKE_FILE}' are"
    " different (see TriBITSPub/TriBITS#129)!")
ENDIF()
