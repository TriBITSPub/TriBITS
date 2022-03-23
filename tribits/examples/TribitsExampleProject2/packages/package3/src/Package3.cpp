#include "Package3.hpp"

#include <sstream>

#include "Package1.hpp"
#include "Package2.hpp"

#include "Tpl2a.hpp"
#include "Tpl2b.hpp"
#include "Tpl4.hpp"

std::string  Package3::itsme()
{
  return "Package3";
}

std::string Package3::deps()
{
  std::ostringstream oss_deps;
  oss_deps
    << Package2::itsme() << "{" << Package2::deps() << "}"
    << ", "
    << Package1::itsme() << "{" << Package1::deps() << "}"
    << ", "
    << Tpl4::itsme() << "{" << Tpl4::deps() << "}"
    << ", "
    << Tpl2::a_itsme() << "{" << Tpl2::a_deps() << "}"
    << ", "
    << Tpl2::b_itsme() << "{" << Tpl2::b_deps() << "}"
    ;
  return oss_deps.str();
}
