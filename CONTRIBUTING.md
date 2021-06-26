# Contributing to TriBITS

**Contents:**
* [Requirements for every change to TriBITS](#requirements)
* [Preferred process for suggesting and making changes to TriBITS](#process):
  * [Process Outline](#process_outline)
  * [Process Details](#process_details)

Contributions to TriBITS are welcomed.  However, there are some [requirements](#requirements) that every contribution needs to follow before it can be integrated into the main development branch of TriBITS and there is a [recommended process](#process) for suggesting and submitted proposed changes.

**NOTE:** See GitHub documentation for overviews and the mechanical steps to create a [GitHub fork](https://help.github.com/articles/about-forks/), [push topic branches](https://help.github.com/articles/pushing-to-a-remote/), and [create pull requests](https://help.github.com/articles/creating-a-pull-request/).  That documentation and links should provide everything you should need to know about how to perform those standard GitHub tasks.  Those mechanical steps are **not** repeated here.

**NOTE:** All contributions that are submitted are assumed to be given under the **[3-clause BSD-like TriBITS License](https://github.com/TriBITSPub/TriBITS/blob/master/tribits/Copyright.txt).**

<a name="requirements"/>

## Requirements for every change to TriBITS

1. **Automated Tests:** Any change in behavior or new behavior needs to be accompanied with automated tests to define and protect these changes.  If automated tests are not possible or too difficult, this can be discussed in the Github Issue or Pull-Request (see below).
2. **GitHub Issue:** All non-trivial changes should have a [GitHub Issue created](#process_create_issue) for them and all associated commits should list the GitHub Issue ID in the commit logs.
3. **Documentation:** Any new feature or change in the behavior of an existing feature must be fully documented before it is accepted.  This documentation is generally added to one or more of the following places:
   * Implementation `*.cmake` file itself (formatted with restructuredText and pulled out automatically into the TriBITS Developers Guide, see existing examples)
   * `TribitsUsersGuide.rst` document (under `tribits/doc/guides/users_guide/`)
   * `TribitsMaintainersGuide.rst` document (under `tribits/doc/guides/maintainers_guide/`)
   * `TribitsBuildReferenceBody.rst` document (under `tribits/doc/build_ref/`)

**NOTE**: All of these tasks may not need to be done by a external contributor.  It is just that *someone* will need to do all of this before a contibution can be merged into the 'master' branch of the TriBITS repo.

<a name="process">

## Preferred process for suggesting and making changes to TriBITS

<a name="process_outline">

### Process Outline

The steps in the preferred process for making changes to TriBITS are:

1. [Create GitHub Issue](#process_create_issue) (communicate about the requirements and design)
2. [Create Pull-Request](#process_create_pull_request) (each commit references the GitHub Issue ID)
3. [Perform Code Review](#process_code_review) (perhaps adding new commits to address issues)
4. [Accept Pull-Request](#process_accept_pull_request) (merge/rebase and push the branch to 'master')

The details are given in the next section.

<a name="process_details"/>

### Process Details

The following roles are mentioned on the process descriptions:
* **TriBITS Maintainer**: Individual with push rights to the main TriBITS repo (i.e. [@bartlettroscoe](https://github.com/bartlettroscoe)).  Must review all issues and suggested changes and accept pull-requests.
* **TriBITS Developer**: Someone who knows how to built TriBITS as a project with its tests, add tests, make acceptable changes, create pull-requests, etc. but can't directly push to the main TriBITS github 'master' branch (see the role of [TriBITS System Developer](https://tribits.org/doc/TribitsMaintainersGuide.html#tribits-system-developer)).  This might be the Issue Reporter.
* **Issue Reporter**: A person who first reports an issue with TriBITS and would like some type of change to happen (i.e. to fix a defect, implement a new feature, etc.).  This might be a TriBITS Developer.

With those definitions in place, the recommended/preferred process for contributing to TriBITS is:

<a name="process_create_issue"/>

1. **Create GitHub Issue:** The Issue Reporter should submit a [GitHub Issue](https://github.com/TriBITSPub/TriBITS/issues) (e.g. with ID `123`) proposing the change (see [Kanban Process](https://github.com/TriBITSPub/TriBITS/wiki/Kanban-Process-for-Issue-Tracking) used to manage TriBITS Issues).  That way, a conversation can be started to make sure the right contribution is made and to avoid wasted effort in case a suggested change can't be accepted for some reason.  **If the TriBITS Maintainer decides that the proposed change is not appropriate, then the Issue may be closed after the justification is added to a comment.**  Also, the TriBITS Maintainer may offer to implement the changes themselves or ask another TriBITS Developer to do so if that is most appropriate.  However, regardless of who actually makes the proposed changes, the following steps should is still be followed.

<a name="process_create_pull_request"/>

2. **Create Pull-Request:** After the proposed change is approved in the GitHub Issue by the TriBITS Maintainer, then the TriBITS Developer should create a Pull-Request performing the following steps:
    * **Create a topic/feature branch** using a descriptive name containing the Issue ID (e.g. `123-some-great-feature`),
    * **Create commits with logs messages referencing the Issue ID** (e.g. `fix that thing (#123)`),
    * **Issue a pull-request (PR)** by [pushing the topic branch to your fork](https://help.github.com/articles/pushing-to-a-remote/) and then [creating the pull request](https://help.github.com/articles/creating-a-pull-request/).
    * The **changes in the PR will automatically be tested** using [Travis CI](https://travis-ci.org/TriBITSPub/TriBITS).  Also, the PR allows for a well managed code review (comments for each line of the change, for example).  The pull request should then reference the original GitHub Issue in a comment  (i.e. `Addressess #123`).  (NOTE: A partial set of changes is just fine in the PR, just enough to start the code review process.)
    * **NOTE:** The TriBITS Maintainers should be given push access to the topic-branch used to create the PR.  That way, the contributors, TriBITS Developers and the TriBITS Maintainer can all push new commits to that branch in a more collaborative way and have the PR Issue get updated automatically.

<a name="process_code_review"/>

3. **Perform Code Review:** A code review process is performed by the TriBITS Maintainer and continued changes are made by the TriBITS Developer and comments are added to the new PR or the original Issue (whatever makes sense but usually comments specific to changes should be added to the PR while more general comments not specific to the PR should go into the associated GitHub Issue).  New updates to the branch can be pushed by the TriBITS Developer as changes are made to address issues with the changes.

<a name="process_accept_pull_request"/>

4. **Accept Pull-Request:** The TriBITS maintainer will then either accept the PR (by optionally rebasing and merging the branch to main development branch) or will state what further issues must be resolved before the change can be incorporated.

**NOTE:** Very simple changes can be attached to a GitHub Issue which are generated using `git format-patch` but the above process involving pull requests is preferred. 

**NOTE:** The above process is just a suggested process.  What is important are the [requirements](#requirements) listed above.
