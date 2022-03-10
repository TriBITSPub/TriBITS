tribits_add_test(package2-prg  NOEXEPREFIX  NOEXESUFFIX
  NAME Prg
  DIRECTORY ${PACKAGE_BINARY_DIR}/src
  NUM_MPI_PROCS 1
  PASS_REGULAR_EXPRESSION "Package2 Deps: Package1{tpl1}, Tpl3{Tpl2a{tpl1}, Tpl2b{no deps}}"
  )
