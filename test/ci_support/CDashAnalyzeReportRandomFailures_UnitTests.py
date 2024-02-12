import unittest
from unittest.mock import patch
import unittest.mock as mock
import datetime


from FindCISupportDir import *
import CDashAnalyzeReportRandomFailures as CDARRF
from example_cdash_analyze_and_report_random_failures import ExampleVersionInfoStrategy, ExampleExtractBuildNameStrategy


####################################################################
#
# Test CDashAnalyzeReportRandomFailuresDriver
#
####################################################################

def getDriver():
  return CDARRF.CDashAnalyzeReportRandomFailuresDriver(
    ExampleVersionInfoStrategy(),
    ExampleExtractBuildNameStrategy())

#
# Test getDateRangeTuple member function
# for how it constructs a tuple containing
# the begin and end of a date range.
#
class Test_GetDateRangeTuple(unittest.TestCase):

  def setUp(self):
    self.driver = getDriver()

  def test_date_range_tuple(self):
    referenceDateTime = datetime.datetime(year=2024, month=2, day=12)
    dayTimeDelta = 3
    expected = ('2024-02-10', '2024-02-12')

    sideEffectList = ['2024-02-10', '2024-02-12']
    with mock.patch('cdash_build_testing_date.getDateStrFromDateTime', side_effect=sideEffectList) as m_getDateStrFromDateTime:
      result = self.driver.getDateRangeTuple(referenceDateTime, dayTimeDelta)

    self.assertEqual(result, expected)


#
# Test getBuildIDFromTest() member function
# to check if it can get correctly get the last value of
# a slash delimited string
#
class Test_GetBuildIdFromTest(unittest.TestCase):

  def setUp(self):
    self.driver = getDriver()

  def test_single_slash(self):
    testDict = {'buildSummaryLink':'build/somenumber'}
    self.assertEqual(
      self.driver.getBuildIdFromTest(testDict), 'somenumber')

  def test_multiple_slash(self):
    testDict = {'buildSummaryLink':'build/two/somenumber'}
    self.assertEqual(
      self.driver.getBuildIdFromTest(testDict), 'somenumber')

  def test_no_slash(self):
    testDict = {'buildSummaryLink':'somenumber'}
    self.assertEqual(
      self.driver.getBuildIdFromTest(testDict), 'somenumber')

if __name__ == '__main__':
  unittest.main()
