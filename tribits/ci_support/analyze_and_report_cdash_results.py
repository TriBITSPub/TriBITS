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
  
  clp.add_option(
    "--date", dest="date", type="string", default="",
    help="Date for the testing day <YYYY-MM-DD>. (Default '')" )
  
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
    "--write-email-to-file", dest="writeEmailToFile", type="string", default="",
    help="Write the body of the HTML email this file. (Default '')" )


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
    "  --write-email-to-file='"+inOptions.writeEmailToFile+"'"+lt
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

  print "***"
  print "*** Check for pass/fail of "+inOptions.buildSetName+" for "+inOptions.date
  print "***"

  htmlEmailBody = \
   "<p><b>Build and Test results for "+inOptions.buildSetName \
      +" on "+inOptions.date+"</b></p>\n\n"

  htmlEmailBody += "<p>\n"

  cdashIndexBuildsBrowserUrl = CDQAR.getCDashIndexBrowserUrl(
    inOptions.cdashSiteUrl, inOptions.cdashProjectName, inOptions.date,
    inOptions.cdashBuildsFilters)
  htmlEmailBody += \
   "<a href=\""+cdashIndexBuildsBrowserUrl+"\">Builds on CDash</a><br>\n"

  cdashNonpassingTestsBrowserUrl = CDQAR.getCDashQueryTestsBrowserUrl(
    inOptions.cdashSiteUrl, inOptions.cdashProjectName, inOptions.date,
    inOptions.cdashNonpassedTestsFilters)
  htmlEmailBody += \
   "<a href=\""+cdashNonpassingTestsBrowserUrl+"\">Nonpassing Tests on CDash</a><br>\n"

  htmlEmailBody += "</p>\n"

  projectExpectedBuilds=[]
  # ToDo: Read this in from inOptions.expectedBuildsFile!

  # ToDo: Write out the date the the cache dir so that it can be read back in
  # to check the cache.

  allBuildsPass = True

  print "\n*** Check the "+inOptions.cdashProjectName+" project builds ...\n"
  (projectBuildsPass, errMsg) = \
      CDQAR.queryCDashAndDeterminePassFail(
       inOptions.cdashSiteUrl,
       inOptions.cdashProjectName,
       inOptions.date,
       inOptions.cdashBuildsFilters,
       projectExpectedBuilds,
       cdashQueriesCacheDir=inOptions.cdashQueriesCacheDir,
       useCachedCDashData=useCachedCDashData,
       )
  if not projectBuildsPass:
    print "\nTrilinos builds failed!\n"
    allBuildsPass = False
    print errMsg
  else:
    print "\nTrilinos builds passed!\n"
  

  if inOptions.writeEmailToFile:
    open(inOptions.writeEmailToFile, 'w').write(htmlEmailBody)

  print "\n*** Determine overall pass/fail ...\n"
  
  if allBuildsPass:
    print "FINAL: The Trilinos builds on "+inOptions.date+" PASSED"
    sys.exit(0)
  else:
    print "FINAL: One or more of the Trilinos builds on "+inOptions.date+" FAILED"
    sys.exit(2)
