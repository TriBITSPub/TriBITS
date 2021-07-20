function(set_test_disables)
  foreach (testName ${ARGN})
    set(testNameDisableVar ${testName}_DISABLE)
    message("-- Setting ${testNameDisableVar}=ON")
    set(${testNameDisableVar} ON CACHE BOOL "Set in ${CMAKE_CURRENT_LIST_FILE}")
  endforeach()
endfunction()

set_test_disables(
#  TriBITS_CTestDriver_PBP_PT_ALL_PASS_CALLS_2
#  TriBITS_CTestDriver_PBP_PT_ALL_PASS_CALLS_4
#  TriBITS_CTestDriver_PBP_ST_ALL_COVERAGE
#  TriBITS_CTestDriver_PBP_ST_ALL_MEMORY
#  TriBITS_CTestDriver_PBP_ST_ALL_PASS
#  TriBITS_CTestDriver_PBP_ST_BreakBuildAllOptionalPkg
#  TriBITS_CTestDriver_PBP_ST_BreakBuildLibOptionalPkg
#  TriBITS_CTestDriver_PBP_ST_BreakConfigureOptionalPkg
#  TriBITS_CTestDriver_PBP_ST_BreakConfigureRequiredPkg
#  TriBITS_CTestDriver_PBP_ST_BreakTestPkg
  )
