
import unittest

from FindCISupportDir import *
from trilinos_cdash_analyze_and_report_random_failures import *


class TestTrilinosVersionInfoStrategy(unittest.TestCase):

  def setUp(self):
    self.strategy = TrilinosVersionInfoStrategy()

  def test_getTargetTopicSha1s_with_valid_versionData(self):
    versionData = "Parent 1:\n target\nParent 2:\n topic"

    expected = ('target','topic')
    result = self.strategy.getTopicTargetSha1s(versionData)

    self.assertEqual(result, expected)

  def test_checkTargetTopicRandomFailure_true(self):
    targetTopicPair = ('target', 'topic')
    knownTargetTopicPairs = {('target','topic')}

    result = self.strategy.checkTargetTopicRandomFailure(targetTopicPair, knownTargetTopicPairs)

    self.assertTrue(result)

  def test_checkTargetTopicRandomFailure_false(self):
    targetTopicPair = ('some','other')
    knownTargetTopicPairs = {('target','topic')}

    result = self.strategy.checkTargetTopicRandomFailure(targetTopicPair, knownTargetTopicPairs)

    self.assertFalse(result)


class TrilinosExtractBuildName(unittest.TestCase):

  def setUp(self):
    self.strategy = TrilinosExtractBuildNameStrategy()

  def test_getCoreBuildName(self):
    fullBuildName = "PR-number-test-core_build-name-number"

    expected = "PR-number-test-core_build-name"
    result = self.strategy.getCoreBuildName(fullBuildName)

    self.assertEqual(result, expected)


if __name__ == '__main__':
  unittest.main()
