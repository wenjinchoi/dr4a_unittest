# -*- coding: UTF-8 -*-

import os
import shutil

SQLITE_VERSION_3_6_21 = 0
SQLITE_VERSION_3_7_15 = 1

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
