tribits_add_test(package3-prg  NOEXEPREFIX  NOEXESUFFIX
  NAME Prg
  DIRECTORY ${PACKAGE_BINARY_DIR}/src
  NUM_MPI_PROCS 1
  PASS_REGULAR_EXPRESSION "Package3 Deps: Package2{Package1{tpl1}, Tpl3{Tpl2a{tpl1}, Tpl2b{no deps}}}, Package1{tpl1}, Tpl4{Tpl3{Tpl2a{tpl1}, Tpl2b{no deps}}, Tpl2a{tpl1}, Tpl2b{no deps}}, Tpl3{Tpl2a{tpl1}, Tpl2b{no deps}}"
  )
