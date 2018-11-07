#!/usr/bin/env python

# @HEADER
# ************************************************************************
#
#            TriBITS: Tribal Build, Integrate, and Test System
#                    Copyright 2013 Sandia Corporation
#
# Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
# the U.S. Government retains certain rights in this software.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the Corporation nor the names of the
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY SANDIA CORPORATION "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL SANDIA CORPORATION OR THE
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# ************************************************************************
# @HEADER

import sys
import pprint
import datetime

from FindGeneralScriptSupport import *
from GeneralScriptSupport import *
import CDashQueryAnalyzeReport as CDQAR
from gitdist import addOptionParserChoiceOption

#
# Help message
#


usageHelp = r"""analyze_and_report_cdash_results.py [options]

This script takes in CDash URL information and other data as command-line
arguments and then analyzes it to look for missing expected and various types
of failures and then reports the findings as an HTML file written to disk
and/or as an HTML formatted email to one or more email addresses.

If all of the expected builds are found (and all of them have test results)
and there are no other failures found, then the script returns 0.  Otherwise
the script returns non-zero.  Therefore, this script can be used to drive
automated workflows by examining data on CDash.

ToDo: Finish documentation!
"""


#
# Helper functions
#


def injectCmndLineOptionsInParser(clp, gitoliteRootDefault=""):

  yesterday = (datetime.date.today()+datetime.timedelta(days=-1)).isoformat()

  clp.add_option(
    "--date", dest="date", type="string", default=yesterday,
    help="Date for the testing day <YYYY-MM-DD>."+\
      " (Default yesterday '"+yesterday+"')" )

  clp.add_option(
    "--cdash-project-name", dest="cdashProjectName", type="string", default="",
    help="CDash project name, e.g. 'Trilinos'. (Default '')" )

  clp.add_option(
    "--build-set-name", dest="buildSetName", type="string", default="",
    help="Name for the set of builds. (Default '')" )

  clp.add_option(
    "--test-set-name", dest="testSetName", type="string", default="",
    help="Name for the set of tests. (Default '')" )

  clp.add_option(
    "--cdash-site-url", dest="cdashSiteUrl", type="string", default="",
    help="Base CDash site, e.g. 'https://testing.sandia.gov/cdash'. (Default '')" )

  clp.add_option(
    "--cdash-builds-filters", dest="cdashBuildsFilters", type="string",
    default="",
    help="Partial URL fragment for index.php making of the filters for" \
      +" the set of builds. (Default '')" )

  clp.add_option(
    "--cdash-nonpassed-tests-filters", dest="cdashNonpassedTestsFilters", type="string",
    default="",
    help="Partial URL fragment for queryTests.php making of the filters for" \
      +" the set of non-passing tests matching this set of builds. (Default '')" )

  clp.add_option(
    "--limit-test-history-days", dest="testHistoryDays", default=30,
    help="Number of days to go back in history for each test" )
    # ToDo: Rename testHistoryDays to limitTestHistoryDays

  clp.add_option(
    "--expected-builds-file", dest="expectedBuildsFile", type="string",
    default="",
    help="Path to CSV file that lists the expected builds. (Default '')" )

  clp.add_option(
    "--tests-with-issue-trackers-file", dest="testsWithIssueTrackersFile",
    type="string",  default="",
    help="the subject line on sent out emails" )

  cdashQueriesCacheDir_default=os.getcwd()

  clp.add_option(
    "--cdash-queries-cache-dir", dest="cdashQueriesCacheDir", type="string",
    default=cdashQueriesCacheDir_default,
    help="Cache CDash query data this directory" \
      +" (default ='"+cdashQueriesCacheDir_default+"')." )

  clp.add_option(
    "--cdash-base-cache-files-prefix", dest="cdashBaseCacheFilesPrefix", type="string",
    default="",
    help="Prefix given to the base-level cache files outside of the test_history/"+\
      " directory.   This is to allow multiple invocations of this script to share"+\
      " the same base cache directory and share the test_history/ in case there are"+\
      " overrlapping sets of tests where the cache could be reused."+\
      " (default is derived from the --build-set-name=<build_set_name> argument where"+\
      " spaces and punctuation in <build_set_name> is replaced with '_')" )

  addOptionParserChoiceOption(
    "--use-cached-cdash-data", "useCachedCDashDataStr",
    ("on", "off"), 1,
    "Use data downloaded from CDash already cached.",
    clp )

  clp.add_option(
    "--limit-table-rows", dest="limitTableRows", type="int",
    default=10,
    help="Limit to the number of table rows. (Default '10')" )

  addOptionParserChoiceOption(
    "--print-details", "printDetailsStr",
    ("on", "off"), 1,
    "Print more info about what is happening.",
    clp )

  clp.add_option(
    "--write-email-to-file", dest="writeEmailToFile", type="string", default="",
    help="Write the body of the HTML email to this file. (Default '')" )

  clp.add_option(
    "--email-from-address=", dest="emailFromAddress", type="string", default="",
    help="Address reported in the sent email. (Default '')" )

  clp.add_option(
    "--send-email-to=", dest="sendEmailTo", type="string", default="",
    help="Send email to 'address1,address2,...'. (Default '')" )


def validateCmndLineOptions(inOptions):
  
  if inOptions.date == "":
    print "Error, can't have empty --date, must pass in --date=YYYY-MM-DD!"
    sys.exit(1)
  else:
    CDQAR.validateAndConvertYYYYMMDD(inOptions.date)

  # ToDo: Assert more of the options to make sure they are correct!


def getCmndLineOptions():
  from optparse import OptionParser
  clp = OptionParser(usage=usageHelp)
  injectCmndLineOptionsInParser(clp)
  (options, args) = clp.parse_args()
  validateCmndLineOptions(options)
  return options


def fwdCmndLineOptions(inOptions, lt=""):
  cmndLineOpts = \
    "  --date='"+inOptions.date+"'"+lt+\
    "  --cdash-project-name='"+inOptions.cdashProjectName+"'"+lt+\
    "  --build-set-name='"+inOptions.buildSetName+"'"+lt+\
    "  --test-set-name='"+inOptions.testSetName+"'"+lt+\
    "  --cdash-site-url='"+inOptions.cdashSiteUrl+"'"+lt+\
    "  --cdash-builds-filters='"+inOptions.cdashBuildsFilters+"'"+lt+\
    "  --cdash-nonpassed-tests-filters='"+inOptions.cdashNonpassedTestsFilters+"'"+lt+\
    "  --expected-builds-file='"+inOptions.expectedBuildsFile+"'"+lt+\
    "  --tests-with-issue-trackers-file='"+inOptions.testsWithIssueTrackersFile+"'"+lt+\
    "  --cdash-queries-cache-dir='"+inOptions.cdashQueriesCacheDir+"'"+lt+\
    "  --cdash-base-cache-files-prefix='"+inOptions.cdashBaseCacheFilesPrefix+"'"+lt+\
    "  --use-cached-cdash-data='"+inOptions.useCachedCDashDataStr+"'"+lt+\
    "  --limit-table-rows='"+str(inOptions.limitTableRows)+"'"+lt+\
    "  --print-details='"+inOptions.printDetailsStr+"'"+lt+\
    "  --write-email-to-file='"+inOptions.writeEmailToFile+"'"+lt+\
    "  --email-from-address='"+inOptions.emailFromAddress+"'"+lt+\
    "  --send-email-to='"+inOptions.sendEmailTo+"'"+lt
  return cmndLineOpts 


def echoCmndLineOptions(inOptions):
  print(fwdCmndLineOptions(inOptions, " \\\n"))


def echoCmndLine(inOptions):

  print("")
  print("**************************************************************************")
  print("analyze_and_report_cdash_results.py \\")

  echoCmndLineOptions(inOptions)


# Temp function to get flat list of tests
def getFlatListOfTestsFromTestDict(testsDict):
  testDictList = []
  for key in testsDict.keys():
    testDictList.append(testsDict[key])
  return testDictList


#
# Run the script
#

if __name__ == '__main__':

  #
  # Get commandline options and bool versions of [on|off] and others
  #

  inOptions = getCmndLineOptions()
  echoCmndLine(inOptions)

  if inOptions.useCachedCDashDataStr == "on":
    setattr(inOptions, 'useCachedCDashData', True)
  else:
    setattr(inOptions, 'useCachedCDashData', False)

  if inOptions.printDetailsStr == "on":
    setattr(inOptions, 'printDetails', True)
  else:
    setattr(inOptions, 'printDetails', False)

  if inOptions.cdashBaseCacheFilesPrefix == "":
    inOptions.cdashBaseCacheFilesPrefix = \
     CDQAR.getFileNameStrFromText(inOptions.buildSetName)

  cacheDirAndBaseFilePrefix = \
    inOptions.cdashQueriesCacheDir+"/"+inOptions.cdashBaseCacheFilesPrefix

  #
  # A) Define common data, etc
  #

  tcd = CDQAR.TableColumnData
  pp = pprint.PrettyPrinter(indent=2)

  groupSiteBuildNameSortOrder = ['group', 'site', 'buildname']

  #
  # B) Sound off
  #

  print "***"
  print "*** Query and analyze CDash results "+inOptions.buildSetName+\
        " for testing day "+inOptions.date
  print "***"

  #
  # C) Create beginning of email body (that does not require getting any data off CDash)
  #

  # This is the top of the body
  htmlEmailBodyTop = ""
  # This is the bottom of the email body
  htmlEmailBodyBottom = ""
  # This var will store the list of data numbers for the summary line
  summaryLineDataNumbersList = []

  htmlEmailBodyTop += \
   "<h2>Build and Test results for "+inOptions.buildSetName \
      +" on "+inOptions.date+"</h2>\n\n"

  #
  # D) Read data files, get data off of CDash, do analysis, and construct HTML
  # body parts
  #
  
  globalPass = True

  try:

    #
    # D.1) Read data from input files
    #
    # Assert this data is correct and abort if there is an error before we run
    # expensive CDash queries!
    #

    # Get list of expected builds from input CSV file
    if inOptions.expectedBuildsFile:
      expectedBuildsLOD = \
        CDQAR.getExpectedBuildsListfromCsvFile(inOptions.expectedBuildsFile)
    else:
      expectedBuildsLOD = []
    print("\nNum expected builds = "+str(len(expectedBuildsLOD)))

    # Get list of tests with issue tracker from input CSV file
    testsWithIssueTrackersLOD = \
      CDQAR.getTestsWtihIssueTrackersListFromCsvFile(inOptions.testsWithIssueTrackersFile)
    print("\nNum tests with issue trackers = "+str(len(expectedBuildsLOD)))
    # Get a SearchableListOfDicts for the tests with issue trackers to allow
    # them to be looked up based on matching ['site', 'buildName', 'testname']
    # key/value pairs.
    testsWithIssueTrackerSLOD = \
      CDQAR.createSearchableListOfTests(testsWithIssueTrackersLOD)
    # Get a functor that will return True if a passed-in dict matches the
    # ['site', 'buildName', and 'testname'] key/value pairs.
    testsWithIssueTrackerMatchFunctor = \
      CDQAR.MatchDictKeysValuesFunctor(testsWithIssueTrackerSLOD)

    # Assert they the list of tests with issue trackers matches the list of
    # expected builds
    (allTestsMatch, errMsg) = CDQAR.testsWithIssueTrackersMatchExpectedBuilds(
      testsWithIssueTrackersLOD, expectedBuildsLOD)
    if not allTestsMatch:
      raise Exception(errMsg)

    #
    # D.2) Get lists of build and test data off CDash
    #

    #
    # D.2.a) Get list of dicts of builds off CDash
    #

    cdashIndexBuildsBrowserUrl = CDQAR.getCDashIndexBrowserUrl(
      inOptions.cdashSiteUrl, inOptions.cdashProjectName, inOptions.date,
      inOptions.cdashBuildsFilters)

    print("\nCDash builds browser URL:\n\n  "+cdashIndexBuildsBrowserUrl+"\n")
   
    cdashIndexBuildsQueryUrl = CDQAR.getCDashIndexQueryUrl(
      inOptions.cdashSiteUrl,
      inOptions.cdashProjectName,
      inOptions.date,
      inOptions.cdashBuildsFilters )

    fullCDashIndexBuildsJsonCacheFile = \
      cacheDirAndBaseFilePrefix+"fullCDashIndexBuilds.json"

    buildsListOfDicts = CDQAR.downloadBuildsOffCDashAndFlatten(
      cdashIndexBuildsQueryUrl,
      fullCDashIndexBuildsJsonCacheFile,
      inOptions.useCachedCDashData )
    print("\nNum builds = "+str(len(buildsListOfDicts)))

    # Beginning of top full bulid and tests CDash links paragraph 
    htmlEmailBodyTop += "<p>\n"
  
    # Builds on CDash
    htmlEmailBodyTop += \
     "<a href=\""+cdashIndexBuildsBrowserUrl+"\">"+\
     "Builds on CDash</a> (num="+str(len(buildsListOfDicts))+")<br>\n"

    # Get a dict to help look up builds
    buildsSLOD = CDQAR.createSearchableListOfBuilds(buildsListOfDicts)

    #
    # D.2.b) Get list of dicts of all non-passing tests off CDash and for
    # tests with issue trackers.
    #

    cdashNonpassingTestsBrowserUrl = CDQAR.getCDashQueryTestsBrowserUrl(
      inOptions.cdashSiteUrl, inOptions.cdashProjectName, inOptions.date,
      inOptions.cdashNonpassedTestsFilters)

    print("\nGetting list of non-passing tests from CDash ...\n")

    print("\nCDash non-passing tests browser URL:\n\n"+\
      "  "+cdashNonpassingTestsBrowserUrl+"\n")

    # Get a single list of dicts of non-passing tests for current testing day
    # off CDash

    cdashNonpassingTestsQueryUrl = CDQAR.getCDashQueryTestsQueryUrl(
      inOptions.cdashSiteUrl, inOptions.cdashProjectName, inOptions.date,
      inOptions.cdashNonpassedTestsFilters)

    cdashNonpassingTestsQueryJsonCacheFile = \
      cacheDirAndBaseFilePrefix+"fullCDashNonpassingTests.json"

    nonpassingTestsLOD = CDQAR.downloadTestsOffCDashQueryTestsAndFlatten(
      cdashNonpassingTestsQueryUrl, cdashNonpassingTestsQueryJsonCacheFile,
      inOptions.useCachedCDashData )
    print("\nNum nonpassing tests direct from CDash query = "+str(len(nonpassingTestsLOD)))

    # Create a searchable list of nonpassing tests
    nonpassingTestsSLOD = CDQAR.createSearchableListOfTests(nonpassingTestsLOD,
      removeExactDuplicateElements=True)
    # NOTE: Above we add the option to remove exact 100% duplicate list items
    # since cdash/queryTests.php can return duplicate tests!
    print("Num nonpassing tests after removing duplicate tests = "+str(len(nonpassingTestsLOD)))

    # Create a functor to match nonpassing tests
    nonpassingTestsMatchFunctor = \
      CDQAR.MatchDictKeysValuesFunctor(nonpassingTestsSLOD)

    # Add issue tracker info for all non passing tests
    CDQAR.foreachTransform(nonpassingTestsLOD,
      CDQAR.AddIssueTrackerInfoToTestDictFunctor(testsWithIssueTrackerSLOD))

    # Split the list of nonpassing tests into those with and without issue
    # trackers
    (nonpassingTestsWithIssueTrackersLOD,nonpassingTestsWithoutIssueTrackersLOD)=\
      CDQAR.splitListOnMatch(
        nonpassingTestsLOD,
        testsWithIssueTrackerMatchFunctor
        )
    print("Num nonpassing tests without issue trackers = "+\
      str(len(nonpassingTestsWithoutIssueTrackersLOD)))
    print("Num nonpassing tests with issue trackers = "+\
      str(len(nonpassingTestsWithIssueTrackersLOD)))

    # Split the list nonpassing tests without issue trackers into 'twoif' and
    # 'twoinp'
    (twoifLOD, twoinrLOD) = CDQAR.splitListOnMatch(
      nonpassingTestsWithoutIssueTrackersLOD, CDQAR.isTestFailed)
    print("Num nonpassing tests without issue trackers Failed = "+str(len(twoifLOD)))
    print("Num nonpassing tests without issue trackers Not Run = "+str(len(twoinrLOD)))

    # Split the list nonpassing tests with issue trackers into 'twif' and
    # 'twinp'
    (twifLOD, twinrLOD) = CDQAR.splitListOnMatch(
      nonpassingTestsWithIssueTrackersLOD, CDQAR.isTestFailed)
    print("Num nonpassing tests with issue trackers Failed = "+str(len(twifLOD)))
    print("Num nonpassing tests with issue trackers Not Run = "+str(len(twinrLOD)))

    # Get list of tests with issue trackers that are not in the list of
    # non-passing tests
    testsWithIssueTrackersNotNonpassingLOD = CDQAR.getFilteredList(
      testsWithIssueTrackerSLOD,
      CDQAR.NotMatchFunctor(nonpassingTestsMatchFunctor) )
    print("Num tests with issue trackers not nonpassing = "+\
      str(len(testsWithIssueTrackersNotNonpassingLOD)))
  
    # Nonpassing Tests on CDash
    htmlEmailBodyTop += \
     "<a href=\""+cdashNonpassingTestsBrowserUrl+"\">"+\
     "Nonpassing Tests on CDash</a> (num="+str(len(nonpassingTestsLOD))+")<br>\n"
  
    # End of full build and test link paragraph and start the next paragraph
    # for the summary of failures and other tables
    htmlEmailBodyTop += \
      "</p>\n\n"+\
      "<p>\n"

    #
    print("\nSearch for any missing expected builds ...\n")
    #

    missingExpectedBuildsLOD = CDQAR.getMissingExpectedBuildsList(
      buildsSLOD, expectedBuildsLOD)
    #pp.pprint(missingExpectedBuildsLOD)

    bmeDescr = "Missing expected builds"
    bmeAcro = "bme"
    bmeNum = len(missingExpectedBuildsLOD)

    bmeSummaryStr = \
      CDQAR.getCDashDataSummaryHtmlTableTitleStr(bmeDescr,  bmeAcro, bmeNum)

    print(bmeSummaryStr)

    if bmeNum > 0:

      globalPass = False

      summaryLineDataNumbersList.append(bmeAcro+"="+str(bmeNum))

      htmlEmailBodyTop += CDQAR.makeHtmlTextRed(bmeSummaryStr)+"<br>\n"

      bmeColDataList = [
        tcd('group', "Group"),
        tcd('site', "Site"),
        tcd('buildname', "Build Name"),
        tcd('status', "Missing Status"),
        ]

      htmlEmailBodyBottom += CDQAR.createCDashDataSummaryHtmlTableStr(
        bmeDescr,  bmeAcro, bmeColDataList, missingExpectedBuildsLOD,
        groupSiteBuildNameSortOrder, None )
      # NOTE: Above we don't want to limit any missing builds in this table
      # because that data is not shown on CDash and that list will never be
      # super big.

    #
    print("\nSearch for any builds with configure failures ...\n")
    #

    buildsWithConfigureFailuresLOD = \
      CDQAR.getFilteredList(buildsSLOD, CDQAR.buildHasConfigureFailures)

    cDescr = "Builds with configure failures"
    cAcro = "c"
    cNum = len(buildsWithConfigureFailuresLOD)

    cSummaryStr = \
      CDQAR.getCDashDataSummaryHtmlTableTitleStr(cDescr,  cAcro, cNum)

    print(cSummaryStr)

    if cNum > 0:

      globalPass = False

      summaryLineDataNumbersList.append(cAcro+"="+str(cNum))

      htmlEmailBodyTop += CDQAR.makeHtmlTextRed(cSummaryStr)+"<br>\n"

      cColDataList = [
        tcd('group', "Group"),
        tcd('site', "Site"),
        tcd('buildname', "Build Name"),
        ]

      htmlEmailBodyBottom += CDQAR.createCDashDataSummaryHtmlTableStr(
        cDescr,  cAcro, cColDataList, buildsWithConfigureFailuresLOD,
        groupSiteBuildNameSortOrder, inOptions.limitTableRows )

      # ToDo: Update to show number of configure failures and the history info
      # for that build with hyperlinks and don't limit the number of builds
      # shown.

    #
    print("\nSearch for any builds with compilation (build) failures ...\n")
    #

    buildsWithBuildFailuresLOD = \
      CDQAR.getFilteredList(buildsSLOD, CDQAR.buildHasBuildFailures)

    bDescr = "Builds with build failures"
    bAcro = "b"
    bNum = len(buildsWithBuildFailuresLOD)

    bSummaryStr = \
      CDQAR.getCDashDataSummaryHtmlTableTitleStr(bDescr,  bAcro, bNum)

    print(bSummaryStr)

    if bNum > 0:

      globalPass = False

      summaryLineDataNumbersList.append(bAcro+"="+str(bNum))

      htmlEmailBodyTop += CDQAR.makeHtmlTextRed(bSummaryStr)+"<br>\n"

      cColDataList = [
        tcd('group', "Group"),
        tcd('site', "Site"),
        tcd('buildname', "Build Name"),
        ]

      htmlEmailBodyBottom += CDQAR.createCDashDataSummaryHtmlTableStr(
        bDescr,  bAcro, cColDataList, buildsWithBuildFailuresLOD,
        groupSiteBuildNameSortOrder, inOptions.limitTableRows )

      # ToDo: Update to show number of builds failures and the history info
      # for that build with hyperlinks and don't limit the number of builds
      # shown.

    #
    # D.3) Analyaize and report test results in different tables
    #

    # Sort order for tests
    testnameBuildnameSiteSortOrder = ['testname', 'buildName', 'site']

    # Cache directory for test history data
    testHistoryCacheDir = inOptions.cdashQueriesCacheDir+"/test_history"

    # Get test history for all of the tests with issue trackers that are not
    # nonpassing.  These will either be tests that are passing toiday (and
    # therefore have history) or they will be tests that are missing.

    twipLOD = []
    twimLOD = []

    if testsWithIssueTrackersNotNonpassingLOD:

      print("\nGetting test history for tests with issue trackers"+\
        " that are not nonpassing: num="+str(len(testsWithIssueTrackersNotNonpassingLOD)))

      CDQAR.foreachTransform(
        testsWithIssueTrackersNotNonpassingLOD,
        CDQAR.AddTestHistoryToTestDictFunctor(
          inOptions.cdashSiteUrl,
          inOptions.cdashProjectName,
          inOptions.date,
          inOptions.testHistoryDays,
          testHistoryCacheDir,
          useCachedCDashData=inOptions.useCachedCDashData,
          alwaysUseCacheFileIfExists=True,
          verbose=True,
          printDetails=inOptions.printDetails,
          )
        )

      # Split into list of tests that are passing vs. those that are missing
      (twipLOD, twimLOD) = CDQAR.splitListOnMatch(
        testsWithIssueTrackersNotNonpassingLOD, CDQAR.isTestPassed )

    print("\nNum tests with issue trackers Passed = "+str(len(twipLOD)))
    print("Num tests with issue trackers Missing = "+str(len(twimLOD)))

    #
    # D.3.a) twoif
    #

    print("")

    twoifDescr = "Failing tests without issue trackers"
    twoifAcro = "twoif"
    twoifNum = len(twoifLOD)

    twoifSummaryStr = \
      CDQAR.getCDashDataSummaryHtmlTableTitleStr(twoifDescr, twoifAcro, twoifNum)

    print(twoifSummaryStr)

    if twoifNum > 0:

      globalPass = False

      summaryLineDataNumbersList.append(twoifAcro+"="+str(twoifNum))

      htmlEmailBodyTop += CDQAR.makeHtmlTextRed(twoifSummaryStr)+"<br>\n"

      # Sort and get only the top <N> non-passing tests without issue trackers
      # (since this can be a huge number of failing tests)
      twoifSortedLimitedLOD = CDQAR.sortAndLimitListOfDicts(
        twoifLOD, testnameBuildnameSiteSortOrder,
        inOptions.limitTableRows )

      # Add test history data to the tope <N> non-assing tests without issue
      # trackres
      CDQAR.foreachTransform(
        twoifSortedLimitedLOD,
        CDQAR.AddTestHistoryToTestDictFunctor(
          inOptions.cdashSiteUrl,
          inOptions.cdashProjectName,
          inOptions.date,
          inOptions.testHistoryDays,
          testHistoryCacheDir,
          useCachedCDashData=inOptions.useCachedCDashData,
          alwaysUseCacheFileIfExists=True,
          verbose=True,
          printDetails=inOptions.printDetails,
          )
        )

      htmlEmailBodyBottom += CDQAR.createCDashTestHtmlTableStr(
        twoifDescr, twoifAcro, twoifNum,
        twoifSortedLimitedLOD,
        inOptions.testHistoryDays, inOptions.limitTableRows )

    #
    # D.3.b) twoinr
    #

    print("")

    twoinrDescr = "Not Run tests without issue trackers"
    twoinrAcro = "twoinr"
    twoinrNum = len(twoinrLOD)

    twoinrSummaryStr = \
      CDQAR.getCDashDataSummaryHtmlTableTitleStr(twoinrDescr, twoinrAcro, twoinrNum)

    print(twoinrSummaryStr)

    if twoinrNum > 0:

      globalPass = False

      summaryLineDataNumbersList.append(twoinrAcro+"="+str(twoinrNum))

      htmlEmailBodyTop += CDQAR.makeHtmlTextRed(twoinrSummaryStr)+"<br>\n"

      # Sort and get only the top <N> non-passing tests without issue trackers
      # (since this can be a huge number of failing tests)
      twoinrSortedLimitedLOD = CDQAR.sortAndLimitListOfDicts(
        twoinrLOD, testnameBuildnameSiteSortOrder,
        inOptions.limitTableRows )

      # Add test history data to the tope <N> non-assing tests without issue
      # trackres
      CDQAR.foreachTransform(
        twoinrSortedLimitedLOD,
        CDQAR.AddTestHistoryToTestDictFunctor(
          inOptions.cdashSiteUrl,
          inOptions.cdashProjectName,
          inOptions.date,
          inOptions.testHistoryDays,
          testHistoryCacheDir,
          useCachedCDashData=inOptions.useCachedCDashData,
          alwaysUseCacheFileIfExists=True,
          verbose=True,
          printDetails=inOptions.printDetails,
          )
        )

      htmlEmailBodyBottom += CDQAR.createCDashTestHtmlTableStr(
        twoinrDescr, twoinrAcro, twoinrNum,
        twoinrSortedLimitedLOD,
        inOptions.testHistoryDays, inOptions.limitTableRows )

    #
    # D.3.c) twif
    #

    print("")

    twifDescr = "Failing tests with issue trackers"
    twifAcro = "twif"
    twifNum = len(twifLOD)

    twifSummaryStr = \
      CDQAR.getCDashDataSummaryHtmlTableTitleStr(twifDescr, twifAcro, twifNum)

    print(twifSummaryStr)

    if twifNum > 0:

      globalPass = False

      summaryLineDataNumbersList.append(twifAcro+"="+str(twifNum))

      htmlEmailBodyTop += twifSummaryStr+"<br>\n"

      # Sort but do't limit the list
      twifSortedLOD = CDQAR.sortAndLimitListOfDicts(
        twifLOD, testnameBuildnameSiteSortOrder)

      # Add test history data to the tope <N> non-assing tests without issue
      # trackres
      CDQAR.foreachTransform(
        twifSortedLOD,
        CDQAR.AddTestHistoryToTestDictFunctor(
          inOptions.cdashSiteUrl,
          inOptions.cdashProjectName,
          inOptions.date,
          inOptions.testHistoryDays,
          testHistoryCacheDir,
          useCachedCDashData=inOptions.useCachedCDashData,
          alwaysUseCacheFileIfExists=True,
          verbose=True,
          printDetails=inOptions.printDetails,
          )
        )

      htmlEmailBodyBottom += CDQAR.createCDashTestHtmlTableStr(
        twifDescr, twifAcro, twifNum, twifSortedLOD,
        inOptions.testHistoryDays )
      # NOTE: We don't limit the number of tests tracked tests listed because
      # we will never have a huge number of failing tests with issue trackers.

    #
    # D.3.d) twinr
    #

    print("")

    twinrDescr = "Not Run tests with issue trackers"
    twinrAcro = "twinr"
    twinrNum = len(twinrLOD)

    twinrSummaryStr = \
      CDQAR.getCDashDataSummaryHtmlTableTitleStr(twinrDescr, twinrAcro, twinrNum)

    print(twinrSummaryStr)

    if twinrNum > 0:

      globalPass = False

      summaryLineDataNumbersList.append(twinrAcro+"="+str(twinrNum))

      htmlEmailBodyTop += twinrSummaryStr+"<br>\n"

      # Sort but do't limit the list
      twinrSortedLOD = CDQAR.sortAndLimitListOfDicts(
        twinrLOD, testnameBuildnameSiteSortOrder)

      # Add test history data to the tope <N> non-assing tests without issue
      # trackres
      CDQAR.foreachTransform(
        twinrSortedLOD,
        CDQAR.AddTestHistoryToTestDictFunctor(
          inOptions.cdashSiteUrl,
          inOptions.cdashProjectName,
          inOptions.date,
          inOptions.testHistoryDays,
          testHistoryCacheDir,
          useCachedCDashData=inOptions.useCachedCDashData,
          alwaysUseCacheFileIfExists=True,
          verbose=True,
          printDetails=inOptions.printDetails,
          )
        )

      htmlEmailBodyBottom += CDQAR.createCDashTestHtmlTableStr(
        twinrDescr, twinrAcro, twinrNum, twinrSortedLOD,
        inOptions.testHistoryDays )

    # Generate table "Tests with issue trackers missing: twim=???"

    # ToDo: Implement!

    # Generate table "Tests with issue trackers currently passing: twip=???"

    # ToDo: Implement!
 
  except Exception:
    # Traceback!
    sys.stdout.flush()
    traceback.print_exc()
    # Report the error
    htmlEmailBodyTop += CDQAR.htmlNewlineBreak(traceback.format_exc()) 
    print("\nError, could not compute the analysis due to"+\
      " above error so return failed!")
    globalPass = False
    summaryLineDataNumbersList.append("SCRIPT CRASHED")

  #
  # E) Put together final email summary  line
  #

  if globalPass:
    summaryLine = "PASSED"
  else:
    summaryLine = "FAILED"

  if summaryLineDataNumbersList:
    summaryLine += " (" + ", ".join(summaryLineDataNumbersList) + ")"

  summaryLine += ": "+inOptions.buildSetName+" on "+inOptions.date

  #
  # F) Finish of HTML body guts and define overall body style
  #

  # Finish off the top paragraph of the summary lines
  htmlEmailBodyTop += \
    "</p>"
    
  # Construct HTML body guts without header or begin/end body.
  htmlEmaiBodyGuts = \
    htmlEmailBodyTop+\
    "\n\n"+\
    htmlEmailBodyBottom

  htmlHeaderAndBeginBody = \
    "<html>\n"+\
    "<head>\n"+\
    "<style>\n"+\
    "h1 {\n"+\
    "  font-size: 40px;\n"+\
    "}\n"+\
    "h2 {\n"+\
    "  font-size: 30px;\n"+\
    "}\n"+\
    "h3 {\n"+\
    "  font-size: 24px;\n"+\
    "}\n"+\
    "p {\n"+\
    "  font-size: 18px;\n"+\
    "}\n"+\
    "</style>\n"+\
    "</head>\n"+\
    "\n"+\
    "<body>\n"+\
    "\n"

  htmlEndBody = \
    "</body>\n"+\
    "</html>\n"

  #
  # G) Write HTML body file and/or send HTML email(s)
  #

  if inOptions.writeEmailToFile:
    print("\nWriting HTML file '"+inOptions.writeEmailToFile+"' ...")
    htmlEmaiBodyFileStr = \
      htmlHeaderAndBeginBody+\
      "<h2>"+summaryLine+"</h2>\n\n"+\
      htmlEmaiBodyGuts+"\n"+\
      htmlEndBody
    with open(inOptions.writeEmailToFile, 'w') as outFile:
      outFile.write(htmlEmaiBodyFileStr)

  if inOptions.sendEmailTo:
    htmlEmaiBody = \
      htmlHeaderAndBeginBody+\
      htmlEmaiBodyGuts+"\n"+\
      htmlEndBody
    for emailAddress in inOptions.sendEmailTo.split(','):
      emailAddress = emailAddress.strip()
      print("\nSending email to '"+emailAddress+"' ...")
      msg=CDQAR.createHtmlMimeEmail(
        inOptions.emailFromAddress, emailAddress, summaryLine, "", htmlEmaiBody)
      CDQAR.sendMineEmail(msg)

  #
  # H) Return final global pass/fail
  #

  print("\n"+summaryLine+"\n")

  if globalPass:
    sys.exit(0)
  else:
    sys.exit(1)
  
