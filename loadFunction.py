# -*- coding: UTF-8 -*-

import os, sys
import time

from ctypes import *

class DeviceInfo(Structure):
    _fields_ = [("manufacturer", c_wchar_p),
                ("model", c_wchar_p),
                ("OSVersion", c_wchar_p)]

    def __str__(self):
        return '{0} {1} {2}'.format(self.manufacturer,
                                    self.model,
                                    self.OSVersion);

# def WSDBRecoveryCallback(callbackType, scanType, current, total):
#    print "I'm callback."
# pWSDBRecoveryCallback = CFUNCTYPE(c_void_p, c_int, c_int, c_int, c_int)  #回调函数类型定义
# pWSDBRecoveryCallbackHandle = pWSDBRecoveryCallback(WSDBRecoveryCallback);

def redirect_stdout():
    # print "Redirecting stdout"
    sys.stdout.flush() # <--- important when redirecting to files
    newstdout = os.dup(1)
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, 1)
    os.close(devnull)
    sys.stdout = os.fdopen(newstdout, 'w')

def isLoaded(lib):
   libp = os.path.abspath(lib)
   ret = os.system("lsof -p %d | grep %s > /dev/null" % (os.getpid(), libp))
   return (ret == 0)

def dlclose(handle):
   libdl = ctypes.CDLL("libdl.so")
   libdl.dlclose(handle)

# TODO: need to set deviceInfo
def ScanSMSDB(sms_file_path, rec_path):
	if not os.path.exists('WSConfigerDB.db'):
		print "Can not find WSConfigerDB.db"
		return False

	if not os.path.exists('WSDBRecovery.dll'):
		print "Can not find WSDBRecovery.dll"
		return False

	if not os.path.exists(sms_file_path) or not os.path.exists(rec_path):
		print "Source DB file path or Recovery Path not exists"
		return False

	pConfigFile = c_wchar_p('WSConfigerDB.db')
	deviceInfo = DeviceInfo(c_wchar_p('sansung'),
                   		    c_wchar_p('s5880'),
                        	c_wchar_p('2.3.4'))
	pDeviceInfo = addressof(deviceInfo)

	saved_stdout = sys.stdout
	redirect_stdout()

	libdr = cdll.LoadLibrary("WSDBRecovery.dll")
	if (libdr.WSDBRecoveryInit(pConfigFile, pDeviceInfo) != 0):
		return False

	pwszDBPath = c_wchar_p(sms_file_path)
	pwszSaveDBPath = c_wchar_p(rec_path)
	scanType = c_int(1)
	pFunc = c_void_p(0)

	if (libdr.WSDBScan(pwszDBPath, pwszSaveDBPath , scanType, pFunc) != 0):
		return False

	libdr.WSDBRecoveryUnInit()

	sys.stdout = saved_stdout

	return True




