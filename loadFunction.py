# -*- coding: UTF-8 -*-

import os, sys
import time
from multiprocessing import Process

from ctypes import *

SCAN_TYPE_CONTACTS = c_int(0)
SCAN_TYPE_MMSSMS   = c_int(1)

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

def scan_db(tDeviceInfo, scan_type, src_path, rec_path):
	assert(os.path.exists("WSDBRecovery.dll"))
	assert(os.path.exists("WSConfigerDB.db"))

	saved_stdout = sys.stdout
	redirect_stdout()

	# Init WSDBRecovery
	pConfigFile = c_wchar_p('WSConfigerDB.db')

	deviceInfo = DeviceInfo(c_wchar_p(tDeviceInfo[0]),
	                 		    c_wchar_p(tDeviceInfo[1]),
	                      	c_wchar_p(tDeviceInfo[2]))
	pDeviceInfo = addressof(deviceInfo)

	libdr = cdll.LoadLibrary("WSDBRecovery.dll")
	if (libdr.WSDBRecoveryInit(pConfigFile, pDeviceInfo) != 0):
		print "WSDBRecoveryInit fail."
		return False

	# Scan and Output
	pwszDBPath = c_wchar_p(src_path)
	pwszSaveDBPath = c_wchar_p(rec_path)
	pFunc = c_void_p(0)

	ret = libdr.WSDBScan(pwszDBPath, pwszSaveDBPath , scan_type, pFunc)
	assert(ret == 0)

	libdr.WSDBRecoveryUnInit()

	sys.stdout = saved_stdout

	return True

# Using multiprocessing
def parsingByLoadLibrary(tDeviceInfo, scan_type, input_db_path, output_db_file):
	src_db_path = os.path.split(os.path.abspath(input_db_path))[0]
	rec_db_path = os.path.split(os.path.abspath(output_db_file))[0]

	# 使用 multiprocessing.Process 加载，主要避免调用动态库后，被解析的数据库文件无法删除
	# 注意：若使用 threading 会导致访问内存的异常
	# Process 的 args 不能传 class DeviceInfo 类型，这里传的时元组
	# 在 scan_db 内转换为 class DeviceInfo 类型
	p = Process(target=scan_db,
							args=(tDeviceInfo, scan_type, src_db_path, rec_db_path))
	p.start()
	p.join()


if __name__ == '__main__':
	tDeviceInfo = ('sansung', 's5880', '2.3.4' )
	print parsingByLoadLibrary(tDeviceInfo,
														 SCAN_TYPE_CONTACTS,
	 						 							 "./src_db/contacts2.db",
	 						 							 "./rec_db/contacts2.db")




