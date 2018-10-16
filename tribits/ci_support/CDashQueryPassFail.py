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
import pprint

from FindGeneralScriptSupport import *

pp = pprint.PrettyPrinter()


# Validate a date format
def validateYYYYMMDD(dateText):
  try:
    return datetime.datetime.strptime(dateText, '%Y-%m-%d')
  except ValueError:
    raise ValueError("Incorrect data format for '"+dateText+"', should be YYYY-MM-DD")


# Construct the full query URL given the pieces
def getCDashIndexQueryUrl(cdashUrl, projectName, date, filterFields):
  return cdashUrl+"/api/v1/index.php?project="+projectName+"&date="+date \
    + "&"+filterFields


# Given a CDash query URL, return the full Python CDash data-structure
def extractCDashApiQueryData(cdashApiQueryUrl):
  response = urlopen(cdashApiQueryUrl)
  return json.load(response)


# Collect CDash index.php build summary fields
def collectCDashIndexBuildSummaryFields(fullCDashIndexBuild):
  summaryBuild = {
    u('buildname') : fullCDashIndexBuild.get('buildname', 'missing_build_name'),
    u('update') : \
      fullCDashIndexBuild.get('update', {'errors':9999,'this_field_was_missing':1}),
    u('configure') : \
      fullCDashIndexBuild.get('configure', {'error':9999,'this_field_was_missing':1}),
    u('compilation') : \
      fullCDashIndexBuild.get('compilation', {'error':9999,'this_field_was_missing':1}),
    u('test') : \
     fullCDashIndexBuild.get('test', {'fail':9999, 'notrun':9999,'this_field_was_missing':1} ),
    }
  return summaryBuild


# Given the full Python CDash API builds data-structure returned from the
# CDash index.php page and query, return an reduced data-structure to be used
# for pass/fail examination.
#
# This function takes in the data-structre directly returned from:
#
#   <cdash-url>/api/v1/index.php?project=<project>&date=<YYYY-MM-DD>&<filter-fields>
#
# The input full CDash API collapsed builds data-structure that has the
# following structure and fields of interest:
#
#  fullCDashIndexBuilds =
#  {
#    'all_buildgroups': [ {'id':1,'name:"Nightly"}, ...],
#    'buildgroups': [
#      {
#        'builds":[
#          {
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
# the reduced data-structure:
#
#   [
#     {
#       'buildname':"???",
#       'update': {'errors':???, ...},
#       'configure':{'error': ???, ...},
#       'compilation':{'error': ???, ...},
#       'test': {'fail':???, 'notrun':???, 'pass':???, ...},
#       ...
#       },
#       ...
#       }
#
# This collects *all* of the builds from all of the build groups, not just the
# 'Nighlty' build group.  Therefore, if you want to only consider on set of
# build groups, you need to add that to the CDash query URL
# (e.g. group='Nighlty').
#
def getCDashIndexBuildsSummary(fullCDashIndexBuilds):
  summaryCDashIndexBuilds = []
  for buildgroup in fullCDashIndexBuilds["buildgroups"]:
    for build in buildgroup["builds"]:
      summaryBuild = collectCDashIndexBuildSummaryFields(build)
      summaryCDashIndexBuilds.append(summaryBuild)
  return summaryCDashIndexBuilds
  

# Return if a CDash Index build passes
def cdashIndexBuildPasses(cdashIndexBuild):
  if cdashIndexBuild['update']['errors'] > 0:
    return False
  if cdashIndexBuild['configure']['error'] > 0:
    return False
  if cdashIndexBuild['compilation']['error'] > 0:
    return False
  if (cdashIndexBuild['test']['fail'] + cdashIndexBuild['test']['notrun'])  > 0:
    return False
  return True
  

# Return if a list of CDash builds pass or fail and return error string if
# they fail.
def cdashIndexBuildsPass(summaryCDashIndexBuilds):
  buildsPass = True
  buildFailedMsg = ""
  for build in summaryCDashIndexBuilds:
    if not cdashIndexBuildPasses(build):
      buildsPass = False
      buildFailedMsg = "Error, the build " + sorted_dict_str(build) + " failed!"
      break
  return (buildsPass, buildFailedMsg)


# Extract the set of build names from a list of build names
def getCDashIndexBuildNames(summaryCDashIndexBuilds):
  buildNames = []
  for build in summaryCDashIndexBuilds:
    buildNames.append(build['buildname'])
  return buildNames


# Return if all of the expected builds exist and an error message if they
# don't.
def doAllExpectedBuildsExist(buildNames, expectedBuildNames):
  allExpectedBuildsExist = True
  errMsg = ""
  for expectedBuildName in expectedBuildNames:
    if findInSequence(buildNames, expectedBuildName) == -1:
      allExpectedBuildsExist = False
      errMsg = "Error, the expected build '"+expectedBuildName+"'" \
        +" does not exist in the list of builds "+str(buildNames) 
      break
  return (allExpectedBuildsExist, errMsg)    


# Return if a list of summary CDash index.php builds pass and has all of the
# expected builds.
def cdashIndexBuildsPassAndExpectedExist(summaryCDashIndexBuilds, 
  expectedBuildNames \
  ):
  cdashIndexBuildsPassAndExpectedExist_pass = True
  errMsg = ""
  # Check that all of the builds pass!
  if cdashIndexBuildsPassAndExpectedExist_pass:
    (buildsPass, buildFailedMsg) = cdashIndexBuildsPass(summaryCDashIndexBuilds)
    if not buildsPass:
      cdashIndexBuildsPassAndExpectedExist_pass = False
      errMsg = buildFailedMsg
  # Check that all of the expected builds are listed
  if cdashIndexBuildsPassAndExpectedExist_pass:
    buildNames = getCDashIndexBuildNames(summaryCDashIndexBuilds)
    (allExpectedBuildsExist, errMsg) = \
      doAllExpectedBuildsExist(buildNames, expectedBuildNames)
    if not allExpectedBuildsExist:
      cdashIndexBuildsPassAndExpectedExist_pass = False
      errMsg = errMsg
  return (cdashIndexBuildsPassAndExpectedExist_pass, errMsg)


# Determine if CDash index.php query builds all pass and has all expected
# builds.
def queryCDashAndDeterminePassFail(cdashUrl, projectName, date, filterFields,
  expectedBuildNames, printCDashUrl=True,
  extractCDashApiQueryData_in=extractCDashApiQueryData \
  ):
  # Get the query data
  cdashQueryUrl = getCDashIndexQueryUrl(cdashUrl, projectName, date, filterFields)
  if printCDashUrl:
    print("Getting data from:\n\n  " + cdashQueryUrl )
  fullCDashIndexBuilds = extractCDashApiQueryData_in(cdashQueryUrl)
  summaryCDashIndexBuilds = getCDashIndexBuildsSummary(fullCDashIndexBuilds)
  # Determine pass/fail
  (cdashIndexBuildsPassAndExpectedExist_pass, errMsg) = \
    cdashIndexBuildsPassAndExpectedExist(summaryCDashIndexBuilds, expectedBuildNames)
  if not cdashIndexBuildsPassAndExpectedExist_pass:
    return (False, errMsg)
  return (True, "")
    
# This will return a dictionary with information about all the tests that were returned
# in the json from cdash as a result of the CDash query from the given inputs
def getTestsJsonFromCdash(cdashUrl, projectName, filterFields, options):

  date=options.date
  # construct the cdash query.  the "/api/v1/" will cause CDash to return a json data 
  # structure instead of a web page
  CdashTestsApiQueryUrl= \
    cdashUrl+ \
    "/api/v1/queryTests.php?"+ \
    "project="+projectName+ \
    "&date="+date+ \
    filterFields
  
  # get the json from CDash using the query constructed above
  json_from_cdash_query=extractCDashApiQueryData(CdashTestsApiQueryUrl)

  # JRF: ToDo: Create a simple function that is the above two statements
  # (which can't be unit tested because it gets real date).

  # convert the date into a datetime.date so we can easiliy add/subtract days for 
  # queries taht need to span many days
  given_date=datetime.date(int(date.split('-')[0]), \
                           int(date.split('-')[1]), \
                           int(date.split('-')[2]))
  # JRF: ToDo: Repalce above with call to validateYYYYMMDD()

  simplified_dict_of_tests={}

  # The CDash json has a lot of information and is many levels deep.  This will collect 
  # relevant data about the tests and stoer it in a dictionary
  for i in range(0, len(json_from_cdash_query["builds"])):

    site=json_from_cdash_query["builds"][i]["site"]
    build_name=json_from_cdash_query["builds"][i]["buildName"]
    test_name=json_from_cdash_query["builds"][i]["testname"]
    days_of_history=int(options.test_history_days)
    
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
      history_title_string="failures_in_last_"+str(options.test_history_days)+"_days"
      simplified_dict_of_tests[dict_key]["site"]=site
      simplified_dict_of_tests[dict_key]["site_url"]=""
      simplified_dict_of_tests[dict_key]["build_name"]=build_name
      simplified_dict_of_tests[dict_key]["build_name_url"]=buildHistoryEmailUrl
      simplified_dict_of_tests[dict_key]["test_name"]=test_name
      simplified_dict_of_tests[dict_key]["test_name_url"]=testHistoryEmailUrl
      simplified_dict_of_tests[dict_key]["issue_tracker"]=""
      simplified_dict_of_tests[dict_key]["issue_tracker_url"]=""
      simplified_dict_of_tests[dict_key]["details"]=json_from_cdash_query["builds"][i]["details"]
      simplified_dict_of_tests[dict_key]["details_url"]=""
      simplified_dict_of_tests[dict_key]["test_history"]="Test History"
      simplified_dict_of_tests[dict_key]["test_history_url"]=testHistoryQueryUrl
      simplified_dict_of_tests[dict_key]["status"]=json_from_cdash_query["builds"][i]["status"]
      simplified_dict_of_tests[dict_key]["status_url"]=""
      simplified_dict_of_tests[dict_key]["previous_failure_date"]=""
      simplified_dict_of_tests[dict_key]["most_recent_failure_date"]=""
      simplified_dict_of_tests[dict_key][history_title_string]=""
      simplified_dict_of_tests[dict_key]["count"]=1
      # Some of the information needed is historical.  For this we need to look at the history of the test
      print("Getting history of "+test_name+" in the build "+build_name+" on "+site)
      test_history_json_from_cdash=extractCDashApiQueryData(testHistoryQueryUrl)

      # JRF: ToDo: Refactor above code that gets test history data into its
      # own function (with minimal code that you can't unit test).

      # JRF: ToDo: Refactor below code that processes data for each test into
      # its own Python function that can be unit tested.

      failed_dates=[]

      # adding up number of failures and collecting dates of the failures
      for cdash_build in test_history_json_from_cdash["builds"]:
        if cdash_build["status"] == "Failed":
          failed_dates.append(cdash_build["buildstarttime"].split('T')[0])

      simplified_dict_of_tests[dict_key][history_title_string]=len(failed_dates)
      print(failed_dates)

      # set most recent and previous failure dates
      failed_dates.sort(reverse=True)
      if len(failed_dates) == 0:
        simplified_dict_of_tests[dict_key]["previous_failure_date"]="None"
        simplified_dict_of_tests[dict_key]["most_recent_failure_date"]="None"
      elif len(failed_dates) == 1:
        simplified_dict_of_tests[dict_key]["previous_failure_date"]="None"
        simplified_dict_of_tests[dict_key]["most_recent_failure_date"]=failed_dates[0]
      else:
        simplified_dict_of_tests[dict_key]["previous_failure_date"]=failed_dates[1]
        simplified_dict_of_tests[dict_key]["most_recent_failure_date"]=failed_dates[0]

  return simplified_dict_of_tests


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
      build_name=line.split(",")[0].strip()
      test_name=line.split(",")[1].strip()
      site=line.split(",")[2].strip()
      dict_key=build_name+"---"+test_name+"---"+site
      dict_of_known_issues[dict_key]={}
      dict_of_known_issues[dict_key]["issue_tracker_url"]=line.split(",")[3].strip()
      dict_of_known_issues[dict_key]["issue_tracker"]=line.split(",")[4].strip()

    f.close()
  
  with open(issueTrackerDBFileName, "a") as f:
    for key in dictOfTests:
      if key in dict_of_known_issues:
        dictOfTests[key]["issue_tracker"]=dict_of_known_issues[key]["issue_tracker"]
        dictOfTests[key]["issue_tracker_url"]=dict_of_known_issues[key]["issue_tracker_url"]
      else:
        f.write("\n"+ \
                dictOfTests[key]["build_name"]+", "+ \
                dictOfTests[key]["test_name"]+", "+ \
                dictOfTests[key]["site"]+", ,")
  f.close()
