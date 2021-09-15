#ifdef TRIBITSEXAPP_HAVE_SIMPLECXX
#  include "SimpleCxx_HelloWorld.hpp"
#endif
#ifdef TRIBITSEXAPP_HAVE_MIXEDLANG
#  include "MixedLang.hpp"
#endif
#ifdef TRIBITSEXAPP_HAVE_WITHSUBPACKAGES
#  include "wsp_c/C.hpp"
#endif


#include <iostream>
#include <string>

//#include <mpi.h>


void appendDepsStr(std::string &depsStr, const std::string &str)
{
  if (depsStr.length()) {
    depsStr += "; "+str;
  }
  else {
    depsStr = str;
  }
}


int main(int argc, char *argv[]) {
  //MPI_Init(&argc, &argv);
  //MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  // Make sure MPI works
  //int oneVal = 1;
  //int numProcs = 0;
  //MPI_Reduce(&onVal, &numProcs, MPI_SUM, 0, MPI_COMM_WORLD);
  const int rank = 0; 

  // Get deps down the deps graph
  std::string depsStr;
#ifdef TRIBITSEXAPP_HAVE_WITHSUBPACKAGES
  appendDepsStr(depsStr, "WithSubpackages:"+WithSubpackages::depsC());
#endif
#ifdef TRIBITSEXAPP_HAVE_MIXEDLANG
  appendDepsStr(depsStr, "MixedLang:"+tribits_mixed::mixedLang());
#endif
#ifdef TRIBITSEXAPP_HAVE_SIMPLECXX
  appendDepsStr(depsStr, "SimpleCxx:"+SimpleCxx::deps());
#endif
  // NOTE: The above all call functions from the libraries and requires that
  // both the header files be found at compile time and the libraries be found
  // at link time and runtime for this these function calls to work.

  if (rank == 0) {
    std::cout << "Full Deps: " << depsStr << "\n";
  }

  return 0;
}
