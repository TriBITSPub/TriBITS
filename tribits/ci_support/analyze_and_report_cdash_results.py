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

print sys.version_info
if sys.version_info < (2,7,9):
  raise Exception("Error: Must be using Python 2.7.9 or newer")
# NOTE: If we use Python 2.6.6. then the urllib2 function crashes!

from FindGeneralScriptSupport import *
from GeneralScriptSupport import *
import CDashQueryAnalizeReport as CDQAR
from gitdist import addOptionParserChoiceOption

#
# Help message
#

# This part can be reused in other scripts that are project-specific
genericUsageHelp = \
r"""
ToDo: Finish documentation!
"""


usageHelp = r"""analyze_and_report_cdash_results.py [options]

ToDo: Finish documentation!

""" + \
genericUsageHelp


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
    "--expected-builds-file", dest="expectedBuildsFile", type="string",
    default="",
    help="Path to CSV file that lists the expected builds. (Default '')" )

  cdashQueriesCacheDir_default=os.getcwd()

  clp.add_option(
    "--cdash-queries-cache-dir", dest="cdashQueriesCacheDir", type="string",
    default=cdashQueriesCacheDir_default,
    help="Cache CDash query data this directory" \
      +" (default ='"+cdashQueriesCacheDir_default+"')." )

  addOptionParserChoiceOption(
    "--use-cached-cdash-data", "useCachedCDashData",
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
    "  --cdash-site-url='"+inOptions.cdashSiteUrl+"'"+lt+\
    "  --cdash-builds-filters='"+inOptions.cdashBuildsFilters+"'"+lt+\
    "  --cdash-nonpassed-tests-filters='"+inOptions.cdashNonpassedTestsFilters+"'"+lt+\
    "  --expected-builds-file='"+inOptions.expectedBuildsFile+"'"+lt +\
    "  --cdash-queries-cache-dir='"+inOptions.cdashQueriesCacheDir+"'"+lt+\
    "  --use-cached-cdash-data='"+inOptions.useCachedCDashData+"'"+lt+\
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


#
# Run the script
#

if __name__ == '__main__':

  inOptions = getCmndLineOptions()
  echoCmndLine(inOptions)

  if inOptions.useCachedCDashData == "on":
    useCachedCDashData=True
  else:
    useCachedCDashData=False

  #
  # Common data, etc.
  #

  tcd = CDQAR.TableColumnData
  pp = pprint.PrettyPrinter(indent=2)


  groupSiteBuildNameSortOrder = ['group', 'site', 'buildname']

  #
  # Sound off
  #

  print "***"
  print "*** Query and analyze CDash results "+inOptions.buildSetName+\
        " for testing day "+inOptions.date
  print "***"

  # ToDo: Write out the date and the query strings data to a cache file and
  # then check it to make sure that the arguments are the same when checking
  # the cache.

  #
  # A) Create beginning of email body (that does not require getting any data off CDash)
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
  # B) Get data off of CDash, do analysis, and construct HTML body parts
  #
  
  globalPass = True

  try:

    #
    # B.1) Get build and test data off of CDash and analize
    #

    #
    # B.1.a) Get list of builds of CDash
    #

    cdashIndexBuildsBrowserUrl = CDQAR.getCDashIndexBrowserUrl(
      inOptions.cdashSiteUrl, inOptions.cdashProjectName, inOptions.date,
      inOptions.cdashBuildsFilters)

    print("\nCDash builds browser URL:\n\n  "+cdashIndexBuildsBrowserUrl+"\n")
   
    buildsSummaryList = \
      CDQAR.downloadBuildsOffCDashAndSummarize(
       # CDash URL Args
       inOptions.cdashSiteUrl,
       inOptions.cdashProjectName,
       inOptions.date,
       inOptions.cdashBuildsFilters,
       # Other args
       useCachedCDashData=useCachedCDashData,
       cdashQueriesCacheDir=inOptions.cdashQueriesCacheDir,
       )

    # Beginning of top full bulid and tests CDash links paragraph 
    htmlEmailBodyTop += "<p>\n"
  
    # Builds on CDash
    htmlEmailBodyTop += \
     "<a href=\""+cdashIndexBuildsBrowserUrl+"\">"+\
     "Builds on CDash</a> (num="+str(len(buildsSummaryList))+")<br>\n"

    # Get a dict to help look up builds
    buildLookupDict = CDQAR.createBuildLookupDict(buildsSummaryList)

    #
    # B.1.b) Get list of non-passing tests of CDash
    #
    cdashNonpassingTestsBrowserUrl = CDQAR.getCDashQueryTestsBrowserUrl(
      inOptions.cdashSiteUrl, inOptions.cdashProjectName, inOptions.date,
      inOptions.cdashNonpassedTestsFilters)

    # ToDo: Get list non-passing tests from CDash
  
    # Nonpassing Tests on CDash
    htmlEmailBodyTop += \
     "<a href=\""+cdashNonpassingTestsBrowserUrl+"\">"+\
     "Nonpassing Tests on CDash</a> (num=???)<br>\n"
  
    # End of full build and test link paragraph 
    htmlEmailBodyTop += "</p>\n"

    #
    print("\nSearch for any missing expected builds ...\n")
    #

    expectedBuildsList = \
      CDQAR.getExpectedBuildsListfromCsvFile(inOptions.expectedBuildsFile)

    missingExpectedBuildsList = CDQAR.getMissingExpectedBuildsList(
      buildLookupDict, expectedBuildsList)
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

      htmlEmailBodyTop += CDQAR.makeHtmlTextRed(bmeSummaryStr)+"<br>"

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
      # because that data is not shown on CDash and that list will never bo
      # super big.

    #
    print("\nSearch for any builds with configure failures ...\n")
    #

    buildsWithConfigureFailuresList = CDQAR.getBuildsWtihConfigureFailures(
      buildsSummaryList)

    cDescr = "Builds with configure failures"
    cAcro = "c"
    cNum = len(buildsWithConfigureFailuresList)

    cSummaryStr = \
      CDQAR.getCDashDataSummaryHtmlTableTitleStr(cDescr,  cAcro, cNum)

    print(cSummaryStr)

    if cNum > 0:

      globalPass = False

      summaryLineDataNumbersList.append(cAcro+"="+str(cNum))

      htmlEmailBodyTop += CDQAR.makeHtmlTextRed(cSummaryStr)+"<br>"

      cColDataList = [
        tcd('group', "Group"),
        tcd('site', "Site"),
        tcd('buildname', "Build Name"),
        ]

      htmlEmailBodyBottom += CDQAR.createCDashDataSummaryHtmlTableStr(
        cDescr,  cAcro, cColDataList, buildsWithConfigureFailuresList,
        groupSiteBuildNameSortOrder, inOptions.limitTableRows )

      # ToDo: Update to show number of configure failures with hyperlinks and
      # don't limit the number of builds shown.

    #
    print("\nSearch for any builds with compilation (build) failures ...\n")
    #

    buildsWithBuildFailuresList = CDQAR.getBuildsWtihBuildFailures(
      buildsSummaryList)

    bDescr = "Builds with build failures"
    bAcro = "b"
    bNum = len(buildsWithBuildFailuresList)

    bSummaryStr = \
      CDQAR.getCDashDataSummaryHtmlTableTitleStr(bDescr,  bAcro, bNum)

    print(bSummaryStr)

    if bNum > 0:

      globalPass = False

      summaryLineDataNumbersList.append(bAcro+"="+str(bNum))

      htmlEmailBodyTop += CDQAR.makeHtmlTextRed(bSummaryStr)+"<br>"

      cColDataList = [
        tcd('group', "Group"),
        tcd('site', "Site"),
        tcd('buildname', "Build Name"),
        ]

      htmlEmailBodyBottom += CDQAR.createCDashDataSummaryHtmlTableStr(
        bDescr,  bAcro, cColDataList, buildsWithBuildFailuresList,
        groupSiteBuildNameSortOrder, inOptions.limitTableRows )

      # ToDo: Update to show number of build failures with hyperlinks and
      # don't limit the number of builds shown.

    #
    # B.2) Get the test results data and analyze
    #

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
  # C) Put together final email summary  line
  #

  if globalPass:
    summaryLine = "PASSED"
  else:
    summaryLine = "FAILED"

  if summaryLineDataNumbersList:
    summaryLine += " (" + ", ".join(summaryLineDataNumbersList) + ")"

  summaryLine += ": "+inOptions.buildSetName+" on "+inOptions.date

  #
  # D) Write and send the email
  #

  htmlEmaiBody = htmlEmailBodyTop + "\n\n" + htmlEmailBodyBottom

  if inOptions.writeEmailToFile:
    print("\nWriting HTML file '"+inOptions.writeEmailToFile+"' ...")
    htmlEmaiBodyFileStr = \
      "<h2>"+summaryLine+"</h2>\n\n"+\
      htmlEmaiBody
    with open(inOptions.writeEmailToFile, 'w') as outFile:
      outFile.write(htmlEmaiBodyFileStr)

  if inOptions.sendEmailTo:
    for emailAddress in inOptions.sendEmailTo.split(','):
      emailAddress = emailAddress.strip()
      print("\nSending email to '"+emailAddress+"' ...")
      msg=CDQAR.createHtmlMimeEmail(
        inOptions.emailFromAddress, emailAddress, summaryLine, "", htmlEmaiBody)
      CDQAR.sendMineEmail(msg)

  #
  # E) Return final global pass/fail
  #

  print("\n"+summaryLine+"\n")

  if globalPass:
    sys.exit(0)
  else:
    sys.exit(2)
  
