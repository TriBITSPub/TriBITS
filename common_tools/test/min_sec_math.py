#!/usr/bin/env python
#
# This simple set of python functions makes it easy to do simple math with
# times formatted as <min>m<sec>s.  This makes it easier to analyze timing
# data.
#

import sys
import os

def minsec_to_sec(mmss):
  #print "mmss =", mmss
  minsec_array = mmss.split("m")
  if len(minsec_array) == 2:
    minutes = float(minsec_array[0])
    seconds = float(minsec_array[1][:-1])
  else:
    minutes = 0.0
    seconds = float(minsec_array[0][:-1])
  return minutes*60 + seconds

def sec_to_minsec(seconds):
  minutes = int(seconds) / 60
  seconds_remainder = seconds - minutes*60
  if minutes == 0:
    return str(seconds_remainder)+"s"
  return str(minutes)+"m"+str(seconds_remainder)+"s"

def subtract_minsec(mmss1, mmss2):
  num1 = minsec_to_sec(mmss1)
  num2 = minsec_to_sec(mmss2)
  return sec_to_minsec(num1 - num2)

def divide_minsec(mmss_num, mmss_denom):
  num_num = minsec_to_sec(mmss_num)
  num_denom = minsec_to_sec(mmss_denom)
  return num_num/num_denom


#
# Unit test suite
#

if __name__ == '__main__':

  import unittest
  
  class test_minsec_to_sec(unittest.TestCase):
  
    def setUp(self):
      None
  
    def test_1(self):
      self.assertEqual(minsec_to_sec("2s"), 2.0)
  
    def test_2(self):
      self.assertEqual(minsec_to_sec("2.53s"), 2.53)
  
    def test_3(self):
      self.assertEqual(minsec_to_sec("0m4.5s"), 4.5)
  
    def test_4(self):
      self.assertEqual(minsec_to_sec("1m2.4s"), 62.4)
  
    def test_5(self):
      self.assertEqual(minsec_to_sec("3m10.531s"), 190.531)
  
  class test_sec_to_minsec(unittest.TestCase):
  
    def setUp(self):
      None
  
    def test_1(self):
      self.assertEqual(sec_to_minsec(2.0), "2.0s")
  
    def test_2(self):
      self.assertEqual(sec_to_minsec(3.456), "3.456s")
  
    def test_3(self):
      self.assertEqual(sec_to_minsec(60.0), "1m0.0s")
  
    def test_4(self):
      self.assertEqual(sec_to_minsec(75.346), "1m15.346s")
  
    def test_4(self):
      self.assertEqual(sec_to_minsec(121.25), "2m1.25s")
  
  class test_subtract_minsec(unittest.TestCase):
  
    def setUp(self):
      None
  
    def test_1(self):
      self.assertEqual(subtract_minsec("2s", "1s"), "1.0s")
  
    def test_2(self):
      self.assertEqual(subtract_minsec("1m5.23s", "45s"), "20.23s")
  
  class test_divide_minsec(unittest.TestCase):
  
    def setUp(self):
      None
  
    def test_1(self):
      self.assertEqual(divide_minsec("2s", "1s"), 2.0)
  
    def test_2(self):
      self.assertEqual(divide_minsec("1s", "2s"), 0.5)
  
    def test_3(self):
      self.assertEqual(divide_minsec("1m50s", "55s"), 2.0)
  
    def test_4(self):
      self.assertEqual(divide_minsec("55s", "1m50s"), 0.5)
    
  unittest.main()
