include(TribitsReadTagFile)


# @FUNCTION: tribits_get_cdash_build_url_from_tag_file()
#
# Create CDash index.php URL from the build parts.
#
# Usage::
#
#   tribits_get_cdash_build_url_from_tag_file(
#     INDEX_PHP_URL <indexPhpUrl>
#     PROJECT_NAME <projectName>
#     SITE_NAME <siteName>
#     BUILD_NAME <buildName>
#     TAG_FILE <tagFile>
#     CDASH_BUILD_URL_OUT <cdashBuildUrlOut>
#     )
#
# Note that spaces are allowed ``<siteName>`` or ``<buildName>`` and those
# will be handled correctly to produce a valid URL.
#
function(tribits_get_cdash_build_url_from_tag_file)
  # Get arguments
  cmake_parse_arguments(
    PREFIX #prefix
    "" #options
    "INDEX_PHP_URL;PROJECT_NAME;SITE_NAME;BUILD_NAME;TAG_FILE;CDASH_BUILD_URL_OUT" #one_value_keywords
    "" #multi_value_keytowrds
    ${ARGN}
    )
  # Read in the tag file and get the build stamp from that
  tribits_read_ctest_tag_file(${PREFIX_TAG_FILE} buildStartTime cdashGroup cdashModel)
  set(buildstamp "${buildStartTime}-${cdashGroup}")
  # Build the URL and return it
  tribits_get_cdash_build_url_from_parts(
    INDEX_PHP_URL "${PREFIX_INDEX_PHP_URL}"
    PROJECT_NAME "${PREFIX_PROJECT_NAME}"
    SITE_NAME "${PREFIX_SITE_NAME}"
    BUILD_NAME "${PREFIX_BUILD_NAME}"
    BUILD_STAMP "${buildstamp}"
    CDASH_BUILD_URL_OUT cdashBuildUrl
    )
  set(${PREFIX_CDASH_BUILD_URL_OUT} "${cdashBuildUrl}" PARENT_SCOPE)
endfunction()


# @FUNCTION: tribits_get_cdash_build_url_from_parts()
#
# Create CDash index.php URL from the build parts.
#
# Usage::
#
#   tribits_get_cdash_build_url_from_parts(
#     INDEX_PHP_URL <indexPhpUrl>
#     PROJECT_NAME <projectName>
#     SITE_NAME <siteName>
#     BUILD_NAME <buildName>
#     BUILD_STAMP <buildStamp>
#     CDASH_BUILD_URL_OUT <cdashBuildUrlOut>
#     )
#
# Note that spaces are allowed ``<siteName>``, ``<buildName>`` or
# ``<buildStamp>`` and those will be handled correctly to produce a valid URL.
#
function(tribits_get_cdash_build_url_from_parts)
  # Get arguments
  cmake_parse_arguments(
    PREFIX #prefix
    "" #options
    "INDEX_PHP_URL;PROJECT_NAME;SITE_NAME;BUILD_NAME;BUILD_STAMP;CDASH_BUILD_URL_OUT" #one_value_keywords
    "" #multi_value_keytowrds
    ${ARGN}
    )
  # Do replacements for spaces and special chars in data
  tribits_replace_chars_for_url("${PREFIX_PROJECT_NAME}" project)
  tribits_replace_chars_for_url("${PREFIX_SITE_NAME}" site)
  tribits_replace_chars_for_url("${PREFIX_BUILD_NAME}" buildname)
  tribits_replace_chars_for_url("${PREFIX_BUILD_STAMP}" buildstamp)
  # Build the URL
  set(cdashIndexProj "${PREFIX_INDEX_PHP_URL}?project=${project}")
  set(filtersPreTxt "filtercount=3&showfilters=1&filtercombine=and")
  set(siteFlt "field1=site&compare1=61&value1=${site}")
  set(buildnameFlt "field2=buildname&compare2=61&value2=${buildname}")
  set(buildStampFlt "field3=buildstamp&compare3=61&value3=${buildstamp}")
  set(cdashBuildUrl
    "${cdashIndexProj}&${filtersPreTxt}&${siteFlt}&${buildnameFlt}&${buildStampFlt}")
  set(${PREFIX_CDASH_BUILD_URL_OUT} "${cdashBuildUrl}" PARENT_SCOPE)
endfunction()


function(tribits_replace_chars_for_url  inputStr  outputStrForUrlOutVar)
  set(outputStrForUrl "${inputStr}")
  string(REPLACE " " "%20" outputStrForUrl "${outputStrForUrl}")
  string(REPLACE "+" "%2B" outputStrForUrl "${outputStrForUrl}")
  set(${outputStrForUrlOutVar} "${outputStrForUrl}" PARENT_SCOPE)
endfunction()
