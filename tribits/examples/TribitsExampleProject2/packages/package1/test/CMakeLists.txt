tribits_add_test(package1-helloworld  NOEXEPREFIX  NOEXESUFFIX
  NAME HelloWorldProg
  DIRECTORY ${PACKAGE_BINARY_DIR}/src
  NUM_MPI_PROCS 1
  PASS_REGULAR_EXPRESSION "Package1 Deps: tpl1"
  )
