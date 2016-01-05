#!/usr/bin/env python
#
# This simple set of python functions makes it easy to do simple math with
# times formatted as <min>m<sec>s.  This makes it easier to analyze timing
# data.
#

import sys
import os

def hms2s(hms):
  #print "mmss =", mmss
  minsec_array = hms.split("m")
  if len(minsec_array) == 2:
    minutes = float(minsec_array[0])
    seconds = float(minsec_array[1][:-1])
  else:
    minutes = 0.0
    seconds = float(minsec_array[0][:-1])
  return minutes*60 + seconds

def s2hms(seconds):
  minutes = int(seconds) / 60
  seconds_remainder = seconds - minutes*60
  if minutes == 0:
    return str(seconds_remainder)+"s"
  return str(minutes)+"m"+str(seconds_remainder)+"s"

def sub_hms(hms1, hms2):
  num1 = hms2s(hms1)
  num2 = hms2s(hms2)
  return s2hms(num1 - num2)

def div_hms(hms_num, hms_denom):
  num_num = hms2s(hms_num)
  num_denom = hms2s(hms_denom)
  return num_num/num_denom


#
# Unit test suite
#

if __name__ == '__main__':

  import unittest
  
  class test_hms2s(unittest.TestCase):
  
    def setUp(self):
      None
  
    def test_1(self):
      self.assertEqual(hms2s("2s"), 2.0)
  
    def test_2(self):
      self.assertEqual(hms2s("2.53s"), 2.53)
  
    def test_3(self):
      self.assertEqual(hms2s("0m4.5s"), 4.5)
  
    def test_4(self):
      self.assertEqual(hms2s("1m2.4s"), 62.4)
  
    def test_5(self):
      self.assertEqual(hms2s("3m10.531s"), 190.531)
  
  class test_s2hms(unittest.TestCase):
  
    def setUp(self):
      None
  
    def test_1(self):
      self.assertEqual(s2hms(2.0), "2.0s")
  
    def test_2(self):
      self.assertEqual(s2hms(3.456), "3.456s")
  
    def test_3(self):
      self.assertEqual(s2hms(60.0), "1m0.0s")
  
    def test_4(self):
      self.assertEqual(s2hms(75.346), "1m15.346s")
  
    def test_4(self):
      self.assertEqual(s2hms(121.25), "2m1.25s")
  
  class test_sub_hms(unittest.TestCase):
  
    def setUp(self):
      None
  
    def test_1(self):
      self.assertEqual(sub_hms("2s", "1s"), "1.0s")
  
    def test_2(self):
      self.assertEqual(sub_hms("1m5.23s", "45s"), "20.23s")
  
  class test_div_hms(unittest.TestCase):
  
    def setUp(self):
      None
  
    def test_1(self):
      self.assertEqual(div_hms("2s", "1s"), 2.0)
  
    def test_2(self):
      self.assertEqual(div_hms("1s", "2s"), 0.5)
  
    def test_3(self):
      self.assertEqual(div_hms("1m50s", "55s"), 2.0)
  
    def test_4(self):
      self.assertEqual(div_hms("55s", "1m50s"), 0.5)
    
  unittest.main()
