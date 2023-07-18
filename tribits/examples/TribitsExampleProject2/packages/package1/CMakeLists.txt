cmake_minimum_required(VERSION 3.23.0 FATAL_ERROR)

macro(include_raw_cmake_build)
  if ((NOT COMMAND tribits_project) OR Package1_USE_RAW_CMAKE)
    include("${CMAKE_CURRENT_SOURCE_DIR}/CMakeLists.raw.cmake"
       NO_POLICY_SCOPE)
    return()
  endif()
endmacro()

if ((COMMAND tribits_package) AND (NOT Package1_USE_RAW_CMAKE))

  message("Configuring package Package1 as full TriBITS package")
  tribits_package(Package1)
  add_subdirectory(src)
  tribits_add_test_directories(test)
  tribits_package_postprocess()

else()

  if (COMMAND tribits_package)
    message("Configuring raw CMake package Package1")
  else()
    message("Configuring raw CMake project Package1")
  endif()
  project(Package1 LANGUAGES C CXX)
  include(GNUInstallDirs)
  find_package(Tpl1 CONFIG REQUIRED)
  add_subdirectory(src)
  if (Package1_ENABLE_TESTS)
    include(CTest)
    add_subdirectory(test)
  endif()

  # Generate the all_libs target(s)
  add_library(Package1_all_libs INTERFACE)
  set_target_properties(Package1_all_libs PROPERTIES
    EXPORT_NAME all_libs)
  target_link_libraries(Package1_all_libs INTERFACE Package1_package1)
  install(TARGETS Package1_all_libs
    EXPORT ${PROJECT_NAME}
    COMPONENT ${PROJECT_NAME}
    INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR} )
  add_library(Package1::all_libs ALIAS Package1_all_libs)

  # Generate Package1Config.cmake file for the build tree
  set(packageBuildDirCMakePackagesDir
    "${${CMAKE_PROJECT_NAME}_BINARY_DIR}/cmake_packages/${PROJECT_NAME}")
  export(EXPORT ${PROJECT_NAME}
    NAMESPACE ${PROJECT_NAME}::
    FILE "${packageBuildDirCMakePackagesDir}/${PROJECT_NAME}ConfigTargets.cmake" )
  configure_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/cmake/raw/Package1Config.cmake.in"
    "${packageBuildDirCMakePackagesDir}/${PROJECT_NAME}/Package1Config.cmake"
    @ONLY )

  # Generate and install the Package1Config.cmake file for the install tree
  if (COMMAND tribits_package)
    set(pkgConfigInstallDir
      "${${CMAKE_PROJECT_NAME}_INSTALL_LIB_DIR}/cmake/${PACKAGE_NAME}")
  else()
    set(pkgConfigInstallDir "${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}")
  endif()
  install(EXPORT ${PROJECT_NAME}
    DESTINATION "${pkgConfigInstallDir}"
    NAMESPACE ${PROJECT_NAME}::
    FILE ${PROJECT_NAME}ConfigTargets.cmake )
  configure_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/cmake/raw/Package1Config.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/CMakeFiles/Package1Config.install.cmake"
    @ONLY )
  install(
    FILES "${CMAKE_CURRENT_BINARY_DIR}/CMakeFiles/Package1Config.install.cmake"
    RENAME "Package1Config.cmake"
    DESTINATION "${pkgConfigInstallDir}" )

endif()


# NOTE: Above, the variable CMAKE_INSTALL_LIBDIR set by
# include(GNUInstallDirs) is different that what is used by TriBITS by default
# in at least some cases.  That is very irritating and this is something that
# needs to be fixed (see TriBITSPub/TriBITS#411).  But note that the location
# of the libraries does not have to be the same as the installed
# `<Package>Config.cmake`.