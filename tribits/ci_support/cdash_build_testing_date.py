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

import datetime

#
# Help message
#


usageHelp = r"""cdash_testing_date.py --cdash-project-start-time="HH:MM" [other options]

Returns to STDOUT the date string YYYY-MM-DD that corresponds the the matching
CDash test day.  Is should be compatible with the 'date=YYYY-MM-DD' argument
to many CDash PHP pages for a build that has a starting time stamp that
matches the requested date.

This tool is meant to match the CDash logic for what testing day a given CDash
build matches for the CDash 'date' field in various PHP pages for a given
CDash build with a give build start time (as reported to CDash from CTest).

For example, if the CDash project start time is 04:00 UTC and the CDash
build start time is 2018-01-22T00:00 UTC, then the relative CDash build date
time would be 2018-01-21T20:00 UTC which is the previous testing day
2018-01-21.  But if the CDash build start time was 2018-01-22T04:10 UTC,
then the relative CDash build date time would be 2018-01-22:00:10 UTC and
the testing day would be 2018-01-22.
"""

#
# Helper functions
#


def injectCmndLineOptionsInParser(clp, gitoliteRootDefault=""):
  
  clp.add_option(
    "--cdash-project-start-time", dest="cdashProjectStartTimeStr", type="string", default="",
    help="Starting time for the CDash testing day in 'HH:MM' in UTC."\
      + " Check the CDash project settings for the testing date." )
  
  clp.add_option(
    "--day-incr", dest="dayIncrInt", type="int", default="0",
    help="Increment for the testing date (default '0') [optional]" )
  
  clp.add_option(
    "--cdash-build-start-time", dest="cdashBuildStartTime", type="string", default="",
    help="CDash build start time in format 'YYYY-MM-DDThh:mm UTC'.  If empty ''"\
      +" then the current date/time in UTC is used.  (default '') [optional]" )
  
  clp.add_option(
    "--debug-level", dest="debugLevel", type="int", default="0",
    help="Debug level.  An integer >= 0 (default '0')" )


def getCmndLineOptions():
  from optparse import OptionParser
  clp = OptionParser(usage=usageHelp)
  injectCmndLineOptionsInParser(clp)
  (options, args) = clp.parse_args()
  if options.cdashProjectStartTimeStr == "":
    raise Exception("Error, input argument --cdash-project-start-time must be non"\
      +"-empty and must be of the format HH:MM UTC")
  return options


# Return the current time in UTC as a datetime object
def getCurrentDateTimeUtc():
  return datetime.datetime.utcnow()


# Get the timezone offset as a timedelta object w.r.t to UTC
#
# The supported timezones for timeZoneStr are the strings:
#
# * UTC: 0
# * EDT: 4
# * EST: 5
# * CDT: 5
# * CST: 6
# * MDT: 6
# * MST: 7
#
# NOTE: Any timezone that CDash returns for the 'buildstarttime' field must be
# added below.
#
def getTimeZoneOffset(timeZoneStr):
  if timeZoneStr == "UTC": timezoneOffsetInt = 0
  elif timeZoneStr == "EDT": timezoneOffsetInt = 4
  elif timeZoneStr == "EST": timezoneOffsetInt = 5
  elif timeZoneStr == "CDT": timezoneOffsetInt = 5
  elif timeZoneStr == "CST": timezoneOffsetInt = 6
  elif timeZoneStr == "MDT": timezoneOffsetInt = 6
  elif timeZoneStr == "MST": timezoneOffsetInt = 7
  else: raise Exception("Error, unrecognized timezone '"+timeZoneStr+"'!")
  return datetime.timedelta(hours=timezoneOffsetInt)


# Return a timezone aware datetime object given an input date and time given
# in the format "<YYYY>-<MM>-<DD>T<hh>:<mm>:<ss> <TZ>".
def getBuildStartTimeUtcFromStr(buildStartTime):
  buildStartTimeArray = buildStartTime.split(" ")
  if len(buildStartTimeArray) == 2:
    timezoneOffset = getTimeZoneOffset(buildStartTimeArray[1])
  else:
    timezoneOffset = 0
  #print timezoneOffset
  localDateTime = datetime.datetime.strptime(buildStartTimeArray[0], "%Y-%m-%dT%H:%M:%S")
  return localDateTime + timezoneOffset 


# Return a timedelta object for the CDash Project start time passed in as a
# string in the format "<hh>:<mm>" in UTC.
def getProjectTestingDayStartTimeDeltaFromStr(cdashProjectStartTimeStr):
  t = datetime.datetime.strptime(cdashProjectStartTimeStr, '%H:%M')
  return datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)


# Return a timedelta object for a day increment pass in as an signed integer.
def getDayIncrTimeDeltaFromInt(dayIncrInt):
  return datetime.timedelta(days=dayIncrInt)


# Return the string "<YYYY>-<MM>-<DD>" for an input datetime object.
def getDateStrFromDateTime(dateTime):
  return dateTime.strftime("%Y-%m-%d")


# Return the shifted CDash build start relative to the given CDash project
# testing day start time (as configured on CDash).
#
# This function is meant to match the CDash logic for what testing day a given
# CDash build matches for the CDash 'date' field in various PHP pages for a
# given CDash build with a give build start time (as reported to CDash from
# CTest).
#
# For example, if the CDash project start time is 04:00 UTC and the CDash
# build start time is 2018-01-22T00:00 UTC, then the relative CDash build date
# time would be 2018-01-21T20:00 UTC which is the previous testing day
# 2018-01-21.  But if the CDash build start time was 2018-01-22T04:10 UTC,
# then the relative CDash build date time would be 2018-01-22:00:10 UTC and
# the testing day would be 2018-01-22.
#
# To extract the "<YYYY>-<MM>-<DD>" string, use the function
# getDateStrFromDateTime().
# 
def getRelativeCDashBuildStartTime(
  cdashBuildStartTime,   # CDash build start time in UTC (datetime objet)
  cdashProjectStartTime, # CDash start time in UTC (timedelta object)
  dayIncr,               # Day increment in past or future (timedelta object)
  ):
  relativeCDashBuildDateTime = cdashBuildStartTime - cdashProjectStartTime + dayIncr
  return relativeCDashBuildDateTime


# Return the shifted CDash build start relative to the given CDash project
# testing day start time given input from the command-line arguments.
#
# This function just converts the input command-line args and then calls
# getRelativeCDashBuildStartTime().
#
def getRelativeCDashBuildStartTimeFromCmndLineArgs(
  cdashBuildStartTimeStr,  # If 'None', then is taken from getCurrentDateTimeUtc()
  cdashProjectStartTimeStr,
  dayIncrInt,
  debugLevel=0,
  ):

  if cdashBuildStartTimeStr:
    buildStartTimeUtc = getBuildStartTimeUtcFromStr(cdashBuildStartTimeStr)
  else:
    buildStartTimeUtc = getCurrentDateTimeUtc()
  if debugLevel: print("buildStartTimeUtc = "+str(buildStartTimeUtc))

  cdashStartTime = \
    getProjectTestingDayStartTimeDeltaFromStr(cdashProjectStartTimeStr)
  if debugLevel: print("cdashStartTime = "+str(cdashStartTime))

  dayIncr = getDayIncrTimeDeltaFromInt(dayIncrInt)
  if debugLevel: print("dayIncr = "+str(dayIncr))

  return getRelativeCDashBuildStartTime(buildStartTimeUtc, cdashStartTime, dayIncr)


#
# Run the script
#

if __name__ == '__main__':

  inOptions = getCmndLineOptions()

  relativeCDashBuildBuildDateTime = getRelativeCDashBuildStartTimeFromCmndLineArgs(
    inOptions.cdashBuildStartTime, inOptions.cdashProjectStartTimeStr,
    inOptions.dayIncrInt, inOptions.debugLevel,
    )

  print(getDateStrFromDateTime(relativeCDashBuildBuildDateTime))
