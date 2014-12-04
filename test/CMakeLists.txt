ADD_SUBDIRECTORY(core)

IF (PYTHON_EXECUTABLE)
  ADD_SUBDIRECTORIES(
    python_utils
    ci_support
    ctest_driver
    devtools_install
    )
ENDIF()
