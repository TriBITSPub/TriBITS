#!/usr/bin/env python
#
# This simple set of python functions makes it easy to do simple math with
# times formatted as <min>m<sec>s.  This makes it easier to analyze timing
# data.
#

import sys
import os

def mmss2s(mmss):
  #print "mmss =", mmss
  minsec_array = mmss.split("m")
  if len(minsec_array) == 2:
    minutes = float(minsec_array[0])
    seconds = float(minsec_array[1][:-1])
  else:
    minutes = 0.0
    seconds = float(minsec_array[0][:-1])
  return minutes*60 + seconds

def s2mmss(seconds):
  minutes = int(seconds) / 60
  seconds_remainder = seconds - minutes*60
  if minutes == 0:
    return str(seconds_remainder)+"s"
  return str(minutes)+"m"+str(seconds_remainder)+"s"

def sub_mmss(mmss1, mmss2):
  num1 = mmss2s(mmss1)
  num2 = mmss2s(mmss2)
  return s2mmss(num1 - num2)

def div_mmss(mmss_num, mmss_denom):
  num_num = mmss2s(mmss_num)
  num_denom = mmss2s(mmss_denom)
  return num_num/num_denom


#
# Unit test suite
#

if __name__ == '__main__':

  import unittest
  
  class test_mmss2s(unittest.TestCase):
  
    def setUp(self):
      None
  
    def test_1(self):
      self.assertEqual(mmss2s("2s"), 2.0)
  
    def test_2(self):
      self.assertEqual(mmss2s("2.53s"), 2.53)
  
    def test_3(self):
      self.assertEqual(mmss2s("0m4.5s"), 4.5)
  
    def test_4(self):
      self.assertEqual(mmss2s("1m2.4s"), 62.4)
  
    def test_5(self):
      self.assertEqual(mmss2s("3m10.531s"), 190.531)
  
  class test_s2mmss(unittest.TestCase):
  
    def setUp(self):
      None
  
    def test_1(self):
      self.assertEqual(s2mmss(2.0), "2.0s")
  
    def test_2(self):
      self.assertEqual(s2mmss(3.456), "3.456s")
  
    def test_3(self):
      self.assertEqual(s2mmss(60.0), "1m0.0s")
  
    def test_4(self):
      self.assertEqual(s2mmss(75.346), "1m15.346s")
  
    def test_4(self):
      self.assertEqual(s2mmss(121.25), "2m1.25s")
  
  class test_sub_mmss(unittest.TestCase):
  
    def setUp(self):
      None
  
    def test_1(self):
      self.assertEqual(sub_mmss("2s", "1s"), "1.0s")
  
    def test_2(self):
      self.assertEqual(sub_mmss("1m5.23s", "45s"), "20.23s")
  
  class test_div_mmss(unittest.TestCase):
  
    def setUp(self):
      None
  
    def test_1(self):
      self.assertEqual(div_mmss("2s", "1s"), 2.0)
  
    def test_2(self):
      self.assertEqual(div_mmss("1s", "2s"), 0.5)
  
    def test_3(self):
      self.assertEqual(div_mmss("1m50s", "55s"), 2.0)
  
    def test_4(self):
      self.assertEqual(div_mmss("55s", "1m50s"), 0.5)
    
  unittest.main()
