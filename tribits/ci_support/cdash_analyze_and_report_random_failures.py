#!/usr/bin/env python

import os
import sys
import datetime
import argparse
import re as regex

#
# Implementation code
#

# Find the implementation
tribitsDir = os.environ.get("TRIBITS_DIR", "")
if tribitsDir:
  sys.path = [os.path.join(tribitsDir, "ci_support")] + sys.path
else:
  raise Exception("ERROR, TRIBITS_DIR must be set in the env to 'tribits' base dir!")

import CreateIssueTrackerFromCDashQuery as CITFCQ
import CDashQueryAnalyzeReport as CDQAR
import cdash_build_testing_date as CBTD
from FindGeneralScriptSupport import *

usageHelp = \
r"""
TEMPLATEs

"""

class RandomFailureSummary:

  def __init__(self, buildName, testName, testHistoryUrl, sha1Pair):
    self.buildName = buildName
    self.testName = testName
    self.testHistoryUrl = testHistoryUrl
    self.sha1Pair = sha1Pair


# The main function
def main():

  args = getCmndLineArgs()

  cdashProjectTestingDayStartTime = "00:00"
  # TODO: This should be moved outside in a project specific
  # driver script or command line input
  cdashSiteUrl = args.cdash_site_url
  cdashProjectName = args.cdash_project_name
  date = args.reference_date
  groupName = args.group_name
  daysOfHistory = args.days_of_history
  printUrlMode = args.print_url_mode

  randomFailureSummaries = []

  cdashInitialNonpassedTestsFilters = \
    "filtercount=2&showfilters=1&filtercombine=and"+\
    "&field1=status&compare1=63&value1=Failed"+\
    "&field2=groupname&compare2=63&value2=Pull%20Request"
  # TODO: This cdashNonpassedTestsFilters should be moved outside
  # and into a project-specific driver script or taken as a
  # command line input.

  # A) Set up date range and directories

  # Construct date range for queryTests filter string
  referenceDateDT = CDQAR.convertInputDateArgToYYYYMMDD(
    cdashProjectTestingDayStartTime, date)
  dateRangeStart, dateRangeEnd = getDateRangeTuple(referenceDateDT, daysOfHistory)
  dateUrlField = "begin="+dateRangeStart+"&end="+dateRangeEnd
  
  print("\n dateRangeBeginStr: "+dateRangeStart+" dateRangeEndStr: "+dateRangeEnd)

  cdashQueriesCacheDir = os.getcwd()+"/test_queries_cache"
  testHistoryCacheDir  = cdashQueriesCacheDir+"/test_history_cache"
  createDirsFromPath(cdashQueriesCacheDir)
  createDirsFromPath(testHistoryCacheDir)

  # Construct queryTest.php filter for a date range
  initialNonpassingTestQueryFilters = \
    dateUrlField+"&"+cdashInitialNonpassedTestsFilters

  # B.1) Get all failing test result for past daysOfHistory

  print("\nGetting list of nonpassing tests from CDash ...")

  initialNonpassingTestsQueryUrl = CDQAR.getCDashQueryTestsQueryUrl(
    cdashSiteUrl, cdashProjectName, None, initialNonpassingTestQueryFilters)

  if printUrlMode == 'initial' or printUrlMode == 'all':
    initialNonpassingTestBrowserUrl = CDQAR.getCDashQueryTestsBrowserUrl(
      cdashSiteUrl, cdashProjectName, None, initialNonpassingTestQueryFilters)
    print("\nCDash nonpassing tests browser URL:\n\n"+\
      "  "+initialNonpassingTestBrowserUrl+"\n")
    print("\nCDash nonpassing tests query URL:\n\n"+\
      "  "+initialNonpassingTestsQueryUrl+"\n")

  initialNonpassingTestsQueryCacheFile = \
    cdashQueriesCacheDir+"/initialCDashNonPassingTests_"+dateRangeStart+"_"+dateRangeEnd+".json"

  # List of dictionaries containing the cdash results in rows
  initialNonpassingTestsLOD = CDQAR.downloadTestsOffCDashQueryTestsAndFlatten(
    initialNonpassingTestsQueryUrl, initialNonpassingTestsQueryCacheFile,\
    alwaysUseCacheFileIfExists=True)

  # B.2) Get each nonpassing test's testing history
  for nonpassingTest in initialNonpassingTestsLOD:

    # Remove unique jenkins run ID from build name
    correctedBuildName = nonpassingTest['buildName'].rsplit('-', 1)[0]
    # NOTE: This is project specific code. As Ross pointed out, buildName
    # contains a lot of Trilinos specific prefix and suffix that should
    # be processed by a Strategy class to be more project agnostic.

    buildNameMax = 80
    shortenedBuildName = correctedBuildName[:buildNameMax]

    print("\n Getting history from "+dateRangeStart+" to "+dateRangeEnd+" for\n"+\
          "  Test name: "+nonpassingTest['testname']+"\n"+\
          "  Build name: "+correctedBuildName)

    groupNameNormUrl, = CDQAR.normalizeUrlStrings(groupName)

    cdashTestHistoryFilters = \
      "filtercount=3&showfilters=1&filtercombine=and"+\
      "&field1=testname&compare1=63&value1="+nonpassingTest['testname']+\
      "&field2=groupname&compare2=63&value2="+groupNameNormUrl+\
      "&field3=buildname&compare3=63&value3="+correctedBuildName

    testHistoryQueryFilters = dateUrlField+"&"+cdashTestHistoryFilters

    cdashTestHistoryCacheFile = testHistoryCacheDir+"/"+nonpassingTest['testname']+"_"+shortenedBuildName+".json"
    print("\n  Creating file to write test history:\n   "+cdashTestHistoryCacheFile)

    testHistoryQueryUrl = CDQAR.getCDashQueryTestsQueryUrl(
      cdashSiteUrl, cdashProjectName, None, testHistoryQueryFilters)
    testHistoryBrowserUrl = CDQAR.getCDashQueryTestsBrowserUrl(
      cdashSiteUrl, cdashProjectName, None, testHistoryQueryFilters)

    testHistoryLOD = CDQAR.downloadTestsOffCDashQueryTestsAndFlatten(
      testHistoryQueryUrl, cdashTestHistoryCacheFile, alwaysUseCacheFileIfExists=True)

    print("\n  Size of test history: "+str(len(testHistoryLOD)))

    if printUrlMode == 'all':
      print("\n  CDash test history browser URL for "+nonpassingTest['testname']+" "+\
        correctedBuildName+":\n\n"+"   "+testHistoryBrowserUrl)
      print("\n  CDash test history query URL for "+nonpassingTest['testname']+" "+\
        correctedBuildName+":\n\n"+"   "+testHistoryQueryUrl)

    if len(testHistoryLOD) < 2:
      print("\n  Size of test history too small for any comparisons, skipping ...\n")
      continue

    # B.3) Split full testing history to passed and nonpassed lists of dicts
    passingTestHistoryLOD = [test for test in testHistoryLOD if test.get("status") == "Passed"]
    nonpassingTestHistoryLOD = [test for test in testHistoryLOD if test.get("status") == "Failed"]
    nonpassingSha1Pairs = set()

    print("\n  Num of passing tests in test history: "+str(len(passingTestHistoryLOD)))
    print("\n  Num of nonpassing tests in test history: "+str(len(nonpassingTestHistoryLOD)))

    buildSummaryCacheDir = cdashQueriesCacheDir+"/build_summary_cache/"+nonpassingTest['testname']+"_"+shortenedBuildName
    createDirsFromPath(buildSummaryCacheDir)
    # NOTE: There is an argumåent to be made that test histories should get their own directory
    # instead of build summaries and that build summaries should live inside of there

    # C.1) Get all nonpassing tests' sha1s into a set
    for test in nonpassingTestHistoryLOD:

      buildId = getBuildIdFromTest(test)

      buildSummaryCacheFile = buildSummaryCacheDir+"/"+buildId
      buildSummaryQueryUrl = CDQAR.getCDashBuildSummaryQueryUrl(cdashSiteUrl, buildId)
      buildConfigOutput = downloadBuildSummaryOffCDash(
        buildSummaryQueryUrl, buildSummaryCacheFile, verbose=printUrlMode =='all',
        alwaysUseCacheFileIfExists=True)['configure']['output']

      nonpassingSha1Pairs.add(getTopicTargetSha1s(buildConfigOutput))

    print("\n  Test history failing sha1s: "+str(nonpassingSha1Pairs))

    # C.2) Check if passing tests' sha1s exist in nonpassing sha1s set
    for test in passingTestHistoryLOD:

      buildId = getBuildIdFromTest(test)

      buildSummaryCacheFile = buildSummaryCacheDir+"/"+buildId
      buildSummaryQueryUrl = CDQAR.getCDashBuildSummaryQueryUrl(cdashSiteUrl, buildId)
      buildConfigOutput = downloadBuildSummaryOffCDash(
        buildSummaryQueryUrl, buildSummaryCacheFile, verbose=printUrlMode =='all',
        alwaysUseCacheFileIfExists=True)['configure']['output']

      passingSha1Pair = getTopicTargetSha1s(buildConfigOutput)

      if checkIfTestUnstable(passingSha1Pair, nonpassingSha1Pairs):
        print("\n  Found passing sha1 pair, " + str(passingSha1Pair)+\
              " in set of nonpassing sha1 pairs: \n"+str(nonpassingSha1Pairs))

        randomFailureSummaries.append(
          RandomFailureSummary(test['buildName'], test['testname'],
            testHistoryBrowserUrl, passingSha1Pair))


  print("\n*** CDash random failure analysis for " +\
    cdashProjectName+" "+groupName+" from " +dateRangeStr)

  print("Total number of initial failing tests: "+str(len(initialNonpassingTestsLOD))+"\n")

  print("Found randomly failing tests: "+str(len(randomFailureSummaries)))
  for summary in randomFailureSummaries:
    print("Test name: "+summary.testName)
    print("Build name: "+summary.buildName)
    print("Identical sha1 pairs: "+str(summary.sha1Pair))
    print("Test history browser URL: \n  "+summary.testHistoryUrl+"\n")


def getCmndLineArgs():
  parser = argparse.ArgumentParser("Arguments for cdash_analyze_and_report_random_failures.py")
  parser.add_argument("--cdash-site-url", default="", required=True)
  parser.add_argument("--cdash-project-name", default="", required=True)
  parser.add_argument("--reference-date", default="yesterday")
  parser.add_argument("--group-name", default="Pull Request")
  parser.add_argument("--days-of-history", default=1, type=int)
  parser.add_argument("--print-url-mode", choices=['none','initial','all'], default='none')

  return parser.parse_args()



def getDateRangeTuple(referenceDateTime, dayTimeDelta):
  beginDateTime = referenceDateTime - datetime.timedelta(days=(dayTimeDelta-1))
  beginDateTimeStr = CBTD.getDateStrFromDateTime(beginDateTime)
  endDateTimeStr = CBTD.getDateStrFromDateTime(referenceDateTime)
  return (beginDateTimeStr, endDateTimeStr)


def getTopicTargetSha1s(buildConfigOutput):
    pattern = r"Parent [12]:\n\s+(\w+)"
    matchedList = regex.findall(pattern, buildConfigOutput)

    if len(matchedList) != 2: return None
    return tuple(matchedList)


def getBuildIdFromTest(test):
  return test['buildSummaryLink'].split("/")[-1]


def downloadBuildSummaryOffCDash(
    cdashBuildSummaryQueryUrl, buildSummaryCacheFile=None,
    useCachedCDashData=False, alwaysUseCacheFileIfExists=False,
    verbose='False'
  ):
  verbose = verbose == 'all'
  buildSummaryJson = CDQAR.getAndCacheCDashQueryDataOrReadFromCache(
      cdashBuildSummaryQueryUrl, buildSummaryCacheFile, useCachedCDashData,
      alwaysUseCacheFileIfExists, verbose)
  return buildSummaryJson


# Check if passing test's SHA1 is in set of failed test SHA1s
def checkIfTestUnstable(passingSha1Pair, nonpassingSha1Pairs):
  return passingSha1Pair in nonpassingSha1Pairs

#
# Execute main if this is being run as a script
#

if __name__ == '__main__':
  sys.exit(main())

