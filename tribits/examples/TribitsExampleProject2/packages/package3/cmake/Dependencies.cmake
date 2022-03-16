tribits_package_define_dependencies(
  LIB_REQUIRED_PACKAGES  Package1
  LIB_OPTIONAL_PACKAGES  Package2
  LIB_REQUIRED_TPLS  Tpl2
    Tpl1  # ToDo: Remove this line once TPL dependencies are implemented! (#299)
  LIB_OPTIONAL_TPLS  Tpl4
    Tpl3  # ToDo: Remove this line once TPL dependencies are implemented! (#299)
  )
