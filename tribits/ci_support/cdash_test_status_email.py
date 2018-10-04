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

usageHelp = r"""TODO """

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
      "--write-email-to-file", dest="write_email_to_file", type="string",  default="",
    help="Write the email out as a file with the given name" )
clp.add_option(
      "--email-recipients", dest="email_recipients", type="string",  default="",
    help="list of email addresses that the email will be sent to" )
clp.add_option(
      "--email-from-address", dest="email_from_address", type="string",  default="",
    help="the from address on sent out emails" )
clp.add_option(
      "--email-subject-line", dest="email_subject_line", type="string",  default="",
    help="the subject line on sent out emails" )
clp.add_option(
      "--cdash-site-url", dest="cdash_site_url", type="string",  default="",
    help="the subject line on sent out emails" )
clp.add_option(
      "--cdash-site-project", dest="cdash_site_project", type="string",  default="",
    help="the subject line on sent out emails" )
clp.add_option(
      "--cdash-site-extra-query-fields", dest="cdash_site_extra_query_fields", type="string",  default="",
    help="the subject line on sent out emails" )
clp.add_option(
      "--issue-tracking-csv-file-name", dest="issue_tracking_csv_file_name", type="string",  default="",
    help="the subject line on sent out emails" )

(options, args) = clp.parse_args()

CDQAR.validateYYYYMMDD(options.date)
print("Analyzing test results from "+options.date)

#
# Define fixed data
#

cdashUrl = options.cdash_site_url
project = options.cdash_site_project
extra_filter_fields= options.cdash_site_extra_query_fields

#
# Run the query commands
#

# get data from cdash and return in a simpler form
all_failing_tests=CDQAR.getTestsJsonFromCdash(cdashUrl, project, extra_filter_fields, options)

# add issue tracking information to the tests' data
#CDQAR.checkForIssueTracker(all_failing_tests, "knownIssues.csv")
CDQAR.checkForIssueTracker(all_failing_tests, options.issue_tracking_csv_file_name)

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
  emailRecipientsList=options.email_recipients.split(",")
  emailFromAddress=options.email_from_address
  emailSubject=options.email_subject_line+": "+options.date
  for recipient in emailRecipientsList:
    msg=CDQAR.createHtmlMimeEmail(emailFromAddress, recipient.strip(), emailSubject, "", htmlBody)
    CDQAR.sendMineEmail(msg)
else:
  print("Email is not being sent")
#
# Done
#
sys.exit(0)
