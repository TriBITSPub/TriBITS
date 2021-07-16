#!/bin/bash -e
#
# Build all of the TriBITS-related documentation
#
# To build this documentation, from any directory, run:
#
#   <base-dir>/build_docs.sh
#

if [ "$TRIBITS_BASE_DIR" == "" ] ; then
  _ABS_FILE_PATH=`readlink -f $0`
  _BASE_DIR=`dirname $_ABS_FILE_PATH`
fi

cd $_BASE_DIR

echo
echo "***"
echo "*** Generating Users and Maintainers guides ..."
echo "***"
echo

cd $_BASE_DIR/guides/
./generate-guide.sh all 
cd -
echo
echo "See generated files:"
echo
ls $_BASE_DIR/guides/users_guide/TribitsUsersGuide.*
ls $_BASE_DIR/guides/maintainers_guide/TribitsMaintainersGuide.*

echo
echo "***"
echo "*** Generating TribitsBuildReference.[rst,html,pdf] ..."
echo "***"
echo

cd $_BASE_DIR/build_ref
./create-build-ref.sh  
echo
echo "See generated files:"
echo
ls $_BASE_DIR/build_ref/TribitsBuildReference.*

#echo
#echo "***"
#echo "*** Generating TribitsOverview.pdf ..."
#echo "***"
#echo
#
#cd $_BASE_DIR/overview
#source source_set_env 
#make
#echo
#echo "See generated files:"
#echo
#ls $_BASE_DIR/overview/TribitsOverview.pdf
#
#echo
#echo "***"
#echo "*** Generating TribitsLifecycleModel.pdf ..."
#echo "***"
#echo
#
#cd $_BASE_DIR/lifecycle_model
#make
#echo
#echo "See generated files:"
#echo
#ls $_BASE_DIR/lifecycle_model/TribitsLifecycleModel.pdf
