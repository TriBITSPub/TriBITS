include(TribitsGetImportedLocationProperty)

set(REQUIRED_HEADERS Tpl1.hpp)
set(REQUIRED_LIBS_NAMES tpl1)

tribits_tpl_allow_pre_find_package(Tpl1  Tpl1_ALLOW_PREFIND)

if (Tpl1_ALLOW_PREFIND)
  message("-- Using find_package(Tpl1 ...) ...")
  find_package(Tpl1)
  if (Tpl1_FOUND)
    message("-- Found Tpl1_DIR='${Tpl1_DIR}'")
    if (Tpl1_EXTRACT_INFO_AFTER_FIND_PACKAGE)
      message("-- Extracting include dirs and libraries from target tpl1::tpl1")
      get_target_property(inclDirs tpl1::tpl1 INTERFACE_INCLUDE_DIRECTORIES)
      tribits_get_imported_location_property(tpl1::tpl1 libfile)
      set(TPL_Tpl1_INCLUDE_DIRS "${inclDirs}" CACHE PATH "Include dirs for Tpl1")
      set(TPL_Tpl1_LIBRARIES "${libfile}" CACHE PATH "Libraries for Tpl1")
    else()
      message(FATAL_ERROR "ToDo: Implement!")
      # ToDo: Put in a call to find_dependency() in the generated
      # Tpl1Config.cmake file and set Tpl1_DIR in that file to the found path so
      # it finds the same file.  For now, just getting the include directories
      # and the library path is enough.
    endif()
  endif()
endif()

tribits_tpl_find_include_dirs_and_libraries( Tpl1
  REQUIRED_HEADERS ${REQUIRED_HEADERS}
  REQUIRED_LIBS_NAMES ${REQUIRED_LIBS_NAMES}
  )
