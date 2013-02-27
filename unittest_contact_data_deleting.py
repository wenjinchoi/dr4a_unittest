# -*- coding: UTF-8 -*-

import os
import sqlite3
import unittest

from loadFunction import parsingByLoadLibrary, SCAN_TYPE_CONTACTS
from templates import testDeviceOfContacts
from sqlite_utils import *

class ContactsDataTableDeletedTestCase(unittest.TestCase):
	def setUp(self):
		self.initWithDeiveAndSchema(testDeviceOfContacts.testDevice1)

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
			mimetype_id, raw_contact_id, data1, data2, data3)
			VALUES (?,?,?,?,?)'''
		self.insertTestDataWithSQL(insertSQL, testData)

	def deleteDataTableWith_ID(self, id):
		with sqlite3.connect(self.input_db_file) as conn:
			curs = conn.cursor()
			deleteSQL = '''DELETE FROM data WHERE _id = %d''' % id
			curs.execute(deleteSQL)
			conn.commit()

	def parsingDataTableByLoadLibrary(self):
		parsingByLoadLibrary(self.deviceInfo,
												 SCAN_TYPE_CONTACTS,
												 self.input_db_file,
												 self.output_db_file)

	def checkResultWithTestDataNum(self, testData, id):
		results =()

		with sqlite3.connect(self.input_db_file) as conn:
			curs = conn.cursor()
			querySQL = '''SELECT mimetype_id,raw_contact_id,data1,data2,data3
				FROM data'''
			curs.execute(querySQL)
			results = curs.fetchall()

		self.assertTrue(testData[id-1] in results)


	def testNameBasic(self):
		testData = (
			(6, 1, "Tom Smith", "Tom", "Smith"),
			(6, 2, "Steven Gates", "Steven", "Gates"))

		deleteRecordID = 2

		self.insertNormalTestData(testData)
		# if need other table...
		self.deleteDataTableWith_ID(deleteRecordID)
		# self.parsingDataTableByLoadLibrary()
		self.checkResultWithTestDataNum(testData, deleteRecordID)

	def testNameInFirstName(self):
		pass

	def testNameWithPhoto(self):
		pass

if __name__ == '__main__':
	unittest.main()
