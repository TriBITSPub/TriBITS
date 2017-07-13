# Contributing to TriBITS

**Contents:**
* [Requirements for every change to TriBITS](#requirements)
* [Preferred process for suggesting and making changes to TriBITS](#process):
  * [Process Outline](#process_outline)
  * [Process Details](#process_details)

Contributions to TriBITS are welcomed.  However, there are some [requirements](#requirements) that every contribution needs to follow before it can be integrated into the main development branch of TriBITS and there is a [recommended process](#process) for suggesting and submitted proposed changes.

**NOTE:** All contributions that are submitted are assumed to be given under the **[3-clause BSD-like TriBITS License](https://github.com/TriBITSPub/TriBITS/blob/master/tribits/Copyright.txt).**

<a name="requirements"/>

## Requirements for every change to TriBITS

1. **Automated Tests:** Any change in behavior or new behavior needs to be accompanied with automated tests to define and protect these changes.  If automated tests are not possible or too difficult, this can be discussed in the Github Issue or Pull-Request (see below).
2. **GitHub Issue:** All non-trivial changes should have a [GitHub Issue created](#process_create_issue) for them and all associated commits should list the GitHub Issue ID in the commit logs.
3. **Documentation:** Any new feature or change in the behavior of an existing feature must be fully documented before it is accepted.  This documentation is generally added to one or more of the following places:
   * Implementation `*.cmake` file itself (formatted with restructuredText and pulled out automatically into the TriBITS Developers Guide, see existing examples)
   * `TribitsDevelopersGuide.rst` document (under `tribits/doc/developers_guide/`)
   * `TribitsBuildReferenceBody.rst` document (under `tribits/doc/build_ref/`)

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
* **TriBITS Maintainer**: Individual with push rights to the main TriBITS repo (i.e. Ross Bartlett).  Must review all issues and suggested changes and accept pull-requests.
* **TriBITS Developer**: Someone who knows how to built TriBITS as a project with its tests, add tests, make acceptable changes, create pull-requests, etc. but can't directly push to the main TriBITS github 'master' branch (see the role of [TriBITS System Developer](https://tribits.org/doc/TribitsDevelopersGuide.html#tribits-developer-and-user-roles)).  This might be the Issue Reporter.
* **Issue Reporter**: A person who first reports an issue with TriBITS and would like some type of change to happen (i.e. to fix a defect, implement a new feature, etc.).  This might be a TriBITS Developer.

With those definitions in place, the recommended/preferred process for contributing to TriBITS is:

<a name="process_create_issue"/>

1. **Create GitHub Issue:** The Issue Reporter should submit a [GitHub Issue](https://github.com/TriBITSPub/TriBITS/issues) proposing the change (see [Kanban Process](https://github.com/TriBITSPub/TriBITS/wiki/Kanban-Process-for-Issue-Tracking) used to manage TriBITS Issues).  That way, a conversation can be started to make sure the right contribution is made and to avoid wasted effort in case a suggested change can't be accepted for some reason.  **If the TriBITS Maintainer decides that the proposed change is not appropriate, then the Issue may be closed after the justification is added to a comment.**  Also, the TriBITS Maintainer may offer to implement the changes themselves or ask another TriBITS Developer to do so if that is most appropriate.  However, regardless of who actually makes the proposed changes, the following steps should is still be followed.

<a name="process_create_pull_request"/>

2. **Create Pull-Request:** After the proposed change is approved in the GitHub Issue by the TriBITS Maintainer, then the TriBITS Developer (who might be the Issue Reporter or the TriBITS Maintainer) should create a Pull-Request performing the following steps:
    * **create a topic/feature branch** in their forked TriBITS repo (use descriptive branch name with issue ID, e.g. `some-great-feature-123`) ,
    * **create commits with logs referencing the Issue ID** (e.g. `fix that thing (#123)`),
    * **issue a [pull-request](https://help.github.com/articles/using-pull-requests/) (i.e. PR)**.
    * The changes in the PR will automatically be tested using [Travis CI](https://travis-ci.org/TriBITSPub/TriBITS).  Also, the PR allows for a well managed code review (comments for each line of the change, for example).  The pull request should then reference the original GitHub Issue in a comment to link the PR to the original Issue.  (NOTE: A partial set of changes is just fine in the PR, just enough to start the code review process.)
    * NOTE: The TriBITS Maintainers should be given push access to the topic-branch used to create the PR.  That way, the contributors, TriBITS Developers and the TriBITS Maintainer can all push new commits to that branch in a more collaborative way and have the PR Issue get updated automatically.

<a name="process_code_review"/>

3. **Perform Code Review:** A code review process is performed by the TriBITS Maintainer and continued changes are made by the TriBITS Developer and comments are added to the new PR or the original Issue (whatever makes sense but usually comments specific to changes should be added to the PR while more general comments not specific to the PR should go into the associated GitHub Issue).  New updates to the branch can be pushed by the TriBITS Developer as changes are made to address issues with the changes.  (And if the topic branch is pushed to the main GitHub repo, then multiple developers can push commits as well.)

<a name="process_accept_pull_request"/>

4. **Accept Pull-Request:** The TriBITS maintainer will then either accept the PR (by rebasing and merging the branch to main development branch) or will state what further issues must be resolved before the change can be incorporated.

**NOTE:** Very simple changes can be attached to a GitHub Issue which are generated using `git format-patch` but the above process involving pull requests is preferred.  But **generally raw patches will not be accepted** due to the added difficulty for the TriBITS Maintainer to review the changes and to eventually apply them to the TriBITS 'master' branch itself.  Also, using git commits sent either through a branch in a pull-request or through `git format-patch` will record the author's contribution and give them credit for the change. 

**NOTE:** The above process is just a suggested process.  What is important are the [requirements](#requirements) listed above.
