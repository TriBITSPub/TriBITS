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
import CDashQueryAnalizeReport as CDQAR

g_testBaseDir = CDQAR.getScriptBaseDir()

tribitsBaseDir=os.path.abspath(g_testBaseDir+"/../../tribits")
mockProjectBaseDir=os.path.abspath(tribitsBaseDir+"/examples/MockTrilinos")

g_pp = pprint.PrettyPrinter(indent=4)


#
# Some helper functions
# 


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
  debugPrint=False,
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
    if debugPrint:
      print("\nstrLine_idx = '"+str(strLine_idx)+"'")
      print("strLine = '"+strLine+"'")
      print("regexList["+str(current_regex_idx)+"] = '"+regexList[current_regex_idx]+"'")
    if currentRe.match(strLine):
      # Found the current regex being looked for!
      if debugPrint:
        print("Found match!")
      current_regex_idx += 1
      if current_regex_idx < len(regexList):
        if debugPrint:
          print("regexList["+str(current_regex_idx)+"] = '"+regexList[current_regex_idx]+"'")
        currentRe = re.compile(regexList[current_regex_idx])
      continue
  # Look to see if you have found all of the regexes being searched for.  If
  # the current one has not been found, then report that you could not find
  # it!
  if current_regex_idx < len(regexList):
    testObj.assertTrue(False,
      "Error, could not find the regex '"+regexList[current_regex_idx]+"'"+\
      " in "+stringsListName+"!")


# Base test directory in the build tree
g_baseTestDir="analyze_and_report_cdash_results"


# Set up the test case directory and copy starter files into it
#
# These files can then be modified in order to define other test cases.
#
def analyze_and_report_cdash_results_setup_test_dir(
  testCaseName,
  buildSetName="ProjectName Nightly Builds",
  copyFrom="raw_cdash_data_twoif_12_twif_9",
  ):
  testInputDir = testCiSupportDir+"/"+g_baseTestDir+"/"+copyFrom
  testOutputDir = g_baseTestDir+"/"+testCaseName
  shutil.copytree(testInputDir, testOutputDir)
  baseFilePrefix = CDQAR.getFileNameStrFromText(buildSetName)
  filesToRename = [ "fullCDashIndexBuilds.json", "fullCDashNonpassingTests.json" ]
  for fileToRename in filesToRename:
    oldName = testOutputDir+"/"+fileToRename
    newName = testOutputDir+"/"+baseFilePrefix+fileToRename
    os.rename(oldName, newName)
  return testOutputDir


# Run a test case involving the analyze_and_report_cdash_results.py
#
# This function runs a test case involving a the script
# analyze_and_report_cdash_results.py.
#
def analyze_and_report_cdash_results_run_case(
  testObj,
  testCaseName,
  extraCmndLineOptionsList,
  expectedRtnCode,
  expectedSummaryLineStr,
  stdoutRegexList,
  htmlFileRegexList,
  verbose=False,
  debugPrint=False,
  ):

  # Change into test directory
  pwdDir = os.getcwd()
  testOutputDir = g_baseTestDir+"/"+testCaseName
  os.chdir(testOutputDir)

  try:

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
      " --expected-builds-file=expectedBuilds.csv"+\
      " --tests-with-issue-trackers-file=testsWithIssueTrackers.csv"+\
      " --write-email-to-file="+htmlFileName+\
      " --use-new-test-code"+\
      " "+" ".join(extraCmndLineOptionsList)
  
    # Run analyze_and_report_cdash_results.py
    stdoutFile = "stdout.out"
    stdoutFileAbsPath = os.getcwd()+"/"+stdoutFile
    rtnCode = CDQAR.echoRunSysCmnd(cmnd, throwExcept=False,
      outFile=stdoutFile, verbose=verbose)
  
    # Check the return code
    testObj.assertEqual(rtnCode, expectedRtnCode)
  
    # Read the STDOUT into a array of string so we can grep it
    with open(stdoutFile, 'r') as stdout:
      stdoutStrList = stdout.read().split("\n")
  
    # Grep the STDOUT for other grep strings
    assertListOfRegexsFoundInLinstOfStrs(testObj, stdoutRegexList,
      stdoutStrList, stdoutFileAbsPath, debugPrint=debugPrint)
  
    # Look for STDOUT for expected summary line
    assertFindStringInListOfStrings(testObj, expectedSummaryLineStr,
      stdoutStrList, stdoutFileAbsPath)
    # NOTE: We search for this last in STDOUT so that we can match the
    # individual parts first.
  
    # Release the list of strings for the STDOUT file
    stdoutStrList = None
  
    # Search for expected regexes and in HTML file
    with open(htmlFileName, 'r') as htmlFile:
      htmlFileStrList = htmlFile.read().split("\n")
    assertListOfRegexsFoundInLinstOfStrs(testObj, htmlFileRegexList,
      htmlFileStrList, htmlFileAbsPath, debugPrint=debugPrint)

  finally:
    os.chdir(pwdDir)


#############################################################################
#
# System-level tests for analyze_and_report_cdash_results.py
#
#############################################################################


class test_analyze_and_report_cdash_results(unittest.TestCase):

  # Base case for raw CDash data we happened to choose
  def test_twoif_12_twif_9(self):
    testCaseName = "twoif_12_twif_9"
    analyze_and_report_cdash_results_setup_test_dir(testCaseName)
    analyze_and_report_cdash_results_run_case(
      self,
      testCaseName,
      [],
      1,
      "FAILED (twoif=12, twif=9): ProjectName Nightly Builds on 2001-01-01",
      [
        "Missing expected builds: bme=0",
        "Builds with configure failures: c=0",
        "Builds with build failures: b=0",
        "Failing tests without issue trackers: twoif=12",
        "Failing tests with issue trackers: twif=9",
        ],
      [
        # Top title
        "<h2>Build and Test results for ProjectName Nightly Builds on 2001-01-01</h2>",

        # First paragraph with with links to build and nonpassing tests results on cdsah
        "<p>",
        "<a href=\"https://something[.]com/cdash/index[.]php[?]project=ProjectName&date=2001-01-01&builds_filters\">Builds on CDash</a> [(]num=6[)]<br>",
        "<a href=\"https://something[.]com/cdash/queryTests[.]php[?]project=ProjectName&date=2001-01-01&nonpasssing_tests_filters\">Nonpassing Tests on CDash</a> [(]num=21[)]<br>",
        "</p>",

        # Second paragraph with listing of different types of tables below
        "<p>",
        "<font color=\"red\">Failing tests without issue trackers: twoif=12</font><br>",
        "Failing tests with issue trackers: twif=9<br>",
        "</p>",
         
        # twoif table
        "<h3>Failing tests without issue trackers [(]limited to 10[)]: twoif=12</h3>",
        # Pin down the first row of this table (pin down this first row
        "<tr>",
        "<td align=\"left\"><a href=\"https://something[.]com/cdash/index[.]php[?]project=ProjectName&filtercombine=and&filtercombine=&filtercount=4&showfilters=1&filtercombine=and&field1=buildname&compare1=61&value1=Trilinos-atdm-mutrino-intel-opt-openmp-KNL&field2=site&compare2=61&value2=mutrino&field3=buildstarttime&compare3=84&value3=2001-01-02T00:00:00&field4=buildstarttime&compare4=83&value4=2000-12-03T00:00:00\">Trilinos-atdm-mutrino-intel-opt-openmp-KNL</a></td>",
        "<td align=\"left\"><a href=\"https://something[.]com/cdash/testDetails[.]php[?]test=57860629&build=4107240\">Anasazi_Epetra_BKS_norestart_test_MPI_4</a></td>",
        "<td align=\"left\"><a href=\"https://something[.]com/cdash/testDetails[.]php[?]test=57860629&build=4107240\">Failed</a></td>",
        "<td align=\"left\">Completed [(]Failed[)]</td>",
        "<td align=\"right\"><a href=\"https://something[.]com/cdash/queryTests[.]php[?]project=ProjectName&filtercombine=and&filtercombine=&filtercount=5&showfilters=1&filtercombine=and&field1=buildname&compare1=61&value1=Trilinos-atdm-mutrino-intel-opt-openmp-KNL&field2=testname&compare2=61&value2=Anasazi_Epetra_BKS_norestart_test_MPI_4&field3=site&compare3=61&value3=mutrino&field4=buildstarttime&compare4=84&value4=2001-01-02T00:00:00&field5=buildstarttime&compare5=83&value5=2000-12-03T00:00:00\">30</a></td>",
        "<td align=\"right\">2018-10-27</td>",
        "<td align=\"right\"></td>",
        "</tr>",
        # Second row
        "<td align=\"left\"><a href=\"https://something[.]com/cdash/testDetails[.]php[?]test=57860535&build=4107241\">Belos_gcrodr_hb_MPI_4</a></td>",

        # twif table
        "<h3>Failing tests with issue trackers: twif=9</h3>",
        "<td align=\"left\"><a href=\"https://something[.]com/cdash/index[.]php[?]project=ProjectName&filtercombine=and&filtercombine=&filtercount=4&showfilters=1&filtercombine=and&field1=buildname&compare1=61&value1=Trilinos-atdm-cee-rhel6-clang-opt-serial&field2=site&compare2=61&value2=cee-rhel6&field3=buildstarttime&compare3=84&value3=2001-01-02T00:00:00&field4=buildstarttime&compare4=83&value4=2000-12-03T00:00:00\">Trilinos-atdm-cee-rhel6-clang-opt-serial</a></td>"
        ],
      #verbose=True,
      #debugPrint=True,
      )
  # NOTE: The above unit test checks several parts of the HTML output that
  # other tests will not check.  In particular, this really pins down the
  # tables 'twoif' and 'twif'.  Other tests will not do this to avoid
  # duplication in testing.


  # Add some missing builds, some builds with configure failuires, and builds
  # with build failures
  def test_bme_2_c_1_b_2_twoif_12_twif_9(self):

    testCaseName = "bme_2_c_1_b_2_twoif_12_twif_9"
    buildSetName = "Project Specialized Builds"

    # Copy the raw files from CDash to get started
    testOutputDir = analyze_and_report_cdash_results_setup_test_dir(testCaseName,
      buildSetName)

    # Add some expected builds that don't exist
    expectedBuildsFilePath = testOutputDir+"/expectedBuilds.csv"
    with open(expectedBuildsFilePath, 'r') as expectedBuildsFile:
      expectedBuildsStrList = expectedBuildsFile.readlines()
    expectedBuildsStrList.extend(
      [
        "Specialized, missing_site, Trilinos-atdm-waterman-gnu-release-debug-openmp\n",
        "Specialized, waterman, Trilinos-atdm-waterman-missing-build\n",
        ]
      )
    with open(expectedBuildsFilePath, 'w') as expectedBuildsFile:
      expectedBuildsFile.write("".join(expectedBuildsStrList))

    # Add some configure and build failures
    fullCDashIndexBuildsJsonFilePath = \
      testOutputDir+\
      "/"+CDQAR.getFileNameStrFromText(buildSetName)+\
      "fullCDashIndexBuilds.json"
    with open(fullCDashIndexBuildsJsonFilePath, 'r') as fullCDashIndexBuildsJsonFile:
      fullCDashIndexBuildsJson = eval(fullCDashIndexBuildsJsonFile.read())
    specializedGroup = fullCDashIndexBuildsJson['buildgroups'][0]
    specializedGroup['builds'][1]['configure']['error'] = 1
    specializedGroup['builds'][3]['compilation']['error'] = 2
    specializedGroup['builds'][5]['compilation']['error'] = 1
    CDQAR.pprintPythonData(fullCDashIndexBuildsJson, fullCDashIndexBuildsJsonFilePath)

    # Run analyze_and_report_cdash_results.py and make sure that it prints
    # the right stuff
    analyze_and_report_cdash_results_run_case(
      self,
      testCaseName,
      [
        "--build-set-name='"+buildSetName+"'",  # Test changing this
        "--limit-table-rows=15",  # Check that this is read correctly
        ],
      1,
      "FAILED (bme=2, c=1, b=2, twoif=12, twif=9): Project Specialized Builds on 2001-01-01",
      [
        "Missing expected builds: bme=2",
        "Builds with configure failures: c=1",
        "Builds with build failures: b=2",
        "Failing tests without issue trackers: twoif=12",
        "Failing tests with issue trackers: twif=9",
        ],
      [
        "<h2>Build and Test results for Project Specialized Builds on 2001-01-01</h2>",

        # Links to build and non-passing tests
        "<a href=\"https://something[.]com/cdash/index[.]php[?]project=ProjectName&date=2001-01-01&builds_filters\">Builds on CDash</a> [(]num=6[)]<br>",
        "<a href=\"https://something[.]com/cdash/queryTests[.]php[?]project=ProjectName&date=2001-01-01&nonpasssing_tests_filters\">Nonpassing Tests on CDash</a> [(]num=21[)]<br>",

        # Top listing of types of data/tables to be displayed below 
        "<font color=\"red\">Missing expected builds: bme=2</font><br>",
        "<font color=\"red\">Builds with configure failures: c=1</font><br>",
        "<font color=\"red\">Builds with build failures: b=2</font><br>",
        "<font color=\"red\">Failing tests without issue trackers: twoif=12</font><br>",
        "Failing tests with issue trackers: twif=9<br>",
        
        # 'bme' table (Really pin down this table)
        "<h3>Missing expected builds: bme=2</h3>",
        "<table.*>",  # NOTE: Other unit test code checks the default style!
        "<tr>",
        "<th>Group</th>",
        "<th>Site</th>",
        "<th>Build Name</th>",
        "<th>Missing Status</th>",
        "</tr>",
        "<tr>",
        "<td align=\"left\">Specialized</td>",
        "<td align=\"left\">missing_site</td>",
        "<td align=\"left\">Trilinos-atdm-waterman-gnu-release-debug-openmp</td>",
        "<td align=\"left\">Build not found on CDash</td>",
        "</tr>",
        "<tr>",
        "<td align=\"left\">Specialized</td>",
        "<td align=\"left\">waterman</td>",
        "<td align=\"left\">Trilinos-atdm-waterman-missing-build</td>",
        "<td align=\"left\">Build not found on CDash</td>",
        "</tr>",
        "</table>",

        # 'c' table (Really pin this down)
        "<h3>Builds with configure failures [(]limited to 15[)]: c=1</h3>",
        "<table.*>",
        "<tr>",
        "<th>Group</th>",
        "<th>Site</th>",
        "<th>Build Name</th>",
        "</tr>",
        "<tr>",
        "<td align=\"left\">Specialized</td>",
        "<td align=\"left\">cee-rhel6</td>",
        "<td align=\"left\">Trilinos-atdm-cee-rhel6-clang-opt-serial</td>",
        "</tr>",
        "</table>",
        # NOTE: Above checks that --limit-table-rows=15 is getting used
        # correctly!

        # 'b' table (Really pin this down)
        "<h3>Builds with build failures [(]limited to 15[)]: b=2</h3>",
        "<table.*>",
        "<tr>",
        "<th>Group</th>",
        "<th>Site</th>",
        "<th>Build Name</th>",
        "</tr>",
        "<tr>",
        "<td align=\"left\">Specialized</td>",
        "<td align=\"left\">cee-rhel6</td>",
        "<td align=\"left\">Trilinos-atdm-cee-rhel6-gnu-4.9.3-opt-serial</td>",
        "</tr>",
        "<tr>",
        "<td align=\"left\">Specialized</td>",
        "<td align=\"left\">cee-rhel6</td>",
        "<td align=\"left\">Trilinos-atdm-cee-rhel6-intel-opt-serial</td>",
        "</tr>",
        "</table>",

        # 'twoif' table
        "<h3>Failing tests without issue trackers [(]limited to 15[)]: twoif=12</h3>",

        # 'twif' table
        "<h3>Failing tests with issue trackers: twif=9</h3>",
       ],
      #verbose=True,
      )
  # NOTE: That above test really pin down the contents of the 'bme', 'c', and
  # 'b' tables.  Other tests will not do that to avoid duplication in testing.

  # Test the all passing case
  def test_passed_clean(self):

    testCaseName = "passed_clean"
    buildSetName = "Project Specialized Builds"

    # Copy the raw files from CDash to get started
    testOutputDir = analyze_and_report_cdash_results_setup_test_dir(testCaseName,
      buildSetName)

    # Remove all of the failing tests
    oldTestListFilePath = testOutputDir+"/test_history/2001-01-01-All-Failing-Tests.json"
    CDQAR.pprintPythonData( {}, oldTestListFilePath )
    testListFilePath = \
      testOutputDir+"/Project_Specialized_Builds_fullCDashNonpassingTests.json"
    CDQAR.pprintPythonData( {'builds':[]}, testListFilePath )
    # ToDo: Fix above once the script caches the raw CDash JSON output.

    # Run analyze_and_report_cdash_results.py and make sure that it prints the
    # right stuff
    analyze_and_report_cdash_results_run_case(
      self,
      testCaseName,
      [
        "--build-set-name='"+buildSetName+"'",  # Test changing this
        ],
      0,
      "PASSED: Project Specialized Builds on 2001-01-01",
      [
        "Missing expected builds: bme=0",
        "Builds with configure failures: c=0",
        "Builds with build failures: b=0",
        "Failing tests without issue trackers: twoif=0",
        "Failing tests with issue trackers: twif=0",
        ],
      [
        "<h2>Build and Test results for Project Specialized Builds on 2001-01-01</h2>",

        # Links to build and non-passing tests
        "<p>",
        "<a href=\"https://something[.]com/cdash/index[.]php[?]project=ProjectName&date=2001-01-01&builds_filters\">Builds on CDash</a> [(]num=6[)]<br>",
        "<a href=\"https://something[.]com/cdash/queryTests[.]php[?]project=ProjectName&date=2001-01-01&nonpasssing_tests_filters\">Nonpassing Tests on CDash</a> [(]num=0[)]<br>",
        "</p>",
       ],
      #verbose=True,
      )

#
# Run the unit tests!
#

if __name__ == '__main__':

  # Clean out and re-recate the base test directory
  if os.path.exists(g_baseTestDir): shutil.rmtree(g_baseTestDir)
  os.mkdir(g_baseTestDir)

  unittest.main()
