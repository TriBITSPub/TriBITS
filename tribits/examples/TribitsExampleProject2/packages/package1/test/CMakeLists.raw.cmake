add_test(NAME Package1_Prg COMMAND package1-prg)
set_tests_properties(Package1_Prg
  PROPERTIES PASS_REGULAR_EXPRESSION "Package1 Deps: tpl1")

add_test(NAME Package1_Prg-advanced COMMAND package1-prg something_extra)
set_tests_properties(Package1_Prg-advanced
  PROPERTIES PASS_REGULAR_EXPRESSION "something_extra")

# NOTE: With raw CMake/CTest, it is not possible to require the matches of
# multiple regexes.  Also, it is not possible to require a non-zero return
# code in addition to requiring a regex match the output.  These more advanced
# features of tribits_add_advanced_test() would need to be provided by writing
# a wrapper script (e.g. using a Python script, a cmake -P script, etc.)
