# -*- coding: UTF-8 -*-

import os
import unittest
import sqlite3

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

	def insertNormalTestData(self, db_file, testData):
		with sqlite3.connect(db_file) as conn:
			curs = conn.cursor()
			insertSQL = '''INSERT INTO data(package_id,mimetype_id,raw_contact_id,data1)
				VALUES (?, ?, ?, ?)'''
			for n in xrange(len(testData)):
				curs.execute(insertSQL, testData[n])
			conn.commit()

	def deleteDataTableWith_ID(self, db_file, id):
		with sqlite3.connect(db_file) as conn:
			curs = conn.cursor()
			deleteSQL = '''DELETE FROM data WHERE _id = %d''' % id
			curs.execute(deleteSQL)
			conn.commit()

	def testBase(self):
		testData = (
			(1, 1, 1, "10086"),
			(1, 1, 1, "13800138000"))

		self.insertNormalTestData(self.input_db_file, testData)
		self.deleteDataTableWith_ID(self.input_db_file, 2)


if __name__ == '__main__':
	unittest.main()
