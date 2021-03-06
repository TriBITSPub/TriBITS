########################################################################
# See associated tribits/Copyright.txt file for copyright and license! #
########################################################################

#
# First, set up the variables for the (backward-compatible) TriBITS way of
# finding HDF5.  These are used in case find_package(HDF5 ...) is not called
# or does not find HDF5.  Also, these variables need to be non-null in order
# to trigger the right behavior in the function
# tribits_tpl_find_include_dirs_and_libraries().
#

set(REQUIRED_HEADERS hdf5.h)
set(REQUIRED_LIBS_NAMES hdf5)

if (HDF5_REQUIRE_FORTRAN)
  set(REQUIRED_LIBS_NAMES ${REQUIRED_LIBS_NAMES} hdf5_fortran)
endif()

if (TPL_ENABLE_MPI)
  set(REQUIRED_LIBS_NAMES ${REQUIRED_LIBS_NAMES} z)
endif()

if (TPL_ENABLE_Netcdf)
  set(REQUIRED_LIBS_NAMES ${REQUIRED_LIBS_NAMES} hdf5_hl)
endif()

#
# Second, search for HDF5 components (if allowed) using the standard
# find_package(HDF5 ...).
#
tribits_tpl_allow_pre_find_package(HDF5  HDF5_ALLOW_PREFIND)
if (HDF5_ALLOW_PREFIND)

  message("-- Using find_package(HDF5 ...) ...")

  set(HDF5_COMPONENTS C)
  if (HDF5_REQUIRE_FORTRAN)
    list(APPEND HDF5_COMPONENTS Fortran)
  endif()

  if (TPL_ENABLE_MPI)
    set(HDF5_PREFER_PARALLEL TRUE)
  endif()

  find_package(HDF5 COMPONENTS ${HDF5_COMPONENTS})

  # Make sure that HDF5 is parallel.
  if (TPL_ENABLE_MPI AND NOT HDF5_IS_PARALLEL)
    message(FATAL_ERROR "Trilinos is configured for MPI, HDF5 is not.
    Did CMake find the correct libraries?
    Try setting HDF5_INCLUDE_DIRS and/or HDF5_LIBRARY_DIRS explicitly.
    ")
  endif()

  if (HDF5_FOUND)
    # Tell TriBITS that we found HDF5 and there no need to look any further!
    set(TPL_HDF5_INCLUDE_DIRS ${HDF5_INCLUDE_DIRS} CACHE PATH
      "HDF5 include dirs")
    set(TPL_HDF5_LIBRARIES ${HDF5_LIBRARIES} CACHE FILEPATH
      "HDF5 libraries")
    set(TPL_HDF5_LIBRARY_DIRS ${HDF5_LIBRARY_DIRS} CACHE PATH
      "HDF5 library dirs")
  endif()

endif()

#
# Third, call tribits_tpl_find_include_dirs_and_libraries()
#
tribits_tpl_find_include_dirs_and_libraries( HDF5
  REQUIRED_HEADERS ${REQUIRED_HEADERS}
  REQUIRED_LIBS_NAMES ${REQUIRED_LIBS_NAMES}
  )
# NOTE: If find_package(HDF5 ...) was called and successfully found HDF5, then
# tribits_tpl_find_include_dirs_and_libraries() will use the already-set
# variables TPL_HDF5_INCLUDE_DIRS and TPL_HDF5_LIBRARIES and then print them
# out (and set some other standard variables as well).  This is the final
# "hook" into the TriBITS TPL system.
