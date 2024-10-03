#!/bin/bash
#
# Run this in a subdir to replace all occurrences of INCLUDE_DIRECTORIES with
# TRIBITS_INCLUDE_DIRECTORIES (and lower-case versions).  Take into account
# token boundaries so will not replace in the middle of a token.
#
# Run as:
#
#   $ cd <some-base-dir>
#   $ <this-script-dir>/replace_include_directories_r.sh
#

_SCRIPT_DIR=`echo $0 | sed "s/\(.*\)\/.*replace_include_directories_r.sh/\1/g"`
#echo $_SCRIPT_DIR

echo
echo "Replacing INCLUDE_DIRECTORIES with TRIBITS_INCLUDE_DIRECTORIES in all CMakeList.txt and *.cmake files ..."
echo

find . \( -name CMakeLists.txt -or -name "*.cmake" \) -exec ${_SCRIPT_DIR}/../tribits/refactoring/token-replace.py -t INCLUDE_DIRECTORIES -r TRIBITS_INCLUDE_DIRECTORIES -f {} \;

echo
echo "Replacing include_directories with tribits_include_directories in all CMakeList.txt and *.cmake files ..."
echo

find . \( -name CMakeLists.txt -or -name "*.cmake" \) -exec ${_SCRIPT_DIR}/../tribits/refactoring/token-replace.py -t include_directories -r tribits_include_directories -f {} \;
