#!/bin/bash -e

#
# Run local configure/build/test and submit to CDash with
# tribits_ctest_driver().
#
# Usage:
#
#   $ cd <some-base-dir>/
#
#   <this-dir>/run_github_actions_ctest_driver.sh \
#     --os <os> --cmake-ver <cmake-ver> \
#     --generator ninja|makefiles \
#     --python-ver <python-ver> \
#     --cxx-compiler-and-ver <cxx-compiler-and-ver> \
#     [ --fortran-compiler-and-ver <fortran-comiler-and-ver> ]
#
# This is called by the GitHub Actions script:
#
#   TriBITS/.github/workflows/tribits_testing.yml
#
# but can also be run locally to develop on and debug.
#
# NOTE: This will create the subdir 'tribits-build' under $PWD if that
# directory does not already exist.  But it will not delete an existing
# directly 'tribits-build' if it already exists (but that is usually fine to
# do rebulids).
#
# NOTE: One can control various behaviors and other options as documented with
# tribits_ctest_driver() including not submitting to CDash to do testing
# output spamming CDash by running with:
#
#   env CTEST_DO_SUBMIT=OFF <this-dir>/run_github_actions_ctest_driver.sh [options]
#

# Get locaiton of TriBITS
if [ "$TRIBITS_BASE_DIR" == "" ] ; then
  _ABS_FILE_PATH=`readlink -f $0`
  _BASE_DIR=`dirname $_ABS_FILE_PATH`
  TRIBITS_BASE_DIR=`realpath $_BASE_DIR/../../..` 
fi


#
# Functions
#


function assert_required_option {
  arg_name=$1
  arg_value=$2
  #echo "${arg_name} ${arg_value}"
  if [[ "${arg_value}" == "" ]] ; then
    echo "Error, argument ${arg_name} can not be empty!"
    exit 1
  fi
}


#
# A) Parse and assert command-line arguments
#

os=
cmake_ver=
cmake_generator=
python_ver=
cxx_compiler_and_ver=
fortran_compiler_and_ver=

while (( "$#" )); do
  case "$1" in
    --os)
      os=$2
      shift 2
      ;;
    --cmake-ver)
      cmake_ver=$2
      shift 2
      ;;
    --generator)
      cmake_generator=$2
      shift 2
      ;;
    --python-ver)
      python_ver=$2
      shift 2
      ;;
    --cxx-compiler-and-ver)
      cxx_compiler_and_ver=$2
      shift 2
      ;;
    --fortran-compiler-and-ver)
      fortran_compiler_and_ver=$2
      shift 2
      ;;
    *)
      echo "Error: The argument '$1' is not supported!"
      exit 1
      ;;
  esac
done

assert_required_option --os ${os}
assert_required_option --cmake-ver "${cmake_ver}"
assert_required_option --generator "${cmake_generator}"
assert_required_option --python-ver "${python_ver}"
assert_required_option --cxx-compiler-and-ver "${cxx_compiler_and_ver}"
# NOTE: Fortran is not required!

#
# B) Set up options for running build
#

# CTEST_SITE
export CTEST_SITE=${os}

# CTEST_BUILD_NAME
CTEST_BUILD_NAME=tribits_cmake-${cmake_ver}_${cmake_generator}_python-${python_ver}_${cxx_compiler_and_ver}
if [[ "${fortran_compiler_and_ver}" == "" ]] ; then
  CTEST_BUILD_NAME=${CTEST_BUILD_NAME}_nofortran
fi
export CTEST_BUILD_NAME

# CTEST_CMAKE_GENERATOR
if [[ "${cmake_generator}" == "ninja" ]] ; then
  CTEST_CMAKE_GENERATOR=Ninja
elif [[ "${cmake_generator}" == "makefiles" ]] ; then
  CTEST_CMAKE_GENERATOR="Unix Makefiles"
else
  echo "Error, --generator ${cmake_generator} is invalid!  Only 'makefiles', 'ninja'!"
  exit 1
fi
export CTEST_CMAKE_GENERATOR

#
# C) Run the local configure, build, test and submit using exported vars above
#

if [[ -d tribits-build ]] ; then
  echo "tribits-build/ already exists so leaving it."
else
  echo "tribits-build/ does not exist yet so creating it."
  mkdir tribits-build
fi

cd tribits-build/

ctest -V -S \
  ${TRIBITS_BASE_DIR}/cmake/ctest/github_actions/ctest_github_actions_serial_debug.cmake
