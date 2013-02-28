# -*- coding: UTF-8 -*-

import os
import random
import shutil
import sqlite3
import unittest

from loadFunction import parsingByLoadLibrary, SCAN_TYPE_CONTACTS
from templates import testDeviceOfContacts
from templates.contacts_table_columns import *
from sqlite_utils import *
from valueMaker import *

class ContactsDataTableDeletedTestCase(unittest.TestCase):
	def setUp(self):
		self.initWithDeiveAndSchema(testDeviceOfContacts.testDevice1)

	def initWithDeiveAndSchema(self, deviceAndSchema):
		self.deviceInfo = deviceAndSchema["deviceInfo"]
		self.schema = deviceAndSchema["schema"]

		if not os.path.exists('./src_db'): os.mkdir('./src_db')
		if not os.path.exists('./rec_db'): os.mkdir('./rec_db')
		self.input_db_file  = './src_db/contacts2.db'
		self.output_db_file = './rec_db/contacts2.db'

		createDB(self.input_db_file, self.schema)

	def insertTestDataWithSQL(self, insertSQL, testData):
		with sqlite3.connect(self.input_db_file) as conn:
			# conn.text_factory = lambda x: unicode(x, "UTF-8", "ignore")
			curs = conn.cursor()
			for n in xrange(len(testData)):
				curs.execute(insertSQL, testData[n])
			conn.commit()

	def insertNormalTestData(self, testData):
		insertSQL = '''INSERT INTO data(
			mimetype_id, raw_contact_id, data1, data2, data3)
			VALUES (?,?,?,?,?)'''
		self.insertTestDataWithSQL(insertSQL, testData)

	def backupDatabaseBeforDeleting(self):
		(path, filename) = os.path.split(os.path.abspath(self.input_db_file))
		bak_filename = "bak_" + filename
		bak_path = os.path.join(path, bak_filename)
		if os.path.exists(bak_path):
			os.remove(bak_path)
		shutil.copy2(self.input_db_file,bak_path)

	def deleteRecordWithSQL(self, sql):
		with sqlite3.connect(self.input_db_file) as conn:
			curs = conn.cursor()
			curs.execute(sql)
			conn.commit()

	def deleteRecordWithID(self, id):
		deleteSQL = '''DELETE FROM data WHERE _id = %d''' % id
		self.deleteRecordWithSQL(deleteSQL)

	def parsingDataTableByLoadLibrary(self):
		parsingByLoadLibrary(self.deviceInfo,
												 SCAN_TYPE_CONTACTS,
												 self.input_db_file,
												 self.output_db_file)

	def fetchallWithSQL(self, db_file, sql):
		with sqlite3.connect(db_file) as conn:
			curs = conn.cursor()
			conn.text_factory = lambda x: unicode(x, "UTF-8", "ignore")
			curs.execute(sql)
			return curs.fetchall()

	def fetchallDefault(self, db_file):
		sql = "SELECT " + default_cols + " FROM data"
		self.fetchallWithSQL(db_file, sql)

	def checkResultWithTestDataNum(self, testData, num):
		results = self.fetchallDefault(self.output_db_file)
		self.assertTrue(testData[num] in results,
			"Could not find testData[%d]" % num)

	def testDefaultCols(self):
		testData = (
			(6, 1, "Tom Smith", "Tom", "Smith"),
			(6, 2, "Steven Gates", "Steven", "Gates"))

		deleteRecordID = 2
		self.insertNormalTestData(testData)
		self.backupDatabaseBeforDeleting()
		self.deleteRecordWithID(deleteRecordID)
		self.parsingDataTableByLoadLibrary()
		self.checkResultWithTestDataNum(testData, deleteRecordID-1)

	def testFullCols(self):
		testData = (
			(1, 6, 1, 1, 1, 10, "data1", "data2", "data3", "data4", "data5", "data6",
				"data7", "data8", "data9", "data10", "data11", "data12", "data13",
				"data14", "data15", "data_sync1", "data_sync2", "data_sync3",
				"data_sync4"),
			(2, 6, 2, 1, 1, 11, "deleted data1", "deleted data2", "deleted data3",
				"deleted data4", "deleted data5", "deleted data6", "deleted data7",
				"deleted data8", "deleted data9", "deleted data10", "deleted data11",
				"deleted data12", "deleted data13", "deleted data14", "deleted data15",
				"deleted data_sync1", "deleted data_sync2", "deleted data_sync3",
				"deleted data_sync4"))

		deleteRecordID = 2

		insertSQL = "INSERT INTO data (" + full_cols + ") VALUES (" + \
			(len(testData[0])-1) * "?," + "?)"
		self.insertTestDataWithSQL(insertSQL, testData)
		self.backupDatabaseBeforDeleting()
		self.deleteRecordWithID(deleteRecordID)
		self.parsingDataTableByLoadLibrary()

		querySQL = "SELECT " + full_cols + " FROM data"
		results = self.fetchallWithSQL(self.output_db_file, querySQL)

		self.assertIn(testData[deleteRecordID-1], results)

	def testDeleteSomeRecordOfOneContact(self):
		self.fail()

	def testDeleteSomeRecordOfSomeContacts(self):
		self.fail()

	def testDeleteAllRecordOfOneContact(self):
		testData = (
			(6, 1, "something", "", ""),
			(6, 2, "First Last", "First", "Last"),
			(5, 3, "not important", "", ""),
			(0, 2, "1234567", "2", None), # phone
			(0, 2, "test@email.com", "1", None), # email, nearby
			(1, 4, "1", "2", "3"),
			(0, 2, "3", None, "Family"), # group
			(12, 5, "111", "222", "333"))

		self.insertNormalTestData(testData)
		self.backupDatabaseBeforDeleting()
		deleteSQL = "DELETE FROM data WHERE raw_contact_id = 2"
		self.deleteRecordWithSQL(deleteSQL)
		self.parsingDataTableByLoadLibrary()
		results = self.fetchallDefault(self.output_db_file)
		for n in xrange(testData):
			if testData[n][1] == 2:
				self.assertIn(testData[n], results)

	def testDeleteAllRecordOfContacts(self):
		self.fail()

	def testNameDel5ContinousRecord(self):
		"""Delete the records which id is  2,3,4,5,6"""
		testData = (
			(6, 1, "Tom Smith", "Tom", "Smith"),
			(6, 2, "Steven Gates", "Steven", "Gates"),
			(6, 3, "Jack Joe", "Jack", "Joe"),
			(6, 4, "Hellen Walls", "Hellen", "Walls"),
			(6, 5, "Mary Larry", "Mary", "Larry"),
			(6, 6, "Ken Kaven", "Ken", "Kaven"))

		deleteRecordID = 2

		self.insertNormalTestData(testData)
		self.backupDatabaseBeforDeleting()

		for n in xrange(2, len(testData)+1):
			self.deleteRecordWithID(n)

		self.parsingDataTableByLoadLibrary()

		for n in xrange(2, len(testData)+1):
			self.checkResultWithTestDataNum(testData, n-1)

	def testNameDelIntermittently(self):
		"""Delete the records which id is  2,4,6"""
		testData = (
			(6, 1, "Tom Smith", "Tom", "Smith"),
			(6, 2, "Steven Gates", "Steven", "Gates"),
			(6, 3, "Jack Joe", "Jack", "Joe"),
			(6, 4, "Hellen Walls", "Hellen", "Walls"),
			(6, 5, "Mary Larry", "Mary", "Larry"),
			(6, 6, "Ken Kaven", "Ken", "Kaven"))

		self.insertNormalTestData(testData)
		self.backupDatabaseBeforDeleting()

		for n in xrange(2, len(testData)+1, 2):
			self.deleteRecordWithID(n)

		self.parsingDataTableByLoadLibrary()

		for n in xrange(2, len(testData)+1, 2):
			self.checkResultWithTestDataNum(testData, n-1)

	def tmplWithRandomString(self, data_length):
		testData = []
		for i in xrange(data_length):
			testData.append((random.randint(1,15),
											 random.randint(1, 1000),
											 randStr(), randStr(), randStr()))

		self.insertNormalTestData(testData)
		src_db_results = self.fetchallDefault(self.input_db_file)
		self.backupDatabaseBeforDeleting()

		# Delete 2,4,6,8,...
		for n in xrange(2, len(testData), 2):
			self.deleteRecordWithID(n)

		self.parsingDataTableByLoadLibrary()

		# Find deleted records: 2,4,6,8,...
		for n in xrange(2, len(testData), 2):
			results = self.fetchallDefault(self.output_db_file)
			self.assertTrue(testData[n] in results,
				"Could not find the deleted Record _id: %d" % n)

		# Find existed records: 1,3,5,7,...
		for n in xrange(1, len(testData), 2):
			results = self.fetchallDefault(self.output_db_file)
			self.assertGreaterEqual(len(results), len(src_db_results))
			self.assertTrue(testData[n] in results,
				"Could not find the exists Record _id: %d" % n)

	def testRandomLettersDigitsAndWhiteSpaceString10(self):
		self.tmplWithRandomString(10)

	def testRandomLettersDigitsAndWhiteSpaceString100(self):
		self.tmplWithRandomString(100)

	def testRandomLettersDigitsAndWhiteSpaceString200(self):
		self.tmplWithRandomString(200)

	# TODO: too ugly...
	def tmplWithRandomString2(self, data_length):
		testData = []
		for i in xrange(data_length):
			testData.append((random.randint(1,15),
											 random.randint(1, 1000),
											 randStr2(), randStr2(), randStr2()))

		self.insertNormalTestData(testData)
		src_db_results = self.fetchallDefault(self.input_db_file)
		self.backupDatabaseBeforDeleting()

		# Delete 2,4,6,8,...
		for n in xrange(2, len(testData), 2):
			self.deleteRecordWithID(n)

		self.parsingDataTableByLoadLibrary()

		# Find deleted records: 2,4,6,8,...
		for n in xrange(2, len(testData), 2):
			results = self.fetchallDefault(self.output_db_file)
			self.assertTrue(testData[n] in results,
				"Could not find the deleted Record _id: %d" % n)

		# Find existed records: 1,3,5,7,...
		for n in xrange(1, len(testData), 2):
			results = self.fetchallDefault(self.output_db_file)
			self.assertGreaterEqual(len(results), len(src_db_results))
			self.assertTrue(testData[n] in results,
				"Could not find the exists Record _id: %d" % n)

	def testRandomPrintableString10(self):
		self.tmplWithRandomString2(10)

	def testRandomPrintableString50(self):
		self.tmplWithRandomString2(50)

	def testRandomPrintableString100(self):
		self.tmplWithRandomString2(100)

	def testRandomPrintableString200(self):
		self.tmplWithRandomString2(200)

	def testNameInFirstName(self):
		self.fail()

	def testNameWithPhoto(self):
		self.fail()

if __name__ == '__main__':
	unittest.main()
