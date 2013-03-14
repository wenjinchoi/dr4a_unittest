# -*- coding: UTF-8 -*-

from utils.loadFunction import scan_db, SCAN_TYPE_MMSSMS

from templates.testDeviceOfMmssms import testDevice8

scan_db(testDevice8["deviceInfo"],
										 SCAN_TYPE_MMSSMS,
							 			 "./src_db",
							 			 "./rec_db")
