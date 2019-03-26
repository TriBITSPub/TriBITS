include("${${PROJECT_NAME}_TRIBITS_DIR}/core/utils/MessageWrapper.cmake")

#
# @FUNCTION: TRIBITS_GET_VERSION_DATE_FROM_RAW_GIT_COMMIT_UTC_TIME()
#
# Takes input of the form "YYYY-MM-DD hh:mm:ss +0000" from the git command::
#
#   git log --format="%cd" --date=iso-local -1 <ref>
# 
# and returns the string integer YYYYMMDDhh.
#
# Usage::
#
#   TRIBITS_GET_VERSION_DATE_FROM_RAW_GIT_COMMIT_UTC_TIME(
#     ""YYYY-MM-DD hh:mm:ss +0000"  <version_date_var> )
#
# This returns a 10-digit integer ``YYYYMMDDhh`` that should fit in a 32-bit
# integer with a max value of ``2^32 / 2 - 1`` = ``2147483647`` and therefore
# should be good until the last hour of of the last day of the last month of
# the year 2147 (i.e. `2147 12 31 23` = `2147123123`).
#
function(TRIBITS_GET_VERSION_DATE_FROM_RAW_GIT_COMMIT_UTC_TIME
  git_raw_commit_time_utc  version_date_out
  )
  # Split by spaces first " "
  string(REPLACE " " ";"  git_raw_commit_time_utc_space_array
    "${git_raw_commit_time_utc}")
  #print_var(git_raw_commit_time_utc_space_array)
  list(GET git_raw_commit_time_utc_space_array 0 YYYY_MM_DD) # YYYY-MM-DD
  list(GET git_raw_commit_time_utc_space_array 1 hh_mm_ss)   # hh:mm:ss
  list(GET git_raw_commit_time_utc_space_array 2 utc_offset) # +0000
  #print_var(YYYY_MM_DD)
  #print_var(hh_mm_ss)
  #print_var(utc_offset)
  if (NOT utc_offset STREQUAL "+0000")
    message_wrapper(FATAL_ERROR "ERROR, '${git_raw_commit_time_utc}' is NOT"
      " in UTC which would have offset '+0000'!")
  endif()
  # Split YYYY-MM-DD into its componets
  string(REPLACE "-" ";" YYYY_MM_DD_array "${YYYY_MM_DD}")
  list(GET YYYY_MM_DD_array 0 YYYY)
  list(GET YYYY_MM_DD_array 1 MM)
  list(GET YYYY_MM_DD_array 2 DD)
  # Split hh:mm:ss into its componets
  string(REPLACE ":" ";" hh_mm_ss_array "${hh_mm_ss}")
  list(GET hh_mm_ss_array 0 hh)
  # Form the full YYYYMMDDhhmm integer and return
  set(${version_date_out} "${YYYY}${MM}${DD}${hh}" PARENT_SCOPE)
endfunction()
