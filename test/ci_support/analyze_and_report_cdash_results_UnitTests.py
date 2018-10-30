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

import os
import sys
import re
import copy
import shutil
import unittest
import pprint

from FindCISupportDir import *
from CDashQueryAnalizeReport import *

g_testBaseDir = getScriptBaseDir()

tribitsBaseDir=os.path.abspath(g_testBaseDir+"/../../tribits")
mockProjectBaseDir=os.path.abspath(tribitsBaseDir+"/examples/MockTrilinos")

g_pp = pprint.PrettyPrinter(indent=4)


#
# Some helper function
# 


# Helper script for creating test directories (in CWD)
def deleteThenCreateTestDir(testDir):
  baseTestDir="analyze_and_report_cdash_results"
  if not os.path.exists(baseTestDir): os.mkdir(baseTestDir)
  testSubdir = baseTestDir+"/"+testDir
  if os.path.exists(testSubdir): shutil.rmtree(testSubdir)
  os.mkdir(testSubdir)
  return testSubdir


# Search for a list of regexs in order in a list of strings
def assertFindStringInListOfStrings(
  testObj,
  stringToFind,
  stringsList,
  stringsListName,
  ):
  foundStringToFind = False
  for stdoutLine in stringsList:
    if stdoutLine.find(stringToFind) != -1:
      foundStringToFind = True
      break
  testObj.assertTrue(foundStringToFind,
    "Error, could not find string '"+stringToFind+"' in "+stringsListName+"!")


# Search for a list of regexs in order in a list of strings
def assertListOfRegexsFoundInLinstOfStrs(
  testObj,
  regexList,
  stringsList,
  stringsListName,
  ):
  # Set up for first regex
  current_regex_idx = 0
  currentRe = re.compile(regexList[current_regex_idx])
  # Loop over the lines in the input strings list and look for the regexes in
  # order!
  strLine_idx = -1
  for strLine in stringsList:
    strLine_idx += 1
    if current_regex_idx == len(regexList):
      # Found all the regexes so we are done!
      break
    #print("\nstrLine_idx = '"+str(strLine_idx)+"'")
    #print("strLine = '"+strLine+"'")
    #print("regexList["+str(current_regex_idx)+"] = '"+regexList[current_regex_idx]+"'")
    if currentRe.match(strLine):
      # Found the current regex being looked for!
      #print("Found match!")
      current_regex_idx += 1
      if current_regex_idx < len(regexList):
        currentRe = re.compile(regexList[current_regex_idx])
      continue
  # Look to see if you have found all of the regexes being searched for.  If
  # the current one has not been found, then report that you could not find
  # it!
  if current_regex_idx < len(regexList):
    testObj.assertTrue(False,
      "Error, could not find the regex '"+regexList[current_regex_idx]+"'"+\
      " in "+stringsListName+"!")



# Run a test case involving the analyze_and_report_cdash_results.py
#
# This function runs a test case involving a the script
# analyze_and_report_cdash_results.py.
#
def analyze_and_report_cdash_results_run_case(
  testObj,
  testCaseName,
  extraCmndLineOptions,
  expectedRtnCode,
  expectedSummaryLineStr,
  stdoutRegexList,
  htmlFileRegexList,
  verbose=False,
  ):

  # Location of test files
  testInputDir = testCiSupportDir+"/analyze_and_report_cdash_results/"+testCaseName

  # Clean out test output directory and move into it
  testOutputDir = deleteThenCreateTestDir(testCaseName)
  os.chdir(testOutputDir)

  # Copy the cached CDash data files
  
  buildsDataCacheFile = "fullCDashIndexBuilds.json"
  shutil.copyfile(testInputDir+"/"+buildsDataCacheFile, buildsDataCacheFile)

  testHistoryDir = "test_history"
  shutil.copytree(testInputDir+"/"+testHistoryDir, testHistoryDir)

  # Create expression commandline to run

  htmlFileName = "htmlFile.html"
  htmlFileAbsPath = os.getcwd()+"/"+htmlFileName

  cmnd = ciSupportDir+"/analyze_and_report_cdash_results.py"+\
    " --date=2001-01-01"+\
    " --cdash-project-name='ProjectName'"+\
    " --build-set-name='ProjectName Nightly Builds'"+\
    " --cdash-site-url='https://something.com/cdash'"+\
    " --cdash-builds-filters='builds_filters'"+\
    " --cdash-nonpassed-tests-filters='nonpasssing_tests_filters'"+\
    " --use-cached-cdash-data=on"+\
    " --expected-builds-file="+testInputDir+"/expectedBuilds.csv"+\
    " --issue-tracking-csv-file-name="+testInputDir+"/testsWithIssueTrackers.csv"+\
    " --write-email-to-file="+htmlFileName+\
    " "+extraCmndLineOptions

  # Run analyze_and_report_cdash_results.py
  stdoutFile = "stdout.out"
  stdoutFileAbsPath = os.getcwd()+"/"+stdoutFile
  rtnCode = echoRunSysCmnd(cmnd, throwExcept=False,
    outFile=stdoutFile, verbose=verbose)

  # Check the return code
  testObj.assertEqual(rtnCode, expectedRtnCode)

  # Read the STDOUT into a array of string so we can grep it
  with open(stdoutFile, 'r') as stdout:
    stdoutStrList = stdout.read().split("\n")

  # Look for STDOUT for expected summary line
  assertFindStringInListOfStrings(testObj, expectedSummaryLineStr,
    stdoutStrList, stdoutFileAbsPath)

  # Grep the STDOUT for other grep strings
  assertListOfRegexsFoundInLinstOfStrs(testObj, stdoutRegexList, stdoutStrList,
    stdoutFileAbsPath)

  # Release the list of strings for the STDOUT file
  stdoutStrList = None

  # Search for expected regexes and in HTML file
  with open(htmlFileName, 'r') as htmlFile:
    htmlFileStrList = htmlFile.read().split("\n")
  assertListOfRegexsFoundInLinstOfStrs(testObj, htmlFileRegexList, htmlFileStrList,
    htmlFileAbsPath)


#############################################################################
#
# System-level tests for analyze_and_report_cdash_results.py
#
#############################################################################


class test_analyze_and_report_cdash_results(unittest.TestCase):

  def test_case1(self):
    analyze_and_report_cdash_results_run_case(
      self,
      "case1",
      "",
      1,
      "FAILED (twoi=12, twi=9): ProjectName Nightly Builds on 2001-01-01",
      [
        "Missing expected builds: bme=0",
        "Builds with configure failures: c=0",
        "Builds with build failures: b=0",
        "Failing tests without issue tracker: twoi=12",
        "Failing tests with issue tracker: twi=9",
        ],
      [
        "<h2>Build and Test results for ProjectName Nightly Builds on 2001-01-01</h2>",

        "<a href=\"https://something[.]com/cdash/index[.]php[?]project=ProjectName&date=2001-01-01&builds_filters\">Builds on CDash</a> [(]num=6[)]<br>",
        "<a href=\"https://something[.]com/cdash/queryTests[.]php[?]project=ProjectName&date=2001-01-01&nonpasssing_tests_filters\">Nonpassing Tests on CDash</a> [(]num=21[)]<br>",

        "<font color=\"red\">Failing tests without issue tracker: twoi=12</font><br>",
        "Failing tests with issue tracker: twi=9<br>",
        
        "<h3>Failing tests without issue tracker [(]limited to 10[)]: twoi=12</h3>",

        # Pin down the first row of this table
        "<td align=\"left\"><a href=\"https://something[.]com/cdash/index[.]php[?]project=ProjectName&filtercombine=and&filtercombine=&filtercount=4&showfilters=1&filtercombine=and&field1=buildname&compare1=61&value1=Trilinos-atdm-mutrino-intel-opt-openmp-KNL&field2=site&compare2=61&value2=mutrino&field3=buildstarttime&compare3=84&value3=2001-01-02T00:00:00&field4=buildstarttime&compare4=83&value4=2000-12-03T00:00:00\">Trilinos-atdm-mutrino-intel-opt-openmp-KNL</a></td>",
        "<td align=\"left\"><a href=\"https://testing[.]sandia[.]gov/cdash/testDetails[.]php[?]test=57860629&build=4107240\">Anasazi_Epetra_BKS_norestart_test_MPI_4</a></td>",
        "<td align=\"left\"><a href=\"https://testing[.]sandia[.]gov/cdash/testDetails[.]php[?]test=57860629&build=4107240\">Failed</a></td>",
        "<td align=\"left\">Completed [(]Failed[)]</td>",
        "<td align=\"right\"><a href=\"https://something[.]com/cdash/queryTests[.]php[?]project=ProjectName&filtercombine=and&filtercombine=&filtercount=5&showfilters=1&filtercombine=and&field1=buildname&compare1=61&value1=Trilinos-atdm-mutrino-intel-opt-openmp-KNL&field2=testname&compare2=61&value2=Anasazi_Epetra_BKS_norestart_test_MPI_4&field3=site&compare3=61&value3=mutrino&field4=buildstarttime&compare4=84&value4=2001-01-02T00:00:00&field5=buildstarttime&compare5=83&value5=2000-12-03T00:00:00\">30</a></td>",
        "<td align=\"right\">2018-10-27</td>",
        "<td align=\"right\"></td>",

        "<td align=\"left\"><a href=\"https://testing[.]sandia[.]gov/cdash/testDetails[.]php[?]test=57860535&build=4107241\">Belos_gcrodr_hb_MPI_4</a></td>",

        "<h3>Failing tests with issue tracker: twi=9</h3>",

        "<td align=\"left\"><a href=\"https://something[.]com/cdash/index[.]php[?]project=ProjectName&filtercombine=and&filtercombine=&filtercount=4&showfilters=1&filtercombine=and&field1=buildname&compare1=61&value1=Trilinos-atdm-cee-rhel6-clang-opt-serial&field2=site&compare2=61&value2=cee-rhel6&field3=buildstarttime&compare3=84&value3=2001-01-02T00:00:00&field4=buildstarttime&compare4=83&value4=2000-12-03T00:00:00\">Trilinos-atdm-cee-rhel6-clang-opt-serial</a></td>"
        ],
      #verbose=True,
      )
  # NOTE: The above unit test checks several parts of the HTML output that
  # other tests will not check.  Ths is done to really pin things down the
  # with this first unit test.


#
# Run the unit tests!
#

if __name__ == '__main__':

  unittest.main()
