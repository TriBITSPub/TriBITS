########################################################################
# TribitsExampleProject2
########################################################################


set(TribitsExampleProject2_COMMON_CONFIG_ARGS
  ${SERIAL_PASSTHROUGH_CONFIGURE_ARGS}
  -DTribitsExProj2_TRIBITS_DIR=${${PROJECT_NAME}_TRIBITS_DIR}
  -DTribitsExProj2_ENABLE_Fortran=${${PROJECT_NAME}_ENABLE_Fortran}
  )


########################################################################


if (NOT "$ENV{TRIBITS_ADD_ENV_PATH_HACK_FOR_TPL1}" STREQUAL "")
  set(TRIBITS_ADD_ENV_PATH_HACK_FOR_TPL1_DEFAULT
    $ENV{TRIBITS_ADD_ENV_PATH_HACK_FOR_TPL1})
else()
  set($ENV{TRIBITS_ADD_ENV_PATH_HACK_FOR_TPL1} OFF)
endif()
advanced_set(TRIBITS_ADD_ENV_PATH_HACK_FOR_TPL1
  ${TRIBITS_ADD_ENV_PATH_HACK_FOR_TPL1_DEFAULT} CACHE BOOL
  "Set to TRUE to add LD_LIBRARY_PATH to libtpl1.so for platforms where RPATH not working")

function(set_ENV_PATH_HACK_FOR_TPL1_ARG sharedOrStatic)
  if (sharedOrStatic STREQUAL "SHARED")
    if (WIN32)
      set(ENV_PATH_HACK_FOR_TPL1_${sharedOrStatic}_ARG_ON
        ENVIRONMENT
	LD_LIBRARY_PATH=${TribitsExampleProject2_Tpls_install_${sharedOrStatic}_DIR}/install_tpl1/lib)
    else()
      set(ENV_PATH_HACK_FOR_TPL1_${sharedOrStatic}_ARG_ON
        ENVIRONMENT
	PATH=${TribitsExampleProject2_Tpls_install_${sharedOrStatic}_DIR}/install_tpl1/bin:$ENV{PATH})
    endif()
  else()
    set(ENV_PATH_HACK_FOR_TPL1_${sharedOrStatic}_ARG_ON "")
  endif()
  if (TRIBITS_ADD_ENV_PATH_HACK_FOR_TPL1)
    set(ENV_PATH_HACK_FOR_TPL1_${sharedOrStatic}_ARG
      ${ENV_PATH_HACK_FOR_TPL1_${sharedOrStatic}_ARG_ON})
  else()
    set(ENV_PATH_HACK_FOR_TPL1_${sharedOrStatic}_ARG "")
  endif()
  set(ENV_PATH_HACK_FOR_TPL1_${sharedOrStatic}_ARG_ON
    ${ENV_PATH_HACK_FOR_TPL1_${sharedOrStatic}_ARG_ON}
    PARENT_SCOPE)
  set(ENV_PATH_HACK_FOR_TPL1_${sharedOrStatic}_ARG
    ${ENV_PATH_HACK_FOR_TPL1_${sharedOrStatic}_ARG}
    PARENT_SCOPE)
endfunction()
set_ENV_PATH_HACK_FOR_TPL1_ARG(STATIC)
set_ENV_PATH_HACK_FOR_TPL1_ARG(SHARED)
# NOTE: Above, we have to set LD_LIBRARY_PATH to pick up the
# libtpl1.so because CMake 3.17.5 and 3.21.2 with the GitHub Actions
# Umbuntu build is refusing to put in the RPATH for libtpl1.so into
# libsimplecxx.so even through CMAKE_INSTALL_RPATH_USE_LINK_PATH=ON is
# set.  This is not needed for the RHEL 7 builds that I have tried where
# CMake is behaving correctly and putting in RPATH correctly.  But because
# I can't log into this system, it is very hard and time consuming to
# debug this so I am just giving up at this point.



########################################################################


macro(TribitsExampleProject2_test_setup_header)
  if (sharedOrStatic STREQUAL "SHARED")
    set(buildSharedLibsArg -DBUILD_SHARED_LIBS=ON)
    if (CYGWIN)
      set(libext ".dll.a")
    else()
      set(libext ".so")
    endif()
  elseif (sharedOrStatic STREQUAL "STATIC")
    set(buildSharedLibsArg -DBUILD_SHARED_LIBS=OFF)
    set(libext ".a")
  else()
    message(FATAL_ERROR "Invalid value for sharedOrStatic='${sharedOrStatic}'!")
  endif()
endmacro()


########################################################################


function(TribitsExampleProject2_find_tpl_parts_test sharedOrStatic)

  TribitsExampleProject2_test_setup_header()

  set(testNameBase TribitsExampleProject2_find_tpl_parts_${sharedOrStatic})
  set(testName ${PACKAGE_NAME}_${testNameBase})
  set(testDir "${CMAKE_CURRENT_BINARY_DIR}/${testName}")

  tribits_add_advanced_test( ${testNameBase}
    OVERALL_WORKING_DIRECTORY TEST_NAME
    OVERALL_NUM_MPI_PROCS 1
    LIST_SEPARATOR "<semicolon>"

    TEST_0
      MESSAGE "Configure TribitsExampleProject2 against pre-installed Tpl1"
      CMND ${CMAKE_COMMAND}
      ARGS
        ${TribitsExampleProject2_COMMON_CONFIG_ARGS}
        -DCMAKE_BUILD_TYPE=DEBUG
        "-DTpl1_INCLUDE_DIRS=${TribitsExampleProject2_Tpls_install_${sharedOrStatic}_DIR}/install_tpl1/include"
        "-DTpl1_LIBRARY_DIRS=${TribitsExampleProject2_Tpls_install_${sharedOrStatic}_DIR}/install_tpl1/lib"
        -DTPL_ENABLE_Tpl3=ON
        "-DTpl3_INCLUDE_DIRS=${TribitsExampleProject2_Tpls_install_${sharedOrStatic}_DIR}/install_tpl3/include"
        "-DTpl3_LIBRARY_DIRS=${TribitsExampleProject2_Tpls_install_${sharedOrStatic}_DIR}/install_tpl3/lib<semicolon>${TribitsExampleProject2_Tpls_install_${sharedOrStatic}_DIR}/install_tpl2/lib"
        "-DTpl3_LIBRARY_NAMES=tpl3<semicolon>tpl2a<semicolon>tpl2b"
        -DTribitsExProj2_ENABLE_TESTS=ON
        -DCMAKE_INSTALL_PREFIX=install
        -DTribitsExProj2_ENABLE_Package1=ON
        -DTribitsExProj2_ENABLE_Package2=ON
        ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject2
      ALWAYS_FAIL_ON_NONZERO_RETURN
      PASS_REGULAR_EXPRESSION_ALL
        "Final set of enabled packages:  Package1 Package2 2"
	"Final set of enabled TPLs:  Tpl1 Tpl3 2"
        "Searching for libs in Tpl1_LIBRARY_DIRS='.*/TriBITS_TribitsExampleProject2_Tpls_install_${sharedOrStatic}/install_tpl1/lib'"
        "Found lib '.*/TriBITS_TribitsExampleProject2_Tpls_install_${sharedOrStatic}/install_tpl1/lib/libtpl1${libext}'"
        "TPL_Tpl1_LIBRARIES='.*/TriBITS_TribitsExampleProject2_Tpls_install_${sharedOrStatic}/install_tpl1/lib/libtpl1${libext}'"
        "Searching for headers in Tpl1_INCLUDE_DIRS='.*/TriBITS_TribitsExampleProject2_Tpls_install_${sharedOrStatic}/install_tpl1/include'"
        "Found header '.*/TriBITS_TribitsExampleProject2_Tpls_install_${sharedOrStatic}/install_tpl1/include/Tpl1.hpp'"
        "TPL_Tpl1_INCLUDE_DIRS='.*/TriBITS_TribitsExampleProject2_Tpls_install_${sharedOrStatic}/install_tpl1/include'"
	"Tpl3_LIBRARY_NAMES='tpl3[;]tpl2a[;]tpl2b'"
	"Searching for libs in Tpl3_LIBRARY_DIRS='.*/TriBITS_TribitsExampleProject2_Tpls_install_${sharedOrStatic}/install_tpl3/lib[;].*/TriBITS_TribitsExampleProject2_Tpls_install_${sharedOrStatic}/install_tpl2/lib'"
        "Found lib '.*/TriBITS_TribitsExampleProject2_Tpls_install_${sharedOrStatic}/install_tpl3/lib/libtpl3${libext}'"
	"Found lib '.*/TriBITS_TribitsExampleProject2_Tpls_install_${sharedOrStatic}/install_tpl2/lib/libtpl2a${libext}'"
	"Found lib '.*/TriBITS_TribitsExampleProject2_Tpls_install_${sharedOrStatic}/install_tpl2/lib/libtpl2b${libext}'"
	"TPL_Tpl3_LIBRARIES='.*/TriBITS_TribitsExampleProject2_Tpls_install_${sharedOrStatic}/install_tpl3/lib/libtpl3${libext}[;].*/TriBITS_TribitsExampleProject2_Tpls_install_${sharedOrStatic}/install_tpl2/lib/libtpl2a${libext}[;].*/TriBITS_TribitsExampleProject2_Tpls_install_${sharedOrStatic}/install_tpl2/lib/libtpl2b${libext}'"
	"Searching for headers in Tpl3_INCLUDE_DIRS='.*/TriBITS_TribitsExampleProject2_Tpls_install_${sharedOrStatic}/install_tpl3/include'"
	"Found header '.*/TriBITS_TribitsExampleProject2_Tpls_install_${sharedOrStatic}/install_tpl3/include/Tpl3.hpp'"
	"TPL_Tpl3_INCLUDE_DIRS='.*/TriBITS_TribitsExampleProject2_Tpls_install_${sharedOrStatic}/install_tpl3/include'"
        "-- Configuring done"
        "-- Generating done"

    TEST_1
      MESSAGE "Build Package1 and tests"
      CMND make
      ALWAYS_FAIL_ON_NONZERO_RETURN
      PASS_REGULAR_EXPRESSION_ALL
        "package1-prg"

    TEST_2
      MESSAGE "Run tests for Package1"
      CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
      ALWAYS_FAIL_ON_NONZERO_RETURN
      PASS_REGULAR_EXPRESSION_ALL
        "Test.*Package1_Prg.*Passed"
        "100% tests passed, 0 tests failed"

    TEST_3
      MESSAGE "Install Package1"
      CMND make ARGS install
      ALWAYS_FAIL_ON_NONZERO_RETURN
      PASS_REGULAR_EXPRESSION_ALL
        "Tpl1Config.cmake"

    ${ENV_PATH_HACK_FOR_TPL1_${sharedOrStatic}_ARG}

    ADDED_TEST_NAME_OUT ${testNameBase}_NAME
    )
  # NOTE: The above test ensures that the basic TriBITS TPL find operations
  # work and it does not call find_package().

  if (${testNameBase}_NAME)
    set(${testNameBase}_NAME ${${testNameBase}_NAME} PARENT_SCOPE)
    set(${testNameBase}_INSTALL_DIR "${testDir}/install" PARENT_SCOPE)
    set_tests_properties(${${testNameBase}_NAME}
      PROPERTIES DEPENDS ${TribitsExampleProject2_Tpls_install_${sharedOrStatic}_NAME} )
  endif()

endfunction()


TribitsExampleProject2_find_tpl_parts_test(STATIC)
TribitsExampleProject2_find_tpl_parts_test(SHARED)


########################################################################


function(TribitsExampleProject2_explicit_tpl_vars_test sharedOrStatic)

  TribitsExampleProject2_test_setup_header()

  set(testNameBase TribitsExampleProject2_explicit_tpl_vars_${sharedOrStatic})
  set(testName ${PACKAGE_NAME}_${testNameBase})
  set(testDir "${CMAKE_CURRENT_BINARY_DIR}/${testName}")

  tribits_add_advanced_test( ${testNameBase}
    OVERALL_WORKING_DIRECTORY TEST_NAME
    OVERALL_NUM_MPI_PROCS 1

    TEST_0
      MESSAGE "Configure TribitsExampleProject2 against pre-installed Tpl1"
      CMND ${CMAKE_COMMAND}
      ARGS
        #-C "${${testName}_CMAKE_PREFIX_PATH_file}"
        ${TribitsExampleProject2_COMMON_CONFIG_ARGS}
        -DCMAKE_BUILD_TYPE=DEBUG
        "-DTPL_Tpl1_INCLUDE_DIRS=${TribitsExampleProject2_Tpls_install_${sharedOrStatic}_DIR}/install_tpl1/include"
        "-DTPL_Tpl1_LIBRARIES=${TribitsExampleProject2_Tpls_install_${sharedOrStatic}_DIR}/install_tpl1/lib/libtpl1${libext}"
        -DTribitsExProj2_ENABLE_TESTS=ON
        -DCMAKE_INSTALL_PREFIX=install
        -DTribitsExProj2_ENABLE_Package1=ON
        ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject2
      ALWAYS_FAIL_ON_NONZERO_RETURN
      PASS_REGULAR_EXPRESSION_ALL
        "TPL_Tpl1_LIBRARIES='.*/TriBITS_TribitsExampleProject2_Tpls_install_${sharedOrStatic}/install_tpl1/lib/libtpl1${libext}'"
        "TPL_Tpl1_INCLUDE_DIRS='.*/TriBITS_TribitsExampleProject2_Tpls_install_${sharedOrStatic}/install_tpl1/include'"
        "-- Configuring done"
        "-- Generating done"

    TEST_1
      MESSAGE "Build Package1 and tests"
      CMND make
      ALWAYS_FAIL_ON_NONZERO_RETURN
      PASS_REGULAR_EXPRESSION_ALL
        "package1-prg"

    TEST_2
      MESSAGE "Run tests for Package1"
      CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
      ALWAYS_FAIL_ON_NONZERO_RETURN
      PASS_REGULAR_EXPRESSION_ALL
        "Test.*Package1_Prg.*Passed"
        "100% tests passed, 0 tests failed"

    TEST_3
      MESSAGE "Install Package1"
      CMND make ARGS install
      ALWAYS_FAIL_ON_NONZERO_RETURN
      PASS_REGULAR_EXPRESSION_ALL
        "Tpl1Config.cmake"

    ${ENV_PATH_HACK_FOR_TPL1_${sharedOrStatic}_ARG}

    ADDED_TEST_NAME_OUT ${testNameBase}_NAME
    )
  # NOTE: The above test ensures that setting TPL_<tplName>_INCLUDE_DIRS and
  # TPL_<tplName>_LIBRARIES bypasses calling the inner find_package().

  if (${testNameBase}_NAME)
    set(${testNameBase}_NAME ${${testNameBase}_NAME} PARENT_SCOPE)
    set(${testNameBase}_INSTALL_DIR "${testDir}/install" PARENT_SCOPE)
    set_tests_properties(${${testNameBase}_NAME}
      PROPERTIES DEPENDS ${TribitsExampleProject2_Tpls_install_${sharedOrStatic}_NAME} )
  endif()

endfunction()


TribitsExampleProject2_explicit_tpl_vars_test(STATIC)
TribitsExampleProject2_explicit_tpl_vars_test(SHARED)


########################################################################


function(TribitsExampleProject2_find_package_test sharedOrStatic)

  TribitsExampleProject2_test_setup_header()

  set(testNameBase TribitsExampleProject2_find_package_${sharedOrStatic})
  set(testName ${PACKAGE_NAME}_${testNameBase})
  set(testDir "${CMAKE_CURRENT_BINARY_DIR}/${testName}")

  tribits_add_advanced_test( ${testNameBase}
    OVERALL_WORKING_DIRECTORY TEST_NAME
    OVERALL_NUM_MPI_PROCS 1

    ENVIRONMENT
      "CMAKE_PREFIX_PATH=${TribitsExampleProject2_Tpls_install_${sharedOrStatic}_DIR}/install_tpl1"

    TEST_0
      MESSAGE "Configure TribitsExampleProject2 against pre-installed Tpl1"
      CMND ${CMAKE_COMMAND}
      ARGS
        ${TribitsExampleProject2_COMMON_CONFIG_ARGS}
        -DCMAKE_BUILD_TYPE=DEBUG
        -DTribitsExProj2_ENABLE_TESTS=ON
        -DCMAKE_INSTALL_PREFIX=install
        -DTribitsExProj2_ENABLE_Package1=ON
        ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject2
      ALWAYS_FAIL_ON_NONZERO_RETURN
      PASS_REGULAR_EXPRESSION_ALL
        "Using find_package[(]Tpl1 [.][.][.][)] [.][.][.]"
        "Found Tpl1_DIR='.*TribitsExampleProject2_Tpls_install_${sharedOrStatic}/install_tpl1/lib/cmake/Tpl1'"
        "TPL_Tpl1_LIBRARIES='Tpl1::all_libs'"
        "TPL_Tpl1_INCLUDE_DIRS=''"
        "-- Configuring done"
        "-- Generating done"

    TEST_1
      MESSAGE "Build Package1 and tests"
      CMND make
      ALWAYS_FAIL_ON_NONZERO_RETURN
      PASS_REGULAR_EXPRESSION_ALL
        "package1-prg"

    TEST_2
      MESSAGE "Run tests for Package1"
      CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
      ALWAYS_FAIL_ON_NONZERO_RETURN
      PASS_REGULAR_EXPRESSION_ALL
        "Test.*Package1_Prg.*Passed"
        "100% tests passed, 0 tests failed"

    TEST_3
      MESSAGE "Install Package1"
      CMND make ARGS install
      PASS_REGULAR_EXPRESSION_ALL
        "Tpl1Config.cmake"
        "Tpl1ConfigVersion.cmake"
      ALWAYS_FAIL_ON_NONZERO_RETURN

    ${ENV_PATH_HACK_FOR_TPL1_${sharedOrStatic}_ARG}

    ADDED_TEST_NAME_OUT ${testNameBase}_NAME
    )
  # NOTE: The above test ensures that find_package() works with manual
  # building of the target .

  if (${testNameBase}_NAME)
    set(${testNameBase}_NAME ${${testNameBase}_NAME} PARENT_SCOPE)
    set(${testNameBase}_INSTALL_DIR "${testDir}/install" PARENT_SCOPE)
    set_tests_properties(${${testNameBase}_NAME}
      PROPERTIES DEPENDS ${TribitsExampleProject2_Tpls_install_${sharedOrStatic}_NAME} )
  endif()

endfunction()


TribitsExampleProject2_find_package_test(STATIC)
TribitsExampleProject2_find_package_test(SHARED)


########################################################################


set(testNameBase TribitsExampleProject2_install_config_again)
set(testName ${PACKAGE_NAME}_${testNameBase})
set(testDir "${CMAKE_CURRENT_BINARY_DIR}/${testName}")

tribits_add_advanced_test( ${testNameBase}
  OVERALL_WORKING_DIRECTORY TEST_NAME
  OVERALL_NUM_MPI_PROCS 1

  ENVIRONMENT
    "CMAKE_PREFIX_PATH=${TribitsExampleProject2_Tpls_install_STATIC_DIR}/install_tpl1"

  TEST_0
    MESSAGE "Configure TribitsExampleProject2 against pre-installed Tpl1"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject2_COMMON_CONFIG_ARGS}
      -DCMAKE_BUILD_TYPE=DEBUG
      -DTpl1_EXTRACT_INFO_AFTER_FIND_PACKAGE=ON
      -DTribitsExProj2_ENABLE_TESTS=ON
      -DCMAKE_INSTALL_PREFIX=install
      -DTribitsExProj2_ENABLE_Package1=ON
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject2
    ALWAYS_FAIL_ON_NONZERO_RETURN
    PASS_REGULAR_EXPRESSION_ALL
      "Using find_package[(]Tpl1 [.][.][.][)] [.][.][.]"
      "Found Tpl1_DIR='.*TribitsExampleProject2_Tpls_install_STATIC/install_tpl1/lib/cmake/Tpl1'"
      "Extracting include dirs and libraries from target tpl1::tpl1"
      "-- Configuring done"
      "-- Generating done"

  TEST_1
    MESSAGE "Build Package1 and tests"
    CMND make
    ALWAYS_FAIL_ON_NONZERO_RETURN
    PASS_REGULAR_EXPRESSION_ALL
      "package1-prg"

  TEST_2
    MESSAGE "Run tests for Package1"
    CMND ${CMAKE_CTEST_COMMAND} ARGS -VV
    ALWAYS_FAIL_ON_NONZERO_RETURN
    PASS_REGULAR_EXPRESSION_ALL
      "Test.*Package1_Prg.*Passed"
      "100% tests passed, 0 tests failed"

  TEST_3
    MESSAGE "Install Package1"
    CMND make ARGS install
    ALWAYS_FAIL_ON_NONZERO_RETURN
    PASS_REGULAR_EXPRESSION_ALL
      "Tpl1Config.cmake"

  TEST_4
    MESSAGE "Remove configuration files for TribitsExampleProject2"
    CMND rm ARGS -r CMakeCache.txt CMakeFiles

  TEST_5
    MESSAGE "Configure  TribitsExampleProject2 against from scratch with install dir first in path"
    CMND ${CMAKE_COMMAND}
    ARGS
      ${TribitsExampleProject2_COMMON_CONFIG_ARGS}
      -DCMAKE_BUILD_TYPE=DEBUG
      -DTpl1_EXTRACT_INFO_AFTER_FIND_PACKAGE=ON
      -DTribitsExProj2_ENABLE_TESTS=ON
      -DCMAKE_PREFIX_PATH="${testDir}/install"
      -DCMAKE_INSTALL_PREFIX=install
      -DTribitsExProj2_ENABLE_Package1=ON
      ${${PROJECT_NAME}_TRIBITS_DIR}/examples/TribitsExampleProject2
    ALWAYS_FAIL_ON_NONZERO_RETURN
    PASS_REGULAR_EXPRESSION_ALL
      "Using find_package[(]Tpl1 [.][.][.][)] [.][.][.]"
      "Found Tpl1_DIR='.*TribitsExampleProject2_Tpls_install_STATIC/install_tpl1/lib/cmake/Tpl1'"
      "-- Configuring done"
      "-- Generating done"

  ADDED_TEST_NAME_OUT ${testNameBase}_NAME
  )
  # Above, we set the cache var CMAKE_PREFIX_PATH=install_tpl1 and the env var
  # CMAKE_PREFIX_PATH=install_tpl1 so that find_package(Tpl1) will look in
  # install_tpl1/ first for Tpl1Config.cmake before looking in install/.
  # (Note that we have to set the cache var CMAKE_PREFIX_PATH=install_tpl1 to
  # put install_tpl1/ in the search path ahead of install/ for this simulation
  # since CMAKE_INSTALL_PREFIX, which initializes CMAKE_SYSTEM_PREFIX_PATH, is
  # searched after the env var CMAKE_PREFIX_PATH.)
  #
  # This test simulates the situation in bug #427 where CMAKE_INSTALL_PREFIX
  # (which initializes CMAKE_SYSTEM_PREFIX_PATH) is searched before PATH and
  # HDF5Config.cmake was getting found in CMAKE_INSTALL_PREFIX from a prior
  # install of Trilinos.  But since I don't want to mess with PATH for this
  # test, I just want to have find_package() search install_tpl1/ before in
  # searches install/ to simulate that scenario.  This test ensures that
  # find_package(Tpl1) will not find Tpl1Config.cmake just because
  # CMAKE_INSTALL_PREFIX is in the search path.
  #
  # NOTE: Updated versions of TriBITS will not find TriBITS-generated files
  # like Tpl1Config.cmake because they are placed under a different subdir
  # <installDir>/external_pacakges/.

if (${testNameBase}_NAME)
  set_tests_properties(${${testNameBase}_NAME}
    PROPERTIES DEPENDS ${TribitsExampleProject2_Tpls_install_STATIC_NAME} )
endif()