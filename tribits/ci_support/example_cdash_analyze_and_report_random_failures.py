#!/usr/bin/env python

import sys
import argparse
import re as regex

import CDashAnalyzeReportRandomFailures as CDARRF


def main():

  cdashAnalyzeAndReportRandomFailures = \
    CDARRF.CDashAnalyzeReportRandomFailuresDriver(
      ExampleVersionInfoStrategy(),
      ExtractBuildNameStrategy())

  cdashAnalyzeAndReportRandomFailures.runDriver()

class ExampleVersionInfoStrategy:

  def getTopicTargetSha1s(self, buildData):
    pattern = r"Parent [12]:\n\s+(\w+)"
    matchedList = regex.findall(pattern, buildData)

    if len(matchedList) != 2: return None
    return tuple(matchedList)

  def checkTargetTopicRandomFailure(self, targetTopicPair, knownTargetTopicPairs):
    return targetTopicPair in knownTargetTopicPairs

class ExtractBuildNameStrategy:
  pass



if __name__ == '__main__':
  sys.exit(main())
