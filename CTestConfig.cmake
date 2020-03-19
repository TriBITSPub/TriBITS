INCLUDE(SetDefaultAndFromEnv)

SET(CTEST_NIGHTLY_START_TIME "04:00:00 UTC")  # Midnight EST
# NOTE: This does not need to be set for git checkouts, but it does need to be
# set for the build time stamp and there is a defect in ctest_start(
# ... APPEND ) that requires this be set.  See:
#
#    https://gitlab.kitware.com/cmake/cmake/issues/20471
#
# This currently matches the start time for the project on CDash which is
# 00:00:00 EST.

IF (NOT DEFINED CTEST_DROP_METHOD)
  SET_DEFAULT_AND_FROM_ENV(CTEST_DROP_METHOD "http")
ENDIF()

IF (CTEST_DROP_METHOD STREQUAL "http" OR CTEST_DROP_METHOD STREQUAL "https")
  SET_DEFAULT_AND_FROM_ENV(CTEST_DROP_SITE "testing.sandia.gov")
  SET_DEFAULT_AND_FROM_ENV(CTEST_PROJECT_NAME "TriBITS")
  SET_DEFAULT_AND_FROM_ENV(CTEST_DROP_LOCATION "/cdash/submit.php?project=TriBITS")
  SET_DEFAULT_AND_FROM_ENV(CTEST_TRIGGER_SITE "")
  SET_DEFAULT_AND_FROM_ENV(CTEST_DROP_SITE_CDASH TRUE)
ENDIF()
