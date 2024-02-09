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

  def getTopicTargetSha1s(buildData):
    pass

  def checkTargetTopicRandomFailure(targetTopic, knownTargetTopics):
    pass

class ExtractBuildNameStrategy:
  pass



if __name__ == '__main__':
  sys.exit(main())
