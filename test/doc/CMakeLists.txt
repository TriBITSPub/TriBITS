advanced_set( ${PROJECT_NAME}_ENABLE_DOC_GENERATION_TESTS OFF
  CACHE BOOL
  "Enable testing for the build of the documentation.  Requries docutils and will blow away and rebuild the existing documentation in the source tree since the documentation builds in place." )


tribits_add_advanced_test( build_docs
  EXCLUDE_IF_NOT_TRUE ${PROJECT_NAME}_ENABLE_DOC_GENERATION_TESTS
    GIT_EXECUTABLE
  OVERALL_WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}/tribits/doc
  SKIP_CLEAN_OVERALL_WORKING_DIRECTORY  # Don't delete our source tree!
  OVERALL_NUM_MPI_PROCS 1
  TEST_0 MESSAGE "Clean out any prior build of the docs"
    CMND ${GIT_EXECUTABLE} ARGS clean -xdf
    SKIP_CLEAN_WORKING_DIRECTORY
  TEST_1 MESSAGE "Build the documentation"
    CMND bash ARGS build_docs.sh
    SKIP_CLEAN_WORKING_DIRECTORY
  TEST_2 CMND ls ARGS build_ref/TribitsBuildReference.html
    PASS_REGULAR_EXPRESSION build_ref/TribitsBuildReference.html
    ALWAYS_FAIL_ON_NONZERO_RETURN
  TEST_3 CMND ls ARGS guides/users_guide/TribitsUsersGuide.html
    PASS_REGULAR_EXPRESSION guides/users_guide/TribitsUsersGuide.html
    ALWAYS_FAIL_ON_NONZERO_RETURN
  TEST_4 CMND ls ARGS guides/maintainers_guide/TribitsMaintainersGuide.html
    PASS_REGULAR_EXPRESSION guides/maintainers_guide/TribitsMaintainersGuide.html
    ALWAYS_FAIL_ON_NONZERO_RETURN
  )
