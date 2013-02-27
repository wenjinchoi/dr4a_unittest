# -*- coding: UTF-8 -*-

from ctypes import c_wchar_p

from loadFunction import *

samsung_S5880_2_3_4 = DeviceInfo(c_wchar_p('sansung'),
                   		    			 c_wchar_p('s5880'),
                        				 c_wchar_p('2.3.4'))

