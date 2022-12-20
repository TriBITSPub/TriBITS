#!/bin/bash
#
# Run this in a subdir to replace all occurrences of SET_AND_INC_DIRS with
# TRIBITS_SET_AND_INC_DIRS (and lower-case versions).  Take into account
# token boundaries so will not replace in the middle of a token.
#
# Run as:
#
#   $ cd <some-base-dir>
#   $ <this-script-dir>/replace_set_and_inc_dirs_r.sh
#

_SCRIPT_DIR=`echo $0 | sed "s/\(.*\)\/.*replace_set_and_inc_dirs_r.sh/\1/g"`
#echo $_SCRIPT_DIR

echo
echo "Replacing SET_AND_INC_DIRS with TRIBITS_SET_AND_INC_DIRS in all CMakeList.txt and *.cmake files ..."
echo

find . \( -name CMakeLists.txt -or -name "*.cmake" \) -exec ${_SCRIPT_DIR}/token-replace.py -t SET_AND_INC_DIRS -r TRIBITS_SET_AND_INC_DIRS -f {} \;

echo
echo "Replacing set_and_inc_dirs with tribits_set_and_inc_dirs in all CMakeList.txt and *.cmake files ..."
echo

find . \( -name CMakeLists.txt -or -name "*.cmake" \) -exec ${_SCRIPT_DIR}/token-replace.py -t set_and_inc_dirs -r tribits_set_and_inc_dirs -f {} \;
