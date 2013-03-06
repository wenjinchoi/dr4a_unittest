# -*- coding: UTF-8 -*-

import os
import random
import shutil
import sqlite3
import unittest

from loadFunction import parsingByLoadLibrary, SCAN_TYPE_CONTACTS, Scanner
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

		# TEST IT
		# Use Scanner Class. I want only import Interface |Scanner|
		if False:
			scanner = Scanner(self.deviceInfo,
												self.input_db_file,
												self.output_db_file)
			scanner.set_scan_type_contacts()
			scanner.start()

	def fetchallWithSQL(self, db_file, sql):
		with sqlite3.connect(db_file) as conn:
			curs = conn.cursor()
			conn.text_factory = lambda x: unicode(x, "UTF-8", "ignore")
			curs.execute(sql)
			return curs.fetchall()

	def fetchallDefault(self, db_file):
		sql = "SELECT " + default_cols + " FROM data"
		return self.fetchallWithSQL(db_file, sql)

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

	@unittest.skip("Not support Empty Text")
	def testEmptyText(self):
		testData = (
			(6, 1, "something", None, ""),
			(6, 2, "Name", "Empty Text at right ->", ""))
			# Could find empty text | "" |, not null value

		self.insertNormalTestData(testData)
		self.backupDatabaseBeforDeleting()
		self.deleteRecordWithID(2)
		self.parsingDataTableByLoadLibrary()
		results = self.fetchallDefault(self.output_db_file)
		self.assertIn(testData[1], results)

	def testDeleteSomeRecordOfOneContact(self):
		testData = (
			(6, 1, "something", "", ""),
			(6, 2, "First Last", "First", "Last"),
			(10, 3, "not important", "", ""),
			(5, 2, "1234567", "1", None), # phone 1, _id: 4
			(1, 2, "test@email.com", "1", None), # email, nearby, _id: 5
			(11, 4, "1", "2", "3"),
			(9, 2, "3", None, "Family"), # group, _id: 7
			(12, 5, "111", "222", "333"),
			(5, 2, "800888999", "2", None),  # phone 2, _id: 8
			(11, 5, "http://abc.com", "", ""),
			(7, 2, "Wondershare", "1", "Saodiseng"))  # organization, _id: 10

		self.insertNormalTestData(testData)
		self.backupDatabaseBeforDeleting()
		self.deleteRecordWithID(7)  # group
		self.deleteRecordWithID(8)  # phone 2
		self.parsingDataTableByLoadLibrary()
		results = self.fetchallDefault(self.output_db_file)
		for n in xrange(len(testData)):
			if testData[n][1] == 2:
				self.assertIn(testData[n], results)

	def testDeleteSomeRecordOfSomeContacts(self):
		testData = (
			(6, 1, "begining", "", ""),
			(6, 2, "First Last", "First", "Last"),   # person 1, name
			(10, 257, "not important", "a", "b"),
			(5, 2, "1234567", "1", None),            # person 1, phone 1
			(1, 2, "test@email.com", "1", None),     # person 1, email
			(6, 3, "Person 2", "Person", "2"),       # person 2, name
			(11, 4, "1", "2", "3"),
			(9, 2, "3", None, "Family"),             # person 1, group
			(5, 3, "2223333", "1", None),            # person 2, phone
			(5, 2, "800888999", "2", None),          # person 1, phone 2
			(6, 5, "Bob Hill", "Bob", "Hill"),
			(11, 3, "http://abc.com", "7", None),    # person 2, website
			(7, 2, "Wondershare", "1", "Saodiseng")) # person 1, organization

		self.insertNormalTestData(testData)
		self.backupDatabaseBeforDeleting()
		deleteSQL = "DELETE FROM data WHERE raw_contact_id = 2" \
		 						" OR raw_contact_id = 3"
		self.deleteRecordWithSQL(deleteSQL)
		self.parsingDataTableByLoadLibrary()
		results = self.fetchallDefault(self.output_db_file)
		for n in xrange(len(testData)):
			if testData[n][1] == 2 or testData[n][1] == 3:
				self.assertIn(testData[n], results)

	def testDeleteAllRecordOfOneContact(self):
		testData = (
			(6, 1, "something", "", ""),
			(6, 2, "First Last", "First", "Last"),
			(10, 3, "not important", "", ""),
			(5, 2, "1234567", "1", None), # phone 1, _id: 4
			(1, 2, "test@email.com", "1", None), # email, nearby, _id: 5
			(11, 4, "1", "2", "3"),
			(9, 2, "3", None, "Family"), # group, _id: 7
			(12, 5, "111", "222", "333"),
			(5, 2, "800888999", "2", None),  # phone 2, _id: 8
			(11, 5, "http://abc.com", "", ""),
			(7, 2, "Wondershare", "1", "Saodiseng"))  # organization, _id: 10

		self.insertNormalTestData(testData)
		self.backupDatabaseBeforDeleting()
		deleteSQL = "DELETE FROM data WHERE raw_contact_id = 2"
		self.deleteRecordWithSQL(deleteSQL)
		self.parsingDataTableByLoadLibrary()
		results = self.fetchallDefault(self.output_db_file)
		for n in xrange(len(testData)):
			if testData[n][1] == 2:
				self.assertIn(testData[n], results)

	def testDeleteAllRecordOfContacts(self):
		testData = (
			(6, 1, "begining", "begining", None),
			(6, 2, "First Last", "First", "Last"),   # person 1, name
			(10, 257, "not important", "a", "b"),
			(5, 2, "1234567", "1", None),            # person 1, phone 1
			(1, 2, "test@email.com", "1", None),     # person 1, email
			(6, 3, "Person 2", "Person", "2"),       # person 2, name
			(11, 4, "1", "2", "3"),
			(9, 2, "3", None, "Family"),             # person 1, group
			(5, 3, "2223333", "1", None),            # person 2, phone
			(5, 2, "800888999", "2", None),          # person 1, phone 2
			(6, 5, "Bob Hill", "Bob", "Hill"),
			(11, 3, "http://abc.com", "7", None),    # person 2, website
			(7, 2, "Wondershare", "1", "Saodiseng")) # person 1, organization

		self.insertNormalTestData(testData)
		self.backupDatabaseBeforDeleting()
		deleteSQL = "DELETE FROM data"
		self.deleteRecordWithSQL(deleteSQL)
		self.parsingDataTableByLoadLibrary()
		results = self.fetchallDefault(self.output_db_file)
		for n in xrange(len(testData)):
			self.assertIn(testData[n], results)

	# 删除5条连续的记录
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

	# 间断地删除记录
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
			testData.append((random.randint(1, 15),
											 random.randint(1, 100),
											 randStr3(), randStr3(), randStr3()))
		testData = tuple(testData)

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
			self.assertIn(src_db_results[n], results)

		# Find existed records: 1,3,5,7,...
		for n in xrange(1, len(testData), 2):
			results = self.fetchallDefault(self.output_db_file)
			self.assertGreaterEqual(len(results), len(src_db_results))
			self.assertIn(src_db_results[n], results)

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
											 random.randint(1, 100),
											 randStr2(), randStr2(), randStr2()))
		testData = tuple(testData)

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
			self.assertIn(testData[n], results)

		# Find existed records: 1,3,5,7,...
		for n in xrange(1, len(testData), 2):
			results = self.fetchallDefault(self.output_db_file)
			self.assertGreaterEqual(len(results), len(src_db_results))
			self.assertTrue(testData[n], results)

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
		with open("./res/pic.jpg") as f:
			data15 = buffer(f.read())

		testData = (
			(6, 1, "Tom Smith", "Tom", "Smith", None),
			(4, 1, None, None, None, data15),
			(5, 1, "123456", None, None, None))

		insertSQL = "INSERT INTO data (%s,data15) " \
			"VALUES(?,?,?,?,?,?)" % default_cols
		self.insertTestDataWithSQL(insertSQL, testData)
		self.backupDatabaseBeforDeleting()
		self.deleteRecordWithID(2)
		self.parsingDataTableByLoadLibrary()

		fetchSQL = "SELECT %s,data15 FROM data" % default_cols
		results = self.fetchallWithSQL(self.output_db_file, fetchSQL)

		self.assertIn(testData[1], results)

	def testDeleteOneRecordAndInsertOneRecord(self):
		testData1 = (
			(6, 1, "begining", "bein", "ing"),
			(10,1, 50 * "a", None, None),
			(5, 2, "1234567", "1", None))

		testData2 = ((5, 1, "123456", None, None),)

		self.insertNormalTestData(testData1)
		sqlpage = getFirstPage(self.input_db_file)
		record2_size = recordSize(sqlpage, 2)

		self.deleteRecordWithID(2)
		self.insertNormalTestData(testData2)
		self.backupDatabaseBeforDeleting()

		self.parsingDataTableByLoadLibrary()

		fetchSQL = "SELECT data1 FROM data WHERE _id = 2"
		result = self.fetchallWithSQL(self.output_db_file, fetchSQL)
		self.assertLess((50 - record2_size + 2) * "a", result[0])

		existed_results = self.fetchallDefault(self.output_db_file)
		for n in xrange(len(testData1)):
			self.assertIn(testData1[n], existed_results)

	def testDeletedOneRecordAndInsertTwoRecords(self):
		testData1 = (
			(6, 1, "begining", "bein", "ing"),
			(10,1, 100 * "a", None, None),
			(5, 2, "1234567", "1", None))

		testData2 = (
			(5, 1, "123456", None, None),
			(6, 2, "OneName", None, None))

		self.insertNormalTestData(testData1)
		sqlpage = getFirstPage(self.input_db_file)

		self.deleteRecordWithID(2)
		self.insertNormalTestData((testData2[0],))
		recordSize_1 = lastRecordSize(self.input_db_file)
		self.insertNormalTestData((testData2[1],))
		recordSize_2 = lastRecordSize(self.input_db_file)

		self.backupDatabaseBeforDeleting()

		self.parsingDataTableByLoadLibrary()

		fetchSQL = "SELECT data1 FROM data WHERE _id = 2"
		result = self.fetchallWithSQL(self.output_db_file, fetchSQL)
		self.assertLess((100 - recordSize_1 - recordSize_2) * "a", result[0])

		existed_results = self.fetchallDefault(self.output_db_file)
		for n in xrange(len(testData1)):
			self.assertIn(testData[1], existed_results)

	def testInsert1200AndRandomDelete500(self):
		photoTestData = []
		with open("./res/pic.jpg") as f:
			data15 = buffer(f.read())
		for n in xrange(200):
			photoTestData.append((6, random.randint(1,200),None, None, None, data15))

		testData = []
		for n in xrange(500):
			# Name or Full data1 to data3
			testData.append((random.randint(1,15),
											 random.randint(1,200),
											 randomLettersDigitsBlank(20),
											 randomLettersDigitsBlank(10),
											 randomLettersDigitsBlank(10), None))
			# Phone or Full data1 to data3
			testData.append((random.randint(1,15),
											 random.randint(1,200),
											 randDig(),
											 str(random.randint(0,9)),
											 None, None))

		testData.extend(photoTestData)
		random.shuffle(testData)
		testData = tuple(testData)

		insertSQL = "INSERT INTO data (%s,data15) " \
			"VALUES(?,?,?,?,?,?)" % default_cols
		self.insertTestDataWithSQL(insertSQL, testData)
		self.backupDatabaseBeforDeleting()

		id_list = [x for x in xrange(len(testData))]
		random.shuffle(id_list)
		for n in id_list[:500]:
			self.deleteRecordWithID(id_list[n])

		self.parsingDataTableByLoadLibrary()

		fetchSQL = "SELECT %s,data15 FROM data" % default_cols
		results = self.fetchallWithSQL(self.output_db_file, fetchSQL)

		for n in xrange(len(testData)):
			self.assertIn(testData[n], results)

	# May be almost same with the previous one.
	def testInsert200ContactsIDAndDelete50(self):
		photoTestData = []
		with open("./res/pic.jpg") as f:
			data15 = buffer(f.read())
		for n in xrange(200):
			photoTestData.append((6, random.randint(1,200),None, None, None, data15))

		testData = []
		for n in xrange(500):
			# Name or Full data1 to data3
			testData.append((random.randint(1,15),
											 random.randint(1,200),
											 randomLettersDigitsBlank(20),
											 randomLettersDigitsBlank(10),
											 randomLettersDigitsBlank(10), None))
			# Phone or Full data1 to data3
			testData.append((random.randint(1,15),
											 random.randint(1,200),
											 randDig(),
											 str(random.randint(0,9)),
											 None, None))

		testData.extend(photoTestData)
		random.shuffle(testData)
		testData = tuple(testData)

		insertSQL = "INSERT INTO data (%s,data15) " \
			"VALUES(?,?,?,?,?,?)" % default_cols
		self.insertTestDataWithSQL(insertSQL, testData)
		self.backupDatabaseBeforDeleting()

		# Random delete 50 contacts_id
		contacts_id_list = [str(x) for x in xrange(200)]
		random.shuffle(contacts_id_list)
		for x in id_list[:50]:
			deleteSQL = "DELETE FROM data WHERE raw_contact_id = %s" % x
			self.deleteRecordWithSQL(deleteSQL)

		self.parsingDataTableByLoadLibrary()

		fetchSQL = "SELECT %s,data15 FROM data" % default_cols
		results = self.fetchallWithSQL(self.output_db_file, fetchSQL)

		for n in xrange(len(testData)):
			self.assertIn(testData[n], results)

	def testDeleteMoreThanOnePageWithAutoVacuum(self):
		createDB(self.input_db_file, self.schema, auto_vacuum = 1)
		filesize = os.path.getsize(self.input_db_file)
		pagesize = filesize/4

		testData = []
		length = 200
		for n in xrange(length):
			testData.append((random.randint(1,15),
											 random.randint(1,200),
											 randomLettersDigitsBlank(20),
											 randomLettersDigitsBlank(10),
											 randomLettersDigitsBlank(10)))

		testData = tuple(testData)
		self.insertNormalTestData(testData)
		self.backupDatabaseBeforDeleting()

		newfilesize = os.path.getsize(self.input_db_file)
		increment_pages = (newfilesize - filesize) / pagesize
		record_nums_per_page = length/increment_pages

		# can found data at [found_start, deleted_end]
		# 1.7 and 1.3 is estimated value
		deleted_end = int(record_nums_per_page * 1.7)
		found_start = int(record_nums_per_page * 1.3)

		for n in xrange(deleted_end):
			self.deleteRecordWithID(n)

		self.parsingDataTableByLoadLibrary()

		results = self.fetchallDefault(self.output_db_file)

		for n in xrange(found_start, length):
			self.assertIn(testData[n], results,
				"testData[%d] not found in results. \n" % n \
				+ "records per page is about: %d \n" % record_nums_per_page \
				+ "delete records from 0 to %d \n" % deleted_end \
				+ "find records from %d to %d" % (found_start, length))

	# May be almost same with the previous one.
	def testDeleteAllWithAutoVacuum(self):
		createDB(self.input_db_file, self.schema, auto_vacuum = 1)
		filesize = os.path.getsize(self.input_db_file)
		pagesize = filesize/4

		testData = []
		length = 200
		for n in xrange(length):
			testData.append((random.randint(1,15),
											 random.randint(1,200),
											 randomLettersDigitsBlank(20),
											 randomLettersDigitsBlank(10),
											 randomLettersDigitsBlank(10)))

		testData = tuple(testData)
		self.insertNormalTestData(testData)
		self.backupDatabaseBeforDeleting()

		newfilesize = os.path.getsize(self.input_db_file)
		increment_pages = (newfilesize - filesize) / pagesize
		record_nums_per_page = length/increment_pages

		# I'm not sure which records will keep
		# The begin or end?
		deleteSQL = "DELETE FROM data WHERE 1=1"
		self.deleteRecordWithSQL(deleteSQL)

		self.parsingDataTableByLoadLibrary()

		results = self.fetchallDefault(self.output_db_file)

		# Could find the end page?
		found_start = int(record_nums_per_page * ((increment_pages - 1) + 0.2))
		for n in xrange(found_start, length):
			self.assertIn(testData[n], results,
				"testData[%d] not found in results. \n" % n \
				+ "records per page is about: %d \n" % record_nums_per_page \
				+ "delete all records \n" \
				+ "find records from %d to %d" % (found_start, length))


if __name__ == '__main__':
	unittest.main()
