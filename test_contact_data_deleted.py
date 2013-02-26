# -*- coding: UTF-8 -*-

import os
import sqlite3
import unittest

from contactsTemplates import *
from sqlite_utily import *

class ContactsDataDeletedTestCase(unittest.TestCase):
	def setUp(self):
		deviceAndSchema = {"deviceInfo": "",
											 "schema": data_1}
		self.initWithDeiveAndSchema(deviceAndSchema)

	def initWithDeiveAndSchema(self, deviceAndSchema):
		self.deviceInfo = deviceAndSchema["deviceInfo"]
		self.schema = deviceAndSchema["schema"]

		if not os.path.exists('./src_db'): os.mkdir('./src_db')
		if not os.path.exists('./rec_db'): os.mkdir('./rec_db')
		self.input_db_file = './src_db/contacts2.db'
		self.output_db_file = './rec_db/contacts2.db'

		createDB(self.input_db_file, self.schema)

	def insertTestDataWithSQL(self, insertSQL, testData):
		with sqlite3.connect(self.input_db_file) as conn:
			curs = conn.cursor()
			for n in xrange(len(testData)):
				curs.execute(insertSQL, testData[n])
			conn.commit()

	def insertNormalTestData(self, testData):
		insertSQL = '''INSERT INTO data(
			package_id,mimetype_id,raw_contact_id,data1)
			VALUES (?, ?, ?, ?)'''
		self.insertTestDataWithSQL(insertSQL, testData)

	def deleteDataTableWith_ID(self, id):
		with sqlite3.connect(self.input_db_file) as conn:
			curs = conn.cursor()
			deleteSQL = '''DELETE FROM data WHERE _id = %d''' % id
			curs.execute(deleteSQL)
			conn.commit()

	def parsingDataTableByLoadLibrary(self):
		pass

	def checkResultWithTestDataNum(self, num):
		pass

	def testBase(self):
		testData = (
			(1, 1, 1, "10086"),
			(1, 1, 1, "13800138000"))

		deleteRecordID = 2

		self.insertNormalTestData(testData)
		self.deleteDataTableWith_ID(deleteRecordID)
		self.parsingDataTableByLoadLibrary()
		self.checkResultWithTestDataNum(deleteRecordID-1)


if __name__ == '__main__':
	unittest.main()
