# @HEADER
# ************************************************************************
#
#            TriBTS: Tribal Build, Integrate, and Test System
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

import os
import shutil
import unittest
import stat
import tempfile

from FindCISupportDir import *
import CDashQueryAnalyzeReport as CDQAR
from cdash_analyze_and_report_random_failures import *
from CDashQueryAnalyzeReportUnitTestHelpers import *

# Base test directory in the build tree
g_baseTestDir = "cdash_analyze_and_report_random_failures"


def cdash_analyze_and_report_random_failures_setup_test_dir(testCaseName):
    testInputDir = testCiSupportDir + "/" + g_baseTestDir + "/" + testCaseName
    testOutputDir = os.getcwd()
    for f in os.listdir(testInputDir):
        thing = os.path.join(testInputDir, f)
        if os.path.isdir(thing):
            shutil.copytree(thing, os.path.join(testOutputDir, f))
        else:
            shutil.copy(thing, testOutputDir)
    return testOutputDir


def remove_dirs(dirname):
    walk_gen = os.walk(dirname, topdown=False)
    for dirpath, dirnames, filenames in walk_gen:
        os.chmod(dirpath, stat.S_IRWXU)
    shutil.rmtree(dirname)


def create_file(fpath, perms=0o600, content=""):
    path = os.path.split(fpath)[0]
    if path and not path == "." and not os.path.isdir(path):
        os.makedirs(path)
    with open(fpath, "w+") as fptr:
        fptr.write(content)
    os.chmod(fpath, perms)
    return os.path.abspath(fpath)


class TemporaryDirectory(object):
    def __init__(self, **kwargs):
        self.orig_dir = os.getcwd()
        self.name = tempfile.mkdtemp(
            suffix=kwargs.get("suffix", ""),
            prefix=kwargs.get("prefix", "tmp"),
            dir=kwargs.get("dir", None),
        )

    def remove(self):
        os.chdir(self.orig_dir)
        if os.path.exists(self.name):
            remove_dirs(self.name)

    def __enter__(self):
        os.chdir(self.name)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.remove()

#############################################################################
#
# Unit tests for cdash_analyze_and_report_random_failures.py
#
#############################################################################


class test_getBuildIdFromTest(unittest.TestCase):

    def test_single_slash(self):
        test_dict = { 'buildSummaryLink':'build/somenumber' }
        self.assertEqual(
            getBuildIdFromTest(test_dict), 'somenumber')

    def test_multiple_slash(self):
        test_dict = { 'buildSummaryLink':'build/path/temp/somenumber' }
        self.assertEqual(
            getBuildIdFromTest(test_dict), 'somenumber')

    def test_no_slash(self):
        test_dict = { 'buildSummaryLink':'buildid' }
        self.assertEqual(
            getBuildIdFromTest(test_dict), 'buildid')


#############################################################################
#
# System-level tests for cdash_analyze_and_report_random_failures.py
#
#############################################################################


class test_cdash_analyze_and_report_random_failures(unittest.TestCase):
    def cdash_analyze_and_report_random_failures_run_case(
        self,
        expectedRtnCode,
        stdoutRegexList,
        extraCmndLineOptionsList=None,
        verbose=False,
        debugPrint=False,
    ):
        if not extraCmndLineOptionsList:
            extraCmndLineOptionsList = []

        cmnd = (
            ciSupportDir
            + "/cdash_analyze_and_report_random_failures.py"
            + " --cdash-project-name='ProjectName'"
            + " --cdash-site-url='https://something.com/cdash'"
            + " --reference-date=2018-10-28"
            + " "
            + " ".join(extraCmndLineOptionsList)
        )

        stdoutFile = "stdout.out"
        stdoutFileAbsPath = os.getcwd() + "/" + stdoutFile
        rtnCode = CDQAR.echoRunSysCmnd(
            cmnd, throwExcept=False, outFile=stdoutFile, verbose=verbose
        )

        stdout = ""
        try:
            with open(stdoutFile, "r") as inf:
                stdout = inf.read()
        except Exception:
            print("WARNING: No stdout available from this test")

        # UNCOMMENT THIS TO SEE OUTPUT FROM THE SCRIPT (Can use the test to help develop)
        # print(stdout)

        self.assertEqual(rtnCode, expectedRtnCode, "Failed with stdout: " + stdout)

        assertListOfRegexsFoundInListOfStrs(
            self,
            stdoutRegexList,
            stdout.splitlines(),
            stdoutFileAbsPath,
            debugPrint=debugPrint,
        )

    def setUp(self):
        self.test_dir = TemporaryDirectory()
        os.chdir(self.test_dir.name)

    def tearDown(self):
        self.test_dir.remove()

    def test_base(self):
        cdash_analyze_and_report_random_failures_setup_test_dir("random")

        self.cdash_analyze_and_report_random_failures_run_case(
            expectedRtnCode=0,
            stdoutRegexList=[
                "Number of failing tests from 2018-10-28 to 2018-10-28: 1"
            ],
        )


if __name__ == "__main__":
    unittest.main()
