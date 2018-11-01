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
import CDashQueryAnalizeReport as CDQAR
from gitdist import addOptionParserChoiceOption

#
# Help message
#


usageHelp = r"""analyze_and_report_cdash_results.py [options]

This script takes in CDash URL information as command-line arguments and then
analyzes it to look for missing expected and various types of failures and
then reports the findings as an HTML file written to disk and/or as an HTML
formatted email to one or more email addresses.

If all of the expected builds are found (and all of them have test results)
and there are no other failures found, then the script returns 0.  Otherwise
the script returns non-zero.

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
    "--limit-test-history-days", dest="test_history_days", default=30,
    help="Number of days to go back in history for each test" )
    # ToDo: Rename test_history_days to limitTestHistoryDays

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

  addOptionParserChoiceOption(
    "--use-cached-cdash-data", "useCachedCDashDataStr",
    ("on", "off"), 1,
    "Use data downloaded from CDash already cached.",
    clp )

  clp.add_option(
    "--limit-table-rows", dest="limitTableRows", type="int",
    default=10,
    help="Limit to the number of table rows. (Default '10')" )

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
    CDQAR.validateYYYYMMDD(inOptions.date)

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
    "  --use-cached-cdash-data='"+inOptions.useCachedCDashDataStr+"'"+lt+\
    "  --limit-table-rows='"+str(inOptions.limitTableRows)+"'"+lt+\
    "  --write-email-to-file='"+inOptions.writeEmailToFile+"'"+lt+\
    "  --send-email-to='"+inOptions.sendEmailTo+"'"+lt+\
    "  --email-from-address='"+inOptions.emailFromAddress+"'"+lt
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

  inOptions = getCmndLineOptions()
  echoCmndLine(inOptions)

  if inOptions.useCachedCDashDataStr == "on":
    setattr(inOptions, 'useCachedCDashData', True)
  else:
    setattr(inOptions, 'useCachedCDashData', False)

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
      expectedBuildsList = \
        CDQAR.getExpectedBuildsListfromCsvFile(inOptions.expectedBuildsFile)
    else:
      expectedBuildsList = []

    # Get list of tests with issue tracker from input CSV file

    testsWithIssueTrackersListOfDicts = CDQAR.readCsvFileIntoListOfDicts(
      inOptions.testsWithIssueTrackersFile,
      [ 'site', 'buildName', 'testname', 'issue_tracker_url', 'issue_tracker' ] )

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

    buildsListOfDicts = CDQAR.downloadBuildsOffCDashAndFlatten(
      cdashIndexBuildsQueryUrl,
      inOptions.cdashQueriesCacheDir+"/fullCDashIndexBuilds.json",
      inOptions.useCachedCDashData )

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
      inOptions.cdashQueriesCacheDir+"/fullCDashNonpassingTests.json"

    nonpassingTestsListOfDicts = CDQAR.downloadTestsOffCDashQueryTestsAndFlatten(
      cdashNonpassingTestsQueryUrl, cdashNonpassingTestsQueryJsonCacheFile,
      inOptions.useCachedCDashData )

    # Get data from cdash and return in a simpler form
    all_failing_tests=CDQAR.getTestsJsonFromCdash(
      inOptions.cdashSiteUrl, inOptions.cdashProjectName,
      inOptions.cdashNonpassedTestsFilters,
      inOptions, printCDashUrl=True )

    # Add issue tracking information to the tests' data
    CDQAR.checkForIssueTracker(all_failing_tests, inOptions.testsWithIssueTrackersFile)
    
    # Split the tests into those with issue tracking and those without
    tests_without_issue_tracking, tests_with_issue_tracking = \
      CDQAR.filterDictionary(all_failing_tests, "issue_tracker")

    # ToDo: Implement!  (Replace above call to CDQAR.getTestsJsonFromCdash())

    # Split out list of nonpassing tests into those without issue trackers and
    # those with issue trackers.

    # ToDo: Implement!

    # Get list of dicts of *all* tests with issue trackers (including those
    # passing, missing, etc.)

    # ToDo: Implement!

    # Get test history of all tests with issue trackers (passing, failing,
    # not-run, and missing)

    # ToDo: Implement!
  
    # Nonpassing Tests on CDash
    htmlEmailBodyTop += \
     "<a href=\""+cdashNonpassingTestsBrowserUrl+"\">"+\
     "Nonpassing Tests on CDash</a> (num="+str(len(all_failing_tests.keys()))+")<br>\n"
  
    # End of full build and test link paragraph and start the next paragraph
    # for the summary of failures and other tables
    htmlEmailBodyTop += \
      "</p>\n\n"+\
      "<p>\n"

    #
    print("\nSearch for any missing expected builds ...\n")
    #

    missingExpectedBuildsList = CDQAR.getMissingExpectedBuildsList(
      buildsSLOD, expectedBuildsList)
    #pp.pprint(missingExpectedBuildsList)

    bmeDescr = "Missing expected builds"
    bmeAcro = "bme"
    bmeNum = len(missingExpectedBuildsList)

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
        bmeDescr,  bmeAcro, bmeColDataList, missingExpectedBuildsList,
        groupSiteBuildNameSortOrder, None )
      # NOTE: Above we don't want to limit any missing builds in this table
      # because that data is not shown on CDash and that list will never be
      # super big.

    #
    print("\nSearch for any builds with configure failures ...\n")
    #

    buildsWithConfigureFailuresList = \
      CDQAR.getFilteredList(buildsSLOD, CDQAR.buildHasConfigureFailures)

    cDescr = "Builds with configure failures"
    cAcro = "c"
    cNum = len(buildsWithConfigureFailuresList)

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
        cDescr,  cAcro, cColDataList, buildsWithConfigureFailuresList,
        groupSiteBuildNameSortOrder, inOptions.limitTableRows )

      # ToDo: Update to show number of configure failures and the history info
      # for that build with hyperlinks and don't limit the number of builds
      # shown.

    #
    print("\nSearch for any builds with compilation (build) failures ...\n")
    #

    buildsWithBuildFailuresList = \
      CDQAR.getFilteredList(buildsSLOD, CDQAR.buildHasBuildFailures)

    bDescr = "Builds with build failures"
    bAcro = "b"
    bNum = len(buildsWithBuildFailuresList)

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
        bDescr,  bAcro, cColDataList, buildsWithBuildFailuresList,
        groupSiteBuildNameSortOrder, inOptions.limitTableRows )

      # ToDo: Update to show number of builds failures and the history info
      # for that build with hyperlinks and don't limit the number of builds
      # shown.

    #
    # D.3) Analyaize and report test results in different tables
    #

    # Column header for listing tests
    testsColDataList = [
      tcd("site", "Site"),
      tcd("build_name", "Build Name"),
      tcd("test_name", "Test Name"),
      tcd("status", "Status"),
      tcd("details", "Details"),
      tcd("failures_in_last_"+str(inOptions.test_history_days)+"_days",
        "Fails last "+str(inOptions.test_history_days)+" Days",
        "right"),
      tcd("previous_failure_date", "Previous Failure Date", "right"),
      tcd("issue_tracker", "Tracker", "right"),
      ]

    # Sort order for tests
    testnameBuildnameSiteSortOrder = ['test_name', 'build_name', 'site']

    #
    print("\nSearch failing tests without issue trackers ...\n")
    #

    testsWithoutIssueTrackerList = getFlatListOfTestsFromTestDict(
      tests_without_issue_tracking)
    #pp.pprint(testsWithoutIssueTrackerList)

    # Sort and get detailed history of CDash for the top <N> 'twoif' tests
    # *without* issue trackers that are failing (and not-run for now)

    # ToDo: Implement!

    twoifDescr = "Failing tests without issue trackers"
    twoifAcro = "twoif"
    twoifNum = len(testsWithoutIssueTrackerList)

    twoifSummaryStr = \
      CDQAR.getCDashDataSummaryHtmlTableTitleStr(twoifDescr,  twoifAcro, twoifNum)

    print(twoifSummaryStr)

    if twoifNum > 0:

      globalPass = False

      summaryLineDataNumbersList.append(twoifAcro+"="+str(twoifNum))

      htmlEmailBodyTop += CDQAR.makeHtmlTextRed(twoifSummaryStr)+"<br>\n"

      htmlEmailBodyBottom += CDQAR.createCDashDataSummaryHtmlTableStr(
        twoifDescr,  twoifAcro, testsColDataList, testsWithoutIssueTrackerList,
        testnameBuildnameSiteSortOrder, inOptions.limitTableRows )

    #
    print("\nSearch failing tests with issue trackers ...\n")
    #

    testsWithIssueTrackerList = getFlatListOfTestsFromTestDict(
      tests_with_issue_tracking)
    #pp.pprint(testsWithIssueTrackerList)

    # Sort and get detailed test history for all 'twif' failing tests with
    # issue trackers.

    # ToDo: Implement!

    twifDescr = "Failing tests with issue trackers"
    twifAcro = "twif"
    twifNum = len(testsWithIssueTrackerList)

    twifSummaryStr = \
      CDQAR.getCDashDataSummaryHtmlTableTitleStr(twifDescr,  twifAcro, twifNum)

    print(twifSummaryStr)

    if twifNum > 0:

      globalPass = False

      summaryLineDataNumbersList.append(twifAcro+"="+str(twifNum))

      htmlEmailBodyTop += twifSummaryStr+"<br>\n"

      htmlEmailBodyBottom += CDQAR.createCDashDataSummaryHtmlTableStr(
        twifDescr,  twifAcro, testsColDataList, testsWithIssueTrackerList,
        testnameBuildnameSiteSortOrder)
      # NOTE: We don't limit the number of tests tracked tests listed because
      # we will never have a huge number of failing tests with issue trackers.

    # Generate table "Tests without issue trackers not run: twoinr=???"
    # (sorted and limited to the top <N> items).

    # ToDo: Implement!

    # Generate table "Tests with issue trackers not run: twinr=???"

    # ToDo: Implement!

    # Generate table "Tests with issue trackers missing: twim=???"

    # ToDo: Implement!

    # Generate table "Tests with issue trackers currently passing: twip=???"

    # ToDo: Implement!
 
  except Exception:
    # Traceback!
    sys.stdout.flush()
    traceback.print_exc()
    # Reporte the error
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
  
