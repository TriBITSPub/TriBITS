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

try:
  # Python 2
  from urllib2 import urlopen
except ImportError:
  # Python 3
  from urllib.request import urlopen

import json
import datetime
import copy
import pprint

from FindGeneralScriptSupport import *
from GeneralScriptSupport import *

# Validate a date format
def validateYYYYMMDD(dateText):
  try:
    return datetime.datetime.strptime(dateText, '%Y-%m-%d')
  except ValueError:
    raise ValueError("Incorrect data format for '"+dateText+"', should be YYYY-MM-DD")


# Given a CDash query URL, return the full Python CDash data-structure
def extractCDashApiQueryData(cdashApiQueryUrl):
  #print sys.version_info
  if sys.version_info < (2,7,9):
    raise Exception("Error: Must be using Python 2.7.9 or newer")
  # NOTE: If we use Python 2.6.6. then the urllib2 function crashes!
  response = urlopen(cdashApiQueryUrl)
  return json.load(response)


# Color HTML text in red
def makeHtmlTextRed(htmlText):
  return("<font color=\"red\">"+htmlText+"</font>")


# Read a CSV file into a list of dictionaries for each row where the rows of
# the output list are dicts with the column names as keys.
#
# For example, for the CSV file:
#
#   col_0, col_1, col_2
#   val_00, val_01, val_02
#   val_10, val_11, val_12
#
# the returned list of dicts will be:
#
#  [
#    { 'col_0':'val_00', 'col_1':'val_01', 'col_2':'val_02' }, 
#    { 'col_0':'val_10', 'col_1':'val_11', 'col_2':'val_12' }, 
#    ]
#
# and the expected list of column headers would be:
#
#   expectedColumnHeadersList = [ 'col_0', 'col_1', 'col_2' ]
#
# But the expectedColumnHeadersList argument is optional.
#
def readCsvFileIntoListOfDicts(csvFileName, expectedColumnHeadersList=None):
  listOfDicts = []
  with open(csvFileName, 'r') as csvFile:
    # Get the list of column headers
    columnHeadersLineStr = csvFile.readline().strip()
    columnHeadersRawStrList = columnHeadersLineStr.split(',')
    columnHeadersList = []
    for headerRawStr in columnHeadersRawStrList:
      columnHeadersList.append(headerRawStr.strip())
    if expectedColumnHeadersList:
      if len(columnHeadersList) != len(expectedColumnHeadersList):
        raise Exception(
          "Error, for CSV file '"+csvFileName+"' the"+\
          " column headers '"+str(columnHeadersList)+"' has"+\
          " "+str(len(columnHeadersList))+" items but the expected"+\
          " set of column headers '"+str(expectedColumnHeadersList)+"'"+\
          " has "+str(len(expectedColumnHeadersList))+" items!")
      for i in range(len(columnHeadersList)):
        if columnHeadersList[i] != expectedColumnHeadersList[i]:
          raise Exception(
            "Error, column header "+str(i)+" '"+columnHeadersList[i]+"' does"+\
            " not match expected column header '"+expectedColumnHeadersList[i]+"'!")
    # Read the rows of the CSV file into dicts
    dataRow = 0
    line = csvFile.readline().strip()
    while line:
      #print("\ndataRow = "+str(dataRow))
      lineList = line.split(',')
      #print(lineList)
      # Assert that the row has the right number of entries
      if len(lineList) != len(columnHeadersList):
        raise Exception(
          "Error, data row "+str(dataRow)+" '"+line+"' has"+\
          " "+str(len(lineList))+" entries which does not macth"+\
          " the number of column headers "+str(len(columnHeadersList))+"!")
      # Read the row entries into a new dict
      rowDict = {}
      for j in range(len(columnHeadersList)):
        rowDict.update( { columnHeadersList[j] : lineList[j].strip() } )
      #print(rowDict)
      listOfDicts.append(rowDict)
      # Update for next row
      line = csvFile.readline().strip()
      dataRow += 1
  # Return the constructed object
  return listOfDicts


# Get list of expected builds from CSV file
def getExpectedBuildsListfromCsvFile(expectedBuildsFileName):
  return readCsvFileIntoListOfDicts(expectedBuildsFileName,
    ['group', 'site', 'buildname'])


# Print print a nested Python data-structure to a file
#
# ToDo: Reimplement this to create a better looking set of indented that that
# involves less right-drift and the expense of more vertical space.
def pprintPythonData(pythonData, filePath):
  pp = pprint.PrettyPrinter(stream=open(filePath,'w'), indent=2)
  pp.pprint(pythonData)


# Get data off CDash and cache it or read from previously cached data
#
# This function can be used to get data off of CDash using any page on CDash
# including cdash/api/v1/index.php, cdash/api/v1/queryTests.php and anything
# other PHP page that returns a JSON data structure (which is all of the
# cdash/api/v1/XXX.php pages).
def getAndCacheCDashQueryDataOrReadFromCache(
  cdashQueryUrl,
  cdashQueryDataCacheFile,  # File name
  useCachedCDashData,  # If 'True', then cdasyQueryDataCacheFile must be non-null
  printCDashUrl = False,
  extractCDashApiQueryData_in=extractCDashApiQueryData,
  ):
  if useCachedCDashData:
    if printCDashUrl:
      print("Using cached data from:\n\n  " + cdashQueryUrl )
    cdashQueryData=eval(open(cdashQueryDataCacheFile, 'r').read())
  else:
    if printCDashUrl:
      print("Getting bulid data from:\n\n  " + cdashQueryUrl )
    cdashQueryData = extractCDashApiQueryData_in(cdashQueryUrl)
    if cdashQueryDataCacheFile:
      pprintPythonData(cdashQueryData, cdashQueryDataCacheFile) 
  return cdashQueryData


# Construct full cdash/api/v1/index.php query URL to pull data down given the
# pieces
def getCDashIndexQueryUrl(cdashUrl, projectName, date, filterFields):
  return cdashUrl+"/api/v1/index.php?project="+projectName+"&date="+date \
    + "&"+filterFields


# Construct full cdash/index.php browser URL given the pieces
def getCDashIndexBrowserUrl(cdashUrl, projectName, date, filterFields):
  return cdashUrl+"/index.php?project="+projectName+"&date="+date \
    + "&"+filterFields


# Construct full cdash/api/v1/queryTests.php query URL given the pieces
def getCDashQueryTestsQueryUrl(cdashUrl, projectName, date, filterFields):
  return cdashUrl+"/api/v1/queryTests.php?project="+projectName+"&date="+date \
    + "&"+filterFields


# Construct full cdash/queryTests.php browser URL given the pieces
def getCDashQueryTestsBrowserUrl(cdashUrl, projectName, date, filterFields):
  return cdashUrl+"/queryTests.php?project="+projectName+"&date="+date \
    + "&"+filterFields


# Copy a key/value pair from one dict to another if it eixsts
def copyKeyDictIfExists(sourceDict_in, keyName_in, dict_inout):
  value = sourceDict_in.get(keyName_in, None)
  if value:
    dict_inout.update( { keyName_in : value } )


# Collect CDash index.php build summary fields
#
# Change this to get all of the fields and add the 'group' field as well.
def collectCDashIndexBuildSummaryFields(fullCDashIndexBuild, groupName):
  summaryBuild = { u'group' : groupName }
  copyKeyDictIfExists(fullCDashIndexBuild, u'site', summaryBuild)
  copyKeyDictIfExists(fullCDashIndexBuild, u'buildname', summaryBuild)
  copyKeyDictIfExists(fullCDashIndexBuild, u'update', summaryBuild)
  copyKeyDictIfExists(fullCDashIndexBuild, u'configure', summaryBuild)
  copyKeyDictIfExists(fullCDashIndexBuild, u'compilation', summaryBuild)
  copyKeyDictIfExists(fullCDashIndexBuild, u'test', summaryBuild)
  return summaryBuild


# Given the full JSON data-structure returned from the page
# cdash/api/v1/index.php query, return an flattened-out data-structure that is
# easier to manipulate.
#
# This function takes in the JSON data-structure (as a nested set of Python
# dicts and listed) directly returned from a query gotten from the page
# cdash/api/v1/index.php with some filters.
#
# The input full CDash index.php JSON data-structure has the following
# structure and fields of interest:
#
#  fullCDashIndexBuildsJson =
#  {
#    'all_buildgroups': [ {'id':1,'name:"Nightly"}, ...],
#    'buildgroups': [
#      {
#        'name':"???",   # group name, e.g. Nightly
#        'builds":[
#          {
#            'site':"???"
#            'buildname':"???",
#            'update': {'errors':???, ...},
#            'configure':{'error': ???, ...},
#            'compilation':{'error': ???, ...},
#            'test': {'fail':???, 'notrun':???, 'pass':???, ...},
#            ...
#            },
#            ...
#          ]
#        },
#        ...
#      ...
#      ]
#      },
#      ...
#    }
#
# This function gets the data from *all* of the collapsed builds and returns
# the flatten-out list of dicts for each build with the 'group' field added in
# as:
#
#   [
#     {
#       'group':"???",
#       'site':"???",
#       'buildname':"???",
#       'update': {'errors':???, ...},
#       'configure':{'error': ???, ...},
#       'compilation':{'error': ???, ...},
#       'test': {'fail':???, 'notrun':???, 'pass':???, ...},
#       ...
#       },
#     ...
#     ]
#
# This collects *all* of the builds from all of the build groups provided by
# that data-structure, not just the 'Nighlty' build group.  Therefore, if you
# want to only consider one set of build groups, you need to add that to the
# CDash query URL (e.g. group='Nighlty').
#
def flattenCDashIndexBuildsToListOfDicts(fullCDashIndexBuildsJson):
  summaryCDashIndexBuilds = []
  for buildgroup in fullCDashIndexBuildsJson["buildgroups"]:
    groupName = buildgroup["name"]
    for build in buildgroup["builds"]:
      summaryBuild = collectCDashIndexBuildSummaryFields(build, groupName)
      summaryCDashIndexBuilds.append(summaryBuild)
  return summaryCDashIndexBuilds

# Given the full JSON data-structure returned from the page
# cdash/api/v1/queryTests.php query, return an flattened-out data-structure
# that is easier to manipulate.
#
# This function takes in the JSON data-structure (as a nested set of Python
# dicts and listed) directly returned from a query gotten from the page
# cdash/api/v1/queryTests.php with some filters.
#
# The input full CDash queryTests.php JSON data-structure has the following
# structure and fields of interest:
#
#  fullCDashQueryTestsJson =
#  {
#    'version':???,
#    'feed_enabled':???,
#    ...
#    'builds': [
#      {
#        'buildName': 'Trilinos-atdm-mutrino-intel-opt-openmp-HSW',
#        'buildSummaryLink': 'buildSummary.php?buildid=4109735',
#        'buildstarttime': '2018-10-29T05:54:03 UTC',
#        'details': 'Completed (Failed)\n',
#        'nprocs': 4,
#        'prettyProcTime': '40s 400ms',
#        'prettyTime': '10s 100ms',
#        'procTime': 40.4,
#        'site': 'mutrino',
#        'siteLink': 'viewSite.php?siteid=223',
#        'status': 'Failed',
#        'statusclass': 'error',
#        'testDetailsLink': 'testDetails.php?test=57925465&build=4109735',
#        'testname': 'Anasazi_Epetra_BKS_norestart_test_MPI_4',
#        'time': 10.1
#        },
#      ...
#      ],
#    ...
#    }
#
# This function gets the data from *all* of the tests and returns the
# flatten-out list of dicts for each test:
#
#   [
#     {
#       'buildName': 'Trilinos-atdm-mutrino-intel-opt-openmp-HSW',
#       'buildSummaryLink': 'buildSummary.php?buildid=4109735',
#       'buildstarttime': '2018-10-29T05:54:03 UTC',
#       'details': 'Completed (Failed)\n',
#       'nprocs': 4,
#       'prettyProcTime': '40s 400ms',
#       'prettyTime': '10s 100ms',
#       'procTime': 40.4,
#       'site': 'mutrino',
#       'siteLink': 'viewSite.php?siteid=223',
#       'status': 'Failed',
#       'statusclass': 'error',
#       'testDetailsLink': 'testDetails.php?test=57925465&build=4109735',
#       'testname': 'Anasazi_Epetra_BKS_norestart_test_MPI_4',
#       'time': 10.1
#       },
#     ...
#     ]
#
# NOTE: This does a shallow copy so any modifications to the returned list and
# dicts will modify the original data-structure fullCDashQueryTestsJson.
#
# This collects *all* of the tests from all of the "build" list provided by
# the CDash JSON data-structure.  Therefore, if you want to only consider one
# set of build groups, you need to add that to the CDash query URL
# (e.g. buildName='<build-name>').
#
def flattenCDashQueryTestsToListOfDicts(fullCDashQueryTestsJson):
  testsListOfDicts = fullCDashQueryTestsJson['builds']
  return testsListOfDicts


# Create a lookup dict for builds "group" => "site" => "build" given summary
# list of builds.
def createBuildLookupDict(summaryBuildsList):
  buildLookupDict = {}
  for buildSummaryDict in summaryBuildsList:
    groupName = buildSummaryDict.get('group')
    siteName = buildSummaryDict.get('site')
    buildName = buildSummaryDict.get('buildname')
    groupDict = buildLookupDict.setdefault(groupName, {})
    siteDict = groupDict.setdefault(siteName, {})
    siteDict.setdefault(buildName, buildSummaryDict)
  return buildLookupDict


# Lookup a build dict given a lookup dict from createBuildLookupDict()
def lookupBuildSummaryGivenLookupDict(groupSiteBuildDict, buildLookupDict):
  groupDict = buildLookupDict.get(groupSiteBuildDict.get('group'), None)
  if not groupDict: return None
  siteDict = groupDict.get(groupSiteBuildDict.get('site'), None)
  if not siteDict: return None
  buildDict = siteDict.get(groupSiteBuildDict.get('buildname'), None)
  return buildDict


# Gather up a list of the missing builds.
#
# Inputs:
#
#   buildLookupDict [in]: Lookup dict of build summary dicts gotten off CDash
#   
#   expectedBuildsList [in]: List of expected builds dict with fields 'group',
#   'site', and 'buildname'.
#
# Returns an array of dicts of missing expected builds with list elements:
#
#    {'group':"???", 'site':"???", 'buildname':"???", 'status':"???", ...}
#
# wher the '...' will be the rest of the fields for builds that exist on CDash
# but don't have full results.
#
# The field 'status' will either be given either:
#
#   "Build not found on CDash"
#
# or
#
#   "Build exists but no test results"
#
# ToDo: Change name of 'status' to 'build_missing_status' and add other
# 'build_missing_status' values like:
#
#   "Build exists but no build results"
#   "Build exists but no configure results"
#
def getMissingExpectedBuildsList(buildLookupDict, expectedBuildsList):
  missingExpectedBuildsList = []
  for expectedBuildDict in expectedBuildsList:
    #print("\nexpectedBuildDict = "+str(expectedBuildDict))
    buildSummaryDict = \
      lookupBuildSummaryGivenLookupDict(expectedBuildDict, buildLookupDict)
    #print("buildSummaryDict = "+str(buildSummaryDict))
    if not buildSummaryDict:
      # Expected build not found!
      missingExpectedBuildDict = copy.deepcopy(expectedBuildDict)
      missingExpectedBuildDict.update({'status':"Build not found on CDash"})
      #print("missingExpectedBuildDict = "+str(missingExpectedBuildDict))
      missingExpectedBuildsList.append(missingExpectedBuildDict)
    elif not buildSummaryDict.get('test', None):
      # Build exists but it is missing tests!
      missingExpectedBuildDict = copy.deepcopy(expectedBuildDict)
      missingExpectedBuildDict.update({'status':"Build exists but no test results"})
      #print("missingExpectedBuildDict = "+str(missingExpectedBuildDict))
      missingExpectedBuildsList.append(missingExpectedBuildDict)
    else:
      # This build exists and it has test results so don't add it
      None
  # Return the list of missing expected builds and status
  return missingExpectedBuildsList


# Download set of builds from CDash builds and return flattened list of dicts
#
# The cdash/api/v1/index.php query URL is built using the arguments:
#
#   cdashUrl,  projectName, date, buildFilterFields
#
# If printCDashUrl==True, the the CDash query URL will be printed to STDOUT.
# Otherwise, this function is silent and will not return any output to STDOUT.
#
# If cdashQueriesCacheDir != None, then the raw JSON data-structure will be
# written to the file cdashQueriesCacheDir/fullCDashIndexBuilds.json.
#
# ToDo: Pass in the full path to the JSON cache file and don't assume the
# total file.
#
# If useCachedCDashData==True, then data will not be pulled off of CDash and
# instead the list of builds will be read from the file
# cdashQueriesCacheDir/fullCDashIndexBuilds.json must already exist from a
# prior call to this function (mostly for debugging and unit testing
# purposes).
# 
# The list of builds pulled off of CDash flattended and summmerized form
# extracted by the funtion flattenCDashIndexBuildsToListOfDicts() (with
# 'group', 'site', 'buildname' and update, configure, build, test and other
# results for the build).
#
# NOTE: The optional argument extractCDashApiQueryData_in is used in unit
# testing to avoid calling CDash.
#
# ToDo: Pass in the full cdashQueryUrl.
#
def downloadBuildsOffCDashAndFlatten(
  cdashUrl,  projectName, date, buildFilters,
  verbose=True,
  cdashQueriesCacheDir=None,
  useCachedCDashData=False,
  extractCDashApiQueryData_in=extractCDashApiQueryData,
  ):
  # Get the query data
  cdashQueryUrl = getCDashIndexQueryUrl(cdashUrl, projectName, date, buildFilters)
  if cdashQueriesCacheDir:
    fullCDashIndexBuildsJsonCacheFile=cdashQueriesCacheDir+"/fullCDashIndexBuilds.json"
  else:
    fullCDashIndexBuildsJsonCacheFile = None
  fullCDashIndexBuildsJson = getAndCacheCDashQueryDataOrReadFromCache(
    cdashQueryUrl, fullCDashIndexBuildsJsonCacheFile, useCachedCDashData,
    verbose, extractCDashApiQueryData_in )
  # Get trimmed down set of builds
  summaryCDashIndexBuilds = \
    flattenCDashIndexBuildsToListOfDicts(fullCDashIndexBuildsJson)
  return summaryCDashIndexBuilds


# Download set of tests from cdash/api/v1/ctest/queryTests.php and return
# flattened list of dicts
#
# cdashQueryTestsUrl [in]: String URL for cdash/api/v1/ctest/queryTests.php
# with filters.
#
# If printCDashUrl==True, the the CDash query URL will be printed to STDOUT.
# Otherwise, this function is silent and will not return any output to STDOUT.
#
# If fullCDashQueryTestsJsonCacheFile != None, then the raw JSON
# data-structure will be written to that file.
#
# If useCachedCDashData==True, then data will not be pulled off of CDash and
# instead the list of builds will be read from the file cdashQueryCacheFile
# which must already exist from a prior call to this function (mostly for
# debugging and unit testing purposes).
# 
# The list of tests pulled off CDash is flattended and returned by the
# function flattenCDashQueryTestsToListOfDicts().
#
# NOTE: The optional argument extractCDashApiQueryData_in is used in unit
# testing to avoid calling CDash.
#
def downloadTestsOffCDashQueryTestsAndFlatten(
  cdashQueryTestsUrl,
  fullCDashQueryTestsJsonCacheFile=None,
  useCachedCDashData=False,
  verbose=True,
  extractCDashApiQueryData_in=extractCDashApiQueryData,
  ):
  # Get the query data
  fullCDashQueryTestsJson = getAndCacheCDashQueryDataOrReadFromCache(
    cdashQueryTestsUrl, fullCDashQueryTestsJsonCacheFile, useCachedCDashData,
    verbose, extractCDashApiQueryData_in )
  # Get flattend set of tests
  #testsListOfDicts = \
  #  flattenCDashIndexBuildsToListOfDicts(fullCDashQueryTestsJson)
  #return testsListOfDicts
  return []


# Return if a build has configure failures
def buildHasConfigureFailures(buildDict):
  configureDict = buildDict.get('configure', None)
  if configureDict and configureDict['error'] > 0:
    return True
  return False


# Return if a build has compilation failures
def buildHasBuildFailures(buildDict):
  compilationDict = buildDict.get('compilation', None)
  if compilationDict and compilationDict['error'] > 0:
    return True
  return False


# Get a list of builds with configure failures
def getBuildsWtihConfigureFailures(buildDictList):
  pp = pprint.PrettyPrinter(indent=2)
  #print("\nbuildDictList:")
  #pp.pprint(buildDictList)
  buildsWithConfigureFailures = []
  for buildDict in buildDictList:
    #print("\nbuildDict:")
    #pp.pprint(buildDict)
    if buildHasConfigureFailures(buildDict):
      buildsWithConfigureFailures.append(buildDict)
  return buildsWithConfigureFailures


# Get a list of builds with configure failures
def getBuildsWtihBuildFailures(buildDictList):
  buildsWithBuildFailures = []
  for buildDict in buildDictList:
    if buildHasBuildFailures(buildDict):
      buildsWithBuildFailures.append(buildDict)
  return buildsWithBuildFailures


# Functor class to sort a row of dicts by multiple columns of string data.
class DictSortFunctor(object):
  def __init__(self, sortKeyList):
    self.sortKeyList = sortKeyList
  def __call__(self, dict_in):
    sortKeyStr=""
    for key in self.sortKeyList:
      keyData = dict_in.get(key)
      if sortKeyStr:
        sortKeyStr += "-"+str(keyData)
      else:
        sortKeyStr = keyData
    return sortKeyStr


# Sort and limit a list of dicts
#
# Arguments:
#
# listOfDicts [in]: List of dicts that will be sorted according to keys.
#
# sortKeyList [in]: List of dict keys that define the sort order for the data
# in the list.  The default is None which means that no sort is performed.
#
# limitRowsToDisplay [in]: The max number of rows to display.  The default is
# None which will result in no limit to the number of rows displayed.  The top
# limitRowsToDisplay items will be dispalyed after the list is sorted.
#
def sortAndLimitListOfDicts(listOfDicts, sortKeyList = None,
  limitRowsToDisplay = None\
  ):
  # Sort the list
  if sortKeyList:
    listOfDictsOrdered = copy.copy(listOfDicts)  # Shallow copy
    listOfDictsOrdered.sort(key=DictSortFunctor(sortKeyList))
  else:
    listOfDictsOrdered = listOfDicts  # No sort being done
  # Limit rows
  if limitRowsToDisplay == None:
    listOfDictsLimited = listOfDictsOrdered
  else:
    listOfDictsLimited = listOfDictsOrdered[0:limitRowsToDisplay]
  # Return the final sorted limited list
  return listOfDictsLimited


# Class to store dict key and table header
class TableColumnData(object):
  validColAlignList=["left","right","center","justify","char"]
  def __init__(self, dictKey, colHeader, colAlign="left"):
    self.dictKey = dictKey
    self.colHeader = colHeader
    if not colAlign in self.validColAlignList:
      raise Excpetion(
        "Error, colAlign="+colAlign+" not valid.  Please choose from"+\
        " the list ['" + "', '".join(validColAlignList) + "']!" )
    self.colAlign = colAlign


# Create an html table string from a list of dicts and column headers.
#
# Arguments:
#
# tableTitle [in]: String for the name of the table included at the top of the
# table.
# 
# colDataList [in]: List of TableColumnData objects where
#   colDataList[j].dictKey gives the name of the key for that column of data,
#   colDataList[j].colHeader is the text name for the column header and
#   colDataList[j].colAlign gives the HTML alignment.  That columns in the
#   table will listed in the order given in this list.
#
# rowDataList [in]: List of dicts that provide the data from the table.  The
#   dict in each row must have the keys specified by colData[j].dictKey.  In
#   addition, if (key_url=rowDataList[i].get(colData[j].dictKey+"_url",#
#   None))!=None, then the table entry will be an HTML link <a
#   href="dataRowList[i].get(key_url)">dataRowList[i].get(key)</a>.
#
# htmlStyle [in]: The HTML style data (between <style></style>.  If None is
# passed in then a default style is provided internally.
#
# htmlTableStyle [in]: The style for the HTML table used in <table
#   style=htmlTableStyle>.  If set to None, then a default style is used.  To
#   not set a style, pass in the empty string "" (not None).
#
def createHtmlTableStr(tableTitle, colDataList, rowDataList,
  htmlStyle=None, htmlTableStyle=None \
  ):

  # style options for the table
  defaultHtmlStyle=\
    "table, th, td {\n"+\
    "  padding: 5px;\n"+\
    "  border: 1px solid black;\n"+\
    "  border-collapse: collapse;\n"+\
    "}\n"+\
    "tr:nth-child(even) {background-color: #eee;}\n"+\
    "tr:nth-child(odd) {background-color: #fff;}\n"
  if htmlStyle != None: htmlStyleUsed = htmlStyle
  else: htmlStyleUsed = defaultHtmlStyle
  htmlStr="<style>"+htmlStyleUsed+"</style>\n"

  # Table title and <table style=...>
  htmlStr+="<h3>"+tableTitle+"</h3>\n"
  if htmlTableStyle != None: htmlTableStyleUsed = htmlTableStyle
  else: htmlTableStyleUsed = "style=\"width:100%\""
  htmlStr+="<table "+htmlTableStyleUsed+">\n\n"

  # Column headings:
  htmlStr+="<tr>\n"
  for colData in colDataList:
    htmlStr+="<th>"+colData.colHeader+"</th>\n"
  htmlStr+="</tr>\n\n"

  # Rows for the table
  row_i = 0
  for rowData in rowDataList:
    #print("\nrowData = "+str(rowData))
    htmlStr+="<tr>\n"
    for colData in colDataList:
      dictKey = colData.dictKey
      #print("\ndictKey = "+dictKey)
      # Get the raw entry for this column
      entry = rowData.get(dictKey, None)
      if entry == None:
        raise Exception(
          "Error, column dict ='"+colData.dictKey+"' row "+str(row_i)+\
          " entry is 'None' which is not allowed! row dict = "+str(rowData))  
      # See if the _url key also exists
      dictKey_url = dictKey+"_url"
      #print("dictKey_url = "+dictKey_url)
      entry_url = rowData.get(dictKey_url, None)
      #print("entry_url = "+str(entry_url))
      # Set the text for this row/column entry with or without the hyperlink
      if entry_url:
        entryStr = "<a href=\""+entry_url+"\">"+str(entry)+"</a>"
      else:
        entryStr = entry
      #print("entryStr = "+entryStr)
      # Set the row entry in the HTML table
      htmlStr+=\
        "<td align=\""+colData.colAlign+"\">"+\
        str(entryStr)+\
        "</td>\n"
    htmlStr+="</tr>\n\n"
    row_i += 1

  # End of table
  htmlStr+="</table>\n\n"  # Use two newlines makes for good formatting!
  return(htmlStr)


# Get string for table title for CDash data to display
#
# Arguments:
#
# Arguments:
#
# dataTitle [in]: Name of the data category.
#
# dataCountAcronym [in]: Acronym for the type of data being displayed
# (e.g. 'twoi' for "Tests With Out issue trackers").  This is printed in the
# table title in the form dataCoutAcronym=len(rowDataList).
#
# numItems [in]: The number of items of data
#
def getCDashDataSummaryHtmlTableTitleStr(dataTitle, dataCountAcronym, numItems,
  limitRowsToDisplay=None \
  ):
  tableTitle = dataTitle
  if limitRowsToDisplay:
    tableTitle += " (limited to "+str(limitRowsToDisplay)+")"
  tableTitle += ": "+dataCountAcronym+"="+str(numItems)
  return tableTitle


# Create an html table string for CDash summary data.
#
# Arguments:
#
# dataTitle [in]: Name of the data that we be included in the table title.
#
# dataCountAcronym [in]: Acronym for the type of data being displayed
# (e.g. 'twoi' for "Tests With Out issue trackers").  This is printed in the
# table title in the form dataCoutAcronym=len(rowDataList).
#
# colDataList [in]: List of TableColumnData objects where
#   colDataList[j].dictKey gives the name of the key for that column of data,
#   colDataList[j].colHeader is the text name for the column header and
#   colDataList[j].colAlign gives the HTML alignment.  That columns in the
#   table will listed in the order given in this list.
#
# rowDataList [in]: List of dicts that provide the data from the table.  The
#   dict in each row must have the keys specified by colData[j].dictKey.
#
# sortKeyList [in]: List of dict keys that define the sort order for the data
# in the list.  The default is None which means that no sort is performed.
#
# limitRowsToDisplay [in]: The max number of rows to display.  The default is
# None which will result in no limit to the number of rows displayed.  The top
# limitRowsToDisplay items will be dispalyed after the list is sorted.
#
# htmlStyle [in]: The HTML style data (between <style></style>.  If None is
# passed in then a default style is provided internally (see
# createHtmlTableStr().
#
# htmlTableStyle [in]: The style for the HTML table used in <table
#   style=htmlTableStyle>.  The default is None in which case a default is
#   picked by createHtmlTableStr(().
#
# NOTE: If len(rowDataList) == 0, then the empty string "" is returned.
# 
# ToDo: Add an argument to sort the data based on some given ordering of keys.
#
def createCDashDataSummaryHtmlTableStr(dataTitle, dataCountAcronym,
  colDataList, rowDataList, sortKeyList = None, limitRowsToDisplay = None,
  htmlStyle=None, htmlTableStyle=None \
  ):
  # If no rows, don't create a table
  if len(rowDataList) == 0:
    return ""
  # Sort the list and limit the list
  rowDataListDisplayed = sortAndLimitListOfDicts(
    rowDataList, sortKeyList, limitRowsToDisplay)
  # Table title
  tableTitle = getCDashDataSummaryHtmlTableTitleStr(
    dataTitle, dataCountAcronym, len(rowDataList), limitRowsToDisplay )

  # Create and return the table
  return createHtmlTableStr( tableTitle,
    colDataList, rowDataListDisplayed, htmlStyle, htmlTableStyle )


#




########################################################################
#
# Joe's CDash test test query and analysis code
#
# ToDo: Once under some basic testing, refactor to reduce duplication and
# improve consistency.
#
########################################################################


# This will return a dictionary with information about all the tests that were returned
# in the json from cdash as a result of the CDash query from the given inputs
def getTestsJsonFromCdash(cdashUrl, projectName, filterFields, options,
  printCDashUrl=False \
  ):

  cacheFolder=options.cdashQueriesCacheDir+"/test_history"
  cacheFile=options.date+"-All-Failing-Tests.json"
  simplified_dict_of_tests={}
  if options.useCachedCDashData:
    simplified_dict_of_tests=getJsonDataFromCache(cacheFolder, cacheFile)
  
  if not simplified_dict_of_tests and (not options.useCachedCDashData):
    raw_json_from_cdash=getRawJsonFromCdash(cdashUrl, projectName, filterFields,
      options, printCDashUrl)
    simplified_dict_of_tests=getTestDictionaryFromCdashJson(raw_json_from_cdash, options)
    if options.cdashQueriesCacheDir:
      writeJsonDataToCache(cacheFolder, cacheFile, simplified_dict_of_tests)

  getHistoricalDataForTests(simplified_dict_of_tests, cdashUrl, projectName,
    filterFields, options)
  return simplified_dict_of_tests


# Construct a URL and return the raw json from cdash
def getRawJsonFromCdash(cdashUrl, projectName, filterFields, options,
  printCDashUrl=False \
  ):
  # construct the cdash query.  the "/api/v1/" will cause CDash to return a json data 
  # structure instead of a web page
  CdashTestsApiQueryUrl= \
    cdashUrl+ \
    "/api/v1/queryTests.php?"+ \
    "project="+projectName+ \
    "&date="+options.date+ \
    "&"+filterFields

  if printCDashUrl:
    print("Getting bulid data from:\n\n  " + CdashTestsApiQueryUrl )
    
  # get the json from CDash using the query constructed above
  json_from_cdash_query=extractCDashApiQueryData(CdashTestsApiQueryUrl)
  return json_from_cdash_query


def getTestDictionaryFromCdashJson(CDash_json, options):
 
  simplified_dict_of_tests={}

  # The CDash json has a lot of information and is many levels deep.  This will collect 
  # relevant data about the tests and store it in a dictionary
  for i in range(0, len(CDash_json["builds"])):

    site=CDash_json["builds"][i]["site"]
    build_name=CDash_json["builds"][i]["buildName"]
    test_name=CDash_json["builds"][i]["testname"]
#    test_name_url=CDash_json["builds"][i]["testname"] 
    days_of_history=int(options.test_history_days)
    
    
    # A unique test is determined by the build name, the test name, and the site where it was run
    # construct a dictionary key unique to each test using those 3 things. And initialize dictionary
    dict_key=build_name+"---"+test_name+"---"+site
    if dict_key in simplified_dict_of_tests:
      simplified_dict_of_tests[dict_key]["count"]+=1
    else:
      simplified_dict_of_tests[dict_key]={}

      # Store relevant information in the dictionary.  This information is all available from the 
      # first CDash query we ran above.  There is only information about the given day no history
      # some of these are just initialized but not used yet
      simplified_dict_of_tests[dict_key]["site"]=site
      simplified_dict_of_tests[dict_key]["build_name"]=build_name
      simplified_dict_of_tests[dict_key]["test_name"]=test_name
      simplified_dict_of_tests[dict_key]["test_name_url"]=options.cdashSiteUrl+"/"+CDash_json["builds"][i]["testDetailsLink"]
      simplified_dict_of_tests[dict_key]["issue_tracker"]=""
      simplified_dict_of_tests[dict_key]["issue_tracker_url"]=""
      simplified_dict_of_tests[dict_key]["details"]=CDash_json["builds"][i]["details"].strip()
      simplified_dict_of_tests[dict_key]["status"]=CDash_json["builds"][i]["status"].strip()
      simplified_dict_of_tests[dict_key]["status_url"]=options.cdashSiteUrl+"/"+CDash_json["builds"][i]["testDetailsLink"]
      simplified_dict_of_tests[dict_key]["count"]=1

  return simplified_dict_of_tests


def getHistoricalDataForTests(testDictionary, cdashUrl, projectName, filterFields, options):
      # Some of the information needed is historical.  For this we need to look at the history of the test
  for dict_key in testDictionary:
    site=testDictionary[dict_key]["site"]
    build_name=testDictionary[dict_key]["build_name"]
    test_name=testDictionary[dict_key]["test_name"]
    days_of_history=int(options.test_history_days)
    given_date=validateYYYYMMDD(options.date)

    history_title_string="failures_in_last_"+str(options.test_history_days)+"_days"
    
    #URL used to get the history of the test in JSON form
    testHistoryQueryUrl= \
    cdashUrl+ \
    "/api/v1/queryTests.php?"+ \
    "project="+projectName+ \
    "&filtercombine=and&filtercombine=&filtercount=5&showfilters=1&filtercombine=and"+ \
    "&field1=buildname&compare1=61&value1="+build_name+ \
    "&field2=testname&compare2=61&value2="+test_name+ \
    "&field3=site&compare3=61&value3="+site+ \
    "&field4=buildstarttime&compare4=84&value4="+(given_date+datetime.timedelta(days=1)).isoformat()+ \
    "&field5=buildstarttime&compare5=83&value5="+(given_date+datetime.timedelta(days=-1*days_of_history+1)).isoformat()

    #URL to imbed in email to show the history of the test to humans
    testHistoryEmailUrl= \
    cdashUrl+ \
    "/queryTests.php?"+ \
    "project="+projectName+ \
    "&filtercombine=and&filtercombine=&filtercount=5&showfilters=1&filtercombine=and"+ \
    "&field1=buildname&compare1=61&value1="+build_name+ \
    "&field2=testname&compare2=61&value2="+test_name+ \
    "&field3=site&compare3=61&value3="+site+ \
    "&field4=buildstarttime&compare4=84&value4="+(given_date+datetime.timedelta(days=1)).isoformat()+ \
    "&field5=buildstarttime&compare5=83&value5="+(given_date+datetime.timedelta(days=-1*days_of_history+1)).isoformat()

    #URL to imbed in email to show the history of the build to humans
    buildHistoryEmailUrl= \
    cdashUrl+ \
    "/index.php?"+ \
    "project="+projectName+ \
    "&filtercombine=and&filtercombine=&filtercount=4&showfilters=1&filtercombine=and"+ \
    "&field1=buildname&compare1=61&value1="+build_name+ \
    "&field2=site&compare2=61&value2="+site+ \
    "&field3=buildstarttime&compare3=84&value3="+(given_date+datetime.timedelta(days=1)).isoformat()+ \
    "&field4=buildstarttime&compare4=83&value4="+(given_date+datetime.timedelta(days=-1*days_of_history+1)).isoformat()                    

    testDictionary[dict_key]["site_url"]=""
    testDictionary[dict_key]["build_name_url"]=buildHistoryEmailUrl
    testDictionary[dict_key]["test_history"]="Test History"
    testDictionary[dict_key]["test_history_url"]=testHistoryQueryUrl
    testDictionary[dict_key]["previous_failure_date"]=""
    testDictionary[dict_key]["most_recent_failure_date"]=""
    testDictionary[dict_key][history_title_string]=""
    testDictionary[dict_key][history_title_string+"_url"]=testHistoryEmailUrl
    testDictionary[dict_key]["count"]=1

    # set the names of the cached files so we can check if they exists and write them out otherwise
    cacheFolder=options.cdashQueriesCacheDir+"/test_history"
    cacheFile=options.date+"-"+site+"-"+build_name+"-"+test_name+"-HIST-"+str(days_of_history)+".json"

    # initialize test_history_json to empty dict.  if it is read from the cache then it will not be empty
    # after these ifs
    test_history_json={}
    if options.useCachedCDashData:
      test_history_json=getJsonDataFromCache(cacheFolder, cacheFile)

    # if test_history_json is still empty then either it was not found in the cache or the user 
    # told us not to look in the cache.  Get the json from CDash
    if not test_history_json:
      print("Getting "+str(days_of_history)+" days of history for "+test_name+" in the build "+build_name+" on "+site+" from CDash")
      test_history_json=extractCDashApiQueryData(testHistoryQueryUrl)      

      # cache json files if the option is on (turned on by default)
      if options.cdashQueriesCacheDir:
        writeJsonDataToCache(cacheFolder, cacheFile, test_history_json)

    # adding up number of failures and collecting dates of the failures
    failed_dates=[]
    for cdash_build in test_history_json["builds"]:
      if cdash_build["status"] == "Failed":
        failed_dates.append(cdash_build["buildstarttime"].split('T')[0])

    testDictionary[dict_key][history_title_string]=len(failed_dates)

    # set most recent and previous failure dates
    failed_dates.sort(reverse=True)
    if len(failed_dates) == 0:
      testDictionary[dict_key]["previous_failure_date"]="None"
      testDictionary[dict_key]["most_recent_failure_date"]="None"
    elif len(failed_dates) == 1:
      testDictionary[dict_key]["previous_failure_date"]="None"
      testDictionary[dict_key]["most_recent_failure_date"]=failed_dates[0]
    else:
      testDictionary[dict_key]["previous_failure_date"]=failed_dates[1]
      testDictionary[dict_key]["most_recent_failure_date"]=failed_dates[0]


def getJsonDataFromCache(cacheFolder, cacheFile):
  # will read json data from specified file and return that data.
  # if the file does not exist then return empy dict

  cacheFilePath=cacheFolder+"/"+cacheFile
  jsonData={}
  if os.path.exists(cacheFilePath):
    print("Reading cache file: "+cacheFilePath)
    f = open(cacheFilePath, "r")
    jsonData=json.load(f)
    f.close
  else:
    print("Cache file: "+cacheFilePath+" not found")
  return jsonData


def writeJsonDataToCache(cacheFolder, cacheFile, jsonData):
  # creating the cache directory if it does not already exist
  if not os.path.exists(os.path.dirname(cacheFolder+"/")):
    os.makedirs(os.path.dirname(cacheFolder+"/"))

  f = open(cacheFolder+"/"+cacheFile, "w")
  json.dump(jsonData, f)
  f.close


def filterDictionary(dictOfTests, fieldToTest, testValue="", testType=""):
  dict_of_tests_that_pass={}
  dict_of_tests_that_fail={}
  
  for key in dictOfTests:
    if dictOfTests[key][fieldToTest] == "":
      dict_of_tests_that_pass[key] = dictOfTests[key]
    else:
      dict_of_tests_that_fail[key] = dictOfTests[key]

  return dict_of_tests_that_pass, dict_of_tests_that_fail


def checkForIssueTracker(dictOfTests, issueTrackerDBFileName):
  
  dict_of_known_issues={}
  with open(issueTrackerDBFileName, "r") as f:
    for line in f:
      site=line.split(",")[0].strip()
      build_name=line.split(",")[1].strip()
      test_name=line.split(",")[2].strip()
      dict_key=build_name+"---"+test_name+"---"+site
      dict_of_known_issues[dict_key]={}
      dict_of_known_issues[dict_key]["issue_tracker_url"]=line.split(",")[3].strip()
      dict_of_known_issues[dict_key]["issue_tracker"]=line.split(",")[4].strip()

    f.close()
  
  for key in dictOfTests:
    if key in dict_of_known_issues:
      dictOfTests[key]["issue_tracker"]=dict_of_known_issues[key]["issue_tracker"]
      dictOfTests[key]["issue_tracker_url"]=dict_of_known_issues[key]["issue_tracker_url"]
  f.close()


#
# Create an HTML MIME Email
#  

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Create MINE formatted email object (but don't send it)
#
def createHtmlMimeEmail(fromAddress, toAddress, subject, textBody, htmlBody):

  # Create message container - the correct MIME type is multipart/alternative.
  msg = MIMEMultipart('alternative')
  msg['From'] = fromAddress
  msg['To'] = toAddress
  msg['Subject'] = subject

  # Record the MIME types of both parts - text/plain and text/html.
  part1 = MIMEText(textBody, 'plain')
  part2 = MIMEText(htmlBody, 'html')

  # Attach parts into message container.
  # According to RFC 2046, the last part of a multipart message, in this case
  # the HTML message, is best and preferred.
  msg.attach(part1)
  msg.attach(part2)

  return msg


# Send a MIME formatted email
#
def sendMineEmail(mimeEmail):
  # Send the message via local SMTP server.
  s = smtplib.SMTP('localhost')
  # sendmail function takes 3 arguments: sender's address, recipient's address
  # and message to send - here it is sent as one string.
  s.sendmail(mimeEmail['From'], mimeEmail['To'], mimeEmail.as_string())
  s.quit()
