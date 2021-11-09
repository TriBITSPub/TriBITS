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


########################################################################
# TribitsExampleProject2 TPLs Install Tests
########################################################################


function(TribitsExampleProject2_Tpls_install_tests sharedOrStatic)

  if (sharedOrStatic STREQUAL "SHARED")
    set(buildSharedLibsArg
      -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_RPATH_USE_LINK_PATH=TRUE
      -DCMAKE_MACOSX_RPATH=TRUE)
  elseif (sharedOrStatic STREQUAL "STATIC")
    set(buildSharedLibsArg -DBUILD_SHARED_LIBS=OFF)
  else()
    message(FATAL_ERROR "Invaid value for sharedOrStatic='${sharedOrStatic}'!")
  endif()

  # A) Build and install Tpl1, ???

  set(testNameBase TribitsExampleProject2_Tpls_install_${sharedOrStatic})
  set(testName ${PACKAGE_NAME}_${testNameBase})
  set(testDir ${CMAKE_CURRENT_BINARY_DIR}/${testName})

  tribits_add_advanced_test( ${testNameBase}
    OVERALL_WORKING_DIRECTORY TEST_NAME
    OVERALL_NUM_MPI_PROCS 1

    TEST_0
      MESSAGE "Copy source for Tpl1"
      CMND ${CMAKE_COMMAND}
      ARGS -E copy_directory ${${PROJECT_NAME}_TRIBITS_DIR}/examples/tpls/Tpl1 .
      WORKING_DIRECTORY Tpl1

    TEST_1
      MESSAGE "Configure Tpl1"
      WORKING_DIRECTORY build_tpl1
      CMND ${CMAKE_COMMAND}
      ARGS
        ${SERIAL_PASSTHROUGH_CONFIGURE_ARGS}
        ${buildSharedLibsArg}
        -DCMAKE_BUILD_TYPE=RelWithDepInfo
        -DCMAKE_INSTALL_PREFIX=${testDir}/install
        -DCMAKE_INSTALL_INCLUDEDIR=include
        -DCMAKE_INSTALL_LIBDIR=lib
        ${testDir}/Tpl1
      PASS_REGULAR_EXPRESSION_ALL
        "Configuring done"
        "Generating done"
      ALWAYS_FAIL_ON_NONZERO_RETURN

    TEST_2
      MESSAGE "Build and install Tpl1"
      WORKING_DIRECTORY build_tpl1
      SKIP_CLEAN_WORKING_DIRECTORY
      CMND make ARGS ${CTEST_BUILD_FLAGS} install
      PASS_REGULAR_EXPRESSION_ALL
        "Built target tpl1"
        "Installing: ${testDir}/install/lib/libtpl1[.]"
        "Installing: ${testDir}/install/include/Tpl1.hpp"
      ALWAYS_FAIL_ON_NONZERO_RETURN

    TEST_3
      MESSAGE "Delete source and build directory for Tpl1"
      CMND ${CMAKE_COMMAND} ARGS -E rm -rf Tpl1 build_tpl1

      ADDED_TEST_NAME_OUT
        TribitsExampleProject2_Tpls_install_${sharedOrStatic}_NAME
    )

  # Name of added test to use to create test dependencies
  set(TribitsExampleProject2_Tpls_install_${sharedOrStatic}_NAME
    ${TribitsExampleProject2_Tpls_install_${sharedOrStatic}_NAME} PARENT_SCOPE)

  # Reusable location of the SimpleTPL install
  set(TribitsExampleProject2_Tpls_install_${sharedOrStatic}_DIR ${testDir}
    PARENT_SCOPE)

endfunction()


TribitsExampleProject2_Tpls_install_tests(SHARED)
TribitsExampleProject2_Tpls_install_tests(STATIC)
