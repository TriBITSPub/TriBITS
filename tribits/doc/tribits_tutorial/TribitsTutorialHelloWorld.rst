=======================================
TriBITS Hello World Tutorial
=======================================

:Author: Roscoe A. Bartlett (bartlettra@ornl.gov), Joe Frye (jfrye@sandia.gov)
:Date: |date|
:Version: .. include:: TribitsGitVersion.txt

.. |date| date::


.. sectnum::
   :depth: 2

.. Above, the depth of the TOC is set to just 2 because I don't want the
.. TriBITS function/macro names to have section numbers appearing before them.
.. Also, some of them are long and I don't want them to go off the page of the
.. PDF document.

.. Sections in this document use the underlines:
..
.. Level-1 ==================
.. Level-2 ------------------
.. Level-3 ++++++++++++++++++
.. Level-4 ..................

.. contents::

The Simplest HelloWorld project
===================================
This short tutorial will walk you through setting up a basic HelloWorld project
built by TriBITS to intdroduce the basic concepts in TriBits.  To begin you
will need cmake and TriBITS installed on your machine.  You will also need a 
working c and c++ compiler.  

TriBITS projects have a specific structure ie a project is a collection of 
packages.  For this example we will be creating a project that has just one 
package, the "HelloPackage" package.

Initial Setup
----------------
First lets create all the directories for our project.  We will need a top level 
directory for the project  which I will call tribits_hello_world. We need a 
directory for the "HelloPackage" package.  We will also need a directory for the 
build which I call "build".  Under the hello_package_dir also create the directories 
"camke" and "src"::

  tribits_hello_world/
  tribits_hello_wolrd/build
  tribits_hello_world/hello_package_dir
  tribits_hello_world/hello_package_dir/cmake
  tribits_hello_world/hello_package_dir/src

  $ tree
  .
  └── tribits_hello_world
      ├── build
      └── hello_package_dir
          ├── cmake
          └── src

Create a TriBITS package
-------------------------
The most basic TriBITS package needs to have 3 files.
* a top level CMakeLists file
* a source file
* a file that track package dependencies

First lets create the source file which is the classic HelloWorld.cpp.  Just 
copy this to HelloWorld.cpp in the src directory::

  #include <iostream>

  int main()
  {
    std::cout << "Hello World!\n";
    return 0;

  }

Second lets create the package dependencies file which should be placed in the 
cmake directory.  Copy the below text into a file called Dependencies.cmake::

  TRIBITS_PACKAGE_DEFINE_DEPENDENCIES()

In this case the package we are creating has no dependencies but we still need 
this file.  The lack of arguments to the TRIBITS_PACKAGE_DEFINE_DEPENDENCIES() call
reflects that this package does not have dependencies.  The last and most interesting 
file we will create in the package directory is the CMakeLists.txt file.  Copy the following
into CMakeLists.txt::

  TRIBITS_PACKAGE(HelloPackage)
  TRIBITS_ADD_EXECUTABLE(Hello-Executable-Name NOEXEPREFIX SOURCES src/HelloWorld.cpp INSTALLABLE)
  TRIBITS_PACKAGE_POSTPROCESS()


**TRIBITS_PACKAGE(HelloPackage)** Sets this up a TriBITS package with the name "HelloPackage"

**TRIBITS_ADD_EXECUTABLE(Hello-Executable-Name NOEXEPREFIX SOURCES src/HelloWorld.cpp INSTALLABLE)** tells 
TriBITS that we want to build an executable named "Hello-Executable-Name" from the source file src/HelloWorld.cpp.
NOEXEPREFIX and INSTALLABLE are options to TRIBITS_ADD_EXECUTABLE() that I will not go into right now.

**TRIBITS_PACKAGE_POSTPROCESS()**  Must be at the end of any packages top level CMakeLists file

**Say some stuff about Tribits packages (here) or at teh top of this section**

Create a Tribits Project
-------------------------
Recall that a TriBITS project is made up of TriBITS packages.  We have just defeined a package now we will create 
a project that consists of just that one package.  In order to do this we are going to create 4 files in the top 
level directory and they are named:
* CMakeLists.txt
* PackageList.cmake
* ProjectName.camke
* TPLsList.cmake

**TPLsList.camke** this file tells Tribits ablout TPLs needed for the project.  In this case, the package does not
depend on any TPLs so this file will be very simple.  It should contain just the following single line::

  TRIBITS_REPOSITORY_DEFINE_TPLS()

**ProjectName.camke** this file sets the name of the project.  Some other options can be specified in this file but we
will just set the project name. It should contain the following::
  
  SET(PROJECT_NAME TribitsHelloWorld)

**PackageList.cmake** defeines which packages are in the project.  We will just need to tell it the name and location
of our one package::

  TRIBITS_REPOSITORY_DEFINE_PACKAGES(
    HelloPackage  hello_package_dir  PT
  )

**CMakeLists.txt** This is the most interesting file in this example.  Here we will set a minimum cmake version, load some 
options, and tell cmake that this is a Tribits project.  The CMakeLists.txt file should have the following contents::

  # To be safe, define your minimum CMake version
  CMAKE_MINIMUM_REQUIRED(VERSION 2.8.11 FATAL_ERROR)
  
  # Make CMake set WIN32 with CYGWIN for older CMake versions
  SET(CMAKE_LEGACY_CYGWIN_WIN32 1 CACHE BOOL "" FORCE)
  
  # Get PROJECT_NAME (must be in file for other parts of system)
  INCLUDE(${CMAKE_CURRENT_SOURCE_DIR}/ProjectName.cmake)
  
  # CMake requires that you declare the CMake project in the top-level file
  PROJECT(${PROJECT_NAME} NONE)

  # This needs to be set to the path to the installation of TriBITS on your machine  
  SET(${PROJECT_NAME}_TRIBITS_DIR ${CMAKE_CURRENT_SOURCE_DIR}/cmake/tribits
    CACHE PATH "TriBITS base directory (default assumes in TriBITS source tree).")

  # Include the TriBITS system
  INCLUDE("${${PROJECT_NAME}_TRIBITS_DIR}/TriBITS.cmake")
  
  # MPI and Fortran are enabled by defualt, turn them off for this project
  SET(TPL_ENABLE_MPI OFF CACHE BOOL "" FORCE)
  # Turn off Fortran support by default
  SET(${PROJECT_NAME}_ENABLE_Fortran_DEFAULT OFF)
  
  # Only one package in this simple project so just enable it :-)
  SET(${PROJECT_NAME}_ENABLE_HelloPackage ON CACHE BOOL "" FORCE)
  
  # Do all of the processing for this Tribits project
  TRIBITS_PROJECT()

**SET(${PROJECT_NAME}_TRIBITS_DIR ${CMAKE_CURRENT_SOURCE_DIR}/cmake/tribits 
    CACHE PATH "TriBITS base directory (default assumes in TriBITS source tree).")** 
Make sure you set this to your Tribits Installation path it may not be the same as
this path.  Now you should have a directory structure that looks like this::

  .
  ├── CMakeLists.txt
  ├── PackagesList.cmake
  ├── ProjectName.cmake
  ├── TPLsList.cmake
  ├── build
  └── hello_package_dir
      ├── CMakeLists.txt
      ├── cmake
      │   └── Dependencies.cmake
      └── src
          └── HelloWorld.cpp


Build your TriBITS project
---------------------------
Go to the build directory and type::
  cmake ../

You should see something very similar to::

..literalinclude:: HelloWorldConfigure.output

Now type::
  make

