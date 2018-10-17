#!/usr/bin/env python

import os
import sys

import CDashQueryAnalizeReport as CDQAR
import json
import pprint
import datetime

#
# Read in the command-line arguments
#

usageHelp = r"""TODO trilinos_atdm_builds_status.py --date=YYYY-MM-DD

This script looks at filtered CDash results for the Trilinos project for the
given testing day --date=YYYY-MM-DD and generates html that is sent in an email.

"""

from optparse import OptionParser

clp = OptionParser(usage=usageHelp)

clp.add_option(
     "--date", dest="date", type="string", default=(datetime.date.today()+datetime.timedelta(days=-1)).isoformat(),
   help="CDash testing date in format YYYY-MM-DD" )
clp.add_option(
      "--limit-test-history-days", dest="test_history_days", default=30,
    help="Number of days to go back in history for each test" )
clp.add_option(
      "--cache-cdash-queries", dest="cache_cdash_queries", default=True,
    help="Have the script save json files from cdash queries" )
clp.add_option(
      "--construct-from-cache", dest="construct_from_cache",  default=True,
    help="Use cached json files instead of cdash queries when possible" )
clp.add_option(
      "--cache-dir", dest="cache_dir",  default="cached_files/",
    help="directory used to read and write cached files" )
clp.add_option(
      "--skip-send-email", dest="skip_send_email", default=False,
    help="Do not send email" )
clp.add_option(
      "--write-email-to-file", dest="write_email_to_file",type="string",  default="",
    help="Write the email out as a file with the given name" )


(options, args) = clp.parse_args()

CDQAR.validateYYYYMMDD(options.date)
print("Analyzing test results from "+options.date)

#
# Define fixed data
#

cdashUrl = "https://testing.sandia.gov/cdash"

project = "Trilinos"

#
# Run the query commands
#

# filters to get all tests that failed on the given date 
all_failed_tests_filter_fields= \
  "&filtercombine=and"+ \
  "&filtercount=4"+ \
  "&showfilters=1"+ \
  "&filtercombine=and"+ \
  "&field1=buildname&compare1=65&value1=Trilinos-atdm-"+ \
  "&field2=status&compare2=62&value2=passed"+ \
  "&field3=status&compare3=62&value3=notrun"+ \
  "&field4=groupname&compare4=61&value4=ATDM"

# get data from cdash and return in a simpler form
all_failing_tests=CDQAR.getTestsJsonFromCdash(cdashUrl, project, all_failed_tests_filter_fields, options)

# add issue tracking information to the tests' data
CDQAR.checkForIssueTracker(all_failing_tests, "knownIssues.csv")

# split the tests into those with issue tracking and those without
tests_without_issue_tracking, tests_with_issue_tracking = CDQAR.filterDictionary(all_failing_tests, "issue_tracker")

#
# Create the html
#

table_headings=["site", \
                "build_name", \
                "test_name", \
                "status", \
                "details", \
                "failures_in_last_"+str(options.test_history_days)+"_days", \
                "previous_failure_date", \
                "issue_tracker"]
htmlBody=CDQAR.createHtmlTable(tests_without_issue_tracking, table_headings, "Failing Tests without Issue Tracking: "+options.date)
htmlBody+=CDQAR.createHtmlTable(tests_with_issue_tracking, table_headings, "Failing Tests with Issue Tracking: "+options.date)

if not options.write_email_to_file == "":
  outfile=open(options.write_email_to_file, "w")
  outfile.write(htmlBody)

if not options.skip_send_email:
  msg=CDQAR.createHtmlMimeEmail("jfrye@sandia.gov", "jfrye@sandia.gov, rabartl@sandia.gov", "ATDM Trlinos Test Summary "+options.date, "", htmlBody)

  CDQAR.sendMineEmail(msg)
#
# Done
#
sys.exit(0)
