=====================================
Tribits beyond HelloWorld
=====================================

:Author: Joe Frye (jfrye@sandia.gov)
:Date: |date|

.. |date| date::

.. sectnum::
   :depth: 2

.. Sections in this document use the underlines:
..
.. Level-1 ==================
.. Level-2 ------------------
.. Level-3 ++++++++++++++++++
.. Level-4 ..................

.. contents::


TriBITS Example Project
========================

The previous tutorial had you create all the files nesseasary for a
very simple tribits project.  This time we will look at an example of
a more complicated example project that is included when you clone the
tribits repository. If you got to::

  TriBITS/tribits/examples/

you will see several examples including one very similar to what we
constructed in the last tutorial.  In this tutorial we will be using
the TribitsExampleProject.  This project has multiple packages as well
as TPL dependencies so we will be able to see how tribits deals with
both types of dependencies. In TribitsExampleProject, looka at::

  PackagesList.cmake
  TPLsList.cmake

and you will see that we have a several packages defined for the
project in PackageList.cmake and a couple TPLs defined in
TPLsList.cmake.  Recall that the package definitions looks like the
following::

  TRIBITS_REPOSITORY_DEFINE_PACKAGES(
    NameOfPackageA     location/of/packageA        <options>
    NameOfPackageB     path/to/packageB            <options>
  )

you must specify the name of the package and where it is located.
Each package must contain a CmakeLists.cmake file and a
Dependencies.cmake file.  The CmakeLists file defines targets for this
package and must begin with a call to TRIBITS\_PACKAGE() and end with
a call to TRIBITS\_PACKAGE\_POSTPROCESS().  Tribits TPLs are defined
similarly in TPLsList.cmake::

  TRIBITS\_REPOSITORY\_DEFINE\_TPLS(
    NameOfTPL-1     location/of/TPL-1        <options>
    NameOfTPL-2     path/to/TPL-2            <options>
  )

more detail on packages and tpls will follow below.  

Tribits Packages
-----------------

TriBITS TPLs
-------------
