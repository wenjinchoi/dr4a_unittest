# -*- coding: UTF-8 -*-

from utils.loadFunction import scan_db, SCAN_TYPE_MMSSMS

from templates.testDeviceOfMmssms import testDevice9

scan_db(testDevice9["deviceInfo"],
										 SCAN_TYPE_MMSSMS,
							 			 "./",
							 			 "./tmp_rec")
