# Working on TriBITS

TriBITS is a CMake-based build, integration, and test system for projects with multiple packages and repositories. Start with [README.rst](README.rst), [CONTRIBUTING.md](CONTRIBUTING.md), and the [Maintainers Guide](https://tribitspub.github.io/TriBITS/maintainers_guide/index.html).

## Repository layout

- `tribits/core/`: CMake package architecture, dependency handling, and test support.
- `tribits/ci_support/`, `tribits/ctest_driver/`, `tribits/python_utils/`: CI, CTest driver, and Python utilities.
- `test/`: automated tests for TriBITS itself.
- `tribits/examples/`: example projects; `tribits/doc/`: documentation sources.
- `dev_testing/`: configuration and testing scripts for TriBITS development.

## Making changes

- Preserve backward compatibility for projects using TriBITS.
- Follow nearby code conventions: `tribits_lower_case_name()` for CMake functions and macros, `TribitsModuleName.cmake` for modules, and `ProperNoun_UPPER_CASE` for global/cache variables.
- Add automated tests for new or changed behavior and update the relevant documentation, including reStructuredText documentation in CMake source files.
- Use existing tests to understand behavior; when documentation and tests disagree, the maintainers' guide treats tests as authoritative.

## Build and test

Use a pre-configured CMake build directory under `./BUILDS/` already configured and ready to go to test TriBITS. The user may tell you the build directory to use as `<build-dir>`.

To reconfigure, build, and test use:

```bash
cd <build-dir>/
./do-configure
ninja
ctest -j $(nproc)
```
