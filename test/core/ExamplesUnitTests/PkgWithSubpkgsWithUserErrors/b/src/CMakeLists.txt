tribits_include_directories(${CMAKE_CURRENT_BINARY_DIR})

tribits_include_directories(${CMAKE_CURRENT_SOURCE_DIR})
tribits_add_library(pwswue_b
  SOURCES B.cpp
  HEADERS B.hpp
  )
