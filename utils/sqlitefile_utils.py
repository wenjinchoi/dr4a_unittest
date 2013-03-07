# -*- coding: UTF-8 -*-

import os
import sqlite3
import struct

def createDB(path, smsSchema, auto_vacuum = 0):
	if os.path.exists(path):
		os.remove(path)
	with sqlite3.connect(path) as conn:
		curs = conn.cursor()
		curs.execute('PRAGMA auto_vacuum = %d' % auto_vacuum)
		curs.execute(smsSchema)
		conn.commit()

def isTableExists(db_file, table_name):
	with sqlite3.connect(db_file) as conn:
		curs = conn.cursor()
		curs.execute('''SELECT COUNT(*)
			FROM sqlite_master
			WHERE type="table" and name="%s"''' % table_name)
		if curs.fetchall()[0][0] > 0:
			return True
		else:
			return False

def getPageSize(sqlite_file):
	pagesize = 0
	with open(sqlite_file, 'rb') as f:
		# Page Size: Offset 16 2 bytes 16 bit integer read big endian
		f.seek(16)
		read_buffer = f.read(2)
		(pagesize,) = struct.unpack(">h", read_buffer)
	return pagesize

def pageHeader(sqlitePage):
	(ptype, first_free_block_offset, cells_count, cell_offset) = \
		struct.unpack(">BHHHx", sqlitePage[:8])
	return (ptype, first_free_block_offset, cells_count, cell_offset)

# TODO: more smart...
def getFirstPage(sqlite_file):
	buffer = []
	with open(sqlite_file, 'rb') as f:
		pagesize = getPageSize(sqlite_file)
		f.seek(pagesize) # auto vacuum 需要 *2
		buffer = f.read(pagesize)
	return buffer

def recordList(sqlite_page):
	records = []
	cells_count = pageHeader(sqlite_page)[2]
	offset = 8
	for n in xrange(cells_count):
		records.append(struct.unpack('>H', sqlite_page[offset:offset+2])[0])
		offset += 2
	return records

def recordSize(sqlite_page, num):
	offset = recordList(sqlite_page)[num]
	return struct.unpack('>B', sqlite_page[offset:offset+1])[0] + 2

def lastRecordSize(sqlite_file):
	sqlite_page = getFirstPage(sqlite_file)
	return recordSize(sqlite_page, -1)

# test
if __name__ == '__main__':
	tmpdb_path = './tmp/example_1.db'
	print getPageSize(tmpdb_path)
	page = SmsFirstPage(tmpdb_path)
	print pageHeader(page)
	records = recordList(page)
	print lastSmsRecordSize(tmpdb_path)
