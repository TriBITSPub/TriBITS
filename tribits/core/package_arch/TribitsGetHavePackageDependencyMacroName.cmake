function(tribits_get_have_package_dependency_macro_name  packageName  upstreamPackageName
    haveDepMacroNameOut
  )
  string(TOUPPER  ${packageName}  packageName_UC)
  string(TOUPPER  ${upstreamPackageName}  upstreamPackageName_UC)
  set(${haveDepMacroNameOut} "HAVE_${packageName_UC}_${upstreamPackageName_UC}"
    PARENT_SCOPE)
endfunction()
