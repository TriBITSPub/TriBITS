#!/bin/bash

# Used to test TriBITS on any of the ORNL CASL Fissile/Spy machines
#
# This script requires that the VERA dev env be loaded by sourcing the script:
#
#  . /projects/vera/gcc-4.8.3/load_dev_env.[sh,csh]
#
# You can source this script either in your shell startup script
# (e.g. .bash_profile) or you can source it manually whenever you need to set
# up to build VERA software.
#
# You can link this script into any location and it will work out of the box.

EXTRA_ARGS=$@

if [ "$TRIBITS_BASE_DIR" == "" ] ; then
  _ABS_FILE_PATH=`readlink -f $0`
  _SCRIPT_DIR=`dirname $_ABS_FILE_PATH`
  TRIBITS_BASE_DIR=$_SCRIPT_DIR/../..
fi

TRIBITS_BASE_DIR_ABS=$(readlink -f $TRIBITS_BASE_DIR)
echo "TRIBITS_BASE_DIR_ABS = $TRIBITS_BASE_DIR_ABS"

# Check to make sure that the env has been loaded correctly
if [ "$LOADED_TRIBITS_DEV_ENV" != "gcc-4.8.3" ] ; then
  echo "Error, must source /projects/vera/gcc-4.8.3/load_dev_env.[sh,csh] before running checkin-test-vera.sh!"
  exit 1
fi

#
# Built-in Primary Tested (PT) --default-builds (DO NOT MODIFY)
#

echo "
-DTrilinos_CONFIGURE_OPTIONS_FILE:FILEPATH='$TRIBITS_BASE_DIR_ABS/dev_testing/generic/do-configure-mpi-debug'
" > MPI_DEBUG.config

echo "
-DTrilinos_CONFIGURE_OPTIONS_FILE:FILEPATH='$TRIBITS_BASE_DIR_ABS/dev_testing/generic/do-configure-serial-release-gcc'
" > SERIAL_RELEASE.config

#
# Invocation
#

# Use CMake 2.8.11 to test since that is the min version we are enforcing!
export PATH=/projects/vera/common_tools/cmake-2.8.11/bin:$PATH

$TRIBITS_BASE_DIR_ABS/checkin-test.py \
-j16 \
--ctest-timeout=180 \
--skip-case-no-email \
$EXTRA_ARGS
