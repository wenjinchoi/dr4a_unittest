# -*- coding: UTF-8 -*-

from loadFunction import *
from SchemaTemplates import *

deviceInfo = DeviceInfo(c_wchar_p('sansung'),
                   		    c_wchar_p('s5880'),
                        	c_wchar_p('2.3.4'))

deviceTestInfo= {"deviceInfo": deviceInfo,
						 "Schema": smsSchema1}

print deviceTestInfo
