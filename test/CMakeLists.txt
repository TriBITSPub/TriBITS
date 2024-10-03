add_subdirectory(core)

if (Python3_EXECUTABLE)
  add_subdirectories(
    python_utils
    ci_support
    ctest_driver
    devtools_install
    doc
    )
endif()

add_subdirectory(codespell)
