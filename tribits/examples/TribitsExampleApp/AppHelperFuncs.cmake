# Find TribitsExProj package(s), load compilers and compiler options, and get
# libs and include dirs to link against.
#
macro(getTribitsExProjStuff)

  set(${PROJECT_NAME}_FIND_INDIVIDUAL_PACKAGES OFF CACHE BOOL
    "Set to TRUE to find individual packages and OFF to find project TribitsExProj")

  if (${PROJECT_NAME}_FIND_INDIVIDUAL_PACKAGES)
    message(FATAL_ERROR "ToDo: Implement!")
  else()
    getTribitsExProjProjectStuff()
  endif()

endmacro()


# Get TribitsExProj stuff from find_package(TribitsExProj)
#
macro(getTribitsExProjProjectStuff)

  find_package(TribitsExProj REQUIRED COMPONENTS ${${PROJECT_NAME}_USE_COMPONENTS})

  MESSAGE("\nFound TribitsExProj!  Here are the details: ")
  MESSAGE("   TribitsExProj_DIR = ${TribitsExProj_DIR}")
  MESSAGE("   TribitsExProj_VERSION = ${TribitsExProj_VERSION}")
  MESSAGE("   TribitsExProj_PACKAGE_LIST = ${TribitsExProj_PACKAGE_LIST}")
  MESSAGE("   TribitsExProj_LIBRARIES = ${TribitsExProj_LIBRARIES}")
  MESSAGE("   TribitsExProj_INCLUDE_DIRS = ${TribitsExProj_INCLUDE_DIRS}")
  MESSAGE("   TribitsExProj_LIBRARY_DIRS = ${TribitsExProj_LIBRARY_DIRS}")
  MESSAGE("   TribitsExProj_TPL_LIST = ${TribitsExProj_TPL_LIST}")
  MESSAGE("   TribitsExProj_TPL_INCLUDE_DIRS = ${TribitsExProj_TPL_INCLUDE_DIRS}")
  MESSAGE("   TribitsExProj_TPL_LIBRARIES = ${TribitsExProj_TPL_LIBRARIES}")
  MESSAGE("   TribitsExProj_TPL_LIBRARY_DIRS = ${TribitsExProj_TPL_LIBRARY_DIRS}")
  MESSAGE("   TribitsExProj_BUILD_SHARED_LIBS = ${TribitsExProj_BUILD_SHARED_LIBS}")
  MESSAGE("End of TribitsExProj details\n")

  # Make sure to use same compilers and flags as TribitsExProj
  set(CMAKE_CXX_COMPILER ${TribitsExProj_CXX_COMPILER} )
  set(CMAKE_C_COMPILER ${TribitsExProj_C_COMPILER} )
  set(CMAKE_Fortran_COMPILER ${TribitsExProj_Fortran_COMPILER} )

  set(CMAKE_CXX_FLAGS "${TribitsExProj_CXX_COMPILER_FLAGS} ${CMAKE_CXX_FLAGS}")
  set(CMAKE_C_FLAGS "${TribitsExProj_C_COMPILER_FLAGS} ${CMAKE_C_FLAGS}")
  set(CMAKE_Fortran_FLAGS "${TribitsExProj_Fortran_COMPILER_FLAGS} ${CMAKE_Fortran_FLAGS}")

  # Get the include directories and libraries for building and linking
  set(APP_DEPS_INCLUDE_DIRS
    ${TribitsExProj_INCLUDE_DIRS} ${TribitsExProj_TPL_INCLUDE_DIRS})
  set(APP_DEPS_LIBRARIES
    ${TribitsExProj_LIBRARIES} ${TribitsExProj_TPL_LIBRARIES})

endmacro()


function(addAppDepCompileDefines)
  addAppDepCompileDefine("SimpleCxx")
  addAppDepCompileDefine("MixedLang")
  addAppDepCompileDefine("WithSubpackages")
endfunction()


function(addAppDepCompileDefine componentName)
  if (${componentName} IN_LIST ${PROJECT_NAME}_USE_COMPONENTS)
    string(TOUPPER "${componentName}" componentNameUpper)
    target_compile_definitions(app PRIVATE TRIBITSEXAPP_HAVE_${componentNameUpper})
  endif()
endfunction()


function(appendTestDepsStr componentName depsStrOut str)
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
