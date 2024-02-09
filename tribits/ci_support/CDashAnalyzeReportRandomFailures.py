
import os
import argparse

from FindGeneralScriptSupport import *
import CDashQueryAnalyzeReport as CDQAR

class CDashAnalyzeReportRandomFailuresDriver:

  def __init__(self, versionInfoStrategy, extractBuildNameStrategy):
    self.getTargetTopicSha1Strategy = versionInfoStrategy
    self.getextractBuildNameStrategy = extractBuildNameStrategy
    self.args = None

  def runDriver(self):
    pass
