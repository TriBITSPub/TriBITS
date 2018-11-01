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
# Helper functions and classes
#


# Mock function object for getting data off of CDash as a stand-in for the
# function extractCDashApiQueryData().
class MockExtractCDashApiQueryDataFunctor(object):
  def __init__(self, cdashApiQueryUrl_expected, dataToReturn):
    self.cdashApiQueryUrl_expected = cdashApiQueryUrl_expected
    self.dataToReturn = dataToReturn
  def __call__(self, cdashApiQueryUrl):
    if cdashApiQueryUrl != self.cdashApiQueryUrl_expected:
      raise Exception(
        "Error, cdashApiQueryUrl='"+cdashApiQueryUrl+"' !="+\
        " cdashApiQueryUrl_expected='"+cdashApiQueryUrl_expected+"'!")
    return self.dataToReturn


# Helper script for creating test directories
def deleteThenCreateTestDir(testDir):
    outputCacheDir="test_getAndCacheCDashQueryDataOrReadFromCache_write_cache"
    if os.path.exists(testDir): shutil.rmtree(testDir)
    os.mkdir(testDir)


#############################################################################
#
# Test CDashQueryAnalizeReport.validateYYYYMMDD_pass1()
#
#############################################################################

class test_validateYYYYMMDD(unittest.TestCase):

  def test_pass1(self):
    yyyyymmdd = validateYYYYMMDD("2015-12-21")
    self.assertEqual(str(yyyyymmdd), "2015-12-21 00:00:00")

  def test_pass2(self):
    yyyyymmdd = validateYYYYMMDD("2015-12-01")
    self.assertEqual(str(yyyyymmdd), "2015-12-01 00:00:00")

  def test_pass3(self):
    yyyyymmdd = validateYYYYMMDD("2015-12-1")
    self.assertEqual(str(yyyyymmdd), "2015-12-01 00:00:00")

  def test_pass4(self):
    yyyyymmdd = validateYYYYMMDD("2015-01-1")
    self.assertEqual(str(yyyyymmdd), "2015-01-01 00:00:00")

  def test_pass4(self):
    yyyyymmdd = validateYYYYMMDD("2015-1-9")
    self.assertEqual(str(yyyyymmdd), "2015-01-09 00:00:00")

  def test_fail_empty(self):
    self.assertRaises(ValueError, validateYYYYMMDD,  "")

  def test_fail1(self):
    self.assertRaises(ValueError, validateYYYYMMDD,  "201512-21")

  def test_fail1(self):
    #yyyyymmdd = validateYYYYMMDD("201512-21")
    self.assertRaises(ValueError, validateYYYYMMDD,  "201512-21")


#############################################################################
#
# Test CDashQueryAnalizeReport.readCsvFileIntoListOfDicts()
#
#############################################################################

class test_readCsvFileIntoListOfDicts(unittest.TestCase):

  def test_col_3_row_2_expected_cols__pass(self):
    csvFileStr=\
        "col_0, col_1, col_2\n"+\
        "val_00, val_01, val_02\n"+\
        "val_10, val_11, val_12\n\n\n"  # Add extra blanks line for extra test!
    csvFileName = "readCsvFileIntoListOfDicts_col_3_row_2_expeced_cols_pass.csv"
    with open(csvFileName, 'w') as csvFileToWrite:
      csvFileToWrite.write(csvFileStr)
    listOfDicts = readCsvFileIntoListOfDicts(csvFileName, ['col_0', 'col_1', 'col_2'])
    listOfDicts_expected = \
      [
        { 'col_0' : 'val_00', 'col_1' : 'val_01', 'col_2' : 'val_02' },
        { 'col_0' : 'val_10', 'col_1' : 'val_11', 'col_2' : 'val_12' },
        ]
    self.assertEqual(len(listOfDicts), 2)
    for i in range(len(listOfDicts_expected)):
      self.assertEqual(listOfDicts[i], listOfDicts_expected[i])

  def test_col_3_row_2_no_expected_cols_pass(self):
    csvFileStr=\
        "col_0, col_1, col_2\n"+\
        "val_00, val_01, val_02\n"+\
        "val_10, val_11, val_12\n\n\n"  # Add extra blanks line for extra test!
    csvFileName = "readCsvFileIntoListOfDicts_col_3_row_2_no_expected_cols_pass.csv"
    with open(csvFileName, 'w') as csvFileToWrite:
      csvFileToWrite.write(csvFileStr)
    listOfDicts = readCsvFileIntoListOfDicts(csvFileName)
    listOfDicts_expected = \
      [
        { 'col_0' : 'val_00', 'col_1' : 'val_01', 'col_2' : 'val_02' },
        { 'col_0' : 'val_10', 'col_1' : 'val_11', 'col_2' : 'val_12' },
        ]
    self.assertEqual(len(listOfDicts), 2)
    for i in range(len(listOfDicts_expected)):
      self.assertEqual(listOfDicts[i], listOfDicts_expected[i])

  def test_too_few_expected_headers_fail(self):
    csvFileStr=\
        "wrong col, col_1, col_2\n"+\
        "val_00, val_01, val_02\n"
    csvFileName = "readCsvFileIntoListOfDicts_too_few_expected_headers_fail.csv"
    with open(csvFileName, 'w') as csvFileToWrite:
      csvFileToWrite.write(csvFileStr)
    #listOfDicts = readCsvFileIntoListOfDicts(csvFileName, ['col_0', 'col_1'])
    self.assertRaises(Exception, readCsvFileIntoListOfDicts,
      csvFileName, ['col_0', 'col_1'])

  def test_too_many_expected_headers_fail(self):
    csvFileStr=\
        "wrong col, col_1, col_2\n"+\
        "val_00, val_01, val_02\n"
    csvFileName = "readCsvFileIntoListOfDicts_too_many_expected_headers_fail.csv"
    with open(csvFileName, 'w') as csvFileToWrite:
      csvFileToWrite.write(csvFileStr)
    #listOfDicts = readCsvFileIntoListOfDicts(csvFileName,
    #  ['col_0', 'col_1', 'col_2', 'col3'])
    self.assertRaises(Exception, readCsvFileIntoListOfDicts,
      csvFileName, ['col_0', 'col_1', 'col_2', 'col3'])

  def test_wrong_expected_col_0_fail(self):
    csvFileStr=\
        "wrong col, col_1, col_2\n"+\
        "val_00, val_01, val_02\n"
    csvFileName = "readCsvFileIntoListOfDicts_wrong_expected_col_0_fail.csv"
    with open(csvFileName, 'w') as csvFileToWrite:
      csvFileToWrite.write(csvFileStr)
    #listOfDicts = readCsvFileIntoListOfDicts(csvFileName, ['col_0', 'col_1', 'col_2'])
    self.assertRaises(Exception, readCsvFileIntoListOfDicts,
      csvFileName, ['col_0', 'col_1', 'col_2'])

  def test_wrong_expected_col_1_fail(self):
    csvFileStr=\
        "col_0, wrong col, col_2\n"+\
        "val_00, val_01, val_02\n"
    csvFileName = "readCsvFileIntoListOfDicts_wrong_expected_col_1_fail.csv"
    with open(csvFileName, 'w') as csvFileToWrite:
      csvFileToWrite.write(csvFileStr)
    #listOfDicts = readCsvFileIntoListOfDicts(csvFileName, ['col_0', 'col_1', 'col_2'])
    self.assertRaises(Exception, readCsvFileIntoListOfDicts,
      csvFileName, ['col_0', 'col_1', 'col_2'])

  def test_col_3_row_2_bad_row_len_fail(self):
    csvFileStr=\
        "col_0, col_1, col_2\n"+\
        "val_00, val_01, val_02\n"+\
        "val_10, val_11, val_12, extra\n"
    csvFileName = "readCsvFileIntoListOfDicts_col_3_row_2_bad_row_len_fail.csv"
    with open(csvFileName, 'w') as csvFileToWrite:
      csvFileToWrite.write(csvFileStr)
    #listOfDicts = readCsvFileIntoListOfDicts(csvFileName)
    self.assertRaises(Exception, readCsvFileIntoListOfDicts, csvFileName)

  # ToDo: Add test for reading a CSV file with no rows

  # ToDo: Add test for reading an empty CSV file (no column headers)


#############################################################################
#
# Test CDashQueryAnalizeReport.getExpectedBuildsListfromCsvFile()
#
#############################################################################

class test_getExpectedBuildsListfromCsvFile(unittest.TestCase):

  def test_getExpectedBuildsListfromCsvFile(self):
    expectedBuildsCsvFileStr=\
        "group, site, buildname\n"+\
        "group1, site1, buildname1\n"+\
        "group1, site1, buildname2\n"+\
        "group2, site2, buildname2\n\n\n\n"
    csvFileName = "test_getExpectedBuildsListfromCsvFile.csv"
    with open(csvFileName, 'w') as csvFileToWrite:
      csvFileToWrite.write(expectedBuildsCsvFileStr)
    expectedBuildsList = getExpectedBuildsListfromCsvFile(csvFileName)
    expectedBuildsList_expected = \
      [
        { 'group' : 'group1', 'site' : 'site1', 'buildname' : 'buildname1' },
        { 'group' : 'group1', 'site' : 'site1', 'buildname' : 'buildname2' },
        { 'group' : 'group2', 'site' : 'site2', 'buildname' : 'buildname2' },
        ]
    self.assertEqual(len(expectedBuildsList), 3)
    for i in range(len(expectedBuildsList_expected)):
      self.assertEqual(expectedBuildsList[i], expectedBuildsList_expected[i])


#############################################################################
#
# Test CDashQueryAnalizeReport.getAndCacheCDashQueryDataOrReadFromCache()
#
#############################################################################

g_getAndCacheCDashQueryDataOrReadFromCache_data = {
  'keyname1' : "value1",
  'keyname2' : "value2",
   }

def dummyGetCDashData_for_getAndCacheCDashQueryDataOrReadFromCache(
  cdashQueryUrl_expected \
  ):
  if cdashQueryUrl_expected != "dummy-cdash-url":
    raise Exception("Error, cdashQueryUrl_expected != \'dummy-cdash-url\'")  
  return g_getAndCacheCDashQueryDataOrReadFromCache_data

class test_getAndCacheCDashQueryDataOrReadFromCache(unittest.TestCase):

  def test_getAndCacheCDashQueryDataOrReadFromCache_write_cache(self):
    outputCacheDir="test_getAndCacheCDashQueryDataOrReadFromCache_write_cache"
    outputCacheFile=outputCacheDir+"/cachedCDashQueryData.json"
    deleteThenCreateTestDir(outputCacheDir)
    mockExtractCDashApiQueryDataFunctor = MockExtractCDashApiQueryDataFunctor(
       "dummy-cdash-url", g_getAndCacheCDashQueryDataOrReadFromCache_data)
    cdashQueryData = getAndCacheCDashQueryDataOrReadFromCache(
      "dummy-cdash-url", outputCacheFile,
      useCachedCDashData=False,
      printCDashUrl=False,
      extractCDashApiQueryData_in=mockExtractCDashApiQueryDataFunctor
      )
    self.assertEqual(cdashQueryData, g_getAndCacheCDashQueryDataOrReadFromCache_data)
    cdashQueryData_cache = eval(open(outputCacheFile, 'r').read())
    self.assertEqual(cdashQueryData_cache, g_getAndCacheCDashQueryDataOrReadFromCache_data)

  def test_getAndCacheCDashQueryDataOrReadFromCache_read_cache(self):
    outputCacheDir="test_getAndCacheCDashQueryDataOrReadFromCache_read_cache"
    outputCacheFile=outputCacheDir+"/cachedCDashQueryData.json"
    deleteThenCreateTestDir(outputCacheDir)
    open(outputCacheFile, 'w').write(str(g_getAndCacheCDashQueryDataOrReadFromCache_data))
    cdashQueryData = getAndCacheCDashQueryDataOrReadFromCache(
      "dummy-cdash-url", outputCacheFile,
      useCachedCDashData=True,
      printCDashUrl=False,
      )
    self.assertEqual(cdashQueryData, g_getAndCacheCDashQueryDataOrReadFromCache_data)


#############################################################################
#
# Test CDashQueryAnalizeReport URL functions
#
#############################################################################

class test_CDashQueryAnalizeReport_UrlFuncs(unittest.TestCase):

  def test_getCDashIndexQueryUrl(self):
    cdashIndexQueryUrl = getCDashIndexQueryUrl(
      "site.com/cdash", "project-name", "2015-12-21", "filtercount=1&morestuff" )
    cdashIndexQueryUrl_expected = \
      "site.com/cdash/api/v1/index.php?project=project-name&date=2015-12-21&filtercount=1&morestuff"
    self.assertEqual(cdashIndexQueryUrl, cdashIndexQueryUrl_expected)

  def test_getCDashIndexBrowserUrl(self):
    cdashIndexQueryUrl = getCDashIndexBrowserUrl(
      "site.com/cdash", "project-name", "2015-12-21", "filtercount=1&morestuff" )
    cdashIndexQueryUrl_expected = \
      "site.com/cdash/index.php?project=project-name&date=2015-12-21&filtercount=1&morestuff"
    self.assertEqual(cdashIndexQueryUrl, cdashIndexQueryUrl_expected)

  def test_getCDashQueryTestsQueryUrl(self):
    cdashIndexQueryUrl = getCDashQueryTestsQueryUrl(
      "site.com/cdash", "project-name", "2015-12-21", "filtercount=1&morestuff" )
    cdashIndexQueryUrl_expected = \
      "site.com/cdash/api/v1/queryTests.php?project=project-name&date=2015-12-21&filtercount=1&morestuff"
    self.assertEqual(cdashIndexQueryUrl, cdashIndexQueryUrl_expected)

  def test_getCDashQueryTestsBrowserUrl(self):
    cdashIndexQueryUrl = getCDashQueryTestsBrowserUrl(
      "site.com/cdash", "project-name", "2015-12-21", "filtercount=1&morestuff" )
    cdashIndexQueryUrl_expected = \
      "site.com/cdash/queryTests.php?project=project-name&date=2015-12-21&filtercount=1&morestuff"
    self.assertEqual(cdashIndexQueryUrl, cdashIndexQueryUrl_expected)


#############################################################################
#
# Test CDashQueryAnalizeReport.collectCDashIndexBuildSummaryFields()
#
#############################################################################

# This summary build has just the minimal required fields
g_singleBuildPassesSummary = {
  'group':'groupName',
  'site':'siteName',
  'buildname':"buildName",
  'update': {'errors':0},
  'configure':{'error': 0},
  'compilation':{'error':0},
  'test': {'fail':0, 'notrun':0},
  }

# Single build with extra stuff
g_singleBuildPassesRaw = {
  'site':'siteName',
  'buildname':"buildName",
  'update': {'errors':0},
  'configure':{'error': 0},
  'compilation':{'error':0},
  'test': {'fail':0, 'notrun':0},
  'extra-stuff':'stuff',
  }

class test_collectCDashIndexBuildSummaryFields(unittest.TestCase):

  def test_collectCDashIndexBuildSummaryFields_full(self):
    buildSummary = collectCDashIndexBuildSummaryFields(g_singleBuildPassesRaw, "groupName")
    self.assertEqual(buildSummary, g_singleBuildPassesSummary)

  def test_collectCDashIndexBuildSummaryFields_missing_update(self):
    fullCDashIndexBuild_in = copy.deepcopy(g_singleBuildPassesRaw)
    del fullCDashIndexBuild_in['update']
    buildSummary = collectCDashIndexBuildSummaryFields(fullCDashIndexBuild_in, "groupName")
    buildSummary_expected = copy.deepcopy(g_singleBuildPassesSummary)
    del buildSummary_expected['update']
    self.assertEqual(buildSummary, buildSummary_expected)

  def test_collectCDashIndexBuildSummaryFields_missing_configure(self):
    fullCDashIndexBuild_in = copy.deepcopy(g_singleBuildPassesRaw)
    del fullCDashIndexBuild_in['configure']
    buildSummary = collectCDashIndexBuildSummaryFields(fullCDashIndexBuild_in, "groupName")
    buildSummary_expected = copy.deepcopy(g_singleBuildPassesSummary)
    del buildSummary_expected['configure']
    self.assertEqual(buildSummary, buildSummary_expected)


#############################################################################
#
# Test CDashQueryAnalizeReport.flattenCDashIndexBuildsToListOfDicts()
#
#############################################################################

# This file was taken from an actual CDash query and then modified a little to
# make for better testing.
g_fullCDashIndexBuildsJson = \
  eval(open(g_testBaseDir+'/cdash_index_query_data.json', 'r').read())
#print("g_fullCDashIndexBuildsJson:")
#g_pp.pprint(g_fullCDashIndexBuildsJson)

# This file was manually created from the above file to match what the reduced
# builds should be.
g_summaryCDashIndexBuilds_expected = \
  eval(open(g_testBaseDir+'/cdash_index_query_data.flattened.json', 'r').read())
#print("g_summaryCDashIndexBuilds_expected:")
#g_pp.pprint(g_summaryCDashIndexBuilds_expected)

class test_flattenCDashIndexBuildsToListOfDicts(unittest.TestCase):

  def test_flattenCDashIndexBuildsToListOfDicts(self):
    summaryCDashIndexBuilds = flattenCDashIndexBuildsToListOfDicts(g_fullCDashIndexBuildsJson)
    #pp.pprint(summaryCDashIndexBuilds)
    self.assertEqual(
      len(summaryCDashIndexBuilds), len(g_summaryCDashIndexBuilds_expected))
    for i in range(0, len(summaryCDashIndexBuilds)):
      self.assertEqual(summaryCDashIndexBuilds[i], g_summaryCDashIndexBuilds_expected[i])


#############################################################################
#
# Test CDashQueryAnalizeReport.flattenCDashQueryTestsToListOfDicts()
#
#############################################################################

# This file was taken from an actual CDash query and then modified a little to
# make for better testing.
g_fullCDashQueryTestsJson = \
  eval(open(g_testBaseDir+'/cdash_query_tests_data.json', 'r').read())
#print("g_fullCDashQueryTestsJson:")
#g_pp.pprint(g_fullCDashQueryTestsJson)

# This file was manually created from the above file to match what the reduced
# builds should be.
g_testsListOfDicts_expected = \
  eval(open(g_testBaseDir+'/cdash_query_tests_data.flattened.json', 'r').read())
#print("g_testsListOfDicts_expected:")
#g_pp.pprint(g_testsListOfDicts_expected)

class test_flattenCDashQueryTestsToListOfDicts(unittest.TestCase):

  def test_flattenCDashQueryTestsToListOfDicts(self):
    testsListOfDicts = \
      flattenCDashQueryTestsToListOfDicts(g_fullCDashQueryTestsJson)
    #pp.pprint(testsListOfDicts)
    self.assertEqual(
      len(testsListOfDicts), len(g_testsListOfDicts_expected))
    for i in range(0, len(testsListOfDicts)):
      self.assertEqual(testsListOfDicts[i], g_testsListOfDicts_expected[i])


#############################################################################
#
# Test CDashQueryAnalizeReport.createLookupDictForListOfDicts()
#
#############################################################################

g_buildsListForExpectedBuilds = [
  { 'group':'group1', 'site':'site1', 'buildname':'build1', 'data':'val1' },
  { 'group':'group1', 'site':'site1', 'buildname':'build2', 'data':'val2' },
  { 'group':'group1', 'site':'site2', 'buildname':'build3', 'data':'val3' },
  { 'group':'group2', 'site':'site1', 'buildname':'build1', 'data':'val4' },
  { 'group':'group2', 'site':'site3', 'buildname':'build4', 'data':'val5' },
  ]

g_buildLookupDictForExpectedBuilds = {
  'group1' : {
    'site1' : {
      'build1':{'group':'group1','site':'site1','buildname':'build1','data':'val1'},
      'build2':{'group':'group1','site':'site1','buildname':'build2','data':'val2'},
      },
    'site2' : {
      'build3':{'group':'group1','site':'site2','buildname':'build3','data':'val3'},
      },
    },
  'group2' : {
    'site1' : {
      'build1':{'group':'group2','site':'site1','buildname':'build1','data':'val4'},
      },
    'site3' : {
      'build4':{'group':'group2','site':'site3','buildname':'build4','data':'val5'},
      },
    },
  }


class test_createLookupDictForListOfDicts(unittest.TestCase):

  def test_unique_dicts(self):
    buildLookupDict = createLookupDictForListOfDicts(
      g_buildsListForExpectedBuilds,
      ['group', 'site', 'buildname'] )
    #print("\nbuildLookupDict:")
    #g_pp.pprint(buildLookupDict)
    #print("\ng_buildLookupDictForExpectedBuilds:")
    #g_pp.pprint(g_buildLookupDictForExpectedBuilds)
    self.assertEqual(buildLookupDict, g_buildLookupDictForExpectedBuilds)

  def test_duplicate_dicts(self):
    listOfDicts = copy.deepcopy(g_buildsListForExpectedBuilds)
    newDictEle = copy.deepcopy(g_buildsListForExpectedBuilds[0])
    newDictEle['data'] = 'new_data_val1'
    listOfDicts.append(newDictEle)
    try:
      buildLookupDict = createLookupDictForListOfDicts(
        listOfDicts,
        ['group', 'site', 'buildname'] )
      self.assertEqual("Did not throw exception!", "no it did not!")
    except Exception, errMsg:
      self.assertEqual(str(errMsg),
        "Error, listOfDicts[5]="+\
        "{'buildname': 'build1', 'group': 'group1', 'data': 'new_data_val1', 'site': 'site1'}"+\
        " has duplicate values for the list of keys [['group', 'site', 'buildname']]"+\
        " with the element already added"+\
        " {'buildname': 'build1', 'data': 'val1', 'group': 'group1', 'site': 'site1'}!" )


#############################################################################
#
# Test CDashQueryAnalizeReport.lookupDictGivenLookupDict()
#
#############################################################################

def gsb(groupName, siteName, buildName):
  return {'group':groupName, 'site':siteName, 'buildname':buildName}

def lookupDictData(groupName, siteName, buildName, buildLookupDict):
  dictFound = lookupDictGivenLookupDict(buildLookupDict,
    ['group', 'site', 'buildname'],
    gsb(groupName, siteName, buildName) )
  if not dictFound : return None
  return dictFound.get('data')
     
class test_lookupDictGivenLookupDict(unittest.TestCase):

  def test_1(self):
    lud = createLookupDictForListOfDicts(g_buildsListForExpectedBuilds,
      ['group', 'site', 'buildname'] )
    self.assertEqual(lookupDictData('group1','site1','build1', lud), 'val1')
    self.assertEqual(lookupDictData('group1','site1','build2', lud), 'val2')
    self.assertEqual(lookupDictData('group1','site2','build3', lud), 'val3')
    self.assertEqual(lookupDictData('group2','site1','build1', lud), 'val4')
    self.assertEqual(lookupDictData('group2','site3','build4', lud), 'val5')
    self.assertEqual(lookupDictData('group2','site3','build1', lud), None)
    self.assertEqual(lookupDictData('group2','site4','build1', lud), None)
    self.assertEqual(lookupDictData('group3','site1','build1', lud), None)


#############################################################################
#
# Test CDashQueryAnalizeReport.SearchableListOfDicts
#
#############################################################################


def slodLookupData(slod, groupName, siteName, buildName):
  dictFound = slod.lookupDictGivenKeyValueDict(gsb(groupName, siteName, buildName))
  if not dictFound : return None
  return dictFound.get('data')


class test_lookupDictGivenLookupDict(unittest.TestCase):

  def test_basic(self):
    slod = SearchableListOfDicts(g_buildsListForExpectedBuilds,
      ['group', 'site', 'buildname'])
    self.assertEqual(slod.getListOfDicts(), g_buildsListForExpectedBuilds)
    self.assertEqual(len(slod), len(g_buildsListForExpectedBuilds))
    self.assertEqual(slod[0], g_buildsListForExpectedBuilds[0])
    self.assertEqual(slod[3], g_buildsListForExpectedBuilds[3])
    self.assertEqual(slodLookupData(slod, 'group1','site1','build1'), 'val1')
    self.assertEqual(slodLookupData(slod, 'group1','site2','build3'), 'val3')
    self.assertEqual(slodLookupData(slod, 'group2','site4','build1'), None)

  def test_iterator(self):
    slod = SearchableListOfDicts(g_buildsListForExpectedBuilds,
      ['group', 'site', 'buildname'])
    i = 0
    for dictEle in slod:
      self.assertEqual(dictEle, g_buildsListForExpectedBuilds[i])
      i += 1  

  def test_in(self):
    slod = SearchableListOfDicts(g_buildsListForExpectedBuilds,
      ['group', 'site', 'buildname'])
    self.assertEqual(g_buildsListForExpectedBuilds[0] in slod, True)
    self.assertEqual(g_buildsListForExpectedBuilds[2] in slod, True)
    dummyDict = copy.deepcopy(g_buildsListForExpectedBuilds[0])
    dummyDict['data'] = 'different_val'
    self.assertEqual(dummyDict in slod, False)


#############################################################################
#
# Test CDashQueryAnalizeReport.createBuildLookupDict()
#
#############################################################################

class test_createBuildLookupDict(unittest.TestCase):

  def test_1(self):
    buildLookupDict = createBuildLookupDict(g_buildsListForExpectedBuilds)
    #print("\nbuildLookupDict:")
    #g_pp.pprint(buildLookupDict)
    #print("\ng_buildLookupDictForExpectedBuilds:")
    #g_pp.pprint(g_buildLookupDictForExpectedBuilds)
    self.assertEqual(buildLookupDict, g_buildLookupDictForExpectedBuilds)


#############################################################################
#
# Test CDashQueryAnalizeReport.lookupBuildSummaryGivenLookupDict()
#
#############################################################################

def gsb(groupName, siteName, buildName):
  return {'group':groupName, 'site':siteName, 'buildname':buildName}

def lookupData(groupName, siteName, buildName, buildLookupDict):
  buildDict = lookupBuildSummaryGivenLookupDict(buildLookupDict,
    gsb(groupName, siteName, buildName) )
  if not buildDict : return None
  return buildDict.get('data')
     
class test_lookupBuildSummaryGivenLookupDict(unittest.TestCase):

  def test_1(self):
    blud = createBuildLookupDict(g_buildsListForExpectedBuilds)
    self.assertEqual(lookupData('group1','site1','build1', blud), 'val1')
    self.assertEqual(lookupData('group1','site1','build2', blud), 'val2')
    self.assertEqual(lookupData('group1','site2','build3', blud), 'val3')
    self.assertEqual(lookupData('group2','site1','build1', blud), 'val4')
    self.assertEqual(lookupData('group2','site3','build4', blud), 'val5')
    self.assertEqual(lookupData('group2','site3','build1', blud), None)
    self.assertEqual(lookupData('group2','site4','build1', blud), None)
    self.assertEqual(lookupData('group3','site1','build1', blud), None)


#############################################################################
#
# Test CDashQueryAnalizeReport.getMissingExpectedBuildsList()
#
#############################################################################
     
class test_getMissingExpectedBuildsList(unittest.TestCase):

  def test_1(self):
    blud = copy.deepcopy(createBuildLookupDict(g_buildsListForExpectedBuilds))
    blud.get('group2').get('site3').get('build4').update({'test':{'pass':1}})
    expectedBuildsList = [
      gsb('group1', 'site2', 'build3'),  # Build exists but missing tests
      gsb('group2', 'site3', 'build4'),  # Build exists and has tests
      gsb('group2', 'site3', 'build8'),  # Build missing all-together
      ]
    missingExpectedBuildsList = getMissingExpectedBuildsList(blud, expectedBuildsList)
    self.assertEqual(len(missingExpectedBuildsList), 2)
    self.assertEqual(missingExpectedBuildsList[0],
      { 'group':'group1', 'site':'site2', 'buildname':'build3',
        'status':"Build exists but no test results" } )
    self.assertEqual(missingExpectedBuildsList[1],
      { 'group':'group2', 'site':'site3', 'buildname':'build8',
        'status':"Build not found on CDash" } )


#############################################################################
#
# Test CDashQueryAnalizeReport.downloadBuildsOffCDashAndFlatten()
#
#############################################################################

class test_downloadBuildsOffCDashAndFlatten(unittest.TestCase):

  def test_allBuilds(self):
    # Define dummy CDash filter data
    cdashUrl = "site.come/cdash"
    projectName = "projectName"
    date = "YYYY-MM-DD"
    buildFilters = "build&filters"
    # Define mock object to return the data
    mockExtractCDashApiQueryDataFunctor = MockExtractCDashApiQueryDataFunctor(
       getCDashIndexQueryUrl(cdashUrl,  projectName, date, buildFilters),
       g_fullCDashIndexBuildsJson )
    # Get the mock data off of CDash
    summaryCDashIndexBuilds = downloadBuildsOffCDashAndFlatten(
      cdashUrl,  projectName, date, buildFilters,
      verbose=False, cdashQueriesCacheDir=None,
      useCachedCDashData=False,
      extractCDashApiQueryData_in=mockExtractCDashApiQueryDataFunctor )
    # Assert the data returned is correct
    #g_pp.pprint(summaryCDashIndexBuilds)
    self.assertEqual(
      len(summaryCDashIndexBuilds), len(g_summaryCDashIndexBuilds_expected))
    for i in range(0, len(summaryCDashIndexBuilds)):
      self.assertEqual(summaryCDashIndexBuilds[i], g_summaryCDashIndexBuilds_expected[i])


#############################################################################
#
# Test CDashQueryAnalizeReport.downloadTestsOffCDashQueryTestsAndFlatten()
#
#############################################################################

class test_downloadTestsOffCDashQueryTestsAndFlatten(unittest.TestCase):

  def test_all_tests(self):
    # Define dummy CDash filter data
    cdashUrl = "site.come/cdash"
    projectName = "projectName"
    date = "YYYY-MM-DD"
    nonpassingTestsFilters = "tests&filters"
    # cdash/api/v1/queryTests.php URL
    nonpassingTestsQueryUrl = getCDashQueryTestsQueryUrl(
      cdashUrl, projectName, date, nonpassingTestsFilters)
    # Define mock object to return the data
    mockExtractCDashApiQueryDataFunctor = MockExtractCDashApiQueryDataFunctor(
       nonpassingTestsQueryUrl, g_fullCDashQueryTestsJson )
    # Get the mock data off of CDash
    testsListOfDicts = downloadTestsOffCDashQueryTestsAndFlatten(
      nonpassingTestsQueryUrl, fullCDashQueryTestsJsonCacheFile=None,
      useCachedCDashData=False,
      verbose=False,
      extractCDashApiQueryData_in=mockExtractCDashApiQueryDataFunctor )
    # Assert the data returned is correct
    #g_pp.pprint(testsListOfDicts)
    self.assertEqual(
      len(testsListOfDicts), len(g_testsListOfDicts_expected))
    for i in range(0, len(testsListOfDicts)):
      self.assertEqual(testsListOfDicts[i], g_testsListOfDicts_expected[i])



#############################################################################
#
# Test CDashQueryAnalizeReport.buildHasConfigureFailures()
#
#############################################################################

class test_buildHasConfigureFailures(unittest.TestCase):

  def test_has_no_configure_failures(self):
    buildDict = copy.deepcopy(g_singleBuildPassesSummary)
    self.assertEqual(buildHasConfigureFailures(buildDict), False)

  def test_has_configure_failures(self):
    buildDict = copy.deepcopy(g_singleBuildPassesSummary)
    buildDict['configure']['error'] = 1
    self.assertEqual(buildHasConfigureFailures(buildDict), True)

  def test_has_no_configure_results(self):
    buildDict = copy.deepcopy(g_singleBuildPassesSummary)
    del buildDict['configure']
    self.assertEqual(buildHasConfigureFailures(buildDict), False)



#############################################################################
#
# Test CDashQueryAnalizeReport.buildHasBuildFailures()
#
#############################################################################

class test_buildHasBuildFailures(unittest.TestCase):

  def test_has_no_build_failures(self):
    buildDict = copy.deepcopy(g_singleBuildPassesSummary)
    self.assertEqual(buildHasBuildFailures(buildDict), False)

  def test_has_build_failures(self):
    buildDict = copy.deepcopy(g_singleBuildPassesSummary)
    buildDict['compilation']['error'] = 1
    self.assertEqual(buildHasBuildFailures(buildDict), True)

  def test_has_no_build_results(self):
    buildDict = copy.deepcopy(g_singleBuildPassesSummary)
    del buildDict['compilation']
    self.assertEqual(buildHasBuildFailures(buildDict), False)


#############################################################################
#
# Test CDashQueryAnalizeReport.getBuildsWtihConfigureFailures()
#
#############################################################################

def dummyBuildWithConfigureFailures(numConfigureFailures):
    buildDict = copy.deepcopy(g_singleBuildPassesSummary)
    buildDict['configure']['error'] = numConfigureFailures
    return buildDict

class test_getBuildsWtihConfigureFailures(unittest.TestCase):

  def test_1(self):
    bwcf = dummyBuildWithConfigureFailures
    buildDictList = [
      bwcf(1),
      bwcf(0),
      bwcf(2)
      ]
    buildWithConfigureFailuresList = getBuildsWtihConfigureFailures(buildDictList)
    buildWithConfigureFailuresList_expected = [
      bwcf(1),
      bwcf(2)
      ]
    self.assertEqual(buildWithConfigureFailuresList,
      buildWithConfigureFailuresList_expected)


#############################################################################
#
# Test CDashQueryAnalizeReport.getBuildsWtihConfigureFailures()
#
#############################################################################

def dummyBuildWithBuildFailures(numBuildFailures):
    buildDict = copy.deepcopy(g_singleBuildPassesSummary)
    buildDict['compilation']['error'] = numBuildFailures
    return buildDict

class test_getBuildsWtihBuildFailures(unittest.TestCase):

  def test_1(self):
    bwbf = dummyBuildWithBuildFailures
    buildDictList = [
      bwbf(1),
      bwbf(0),
      bwbf(2)
      ]
    buildWithBuildFailuresList = getBuildsWtihBuildFailures(buildDictList)
    buildWithBuildFailuresList_expected = [
      bwbf(1),
      bwbf(2)
      ]
    self.assertEqual(buildWithBuildFailuresList,
      buildWithBuildFailuresList_expected)


#############################################################################
#
# Test CDashQueryAnalizeReport.sortAndLimitListOfDicts()
#
#############################################################################

def createDictForTest(data1, data2, data3):
  return { 'key1':data1, 'key2':data2, 'key3':data3 }

def createDictForTestWithUrl(data1, data2, data3):
  return {
    'key1':data1[0], 'key1_url':data1[1],
    'key2':data2[0], 'key2_url':data2[1],
    'key3':data3[0], 'key3_url':data3[1],
    }
 
class test_sortAndLimitListOfDicts(unittest.TestCase):
  
  def test_no_sort_no_limit(self):
    cd = createDictForTest
    origList = [
      cd("c1_a", 3, "c2_b"),
      cd("c1_a", 1, "c2_c"),
      cd("c1_b", 2, "c2_a"),
      ]
    resultList = sortAndLimitListOfDicts(origList)
    resultList_expected = origList
    self.assertEqual(resultList, resultList_expected)
  
  def test_multicol_sort_no_limit(self):
    cd = createDictForTest
    origList = [
      cd("c1_a", 3, "c2_b"),
      cd("c1_b", 2, "c2_a"),
      cd("c1_a", 1, "c2_c"),
      ]
    resultList = sortAndLimitListOfDicts(origList,  ['key1', 'key2'])
    resultList_expected = [
      cd("c1_a", 1, "c2_c"),
      cd("c1_a", 3, "c2_b"),
      cd("c1_b", 2, "c2_a"),
      ]
    self.assertEqual(resultList, resultList_expected)
  
  def test_multicol_sort_limit_2(self):
    cd = createDictForTest
    origList = [
      cd("c1_a", 3, "c2_b"),
      cd("c1_b", 2, "c2_a"),
      cd("c1_a", 1, "c2_c"),
      ]
    resultList = sortAndLimitListOfDicts(origList,  ['key1', 'key2'], 2)
    resultList_expected = [
      cd("c1_a", 1, "c2_c"),
      cd("c1_a", 3, "c2_b"),
      ]
    self.assertEqual(resultList, resultList_expected)
  
  def test_multicol_sort_limit_3(self):
    cd = createDictForTest
    origList = [
      cd("c1_a", 3, "c2_b"),
      cd("c1_b", 2, "c2_a"),
      cd("c1_a", 1, "c2_c"),
      ]
    resultList = sortAndLimitListOfDicts(origList,  ['key1', 'key2'], 3)
    resultList_expected = [
      cd("c1_a", 1, "c2_c"),
      cd("c1_a", 3, "c2_b"),
      cd("c1_b", 2, "c2_a"),
      ]
    self.assertEqual(resultList, resultList_expected)
  
  def test_multicol_sort_limit_4(self):
    cd = createDictForTest
    origList = [
      cd("c1_a", 3, "c2_b"),
      cd("c1_b", 2, "c2_a"),
      cd("c1_a", 1, "c2_c"),
      ]
    resultList = sortAndLimitListOfDicts(origList,  ['key1', 'key2'], 4)
    resultList_expected = [
      cd("c1_a", 1, "c2_c"),
      cd("c1_a", 3, "c2_b"),
      cd("c1_b", 2, "c2_a"),
      ]
    self.assertEqual(resultList, resultList_expected)
  
  def test_multicol_sort_limit_0(self):
    cd = createDictForTest
    origList = [
      cd("c1_a", 3, "c2_b"),
      cd("c1_b", 2, "c2_a"),
      cd("c1_a", 1, "c2_c"),
      ]
    resultList = sortAndLimitListOfDicts(origList,  ['key1', 'key2'], 0)
    resultList_expected = []
    self.assertEqual(resultList, resultList_expected)
  
  def test_no_sort_limit_2(self):
    cd = createDictForTest
    origList = [
      cd("c1_a", 3, "c2_b"),
      cd("c1_a", 1, "c2_c"),
      cd("c1_b", 2, "c2_a"),
      ]
    resultList = sortAndLimitListOfDicts(origList, None, 2)
    resultList_expected = [
      cd("c1_a", 3, "c2_b"),
      cd("c1_a", 1, "c2_c"),
      ]
    self.assertEqual(resultList, resultList_expected)
  
  def test_sort_key2_no_limit(self):
    cd = createDictForTest
    origList = [
      cd("c1_a", 3, "c2_b"),
      cd("c1_a", 1, "c2_c"),
      cd("c1_b", 2, "c2_a"),
      ]
    resultList = sortAndLimitListOfDicts(origList, ['key2'])
    resultList_expected = [
      cd("c1_a", 1, "c2_c"),
      cd("c1_b", 2, "c2_a"),
      cd("c1_a", 3, "c2_b"),
      ]
    self.assertEqual(resultList, resultList_expected)


#############################################################################
#
# Test CDashQueryAnalizeReport.createHtmlTableStr()
#
#############################################################################
 
class test_createHtmlTableStr(unittest.TestCase):
  
  # Check that the contents are put in the right place, the correct alignment,
  # correct handling of non-string data, etc.
  def test_3x3_table_correct_contents(self):
    tcd = TableColumnData
    trd = createDictForTest
    colDataList = [
      tcd('key3', "Data 3"),
      tcd('key1', "Data 1"),
      tcd('key2', "Data 2", "right"),  # Alignment and non-string dat3
      ]
    rowDataList = [
      trd("r1d1", 1, "r1d3"),
      trd("r2d1", 2, "r2d3"),
      trd("r3d1", 3, "r3d3"),
      ]
    htmlTable = createHtmlTableStr("My great data", colDataList, rowDataList,
      htmlStyle="my_style",  # Test custom table style
      #htmlStyle=None,       # Uncomment to view this style
      #htmlTableStyle="",    # Uncomment to view this style
      )
    #print(htmlTable)
    #with open("test_3x2_table.html", 'w') as outFile: outFile.write(htmlTable)
    # NOTE: Above, uncomment the htmlStyle=None, ... line and the print and
    # file write commands to view the formatted table in a browser to see if
    # this gets the data right and you like the default table style.
    htmlTable_expected = \
r"""<style>my_style</style>
<h3>My great data</h3>
<table style="width:100%">

<tr>
<th>Data 3</th>
<th>Data 1</th>
<th>Data 2</th>
</tr>

<tr>
<td align="left">r1d3</td>
<td align="left">r1d1</td>
<td align="right">1</td>
</tr>

<tr>
<td align="left">r2d3</td>
<td align="left">r2d1</td>
<td align="right">2</td>
</tr>

<tr>
<td align="left">r3d3</td>
<td align="left">r3d1</td>
<td align="right">3</td>
</tr>

</table>

"""
    self.assertEqual(htmlTable, htmlTable_expected)

  # Check the correct default table style is set
  def test_1x1_table_correct_style(self):
    tcd = TableColumnData
    colDataList = [  tcd('key1', "Data 1") ]
    rowDataList = [ {'key1':'data1'} ]
    htmlTable = createHtmlTableStr("My great data", colDataList, rowDataList, htmlTableStyle="")
    #print(htmlTable)
    #with open("test_1x1_table_style.html", 'w') as outFile: outFile.write(htmlTable)
    # NOTE: Above, uncomment the print and file write to view the formatted
    # table in a browser to see if this gets the data right and you like the
    # default table style.
    htmlTable_expected = \
r"""<style>table, th, td {
  padding: 5px;
  border: 1px solid black;
  border-collapse: collapse;
}
tr:nth-child(even) {background-color: #eee;}
tr:nth-child(odd) {background-color: #fff;}
</style>
<h3>My great data</h3>
<table >

<tr>
<th>Data 1</th>
</tr>

<tr>
<td align="left">data1</td>
</tr>

</table>

"""
    self.assertEqual(htmlTable, htmlTable_expected)

  # Check that a bad column dict key name throws
  def test_1x1_bad_key_fail(self):
    tcd = TableColumnData
    colDataList = [  tcd('badKey', "Data 1") ]
    rowDataList = [ {'key1':'data1'} ]
    try:
      htmlTable = createHtmlTableStr("Title", colDataList, rowDataList)
      self.assertEqual("Excpetion did not get thrown!", "No it did not!")
    except Exception, errMsg:
      self.assertEqual(str(errMsg),
         "Error, column dict ='badKey' row 0 entry is 'None' which is"+\
         " not allowed! row dict = {'key1': 'data1'}")
  
  # Check that the contents are put in the right place, the correct alignment,
  # correct handling of non-string data, etc.
  def test_3x3_table_with_url_correct_contents(self):
    tcd = TableColumnData
    trdu = createDictForTestWithUrl
    colDataList = [
      tcd('key3', "Data 3"),
      tcd('key1', "Data 1"),
      tcd('key2', "Data 2", "right"),  # Alignment and non-string dat3
      ]
    rowDataList = [
      trdu(["r1d1","some.com/r1d1"], [1,"some.com/r1d2"], ["r1d3","some.com/r1d3"]),
      trdu(["r2d1","some.com/r2d1"], [2,"some.com/r2d2"], ["r2d3","some.com/r2d3"]),
      trdu(["r3d1","some.com/r3d1"], [3,"some.com/r3d2"], ["r3d3","some.com/r3d3"]),
      ]
    htmlTable = createHtmlTableStr("My great data", colDataList, rowDataList,
      htmlStyle="my_style",  # Test custom table style
      #htmlStyle=None,       # Uncomment to view this style
      htmlTableStyle="",    # Uncomment to view this style
      )
    #print(htmlTable)
    #with open("test_3x3_table_with_url_correct_contents.html", 'w') as outFile:
    #  outFile.write(htmlTable)
    # NOTE: Above, uncomment the htmlStyle=None, ... line and the print and
    # file write commands to view the formatted table in a browser to see if
    # this gets the data right and you like the default table style.
    htmlTable_expected = \
r"""<style>my_style</style>
<h3>My great data</h3>
<table >

<tr>
<th>Data 3</th>
<th>Data 1</th>
<th>Data 2</th>
</tr>

<tr>
<td align="left"><a href="some.com/r1d3">r1d3</a></td>
<td align="left"><a href="some.com/r1d1">r1d1</a></td>
<td align="right"><a href="some.com/r1d2">1</a></td>
</tr>

<tr>
<td align="left"><a href="some.com/r2d3">r2d3</a></td>
<td align="left"><a href="some.com/r2d1">r2d1</a></td>
<td align="right"><a href="some.com/r2d2">2</a></td>
</tr>

<tr>
<td align="left"><a href="some.com/r3d3">r3d3</a></td>
<td align="left"><a href="some.com/r3d1">r3d1</a></td>
<td align="right"><a href="some.com/r3d2">3</a></td>
</tr>

</table>

"""
    self.assertEqual(htmlTable, htmlTable_expected)












      

#############################################################################
#
# Test CDashQueryAnalizeReport.createCDashDataSummaryHtmlTableStr()
#
#############################################################################


def missingExpectedBuildsRow(groupName, siteName, buildName, missingStatus):
  return { 'group':groupName, 'site':siteName, 'buildname':buildName,
    'status':missingStatus }

class test_getCDashDataSummaryHtmlTableTitleStr(unittest.TestCase):

  def test_no_limitRowsToDisplay(self):
    self.assertEqual(
      getCDashDataSummaryHtmlTableTitleStr("data name", "dac", 30),
      "data name: dac=30" )

  def test_limitRowsToDisplay(self):
    self.assertEqual(
      getCDashDataSummaryHtmlTableTitleStr("data name", "dac", 30, 15),
      "data name (limited to 15): dac=30" )

class test_DictSortFunctor(unittest.TestCase):

  def test_call(self):
    meb = missingExpectedBuildsRow
    row = meb("group1", "site1", "build2", "Build exists but not tests")
    sortKeyFunctor = DictSortFunctor(['group', 'site', 'buildname'])
    sortKey = sortKeyFunctor(row)
    self.assertEqual(sortKey, "group1-site1-build2")
    
  def test_sort(self):
    meb = missingExpectedBuildsRow
    rowDataList = [
      meb("group1", "site1", "build2", "Build exists but not tests"),
      meb("group1", "site1", "build1", "Build is missing"),
      ]
    sortKeyFunctor = DictSortFunctor(['group', 'site', 'buildname'])
    rowDataList.sort(key=sortKeyFunctor)
    rowDataList_expected = [
      meb("group1", "site1", "build1", "Build is missing"),
      meb("group1", "site1", "build2", "Build exists but not tests"),
      ]
    self.assertEqual(rowDataList, rowDataList_expected)
   
   
class test_createCDashDataSummaryHtmlTableStr(unittest.TestCase):

  def test_2x4_missing_expected_builds(self):
    tcd = TableColumnData
    meb = missingExpectedBuildsRow
    colDataList = [
      tcd('group', "Group"),
      tcd('site', "Site"),
      tcd('buildname', "Build Name"),
      tcd('status', "Missing Status"),
      ]
    rowDataList = [
      meb("group1", "site1", "build2", "Build exists but not tests"),
      meb("group1", "site1", "build1", "Build is missing"),  # Should be listed first!
      ]
    rowDataListCopy = copy.deepcopy(rowDataList)  # Make sure a copy is sorted!
    htmlTable = createCDashDataSummaryHtmlTableStr(
      "Missing expected builds", "bme",
      colDataList, rowDataList,
      ['group', 'site', 'buildname'],
      #htmlStyle="my_style",  # Don't check default style
      #htmlStyle=None,       # Uncomment to view this style
      #htmlTableStyle="",    # Uncomment to view this style
      )
    #print(htmlTable)
    #with open("test_2x4_missing_expected_builds.html", 'w') as outFile: outFile.write(htmlTable)
    # NOTE: Above, uncomment the htmlStyle=None, ... line and the print and
    # file write commands to view the formatted table in a browser to see if
    # this gets the data right and you like the default table style.
    htmlTable_expected = \
r"""<style>table, th, td {
  padding: 5px;
  border: 1px solid black;
  border-collapse: collapse;
}
tr:nth-child(even) {background-color: #eee;}
tr:nth-child(odd) {background-color: #fff;}
</style>
<h3>Missing expected builds: bme=2</h3>
<table style="width:100%">

<tr>
<th>Group</th>
<th>Site</th>
<th>Build Name</th>
<th>Missing Status</th>
</tr>

<tr>
<td align="left">group1</td>
<td align="left">site1</td>
<td align="left">build1</td>
<td align="left">Build is missing</td>
</tr>

<tr>
<td align="left">group1</td>
<td align="left">site1</td>
<td align="left">build2</td>
<td align="left">Build exists but not tests</td>
</tr>

</table>

"""
    self.assertEqual(htmlTable, htmlTable_expected)
    self.assertEqual(rowDataList, rowDataListCopy)   # Make sure not sorting in place

# ToDo: Test without sorting

# ToDo: Test with limitRowsToDisplay > len(rowDataList)

# ToDo: Test with limitRowsToDisplay == len(rowDataList)

# ToDo: Test with limitRowsToDisplay < len(rowDataList)

# ToDo: Test with now rows and therefore now table printed


#
# Run the unit tests!
#

if __name__ == '__main__':

  unittest.main()
