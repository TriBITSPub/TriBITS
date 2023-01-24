# This file contains logic for the expected dependencies for each package and
# TPLs used in TribitsExampleProject.  This logic is contained here instead of
# in the packages's CMakeLists.txt files in case some of these are pulled in
# as external packages and that package's CMakeLists.txt files are not
# actually processed.  CMakeLists.txt files that need this info just include
# this file at the point of where it is needed.
#
# NOTE: A file like this that gets included in the individual TriBITS packages
# would be a bad idea in real TriBITS packages.  A TriBITS package should be
# self-contained and not refer to any files outside of its base package
# directory.  But in this case, we do this so that we can avoid duplication in
# this logic.  If we really wanted to, we could put this info into the
# <Package>Config.cmake files that get installed so that this info was
# self-contained in each package like it was before.

tribits_get_package_enable_status(SimpleCxx SimpleCxx_enabled "")
if (SimpleCxx_enabled)
  if (SimpleCxx_ENABLE_SimpleTpl)
    set(simpletplText "simpletpl ")
  else()
    set(simpletplText)
  endif()
  set(EXPECTED_SIMPLECXX_AND_DEPS
    "SimpleCxx ${simpletplText}headeronlytpl")
endif()

tribits_get_package_enable_status(InsertedPkg InsertedPkg_enabled "")
if (InsertedPkg_enabled)
  set(EXPECTED_INSERTEDPKG_AND_DEPS "InsertedPkg ${EXPECTED_SIMPLECXX_AND_DEPS}")
  set(EXPECTED_INSERTEDPKG_AND_DEPS_STR "${EXPECTED_INSERTEDPKG_AND_DEPS} ")
else()
  set(EXPECTED_INSERTEDPKG_DEPS "")
  set(EXPECTED_INSERTEDPKG_DEPS_STR "")
endif()

tribits_get_package_enable_status(WithSubpackagesA WithSubpackagesA_enabled "")
if (WithSubpackagesA_enabled)
  set(EXPECTED_A_AND_DEPS "A ${EXPECTED_SIMPLECXX_AND_DEPS}")
  set(EXPECTED_A_AND_DEPS_STR "${EXPECTED_A_AND_DEPS} ")
else()
  set(EXPECTED_A_AND_DEPS "")
  set(EXPECTED_A_AND_DEPS_STR "")
endif()

tribits_get_package_enable_status(WithSubpackagesB WithSubpackagesB_enabled "")
if (WithSubpackagesB_enabled)
  set(EXPECTED_B_DEPS
  "${EXPECTED_A_AND_DEPS_STR}${EXPECTED_INSERTEDPKG_AND_DEPS_STR}${EXPECTED_SIMPLECXX_AND_DEPS}")
endif()
