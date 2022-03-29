set(HEADERS "")
set(SOURCES "")

include_directories(${CMAKE_CURRENT_SOURCE_DIR})

append_set(HEADERS
  Package3.hpp
  )
append_set(SOURCES
  Package3.cpp
  )

tribits_add_library(
  package3
  HEADERS ${HEADERS}
  SOURCES ${SOURCES}
  )

tribits_add_executable(package3-prg  NOEXEPREFIX  NOEXESUFFIX
  SOURCES  Package3_Prg.cpp
  INSTALLABLE
  )
