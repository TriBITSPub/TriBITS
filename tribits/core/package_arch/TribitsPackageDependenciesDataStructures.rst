TriBITS Package Dependencies Data Structures
--------------------------------------------

This section describes the global CMake variables that make up the
data-structures that define the TriBITS package system.  This defines a graph
of package and TPL dependencies.  This information is meant for maintainers of
the TriBITS system itself and should not need to be know by TriBITS Project
maintainers.


List of all defined internal (TriBITS) and external (TPL) packages
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

The full list of defined external packages (TPLs) and top-level internal
packages (TriBITS packages) is storied in the project-level non-cache list
variable::

  ${PROJECT_NAME}_ALL_PACKAGES

The first set of elements in this list are the defined external packages
(TPLs) that are read in from the `<repoDir>/TPLsList.cmake`_ files from each
processed TriBITS repository, in order.  This is followed by the set of
internal packages (TriBITS packages) that are defined in the
`<repoDir>/PackagesList.cmake`_ files from each processed TriBITS repository,
read in order.

An internal TriBITS Package (i.e. a package that can be built from source)
will have a non-empty `${PACKAGE_NAME}_SOURCE_DIR`_ varaible set while an
external package (i.e. TPL that is prebuilt and installed in some way) in this
list will have a non-empty `${PACKAGE_NAME}_FINDMOD`_ varaible set.  However,
the final decision if a package is treated as an internal or external package
is determiend by the variable::

  ${PACKAGE_NAME}_PACKAGE_STATUS=[INTERNAL|EXTERNAL]

For example, a package that has a non-empty ``${PACKAGE_NAME}_SOURCE_DIR``
variable can in facth have ``${PACKAGE_NAME}_PACKAGE_STATUS=EXTERNAL`` in a
number of different use cases.  (One example is if the user configured with
``TPL_ENABLE_${PACKAGE_NAME}=ON`` telling the TriBITS project to not build the
package ``${PACKAGE_NAME}`` from source but instead to look for it out on the
system.)






ToDo: Deal with old data-structures below after the refactoring for #63 is
complete.

The full list of defined top-level parent packages is stored in the
project-level non-cache list variable::

  ${PROJECT_NAME}_PACKAGES

This list does **not** include any subpackages.  This gets created from the
`<repoDir>/PackagesList.cmake`_ file from each processed TriBITS repository.

The full list of all of the defined packages and subpackages is stored in the
project-level non-cache list variable::

  ${PROJECT_NAME}_SE_PACKAGES

That list is created from the information in the
`<repoDir>/PackagesList.cmake`_ and `<packageDir>/cmake/Dependencies.cmake`_
files for the top-level packages read and processed in the macro
`TRIBITS_READ_ALL_PACKAGE_DEPENDENCIES()`_ using macros in the file::

  TribitsAdjustPackageEnables.cmake

One can determine if a package in this list is a top-level parent package or a
sub-subpackage based on the value of the varaible
`${PACKAGE_NAME}_PARENT_PACKAGE`_.  If the value is non empty, then
``${PACKAGE_NAME}`` is a subpackage.  If the value is empty "", then
``${PACKAGE_NAME}`` is a parent package.

This full number of defined top-level parent packages (i.e. the number of
items in the array ``${PROJECT_NAME}_PACKAGES``) is given in the variable::

  ${PROJECT_NAME}_NUM_PACKAGES

and the 0-based index of the last package in the array
``${PROJECT_NAME}_PACKAGES`` (i.e. ``${PROJECT_NAME}_NUM_PACKAGES - 1``) is
given in::

  ${PROJECT_NAME}_LAST_PACKAGE_IDX

This data gets set in functions in the file::

  TribitsProcessPackagesAndDirsLists.cmake

The full list of defined TPLs is stored in the variable::

  ${PROJECT_NAME}_TPLS

This list is created from the `<repoDir>/TPLsList.cmake`_ files from each
defined TriBITS Repository.  Along with this, the following variables for each
of these TriBITS TPLs are defined::

* `${TPL_NAME}_FINDMOD`_
* `${TPL_NAME}_TESTGROUP`_

This data gets set in functions in the file::

  TribitsProcessTplsLists.cmake  

NOTE: The same external package (TPL) can be duplicated in multiple
``TPLsList.cmake`` files.  This has the affect of allowing overrides of the
``FindTPL<TPLName>.cmake`` module.  See the discussion in `TriBITS TPL`_ for
more details.


Top-level user cache variables
++++++++++++++++++++++++++++++

The following variables are set by the user to determine what packages get
enabled or disabled::
  
  ${PROJECT_NAME}_ENABLE_ALL_PACKAGES
  
  ${PROJECT_NAME}_ENABLE_ALL_FORWARD_DEP_PACKAGES
  
  ${PROJECT_NAME}_ENABLE_ALL_OPTIONAL_PACKAGES

  ${PROJECT_NAME}_ENABLE_${PACKAGE_NAME}
  
  ${PROJECT_NAME}_ENABLE_TESTS
  
  ${PROJECT_NAME}_ENABLE_EXAMPLES
  
  ${PACKAGE_NAME}_ENABLE_${OPTIONAL_DEP_PACKAGE_NAME}
  
  ${PACKAGE_NAME}_ENABLE_TESTS
  
  ${PACKAGE_NAME}_ENABLE_EXAMPLES

These variables are defined in the file::

   TribitsGlobalMacros.cmake

This dependency logic is executed in the TriBITS file::

    TribitsAdjustPackageEnables.cmake

There are pretty good unit and regression tests to demonstrate and protect
this functionality in the directory::

  tribits/package_arch/UntiTests/


Top-level internal non-cache variables defining direct package dependencies
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

The following top-level non-cache variables are defined after reading in each
SE package's Dependencies.cmake file and they are used to define the basic
dependencies that exist between ${PROJECT_NAME} SE packages to support the SE
package enable and disable logic described above.  These variables taken
together constitute a bidirectionally navigate-able tree data-structure for SE
package and TPL dependencies::

  ${PACKAGE_NAME}_LIB_REQUIRED_DEP_PACKAGES
  
    The list of *direct* SE package dependencies that are required for the
    libraries built by ${PACKAGE_NAME}.  These should not include indirect
    dependencies but it is harmless to list these also.
  
  ${PACKAGE_NAME}_LIB_OPTIONAL_DEP_PACKAGES
  
    The list of *direct* SE package dependencies that are only optional for
    the libraries built by ${PACKAGE_NAME}.  These should not include indirect
    dependencies but it is harmless to list these also.
  
  ${PACKAGE_NAME}_TEST_REQUIRED_DEP_PACKAGES
  
    The list of *direct* SE package dependencies that are required for the
    tests/examples built by ${PACKAGE_NAME}.  This list should not contain any
    of the packages listed in ${PACKAGE_NAME}_LIB_REQUIRED_DEP_PACKAGES.
    These should not include indirect dependencies but it is harmless to list
    these also.
  
  ${PACKAGE_NAME}_TEST_OPTIONAL_DEP_PACKAGES
  
    The list of *direct* SE package dependencies that are optional for the
    tests/examples built by ${PACKAGE_NAME}.  This list should not contain any
    of the SE packages listed in ${PACKAGE_NAME}_LIB_REQUIRED_DEP_PACKAGES,
    ${PACKAGE_NAME}_LIB_OPTIONAL_DEP_PACKAGES, or
    ${PACKAGE_NAME}_TEST_REQUIRED_DEP_PACKAGES.  These should not include
    indirect dependencies but it is harmless to list these also.

Given the above variables, the following derived variables are then set which
provide navigation from a package to its downstream/forward dependent
packages::

  ${PACKAGE_NAME}_FORWARD_LIB_REQUIRED_DEP_PACKAGES
  
    For a given SE package ${PACKAGE_NAME}, gives the names of all of the
    forward SE packages that list this SE package in their
    ${FORWARD_PACKAGE_NAME}_LIB_REQUIRED_DEP_PACKAGES variables.
  
  ${PACKAGE_NAME}_FORWARD_LIB_OPTIONAL_DEP_PACKAGES
  
    For a given SE package ${PACKAGE_NAME}, gives the names of all of the
    forward SE packages that list this SE package in their
    ${FORWARD_PACKAGE_NAME}_LIB_OPTIONAL_DEP_PACKAGES variables.
  
  ${PACKAGE_NAME}_FORWARD_TEST_REQUIRED_DEP_PACKAGES
  
    For a given SE package ${PACKAGE_NAME}, gives the names of all of the
    forward SE packages that list this SE package in their
    ${FORWARD_PACKAGE_NAME}_TEST_REQUIRED_DEP_PACKAGES variables.
  
  ${PACKAGE_NAME}_FORWARD_TEST_OPTIONAL_DEP_PACKAGES
  
    For a given SE package ${PACKAGE_NAME}, gives the names of all of the
    forward SE packages that list this SE package in their
    ${FORWARD_PACKAGE_NAME}_TEST_OPTIONAL_DEP_PACKAGES variables.

Some subset of these packages will turn out to be external packages
(e.g. TPLs).  If a package can be built internally, it will have::

  ${PACKAGE_NAME}_SOURCE_DIR != ""

set which means that it could be built internally.  However, even packages
that could be built internally may be chosen to be treated as TPLs by
setting::

  -D TPL_ENABLE_<ExternalPackage>=ON

Therefore, the final status if a listed dependency is an internal packages or
an external package is provided by the variable::

  ${PACKAGE_NAME}_PACKAGE_STATUS=[INTERNAL|EXTERNAL]

Even other package upstream from an <ExternalPackage> must therefore be
treated as an external package automatically.

The primary TriBITS file that processes and defines these variables is:

  TribitsAdjustPackageEnables.cmake

There are pretty good unit and regression tests to demonstrate and protect
this functionality in the directory:

  tribits/package_arch/UntiTests/


External Package/TPL Dependencies
+++++++++++++++++++++++++++++++++

ToDo: Document how dependencies between external packages/TPLs are determined
in FindTPL<ExternalPackage>Dependencies.cmake files and
<ExternalPackage>_LIB_REQUIRED_DEP_PACKAGES_OVERRIDE and
<ExternalPackage>_LIB_OPTIONAL_DEP_PACKAGES_OVERRIDE variables that can be
overridden in the cache.


Top-level internal cache variables defining header and library dependencies
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

The following global internal cache variables are used to communicate
the required header directory paths and libraries needed to build and
link against a given package's capabilities::

  ${PACKAGE_NAME}_INCLUDE_DIRS

    Defines a list of include paths needed to find all of the headers needed
    to compile client code against this (sub)packages sources and it's
    upstream packages and TPL sources.  This variable is used whenever
    building downstream code including downstream libraries or executables in
    the same package, or libraries or executables in downstream packages.  It
    is also used to list out in ${PACKAGE_NAME}Config.cmake and
    Makefile.export.${PACKAGE_NAME} files.

    ToDo: Look to eliminate this variable and just add it to the package's
    library targets with target_include_directories().

    ToDo: Split off ${PACKAGE_NAME}_TPL_INCLUDE_DIRS
  
  ${PACKAGE_NAME}_LIBRARY_DIRS
  
    Defines as list of the link directories needed to find all of the
    libraries for this packages and it's upstream packages and TPLs.  Adding
    these library directories to the CMake link line is unnecessary and would
    cause link-line too long errors on some systems.  Instead, this list of
    library directories is used when creating ${PACKAGE_NAME}Config.cmake and
    Makefile.export.${PACKAGE_NAME} files.
  
  ${PACKAGE_NAME}_LIBRARIES
  
    Defines list of *only* the libraries associated with the given
    (sub)package and does *not* list libraries in upstream packages.  Linkages
    to upstream packages is taken care of with calls to
    TARGET_LINK_LIBRARIES(...) and the dependency management system in CMake
    takes care of adding these to various link lines as needed (this is what
    CMake does well).  However, when a package has no libraries of its own
    (which is often the case for packages that have subpackages, for example),
    then this list of libraries will contain the libraries to the direct
    dependent upstream packages in order to allow the chain of dependencies to
    be handled correctly in downstream packages and executables in the same
    package.  In this case, ${PACKAGE_NAME}_HAS_NATIVE_LIBRARIES will be
    false.  The primary purpose of this variable is to passe to
    TARGET_LINK_LIBRARIES(...) by downstream libraries and executables.

  ${PACKAGE_NAME}_HAS_NATIVE_LIBRARIES

    Will be true if a package has native libraries.  Otherwise, it will be
    false.  This information is used to build export makefiles to avoid
    duplicate libraries on the link line.

  ${PACKAGE_NAME}_FULL_ENABLED_DEP_PACKAGES

    Lists out, in order, all of the enabled upstream SE packages that the
    given package depends on and support that package is enabled in the given
    package.  This is only computed if
    ${PROJECT_NAME}_GENERATE_EXPORT_FILE_DEPENDENCIES=ON.  This is needed to
    generate the export makefile Makefile.export.${PACKAGE_NAME}.  NOTE: This
    list does *not* include the package itself.  This list is created after
    all of the enable/disable logic is applied.
 
  ${PARENT_PACKAGE_NAME}_LIB_TARGETS
 
    Lists all of the library targets for this package only that are as part of
    this package added by the TRIBITS_ADD_LIBRARY(...) function.  This is used
    to define a target called ${PACKAGE_NAME}_libs that is then used by
    TRIBITS_CTEST_DRIVER().  If a package has no libraries, then the library
    targets for all of the immediate upstream direct dependent packages will
    be added.  This is needed for the chain of dependencies to work correctly.
    Note that subpackages don't have this variable defined for them.
 
  ${PARENT_PACKAGE_NAME}_ALL_TARGETS
 
    Lists all of the targets associated with this package.  This includes all
    libraries and tests added with TRIBITS_ADD_LIBRARY(...) and
    TRIBITS_ADD_EXECUTABLE(...).  If this package has no targets (no libraries
    or executables) this this will have the dependency only on
    ${PARENT_PACKAGE_NAME}_libs.  Note that subpackages don't have this
    variable defined for them.


Notes on dependency logic
+++++++++++++++++++++++++

The logic used to define the intra-package linkage variables is complex due to
a number of factors:

1) Packages can have libraries or no libraries.  

2) In installation-testing mode, the libraries for a package are read from a
file instead of generated in source.

3) A library can be a regular package library, or a test-only library, in
which case it will not be listed in ${PACKAGE_NAME}_LIBRARIES.  The above
description does not even talk about how test-only libraries are handed within
the system except to say that they are excluded from the package's exported
library dependencies.

The management and usage of the intra-package linkage variables is spread
across a number of TriBITS ``*.cmake`` files but the primary ones are::

  TribitsPackageMacros.cmake
  TribitsSubPackageMacros.cmake
  TribitsLibraryMacros.cmake
  TribitsAddExecutable.cmake

There are other TriBITS cmake files that also access these variables but these
are the key files.  The CMake code in these files all work together in
coordination to set up and use these variables in a way that allows for smooth
compiling and linking of source code for users of the TriBITS system.

Another file with complex dependency logic related to these variables is::

   TribitsWriteClientExportFiles.cmake

The TriBITS cmake code in this file servers a very similar role for external
clients and therefore needs to be considered in this setting.

All of these variations and features makes this a bit of a complex system to
say the least.  Also, currently, there is essentially no unit or regression
testing in place for the CMake code in these files that manipulate these
intra-package dependency variables.  Because this logic is tied in with
actually building and linking code, there has not been a way set up yet to
allow it to be efficiently tested outside of the actual build.  But there are
a number of example projects that are part of the automated TriBITS test suite
that do test much of the logic used in these variables.
