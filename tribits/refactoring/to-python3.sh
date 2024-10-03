#!/bin/sh
#
# Usage:
#
#   to-python3.sh <base-dir>
#

_SCRIPT_DIR=`echo $0 | sed "s/\(.*\)\/to-python3[.]sh/\1/g"`
baseDir=$1
find ${baseDir} -type f \
  \( -name CMakeLists.txt -or -name "*.cmake" -or -name "*.cmake.in" -or -name "*.rst" \) \
  -exec $_SCRIPT_DIR/token-replace.py -t PYTHON_EXECUTABLE -r Python3_EXECUTABLE -f {} ';'
