# @HEADER
# ************************************************************************
#
#            TriBITS: Tribal Build, Integrate, and Test System
#                    Copyright 2013 Sandia Corporation
#
# Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
# the U.S. Government retains certain rights in this software.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the Corporation nor the names of the
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY SANDIA CORPORATION "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL SANDIA CORPORATION OR THE
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# ************************************************************************
# @HEADER

message("CURRENT_TEST_DIRECTORY = ${CURRENT_TEST_DIRECTORY}")

include(${CMAKE_CURRENT_LIST_DIR}/TribitsAdjustPackageEnablesHelpers.cmake)
include(TribitsPackageMacros)
include(TribitsWriteClientExportFiles)


#####################################################################
#
# Unit tests for code in TribitsWriteClientExportFiles.cmake
#
#####################################################################


macro(setup_write_specialized_package_export_makefile_test_stuff)

  # These would be set the TriBITS env probing code or by CMake
  set(${PROJECT_NAME}_ENABLE_C ON)
  set(${PROJECT_NAME}_ENABLE_CXX ON)
  set(${PROJECT_NAME}_ENABLE_Fortran ON)

  # These would be set automatically by CMake if we were not in script mode!
  set(CMAKE_LINK_LIBRARY_FLAG -l)
  set(CMAKE_LIBRARY_PATH_FLAG -L)

  # Make sure this is defined!
  assert_defined(${PROJECT_NAME}_TRIBITS_DIR)

  # Need to define these:
  set(${PROJECT_NAME}_INSTALL_LIB_DIR "dummy_install_lib_dir")
  set(${PROJECT_NAME}_INSTALL_INCLUDE_DIR "dummy_install_include_dir")

endmacro()


#
# A) Test basic package processing and reading dependencies
#


function(unittest_write_specialized_package_export_makefile_rtop_before_libs)

  message("\n***")
  message("*** Testing the generation of a specialized export makefile for RTOp *before* libs")
  message("***\n")

  setup_write_specialized_package_export_makefile_test_stuff()

  # Debugging
  set(${PROJECT_NAME}_VERBOSE_CONFIGURE ON)
  set(TRIBITS_WRITE_FLEXIBLE_PACKAGE_CLIENT_EXPORT_FILES_DEBUG_DUMP ON)

  set(${PROJECT_NAME}_ENABLE_RTOp ON)
  set(${PROJECT_NAME}_GENERATE_EXPORT_FILE_DEPENDENCIES ON)

  unittest_helper_read_and_process_packages()

  # These are basic global VARS we want to pass along
  set(CMAKE_BUILD_TYPE DEBUG)

  # These vars would be set up by the FindTPL<TPLNAME>.cmake modules if they
  # were called
  set(TPL_BLAS_LIBRARIES "blaspath/lib/libblas.a")
  set(TPL_BLAS_LIBRARY_DIRS "blashpath/lib")
  set(TPL_BLAS_INCLUDE_DIRS "blaspath/include")
  set(TPL_LAPACK_LIBRARIES "lapackpath/lib/liblapack.a")
  set(TPL_LAPACK_LIBRARY_DIRS "lapackhpath/lib")
  set(TPL_LAPACK_INCLUDE_DIRS "lapackhpath/include")

  # These vars should be generated automatically by tribits_package() that
  # begins with the upstreams packages.
  set(Teuchos_LIBRARY_DIRS "teuchos/core/src;teuchos/numeric/src")
  set(Teuchos_INCLUDE_DIRS "teuchos/core/include;teuchos/numeric/include")
  set(Teuchos_LIBRARIES "teuchoscore;teuchosnumeric")
  set(Teuchos_HAS_NATIVE_LIBRARIES_TO_INSTALL TRUE)

  set(GENERATED_EXPORT_CONFIG
    "${CURRENT_TEST_DIRECTORY}/RTOpBeforeConfig.cmake")

  set(GENERATED_EXPORT_MAKEFILE
    "${CURRENT_TEST_DIRECTORY}/Makefile.export.RTOp.before")

  tribits_write_flexible_package_client_export_files(
    PACKAGE_NAME RTOp
    EXPORT_FILE_VAR_PREFIX RTOp1
    WRITE_CMAKE_CONFIG_FILE "${GENERATED_EXPORT_CONFIG}"
    WRITE_EXPORT_MAKEFILE "${GENERATED_EXPORT_MAKEFILE}"
    )

  unittest_file_regex("${GENERATED_EXPORT_CONFIG}"
    REGEX_STRINGS
      "set[(]RTOp1_CMAKE_BUILD_TYPE .DEBUG."
      "if [(]RTOp1_CONFIG_INCLUDED."
      "set[(]RTOp1_CONFIG_INCLUDED TRUE."
      "set[(]RTOp1_INCLUDE_DIRS .teuchos/core/include.teuchos/numeric/include.."
      "set[(]RTOp1_LIBRARY_DIRS .teuchos/core/src.teuchos/numeric/src.."
      "set[(]RTOp1_LIBRARIES .teuchoscore.teuchosnumeric.."
      "set[(]RTOp1_TPL_INCLUDE_DIRS .lapackhpath/include.blaspath/include.."
      "set[(]RTOp1_TPL_LIBRARY_DIRS .lapackhpath/lib.blashpath/lib.."
      "set[(]RTOp1_TPL_LIBRARIES .lapackpath/lib/liblapack.a.blaspath/lib/libblas.a.."
      "set[(]RTOp1_PACKAGE_LIST .Teuchos.."
      "set[(]RTOp1_TPL_LIST .LAPACK.BLAS.."
    )

  unittest_file_regex("${GENERATED_EXPORT_MAKEFILE}"
    REGEX_STRINGS
      "RTOp1_INCLUDE_DIRS= -Iteuchos/core/include -Iteuchos/numeric/include"
      "RTOp1_LIBRARY_DIRS= -Lteuchos/core/src -Lteuchos/numeric/src"
      "RTOp1_LIBRARIES= -lteuchoscore -lteuchosnumeric"
      "RTOp1_TPL_INCLUDE_DIRS= -Ilapackhpath/include -Iblaspath/include"
      "RTOp1_TPL_LIBRARIES= -llapackpath/lib/liblapack.a -lblaspath/lib/libblas.a"
      "RTOp1_PACKAGE_LIST= Teuchos"
      "RTOp1_TPL_LIST= LAPACK BLAS"
    )

endfunction()


function(unittest_write_specialized_package_export_makefile_rtop_after_libs)

  message("\n***")
  message("*** Testing the generation of a specialized export makefile for RTOp *after* libs")
  message("***\n")

  setup_write_specialized_package_export_makefile_test_stuff()

  # Debugging
  set(${PROJECT_NAME}_VERBOSE_CONFIGURE ON)
  set(TRIBITS_WRITE_FLEXIBLE_PACKAGE_CLIENT_EXPORT_FILES_DEBUG_DUMP ON)

  set(${PROJECT_NAME}_ENABLE_RTOp ON)
  set(${PROJECT_NAME}_GENERATE_EXPORT_FILE_DEPENDENCIES ON)

  unittest_helper_read_and_process_packages()

  # These are basic global VARS we want to pass along
  set(CMAKE_BUILD_TYPE RELEASE)

  # These vars would be set up by the FindTPL<TPLNAME>.cmake modules if they
  # were called
  set(TPL_BLAS_LIBRARIES "blaspath/lib/libblas.a")
  set(TPL_BLAS_LIBRARY_DIRS "blashpath/lib")
  set(TPL_BLAS_INCLUDE_DIRS "blaspath/include")
  set(TPL_LAPACK_LIBRARIES "lapackpath/lib/liblapack.a")
  set(TPL_LAPACK_LIBRARY_DIRS "lapackhpath/lib")
  set(TPL_LAPACK_INCLUDE_DIRS "lapackhpath/include")

  # These vars should be generated automatically by tribits_package() that
  # begins with the upstreams packages.
  set(Teuchos_LIBRARY_DIRS "teuchos/core/src;teuchos/numeric/src")
  set(Teuchos_INCLUDE_DIRS "teuchos/core/include;teuchos/numeric/include")
  set(Teuchos_LIBRARIES "teuchoscore;teuchosnumeric")
  set(Teuchos_HAS_NATIVE_LIBRARIES_TO_INSTALL TRUE)
  set(RTOp_LIBRARY_DIRS "rtop/src;teuchos/core/src;teuchos/numeric/src")
  set(RTOp_INCLUDE_DIRS "rtop/include;teuchos/core/include;teuchos/numeric/include")
  set(RTOp_LIBRARIES "rtop")
  set(RTOp_HAS_NATIVE_LIBRARIES_TO_INSTALL TRUE)

  set(GENERATED_EXPORT_CONFIG
    "${CURRENT_TEST_DIRECTORY}/RTOpAfterConfig.cmake")

  set(GENERATED_EXPORT_MAKEFILE
    "${CURRENT_TEST_DIRECTORY}/Makefile.export.RTOp.after")

  tribits_write_flexible_package_client_export_files(
    PACKAGE_NAME RTOp
    EXPORT_FILE_VAR_PREFIX RTOp2
    WRITE_CMAKE_CONFIG_FILE "${GENERATED_EXPORT_CONFIG}"
    WRITE_EXPORT_MAKEFILE "${GENERATED_EXPORT_MAKEFILE}"
    )

  unittest_file_regex("${GENERATED_EXPORT_CONFIG}"
    REGEX_STRINGS
      "set[(]RTOp2_CMAKE_BUILD_TYPE .RELEASE."
      "if [(]RTOp2_CONFIG_INCLUDED."
      "set[(]RTOp2_CONFIG_INCLUDED TRUE."
      "set[(]RTOp2_INCLUDE_DIRS .rtop/include.teuchos/core/include.teuchos/numeric/include.."
      "set[(]RTOp2_LIBRARY_DIRS .rtop/src.teuchos/core/src.teuchos/numeric/src.."
      "set[(]RTOp2_LIBRARIES .rtop.teuchoscore.teuchosnumeric.."
      "set[(]RTOp2_TPL_INCLUDE_DIRS .lapackhpath/include.blaspath/include.."
      "set[(]RTOp2_TPL_LIBRARY_DIRS .lapackhpath/lib.blashpath/lib.."
      "set[(]RTOp2_TPL_LIBRARIES .lapackpath/lib/liblapack.a.blaspath/lib/libblas.a.."
      "set[(]RTOp2_PACKAGE_LIST .RTOp.Teuchos.."
      "set[(]RTOp2_TPL_LIST .LAPACK.BLAS.."
    )

  unittest_file_regex("${GENERATED_EXPORT_MAKEFILE}"
    REGEX_STRINGS
      "RTOp2_INCLUDE_DIRS= -Irtop/include -Iteuchos/core/include -Iteuchos/numeric/include"
      "RTOp2_LIBRARY_DIRS= -Lrtop/src -Lteuchos/core/src -Lteuchos/numeric/src"
      "RTOp2_LIBRARIES= -lrtop -lteuchoscore -lteuchosnumeric"
      "RTOp2_TPL_INCLUDE_DIRS= -Ilapackhpath/include -Iblaspath/include"
      "RTOp2_TPL_LIBRARIES= -llapackpath/lib/liblapack.a -lblaspath/lib/libblas.a"
      "RTOp2_PACKAGE_LIST= RTOp Teuchos"
      "RTOp2_TPL_LIST= LAPACK BLAS"
    )

endfunction()


#####################################################################
#
# Execute the unit tests
#
#####################################################################

# Assume that all unit tests will pass by default
global_set(UNITTEST_OVERALL_PASS TRUE)
global_set(UNITTEST_OVERALL_NUMPASSED 0)
global_set(UNITTEST_OVERALL_NUMRUN 0)

#
# Run the unit tests
#

unittest_write_specialized_package_export_makefile_rtop_before_libs()
unittest_write_specialized_package_export_makefile_rtop_after_libs()

# Pass in the number of expected tests that must pass!
unittest_final_result(36)
