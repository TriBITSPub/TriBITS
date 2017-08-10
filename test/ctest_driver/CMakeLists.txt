ADD_SUBDIRECTORY(MockCTestDriver)

IF (
  (CMAKE_HOST_SYSTEM_NAME STREQUAL "Linux")
  AND
  (NOT CMAKE_VERSION VERSION_LESS "3.3.0")
  )
  ADD_SUBDIRECTORY(TribitsExampleProject)
  # NOTE: For some reason, these tests do not work correctly when run with
  # CMake 2.8.11.  I tested them locally with CMake 3.3.2 and they worked
  # locally at least.
ENDIF()
