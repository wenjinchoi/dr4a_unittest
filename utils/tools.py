# -*- coding: UTF-8 -*-

import os
import shutil

SQLITE_VERSION_3_6_21 = 0
SQLITE_VERSION_3_7_15 = 1

def isLoaded(lib):
   libp = os.path.abspath(lib)
   ret = os.system("lsof -p %d | grep %s > /dev/null" % (os.getpid(), libp))
   return (ret == 0)

def dlclose(handle):
   libdl = ctypes.CDLL("libdl.so")
   libdl.dlclose(handle)

def switch_pysqlite_version(path, version):
	tmp_path = path
	if os.path.isfile(tmp_path):
		tmp_path = os.path.split(tmp_path)[0]
	if os.path.exists(os.path.join(tmp_path, "sqlite3.dll")):
		pass
	if version == SQLITE_VERSION_3_6_21:
		shutil.copy2("./lib/sqlite3_6_21.dll",
								 os.path.join(tmp_path, "sqlite3.dll"))
	elif version == SQLITE_VERSION_3_7_15:
		shutil.copy2("./lib/sqlite3_7_15.dll",
						 os.path.join(tmp_path, "sqlite3.dll"))
