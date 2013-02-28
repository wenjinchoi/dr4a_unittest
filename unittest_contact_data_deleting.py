# -*- coding: UTF-8 -*-

import os
import random
import sqlite3
import unittest

from loadFunction import parsingByLoadLibrary, SCAN_TYPE_CONTACTS
from templates import testDeviceOfContacts
from sqlite_utils import *


from valueMaker import *

def random_str(randomlength=8):
    a = list(string.ascii_letters)
    random.shuffle(a)
    return ''.join(a[:randomlength])


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

	def fetchallData1_3(self, db_file):
		with sqlite3.connect(db_file) as conn:
			curs = conn.cursor()
			conn.text_factory = str
			querySQL = '''SELECT mimetype_id,raw_contact_id,data1,data2,data3
				FROM data'''
			curs.execute(querySQL)
			results = curs.fetchall()
			return results

	def checkResultWithTestDataNum(self, testData, num):
		results = self.fetchallData1_3(self.output_db_file)
		self.assertTrue(testData[num] in results,
			"Could not find testData[%d]" % num)

	def testNameBasic(self):
		testData = (
			(6, 1, "Tom Smith", "Tom", "Smith"),
			(6, 2, "Steven Gates", "Steven", "Gates"))

		deleteRecordID = 2
		self.insertNormalTestData(testData)
		self.deleteDataTableWith_ID(deleteRecordID)
		self.parsingDataTableByLoadLibrary()
		self.checkResultWithTestDataNum(testData, deleteRecordID-1)

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

		for n in xrange(2, len(testData)+1):
			self.deleteDataTableWith_ID(n)

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

		for n in xrange(2, len(testData)+1, 2):
			self.deleteDataTableWith_ID(n)

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
		src_db_results = self.fetchallData1_3(self.input_db_file)

		# Delete 2,4,6,8,...
		for n in xrange(2, len(testData), 2):
			self.deleteDataTableWith_ID(n)

		self.parsingDataTableByLoadLibrary()

		# Find deleted records: 2,4,6,8,...
		for n in xrange(2, len(testData), 2):
			results = self.fetchallData1_3(self.output_db_file)
			self.assertTrue(testData[n] in results,
				"Could not find the deleted Record _id: %d" % n)

		# Find existed records: 1,3,5,7,...
		for n in xrange(1, len(testData), 2):
			results = self.fetchallData1_3(self.output_db_file)
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
		src_db_results = self.fetchallData1_3(self.input_db_file)

		# Delete 2,4,6,8,...
		for n in xrange(2, len(testData), 2):
			self.deleteDataTableWith_ID(n)

		self.parsingDataTableByLoadLibrary()

		# Find deleted records: 2,4,6,8,...
		for n in xrange(2, len(testData), 2):
			results = self.fetchallData1_3(self.output_db_file)
			self.assertTrue(testData[n] in results,
				"Could not find the deleted Record _id: %d" % n)

		# Find existed records: 1,3,5,7,...
		for n in xrange(1, len(testData), 2):
			results = self.fetchallData1_3(self.output_db_file)
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
		pass

	def testNameWithPhoto(self):
		pass

if __name__ == '__main__':
	unittest.main()
