set(HEADERS "")
set(SOURCES "")

include_directories(${CMAKE_CURRENT_SOURCE_DIR})

append_set(HEADERS
  Package1_HelloWorld.hpp
  )
append_set(SOURCES
  Package1_HelloWorld.cpp
  )

tribits_add_library(
  package1
  HEADERS ${HEADERS}
  SOURCES ${SOURCES}
  )

tribits_add_executable(package1-helloworld  NOEXEPREFIX  NOEXESUFFIX
  SOURCES  Package1_HelloWorld_Prog.cpp
  INSTALLABLE
  )
