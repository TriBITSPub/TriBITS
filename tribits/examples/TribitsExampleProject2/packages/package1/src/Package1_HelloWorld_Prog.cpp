#include <iostream>

#include "Package1_HelloWorld.hpp"

int main()
{
  std::cout << "Package1 Deps: " << Package1::deps() << "\n";
  return 0;
}
