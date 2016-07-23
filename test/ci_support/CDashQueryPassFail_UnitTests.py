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
import copy
import unittest

from FindCISupportDir import *
from CDashQueryPassFail import *

pythonVersion = sys.version_info.major

g_testBaseDir = getScriptBaseDir()

tribitsBaseDir=os.path.abspath(g_testBaseDir+"/../../tribits")
mockProjectBaseDir=os.path.abspath(tribitsBaseDir+"/examples/MockTrilinos")

#
# Data for tests
#

# This file was taken from an actual CDash query and then modified a little to
# make for better testing.
g_fullCDashIndexBuilds = \
  eval(open(g_testBaseDir+'/cdash_index_query_data.txt', 'r').read())

# This file was manually created from the above file to match what the reduced
# builds should be.
g_summmaryCDashIndexBuilds_expected = \
  eval(open(g_testBaseDir+'/cdash_index_query_data.summary.txt', 'r').read())

# This summary build has just the minimal required fields
singleBuildPasses = {
  'buildname':"buildName",
  'update': {'errors':0},
  'configure':{'error': 0},
  'compilation':{'error':0},
  'test': {'fail':0, 'notrun':0},
  }

# Dummy queryCDashAndDeterminePassFail() for unit testing

g_extractCDashApiQueryData_builds = None

def dummyExtractCDashApiQueryData(cdashQueryUrl_expected):
  return g_extractCDashApiQueryData_builds


#############################################################################
#
# Test CDashQueryPassFail.py
#
#############################################################################

class test_CDashQueryPassFail(unittest.TestCase):

  def test_validateYYYYMMDD_pass1(self):
    yyyyymmdd = validateYYYYMMDD("2015-12-21")
    self.assertEqual(str(yyyyymmdd), "2015-12-21 00:00:00")

  def test_validateYYYYMMDD_pass2(self):
    yyyyymmdd = validateYYYYMMDD("2015-12-01")
    self.assertEqual(str(yyyyymmdd), "2015-12-01 00:00:00")

  def test_validateYYYYMMDD_pass3(self):
    yyyyymmdd = validateYYYYMMDD("2015-12-1")
    self.assertEqual(str(yyyyymmdd), "2015-12-01 00:00:00")

  def test_validateYYYYMMDD_pass4(self):
    yyyyymmdd = validateYYYYMMDD("2015-01-1")
    self.assertEqual(str(yyyyymmdd), "2015-01-01 00:00:00")

  def test_validateYYYYMMDD_pass4(self):
    yyyyymmdd = validateYYYYMMDD("2015-1-9")
    self.assertEqual(str(yyyyymmdd), "2015-01-09 00:00:00")

  def test_validateYYYYMMDD_fail_empty(self):
    self.assertRaises(ValueError, validateYYYYMMDD,  "")

  def test_validateYYYYMMDD_fail1(self):
    self.assertRaises(ValueError, validateYYYYMMDD,  "201512-21")

  def test_validateYYYYMMDD_fail1(self):
    #yyyyymmdd = validateYYYYMMDD("201512-21")
    self.assertRaises(ValueError, validateYYYYMMDD,  "201512-21")

  def test_getCDashIndexQueryUrl(self):
    cdashIndexQueryUrl = getCDashIndexQueryUrl(
      "https://casl-dev.ornl.gov/testing", "VERA", "2015-12-21",
      "filtercount=1&showfilters=1&filtercombine=and&field1=groupname&compare1=61&value1=Nightly" \
    )
    cdashIndexQueryUrl_expected = \
    "https://casl-dev.ornl.gov/testing/api/v1/index.php?project=VERA&date=2015-12-21&filtercount=1&showfilters=1&filtercombine=and&field1=groupname&compare1=61&value1=Nightly"
    self.assertEqual(cdashIndexQueryUrl, cdashIndexQueryUrl_expected)

  def test_getCDashIndexBuildsSummary(self):
    summaryCDashIndexBuilds = getCDashIndexBuildsSummary(g_fullCDashIndexBuilds)
    #pp.pprint(summaryCDashIndexBuilds)
    self.assertEqual(len(summaryCDashIndexBuilds), len(g_summmaryCDashIndexBuilds_expected))
    for i in range(0, len(summaryCDashIndexBuilds)):
      self.assertEqual(summaryCDashIndexBuilds[i], g_summmaryCDashIndexBuilds_expected[i])

  def test_collectCDashIndexBuildSummaryFields_full(self):
    summaryCDashIndexBuild = collectCDashIndexBuildSummaryFields(singleBuildPasses)
    self.assertEqual(summaryCDashIndexBuild, singleBuildPasses)

  def test_collectCDashIndexBuildSummaryFields_missing_update(self):
    fullCDashIndexBuild_in = copy.deepcopy(singleBuildPasses)
    del fullCDashIndexBuild_in['update']
    summaryCDashIndexBuild = collectCDashIndexBuildSummaryFields(fullCDashIndexBuild_in)
    summaryCDashIndexBuild_expected = copy.deepcopy(singleBuildPasses)
    summaryCDashIndexBuild_expected['update'] = {'errors':9999, 'this_field_was_missing':1} 
    self.assertEqual(summaryCDashIndexBuild, summaryCDashIndexBuild_expected)

  def test_collectCDashIndexBuildSummaryFields_missing_configure(self):
    fullCDashIndexBuild_in = copy.deepcopy(singleBuildPasses)
    del fullCDashIndexBuild_in['configure']
    summaryCDashIndexBuild = collectCDashIndexBuildSummaryFields(fullCDashIndexBuild_in)
    summaryCDashIndexBuild_expected = copy.deepcopy(singleBuildPasses)
    summaryCDashIndexBuild_expected['configure'] = {'error':9999, 'this_field_was_missing':1} 
    self.assertEqual(summaryCDashIndexBuild, summaryCDashIndexBuild_expected)

  def test_collectCDashIndexBuildSummaryFields_missing_compilation(self):
    fullCDashIndexBuild_in = copy.deepcopy(singleBuildPasses)
    del fullCDashIndexBuild_in['compilation']
    summaryCDashIndexBuild = collectCDashIndexBuildSummaryFields(fullCDashIndexBuild_in)
    summaryCDashIndexBuild_expected = copy.deepcopy(singleBuildPasses)
    summaryCDashIndexBuild_expected['compilation'] = {'error':9999, 'this_field_was_missing':1} 
    self.assertEqual(summaryCDashIndexBuild, summaryCDashIndexBuild_expected)

  def test_collectCDashIndexBuildSummaryFields_missing_test(self):
    fullCDashIndexBuild_in = copy.deepcopy(singleBuildPasses)
    del fullCDashIndexBuild_in['test']
    summaryCDashIndexBuild = collectCDashIndexBuildSummaryFields(fullCDashIndexBuild_in)
    summaryCDashIndexBuild_expected = copy.deepcopy(singleBuildPasses)
    summaryCDashIndexBuild_expected['test'] = {'fail':9999, 'notrun':9999,'this_field_was_missing':1} 
    self.assertEqual(summaryCDashIndexBuild, summaryCDashIndexBuild_expected)

  def test_cdashIndexBuildPasses_pass(self):
    build = copy.deepcopy(singleBuildPasses)
    self.assertEqual(cdashIndexBuildPasses(build), True)

  def test_cdashIndexBuildPasses_update_fail(self):
    build = copy.deepcopy(singleBuildPasses)
    build['update']['errors'] = 1
    self.assertEqual(cdashIndexBuildPasses(build), False)

  def test_cdashIndexBuildPasses_configure_fail(self):
    build = copy.deepcopy(singleBuildPasses)
    build['configure']['error'] = 1
    self.assertEqual(cdashIndexBuildPasses(build), False)

  def test_cdashIndexBuildPasses_compilation_fail(self):
    build = copy.deepcopy(singleBuildPasses)
    build['compilation']['error'] = 1
    self.assertEqual(cdashIndexBuildPasses(build), False)

  def test_cdashIndexBuildPasses_test_fail_fail(self):
    build = copy.deepcopy(singleBuildPasses)
    build['test']['fail'] = 1
    self.assertEqual(cdashIndexBuildPasses(build), False)

  def test_cdashIndexBuildPasses_test_notrun_fail(self):
    build = copy.deepcopy(singleBuildPasses)
    build['test']['notrun'] = 1
    self.assertEqual(cdashIndexBuildPasses(build), False)

  def test_cdashIndexBuildsPass_1_pass(self):
    builds = [copy.deepcopy(singleBuildPasses)]
    (buildPasses, buildFailedMsg) = cdashIndexBuildsPass(builds)
    self.assertEqual(buildPasses, True)
    self.assertEqual(buildFailedMsg, "")

  def test_cdashIndexBuildsPass_1_fail(self):
    build = copy.deepcopy(singleBuildPasses)
    build['compilation']['error'] = 1
    builds = [build]
    (buildPasses, buildFailedMsg) = cdashIndexBuildsPass(builds)
    self.assertEqual(buildPasses, False)
    self.assertEqual(buildFailedMsg, "Error, the build "+str(build)+" failed!")

  def test_cdashIndexBuildsPass_2_pass(self):
    build = copy.deepcopy(singleBuildPasses)
    builds = [build, build]
    (buildPasses, buildFailedMsg) = cdashIndexBuildsPass(builds)
    self.assertEqual(buildPasses, True)
    self.assertEqual(buildFailedMsg, "")

  def test_cdashIndexBuildsPass_2_fail_1(self):
    build = copy.deepcopy(singleBuildPasses)
    buildFailed = copy.deepcopy(singleBuildPasses)
    buildFailed['buildname'] = "failedBuild"
    buildFailed['compilation']['error'] = 1
    builds = [buildFailed, build]
    (buildPasses, buildFailedMsg) = cdashIndexBuildsPass(builds)
    self.assertEqual(buildPasses, False)
    self.assertEqual(buildFailedMsg, "Error, the build "+str(buildFailed)+" failed!")

  def test_cdashIndexBuildsPass_2_fail_2(self):
    build = copy.deepcopy(singleBuildPasses)
    buildFailed = copy.deepcopy(singleBuildPasses)
    buildFailed['buildname'] = "failedBuild"
    buildFailed['compilation']['error'] = 1
    builds = [build, buildFailed]
    (buildPasses, buildFailedMsg) = cdashIndexBuildsPass(builds)
    self.assertEqual(buildPasses, False)
    self.assertEqual(buildFailedMsg, "Error, the build "+str(buildFailed)+" failed!")

  def test_getCDashIndexBuildNames(self):
    build1 = copy.deepcopy(singleBuildPasses)
    build1['buildname'] = "build1"
    build2 = copy.deepcopy(singleBuildPasses)
    build2['buildname'] = "build2"
    build3 = copy.deepcopy(singleBuildPasses)
    build3['buildname'] = "build3"
    builds = [build1, build2, build3]
    buildNames_expected = [ "build1", "build2", "build3" ]
    self.assertEqual(getCDashIndexBuildNames(builds), buildNames_expected)

  def test_doAllExpectedBuildsExist_1_pass(self):
    buildNames = ["build1"]
    expectedBuildNames = ["build1"]
    (allExpectedBuildsExist, errMsg) = \
      doAllExpectedBuildsExist(buildNames, expectedBuildNames)
    self.assertEqual(errMsg, "")
    self.assertEqual(allExpectedBuildsExist, True)

  def test_doAllExpectedBuildsExist_1_fail(self):
    buildNames = ["build1"]
    expectedBuildNames = ["build2"]
    (allExpectedBuildsExist, errMsg) = \
      doAllExpectedBuildsExist(buildNames, expectedBuildNames)
    self.assertEqual(errMsg,
      "Error, the expected build 'build2' does not exist in the list of builds ['build1']")
    self.assertEqual(allExpectedBuildsExist, False)

  def test_doAllExpectedBuildsExist_2_2_a_pass(self):
    buildNames = ["build1", "build2"]
    expectedBuildNames = ["build1", "build2"]
    (allExpectedBuildsExist, errMsg) = \
      doAllExpectedBuildsExist(buildNames, expectedBuildNames)
    self.assertEqual(errMsg, "")
    self.assertEqual(allExpectedBuildsExist, True)

  def test_doAllExpectedBuildsExist_2_2_b_fail(self):
    buildNames = ["build2", "build1"]
    expectedBuildNames = ["build1", "build2"]
    (allExpectedBuildsExist, errMsg) = \
      doAllExpectedBuildsExist(buildNames, expectedBuildNames)
    self.assertEqual(errMsg, "")
    self.assertEqual(allExpectedBuildsExist, True)

  def test_doAllExpectedBuildsExist_2_1_pass(self):
    buildNames = ["build1", "build2"]
    expectedBuildNames = ["build1"]
    (allExpectedBuildsExist, errMsg) = \
      doAllExpectedBuildsExist(buildNames, expectedBuildNames)
    self.assertEqual(errMsg, "")
    self.assertEqual(allExpectedBuildsExist, True)

  def test_doAllExpectedBuildsExist_2_1_fail(self):
    buildNames = ["build1", "build2"]
    expectedBuildNames = ["build3"]
    (allExpectedBuildsExist, errMsg) = \
      doAllExpectedBuildsExist(buildNames, expectedBuildNames)
    self.assertEqual(errMsg,
      "Error, the expected build 'build3' does not exist in the list of builds ['build1', 'build2']")
    self.assertEqual(allExpectedBuildsExist, False)

  def test_doAllExpectedBuildsExist_1_2_a_fail(self):
    buildNames = ["build1"]
    expectedBuildNames = ["build1", "build2"]
    (allExpectedBuildsExist, errMsg) = \
      doAllExpectedBuildsExist(buildNames, expectedBuildNames)
    self.assertEqual(errMsg,
      "Error, the expected build 'build2' does not exist in the list of builds ['build1']")
    self.assertEqual(allExpectedBuildsExist, False)

  def test_doAllExpectedBuildsExist_1_2_b_fail(self):
    buildNames = ["build1"]
    expectedBuildNames = ["build2", "build1"]
    (allExpectedBuildsExist, errMsg) = \
      doAllExpectedBuildsExist(buildNames, expectedBuildNames)
    self.assertEqual(errMsg,
      "Error, the expected build 'build2' does not exist in the list of builds ['build1']")
    self.assertEqual(allExpectedBuildsExist, False)

  def test_cdashIndexBuildsPassAndExpectedExist_1_pass(self):
    build1 = copy.deepcopy(singleBuildPasses)
    build1['buildname'] = "build1"
    builds = [ build1 ]
    expectedBuildNames = ["build1"]
    (cdashIndexBuildsPassAndExpectedExist_passed, errMsg) = \
      cdashIndexBuildsPassAndExpectedExist(builds, expectedBuildNames)
    self.assertEqual(errMsg,
      "")
    self.assertEqual(cdashIndexBuildsPassAndExpectedExist_passed, True)

  def test_cdashIndexBuildsPassAndExpectedExist_1_build_fail(self):
    build1 = copy.deepcopy(singleBuildPasses)
    build1['buildname'] = "build1"
    build1['configure']['error'] = 5
    builds = [ build1 ]
    expectedBuildNames = ["build1"]
    (cdashIndexBuildsPassAndExpectedExist_passed, errMsg) = \
      cdashIndexBuildsPassAndExpectedExist(builds, expectedBuildNames)
    expectedErrMsg = "Error, the build {'buildname': 'build1', 'test': " \
                     "{'fail': 0, 'notrun': 0}, 'compilation': {'error': 0}, " \
                     "'update': {'errors': 0}, 'configure': {'error': 5}} " \
                     "failed!"
    if pythonVersion == 2:
      self.assertEqual(errMsg, expectedErrMsg)
    elif pythonVersion == 3:
      # wfspotz, 23 Jul 2016: I tried the Python 2 test
      #
      #     self.assertEqual(errMsg, expectedErrMsg)
      #
      # but this does not work in Python 3 because the order of the keys keeps
      # changing. It appears the hash algorithm for sorting the keys is
      # non-deterministic (I also believe, in Python 2, that the order can
      # change from platform to platform). So here I only check the
      # deterministic part of the error message.
      self.assertEqual(errMsg[:18], "Error, the build {")
      self.assertEqual(errMsg[-9:], "} failed!")
    self.assertEqual(cdashIndexBuildsPassAndExpectedExist_passed, False)

  def test_cdashIndexBuildsPassAndExpectedExist_1_missing_expected_build(self):
    build1 = copy.deepcopy(singleBuildPasses)
    build1['buildname'] = "build1"
    builds = [ build1 ]
    expectedBuildNames = ["build2"]
    (cdashIndexBuildsPassAndExpectedExist_passed, errMsg) = \
      cdashIndexBuildsPassAndExpectedExist(builds, expectedBuildNames)
    self.assertEqual(errMsg,
      "Error, the expected build 'build2' does not exist in the list of builds ['build1']")
    self.assertEqual(cdashIndexBuildsPassAndExpectedExist_passed, False)

  def test_queryCDashAndDeterminePassFail_1_pass(self):
    build1 = copy.deepcopy(singleBuildPasses)
    build1['buildname'] = "build1"
    fullCDashIndexBuilds = {
      'buildgroups':[
        {'builds':[build1]}
        ]
      }
    global g_extractCDashApiQueryData_builds
    g_extractCDashApiQueryData_builds = fullCDashIndexBuilds 
    expectedBuildNames = ["build1"]
    (allPassed, errMsg) = queryCDashAndDeterminePassFail(
      "https://casl-dev.ornl.gov/testing", "VERA", "2015-12-21", "dummy-filter-fields",
      expectedBuildNames, False, dummyExtractCDashApiQueryData)
    self.assertEqual(errMsg, "")
    self.assertEqual(allPassed, True)

  def test_queryCDashAndDeterminePassFail_2_pass(self):
    build1 = copy.deepcopy(singleBuildPasses)
    build1['buildname'] = "build1"
    build2 = copy.deepcopy(singleBuildPasses)
    build2['buildname'] = "build2"
    fullCDashIndexBuilds = {
      'buildgroups':[
        {'builds':[build1]},
        {'builds':[build2]}
        ]
      }
    global g_extractCDashApiQueryData_builds
    g_extractCDashApiQueryData_builds = fullCDashIndexBuilds 
    expectedBuildNames = ["build1", "build2"]
    (allPassed, errMsg) = queryCDashAndDeterminePassFail(
      "https://casl-dev.ornl.gov/testing", "VERA", "2015-12-21", "dummy-filter-fields",
      expectedBuildNames, False, dummyExtractCDashApiQueryData)
    self.assertEqual(errMsg, "")
    self.assertEqual(allPassed, True)

  def test_queryCDashAndDeterminePassFail_1_missing_expected(self):
    build1 = copy.deepcopy(singleBuildPasses)
    build1['buildname'] = "build1"
    fullCDashIndexBuilds = {
      'buildgroups':[
        {'builds':[build1]}
        ]
      }
    global g_extractCDashApiQueryData_builds
    g_extractCDashApiQueryData_builds = fullCDashIndexBuilds 
    expectedBuildNames = ["missing"]
    (allPassed, errMsg) = queryCDashAndDeterminePassFail(
      "https://casl-dev.ornl.gov/testing", "VERA", "2015-12-21", "dummy-filter-fields",
      expectedBuildNames, False, dummyExtractCDashApiQueryData)
    self.assertEqual(errMsg,
      "Error, the expected build 'missing' does not exist in the list of builds ['build1']")
    self.assertEqual(allPassed, False)

  def test_queryCDashAndDeterminePassFail_1_fail(self):
    build1 = copy.deepcopy(singleBuildPasses)
    build1['buildname'] = "build1"
    build1['test']['fail'] = 3
    fullCDashIndexBuilds = {
      'buildgroups':[
        {'builds':[build1]}
        ]
      }
    global g_extractCDashApiQueryData_builds
    g_extractCDashApiQueryData_builds = fullCDashIndexBuilds 
    expectedBuildNames = ["build1"]
    (allPassed, errMsg) = queryCDashAndDeterminePassFail(
      "https://casl-dev.ornl.gov/testing", "VERA", "2015-12-21", "dummy-filter-fields",
      expectedBuildNames, False, dummyExtractCDashApiQueryData)
    if pythonVersion == 2:
      expectedErrMsg = "Error, the build {u'buildname': 'build1', u'test': " \
                       "{'fail': 3, 'notrun': 0}, u'compilation': {'error': " \
                       "0}, u'update': {'errors': 0}, u'configure': " \
                       "{'error': 0}} failed!"
      self.assertEqual(errMsg, expectedErrMsg)
    elif pythonVersion == 3:
      expectedErrMsg = "Error, the build {'buildname': 'build1', 'test': " \
                       "{'fail': 3, 'notrun': 0}, 'compilation': {'error': " \
                       "0}, 'update': {'errors': 0}, 'configure': " \
                       "{'error': 0}} failed!"
      # wfspotz, 23 Jul 2016: I tried the Python 2 test
      #
      #     self.assertEqual(errMsg, expectedErrMsg)
      #
      # but this does not work in Python 3 because the order of the keys keeps
      # changing. It appears the hash algorithm for sorting the keys is
      # non-deterministic (I also believe, in Python 2, that the order can
      # change from platform to platform). So here I only check the
      # deterministic part of the error message.
      self.assertEqual(errMsg[:18], "Error, the build {")
      self.assertEqual(errMsg[-9:], "} failed!")
    self.assertEqual(allPassed, False)

  def test_queryCDashAndDeterminePassFail_2_fail(self):
    build1 = copy.deepcopy(singleBuildPasses)
    build1['buildname'] = "build1"
    build2 = copy.deepcopy(singleBuildPasses)
    build2['buildname'] = "build2"
    build2['test']['notrun'] = 2
    fullCDashIndexBuilds = {
      'buildgroups':[
        {'builds':[build1]},
        {'builds':[build2]}
        ]
      }
    global g_extractCDashApiQueryData_builds
    g_extractCDashApiQueryData_builds = fullCDashIndexBuilds 
    expectedBuildNames = ["build1", "build2"]
    (allPassed, errMsg) = queryCDashAndDeterminePassFail(
      "https://casl-dev.ornl.gov/testing", "VERA", "2015-12-21", "dummy-filter-fields",
      expectedBuildNames, False, dummyExtractCDashApiQueryData)
    if pythonVersion == 2:
      expectedErrMsg = "Error, the build {u'buildname': 'build2', u'test': " \
                       "{'fail': 0, 'notrun': 2}, u'compilation': {'error': " \
                       "0}, u'update': {'errors': 0}, u'configure': " \
                       "{'error': 0}} failed!"
      self.assertEqual(errMsg, expectedErrMsg)
    elif pythonVersion == 3:
      expectedErrMsg = "Error, the build {'configure': {'error': 0}, " \
                       "'update': {'errors': 0}, 'buildname': 'build2', " \
                       "'test': {'notrun': 2, 'fail': 0}, 'compilation': " \
                       "{'error': 0}} failed!"
      # wfspotz, 23 Jul 2016: I tried the Python 2 test
      #
      #     self.assertEqual(errMsg, expectedErrMsg)
      #
      # but this does not work in Python 3 because the order of the keys keeps
      # changing. It appears the hash algorithm for sorting the keys is
      # non-deterministic (I also believe, in Python 2, that the order can
      # change from platform to platform). So here I only check the
      # deterministic part of the error message.
      self.assertEqual(errMsg[:18], "Error, the build {")
      self.assertEqual(errMsg[-9:], "} failed!")
    self.assertEqual(allPassed, False)


if __name__ == '__main__':

  unittest.main()
