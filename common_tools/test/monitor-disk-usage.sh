#!/bin/bash

#
# Send an email of the given partition is greater than percentage threadshold.
#
# Usage:
#
#   monitor-disk-usage.sh <partition> <percentage_usage> <email_address>
#
# For example:
#
#   monitor-disk-usage.sh /home 95 your-uid@sandia.gov
#
# In this case, an email will be sent to your-uid@sandia.gov if the disk
# containing /home is more than 95% full.
#
# This script should be run as a cron job every day.
#
# This is a stand-alone script and can be run from any directory.
#

partition=$1
percentage_usage_warn=$2
email_addresss=$3

hostname=`hostname`

CURRENT=$(df ${partition} | grep ${partition} | awk '{ print $5}' | sed 's/%//g')

usage_str="${hostname}:${partition} ${CURRENT}% full, threashold ${percentage_usage_warn}%"

df_h_output=$(df -h ${partition})

echo "${usage_str}"
echo
echo "${df_h_output}"

if [ "${CURRENT}" -gt "${percentage_usage_warn}" ] ; then
  echo "Sending notiviation email to ${email_addresss}"
  mail -s "${usage_str}" ${email_addresss} << EOF
WARNING: Partition ${partition} on ${hostname} is critically low!
  Used: ${CURRENT}%
  Warning threshold: ${percentage_usage_warn}%

  ${df_h_output}
EOF
fi
