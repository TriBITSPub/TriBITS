#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @HEADER
# ************************************************************************
#
#            TriBITS: Tribal Build, Integrate, and Test System
#                    Copyright 2013 Sandia Corporation
#
# Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
# the U.S. Government retains certain rights in this software.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the Corporation nor the names of the
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY SANDIA CORPORATION "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL SANDIA CORPORATION OR THE
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# ************************************************************************
# @HEADER

#################################
# Unit testing code for gitdist #
#################################

import sys
import shutil
import tempfile
import json
import shlex

from unittest_helpers import *

pythonDir = os.path.abspath(GeneralScriptSupport.getScriptBaseDir())
utilsDir = pythonDir+"/utils"
tribitsDir = os.path.abspath(pythonDir+"/..")

sys.path = [pythonUtilsDir] + sys.path
from gitdist import *


#
# Utility functions for testing
#


gitdistPath = pythonUtilsDir+"/gitdist"
gitdistPathNoColor = gitdistPath+" --dist-no-color"
gitdistPathMock = gitdistPathNoColor+" --dist-use-git=mockgit --dist-no-opt"
mockGitPath = pythonUtilsDir+"/mockprogram.py"

unitTestDataDir = testPythonUtilsDir

tempMockProjectDir = "MockProjectDir"

testBaseDir = os.getcwd()


def getCmndOutputInMockProjectDir(cmnd):
  os.chdir(mockProjectDir)
  cmndOut = getCmndOutput(cmnd)
  os.chdir(testBaseDir)
  return cmndOut


def createAndMoveIntoTestDir(testDir):
  if os.path.exists(testDir): shutil.rmtree(testDir)
  os.mkdir(testDir)
  os.chdir(testDir)
  if not os.path.exists(tempMockProjectDir): os.mkdir(tempMockProjectDir)
  os.chdir(tempMockProjectDir)
  return os.path.join(testBaseDir, testDir, tempMockProjectDir)


class GitDistOptions:

  def __init__(self, useGit):
    self.useGit = useGit


#
# Unit tests for createTable
#


class test_createTable(unittest.TestCase):


  def setUp(self):
    self.gitdistMoveToBaseDir = os.environ.get("GITDIST_MOVE_TO_BASE_DIR", "")
    os.environ["GITDIST_MOVE_TO_BASE_DIR"] = ""
    self.pwd = os.environ.get("PWD", "")
    self.gitdistUnitTestSttySize = os.environ.get(
      "GITDIST_UNIT_TEST_STTY_SIZE", ""
    )


  def tearDown(self):
    os.environ["GITDIST_MOVE_TO_BASE_DIR"] = self.gitdistMoveToBaseDir
    os.environ["PWD"] = self.pwd
    os.environ["GITDIST_UNIT_TEST_STTY_SIZE"] = self.gitdistUnitTestSttySize


  def test_full_table(self):
    tableData = [
      { "label" : "ID", "align" : "R",
        "fields" : ["0", "1", "2"] },
      { "label" : "Repo Dir", "align" : "L",
         "fields" : ["Base: BaseRepo", "ExtraRepo1", "Path/To/ExtraRepo2" ] },
      { "label":"Branch", "align":"L",
        "fields" : ["dummy", "master", "HEAD" ] },
      { "label" : "Tracking Branch", "align":"L",
        "fields" : ["", "origin/master", "" ] },
      { "label" : "C", "align":"R", "fields" : ["", "1", "" ] },
      { "label" : "M", "align":"R", "fields" : ["0", "2", "25" ] },
      { "label" : "?", "align":"R", "fields" : ["0", "0", "4" ] },
      ]
    table = createTable(tableData)
    #print(table)
    table_expected = \
      "-------------------------------------------------------------------\n" \
      "| ID | Repo Dir           | Branch | Tracking Branch | C | M  | ? |\n" \
      "|----|--------------------|--------|-----------------|---|----|---|\n" \
      "|  0 | Base: BaseRepo     | dummy  |                 |   |  0 | 0 |\n" \
      "|  1 | ExtraRepo1         | master | origin/master   | 1 |  2 | 0 |\n" \
      "|  2 | Path/To/ExtraRepo2 | HEAD   |                 |   | 25 | 4 |\n" \
      "-------------------------------------------------------------------\n"
    self.assertEqual(table, table_expected)


  def test_full_table_utf8(self):
    if sys.version_info < (3,):
      print("Test disabled for Python 2.")
    else:
      tableData = [
        { "label" : "ID", "align" : "R",
          "fields" : ["0", "1", "2"] },
        { "label" : "Repo Dir", "align" : "L",
           "fields" : ["Base: BaseRepo", "ExtraRepo1", "Path/To/ExtraRepo2" ] },
        { "label":"Branch", "align":"L",
          "fields" : ["dummy", "master", "HEAD" ] },
        { "label" : "Tracking Branch", "align":"L",
          "fields" : ["", "origin/master", "" ] },
        { "label" : "C", "align":"R", "fields" : ["", "1", "" ] },
        { "label" : "M", "align":"R", "fields" : ["0", "2", "25" ] },
        { "label" : "?", "align":"R", "fields" : ["0", "0", "4" ] },
        ]
      table = createTable(tableData, True)
      #print(table)
      table_expected = \
        "┌────┬────────────────────┬────────┬─────────────────┬───┬────┬───┐\n" \
        "│ ID │ Repo Dir           │ Branch │ Tracking Branch │ C │ M  │ ? │\n" \
        "┝━━━━┿━━━━━━━━━━━━━━━━━━━━┿━━━━━━━━┿━━━━━━━━━━━━━━━━━┿━━━┿━━━━┿━━━┥\n" \
        "│  0 │ Base: BaseRepo     │ dummy  │                 │   │  0 │ 0 │\n" \
        "│  1 │ ExtraRepo1         │ master │ origin/master   │ 1 │  2 │ 0 │\n" \
        "│  2 │ Path/To/ExtraRepo2 │ HEAD   │                 │   │ 25 │ 4 │\n" \
        "└────┴────────────────────┴────────┴─────────────────┴───┴────┴───┘\n"
      self.assertEqual(table, table_expected)


  def test_no_rows(self):
    tableData = [
      { "label" : "ID", "align" : "R",
        "fields" : [] },
      { "label" : "Repo Dir", "align" : "L",
         "fields" : [] },
      { "label":"Branch", "align":"L",
        "fields" : [] },
      { "label" : "Tracking Branch", "align":"L",
        "fields" : [] },
      { "label" : "C", "align":"R", "fields" : [] },
      { "label" : "M", "align":"R", "fields" : [] },
      { "label" : "?", "align":"R", "fields" : [] },
      ]
    table = createTable(tableData)
    #print(table)
    table_expected = \
      "--------------------------------------------------------\n" \
      "| ID | Repo Dir | Branch | Tracking Branch | C | M | ? |\n" \
      "|----|----------|--------|-----------------|---|---|---|\n" \
      "--------------------------------------------------------\n"
    self.assertEqual(table, table_expected)


  def test_no_rows_utf8(self):
    if sys.version_info < (3,):
      print("Test disabled for Python 2.")
    else:
      tableData = [
        { "label" : "ID", "align" : "R",
          "fields" : [] },
        { "label" : "Repo Dir", "align" : "L",
           "fields" : [] },
        { "label":"Branch", "align":"L",
          "fields" : [] },
        { "label" : "Tracking Branch", "align":"L",
          "fields" : [] },
        { "label" : "C", "align":"R", "fields" : [] },
        { "label" : "M", "align":"R", "fields" : [] },
        { "label" : "?", "align":"R", "fields" : [] },
        ]
      table = createTable(tableData, True)
      #print(table)
      table_expected = \
        "┌────┬──────────┬────────┬─────────────────┬───┬───┬───┐\n" \
        "│ ID │ Repo Dir │ Branch │ Tracking Branch │ C │ M │ ? │\n" \
        "┝━━━━┿━━━━━━━━━━┿━━━━━━━━┿━━━━━━━━━━━━━━━━━┿━━━┿━━━┿━━━┥\n" \
        "└────┴──────────┴────────┴─────────────────┴───┴───┴───┘\n"
      self.assertEqual(table, table_expected)


  def test_one_row(self):
    tableData = [
      { "label" : "ID", "align" : "R",
        "fields" : ["0"] },
      { "label" : "Repo Dir", "align" : "L",
         "fields" : ["Base: BaseRepo"] },
      { "label":"Branch", "align":"L",
        "fields" : ["dummy"] },
      { "label" : "Tracking Branch", "align":"L",
        "fields" : ["origin/master"] },
      { "label" : "C", "align":"R", "fields" : ["24"] },
      { "label" : "M", "align":"R", "fields" : ["25"] },
      { "label" : "?", "align":"R", "fields" : ["4"] },
      ]
    table = createTable(tableData)
    #print(table)
    table_expected = \
      "----------------------------------------------------------------\n" \
      "| ID | Repo Dir       | Branch | Tracking Branch | C  | M  | ? |\n" \
      "|----|----------------|--------|-----------------|----|----|---|\n" \
      "|  0 | Base: BaseRepo | dummy  | origin/master   | 24 | 25 | 4 |\n" \
      "----------------------------------------------------------------\n"
    self.assertEqual(table, table_expected)


  def test_one_row_utf8(self):
    if sys.version_info < (3,):
      print("Test disabled for Python 2.")
    else:
      tableData = [
        { "label" : "ID", "align" : "R",
          "fields" : ["0"] },
        { "label" : "Repo Dir", "align" : "L",
           "fields" : ["Base: BaseRepo"] },
        { "label":"Branch", "align":"L",
          "fields" : ["dummy"] },
        { "label" : "Tracking Branch", "align":"L",
          "fields" : ["origin/master"] },
        { "label" : "C", "align":"R", "fields" : ["24"] },
        { "label" : "M", "align":"R", "fields" : ["25"] },
        { "label" : "?", "align":"R", "fields" : ["4"] },
        ]
      table = createTable(tableData, True)
      #print(table)
      table_expected = \
        "┌────┬────────────────┬────────┬─────────────────┬────┬────┬───┐\n" \
        "│ ID │ Repo Dir       │ Branch │ Tracking Branch │ C  │ M  │ ? │\n" \
        "┝━━━━┿━━━━━━━━━━━━━━━━┿━━━━━━━━┿━━━━━━━━━━━━━━━━━┿━━━━┿━━━━┿━━━┥\n" \
        "│  0 │ Base: BaseRepo │ dummy  │ origin/master   │ 24 │ 25 │ 4 │\n" \
        "└────┴────────────────┴────────┴─────────────────┴────┴────┴───┘\n"
      self.assertEqual(table, table_expected)


  def test_row_mismatch(self):
    tableData = [
      { "label" : "ID", "align" : "R",
        "fields" : ["0", "1"] },
      { "label" : "Repo Dir", "align" : "L",
         "fields" : ["Base: BaseRepo"] },
      ]
    #createTable(tableData)
    self.assertRaises(Exception, createTable, tableData)
  

  def create_stty_size_table(self):
    tableData = [
      { "label" : "ID", "align" : "R", "fields" : ["0", "1", "2"] },
      { "label" : "Repo Dir", "align" : "L",
        "fields" : [
          "MockProjectDir (Base)",
          "ExtraRepo1",
          "really/long/path/to/ExtraRepo2"
        ]
      },
      { "label" : "Branch", "align" : "L",
        "fields" : [
          "medium_branch",
          "short_br",
          "really_long_branch_name"
        ]
      },
      { "label" : "Tracking Branch", "align" : "L",
        "fields" : [
          "medium_remote/medium_branch",
          "origin/short_br",
          "long_remote_name/really_long_branch_name"
        ]
      },
      { "label" : "C", "align" : "R", "fields" : ["", "", ""] },
      { "label" : "M", "align" : "R", "fields" : ["", "", ""] },
      { "label" : "?", "align" : "R", "fields" : ["", "", ""] }
    ]
    return tableData


  def test_stty_size_larger_than_needed(self):
    os.environ["GITDIST_UNIT_TEST_STTY_SIZE"] = "60 140"
    table = createTable(self.create_stty_size_table())
    #print(table)
    table_expected = \
      "------------------------------------------------------------------------------------------------------------------------\n" \
      "| ID | Repo Dir                       | Branch                  | Tracking Branch                          | C | M | ? |\n" \
      "|----|--------------------------------|-------------------------|------------------------------------------|---|---|---|\n" \
      "|  0 | MockProjectDir (Base)          | medium_branch           | medium_remote/medium_branch              |   |   |   |\n" \
      "|  1 | ExtraRepo1                     | short_br                | origin/short_br                          |   |   |   |\n" \
      "|  2 | really/long/path/to/ExtraRepo2 | really_long_branch_name | long_remote_name/really_long_branch_name |   |   |   |\n" \
      "------------------------------------------------------------------------------------------------------------------------\n"
    self.assertEqual(table, table_expected)


  def test_stty_size_exactly_right(self):
    os.environ["GITDIST_UNIT_TEST_STTY_SIZE"] = "60 120"
    table = createTable(self.create_stty_size_table())
    #print(table)
    table_expected = \
      "------------------------------------------------------------------------------------------------------------------------\n" \
      "| ID | Repo Dir                       | Branch                  | Tracking Branch                          | C | M | ? |\n" \
      "|----|--------------------------------|-------------------------|------------------------------------------|---|---|---|\n" \
      "|  0 | MockProjectDir (Base)          | medium_branch           | medium_remote/medium_branch              |   |   |   |\n" \
      "|  1 | ExtraRepo1                     | short_br                | origin/short_br                          |   |   |   |\n" \
      "|  2 | really/long/path/to/ExtraRepo2 | really_long_branch_name | long_remote_name/really_long_branch_name |   |   |   |\n" \
      "------------------------------------------------------------------------------------------------------------------------\n"
    self.assertEqual(table, table_expected)


  def test_stty_size_slightly_too_small(self):
    os.environ["GITDIST_UNIT_TEST_STTY_SIZE"] = "60 106"
    table = createTable(self.create_stty_size_table())
    #print(table)
    table_expected = \
      "----------------------------------------------------------------------------------------------------------\n" \
      "| ID | Repo Dir                  | Branch              | Tracking Branch                     | C | M | ? |\n" \
      "|----|---------------------------|---------------------|-------------------------------------|---|---|---|\n" \
      "|  0 | MockProjectDir (Base)     | medium_branch       | medium_remote/medium_branch         |   |   |   |\n" \
      "|  1 | ExtraRepo1                | short_br            | origin/short_br                     |   |   |   |\n" \
      "|  2 | really/long.../ExtraRepo2 | really_l...nch_name | long_remote_name...long_branch_name |   |   |   |\n" \
      "----------------------------------------------------------------------------------------------------------\n"
    self.assertEqual(table, table_expected)


  def test_stty_size_significantly_too_small(self):
    os.environ["GITDIST_UNIT_TEST_STTY_SIZE"] = "60 70"
    table = createTable(self.create_stty_size_table())
    #print(table)
    table_expected = \
      "----------------------------------------------------------------------\n" \
      "| ID | Repo Dir      | Branch     | Tracking Branch      | C | M | ? |\n" \
      "|----|---------------|------------|----------------------|---|---|---|\n" \
      "|  0 | MockP...Base) | medi...nch | medium_re...m_branch |   |   |   |\n" \
      "|  1 | ExtraRepo1    | short_br   | origin/short_br      |   |   |   |\n" \
      "|  2 | reall...Repo2 | real...ame | long_remo...nch_name |   |   |   |\n" \
      "----------------------------------------------------------------------\n"
    self.assertEqual(table, table_expected)


  def test_stty_size_too_small_for_heading(self):
    os.environ["GITDIST_UNIT_TEST_STTY_SIZE"] = "60 50"
    table = createTable(self.create_stty_size_table())
    #print(table)
    table_expected = \
      "------------------------------------------------------------------------------------------------------------------------\n" \
      "| ID | Repo Dir                       | Branch                  | Tracking Branch                          | C | M | ? |\n" \
      "|----|--------------------------------|-------------------------|------------------------------------------|---|---|---|\n" \
      "|  0 | MockProjectDir (Base)          | medium_branch           | medium_remote/medium_branch              |   |   |   |\n" \
      "|  1 | ExtraRepo1                     | short_br                | origin/short_br                          |   |   |   |\n" \
      "|  2 | really/long/path/to/ExtraRepo2 | really_long_branch_name | long_remote_name/really_long_branch_name |   |   |   |\n" \
      "------------------------------------------------------------------------------------------------------------------------\n"
    self.assertEqual(table, table_expected)


#
# Unit tests for createMarkdownTable
#


class test_createMarkdownTable(unittest.TestCase):


  def create_table_data(self):
    tableData = [
      {"label": "Repository", "align": "L",
       "fields": ["MockProjectDir", "ExtraRepo1", "ExtraRepo2"]},
      {"label": "SHA1", "align": "C",
       "fields": ["e2dc488", "f671414", "50bbf3e"]},
      {"label": "Commit Date", "align": "L",
       "fields": ["2019-10-23 10:16:07", "2019-10-22 11:18:47",
                  "2019-10-17 16:32:15"]},
      {"label": "Author", "align": "L",
       "fields": ["user@domain.com", "wile.e.coyote@acme.com",
                  "someone@somewhere.com"]},
      {"label": "Summary", "align": "L",
       "fields": ["Merge Pull Request #1234 from user/repo/branch",
                  "Fixed a Bug", "Did Some Work"]}
      ]
    return tableData


  def test_full_markdown_table(self):
    tableData = self.create_table_data()
    table = createMarkdownTable(tableData)
    #print(table)
    table_expected = \
      "| Repository     | SHA1    | Commit Date         | Author                 | Summary                                        |\n" \
      "|:-------------- |:-------:|:------------------- |:---------------------- |:---------------------------------------------- |\n" \
      "| MockProjectDir | e2dc488 | 2019-10-23 10:16:07 | user@domain.com        | Merge Pull Request #1234 from user/repo/branch |\n" \
      "| ExtraRepo1     | f671414 | 2019-10-22 11:18:47 | wile.e.coyote@acme.com | Fixed a Bug                                    |\n" \
      "| ExtraRepo2     | 50bbf3e | 2019-10-17 16:32:15 | someone@somewhere.com  | Did Some Work                                  |"
    self.assertEqual(table, table_expected)


  def test_short_markdown_table(self):
    tableData = self.create_table_data()[0:2]
    table = createMarkdownTable(tableData)
    #print(table)
    table_expected = \
      "| Repository     | SHA1    |\n" \
      "|:-------------- |:-------:|\n" \
      "| MockProjectDir | e2dc488 |\n" \
      "| ExtraRepo1     | f671414 |\n" \
      "| ExtraRepo2     | 50bbf3e |"
    self.assertEqual(table, table_expected)


  def test_no_rows(self):
    tableData = self.create_table_data()
    for entry in tableData:
        entry["fields"][:] = []
    table = createMarkdownTable(tableData)
    #print(table)
    table_expected = \
      "| Repository | SHA1 | Commit Date | Author | Summary |\n" \
      "|:---------- |:----:|:----------- |:------ |:------- |"
    self.assertEqual(table, table_expected)


  def test_one_row(self):
    tableData = self.create_table_data()
    for entry in tableData:
        entry["fields"][:] = [entry["fields"][0]]
    table = createMarkdownTable(tableData)
    #print(table)
    table_expected = \
      "| Repository     | SHA1    | Commit Date         | Author          | Summary                                        |\n" \
      "|:-------------- |:-------:|:------------------- |:--------------- |:---------------------------------------------- |\n" \
      "| MockProjectDir | e2dc488 | 2019-10-23 10:16:07 | user@domain.com | Merge Pull Request #1234 from user/repo/branch |"
    self.assertEqual(table, table_expected)


  def test_row_mismatch(self):
    tableData = self.create_table_data()
    tableData[0]["fields"][:] = []
    self.assertRaises(Exception, createMarkdownTable, tableData)


#
# Unit tests for functions in gitdist
#


class test_gitdist_getRepoStats(unittest.TestCase):


  def setUp(self):
    self.gitdistMoveToBaseDir = os.environ.get("GITDIST_MOVE_TO_BASE_DIR", "")
    os.environ["GITDIST_MOVE_TO_BASE_DIR"] = ""


  def tearDown(self):
    os.environ["GITDIST_MOVE_TO_BASE_DIR"] = self.gitdistMoveToBaseDir


  def test_no_change(self):
    try:
      testDir = createAndMoveIntoTestDir("gitdist_getRepoStats_no_change")
      with open(".mockprogram_inout.txt", "w") as fileHandle:
        fileHandle.write(
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref HEAD\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: local_branch\n" \
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref --symbolic-full-name @{u}\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: origin_repo/remote_branch\n" \
          "MOCK_PROGRAM_INPUT: shortlog -s HEAD ^origin_repo/remote_branch\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: \n" \
          "MOCK_PROGRAM_INPUT: status --porcelain\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: \n" \
          )
      options = GitDistOptions(mockGitPath)
      repoStats = getRepoStats(options, showMoreHeadDetails="")
      repoStats_expected = "{branch='local_branch'," \
        " trackingBranch='origin_repo/remote_branch', numCommits='0'," \
        " numModified='0', numUntracked='0'}" 
      self.assertEqual(str(repoStats), repoStats_expected)
    finally:
      os.chdir(testBaseDir)


  def test_all_changed_no_tracking_branch(self):
    try:
      testDir = createAndMoveIntoTestDir(
        "gitdist_getRepoStats_all_changed_no_tracking_branch")
      with open(".mockprogram_inout.txt", "w") as fileHandle:
        fileHandle.write(
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref HEAD\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: local_branch\n" \
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref --symbolic-full-name @{u}\n" \
          "MOCK_PROGRAM_RETURN: 55\n" \
          "MOCK_PROGRAM_OUTPUT: error: blah blahh blah\n" \
          "MOCK_PROGRAM_INPUT: status --porcelain\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: M  file1\n" \
          " T file2\n" \
          " D file3\n" \
          "?? file4\n" \
          "?? file5\n" \
          )
      options = GitDistOptions(mockGitPath)
      repoStats = getRepoStats(options, showMoreHeadDetails="")
      repoStats_expected = "{branch='local_branch'," \
        " trackingBranch='', numCommits=''," \
        " numModified='3', numUntracked='2'}" 
      self.assertEqual(str(repoStats), repoStats_expected)
    finally:
      os.chdir(testBaseDir)


  def test_modified_and_staged_no_tracking_branch(self):
    try:
      testDir = createAndMoveIntoTestDir(
        "gitdist_getRepoStats_all_changed_no_tracking_branch")
      with open(".mockprogram_inout.txt", "w") as fileHandle:
        fileHandle.write(
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref HEAD\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: local_branch\n" \
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref --symbolic-full-name @{u}\n" \
          "MOCK_PROGRAM_RETURN: 55\n" \
          "MOCK_PROGRAM_OUTPUT: error: blah blahh blah\n" \
          "MOCK_PROGRAM_INPUT: status --porcelain\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: M  file1\n" \
          "MM file1b\n" \
          " T file2\n" \
          "MT file2b\n" \
          " D file3\n" \
          "MD file3\n" \
          "?? file4\n" \
          "?? file5\n" \
          "?? file5b\n" \
          " A file6\n" \
          "A  file6b\n" \
          " U file7\n" \
          "U  file7b\n" \
          "R  file8\n" \
          )
      options = GitDistOptions(mockGitPath)
      repoStats = getRepoStats(options, showMoreHeadDetails="SHOW_MORE_HEAD_DETAILS")
      repoStats_expected = "{branch='local_branch'," \
        " trackingBranch='', numCommits=''," \
        " numModified='11', numUntracked='3'}" 
      self.assertEqual(str(repoStats), repoStats_expected)
    finally:
      os.chdir(testBaseDir)


  def test_all_changed_detached_head_tag(self):
    try:
      testDir = createAndMoveIntoTestDir("gitdist_getRepoStats_all_changed_detached_head_tag")
      with open(".mockprogram_inout.txt", "w") as fileHandle:
        fileHandle.write(
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref HEAD\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: HEAD\n" \
          "MOCK_PROGRAM_INPUT: tag --points-at\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: 1.2.3\n" \
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref --symbolic-full-name @{u}\n" \
          "MOCK_PROGRAM_RETURN: 128\n" \
          "MOCK_PROGRAM_OUTPUT: fatal: blah blahh blah\n" \
          "MOCK_PROGRAM_INPUT: status --porcelain\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: M  file1\n" \
          " M file2\n" \
          "?? file3\n" \
          "?? file4\n" \
          "?? file5\n" \
          )
      options = GitDistOptions(mockGitPath)
      repoStats = getRepoStats(options, showMoreHeadDetails="SHOW_MORE_HEAD_DETAILS")
      repoStats_expected = "{branch='1.2.3'," \
        " trackingBranch='', numCommits=''," \
        " numModified='2', numUntracked='3'}"
      self.assertEqual(str(repoStats), repoStats_expected)
    finally:
      os.chdir(testBaseDir)


  def test_all_changed_detached_head(self):
    try:
      testDir = createAndMoveIntoTestDir("gitdist_getRepoStats_all_changed_detached_head")
      with open(".mockprogram_inout.txt", "w") as fileHandle:
        fileHandle.write(
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref HEAD\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: HEAD\n" \
          "MOCK_PROGRAM_INPUT: tag --points-at\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: \n" \
          "MOCK_PROGRAM_INPUT: log --pretty=%h -1\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: 1235abcd\n" \
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref --symbolic-full-name @{u}\n" \
          "MOCK_PROGRAM_RETURN: 128\n" \
          "MOCK_PROGRAM_OUTPUT: fatal: blah blahh blah\n" \
          "MOCK_PROGRAM_INPUT: status --porcelain\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: M  file1\n" \
          " M file2\n" \
          "?? file3\n" \
          "?? file4\n" \
          "?? file5\n" \
          )
      options = GitDistOptions(mockGitPath)
      repoStats = getRepoStats(options, showMoreHeadDetails="SHOW_MORE_HEAD_DETAILS")
      repoStats_expected = "{branch='1235abcd'," \
        " trackingBranch='', numCommits=''," \
        " numModified='2', numUntracked='3'}" 
      self.assertEqual(str(repoStats), repoStats_expected)
    finally:
      os.chdir(testBaseDir)


  def test_all_ambiguous_head(self):
    try:
      testDir = createAndMoveIntoTestDir("gitdist_getRepoStats_all_changed_detached_head")
      with open(".mockprogram_inout.txt", "w") as fileHandle:
        fileHandle.write(
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref HEAD\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: warning: refname 'HEAD' is ambiguous.\n" \
          "error: refname 'HEAD' is ambiguous\n" \
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref --symbolic-full-name @{u}\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: remoterepo/trackingbranch\n" \
          "MOCK_PROGRAM_INPUT: shortlog -s HEAD ^remoterepo/trackingbranch\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: 7\n" \
          "MOCK_PROGRAM_INPUT: status --porcelain\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: M  file1\n" \
          " M file2\n" \
          "?? file3\n" \
          "?? file4\n" \
          "?? file5\n" \
          )
      options = GitDistOptions(mockGitPath)
      repoStats = getRepoStats(options, showMoreHeadDetails="SHOW_MORE_HEAD_DETAILS")
      repoStats_expected = "{branch='<AMBIGUOUS-HEAD>'," \
        " trackingBranch='remoterepo/trackingbranch', numCommits='7'," \
        " numModified='2', numUntracked='3'}" 
      self.assertEqual(str(repoStats), repoStats_expected)
    finally:
      os.chdir(testBaseDir)
    # NOTE: Above is a very strange test case.  It is what happens when
    # someone creates a tag called 'HEAD' using the command 'git tag HEAD'
    # (which was an accident obviously).  But amazingly, 'git rev-parse
    # --abbrev HEAD' still returns 0 but returns no name!  See TriBITS #100
    # for details.


  def test_all_changed_1_author(self):
    try:
      testDir = createAndMoveIntoTestDir("gitdist_getRepoStats_all_changed_1_author")
      with open(".mockprogram_inout.txt", "w") as fileHandle:
        fileHandle.write(
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref HEAD\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: local_branch\n" \
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref --symbolic-full-name @{u}\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: origin_repo/remote_branch\n" \
          "MOCK_PROGRAM_INPUT: shortlog -s HEAD ^origin_repo/remote_branch\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: 1\tsome author\n" \
          "MOCK_PROGRAM_INPUT: status --porcelain\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: M  file1\n" \
          " M file2\n" \
          "?? file3\n" \
          "?? file4\n" \
          "?? file5\n" \
          )
      options = GitDistOptions(mockGitPath)
      repoStats = getRepoStats(options, showMoreHeadDetails="SHOW_MORE_HEAD_DETAILS")
      repoStats_expected = "{branch='local_branch'," \
        " trackingBranch='origin_repo/remote_branch', numCommits='1'," \
        " numModified='2', numUntracked='3'}" 
      self.assertEqual(str(repoStats), repoStats_expected)
    finally:
      os.chdir(testBaseDir)


  def test_all_changed_3_authors(self):
    try:
      testDir = createAndMoveIntoTestDir("gitdist_getRepoStats_all_changed_3_authors")
      with open(".mockprogram_inout.txt", "w") as fileHandle:
        fileHandle.write(
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref HEAD\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: local_branch\n" \
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref --symbolic-full-name @{u}\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: origin_repo/remote_branch\n" \
          "MOCK_PROGRAM_INPUT: shortlog -s HEAD ^origin_repo/remote_branch\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: 1 some author1\n" \
          "2 some author2\n" \
          "3 some author2\n" \
          "MOCK_PROGRAM_INPUT: status --porcelain\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: M  file1\n" \
          " M file2\n" \
          "?? file3\n" \
          "?? file4\n" \
          "?? file5\n" \
          )
      options = GitDistOptions(mockGitPath)
      repoStats = getRepoStats(options, showMoreHeadDetails="SHOW_MORE_HEAD_DETAILS")
      repoStats_expected = "{branch='local_branch'," \
        " trackingBranch='origin_repo/remote_branch', numCommits='6'," \
        " numModified='2', numUntracked='3'}" 
      self.assertEqual(str(repoStats), repoStats_expected)
    finally:
      os.chdir(testBaseDir)


repoVersionFile_withSummary_1 = """*** Base Git Repo: MockTrilinos
sha1_1 [Mon Sep 23 11:34:59 2013 -0400] <author_1@ornl.gov>
First summary message
*** Git Repo: extraTrilinosRepo
sha1_2 [Fri Aug 30 09:55:07 2013 -0400] <author_2@ornl.gov>
Second summary message
*** Git Repo: extraRepoOnePackage
sha1_3 [Thu Dec 1 23:34:06 2011 -0500] <author_3@ornl.gov>
Third summary message
"""

repoVersionFile_withoutSummary_1 = """*** Base Git Repo: MockTrilinos
sha1_1 [Mon Sep 23 11:34:59 2013 -0400] <author_1@ornl.gov>
*** Git Repo: extraRepoTwoPackages
sha1_2 [Fri Aug 30 09:55:07 2013 -0400] <author_2@ornl.gov>
*** Git Repo: extraRepoOnePackageThreeSubpackages
sha1_3 [Thu Dec 1 23:34:06 2011 -0500] <author_3@ornl.gov>
"""


# ToDo: Factor out functions to generate list of commands for a single repo
# for a call to getRepoStats() with input arguments for different criteria to
# make the below code more maintainable.


def writeGitMockProgram_base_3_2_1_repo1_22_0_2_repo2_0_0_0():

  with open(".mockprogram_inout.txt", "w") as fileHandle:
    fileHandle.write(
      "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref HEAD\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: local_branch0\n" \
      "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref --symbolic-full-name @{u}\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: origin_repo0/remote_branch0\n" \
      "MOCK_PROGRAM_INPUT: shortlog -s HEAD ^origin_repo0/remote_branch0\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: 3 some author\n" \
      "MOCK_PROGRAM_INPUT: status --porcelain\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: M  file1\n" \
      " M file2\n" \
      "?? file2\n" \
      "MOCK_PROGRAM_INPUT: -c color.status=never status\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: On branch local_branch0\n" \
      "Your branch is ahead of 'origin_repo0/remote_branch0' by 3 commits.\n" \
      )

  os.mkdir("ExtraRepo1")

  with open("ExtraRepo1/.mockprogram_inout.txt", "w") as fileHandle:
    fileHandle.write(
      "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref HEAD\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: local_branch1\n" \
      "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref --symbolic-full-name @{u}\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: origin_repo1/remote_branch1\n" \
      "MOCK_PROGRAM_INPUT: shortlog -s HEAD ^origin_repo1/remote_branch1\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: 22 some author\n" \
      "MOCK_PROGRAM_INPUT: status --porcelain\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: ?? file1\n" \
      "MOCK_PROGRAM_INPUT: -c color.status=never status\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: On branch local_branch1\n" \
      "Your branch is ahead of 'origin_repo1/remote_branch1' by 22 commits.\n" \
      )

  os.mkdir("ExtraRepo2")

  with open("ExtraRepo2/.mockprogram_inout.txt", "w") as fileHandle:
    fileHandle.write(
      "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref HEAD\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: local_branch2\n" \
      "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref --symbolic-full-name @{u}\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: origin_repo2/remote_branch2\n" \
      "MOCK_PROGRAM_INPUT: shortlog -s HEAD ^origin_repo2/remote_branch2\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: \n" \
      "MOCK_PROGRAM_INPUT: status --porcelain\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: \n" \
      )


def writeGitMockProgram_base_3_2_1_repo1_22_0_2_repo2_sha1_0_0_0():

  with open(".mockprogram_inout.txt", "w") as fileHandle:
    fileHandle.write(
      "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref HEAD\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: local_branch0\n" \
      "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref --symbolic-full-name @{u}\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: origin_repo0/remote_branch0\n" \
      "MOCK_PROGRAM_INPUT: shortlog -s HEAD ^origin_repo0/remote_branch0\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: 3 some author\n" \
      "MOCK_PROGRAM_INPUT: status --porcelain\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: M  file1\n" \
      " M file2\n" \
      "?? file2\n" \
      "MOCK_PROGRAM_INPUT: -c color.status=never status\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: On branch local_branch0\n" \
      "Your branch is ahead of 'origin_repo0/remote_branch0' by 3 commits.\n" \
      )

  os.mkdir("ExtraRepo1")

  with open("ExtraRepo1/.mockprogram_inout.txt", "w") as fileHandle:
    fileHandle.write(
      "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref HEAD\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: local_branch1\n" \
      "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref --symbolic-full-name @{u}\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: origin_repo1/remote_branch1\n" \
      "MOCK_PROGRAM_INPUT: shortlog -s HEAD ^origin_repo1/remote_branch1\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: 22 some author\n" \
      "MOCK_PROGRAM_INPUT: status --porcelain\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: ?? file1\n" \
      "MOCK_PROGRAM_INPUT: -c color.status=never status\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: On branch local_branch1\n" \
      "Your branch is ahead of 'origin_repo1/remote_branch1' by 22 commits.\n" \
      )

  os.mkdir("ExtraRepo2")

  with open("ExtraRepo2/.mockprogram_inout.txt", "w") as fileHandle:
    fileHandle.write(
      "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref HEAD\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: HEAD\n" \
      "MOCK_PROGRAM_INPUT: tag --points-at\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: \n" \
      "MOCK_PROGRAM_INPUT: log --pretty=%h -1\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: 1235abcd\n" \
      "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref --symbolic-full-name @{u}\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: \n" \
      "MOCK_PROGRAM_INPUT: shortlog -s HEAD ^origin_repo2/remote_branch2\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: \n" \
      "MOCK_PROGRAM_INPUT: status --porcelain\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: \n" \
      )


def writeGitMockProgram_dist_repo_versions_table():

  with open(".mockprogram_inout.txt", "w") as f:
    f.write(
      "MOCK_PROGRAM_INPUT: rev-parse --short HEAD\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: e2dc488\n" \
      "MOCK_PROGRAM_INPUT: log -1 --pretty=format:%cd --date=format:%G-%m-%d %H:%M:%S\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: 2019-10-23 10:16:07\n" \
      "MOCK_PROGRAM_INPUT: log -1 --pretty=format:%ae\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: user@domain.com\n" \
      "MOCK_PROGRAM_INPUT: log -1 --pretty=format:%s\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: Merge Pull Request #1234 from user/repo/branch\n" \
    )

  os.mkdir("ExtraRepo1")

  with open("ExtraRepo1/.mockprogram_inout.txt", "w") as f:
    f.write(
      "MOCK_PROGRAM_INPUT: rev-parse --short HEAD\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: f671414\n" \
      "MOCK_PROGRAM_INPUT: log -1 --pretty=format:%cd --date=format:%G-%m-%d %H:%M:%S\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: 2019-10-22 11:18:47\n" \
      "MOCK_PROGRAM_INPUT: log -1 --pretty=format:%ae\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: wile.e.coyote@acme.com\n" \
      "MOCK_PROGRAM_INPUT: log -1 --pretty=format:%s\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: Fixed a Bug\n" \
    )

  os.mkdir("ExtraRepo2")

  with open("ExtraRepo2/.mockprogram_inout.txt", "w") as f:
    f.write(
      "MOCK_PROGRAM_INPUT: rev-parse --short HEAD\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: 50bbf3e\n" \
      "MOCK_PROGRAM_INPUT: log -1 --pretty=format:%cd --date=format:%G-%m-%d %H:%M:%S\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: 2019-10-17 16:32:15\n" \
      "MOCK_PROGRAM_INPUT: log -1 --pretty=format:%ae\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: someone@somewhere.com\n" \
      "MOCK_PROGRAM_INPUT: log -1 --pretty=format:%s\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: Did Some Work\n" \
    )


def writeGitMockProgram_dist_repo_versions_table_1_change_base():

  with open(".mockprogram_inout.txt", "w") as f:
    f.write(
      "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref HEAD\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: local_branch0\n" \
      "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref --symbolic-full-name @{u}\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: origin_repo0/remote_branch0\n" \
      "MOCK_PROGRAM_INPUT: shortlog -s HEAD ^origin_repo0/remote_branch0\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: 3 some author\n" \
      "MOCK_PROGRAM_INPUT: status --porcelain\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: M  file1\n" \
      "MOCK_PROGRAM_INPUT: rev-parse --short HEAD\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: e2dc488\n" \
      "MOCK_PROGRAM_INPUT: log -1 --pretty=format:%cd --date=format:%G-%m-%d %H:%M:%S\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: 2019-10-23 10:16:07\n" \
      "MOCK_PROGRAM_INPUT: log -1 --pretty=format:%ae\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: user@domain.com\n" \
      "MOCK_PROGRAM_INPUT: log -1 --pretty=format:%s\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: Merge Pull Request #1234 from user/repo/branch\n" \
    )

  os.mkdir("ExtraRepo1")

  with open("ExtraRepo1/.mockprogram_inout.txt", "w") as f:
    f.write(
      "MOCK_PROGRAM_INPUT: rev-parse --short HEAD\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: f671414\n" \
      "MOCK_PROGRAM_INPUT: log -1 --pretty=format:%cd --date=format:%G-%m-%d %H:%M:%S\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: 2019-10-22 11:18:47\n" \
      "MOCK_PROGRAM_INPUT: log -1 --pretty=format:%ae\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: wile.e.coyote@acme.com\n" \
      "MOCK_PROGRAM_INPUT: log -1 --pretty=format:%s\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: Fixed a Bug\n" \
    )

  os.mkdir("ExtraRepo2")

  with open("ExtraRepo2/.mockprogram_inout.txt", "w") as f:
    f.write(
      "MOCK_PROGRAM_INPUT: rev-parse --short HEAD\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: 50bbf3e\n" \
      "MOCK_PROGRAM_INPUT: log -1 --pretty=format:%cd --date=format:%G-%m-%d %H:%M:%S\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: 2019-10-17 16:32:15\n" \
      "MOCK_PROGRAM_INPUT: log -1 --pretty=format:%ae\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: someone@somewhere.com\n" \
      "MOCK_PROGRAM_INPUT: log -1 --pretty=format:%s\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: Did Some Work\n" \
    )


def writeGitMockProgram_base_3_2_1_repo1_0_0_0_repo2_4_0_2():

  with open(".mockprogram_inout.txt", "w") as fileHandle:
    fileHandle.write(
      "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref HEAD\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: local_branch0\n" \
      "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref --symbolic-full-name @{u}\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: origin_repo0/remote_branch0\n" \
      "MOCK_PROGRAM_INPUT: shortlog -s HEAD ^origin_repo0/remote_branch0\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: 3 some author\n" \
      "MOCK_PROGRAM_INPUT: status --porcelain\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: M  file1\n" \
      " M file2\n" \
      "?? file3\n" \
      "MOCK_PROGRAM_INPUT: -c color.status=never status\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: On branch local_branch0\n" \
      "Your branch is ahead of 'origin_repo0/remote_branch0' by 3 commits.\n" \
      )

  os.mkdir("ExtraRepo1")

  with open("ExtraRepo1/.mockprogram_inout.txt", "w") as fileHandle:
    fileHandle.write(
      "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref HEAD\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: local_branch1\n" \
      "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref --symbolic-full-name @{u}\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: origin_repo1/remote_branch1\n" \
      "MOCK_PROGRAM_INPUT: shortlog -s HEAD ^origin_repo1/remote_branch1\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: \n" \
      "MOCK_PROGRAM_INPUT: status --porcelain\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: \n" \
      )

  os.mkdir("ExtraRepo2")

  with open("ExtraRepo2/.mockprogram_inout.txt", "w") as fileHandle:
    fileHandle.write(
      "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref HEAD\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: local_branch2\n" \
      "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref --symbolic-full-name @{u}\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: origin_repo2/remote_branch2\n" \
      "MOCK_PROGRAM_INPUT: shortlog -s HEAD ^origin_repo2/remote_branch2\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: 3 some author\n" \
      "1 some other author\n" \
      "MOCK_PROGRAM_INPUT: status --porcelain\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: ??  file1\n" \
      "?? file3\n" \
      "MOCK_PROGRAM_INPUT: -c color.status=never status\n" \
      "MOCK_PROGRAM_RETURN: 0\n" \
      "MOCK_PROGRAM_OUTPUT: On branch local_branch2\n" \
      "Your branch is ahead of 'origin_repo2/remote_branch2' by 4 commits.\n" \
      )


class test_gitdist_getRepoVersionDictFromRepoVersionFileString(unittest.TestCase):


  def setUp(self):
    self.gitdistMoveToBaseDir = os.environ.get("GITDIST_MOVE_TO_BASE_DIR", "")
    os.environ["GITDIST_MOVE_TO_BASE_DIR"] = ""


  def tearDown(self):
    os.environ["GITDIST_MOVE_TO_BASE_DIR"] = self.gitdistMoveToBaseDir


  def test_repoVersionFile_withSummary_1(self):
    repoVersionDict = \
      getRepoVersionDictFromRepoVersionFileString(repoVersionFile_withSummary_1)
    expectedDict = {
      'MockTrilinos': 'sha1_1',
      'extraTrilinosRepo': 'sha1_2',
      'extraRepoOnePackage': 'sha1_3'
      }
    #print("repoVersionDict =\n" + str(repoVersionDict))
    self.assertEqual(repoVersionDict, expectedDict)


  def test_repoVersionFile_withoutSummary_1(self):
    repoVersionDict = \
      getRepoVersionDictFromRepoVersionFileString(repoVersionFile_withoutSummary_1)
    expectedDict = {
      'MockTrilinos': 'sha1_1',
      'extraRepoTwoPackages': 'sha1_2',
      'extraRepoOnePackageThreeSubpackages': 'sha1_3'
      }
    #print("repoVersionDict =\n" + str(repoVersionDict))
    self.assertEqual(repoVersionDict, expectedDict)


# ToDo: Add unit tests for requoteCmndLineArgsIntoArray!


#
# Test entire script gitdist
#


def assertContainsGitdistHelpHeader(testObj, cmndOut):
  cmndOutList = cmndOut.splitlines()
  cmndOutFirstLine = cmndOutList[0]
  cmndOutFirstLineAfterComma = cmndOutFirstLine.split(s(":"))[1].strip() 
  cmndOutFirstLineAfterComma_expected = s("gitdist [gitdist arguments] <raw-git-command> [git arguments]")
  testObj.assertEqual(cmndOutFirstLineAfterComma, cmndOutFirstLineAfterComma_expected)


def assertContainsAllGitdistHelpSections(testObj, cmndOut):
  testObj.assertEqual(
    GeneralScriptSupport.extractLinesMatchingRegex(cmndOut,"^CLONE SUBREPOSITORIES:$"), "CLONE SUBREPOSITORIES:\n")
  testObj.assertEqual(
    GeneralScriptSupport.extractLinesMatchingRegex(cmndOut,"^OVERVIEW:$"), "OVERVIEW:\n")
  testObj.assertEqual(
    GeneralScriptSupport.extractLinesMatchingRegex(cmndOut,"^REPO SELECTION AND SETUP:$"), "REPO SELECTION AND SETUP:\n")
  testObj.assertEqual(
    GeneralScriptSupport.extractLinesMatchingRegex(cmndOut,"^SUMMARY OF REPO STATUS:$"), "SUMMARY OF REPO STATUS:\n")
  testObj.assertEqual(
    GeneralScriptSupport.extractLinesMatchingRegex(cmndOut,"^REPO VERSION FILES:$"), "REPO VERSION FILES:\n")
  testObj.assertEqual(
    GeneralScriptSupport.extractLinesMatchingRegex(cmndOut,"^USEFUL ALIASES:$"), "USEFUL ALIASES:\n")
  testObj.assertEqual(
    GeneralScriptSupport.extractLinesMatchingRegex(cmndOut,"^USAGE TIPS:$"), "USAGE TIPS:\n")
  testObj.assertEqual(
    GeneralScriptSupport.extractLinesMatchingRegex(cmndOut,"^SCRIPT DEPENDENCIES:$"), "SCRIPT DEPENDENCIES:\n")
  testObj.assertEqual(
    GeneralScriptSupport.extractLinesMatchingRegex(cmndOut,"^DEFAULT BRANCH SPECIFICATION:$"), "DEFAULT BRANCH SPECIFICATION:\n")
  testObj.assertEqual(
    GeneralScriptSupport.extractLinesMatchingRegex(cmndOut,"^MOVE TO BASE DIRECTORY:$"), "MOVE TO BASE DIRECTORY:\n")
  testObj.assertEqual(
    GeneralScriptSupport.extractLinesMatchingRegex(cmndOut,"^REPO VERSION TABLE:$"), "REPO VERSION TABLE:\n")


class test_gitdist(unittest.TestCase):


  def setUp(self):
    self.gitdistMoveToBaseDir = os.environ.get("GITDIST_MOVE_TO_BASE_DIR", "")
    os.environ["GITDIST_MOVE_TO_BASE_DIR"] = ""
    self.gitdistUnitTestSttySize = os.environ.get(
      "GITDIST_UNIT_TEST_STTY_SIZE", ""
    )
    os.environ["GITDIST_UNIT_TEST_STTY_SIZE"] = "60 120"


  def tearDown(self):
    os.environ["GITDIST_MOVE_TO_BASE_DIR"] = self.gitdistMoveToBaseDir
    os.environ["GITDIST_UNIT_TEST_STTY_SIZE"] = self.gitdistUnitTestSttySize


  def test_default(self):
    (cmndOut, errOut) = getCmndOutput(gitdistPathNoColor, rtnCode=True)
    cmndOut_expected = "Must specify git command. See 'git --help' for options.\n"
    self.assertEqual(s(cmndOut), s(cmndOut_expected))
    self.assertEqual(errOut, 1)


  # Make sure the default --help shows the section "OVERVIEW"
  def test_help(self):
    cmndOut = getCmndOutput(gitdistPath+" --help")
    assertContainsGitdistHelpHeader(self, cmndOut)
    self.assertEqual(
      GeneralScriptSupport.extractLinesMatchingRegex(cmndOut,"^OVERVIEW:$"), "")
    self.assertEqual(
      GeneralScriptSupport.extractLinesMatchingRegex(cmndOut,"^REPO SELECTION AND SETUP:$"), "")
  def test_short_help(self):
    cmndOut = getCmndOutput(gitdistPath+" -h")
    assertContainsGitdistHelpHeader(self, cmndOut)
    self.assertEqual(
      GeneralScriptSupport.extractLinesMatchingRegex(cmndOut,"^OVERVIEW:$"), "")
    self.assertEqual(
      GeneralScriptSupport.extractLinesMatchingRegex(cmndOut,"^REPO SELECTION AND SETUP:$"), "")


  # Make sure --dist-help= does not print OVERVIEW section
  def test_dist_help_none_help(self):
    cmndOut = getCmndOutput(gitdistPath+" --dist-help= --help")
    assertContainsGitdistHelpHeader(self, cmndOut)
    self.assertEqual(
      GeneralScriptSupport.extractLinesMatchingRegex(cmndOut,"^OVERVIEW:$"), "")
    self.assertEqual(
      GeneralScriptSupport.extractLinesMatchingRegex(cmndOut,"^Options:$"), "Options:\n")


  # --dist-help=aliases --help
  def test_dist_help_aliases_help(self):
    cmndOut = getCmndOutput(gitdistPath+" --dist-help=aliases --help")
    assertContainsGitdistHelpHeader(self, cmndOut)
    self.assertEqual(
      GeneralScriptSupport.extractLinesMatchingRegex(cmndOut,"^USEFUL ALIASES:$"), "USEFUL ALIASES:\n")
    self.assertEqual(
      GeneralScriptSupport.extractLinesMatchingRegex(cmndOut,"^REPO SELECTION AND SETUP:$"), "")


  # Make sure --dist-help=all prints all the topic headers
  def test_dist_help_all_help(self):
    cmndOut = getCmndOutput(gitdistPath+" --dist-help=all --help")
    assertContainsGitdistHelpHeader(self, cmndOut)
    assertContainsAllGitdistHelpSections(self, cmndOut)


  # Test that --dist-help --help prints nice error message
  def test_dist_help_help(self):
    cmndOut = getCmndOutput(gitdistPath+" --dist-help --help")
    cmndOut_expected = "gitdist: error: option --dist-help: invalid choice: '--help' (choose from '', 'overview', 'repo-selection-and-setup', 'dist-clone-subrepos', 'dist-repo-status', 'repo-versions', 'dist-repo-versions-table', 'aliases', 'default-branch', 'move-to-base-dir', 'usage-tips', 'script-dependencies', 'all')\n"
    self.assertEqual(s(cmndOut), s(cmndOut_expected))


  # Test --dist-helps=invalid-pick picked up as invalid value.
  def test_dist_help_invalid_pick_help(self):
    cmndOut = getCmndOutput(gitdistPath+" --dist-help=invalid-pick --help")
    assertContainsGitdistHelpHeader(self, cmndOut)
    errorToFind = "gitdist: error: option --dist-help: invalid choice: 'invalid-pick' (choose from '', 'overview', 'repo-selection-and-setup', 'dist-clone-subrepos', 'dist-repo-status', 'repo-versions', 'dist-repo-versions-table', 'aliases', 'default-branch', 'move-to-base-dir', 'usage-tips', 'script-dependencies', 'all')"
    self.assertEqual(
      GeneralScriptSupport.extractLinesMatchingSubstr(cmndOut,errorToFind), errorToFind+"\n")


  # Test --dist-help (show error string)
  def test_dist_help(self):
    (cmndOut, errOut) = getCmndOutput(gitdistPath+" --dist-help", rtnCode=True)
    if sys.version_info < (3,):
      anOrOne = "an"
    else:
      anOrOne = "1"
    self.assertEqual(
      s(cmndOut), s("gitdist: error: --dist-help option requires "+anOrOne+" argument\n"))
    self.assertEqual(errOut, 2)


  # Test --dist-help= (show no-op string)
  def test_dist_help_none(self):
    (cmndOut, errOut) = getCmndOutput(gitdistPathNoColor+" --dist-help=", rtnCode=True)
    self.assertEqual(
      s(cmndOut), s("Must specify git command. See 'git --help' for options.\n"))
    self.assertEqual(errOut, 1)


  # Test --dist-help=overview
  def test_dist_help_overview(self):
    cmndOut = getCmndOutput(gitdistPath+" --dist-help=overview")
    self.assertEqual(
      GeneralScriptSupport.extractLinesMatchingRegex(cmndOut,"^OVERVIEW:$"), "OVERVIEW:\n")
    self.assertEqual(
      GeneralScriptSupport.extractLinesMatchingRegex(cmndOut,"^Options:$"), "")


  # Test --dist-help=usage-tips
  def test_dist_help_usage_tips(self):
    cmndOut = getCmndOutput(gitdistPath+" --dist-help=usage-tips")
    self.assertEqual(
      GeneralScriptSupport.extractLinesMatchingRegex(cmndOut,"^USAGE TIPS:$"), "USAGE TIPS:\n")
    self.assertEqual(
      GeneralScriptSupport.extractLinesMatchingRegex(cmndOut,"^Options:$"), "")


  # Test --dist-help=all
  def test_dist_help_all(self):
    cmndOut = getCmndOutput(gitdistPath+" --dist-help=all")
    assertContainsAllGitdistHelpSections(self, cmndOut)
    self.assertEqual(
      GeneralScriptSupport.extractLinesMatchingRegex(cmndOut,"^Options:$"), "")


  def test_noEgGit(self):
    (cmndOut, errOut) = getCmndOutput(gitdistPathNoColor+" --dist-use-git= log",
      rtnCode=True)
    cmndOut_expected = "Can't find git, please set --dist-use-git\n"
    self.assertEqual(s(cmndOut), s(cmndOut_expected))
    self.assertEqual(errOut, 1)


  def test_log_args(self):
    cmndOut = getCmndOutputInMockProjectDir(gitdistPathMock+" log HEAD -1")
    cmndOut_expected = \
      "\n*** Base Git Repo: MockTrilinos\n" \
      "['mockgit', '-c', 'color.status=never', 'log', 'HEAD', '-1']\n\n"
    self.assertEqual(s(cmndOut), s(cmndOut_expected))


  def test_dot_gitdist(self):
    os.chdir(testBaseDir)
    try:

      # Create a mock git meta-project

      testDir = createAndMoveIntoTestDir("gitdist_dot_gitdist")

      os.mkdir("ExtraRepo1")
      os.makedirs("Path/To/ExtraRepo2")
      os.mkdir("ExtraRepo3")

      # Make sure .gitdist.default is found and read correctly
      with open(".gitdist.default", "w") as fileHandle:
        fileHandle.write(
          ".\n" \
          "ExtraRepo1\n" \
          "Path/To/ExtraRepo2\n" \
          "MissingExtraRep\n" \
          "ExtraRepo3\n"
          )
      cmndOut = GeneralScriptSupport.getCmndOutput(gitdistPathMock+" status",
        workingDir=testDir)
      cmndOut_expected = \
        "\n*** Base Git Repo: MockProjectDir\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n" \
        "*** Git Repo: ExtraRepo1\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n" \
        "*** Git Repo: Path/To/ExtraRepo2\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n" \
        "*** Git Repo: ExtraRepo3\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n"
      self.assertEqual(s(cmndOut), s(cmndOut_expected))
      # NOTE: Above ensures that all of the paths are read correctly and that
      # missing paths (MissingExtraRepo) are ignored.

      # Make sure that .gitdist overrides .gitdist.default
      with open(".gitdist", "w") as fileHandle:
        fileHandle.write(
          ".\n" \
          "ExtraRepo1\n" \
          "\n" \
          "   \n" \
          "ExtraRepo3\n" \
          "\n"
          )
      cmndOut = GeneralScriptSupport.getCmndOutput(gitdistPathMock+" status",
        workingDir=testDir)
      cmndOut_expected = \
        "\n*** Base Git Repo: MockProjectDir\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n" \
        "*** Git Repo: ExtraRepo1\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n" \
        "*** Git Repo: ExtraRepo3\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n"
      self.assertEqual(s(cmndOut), s(cmndOut_expected))

      # Make sure that --dist-repos overrides all files
      cmndOut = GeneralScriptSupport.getCmndOutput(
        gitdistPathMock+" --dist-repos=.,ExtraRepo1,Path/To/ExtraRepo2 status",
        workingDir=testDir)
      cmndOut_expected = \
        "\n*** Base Git Repo: MockProjectDir\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n" \
        "*** Git Repo: ExtraRepo1\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n" \
        "*** Git Repo: Path/To/ExtraRepo2\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n"
      self.assertEqual(s(cmndOut), s(cmndOut_expected))

    finally:
      os.chdir(testBaseDir)
    

  def test_log_args_extra_repo_1(self):
    cmndOut = getCmndOutputInMockProjectDir(
      gitdistPathMock+" --dist-repos=.,extraTrilinosRepo log HEAD -1")
    cmndOut_expected = \
      "\n*** Base Git Repo: MockTrilinos\n" \
      "['mockgit', '-c', 'color.status=never', 'log', 'HEAD', '-1']\n\n" \
      "*** Git Repo: extraTrilinosRepo\n" \
      "['mockgit', '-c', 'color.status=never', 'log', 'HEAD', '-1']\n\n"
    self.assertEqual(s(cmndOut), s(cmndOut_expected))


  def test_log_args_extra_repo_2_not_first(self):
    cmndOut = getCmndOutputInMockProjectDir(
      gitdistPathMock+\
        " --dist-repos=.,extraTrilinosRepo,extraRepoOnePackage "+\
        " --dist-not-repos=extraTrilinosRepo "+\
        " log HEAD -1"
      )
    cmndOut_expected = \
      "\n*** Base Git Repo: MockTrilinos\n" \
      "['mockgit', '-c', 'color.status=never', 'log', 'HEAD', '-1']\n\n" \
      "*** Git Repo: extraRepoOnePackage\n" \
      "['mockgit', '-c', 'color.status=never', 'log', 'HEAD', '-1']\n\n"
    self.assertEqual(s(cmndOut), s(cmndOut_expected))


  def test_log_args_extra_repo_2_not_second(self):
    cmndOut = getCmndOutputInMockProjectDir(
      gitdistPathMock+\
        " --dist-repos=.,extraTrilinosRepo,extraRepoOnePackage "+\
        " --dist-not-repos=extraTrilinosRepo "+\
        " log HEAD -1"
      )
    cmndOut_expected = \
      "\n*** Base Git Repo: MockTrilinos\n" \
      "['mockgit', '-c', 'color.status=never', 'log', 'HEAD', '-1']\n\n" \
      "*** Git Repo: extraRepoOnePackage\n" \
      "['mockgit', '-c', 'color.status=never', 'log', 'HEAD', '-1']\n\n"
    self.assertEqual(s(cmndOut), s(cmndOut_expected))


  def test_log_args_extra_repo_1_not_base(self):
    cmndOut = getCmndOutputInMockProjectDir(
      gitdistPathMock+\
        " --dist-repos=.,extraTrilinosRepo "+\
        " --dist-not-repos=. "+\
        " log HEAD -1"
      )
    cmndOut_expected = \
      "\n*** Git Repo: extraTrilinosRepo\n" \
      "['mockgit', '-c', 'color.status=never', 'log', 'HEAD', '-1']\n\n"
    self.assertEqual(s(cmndOut), s(cmndOut_expected))


  def test_dist_mod_only_1_change_base(self):
    os.chdir(testBaseDir)
    try:

      # Create a mock git meta-project

      testDir = createAndMoveIntoTestDir("gitdist_dist_mod_only_1_change_base")

      os.mkdir("ExtraRepo1")
      os.mkdir("ExtraRepo2")

      with open(".mockprogram_inout.txt", "w") as fileHandle:
        fileHandle.write(
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref HEAD\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: local_branch0\n" \
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref --symbolic-full-name @{u}\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: origin_repo0/remote_branch0\n" \
          "MOCK_PROGRAM_INPUT: shortlog -s HEAD ^origin_repo0/remote_branch0\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: 3 some author\n" \
          "MOCK_PROGRAM_INPUT: status --porcelain\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: M  file1\n" \
          "MOCK_PROGRAM_INPUT: -c color.status=never status\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: On branch local_branch0\n" \
          "Your branch is ahead of 'origin_repo0/remote_branch0' by 3 commits.\n" \
          )

      with open("ExtraRepo1/.mockprogram_inout.txt", "w") as fileHandle:
        fileHandle.write(
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref HEAD\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: local_branch1\n" \
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref --symbolic-full-name @{u}\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: origin_repo1/remote_branch1\n" \
          "MOCK_PROGRAM_INPUT: shortlog -s HEAD ^origin_repo1/remote_branch1\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: \n" \
          "MOCK_PROGRAM_INPUT: status --porcelain\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: \n" \
          )

      with open("ExtraRepo2/.mockprogram_inout.txt", "w") as fileHandle:
        fileHandle.write(
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref HEAD\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: local_branch2\n" \
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref --symbolic-full-name @{u}\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: origin_repo2/remote_branch2\n" \
          "MOCK_PROGRAM_INPUT: shortlog -s HEAD ^origin_repo2/remote_branch2\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: \n" \
          "MOCK_PROGRAM_INPUT: status --porcelain\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: \n" \
          )

      cmndOut = GeneralScriptSupport.getCmndOutput(
        gitdistPath + " --dist-no-color --dist-use-git="+mockGitPath \
          +" --dist-mod-only --dist-repos=.,ExtraRepo1,ExtraRepo2 status",
        workingDir=testDir)
      cmndOut_expected = \
        "\n*** Base Git Repo: MockProjectDir\n" \
        "On branch local_branch0\n" \
        "Your branch is ahead of 'origin_repo0/remote_branch0' by 3 commits.\n\n\n"
      self.assertEqual(s(cmndOut), s(cmndOut_expected))

    finally:
      os.chdir(testBaseDir)


  def test_dist_mod_only_1_change_extrarepo1(self):
    os.chdir(testBaseDir)
    try:

      # Create a mock git meta-project

      testDir = createAndMoveIntoTestDir("gitdist_dist_mod_only_1_change_extrarepo1")

      os.mkdir("ExtraRepo1")
      os.mkdir("ExtraRepo2")

      with open(".mockprogram_inout.txt", "w") as fileHandle:
        fileHandle.write(
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref HEAD\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: local_branch0\n" \
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref --symbolic-full-name @{u}\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: origin_repo0/remote_branch0\n" \
          "MOCK_PROGRAM_INPUT: shortlog -s HEAD ^origin_repo0/remote_branch0\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: \n" \
          "MOCK_PROGRAM_INPUT: status --porcelain\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: \n" \
          )

      with open("ExtraRepo1/.mockprogram_inout.txt", "w") as fileHandle:
        fileHandle.write(
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref HEAD\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: local_branch1\n" \
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref --symbolic-full-name @{u}\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: origin_repo1/remote_branch1\n" \
          "MOCK_PROGRAM_INPUT: shortlog -s HEAD ^origin_repo1/remote_branch1\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: 1 some author\n" \
          "MOCK_PROGRAM_INPUT: status --porcelain\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: \n" \
          "MOCK_PROGRAM_INPUT: -c color.status=never status\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: On branch local_branch1\n" \
          "Your branch is ahead of 'origin_repo1/remote_branch1' by 1 commits.\n" \
          )

      with open("ExtraRepo2/.mockprogram_inout.txt", "w") as fileHandle:
        fileHandle.write(
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref HEAD\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: local_branch2\n" \
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref --symbolic-full-name @{u}\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: origin_repo2/remote_branch2\n" \
          "MOCK_PROGRAM_INPUT: shortlog -s HEAD ^origin_repo2/remote_branch2\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: \n" \
          "MOCK_PROGRAM_INPUT: status --porcelain\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: \n" \
          )

      cmndOut = GeneralScriptSupport.getCmndOutput(
        gitdistPath + " --dist-no-color --dist-use-git="+mockGitPath \
          +" --dist-mod-only --dist-repos=.,ExtraRepo1,ExtraRepo2 status",
        workingDir=testDir)
      cmndOut_expected = \
        "\n*** Git Repo: ExtraRepo1\nOn branch local_branch1\n" \
        "Your branch is ahead of 'origin_repo1/remote_branch1' by 1 commits.\n\n\n"
      self.assertEqual(s(cmndOut), s(cmndOut_expected))

    finally:
      os.chdir(testBaseDir)


  def test_dist_mod_only_1_extrarepo1_not_tracking_branch(self):
    os.chdir(testBaseDir)
    try:

      # Create a mock git meta-project

      testDir = createAndMoveIntoTestDir("dist_mod_only_1_extrarepo1_not_tracking_branch")

      os.mkdir("ExtraRepo1")

      with open(".mockprogram_inout.txt", "w") as fileHandle:
        fileHandle.write(
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref HEAD\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: local_branch0\n" \
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref --symbolic-full-name @{u}\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: origin_repo0/remote_branch0\n" \
          "MOCK_PROGRAM_INPUT: shortlog -s HEAD ^origin_repo0/remote_branch0\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: 3 some author\n" \
          "MOCK_PROGRAM_INPUT: status --porcelain\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: M  file1\n" \
          "MOCK_PROGRAM_INPUT: -c color.status=never status\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: On branch local_branch0\n" \
          "Your branch is ahead of 'origin_repo0/remote_branch0' by 3 commits.\n" \
          )

      with open("ExtraRepo1/.mockprogram_inout.txt", "w") as fileHandle:
        fileHandle.write(
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref HEAD\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: local_branch1\n" \
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref --symbolic-full-name @{u}\n" \
          "MOCK_PROGRAM_RETURN: 128\n" \
          "MOCK_PROGRAM_OUTPUT: error: No upstream branch found for ''\n" \
          "MOCK_PROGRAM_INPUT: status --porcelain\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: \n" \
          )

      cmndOut = GeneralScriptSupport.getCmndOutput(
        gitdistPath + " --dist-no-color --dist-use-git="+mockGitPath \
          +" --dist-mod-only --dist-repos=.,ExtraRepo1,ExtraRepo2 status",
        workingDir=testDir)
      cmndOut_expected = \
        "\n*** Base Git Repo: MockProjectDir\n" \
        "On branch local_branch0\n" \
        "Your branch is ahead of 'origin_repo0/remote_branch0' by 3 commits.\n\n\n"
      self.assertEqual(s(cmndOut), s(cmndOut_expected))

    finally:
      os.chdir(testBaseDir)


  def test_dist_mod_only_1_extrarepo1_not_tracking_branch_with_mods(self):
    os.chdir(testBaseDir)
    try:

      # Create a mock git meta-project

      testDir = createAndMoveIntoTestDir("dist_mod_only_1_extrarepo1_not_tracking_branch_with_mods")

      os.mkdir("ExtraRepo1")

      with open(".mockprogram_inout.txt", "w") as fileHandle:
        fileHandle.write(
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref HEAD\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: local_branch0\n" \
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref --symbolic-full-name @{u}\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: origin_repo0/remote_branch0\n" \
          "MOCK_PROGRAM_INPUT: shortlog -s HEAD ^origin_repo0/remote_branch0\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: \n" \
          "MOCK_PROGRAM_INPUT: status --porcelain\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: \n" \
          )

      with open("ExtraRepo1/.mockprogram_inout.txt", "w") as fileHandle:
        fileHandle.write(
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref HEAD\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: local_branch1\n" \
          "MOCK_PROGRAM_INPUT: rev-parse --abbrev-ref --symbolic-full-name @{u}\n" \
          "MOCK_PROGRAM_RETURN: 128\n" \
          "MOCK_PROGRAM_OUTPUT: error: No upstream branch found for ''\n" \
          "MOCK_PROGRAM_INPUT: status --porcelain\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: M  file1\n" \
          "MOCK_PROGRAM_INPUT: -c color.status=never status\n" \
          "MOCK_PROGRAM_RETURN: 0\n" \
          "MOCK_PROGRAM_OUTPUT: On branch local_branch1\n" \
          "Your branch is ahead of 'origin_repo1/remote_branch1' by 1 commits.\n" \
          )

      # Make sure that --dist-repos overrides all files
      cmndOut = GeneralScriptSupport.getCmndOutput(
        gitdistPath + " --dist-no-color --dist-use-git="+mockGitPath \
          +" --dist-mod-only --dist-repos=.,ExtraRepo1,ExtraRepo2 status",
        workingDir=testDir)
      cmndOut_expected = \
        "\n*** Git Repo: ExtraRepo1\n" \
        "On branch local_branch1\n" \
        "Your branch is ahead of 'origin_repo1/remote_branch1' by 1 commits.\n\n\n"
      self.assertEqual(s(cmndOut), s(cmndOut_expected))

    finally:
      os.chdir(testBaseDir)


  def test_log_version_file(self):
    cmndOut = getCmndOutputInMockProjectDir(
      gitdistPathMock+ \
      " --dist-version-file="+unitTestDataDir+"/versionFile_withSummary_1.txt"+\
      " log _VERSION_ --some -other args")
    cmndOut_expected = \
      "\n*** Base Git Repo: MockTrilinos\n" \
      "['mockgit', '-c', 'color.status=never', 'log', 'sha1_1', '--some', '-other', 'args']\n\n"
    self.assertEqual(s(cmndOut), s(cmndOut_expected))


  def test_log_version_file_extra_repo_1(self):
    cmndOut = getCmndOutputInMockProjectDir(
      gitdistPathMock+ \
      " --dist-version-file="+unitTestDataDir+"/versionFile_withSummary_1.txt"+ \
      " --dist-repos=.,extraTrilinosRepo"+ \
      " log _VERSION_")
    cmndOut_expected = \
      "\n*** Base Git Repo: MockTrilinos\n" \
      "['mockgit', '-c', 'color.status=never', 'log', 'sha1_1']\n" \
      "\n*** Git Repo: extraTrilinosRepo\n['mockgit', '-c', 'color.status=never', 'log', 'sha1_2']\n\n"
    self.assertEqual(s(cmndOut), s(cmndOut_expected))


  def test_log_version_file_extra_repo_2(self):
    cmndOut = getCmndOutputInMockProjectDir(
      gitdistPathMock+ \
      " --dist-version-file="+unitTestDataDir+"/versionFile_withSummary_1.txt"+ \
      " --dist-repos=.,extraRepoOnePackage,extraTrilinosRepo"+ \
      " log _VERSION_")
    cmndOut_expected = \
      "\n*** Base Git Repo: MockTrilinos\n" \
      "['mockgit', '-c', 'color.status=never', 'log', 'sha1_1']\n" \
      "\n*** Git Repo: extraRepoOnePackage\n['mockgit', '-c', 'color.status=never', 'log', 'sha1_3']\n" \
      "\n*** Git Repo: extraTrilinosRepo\n['mockgit', '-c', 'color.status=never', 'log', 'sha1_2']\n\n"
    self.assertEqual(s(cmndOut), s(cmndOut_expected))


  def test_log_HEAD_version_file_extra_repo_1(self):
    cmndOut = getCmndOutputInMockProjectDir(
      gitdistPathMock+ \
      " --dist-version-file="+unitTestDataDir+"/versionFile_withSummary_1.txt"+ \
      " --dist-repos=.,extraTrilinosRepo"+ \
      " log HEAD ^_VERSION_")
    cmndOut_expected = \
      "\n*** Base Git Repo: MockTrilinos\n" \
      "['mockgit', '-c', 'color.status=never', 'log', 'HEAD', '^sha1_1']\n" \
      "\n*** Git Repo: extraTrilinosRepo\n['mockgit', '-c', 'color.status=never', 'log', 'HEAD', '^sha1_2']\n\n"
    self.assertEqual(s(cmndOut), s(cmndOut_expected))


  def test_version_file_invalid_extra_repo(self):
    cmndOut = getCmndOutputInMockProjectDir(
      gitdistPathMock+ \
      " --dist-version-file="+unitTestDataDir+"/versionFile_withSummary_1.txt"+ \
      " --dist-repos=.,extraRepoTwoPackages"+ \
      " log _VERSION_")
    cmndOut_expected = \
      "\n*** Base Git Repo: MockTrilinos\n['mockgit', '-c', 'color.status=never', 'log', 'sha1_1']\n" \
      "\n*** Git Repo: extraRepoTwoPackages\nRepo 'extraRepoTwoPackages' is not in the list of repos ['.', 'extraRepoOnePackage', 'extraTrilinosRepo'] read in from the version file.\n"
    self.assertEqual(s(cmndOut), s(cmndOut_expected))


  def test_log_not_version_file_2(self):
    cmndOut = getCmndOutputInMockProjectDir(
      gitdistPathMock+ \
      " --dist-version-file="+unitTestDataDir+"/versionFile_withSummary_1.txt"+ \
      " --dist-version-file2="+unitTestDataDir+"/versionFile_withSummary_1_2.txt"+ \
      " log _VERSION_ ^_VERSION2_")
    cmndOut_expected = \
      "\n*** Base Git Repo: MockTrilinos\n" \
      "['mockgit', '-c', 'color.status=never', 'log', 'sha1_1', '^sha1_1_2']\n\n"
    self.assertEqual(s(cmndOut), s(cmndOut_expected))


  def test_log_not_version_file_2_extra_repo_1(self):
    cmndOut = getCmndOutputInMockProjectDir(
      gitdistPathMock+ \
      " --dist-version-file="+unitTestDataDir+"/versionFile_withSummary_1.txt"+ \
      " --dist-version-file2="+unitTestDataDir+"/versionFile_withSummary_1_2.txt"+ \
      " --dist-repos=.,extraTrilinosRepo"+ \
      " log _VERSION_ ^_VERSION2_")
    cmndOut_expected = \
      "\n*** Base Git Repo: MockTrilinos\n" \
      "['mockgit', '-c', 'color.status=never', 'log', 'sha1_1', '^sha1_1_2']\n" \
      "\n*** Git Repo: extraTrilinosRepo\n['mockgit', '-c', 'color.status=never', 'log', 'sha1_2', '^sha1_2_2']\n\n"
    self.assertEqual(s(cmndOut), s(cmndOut_expected))


  def test_log_since_until_version_file_2_extra_repo_1(self):
    cmndOut = getCmndOutputInMockProjectDir(
      gitdistPathMock+ \
      " --dist-version-file="+unitTestDataDir+"/versionFile_withSummary_1.txt"+ \
      " --dist-version-file2="+unitTestDataDir+"/versionFile_withSummary_1_2.txt"+ \
      " --dist-repos=.,extraTrilinosRepo"+ \
      " log _VERSION2_.._VERSION_")
    cmndOut_expected = \
      "\n*** Base Git Repo: MockTrilinos\n" \
      "['mockgit', '-c', 'color.status=never', 'log', 'sha1_1_2..sha1_1']\n" \
      "\n*** Git Repo: extraTrilinosRepo\n['mockgit', '-c', 'color.status=never', 'log', 'sha1_2_2..sha1_2']\n\n"
    self.assertEqual(s(cmndOut), s(cmndOut_expected))
  # The above test ensures that it repalces the SHA1s for in the same cmndline args


  def test_dist_repo_status_all(self):
    os.chdir(testBaseDir)
    try:

      # Create a mock git meta-project

      testDir = createAndMoveIntoTestDir("gitdist_dist_repo_status_all")

      writeGitMockProgram_base_3_2_1_repo1_22_0_2_repo2_0_0_0()

      cmndOut = GeneralScriptSupport.getCmndOutput(
        gitdistPath + " --dist-no-color --dist-use-git="+mockGitPath \
          +" --dist-repos=.,ExtraRepo1,ExtraRepo2 dist-repo-status",
        workingDir=testDir)
      #print(cmndOut)
      cmndOut_expected = \
        "-----------------------------------------------------------------------------------------\n" \
        "| ID | Repo Dir              | Branch        | Tracking Branch             | C  | M | ? |\n" \
        "|----|-----------------------|---------------|-----------------------------|----|---|---|\n" \
        "|  0 | MockProjectDir (Base) | local_branch0 | origin_repo0/remote_branch0 |  3 | 2 | 1 |\n" \
        "|  1 | ExtraRepo1            | local_branch1 | origin_repo1/remote_branch1 | 22 |   | 1 |\n" \
        "|  2 | ExtraRepo2            | local_branch2 | origin_repo2/remote_branch2 |    |   |   |\n" \
        "-----------------------------------------------------------------------------------------\n" \
        "\n" \
        "(tip: to see a legend, pass in --dist-legend.)\n"
      self.assertEqual(s(cmndOut), s(cmndOut_expected))

    finally:
      os.chdir(testBaseDir)


  def test_dist_repo_status_all_with_sha1(self):
    os.chdir(testBaseDir)
    try:

      # Create a mock git meta-project

      testDir = createAndMoveIntoTestDir("gitdist_dist_repo_status_all")

      writeGitMockProgram_base_3_2_1_repo1_22_0_2_repo2_sha1_0_0_0()

      cmndOut = GeneralScriptSupport.getCmndOutput(
        gitdistPath + " --dist-no-color --dist-use-git="+mockGitPath \
          +" --dist-repos=.,ExtraRepo1,ExtraRepo2 dist-repo-status",
        workingDir=testDir)
      cmndOut_expected = \
        "-----------------------------------------------------------------------------------------\n" \
        "| ID | Repo Dir              | Branch        | Tracking Branch             | C  | M | ? |\n" \
        "|----|-----------------------|---------------|-----------------------------|----|---|---|\n" \
        "|  0 | MockProjectDir (Base) | local_branch0 | origin_repo0/remote_branch0 |  3 | 2 | 1 |\n" \
        "|  1 | ExtraRepo1            | local_branch1 | origin_repo1/remote_branch1 | 22 |   | 1 |\n" \
        "|  2 | ExtraRepo2            | 1235abcd      |                             |    |   |   |\n" \
        "-----------------------------------------------------------------------------------------\n" \
        "\n" \
        "(tip: to see a legend, pass in --dist-legend.)\n"
      self.maxDiff = None
      self.assertEqual(s(cmndOut), s(cmndOut_expected))

    finally:
      os.chdir(testBaseDir)


  def test_dist_repo_versions_table(self):
    os.chdir(testBaseDir)
    try:

      # Create a mock git meta-project

      testDir = createAndMoveIntoTestDir("gitdist_dist_repo_versions_table")

      writeGitMockProgram_dist_repo_versions_table()

      cmndOut = GeneralScriptSupport.getCmndOutput(
        gitdistPath + " --dist-use-git=" + mockGitPath \
          + " --dist-repos=.,ExtraRepo1,ExtraRepo2 dist-repo-versions-table",
        workingDir=testDir)
      #print(cmndOut.decode("ascii"))
      cmndOut_expected = \
        "| Repository     | SHA1    | Commit Date         | Author                 | Summary                                        |\n" \
        "|:-------------- |:-------:|:------------------- |:---------------------- |:---------------------------------------------- |\n" \
        "| MockProjectDir | e2dc488 | 2019-10-23 10:16:07 | user@domain.com        | Merge Pull Request #1234 from user/repo/branch |\n" \
        "| ExtraRepo1     | f671414 | 2019-10-22 11:18:47 | wile.e.coyote@acme.com | Fixed a Bug                                    |\n" \
        "| ExtraRepo2     | 50bbf3e | 2019-10-17 16:32:15 | someone@somewhere.com  | Did Some Work                                  |\n"
      self.assertEqual(s(cmndOut), s(cmndOut_expected))

    finally:
      os.chdir(testBaseDir)


  def test_dist_repo_versions_table_1_change_base(self):
    os.chdir(testBaseDir)
    try:

      # Create a mock git meta-project

      testDir = createAndMoveIntoTestDir(
        "gitdist_dist_repo_versions_table_1_change_base")

      writeGitMockProgram_dist_repo_versions_table_1_change_base()

      cmndOut = GeneralScriptSupport.getCmndOutput(
        gitdistPath + " --dist-use-git=" + mockGitPath \
          + " --dist-repos=.,ExtraRepo1,ExtraRepo2 dist-repo-versions-table"
          + " --dist-mod-only",
        workingDir=testDir)
      #print(cmndOut.decode("ascii"))
      cmndOut_expected = \
        "| Repository     | SHA1    | Commit Date         | Author          | Summary                                        |\n" \
        "|:-------------- |:-------:|:------------------- |:--------------- |:---------------------------------------------- |\n" \
        "| MockProjectDir | e2dc488 | 2019-10-23 10:16:07 | user@domain.com | Merge Pull Request #1234 from user/repo/branch |\n"
      self.assertEqual(s(cmndOut), s(cmndOut_expected))

    finally:
      os.chdir(testBaseDir)


  def test_dist_repo_versions_short_table(self):
    os.chdir(testBaseDir)
    try:

      # Create a mock git meta-project

      testDir = createAndMoveIntoTestDir("gitdist_dist_repo_versions_short_table")

      writeGitMockProgram_dist_repo_versions_table()

      cmndOut = GeneralScriptSupport.getCmndOutput(
        gitdistPath + " --dist-use-git=" + mockGitPath \
          + " --dist-repos=.,ExtraRepo1,ExtraRepo2 dist-repo-versions-table" \
          + " --dist-short",
        workingDir=testDir)
      #print(cmndOut.decode("ascii"))
      cmndOut_expected = \
        "| Repository     | SHA1    |\n" \
        "|:-------------- |:-------:|\n" \
        "| MockProjectDir | e2dc488 |\n" \
        "| ExtraRepo1     | f671414 |\n" \
        "| ExtraRepo2     | 50bbf3e |\n"
      self.assertEqual(s(cmndOut), s(cmndOut_expected))

    finally:
      os.chdir(testBaseDir)


  def test_dist_repo_status_all_utf8(self):
    if sys.version_info < (3,):
      print("Test disabled for Python 2.")
    else:
      os.chdir(testBaseDir)
      try:

        # Create a mock git meta-project

        testDir = createAndMoveIntoTestDir("gitdist_dist_repo_status_all")

        writeGitMockProgram_base_3_2_1_repo1_22_0_2_repo2_0_0_0()

        cmndOut = GeneralScriptSupport.getCmndOutput(
          gitdistPath + " --dist-utf8-output --dist-no-color --dist-use-git=" \
            +mockGitPath \
            +" --dist-repos=.,ExtraRepo1,ExtraRepo2 dist-repo-status",
          workingDir=testDir)
        #print(cmndOut)
        cmndOut_expected = \
          "┌────┬───────────────────────┬───────────────┬─────────────────────────────┬────┬───┬───┐\n" \
          "│ ID │ Repo Dir              │ Branch        │ Tracking Branch             │ C  │ M │ ? │\n" \
          "┝━━━━┿━━━━━━━━━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┿━━━━┿━━━┿━━━┥\n" \
          "│  0 │ MockProjectDir (Base) │ local_branch0 │ origin_repo0/remote_branch0 │  3 │ 2 │ 1 │\n" \
          "│  1 │ ExtraRepo1            │ local_branch1 │ origin_repo1/remote_branch1 │ 22 │   │ 1 │\n" \
          "│  2 │ ExtraRepo2            │ local_branch2 │ origin_repo2/remote_branch2 │    │   │   │\n" \
          "└────┴───────────────────────┴───────────────┴─────────────────────────────┴────┴───┴───┘\n" \
          "\n" \
          "(tip: to see a legend, pass in --dist-legend.)\n"
        self.assertEqual(s(cmndOut), s(cmndOut_expected))

      finally:
        os.chdir(testBaseDir)


  def test_dist_repo_status_mod_only_first(self):
    os.chdir(testBaseDir)
    try:

      # Create a mock git meta-project

      testDir = createAndMoveIntoTestDir("gitdist_dist_repo_status_mod_only_first")

      writeGitMockProgram_base_3_2_1_repo1_22_0_2_repo2_0_0_0()

      cmndOut = GeneralScriptSupport.getCmndOutput(
        gitdistPath + " --dist-no-color --dist-use-git="+mockGitPath \
          +" --dist-repos=.,ExtraRepo1,ExtraRepo2 --dist-mod-only dist-repo-status",
        workingDir=testDir)
      #print(cmndOut)
      cmndOut_expected = \
        "-----------------------------------------------------------------------------------------\n" \
        "| ID | Repo Dir              | Branch        | Tracking Branch             | C  | M | ? |\n" \
        "|----|-----------------------|---------------|-----------------------------|----|---|---|\n" \
        "|  0 | MockProjectDir (Base) | local_branch0 | origin_repo0/remote_branch0 |  3 | 2 | 1 |\n" \
        "|  1 | ExtraRepo1            | local_branch1 | origin_repo1/remote_branch1 | 22 |   | 1 |\n" \
        "-----------------------------------------------------------------------------------------\n" \
        "\n" \
        "(tip: to see a legend, pass in --dist-legend.)\n"
      self.assertEqual(s(cmndOut), s(cmndOut_expected))

    finally:
      os.chdir(testBaseDir)


  def test_dist_repo_status_mod_only_first_utf8(self):
    if sys.version_info < (3,):
      print("Test disabled for Python 2.")
    else:
      os.chdir(testBaseDir)
      try:

        # Create a mock git meta-project

        testDir = createAndMoveIntoTestDir("gitdist_dist_repo_status_mod_only_first")

        writeGitMockProgram_base_3_2_1_repo1_22_0_2_repo2_0_0_0()

        cmndOut = GeneralScriptSupport.getCmndOutput(
          gitdistPath + " --dist-utf8-output --dist-no-color --dist-use-git=" \
            +mockGitPath \
            +" --dist-repos=.,ExtraRepo1,ExtraRepo2 --dist-mod-only dist-repo-status",
          workingDir=testDir)
        #print(cmndOut)
        cmndOut_expected = \
          "┌────┬───────────────────────┬───────────────┬─────────────────────────────┬────┬───┬───┐\n" \
          "│ ID │ Repo Dir              │ Branch        │ Tracking Branch             │ C  │ M │ ? │\n" \
          "┝━━━━┿━━━━━━━━━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┿━━━━┿━━━┿━━━┥\n" \
          "│  0 │ MockProjectDir (Base) │ local_branch0 │ origin_repo0/remote_branch0 │  3 │ 2 │ 1 │\n" \
          "│  1 │ ExtraRepo1            │ local_branch1 │ origin_repo1/remote_branch1 │ 22 │   │ 1 │\n" \
          "└────┴───────────────────────┴───────────────┴─────────────────────────────┴────┴───┴───┘\n" \
          "\n" \
          "(tip: to see a legend, pass in --dist-legend.)\n"
        self.assertEqual(s(cmndOut), s(cmndOut_expected))

      finally:
        os.chdir(testBaseDir)


  def test_dist_repo_status_mod_only_first_legend(self):
    os.chdir(testBaseDir)
    try:

      # Create a mock git meta-project

      testDir = createAndMoveIntoTestDir("gitdist_dist_repo_status_mod_only_first_legend")

      writeGitMockProgram_base_3_2_1_repo1_22_0_2_repo2_0_0_0()

      cmndOut = GeneralScriptSupport.getCmndOutput(
        gitdistPath + " --dist-no-color --dist-use-git="+mockGitPath \
          +" --dist-repos=.,ExtraRepo1,ExtraRepo2 --dist-mod-only" \
          +" --dist-legend dist-repo-status",
        workingDir=testDir)
      #print("+++++++++\n" + cmndOut + "+++++++\n")
      cmndOut_expected = \
        "-----------------------------------------------------------------------------------------\n" \
        "| ID | Repo Dir              | Branch        | Tracking Branch             | C  | M | ? |\n" \
        "|----|-----------------------|---------------|-----------------------------|----|---|---|\n" \
        "|  0 | MockProjectDir (Base) | local_branch0 | origin_repo0/remote_branch0 |  3 | 2 | 1 |\n" \
        "|  1 | ExtraRepo1            | local_branch1 | origin_repo1/remote_branch1 | 22 |   | 1 |\n" \
        "-----------------------------------------------------------------------------------------\n" \
        "\n" \
        "Legend:\n" \
        "* ID: Repository ID, zero based (order git commands are run)\n" \
        "* Repo Dir: Relative to base repo (base repo shown first with '(Base)')\n" \
        "* Branch: Current branch, or (if detached HEAD) tag name or SHA1\n" \
        "* Tracking Branch: Tracking branch (or empty if no tracking branch exists)\n" \
        "* C: Number local commits w.r.t. tracking branch (empty if zero or no TB)\n" \
        "* M: Number of tracked modified (uncommitted) files (empty if zero)\n" \
        "* ?: Number of untracked, non-ignored files (empty if zero)\n\n"
      self.maxDiff = None
      self.assertEqual(s(cmndOut), s(cmndOut_expected))

    finally:
      os.chdir(testBaseDir)


  def test_dist_repo_status_mod_only_first_legend_utf8(self):
    if sys.version_info < (3,):
      print("Test disabled for Python 2.")
    else:
      os.chdir(testBaseDir)
      try:

        # Create a mock git meta-project

        testDir = \
          createAndMoveIntoTestDir("gitdist_dist_repo_status_mod_only_first_legend")

        writeGitMockProgram_base_3_2_1_repo1_22_0_2_repo2_0_0_0()

        cmndOut = GeneralScriptSupport.getCmndOutput(
          gitdistPath + " --dist-utf8-output --dist-no-color --dist-use-git=" \
            +mockGitPath \
            +" --dist-repos=.,ExtraRepo1,ExtraRepo2 --dist-mod-only" \
            +" --dist-legend dist-repo-status",
          workingDir=testDir)
        #print("+++++++++\n" + cmndOut + "+++++++\n")
        cmndOut_expected = \
          "┌────┬───────────────────────┬───────────────┬─────────────────────────────┬────┬───┬───┐\n" \
          "│ ID │ Repo Dir              │ Branch        │ Tracking Branch             │ C  │ M │ ? │\n" \
          "┝━━━━┿━━━━━━━━━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┿━━━━┿━━━┿━━━┥\n" \
          "│  0 │ MockProjectDir (Base) │ local_branch0 │ origin_repo0/remote_branch0 │  3 │ 2 │ 1 │\n" \
          "│  1 │ ExtraRepo1            │ local_branch1 │ origin_repo1/remote_branch1 │ 22 │   │ 1 │\n" \
          "└────┴───────────────────────┴───────────────┴─────────────────────────────┴────┴───┴───┘\n" \
          "\n" \
          "Legend:\n" \
          "* ID: Repository ID, zero based (order git commands are run)\n" \
          "* Repo Dir: Relative to base repo (base repo shown first with '(Base)')\n" \
          "* Branch: Current branch, or (if detached HEAD) tag name or SHA1\n" \
          "* Tracking Branch: Tracking branch (or empty if no tracking branch exists)\n" \
          "* C: Number local commits w.r.t. tracking branch (empty if zero or no TB)\n" \
          "* M: Number of tracked modified (uncommitted) files (empty if zero)\n" \
          "* ?: Number of untracked, non-ignored files (empty if zero)\n\n"
        self.maxDiff = None
        self.assertEqual(s(cmndOut), s(cmndOut_expected))

      finally:
        os.chdir(testBaseDir)


  def test_dist_repo_status_mod_only_first_last(self):
    os.chdir(testBaseDir)
    try:

      # Create a mock git meta-project

      testDir = createAndMoveIntoTestDir("gitdist_dist_repo_status_mod_only_first_last")

      writeGitMockProgram_base_3_2_1_repo1_0_0_0_repo2_4_0_2()

      cmndOut = GeneralScriptSupport.getCmndOutput(
        gitdistPath + " --dist-no-color --dist-use-git="+mockGitPath \
          +" --dist-repos=.,ExtraRepo1,ExtraRepo2 --dist-mod-only dist-repo-status",
        workingDir=testDir)
      #print(cmndOut)
      cmndOut_expected = \
        "----------------------------------------------------------------------------------------\n" \
        "| ID | Repo Dir              | Branch        | Tracking Branch             | C | M | ? |\n" \
        "|----|-----------------------|---------------|-----------------------------|---|---|---|\n" \
        "|  0 | MockProjectDir (Base) | local_branch0 | origin_repo0/remote_branch0 | 3 | 2 | 1 |\n" \
        "|  2 | ExtraRepo2            | local_branch2 | origin_repo2/remote_branch2 | 4 |   | 2 |\n" \
        "----------------------------------------------------------------------------------------\n" \
        "\n" \
        "(tip: to see a legend, pass in --dist-legend.)\n"
      self.assertEqual(s(cmndOut), s(cmndOut_expected))

    finally:
      os.chdir(testBaseDir)


  def test_dist_repo_status_mod_only_first_last_utf8(self):
    if sys.version_info < (3,):
      print("Test disabled for Python 2.")
    else:
      os.chdir(testBaseDir)
      try:

        # Create a mock git meta-project

        testDir = createAndMoveIntoTestDir("gitdist_dist_repo_status_mod_only_first_last")

        writeGitMockProgram_base_3_2_1_repo1_0_0_0_repo2_4_0_2()

        cmndOut = GeneralScriptSupport.getCmndOutput(
          gitdistPath + " --dist-utf8-output --dist-no-color --dist-use-git=" \
            +mockGitPath \
            +" --dist-repos=.,ExtraRepo1,ExtraRepo2 --dist-mod-only dist-repo-status",
          workingDir=testDir)
        #print(cmndOut)
        cmndOut_expected = \
          "┌────┬───────────────────────┬───────────────┬─────────────────────────────┬───┬───┬───┐\n" \
          "│ ID │ Repo Dir              │ Branch        │ Tracking Branch             │ C │ M │ ? │\n" \
          "┝━━━━┿━━━━━━━━━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┿━━━┿━━━┿━━━┥\n" \
          "│  0 │ MockProjectDir (Base) │ local_branch0 │ origin_repo0/remote_branch0 │ 3 │ 2 │ 1 │\n" \
          "│  2 │ ExtraRepo2            │ local_branch2 │ origin_repo2/remote_branch2 │ 4 │   │ 2 │\n" \
          "└────┴───────────────────────┴───────────────┴─────────────────────────────┴───┴───┴───┘\n" \
          "\n" \
          "(tip: to see a legend, pass in --dist-legend.)\n"
        self.assertEqual(s(cmndOut), s(cmndOut_expected))

      finally:
        os.chdir(testBaseDir)


  def test_dist_repo_status_extra_args_fail(self):
    os.chdir(testBaseDir)
    try:

      # Create a mock git meta-project

      testDir = createAndMoveIntoTestDir("dist_repo_status_extra_args_fail")

      (cmndOut, errOut) = getCmndOutput(
        gitdistPath + " --dist-no-color --dist-use-git="+mockGitPath \
          +" --dist-repos=.,ExtraRepo1,ExtraRepo2 --dist-mod-only" \
          +" --dist-legend dist-repo-status --name-status",
        rtnCode=True)
      #print(cmndOut)
      cmndOut_expected = \
        "Error, passing in extra git commands/args ='--name-status' with special command 'dist-repo-status' is not allowed!\n"
      self.assertEqual(cmndOut, s(cmndOut_expected))
      self.assertEqual(errOut, 1)

    finally:
      os.chdir(testBaseDir)


  def test_dist_repo_versions_table_extra_args_fail(self):
    os.chdir(testBaseDir)
    try:

      # Create a mock git meta-project

      testDir = createAndMoveIntoTestDir("dist_repo_versions_table_extra_args_fail")

      (cmndOut, errOut) = getCmndOutput(
        gitdistPath + " --dist-no-color --dist-use-git=" + mockGitPath \
          + " --dist-repos=.,ExtraRepo1,ExtraRepo2 dist-repo-versions-table" \
          + " --name-status",
        rtnCode=True)
      #print(cmndOut)
      cmndOut_expected = \
        "Error, passing in extra git commands/args ='--name-status' with special command 'dist-repo-versions-table' is not allowed!\n"
      self.assertEqual(cmndOut, s(cmndOut_expected))
      self.assertEqual(errOut, 1)

    finally:
      os.chdir(testBaseDir)


  def test_dist_default_branch(self):
    os.chdir(testBaseDir)
    try:

      # Create a mock git meta-project

      testDir = createAndMoveIntoTestDir("gitdist_default_branch")
      os.mkdir("ExtraRepo1")
      os.makedirs("Path/To/ExtraRepo2")
      os.mkdir("ExtraRepo3")

      # Make sure .gitdist.default is found and read correctly
      with open(".gitdist.default", "w") as fileHandle:
        fileHandle.write(
          ". master\n" \
          "ExtraRepo1 develop\n" \
          "Path/To/ExtraRepo2 app-devel\n" \
          "MissingExtraRepo\n" \
          "ExtraRepo3\n"
          )
      cmndOut = GeneralScriptSupport.getCmndOutput(
        gitdistPathMock+" checkout _DEFAULT_BRANCH_", workingDir=testDir)
      cmndOut_expected = \
        "\n*** Base Git Repo: MockProjectDir\n" \
        "['mockgit', '-c', 'color.status=never', 'checkout', 'master']\n\n" \
        "*** Git Repo: ExtraRepo1\n" \
        "['mockgit', '-c', 'color.status=never', 'checkout', 'develop']\n\n" \
        "*** Git Repo: Path/To/ExtraRepo2\n" \
        "['mockgit', '-c', 'color.status=never', 'checkout', 'app-devel']\n\n" \
        "*** Git Repo: ExtraRepo3\n" \
        "['mockgit', '-c', 'color.status=never', 'checkout', 'master']\n\n"
      self.assertEqual(s(cmndOut), s(cmndOut_expected))
      # NOTE: Above ensures that all of the paths are read correctly and that
      # missing paths (MissingExtraRepo) are ignored.

      # Make sure that .gitdist overrides .gitdist.default
      with open(".gitdist", "w") as fileHandle:
        fileHandle.write(
          ". develop\n" \
          "ExtraRepo1 develop\n" \
          "ExtraRepo3 develop\n"
          )
      cmndOut = GeneralScriptSupport.getCmndOutput(
        gitdistPathMock+" checkout _DEFAULT_BRANCH_", workingDir=testDir)
      cmndOut_expected = \
        "\n*** Base Git Repo: MockProjectDir\n" \
        "['mockgit', '-c', 'color.status=never', 'checkout', 'develop']\n\n" \
        "*** Git Repo: ExtraRepo1\n" \
        "['mockgit', '-c', 'color.status=never', 'checkout', 'develop']\n\n" \
        "*** Git Repo: ExtraRepo3\n" \
        "['mockgit', '-c', 'color.status=never', 'checkout', 'develop']\n\n"
      self.assertEqual(s(cmndOut), s(cmndOut_expected))

      # Make sure that --dist-repos overrides all files
      cmndOut = GeneralScriptSupport.getCmndOutput(
        gitdistPathMock+" --dist-repos=.,ExtraRepo1,Path/To/ExtraRepo2 "+ \
        "checkout _DEFAULT_BRANCH_",
        workingDir=testDir)
      cmndOut_expected = \
        "\n*** Base Git Repo: MockProjectDir\n" \
        "['mockgit', '-c', 'color.status=never', 'checkout', 'master']\n\n" \
        "*** Git Repo: ExtraRepo1\n" \
        "['mockgit', '-c', 'color.status=never', 'checkout', 'master']\n\n" \
        "*** Git Repo: Path/To/ExtraRepo2\n" \
        "['mockgit', '-c', 'color.status=never', 'checkout', 'master']\n\n"
      self.assertEqual(s(cmndOut), s(cmndOut_expected))
      
    finally:
      os.chdir(testBaseDir)


  def test_gitdist_move_to_base_dir_invalid_env_var(self):
    os.environ["GITDIST_MOVE_TO_BASE_DIR"] = "INVALID"
    cmndOut = getCmndOutput(gitdistPath+" status")
    cmndOut_expected = "Error, env var GITDIST_MOVE_TO_BASE_DIR='INVALID' is invalid!  Valid choices include empty '', IMMEDIATE_BASE, and EXTREME_BASE.\n"
    #print("cmndOut = ", cmndOut)
    #print("cmndOut_expected = ", cmndOut_expected)
    self.assertEqual(s(cmndOut), s(cmndOut_expected))


  def test_gitdist_move_to_base_dir(self):
    os.chdir(testBaseDir)
    try:

      # Create a mock git meta-project.
      testDir = createAndMoveIntoTestDir("gitdist_move_to_base_dir")
      os.makedirs("ExtraRepo/path/to/somewhere")
      with open(".gitdist", "w") as fileHandle:
        fileHandle.write(
          ".\n" \
          "ExtraRepo\n"
          )
      with open("ExtraRepo/.gitdist", "w") as fileHandle:
        fileHandle.write(
          ".\n"
          )
      os.chdir("ExtraRepo/path/to/somewhere")

      # Test with the default setting.
      os.environ["GITDIST_MOVE_TO_BASE_DIR"] = ""
      cmndOut = GeneralScriptSupport.getCmndOutput(gitdistPathMock+" status")
      cmndOut_expected = \
        "\n*** Base Git Repo: somewhere\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n"
      self.assertEqual(s(cmndOut), s(cmndOut_expected))

      # Test moving up the directory tree until we find a .gitdist file.
      os.environ["GITDIST_MOVE_TO_BASE_DIR"] = "IMMEDIATE_BASE"
      cmndOut = GeneralScriptSupport.getCmndOutput(gitdistPathMock+" status")
      cmndOut_expected = \
        "\n*** Base Git Repo: ExtraRepo\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n"
      self.assertEqual(s(cmndOut), s(cmndOut_expected))

      # Test moving up the directory tree until we find the outer-most .gitdist
      # file.
      os.environ["GITDIST_MOVE_TO_BASE_DIR"] = "EXTREME_BASE"
      cmndOut = GeneralScriptSupport.getCmndOutput(gitdistPathMock+" status")
      cmndOut_expected = \
        "\n*** Base Git Repo: MockProjectDir\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n" \
        "*** Git Repo: ExtraRepo\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n"
      self.assertEqual(s(cmndOut), s(cmndOut_expected))
      
      # Rename the .gitdist files .gitdist.default, and try the tests again.
      os.rename("../../../.gitdist", "../../../.gitdist.default")
      os.rename("../../../../.gitdist", "../../../../.gitdist.default")

      # Test with the default setting.
      os.environ["GITDIST_MOVE_TO_BASE_DIR"] = ""
      cmndOut = GeneralScriptSupport.getCmndOutput(gitdistPathMock+" status")
      cmndOut_expected = \
        "\n*** Base Git Repo: somewhere\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n"
      self.assertEqual(s(cmndOut), s(cmndOut_expected))

      # Test moving up the directory tree until we find a .gitdist file.
      os.environ["GITDIST_MOVE_TO_BASE_DIR"] = "IMMEDIATE_BASE"
      cmndOut = GeneralScriptSupport.getCmndOutput(gitdistPathMock+" status")
      cmndOut_expected = \
        "\n*** Base Git Repo: ExtraRepo\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n"
      self.assertEqual(s(cmndOut), s(cmndOut_expected))

      # Test moving up the directory tree until we find the outer-most .gitdist
      # file.
      os.environ["GITDIST_MOVE_TO_BASE_DIR"] = "EXTREME_BASE"
      cmndOut = GeneralScriptSupport.getCmndOutput(gitdistPathMock+" status")
      cmndOut_expected = \
        "\n*** Base Git Repo: MockProjectDir\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n" \
        "*** Git Repo: ExtraRepo\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n"
      self.assertEqual(s(cmndOut), s(cmndOut_expected))
      
    finally:
      os.chdir(testBaseDir)


  def test_gitdist_move_to_base_dir_nested_subrepo(self):
    os.chdir(testBaseDir)
    try:

      # Create a mock git meta-project with a nested git repo that is listed
      # by both the immediate and the outer-most .gitdist files.
      testDir = createAndMoveIntoTestDir("gitdist_move_to_base_dir_nested_subrepo")
      os.makedirs("ExtraRepo/NestedRepo/doc")
      os.makedirs("ExtraRepo/NestedRepo/.git")
      with open(".gitdist", "w") as fileHandle:
        fileHandle.write(
          ".\n" \
          "ExtraRepo\n" \
          "ExtraRepo/NestedRepo\n"
          )
      with open("ExtraRepo/.gitdist.default", "w") as fileHandle:
        fileHandle.write(
          ".\n" \
          "NestedRepo\n"
          )
      os.chdir("ExtraRepo/NestedRepo/doc")

      os.environ["GITDIST_MOVE_TO_BASE_DIR"] = "IMMEDIATE_BASE"
      cmndOut = GeneralScriptSupport.getCmndOutput(gitdistPathMock+" status")
      cmndOut_expected = \
        "\n*** Base Git Repo: ExtraRepo\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n" \
        "*** Git Repo: NestedRepo\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n"
      self.assertEqual(s(cmndOut), s(cmndOut_expected))

      os.environ["GITDIST_MOVE_TO_BASE_DIR"] = "EXTREME_BASE"
      cmndOut = GeneralScriptSupport.getCmndOutput(gitdistPathMock+" status")
      cmndOut_expected = \
        "\n*** Base Git Repo: MockProjectDir\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n" \
        "*** Git Repo: ExtraRepo\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n" \
        "*** Git Repo: ExtraRepo/NestedRepo\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n"
      self.assertEqual(s(cmndOut), s(cmndOut_expected))

    finally:
      os.chdir(testBaseDir)


  def test_gitdist_move_to_base_dir_nested_subrepo_logical_pwd(self):
    os.chdir(testBaseDir)
    try:

      # Create a mock meta-project where the current subrepo is reached through
      # a symlink.  This covers the case where os.getcwd() returns the physical
      # path but PWD contains the logical path with the outer .gitdist file.
      testDir = createAndMoveIntoTestDir(
        "gitdist_move_to_base_dir_nested_subrepo_logical_pwd")
      os.makedirs("../RealExtraRepo/NestedRepo/doc")
      os.makedirs("../RealExtraRepo/NestedRepo/.git")
      os.symlink("../RealExtraRepo", "ExtraRepo")
      with open(".gitdist", "w") as fileHandle:
        fileHandle.write(
          ".\n" \
          "ExtraRepo\n" \
          "ExtraRepo/NestedRepo\n"
          )
      with open("ExtraRepo/.gitdist.default", "w") as fileHandle:
        fileHandle.write(
          ".\n" \
          "NestedRepo\n"
          )
      logicalCwd = os.path.join(testDir, "ExtraRepo", "NestedRepo", "doc")
      os.chdir(logicalCwd)
      os.environ["PWD"] = logicalCwd

      os.environ["GITDIST_MOVE_TO_BASE_DIR"] = "EXTREME_BASE"
      cmndOut = GeneralScriptSupport.getCmndOutput(gitdistPathMock+" status")
      cmndOut_expected = \
        "\n*** Base Git Repo: MockProjectDir\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n" \
        "*** Git Repo: ExtraRepo\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n" \
        "*** Git Repo: ExtraRepo/NestedRepo\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n"
      self.assertEqual(s(cmndOut), s(cmndOut_expected))

    finally:
      os.chdir(testBaseDir)


  def test_gitdist_move_to_base_dir_inside_git_repo_below_nonbase_gitdist(self):
    os.chdir(testBaseDir)
    try:

      # Create a mock git repo with an intermediate .gitdist that does not
      # describe the current base repo.  IMMEDIATE_BASE should keep walking up
      # to the git repo root and use the .gitdist file there.
      testDir = createAndMoveIntoTestDir(
        "gitdist_move_to_base_dir_inside_git_repo_below_nonbase_gitdist")
      os.makedirs(".git")
      os.makedirs("ExtraRepo")
      os.makedirs("path/to/intermediate/working/dir")
      with open(".gitdist", "w") as fileHandle:
        fileHandle.write(
          ".\n" \
          "ExtraRepo\n"
          )
      with open("path/to/intermediate/.gitdist", "w") as fileHandle:
        fileHandle.write(
          "SomeOtherRepo\n"
          )
      os.chdir("path/to/intermediate/working/dir")

      os.environ["GITDIST_MOVE_TO_BASE_DIR"] = "IMMEDIATE_BASE"
      cmndOut = GeneralScriptSupport.getCmndOutput(gitdistPathMock+" status")
      cmndOut_expected = \
        "\n*** Base Git Repo: MockProjectDir\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n" \
        "*** Git Repo: ExtraRepo\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n"
      self.assertEqual(s(cmndOut), s(cmndOut_expected))

    finally:
      os.chdir(testBaseDir)


  def test_gitdist_move_to_base_dir_no_dist_gitdist_file(self):
    os.chdir(testBaseDir)
    try:

      # Create a mock git meta-project but with no .gitdist[.default] files!
      testDir = createAndMoveIntoTestDir("gitdist_move_to_base_dir_no_dist_gitdist_file")
      os.makedirs(".git")
      os.makedirs("ExtraRepo/.git")
      os.makedirs("ExtraRepo/path/to/somewhere")
      os.chdir("ExtraRepo/path/to/somewhere")

      os.environ["GITDIST_MOVE_TO_BASE_DIR"] = ""
      cmndOut = GeneralScriptSupport.getCmndOutput(gitdistPathMock+" status")
      cmndOut_expected = \
        "\n*** Base Git Repo: somewhere\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n"
      self.assertEqual(s(cmndOut), s(cmndOut_expected))

      os.environ["GITDIST_MOVE_TO_BASE_DIR"] = "IMMEDIATE_BASE"
      cmndOut = GeneralScriptSupport.getCmndOutput(gitdistPathMock+" status")
      cmndOut_expected = \
        "\n*** Base Git Repo: somewhere\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n"
      self.assertEqual(s(cmndOut), s(cmndOut_expected))

      os.environ["GITDIST_MOVE_TO_BASE_DIR"] = "EXTREME_BASE"
      cmndOut = GeneralScriptSupport.getCmndOutput(gitdistPathMock+" status")
      cmndOut_expected = \
        "\n*** Base Git Repo: somewhere\n" \
        "['mockgit', '-c', 'color.status=never', 'status']\n\n"
      self.assertEqual(s(cmndOut), s(cmndOut_expected))

    finally:
      os.chdir(testBaseDir)


class test_gitdist_clone_subrepos(unittest.TestCase):

  def setUp(self):
    self.savedCwd = os.getcwd()
    self.savedEnv = dict(os.environ)
    self.testDir = tempfile.mkdtemp(prefix="gitdist-clone-", dir=self.savedCwd)
    self.base = os.path.join(self.testDir, "base")
    os.makedirs(os.path.join(self.base, ".git"))
    os.chdir(self.base)
    os.environ["PWD"] = self.base
    os.environ["GITDIST_MOVE_TO_BASE_DIR"] = ""
    os.environ.pop("GITDIST_DEBUG_OVERRIDE", None)
    self.log = os.path.join(self.testDir, "git-calls.jsonl")
    self.fakeGit = os.path.join(self.testDir, "fake git")
    self.config = {}
    # This executable never delegates to Git. Unknown commands fail closed.
    with open(self.fakeGit, "w") as script:
      script.write("#!" + sys.executable + "\n" + r'''
import json
import os
import sys
args = sys.argv[1:]
config = json.loads(os.environ['GITDIST_CLONE_TEST_CONFIG'])
with open(os.environ['GITDIST_CLONE_TEST_LOG'], 'a') as log:
  log.write(json.dumps([os.getcwd(), args]) + '\n')
key = ' '.join(args)
if key in config.get('responses', {}):
  code, output = config['responses'][key]
  sys.stdout.write(output)
  sys.exit(code)
if args == ['rev-parse', '--show-toplevel']:
  root = os.getcwd()
  while not os.path.exists(os.path.join(root, '.git')):
    parent = os.path.dirname(root)
    if parent == root:
      sys.stderr.write('not a git repository\n')
      sys.exit(128)
    root = parent
  print(root)
elif args == ['remote']:
  print(config.get('remotes', 'glex-ascdor'))
elif args == ['symbolic-ref', '--quiet', '--short', 'HEAD']:
  print(config.get('branch', 'main'))
elif args[:2] == ['config', '--get']:
  print(config.get('branchRemote', 'glex-ascdor'))
elif args[:2] == ['config', '--get-all'] and args[2].endswith('.url'):
  print(config.get('url', 'https://example.com/ascdor-open/ascdor-ai-tools.git'))
elif args[:1] == ['clone']:
  dest = args[-1]
  if dest == config.get('failClone') or dest in config.get('failClones', []):
    sys.stderr.write('simulated clone failure\n')
    sys.exit(17)
  os.makedirs(os.path.join(dest, '.git'))
  for path, kind in config.get('effects', {}).get(dest, []):
    if kind == 'directory':
      os.makedirs(path)
    elif kind == 'file':
      with open(path, 'w') as handle:
        handle.write('tracked file')
    else:
      os.symlink(kind, path)
else:
  sys.stderr.write('Unexpected fake Git command: ' + repr(args) + '\n')
  sys.exit(90)
''')
    os.chmod(self.fakeGit, 0o755)

  def tearDown(self):
    os.chdir(self.savedCwd)
    os.environ.clear()
    os.environ.update(self.savedEnv)
    shutil.rmtree(self.testDir)

  def manifest(self, contents, name=".gitdist.default"):
    with open(name, "w") as handle:
      handle.write(contents)

  def invoke(self, args=None, entryPoint="gitdist.py"):
    os.environ["GITDIST_CLONE_TEST_CONFIG"] = json.dumps(self.config)
    os.environ["GITDIST_CLONE_TEST_LOG"] = self.log
    if os.path.exists(self.log):
      os.remove(self.log)
    child = subprocess.Popen([sys.executable, os.path.join(pythonUtilsDir, entryPoint),
      "--dist-use-git=" + self.fakeGit, "--dist-no-color"] +
      (args if args is not None else ["dist-clone-subrepos"]),
      stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    out, err = child.communicate()
    self.calls = []
    if os.path.exists(self.log):
      with open(self.log) as handle:
        self.calls = [json.loads(line) for line in handle]
    self.clones = [args for cwd, args in self.calls if args[0] == "clone"]
    return child.returncode, s(out), s(err)

  def test_four_repository_example(self):
    destinations = ["ascdor-container-setup-utils", "cass-clang-metrics",
      "cass-clang-metrics/ascdor-numerical-coverage-examples",
      "cass-clang-metrics/filter-sort-list-of-dicts"]
    self.manifest(". main\n" + "".join(path + " master\n" for path in destinations))
    code, out, err = self.invoke()
    self.assertEqual((code, err), (0, ""))
    self.assertEqual(self.clones, [["clone", "-o", "glex-ascdor", "-b", "master",
      "https://example.com/ascdor-open/" + os.path.basename(path) + ".git", path]
      for path in destinations])
    self.assertTrue(all(cwd == self.base for cwd, args in self.calls))
    self.assertTrue(all(os.path.isdir(path + "/.git") for path in destinations))

  def test_four_repository_example_preserves_git_at_protocol(self):
    self.config['url'] = "git@gitlab-ex.sandia.gov:ascdor-open/ascdor-ai-tools.git"
    destinations = ["ascdor-container-setup-utils", "cass-clang-metrics",
      "cass-clang-metrics/ascdor-numerical-coverage-examples",
      "cass-clang-metrics/filter-sort-list-of-dicts"]
    self.manifest(". main\n" + "".join(path + " master\n" for path in destinations))
    expectedClones = [["clone", "-o", "glex-ascdor", "-b", "master",
      "git@gitlab-ex.sandia.gov:ascdor-open/" + os.path.basename(path) + ".git", path]
      for path in destinations]

    code, preview, err = self.invoke(["dist-clone-subrepos", "--dist-no-opt"])
    self.assertEqual((code, err), (0, ""))
    self.assertEqual(self.clones, [])
    self.assertFalse(any(os.path.exists(path) for path in destinations))
    self.assertEqual([shlex.split(line) for line in preview.splitlines()],
      [[self.fakeGit] + args for args in expectedClones])

    code, out, err = self.invoke()
    self.assertEqual((code, err), (0, ""))
    self.assertEqual(self.clones, expectedClones)
    self.assertEqual(out, preview)
    self.assertTrue(all(cwd == self.base for cwd, args in self.calls))
    self.assertTrue(all(os.path.isdir(path + "/.git") for path in destinations))

  def test_explicit_and_remote_default_branches(self):
    self.manifest("\n. main\nsubrepo1 dev\n\nsubrepo1/subrepo2\n")
    code, out, err = self.invoke()
    self.assertEqual((code, err), (0, ""))
    self.assertEqual(self.clones, [
      ["clone", "-o", "glex-ascdor", "-b", "dev",
        "https://example.com/ascdor-open/subrepo1.git", "subrepo1"],
      ["clone", "-o", "glex-ascdor",
        "https://example.com/ascdor-open/subrepo2.git", "subrepo1/subrepo2"]])

  def test_clone_parser_preserves_existing_default(self):
    self.manifest("repo\nexplicit master\nother dev\n")
    repos, branches = parseGitdistFile(".gitdist.default")
    self.assertEqual(branches, {"repo": "master", "explicit": "master", "other": "dev"})
    repos, branches = parseGitdistFile(".gitdist.default", None)
    self.assertEqual(branches, {"repo": None, "explicit": "master", "other": "dev"})


  def test_peer_url_transports_and_suffixes(self):
    cases = [
      ("https://host/team/base.git", "https://host/team/extra.git"),
      ("https://host/team/base", "https://host/team/extra.git"),
      ("http://host/deep/team/base.git/", "http://host/deep/team/extra.git"),
      ("user@host:team/base.git", "user@host:team/extra.git"),
      ("user@host:team/base/", "user@host:team/extra.git"),
      ("host:base", "host:extra.git"),
      ("ssh://user@host:2222/deep/team/base", "ssh://user@host:2222/deep/team/extra.git"),
      ("ssh://user@[::1]:2222/team/base.git", "ssh://user@[::1]:2222/team/extra.git"),
      ("user@[::1]:team/base.git", "user@[::1]:team/extra.git"),
      ("git://host/team/base.git", "git://host/team/extra.git"),
      ("file:///tmp/team/base.git", "file:///tmp/team/extra.git"),
      ("/tmp/team/base.git/", "/tmp/team/extra.git"),
      ("../team/base", "../team/extra.git"),
      ("base.git", "./extra.git"),
      ("-team/base.git", "./-team/extra.git"),
      ("https://host/team/$base;name.git", "https://host/team/extra.git")]
    for baseUrl, expected in cases:
      self.assertEqual(getClonePeerUrl(baseUrl, "different-checkout/extra"), expected)
      self.assertEqual(getClonePeerUrl(baseUrl, "extra.git"), expected)

  def test_malformed_peer_urls(self):
    for url in ["", "/", "https://host", "https:///base.git", "ext::command",
        "user@host:", "ftp://host/team/base", "https://host:bad/team/base",
        "https://host/team/base?query", "https://host/team/base#fragment", "../.."]:
      self.assertRaises(ValueError, getClonePeerUrl, url, "extra")

  def test_multiple_remotes_use_branch_config_and_first_fetch_url(self):
    self.manifest("extra\n")
    self.config.update(remotes="origin\nteam/upstream", branch="feature/topic",
      branchRemote="team/upstream", url="ssh://host:2222/team/base.git\nhttps://other/ignored.git")
    code, out, err = self.invoke()
    self.assertEqual((code, err), (0, ""))
    self.assertEqual(self.clones, [["clone", "-o", "team/upstream",
      "ssh://host:2222/team/extra.git", "extra"]])
    self.assertTrue(["config", "--get", "branch.feature/topic.remote"] in
      [args for cwd, args in self.calls])
    self.assertFalse(any("pushurl" in " ".join(args) for cwd, args in self.calls))

  def test_sole_remote_does_not_query_branch_even_when_detached(self):
    self.manifest("extra\n")
    self.config['responses'] = {"symbolic-ref --quiet --short HEAD": [1, ""]}
    code, out, err = self.invoke()
    self.assertEqual((code, err), (0, ""))
    self.assertFalse(any(args[0] == "symbolic-ref" for cwd, args in self.calls))

  def test_remote_selection_errors(self):
    self.manifest("extra\n")
    cases = [
      ({"remotes": ""}, "no configured remotes"),
      ({"remotes": "origin\nother", "branchRemote": "stale"}, "configured remote"),
      ({"remotes": "origin\nother", "branchRemote": "."}, "configured remote"),
      ({"remotes": "origin\nother", "responses": {"config --get branch.main.remote": [1, ""]}}, "configured remote"),
      ({"remotes": "origin\nother", "responses": {"symbolic-ref --quiet --short HEAD": [1, ""]}}, "Detached HEAD"),
      ({"responses": {"config --get-all remote.glex-ascdor.url": [1, ""]}}, "no fetch URL"),
      ({"url": "\nhttps://host/second.git"}, "no fetch URL"),
      ({"responses": {"remote": [128, ""]}}, "Git discovery failed"),
      ({"remotes": "origin\nother", "responses": {"config --get branch.main.remote": [128, ""]}}, "Git discovery failed"),
      ({"responses": {"config --get-all remote.glex-ascdor.url": [128, ""]}}, "Git discovery failed")]
    for config, diagnostic in cases:
      self.config = config
      code, out, err = self.invoke()
      self.assertNotEqual(code, 0)
      self.assertTrue(diagnostic in err, err)
      self.assertEqual(self.clones, [])
      self.assertFalse(os.path.exists("extra"))


  def test_manifest_precedence_and_override(self):
    self.manifest("default dev\n")
    self.manifest("chosen topic\n", ".gitdist")
    code, out, err = self.invoke(["dist-clone-subrepos", "--dist-no-opt"])
    self.assertEqual((code, err), (0, ""))
    self.assertTrue("-b topic" in out and "chosen.git" in out)
    self.assertFalse("default.git" in out)
    code, out, err = self.invoke(["dist-clone-subrepos", "--dist-repos=override"])
    self.assertEqual((code, err), (0, ""))
    self.assertEqual(self.clones[0][-1], "override")
    self.assertFalse("-b" in self.clones[0])

  def test_empty_selections_do_not_resolve_remote(self):
    self.config['remotes'] = ""
    for manifest in [None, "", "\n", ". main\n./\n"]:
      if manifest is not None:
        self.manifest(manifest)
      code, out, err = self.invoke()
      self.assertEqual((code, err), (0, ""))
      self.assertTrue("No selected subrepositories" in out)
      self.assertEqual([args for cwd, args in self.calls], [["rev-parse", "--show-toplevel"]])

  def test_explicit_empty_override_selects_nothing(self):
    self.manifest("extra\n")
    code, out, err = self.invoke(["dist-clone-subrepos", "--dist-repos="])
    self.assertEqual((code, err), (0, ""))
    self.assertEqual(self.clones, [])

  def test_normalized_exclusions_do_not_exclude_descendants(self):
    self.manifest("./parent/ dev\nparent/child\nother\n")
    code, out, err = self.invoke(["dist-clone-subrepos", "--dist-not-repos=parent/,./other/"])
    self.assertEqual((code, err), (0, ""))
    self.assertEqual([args[-1] for args in self.clones], ["parent/child"])
    self.assertFalse(os.path.exists("parent/.git"))

  def test_stable_parent_first_order(self):
    self.manifest("parent/child\nunrelated\nparent\nlast\nparent/child/grandchild\n")
    code, out, err = self.invoke()
    self.assertEqual((code, err), (0, ""))
    self.assertEqual([args[-1] for args in self.clones],
      ["unrelated", "parent", "parent/child", "last", "parent/child/grandchild"])

  def test_normalized_and_intermediate_directories(self):
    self.manifest("./a//b/./extra/ dev\n")
    code, out, err = self.invoke()
    self.assertEqual((code, err), (0, ""))
    self.assertEqual(self.clones[0][-1], "a/b/extra")
    self.assertFalse(os.path.exists("a/.git"))

  def test_invalid_paths_fail_before_any_clone(self):
    for path in ["/absolute", "../outside", "a/../outside", "extra\n./extra/", "extra\nextra"]:
      self.manifest("valid\n" + path + "\n")
      code, out, err = self.invoke()
      self.assertNotEqual(code, 0)
      self.assertTrue("path" in err or "Duplicate" in err, err)
      self.assertEqual(self.clones, [])
      self.assertFalse(os.path.exists("valid"))

  def test_symlink_escape_fails_before_any_clone(self):
    os.symlink(self.testDir, "escape")
    self.manifest("valid\nescape/extra\n")
    code, out, err = self.invoke()
    self.assertNotEqual(code, 0)
    self.assertTrue("outside the base: escape/extra" in err)
    self.assertEqual(self.clones, [])

  def test_existing_repo_skipped_and_child_cloned_then_rerun_skips_all(self):
    os.makedirs("parent/.git")
    self.manifest("parent\nparent/child\n")
    code, out, err = self.invoke()
    self.assertEqual((code, err), (0, ""))
    self.assertTrue("Skipping existing repository: parent" in out)
    self.assertEqual([args[-1] for args in self.clones], ["parent/child"])
    self.config['remotes'] = ""
    code, out, err = self.invoke(entryPoint="gitdist")
    self.assertEqual((code, err), (0, ""))
    self.assertEqual(out.count("Skipping existing repository:"), 2)
    self.assertEqual([args for cwd, args in self.calls], [["rev-parse", "--show-toplevel"]])

  def makeConflicts(self):
    os.mkdir("empty")
    os.mkdir("nonempty")
    os.mkdir("worktree")
    for path in ["nonempty/tracked", "worktree/.git", "file"]:
      with open(path, "w") as handle:
        handle.write("fixture content")
    return ["empty", "nonempty", "worktree", "file"]

  def test_conflicts_report_stderr_and_continue_in_execution_and_preview(self):
    conflicts = self.makeConflicts()
    self.manifest("\n".join(conflicts + ["empty/child", "valid"]) + "\n")
    code, preview, err = self.invoke(["dist-clone-subrepos", "--dist-no-opt"])
    self.assertNotEqual(code, 0)
    self.assertEqual(self.clones, [])
    for path in conflicts:
      self.assertTrue("Destination '" + path + "'" in err, err)
    self.assertFalse("Error:" in preview)
    self.assertFalse(os.path.exists("empty/child"))
    self.assertFalse(os.path.exists("valid"))
    code, out, err = self.invoke()
    self.assertNotEqual(code, 0)
    self.assertEqual([args[-1] for args in self.clones], ["empty/child", "valid"])
    self.assertEqual(out, preview)
    for path in conflicts:
      self.assertTrue("Destination '" + path + "'" in err)

  def test_conflicts_only_do_not_resolve_remote(self):
    self.config['remotes'] = ""
    self.manifest("\n".join(self.makeConflicts()) + "\n")
    code, out, err = self.invoke()
    self.assertNotEqual(code, 0)
    self.assertEqual(err.count("exists without a .git directory"), 4)
    self.assertEqual([args for cwd, args in self.calls], [["rev-parse", "--show-toplevel"]])

  def test_file_parent_conflict_continues(self):
    self.makeConflicts()
    self.manifest("file\nfile/child\nvalid\n")
    code, out, err = self.invoke()
    self.assertNotEqual(code, 0)
    self.assertTrue("Destination 'file/child'" in err)
    self.assertEqual([args[-1] for args in self.clones], ["valid"])

  def test_parent_clone_introduces_destination_conflicts(self):
    self.manifest("parent\nparent/dir\nparent/file\nparent/dir/child\nvalid\n")
    self.config['effects'] = {"parent": [["parent/dir", "directory"], ["parent/file", "file"]]}
    code, out, err = self.invoke()
    self.assertNotEqual(code, 0)
    self.assertTrue("Destination 'parent/dir'" in err)
    self.assertTrue("Destination 'parent/file'" in err)
    self.assertEqual([args[-1] for args in self.clones], ["parent", "parent/dir/child", "valid"])

  def test_parent_clone_introduces_escaping_symlink(self):
    self.manifest("parent\nparent/escape/child\nvalid\n")
    self.config['effects'] = {"parent": [["parent/escape", self.testDir]]}
    code, out, err = self.invoke()
    self.assertNotEqual(code, 0)
    self.assertTrue("outside the base: parent/escape/child" in err)
    self.assertEqual([args[-1] for args in self.clones], ["parent", "valid"])
    self.assertFalse(os.path.exists(os.path.join(self.testDir, "child")))

  def test_failed_first_clone_continues_and_returns_error(self):
    self.manifest("first\nlater\n")
    self.config['failClone'] = "first"
    code, out, err = self.invoke()
    self.assertNotEqual(code, 0)
    self.assertTrue("git clone failed for 'first'" in err)
    self.assertTrue("exit status 17" in err)
    self.assertFalse("git clone failed" in out)
    self.assertEqual([args[-1] for args in self.clones], ["first", "later"])
    self.assertTrue(os.path.isdir("later/.git"))

  def test_failed_later_clone_continues_and_preserves_completed_clone(self):
    self.manifest("first\nsecond\nlater\n")
    self.config['failClone'] = "second"
    code, out, err = self.invoke()
    self.assertNotEqual(code, 0)
    self.assertTrue("git clone failed for 'second'" in err)
    self.assertFalse("git clone failed" in out)
    self.assertEqual([args[-1] for args in self.clones], ["first", "second", "later"])
    self.assertTrue(os.path.isdir("first/.git"))
    self.assertTrue(os.path.isdir("later/.git"))

  def test_multiple_clone_failures_report_each_and_attempt_all_repos(self):
    self.manifest("first\nsecond\nlast\n")
    self.config['failClones'] = ["first", "last"]
    code, out, err = self.invoke()
    self.assertNotEqual(code, 0)
    self.assertEqual(err.count("git clone failed for"), 2)
    self.assertTrue("git clone failed for 'first'" in err)
    self.assertTrue("git clone failed for 'last'" in err)
    self.assertFalse("git clone failed" in out)
    self.assertEqual([args[-1] for args in self.clones], ["first", "second", "last"])
    self.assertTrue(os.path.isdir("second/.git"))

  def test_preview_is_shell_copyable_and_custom_git_used(self):
    self.config['url'] = "https://host/team;$value/base.git"
    destination = "a dir/repo;'$value"
    code, preview, err = self.invoke(["dist-clone-subrepos", "--dist-no-opt",
      "--dist-repos=" + destination])
    self.assertEqual((code, err), (0, ""))
    self.assertEqual(self.clones, [])
    self.assertFalse(os.path.exists("a dir"))
    code, out, err = self.invoke(["dist-clone-subrepos", "--dist-repos=" + destination])
    self.assertEqual((code, err), (0, ""))
    self.assertEqual(preview, out)
    self.assertEqual(shlex.split(preview), [self.fakeGit] + self.clones[0])
    self.assertEqual(self.clones[0][-2:],
      ["https://host/team;$value/repo;'$value.git", destination])

  def test_branch_shell_metacharacters_remain_one_argument(self):
    self.manifest("extra topic;'$value\n")
    code, out, err = self.invoke()
    self.assertEqual((code, err), (0, ""))
    self.assertEqual(self.clones[0][3:5], ["-b", "topic;'$value"])
    self.assertEqual(shlex.split(out), [self.fakeGit] + self.clones[0])

  def test_debug_does_not_collect_status(self):
    self.manifest("extra\n")
    code, out, err = self.invoke(["dist-clone-subrepos", "--dist-debug"])
    self.assertEqual((code, err), (0, ""))
    self.assertTrue("*** Querying Git:" in out)
    self.assertFalse(any(args[0] in ["status", "diff", "log"] for cwd, args in self.calls))

  def test_incompatible_flags_and_extra_args_fail_before_discovery(self):
    self.manifest("extra\n")
    for arg in ["gitdist", "status", "--raw-arg", "--dist-mod-only",
        "--dist-version-file=missing", "--dist-version-file2=", "--dist-legend",
        "--dist-short", "--dist-utf8-output", "dist-repo-status", "dist-repo-versions-table"]:
      code, out, err = self.invoke(["dist-clone-subrepos", arg])
      self.assertNotEqual(code, 0)
      self.assertTrue("error:" in err.lower(), err)
      self.assertFalse("Traceback" in err, err)
      self.assertEqual(self.calls, [])

  def test_non_repository_and_non_root_rejected(self):
    self.config['responses'] = {"rev-parse --show-toplevel": [128, ""]}
    code, out, err = self.invoke()
    self.assertNotEqual(code, 0)
    self.assertTrue("Git discovery failed" in err)
    self.config = {}
    os.mkdir("subdir")
    os.chdir("subdir")
    code, out, err = self.invoke()
    self.assertNotEqual(code, 0)
    self.assertTrue("working-tree root" in err)
    self.assertEqual(self.clones, [])

  def test_worktree_base_accepted(self):
    os.rmdir(".git")
    with open(".git", "w") as handle:
      handle.write("gitdir: /mock/worktree/admin")
    self.manifest("extra\n")
    code, out, err = self.invoke()
    self.assertEqual((code, err), (0, ""))
    self.assertEqual([args[-1] for args in self.clones], ["extra"])

  def test_base_relocation_precedes_manifest_and_git_discovery(self):
    self.manifest(".\nparent\nparent/nested\nouter-extra\n")
    os.makedirs("parent/.git")
    os.makedirs("parent/nested/.git")
    with open("parent/.gitdist", "w") as handle:
      handle.write(".\nnested\ninner-extra\n")
    os.chdir("parent/nested")
    self.manifest(".\nlocal-extra\n")
    for mode, root, destinations in [
        ("", os.path.join(self.base, "parent/nested"), ["local-extra"]),
        ("IMMEDIATE_BASE", os.path.join(self.base, "parent"), ["inner-extra"]),
        ("EXTREME_BASE", self.base, ["outer-extra"])]:
      if mode == "IMMEDIATE_BASE":
        os.remove(".gitdist.default")
      os.environ["GITDIST_MOVE_TO_BASE_DIR"] = mode
      os.environ["PWD"] = os.getcwd()
      code, out, err = self.invoke()
      self.assertEqual((code, err), (0, ""))
      self.assertEqual([args[-1] for args in self.clones], destinations)
      self.assertTrue(all(cwd == root for cwd, args in self.calls))


  def test_clone_help_topic_and_sample(self):
    for args in [["--dist-help=dist-clone-subrepos"],
        ["--dist-help=dist-clone-subrepos", "--help"], ["--dist-help=all"]]:
      code, out, err = self.invoke(args)
      self.assertEqual((code, err), (0, ""))
      self.assertTrue("CLONE SUBREPOSITORIES:" in out)
      self.assertTrue("  . main\n  subrepo1 dev\n  subrepo1/subrepo2\n" in out)
      commands = " ".join(out.replace("\\\n", "").split())
      self.assertTrue("git clone -o gl-proj -b dev https://some-git-host.com/proj/subrepo1.git subrepo1" in commands)
      self.assertTrue("git clone -o gl-proj https://some-git-host.com/proj/subrepo2.git subrepo1/subrepo2" in commands)
      for guidance in ["remote's", "Parents", "STDERR", "--dist-no-opt", "local Git queries"]:
        self.assertTrue(guidance in out)
      self.assertEqual(self.calls, [])

  def test_usage_header_exposes_clone_command(self):
    code, out, err = self.invoke(["--help"])
    self.assertEqual((code, err), (0, ""))
    assertContainsGitdistHelpHeader(self, out)
    self.assertTrue("gitdist [gitdist arguments] dist-clone-subrepos" in out)
    self.assertTrue("read-only" in out)


if __name__ == '__main__':
  unittest.main()
