#include "Tpl1.hpp"
#include "Tpl2b.hpp"

std::string Tpl2::b_itsme()
{
  return "tpl2b";
}

std::string Tpl2::b_deps()
{
  return Tpl1::itsme();
}
