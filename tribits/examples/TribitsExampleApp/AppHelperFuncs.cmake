# Find TribitsExProj package(s), load compilers and compiler options, and get
# libs and include dirs to link against.
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

  # Get the list of all of package build dirs that have <Package>Config.cmake
  # files in the build tree.
  file(GLOB_RECURSE allPackageConfigFiles
    "${${PROJECT_NAME}_FIND_UNDER_BUILD_DIR}/packages/*Config.cmake")
  #print_var(allPackageConfigFiles)
  set(allPackageBuildDirs "")
  foreach (packageConfigFile IN LISTS allPackageConfigFiles)
    get_filename_component(packageBuildDir "${packageConfigFile}" DIRECTORY)
    list(APPEND allPackageBuildDirs "${packageBuildDir}")
  endforeach()
  #print_var(allPackageBuildDirs)
  list(PREPEND CMAKE_PREFIX_PATH "${allPackageBuildDirs}")

  # Now find those <Package>Config.cmake files and process them just like they
  # were in the install tree.
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

  # Find each package and gather up all the include dirs and libs for each
  # package and their TPLs and preserve the order.
  set(APP_DEPS_PACKAGE_INCLUDE_DIRS "")
  set(APP_DEPS_TPL_INCLUDE_DIRS "")
  set(APP_DEPS_PACKAGE_LIBRARIES "")
  foreach (packageName IN LISTS ${PROJECT_NAME}_USE_COMPONENTS)
    find_package(${packageName} REQUIRED)
    message("Found ${packageName}!")
    list(APPEND APP_DEPS_PACKAGE_INCLUDE_DIRS ${${packageName}_INCLUDE_DIRS})
    list(APPEND APP_DEPS_TPL_INCLUDE_DIRS ${${packageName}_TPL_INCLUDE_DIRS})
    list(APPEND APP_DEPS_PACKAGE_LIBRARIES ${${packageName}_LIBRARIES})
  endforeach()

  # Get the full list of include dirs and libs
  set(APP_DEPS_INCLUDE_DIRS
    ${APP_DEPS_PACKAGE_INCLUDE_DIRS} ${APP_DEPS_TPL_INCLUDE_DIRS})
  set(APP_DEPS_LIBRARIES ${APP_DEPS_PACKAGE_LIBRARIES})

  # Remove duplicates
  list(REVERSE APP_DEPS_INCLUDE_DIRS)
  list(REMOVE_DUPLICATES APP_DEPS_INCLUDE_DIRS)
  list(REVERSE APP_DEPS_INCLUDE_DIRS)
  print_var(APP_DEPS_INCLUDE_DIRS)
  list(REVERSE APP_DEPS_LIBRARIES)
  list(REMOVE_DUPLICATES APP_DEPS_LIBRARIES)
  list(REVERSE APP_DEPS_LIBRARIES)
  print_var(APP_DEPS_LIBRARIES)

endmacro()


# Get TribitsExProj stuff from find_package(TribitsExProj)
#
macro(getTribitsExProjStuffByProject)

  find_package(TribitsExProj REQUIRED COMPONENTS ${${PROJECT_NAME}_USE_COMPONENTS})

  message("\nFound TribitsExProj!  Here are the details: ")
  message("   TribitsExProj_DIR = ${TribitsExProj_DIR}")
  message("   TribitsExProj_VERSION = ${TribitsExProj_VERSION}")
  message("   TribitsExProj_PACKAGE_LIST = ${TribitsExProj_PACKAGE_LIST}")
  message("   TribitsExProj_LIBRARIES = ${TribitsExProj_LIBRARIES}")
  message("   TribitsExProj_INCLUDE_DIRS = ${TribitsExProj_INCLUDE_DIRS}")
  message("   TribitsExProj_LIBRARY_DIRS = ${TribitsExProj_LIBRARY_DIRS}")
  message("   TribitsExProj_TPL_LIST = ${TribitsExProj_TPL_LIST}")
  message("   TribitsExProj_TPL_INCLUDE_DIRS = ${TribitsExProj_TPL_INCLUDE_DIRS}")
  message("   TribitsExProj_TPL_LIBRARIES = ${TribitsExProj_TPL_LIBRARIES}")
  message("   TribitsExProj_TPL_LIBRARY_DIRS = ${TribitsExProj_TPL_LIBRARY_DIRS}")
  message("   TribitsExProj_BUILD_SHARED_LIBS = ${TribitsExProj_BUILD_SHARED_LIBS}")
  message("End of TribitsExProj details\n")

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
  set(APP_DEPS_LIBRARIES ${TribitsExProj_LIBRARIES})

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


function(print_var varName)
  message("-- ${varName} = '${${varName}}'")
endfunction()
