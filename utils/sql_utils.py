# -*- coding: UTF-8 -*-

import sqlite3

def insertTestDataWithSQL(db_file, testData, sql):
	with sqlite3.connect(db_file) as conn:
		curs = conn.cursor()
		for n in range(len(testData)):
			curs.execute(sql, testData[n])
		conn.commit()

def deleteWithSQL(db_file, sql):
	with sqlite3.connect(db_file) as conn:
		curs = con.cursor()
		curs.execute(sql)
		conn.commit()

def deleteWithID(db_file, table_name, id):
	sql = "DELETE FROM " + table_name + " WHERE _id = " + id
	deleteWithSQL(sql)

def deleteWithIDs(db_file, ids):
	for id in ids:
		deleteWithID(db_file, id)

def fetchallWithSQL(db_file, sql):
	with sqlite3.connect(db_file) as conn:
		conn.text_factory = lambda x: unicode(x, "UTF-8", "ignore")
		curs = conn.cursor()
		curs.execute(sql)
		return curs.fetchall()

def fetchColsInTableWithID(db_file, table_name, cols, id):
	sql = "SELECT %s FROM %s WHERE _id = %d" % (cols, table_name, id)
	return fetchallWithSQL(db_file, sql)

