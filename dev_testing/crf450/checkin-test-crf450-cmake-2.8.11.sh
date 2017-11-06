#!/bin/bash
 
# Used to test TriBITS on crf450 using the VERA Dev Env using CMake 2.8.11
#
# You can link this script into any location and it will work out of the box.
#

if [ "$TRIBITS_BASE_DIR" == "" ] ; then
  _ABS_FILE_PATH=`readlink -f $0`
  _SCRIPT_DIR=`dirname $_ABS_FILE_PATH`
  TRIBITS_BASE_DIR=$_SCRIPT_DIR/../..
fi

TRIBITS_BASE_DIR_ABS=$(readlink -f $TRIBITS_BASE_DIR)
#echo "TRIBITS_BASE_DIR_ABS = $TRIBITS_BASE_DIR_ABS"

# Load the env:
source /home/vera_env/gcc-4.8.3/load_dev_env.sh
export PATH=/home/vera_env/common_tools/cmake-2.8.11/bin:$PATH

# Create local defaults file if one does not exist
_LOCAL_CHECKIN_TEST_DEFAULTS=local-checkin-test-defaults.py
if [ -f $_LOCAL_CHECKIN_TEST_DEFAULTS ] ; then
  echo "File $_LOCAL_CHECKIN_TEST_DEFAULTS already exists, leaving it!"
else
  echo "Creating default file $_LOCAL_CHECKIN_TEST_DEFAULTS!"
  echo "
defaults = [
  \"-j16\",
  ]
  " > $_LOCAL_CHECKIN_TEST_DEFAULTS
fi

$TRIBITS_BASE_DIR_ABS/checkin-test.py \
--extra-cmake-options="-DPYTHON_EXECUTABLE=/usr/bin/python2.6" \
--ctest-timeout=180 \
--skip-case-no-email \
"$@"
