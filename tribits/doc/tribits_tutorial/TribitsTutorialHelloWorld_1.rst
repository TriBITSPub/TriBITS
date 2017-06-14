=======================================
TriBITS Example Project Tutorial
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

Section Tiile
===================================
The previous tutorial had you create all the files nesseasary for a very simple tribits
project.  This time we will look at an example of a more complicated example project that 
is included when you clone the tribits repository. If you got to::
  
  TriBITS/tribits/examples/

you will several examples including one very similar to what we constructed in the last tutorial.
In this tutorail we will be using the TribitsExampleProject.  This project has multiple packages
as well as TPL dependencies so we will be able to see how tribits deals with both types of 
dependencies. In TribitsExampleProject, looka at::

  PackagesList.cmake
  TPLsList.cmake

and you will see that we have a several packages defined in this project and a couple TPLs

Tribits Packages
-------------------------
