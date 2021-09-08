cmake_minimum_required(VERSION 3.17.1)

project(TribitsExApp
  DESCRIPTION
    "Example raw CMake project using packages installed from TribitsExampleProject"
  VERSION 0.0.0
  LANGUAGES NONE  # Defined below after reading in compilers
  )

list(PREPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}")
include(AppHelperFuncs)

set(${PROJECT_NAME}_USE_COMPONENTS "" CACHE STRING
  "Components/Packages to use from TribitsExampleProject: <C0>,<C1>,..." )
string(REPLACE "," ";" ${PROJECT_NAME}_USE_COMPONENTS
  "${${PROJECT_NAME}_USE_COMPONENTS}")

getTribitsExProjStuff()

# Now enable the compilers now that we have gotten them from TribitsExProj
enable_language(C)
enable_language(CXX)
if (CMAKE_Fortran_COMPILER)
  enable_language(Fortran)
endif()

# Build the APP and link to TribitsExProj
add_executable(app ${CMAKE_CURRENT_SOURCE_DIR}/app.cpp)
target_include_directories(app PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}
  ${APP_DEPS_INCLUDE_DIRS})
target_link_libraries(app PRIVATE ${APP_DEPS_LIBRARIES})
addAppDepCompileDefines()

# Set up tests

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
appendTestDepsStr("WithSubpackages" depsStr "WithSubpackages:B A no_deps no_deps")
appendTestDepsStr("MixedLang" depsStr "MixedLang:Mixed Language")
appendTestDepsStr("SimpleCxx" depsStr "SimpleCxx:no_deps")

add_test(app_test app)
set_tests_properties(app_test PROPERTIES
  PASS_REGULAR_EXPRESSION "Full Deps: ${depsStr}"
  )
