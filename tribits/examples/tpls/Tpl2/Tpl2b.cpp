#include "Tpl1.hpp"
#include "Tpl2a.hpp"

std::string Tpl2::a_itsme()
{
  return "tpl2a";
}

std::string Tpl2::a_deps()
{
  return Tpl1::itsme();
}
