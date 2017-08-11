TRIBITS_ADD_EXECUTABLE_AND_TEST( PkgWithUserErrorsTest
  SOURCES  PkgWithUserErrorsTest.cpp
  NUM_MPI_PROCS 1
  PASS_REGULAR_EXPRESSION
    "PkgWithUserErrorsLib returns PkgWithUserErrorsThing"
  )
