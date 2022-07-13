tribits_repository_define_tpls(
  Tpl1      "cmake/tpls/"      PT
  Tpl2      "cmake/tpls/"      PT
  Tpl3      "cmake/tpls/"      PT
  Tpl4      "cmake/tpls/"      PT
  )

# Temp hack for setting up TPL dependencies
tribits_external_package_define_dependencies(Tpl2  DEPENDENCIES  Tpl1)
tribits_external_package_define_dependencies(Tpl3  DEPENDENCIES  Tpl2)
tribits_external_package_define_dependencies(Tpl4  DEPENDENCIES  Tpl2  Tpl3)
