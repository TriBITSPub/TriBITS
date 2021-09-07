function(addDepCompileDefine componentName)
  if (${componentName} IN_LIST ${PROJECT_NAME}_USE_COMPONENTS)
    string(TOUPPER "${componentName}" componentNameUpper)
    target_compile_definitions(app PRIVATE TRIBITSEXAPP_HAVE_${componentNameUpper})
  endif()
endfunction()


function(appendDepsStr componentName depsStrOut str)
  set(depsStr "${${depsStrOut}}")  # Should be value of var in parent scope!
  #message("-- depsStr (inner) = '${depsStr}'")
  if (${componentName} IN_LIST ${PROJECT_NAME}_USE_COMPONENTS)
    if (depsStr)
      set(depsStr "${depsStr}[;] ${str}")
    else()
      set(depsStr "${str}")
    endif()
  endif()
  set(${depsStrOut} "${depsStr}" PARENT_SCOPE)
endfunction()


