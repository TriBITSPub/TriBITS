#include "Package2.hpp"

#include <sstream>

#include "Tpl3.hpp"
#include "Package1.hpp"

std::string  Package2::itsme()
{
  return "Package2";
}

std::string Package2::deps()
{
  std::ostringstream oss_deps;
  oss_deps
    << Package1::itsme() << "{" << Package1::deps() << "}"
    << ", " << Tpl3::itsme() << "{" << Tpl3::deps() << "}";
  return oss_deps.str();
}
