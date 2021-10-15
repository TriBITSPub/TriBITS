# Find TribitsExProj package(s), load compilers and compiler options, and get
# CMake lib targets (which have include dirs also) to link against.
#
macro(getTribitsExProjStuff)

  set(${PROJECT_NAME}_FIND_INDIVIDUAL_PACKAGES OFF CACHE BOOL
    "Set to TRUE to find individual packages and OFF to find project TribitsExProj")

  set(${PROJECT_NAME}_FIND_UNDER_BUILD_DIR "" CACHE STRING
    "Find <Package>Config.cmake files under this build dir instead of under install dir")
  get_filename_component(${PROJECT_NAME}_FIND_UNDER_BUILD_DIR
    "${${PROJECT_NAME}_FIND_UNDER_BUILD_DIR}" ABSOLUTE)

  if (${PROJECT_NAME}_FIND_INDIVIDUAL_PACKAGES)
    if (${PROJECT_NAME}_FIND_UNDER_BUILD_DIR)
      getTribitsExProjStuffByPackageUnderBuildDir()
    else()
      getTribitsExProjStuffByPackage()
    endif()
  else()
    getTribitsExProjStuffByProject()
  endif()

endmacro()


# Get TribitsExProj stuff with find_package(<Package>) for each
# package/component from a build dir.
#
macro(getTribitsExProjStuffByPackageUnderBuildDir)

  list(PREPEND CMAKE_PREFIX_PATH
    "${${PROJECT_NAME}_FIND_UNDER_BUILD_DIR}/cmake_packages")

  getTribitsExProjStuffByPackage()

endmacro()
# NOTE: Above, having to get all of the package build dirs for each package is
# pretty ridiculous and not very scalable but that is what you have to do
# currently.


# Get TribitsExProj stuff with find_package(<Package>) for each
# package/component.
#
# NOTE: This expects that CMAKE_PREFIX_PATH is already set up to find the
# <Package>Config.cmake files correctly.
#
macro(getTribitsExProjStuffByPackage)

  # Find each package and gather up all the <Package>::all_libs targets.
  set(APP_DEPS_PACKAGE_LIB_TARGETS "")
  foreach (packageName IN LISTS ${PROJECT_NAME}_USE_COMPONENTS)
    find_package(${packageName} REQUIRED)
    message("Found ${packageName}!")
    list(APPEND APP_DEPS_PACKAGE_LIB_TARGETS ${packageName}::all_libs)
  endforeach()

  # Get the full list libs
  set(APP_DEPS_LIB_TARGETS ${APP_DEPS_PACKAGE_LIB_TARGETS})
  print_var(APP_DEPS_LIB_TARGETS)

  # Set TribitsExProj_SELECTED_PACKAGE_LIST
  set(TribitsExProj_SELECTED_PACKAGE_LIST ${${PROJECT_NAME}_USE_COMPONENTS})

endmacro()


# Get TribitsExProj stuff from find_package(TribitsExProj)
#
macro(getTribitsExProjStuffByProject)

  find_package(TribitsExProj REQUIRED COMPONENTS ${${PROJECT_NAME}_USE_COMPONENTS})

  message("\nFound TribitsExProj!  Here are the details: ")
  message("   TribitsExProj_DIR = ${TribitsExProj_DIR}")
  message("   TribitsExProj_VERSION = ${TribitsExProj_VERSION}")
  message("   TribitsExProj_PACKAGE_LIST = ${TribitsExProj_PACKAGE_LIST}")
  message("   TribitsExProj_TPL_LIST = ${TribitsExProj_TPL_LIST}")
  message("   TribitsExProj_BUILD_SHARED_LIBS = ${TribitsExProj_BUILD_SHARED_LIBS}")
  message("End of TribitsExProj details\n")

  # Make sure to use same compilers and flags as TribitsExProj
  set(CMAKE_CXX_COMPILER ${TribitsExProj_CXX_COMPILER} )
  set(CMAKE_C_COMPILER ${TribitsExProj_C_COMPILER} )
  set(CMAKE_Fortran_COMPILER ${TribitsExProj_Fortran_COMPILER} )

  set(CMAKE_CXX_FLAGS "${TribitsExProj_CXX_COMPILER_FLAGS} ${CMAKE_CXX_FLAGS}")
  set(CMAKE_C_FLAGS "${TribitsExProj_C_COMPILER_FLAGS} ${CMAKE_C_FLAGS}")
  set(CMAKE_Fortran_FLAGS "${TribitsExProj_Fortran_COMPILER_FLAGS} ${CMAKE_Fortran_FLAGS}")

  # Get the libraries for building and linking
  if (${PROJECT_NAME}_USE_COMPONENTS)
    set(APP_DEPS_LIB_TARGETS TribitsExProj::all_selected_libs)
  else()
    set(APP_DEPS_LIB_TARGETS TribitsExProj::all_libs)
  endif()

endmacro()


function(addAppDepCompileDefines)
  addAppDepCompileDefine("SimpleCxx")
  addAppDepCompileDefine("MixedLang")
  addAppDepCompileDefine("WithSubpackages")
endfunction()


function(addAppDepCompileDefine componentName)
  if (${componentName} IN_LIST TribitsExProj_SELECTED_PACKAGE_LIST)
    string(TOUPPER "${componentName}" componentNameUpper)
    target_compile_definitions(app PRIVATE TRIBITSEXAPP_HAVE_${componentNameUpper})
  endif()
endfunction()


function(appendTestDepsStr componentName depsStrOut str)
  set(depsStr "${${depsStrOut}}")  # Should be value of var in parent scope!
  #message("-- depsStr (inner) = '${depsStr}'")
  if (${componentName} IN_LIST TribitsExProj_SELECTED_PACKAGE_LIST)
    if (depsStr)
      set(depsStr "${depsStr}[;] ${str}")
    else()
      set(depsStr "${str}")
    endif()
  endif()
  set(${depsStrOut} "${depsStr}" PARENT_SCOPE)
endfunction()


function(print_var varName)
  message("-- ${varName} = '${${varName}}'")
endfunction()
