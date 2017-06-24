#!/bin/bash
# 
# Used to test and push TriBITS on crf450 using the VERA Dev Env with CMake
# 3.8.11 and CMake 3.6.2.
#
# Unlike regular checkin-tset.py drivers, this script is hard-coded with
# --do-all --push and does not accept any other arguments.  To use this, you
# need to also symlink in the scripts checkin-test-crf450-cmake-2.8.11.sh
# checkin-test-crf450-cmake-3.6.2.sh then run as:
#
#   $ ./checkin-test-crf450-cmake-3.6.2.sh
#
# WARNING: This does the --push as well so make sure you want to do that!
#
# You can skip the push by running with:
#
#   $ env CHECKIN_TEST_CRF450_SKIP_PUSH=1 ./checkin-test-crf450-cmake-3.6.2.sh
#
# You can also just do a local test with:
#
#   $ env CHECKIN_TEST_CRF450_SKIP_PUSH=1 \
#      CHECKIN_TEST_CRF450_LOCAL_DO_ALL=1 \
#      ./checkin-test-crf450-cmake-3.6.2.sh
#
# This script does not send out any email except for the final checkin-test.py
# --push command.
#
# NOTE: This script is NOT run with 'bash -e' so failures in the individual
# checkin-test calls are ignored until the final checkin-test.py script is
# called.  But that final checkin-test.py script will not push unless all of
# the listed builds all passed.
#

if [ "$TRIBITS_BASE_DIR" == "" ] ; then
  _ABS_FILE_PATH=`readlink -f $0`
  _SCRIPT_DIR=`dirname $_ABS_FILE_PATH`
  TRIBITS_BASE_DIR=$_SCRIPT_DIR/../..
fi

TRIBITS_BASE_DIR_ABS=$(readlink -f $TRIBITS_BASE_DIR)
#echo "TRIBITS_BASE_DIR_ABS = $TRIBITS_BASE_DIR_ABS"

if [ "$CHECKIN_TEST_CRF450_LOCAL_DO_ALL" == "1" ] ; then
  CHECKIN_TEST_1_DO_ALL_ARG=--local-do-all
  CHECKIN_TEST_2_ALLOW_NO_PULL_ARG=--allow-no-pull
else
  CHECKIN_TEST_1_DO_ALL_ARG=--do-all
  CHECKIN_TEST_2_ALLOW_NO_PULL_ARG=
fi

if [ "$CHECKIN_TEST_CRF450_SKIP_PUSH" == "1" ] ; then
  CHECKIN_TEST_PUSH_ARG=
else
  CHECKIN_TEST_PUSH_ARG=--push
fi

echo
echo "***"
echo "*** A) Running checkin-test-crf450-cmake-2.8.11.sh $CHECKIN_TEST_1_DO_ALL_ARG --send-email-to= ..."
echo "***"
echo

./checkin-test-crf450-cmake-2.8.11.sh $CHECKIN_TEST_1_DO_ALL_ARG --send-email-to=

echo
echo "***"
echo "*** B) Running checkin-test-crf450-cmake-3.6.2.sh $CHECKIN_TEST_2_ALLOW_NO_PULL_ARG --configure --build --test --send-email-to= ..."
echo "***"
echo

./checkin-test-crf450-cmake-3.6.2.sh $CHECKIN_TEST_2_ALLOW_NO_PULL_ARG --configure --build --test --send-email-to=

echo
echo "***"
echo "*** C) Running checkin-test.py [all the builds] --no-rebase $CHECKIN_TEST_PUSH_ARG ..."
echo "***"
echo

$TRIBITS_BASE_DIR_ABS/checkin-test.py \
--st-extra-builds=MPI_DEBUG_CMAKE-3.6.2,SERIAL_RELEASE_CMAKE-3.6.2 \
--no-rebase $CHECKIN_TEST_PUSH_ARG
