# -*- coding: UTF-8 -*-

import unittest

# from utils.tools import *
# switch_pysqlite_version(r"C:\Python27\DLLs", SQLITE_VERSION_3_7_15)

from unittest_sms_deleting import SMSTestCase
from templates import testDeviceOfMmssms

class Samsung_gtn7000_4_0_4_TestCase(SMSTestCase):
	def setUp(self):
		self.initWithDeviceAndSchema(testDeviceOfMmssms.testDevice3)

class Samsung_GT_N7000_4_0_4_TestCase(SMSTestCase):
	def setUp(self):
		self.initWithDeviceAndSchema(testDeviceOfMmssms.testDevice6)

class Samsung_gt_i9300_4_1_2_TestCase(SMSTestCase):
	def setUp(self):
		self.initWithDeviceAndSchema(testDeviceOfMmssms.testDevice8)

class Samsung_gt_n7100_4_1_1_TestCase(SMSTestCase):
	def setUp(self):
		self.initWithDeviceAndSchema(testDeviceOfMmssms.testDevice9)

if __name__ == '__main__':
	unittest.main()
