#!/usr/bin/env python3

import sys
import argparse
import re as regex

from FindCISupportDir import *
import CDashAnalyzeReportRandomFailures as CDARRF


usageHelp = \
r"""
Example usageHelp string
"""


def main():

  cdashAnalyzeAndReportRandomFailures = \
    CDARRF.CDashAnalyzeReportRandomFailuresDriver(
      ExampleVersionInfoStrategy(),
      ExampleExtractBuildNameStrategy(),
      usageHelp=usageHelp)

  cdashAnalyzeAndReportRandomFailures.runDriver()


class ExampleVersionInfoStrategy:

  def getTargetTopicSha1s(self, buildData):
    pattern = r"Parent [12]:\n\s+(\w+)"
    matchedList = regex.findall(pattern, buildData)

    if len(matchedList) != 2: return None
    return tuple(matchedList)

  def checkTargetTopicRandomFailure(self, targetTopicPair, knownTargetTopicPairs):
    return targetTopicPair in knownTargetTopicPairs


class ExampleExtractBuildNameStrategy:

  def getCoreBuildName(self, fullBuildName):
    coreBuildName = fullBuildName.rsplit('-',1)[0]
    return coreBuildName


if __name__ == '__main__':
  sys.exit(main())
