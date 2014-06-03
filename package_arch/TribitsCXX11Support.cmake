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

INCLUDE(CheckCXXSourceCompiles)


#
# Sets up C++11 flags if not already set.
#
# On input, if ${PROJECT_NAME}_CXX11_FLAGS is already set, then this
# function does nothing.  If not already set on input, then a set of
# try-compile (but not try-run) commands are performed to try common C++11
# compiler flags testing against known flags.  If a set of flags is found that
# enables C++11, then those flags are used.  The first set of flags that
# passes the try-compile test is set into the cache variable
# ${PROJECT_NAME}_CXX11_FLAGS on output.
# 
FUNCTION(TRIBITS_FIND_CXX11_FLAGS)

  ##
  ## Only try introspection if we have not already
  ## or if the user has not overridden then
  ##

  IF(NOT ${PROJECT_NAME}_CXX11_FLAGS)

     MESSAGE("-- " "Search for C++11 compiler flag ...")
     INCLUDE(CheckCXXSourceCompiles)

     ##
     ## List of possible compiler flags to use
     ##
     SET(CXX11_FLAG_OPTIONS
       "-std=c++11"    # intel/clang linux/mac
       "-std=c++0x"    # Older gcc
       "-std=gnu++11"  # gcc
       "/Qstd=c++11"   # intel windows
       )

     ##
     ## Same CXX11 source
     ##
     SET(TSOURCE
        "
        #include <vector>
        #include <algorithm>
        int main() {
          // check >> closing brackets
          std::vector<std::vector<float>> vecvecfloat(1);
          vecvecfloat[0].resize(1);
          vecvecfloat[0][0] = 0.0f;
          std::vector<int> vec(10);
          auto b        = vec.begin();
          decltype(b) e = vec.end();
          std::fill(b,e,1);
          // two examples, taken from the wikipedia article on C++0x :)
          std::vector<int> some_list;
          int total = 0;
          int value = 5;
          std::for_each(some_list.begin(), some_list.end(), [&total](int x) {
              total += x;
              });
          std::for_each(some_list.begin(), some_list.end(), [&, value](int x) {
              total += x * value;
              });
          return 0;
        }
        "
     )

     ##
     ## Try to compile with each flag
     ##

     SET(TOPTION_IDX "0")
     FOREACH( TOPTION ${CXX11_FLAG_OPTIONS})

        IF(${PROJECT_NAME}_VERBOSE_CONFIGURE OR TRIBITS_ENABLE_CXX11_DEBUG_DUMP)
          MESSAGE("-- " "Testing C++11 flag: ${TOPTION}")
        ENDIF()

        SET(CMAKE_REQUIRED_FLAGS "${CMAKE_CXX_FLAGS} ${TOPTION}")

        SET(CXX11_FLAGS_COMPILE_RESULT_VAR CXX11_FLAGS_COMPILE_RESULT_${TOPTION_IDX})

        CHECK_CXX_SOURCE_COMPILES("${TSOURCE}" ${CXX11_FLAGS_COMPILE_RESULT_VAR}
           ## Some compilers do not fail with a bad flag
           FAIL_REGEX "unrecognized .*option"                     # GNU
           FAIL_REGEX "unrecognized .*option"                     # GNU
           FAIL_REGEX "ignoring unknown option"                   # MSVC
           FAIL_REGEX "warning D9002"                             # MSVC, any lang
           FAIL_REGEX "[Uu]nknown option"                         # HP
           FAIL_REGEX "[Ww]arning: [Oo]ption"                     # SunPro
           FAIL_REGEX "command option .* is not recognized"       # XL
        )

        IF(${CXX11_FLAGS_COMPILE_RESULT_VAR})
          MESSAGE("-- " "Successful C++11 flag: '${TOPTION}'")
          ADVANCED_SET(${PROJECT_NAME}_CXX11_FLAGS ${TOPTION}
            CACHE STRING
            "Special C++ compiler flags to turn on C++11 support.  Determined automatically by default."
            )
          BREAK()
        ENDIF()

        MATH(EXPR TOPTION_IDX "${TOPTION_IDX}+1")

     ENDFOREACH()

  ELSE()

     ##
     ## We already detected or set the cxx11 flags
     ##
     MESSAGE("-- " "C++11 Flags already set: '${${PROJECT_NAME}_CXX11_FLAGS}'")

  ENDIF()

ENDFUNCTION()


#
# Assert of C++11 support is working and otherwise disable support.
#

FUNCTION(TRIBITS_CHECK_CXX11_SUPPORT VARNAME)

  INCLUDE(CheckCXXSourceCompiles)

  IF (${PROJECT_NAME}_CXX11_FLAGS)
    SET(CMAKE_REQUIRED_FLAGS "${CMAKE_REQUIRED_FLAGS} ${${PROJECT_NAME}_CXX11_FLAGS}")
  ENDIF()

  # support for >> in addition to > > when closing double templates
  SET(SOURCE_CXX11_CONSECUTIVE_RIGHT_ANGLE_BRACKETS
  "
#include <vector>
int main() {
  // check >> closing brackets
  std::vector<std::vector<float>> vecvecfloat(1);
  vecvecfloat[0].resize(1);
  vecvecfloat[0][0] = 0.0f;
  return 0;
}
  "
  )
  CHECK_CXX_SOURCE_COMPILES("${SOURCE_CXX11_CONSECUTIVE_RIGHT_ANGLE_BRACKETS}"
    CXX11_CONSECUTIVE_RIGHT_ANGLE_BRACKETS)

  # support for auto and typedecl()
  SET(SOURCE_CXX11_AUTOTYPEDVARIABLES
  "
#include <vector>
int main() {
  std::vector<int> vec(10);
  auto b        = vec.begin();
  decltype(b) e = vec.end();
  std::fill(b,e,1);
  return 0;
}
  "
  )
  CHECK_CXX_SOURCE_COMPILES("${SOURCE_CXX11_AUTOTYPEDVARIABLES}"
    CXX11_AUTOTYPEDVARIABLES)

  # support for lambda expressions
  SET(SOURCE_CXX11_LAMBDAS
  "
#include <vector>
#include <algorithm>
int main() {
  // two examples, taken from the wikipedia article on C++0x :)
  std::vector<int> some_list;
  int total = 0;
  int value = 5;
  std::for_each(some_list.begin(), some_list.end(), [&total](int x) {
      total += x;
      });
  std::for_each(some_list.begin(), some_list.end(), [&, value](int x) {
      total += x * value;
      });
  // 
  return 0;
}
  "
  )

  CHECK_CXX_SOURCE_COMPILES("${SOURCE_CXX11_LAMBDAS}" CXX11_LAMBDAS)

  IF (NOT CXX11_CONSECUTIVE_RIGHT_ANGLE_BRACKETS OR
    NOT CXX11_AUTOTYPEDVARIABLES OR
    NOT CXX11_LAMBDAS
    )
    SET(${VARNAME} FALSE PARENT_SCOPE)
  ELSE()
    SET(${VARNAME} TRUE PARENT_SCOPE)
  ENDIF()

ENDFUNCTION()
