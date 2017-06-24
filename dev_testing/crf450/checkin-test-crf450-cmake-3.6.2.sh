#!/bin/bash
 
# Used to test TriBITS on crf450 using the VERA Dev Env with CMake 3.6.2.
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
export PATH=/home/vera_env/common_tools/cmake-3.6.2/bin:$PATH

# Create extra builds run by this script

echo "
-DTPL_ENABLE_MPI:BOOL=ON
-DCMAKE_BUILD_TYPE:STRING=DEBUG
-DTriBITS_ENABLE_DEBUG:BOOL=ON
-DTriBITS_ENABLE_Fortran:BOOL=ON
" > MPI_DEBUG_CMAKE-3.6.2.config

echo "
-DTPL_ENABLE_MPI:BOOL=OFF
-DCMAKE_BUILD_TYPE:STRING=RELEASE
-DTriBITS_ENABLE_DEBUG:BOOL=OFF
-DCMAKE_C_COMPILER=gcc
-DCMAKE_CXX_COMPILER=g++
-DCMAKE_Fortran_COMPILER=gfortran
" > SERIAL_RELEASE_CMAKE-3.6.2.config

# Run checkin-test.py

$TRIBITS_BASE_DIR_ABS/checkin-test.py \
--extra-cmake-options="-DPYTHON_EXECUTABLE=/usr/bin/python2.6" \
--default-builds= \
--st-extra-builds=MPI_DEBUG_CMAKE-3.6.2,SERIAL_RELEASE_CMAKE-3.6.2 \
--ctest-timeout=180 \
--skip-case-no-email \
"$@"
