cmake_minimum_required(VERSION 3.17.1)

project(TribitsExApp
  DESCRIPTION
    "Example raw CMake project using packages installed from TribitsExampleProject"
  VERSION 0.0.0
  LANGUAGES NONE  # Defined below after reading in compilers
  )

set(${PROJECT_NAME}_USE_COMPONENTS "" CACHE STRING
  "Components to use from TribitsExampleProject: <C0>,<C1>,..." )
string(REPLACE "," ";" ${PROJECT_NAME}_USE_COMPONENTS
  "${${PROJECT_NAME}_USE_COMPONENTS}")

find_package(TribitsExProj REQUIRED COMPONENTS ${${PROJECT_NAME}_USE_COMPONENTS})

MESSAGE("\nFound TribitsExProj!  Here are the details: ")
MESSAGE("   TribitsExProj_DIR = ${TribitsExProj_DIR}")
MESSAGE("   TribitsExProj_VERSION = ${TribitsExProj_VERSION}")
MESSAGE("   TribitsExProj_PACKAGE_LIST = ${TribitsExProj_PACKAGE_LIST}")
MESSAGE("   TribitsExProj_LIBRARIES = ${TribitsExProj_LIBRARIES}")
MESSAGE("   TribitsExProj_INCLUDE_DIRS = ${TribitsExProj_INCLUDE_DIRS}")
MESSAGE("   TribitsExProj_LIBRARY_DIRS = ${TribitsExProj_LIBRARY_DIRS}")
MESSAGE("   TribitsExProj_TPL_LIST = ${TribitsExProj_TPL_LIST}")
MESSAGE("   TribitsExProj_TPL_INCLUDE_DIRS = ${TribitsExProj_TPL_INCLUDE_DIRS}")
MESSAGE("   TribitsExProj_TPL_LIBRARIES = ${TribitsExProj_TPL_LIBRARIES}")
MESSAGE("   TribitsExProj_TPL_LIBRARY_DIRS = ${TribitsExProj_TPL_LIBRARY_DIRS}")
MESSAGE("   TribitsExProj_BUILD_SHARED_LIBS = ${TribitsExProj_BUILD_SHARED_LIBS}")
MESSAGE("End of TribitsExProj details\n")

# Make sure to use same compilers and flags as TribitsExProj
set(CMAKE_CXX_COMPILER ${TribitsExProj_CXX_COMPILER} )
set(CMAKE_C_COMPILER ${TribitsExProj_C_COMPILER} )
set(CMAKE_Fortran_COMPILER ${TribitsExProj_Fortran_COMPILER} )

set(CMAKE_CXX_FLAGS  "${TribitsExProj_CXX_COMPILER_FLAGS} ${CMAKE_CXX_FLAGS}")
set(CMAKE_C_FLAGS  "${TribitsExProj_C_COMPILER_FLAGS} ${CMAKE_C_FLAGS}")
set(CMAKE_Fortran_FLAGS  "${TribitsExProj_Fortran_COMPILER_FLAGS} ${CMAKE_Fortran_FLAGS}")

# Now enable the compilers now that we have gotten them from TribitsExProj
enable_language(C)
enable_language(CXX)
if (CMAKE_Fortran_COMPILER)
  enable_language(Fortran)
endif()

# Load modules
list(PREPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}")
include(AppHelperFuncs)

# Build the APP and link to TribitsExProj
add_executable(app ${CMAKE_CURRENT_SOURCE_DIR}/app.cpp)
target_include_directories(app PRIVATE
  ${CMAKE_CURRENT_SOURCE_DIR} ${TribitsExProj_INCLUDE_DIRS} ${TribitsExProj_TPL_INCLUDE_DIRS})
target_link_libraries(app PRIVATE
  ${TribitsExProj_LIBRARIES} ${TribitsExProj_TPL_LIBRARIES})

# Tell app.cpp what components are supported
addDepCompileDefine("SimpleCxx")
addDepCompileDefine("MixedLang")
addDepCompileDefine("WithSubpackages")

# Set up a test
enable_testing()

#set(NUM_MPI_PROCS ${TribitsExProj_MPI_EXEC_MAX_NUMPROCS})
#add_test(app_test
#  ${TribitsExProj_MPI_EXEC} ${TribitsExProj_MPI_EXEC_NUMPROCS_FLAG} ${NUM_MPI_PROCS}
#  app)
#set_tests_properties(app_test PROPERTIES
#  PROCESSORS ${NUM_MPI_PROCS}
#  PASS_REGULAR_EXPRESSION "DUMMY NO MATCH"
#  )

set(depsStr "")
appendDepsStr("WithSubpackages" depsStr "WithSubpackages:B A no_deps no_deps")
appendDepsStr("MixedLang" depsStr "MixedLang:Mixed Language")
appendDepsStr("SimpleCxx" depsStr "SimpleCxx:no_deps")

add_test(app_test app)
set_tests_properties(app_test PROPERTIES
  PASS_REGULAR_EXPRESSION "Full Deps: ${depsStr}"
  )
