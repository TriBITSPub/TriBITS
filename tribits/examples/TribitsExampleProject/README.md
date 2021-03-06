# TribitsExampleProject Documentation

The project TribitsExampleProject defines a TriBITS CMake project designed to
provide a simple example to demonstrate how to use the TriBITS system to
create a CMake build, test, and deployment system using a package-based
architecture.

To get started building you can create a directory structure like:

```
    ~/TribitsExampleProject.base/
        TribitsExampleProject/   # This directory
        BUILDS/
          SERIAL/
```

After that configure pointing to some value TriBITS source dir <tribits-dir>
(i.e. TriBITS/tribits) with:

```
  cd BUILDS/SERIAL/ 

  cmake -D \
    -DTribitsExProj_TRIBITS_DIR=<tribits-dir> \
    -DTribitsExProj_ENABLE_TESTS=ON \
    -DTribitsExProj_ENABLE_ALL_PACKAGES=ON
    -DCMAKE_CXX_COMPILER=g++ \
    ../../examples/TribitsExampleProject
```

and then build and test with:

```
  make -j4 && ctest -j4
```

The layout of a TriBITS project is described in:

* https://tribits.org/doc/TribitsUsersGuide.html#tribits-project-structure

Otherwise, this example TriBITS project is simple enough that it should be
enough to get started as a template.
