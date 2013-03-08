# -*- coding: UTF-8 -*-

import os
import random
import shutil
import sqlite3
import unittest

from templates import testDeviceOfContacts
from templates.contacts_table_columns import *

from utils.sqlitefile_utils import *
from utils.valueMaker import *
from utils.loadFunction import parsingByLoadLibrary, SCAN_TYPE_CONTACTS

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
			# conn.text_factory = str
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

		# Not Complete.
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
			conn.text_factory = lambda x: unicode(x, "UTF-8", "replace")
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
		self.assertTrue(isTableExists(self.output_db_file, "data"))
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
		self.assertTrue(isTableExists(self.output_db_file, "data"))

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
		self.assertTrue(isTableExists(self.output_db_file, "data"))
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
		self.assertTrue(isTableExists(self.output_db_file, "data"))
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
		self.assertTrue(isTableExists(self.output_db_file, "data"))
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
		self.assertTrue(isTableExists(self.output_db_file, "data"))
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
		self.assertTrue(isTableExists(self.output_db_file, "data"))
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
		self.assertTrue(isTableExists(self.output_db_file, "data"))

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
		self.assertTrue(isTableExists(self.output_db_file, "data"))

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
		self.assertTrue(isTableExists(self.output_db_file, "data"))

		# Find existed records id: 1,3,5,7,...
		results = self.fetchallDefault(self.output_db_file)
		for n in xrange(2, len(testData), 2):
			self.assertIn(src_db_results[n], results)

		# Find deleted records id: 2,4,6,8,...
		not_found_count = 0.0
		for n in xrange(1, len(testData), 2):
			if src_db_results[n] not in results:
				not_found_count += 1
		not_found_radio = not_found_count/(data_length-4)
		self.assertLessEqual(not_found_radio, 0.1)

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
		self.assertTrue(isTableExists(self.output_db_file, "data"))

		results = self.fetchallDefault(self.output_db_file)
		# Find existed records id: 1,3,5,7,...
		for n in xrange(2, len(testData), 2):
			self.assertIn(testData[n], results)

		# Find deleted records id : 2,4,6,8,...
		not_found_count = 0.0
		for n in xrange(1, len(testData), 2):
			if src_db_results[n] not in results:
				not_found_count += 1
		not_found_radio = not_found_count/(data_length-4)
		self.assertLessEqual(not_found_radio, 0.1)

	def testRandomPrintableString10(self):
		self.tmplWithRandomString2(10)

	def testRandomPrintableString50(self):
		self.tmplWithRandomString2(50)

	def testRandomPrintableString100(self):
		self.tmplWithRandomString2(100)

	def testRandomPrintableString200(self):
		self.tmplWithRandomString2(200)

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
		self.assertTrue(isTableExists(self.output_db_file, "data"))

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
		self.assertTrue(isTableExists(self.output_db_file, "data"))

		fetchSQL = "SELECT data1 FROM data WHERE _id = 2"
		result = self.fetchallWithSQL(self.output_db_file, fetchSQL)
		self.assertGreater(len(result), 0)
		self.assertLess((50 - record2_size + 2) * "a", result[0])

		existed_results = self.fetchallDefault(self.output_db_file)
		for n in xrange(len(testData1)):
			if n == 1: continue
			self.assertIn(testData1[n], existed_results)

	def testDeletedOneRecordAndInsertTwoRecords(self):
		testData1 = (
			(6, 1, "begining", "bein", "ing"),
			(10,1, 200 * "a", None, None),
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
		self.assertTrue(isTableExists(self.output_db_file, "data"))

		fetchSQL = "SELECT data1 FROM data WHERE isdeleted = 1"
		result = self.fetchallWithSQL(self.output_db_file, fetchSQL)
		self.assertGreater(len(result), 0, "could not found any delete record")
		self.assertLess((200 - recordSize_1 - recordSize_2) * "a", result[0])

		existed_results = self.fetchallDefault(self.output_db_file)
		for n in xrange(len(testData1)):
			if n == 1: continue
			self.assertIn(testData1[n], existed_results)
		for n in xrange(len(testData2)):
			self.assertIn(testData2[n], existed_results)

	def testInsert700AndRandomDelete300(self):
		photoTestData = []
		with open("./res/pic.jpg") as f:
			data15 = buffer(f.read())
		for n in xrange(100):
			photoTestData.append((6, random.randint(1,200),None, None, None, data15))

		testData = []
		for n in xrange(300):
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
		for n in id_list[:300]:
			self.deleteRecordWithID(id_list[n])

		self.parsingDataTableByLoadLibrary()
		self.assertTrue(isTableExists(self.output_db_file, "data"))

		fetchSQL = "SELECT %s,data15 FROM data" % default_cols
		results = self.fetchallWithSQL(self.output_db_file, fetchSQL)

		not_found_count = 0.0
		for n in xrange(len(testData)):
			if testData[n] not in results:
				not_found_count += 1

		self.assertTrue(not_found_count/len(testData) < 0.03,
				"not found records greater than 3%")

	# May be almost same with the previous one.
	# Sometimes Failed.
	def testInsert200ContactsIDAndDelete50(self):
		photoTestData = []
		with open("./res/pic.jpg") as f:
			data15 = buffer(f.read())
		for n in xrange(100):
			photoTestData.append((6, random.randint(1,200),None, None, None, data15))

		testData = []
		for n in xrange(300):
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
		for x in contacts_id_list[:50]:
			deleteSQL = "DELETE FROM data WHERE raw_contact_id = %s" % x
			self.deleteRecordWithSQL(deleteSQL)

		self.parsingDataTableByLoadLibrary()
		self.assertTrue(isTableExists(self.output_db_file, "data"))

		fetchSQL = "SELECT %s,data15 FROM data" % default_cols
		results = self.fetchallWithSQL(self.output_db_file, fetchSQL)

		not_found_count = 0.0
		for n in xrange(len(testData)):
			if testData[n] not in results:
				not_found_count += 1

		self.assertTrue(not_found_count/len(testData) < 0.03,
				"not found records greater than 3%")

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
		# 1.8 and 1.45 is estimated value
		deleted_end = int(record_nums_per_page * 1.8)
		found_start = int(record_nums_per_page * 1.45)

		for n in xrange(deleted_end):
			self.deleteRecordWithID(n)

		self.parsingDataTableByLoadLibrary()
		self.assertTrue(isTableExists(self.output_db_file, "data"))

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
		self.assertTrue(isTableExists(self.output_db_file, "data"))

		results = self.fetchallDefault(self.output_db_file)

		# Could find the end page?
		found_start = int(length - record_nums_per_page)

		for n in xrange(found_start, length):
				self.assertIn(testData[n], results,
					"testData[%d] not found in results. \n" % n \
					+ "records per page is about: %d \n" % record_nums_per_page \
					+ "delete all records \n" \
					+ "find records from %d to %d" % (found_start, length))

	def testDeletedRecordBeforeValidCells(self):
		testData1 = (
			(6, 1, "Tom Smith", "Tom", "Smith"),
			(6, 2, "Steven Gates", "Steven", "Gates"), #del, overwrite, can not found
			(6, 3, "Jack Johnao", "Jack", "Johnao"),   #del, overwrite, can not found
			(6, 4, "Hellen Walls", "Hellen", "Walls"))

		testData2 = (
			(6, 5, "Mary Larry", "Mary", "Larry"),
			(6, 6, "Ken Kaven", "Ken", "Kaven"))

		self.insertNormalTestData(testData1)
		self.deleteRecordWithID(2)
		self.deleteRecordWithID(3)
		self.deleteRecordWithID(4)
		self.insertNormalTestData(testData2)

		self.parsingDataTableByLoadLibrary()
		self.assertTrue(isTableExists(self.output_db_file, "data"))

		results = self.fetchallDefault(self.output_db_file)

		self.assertIn(testData1[0], results)
		self.assertIn(testData1[3], results)
		self.assertIn(testData2[0], results)
		self.assertIn(testData2[1], results)

# Extend the Device Test Case
class samsung_GT_I9001_2_3_6_TestCase(ContactsDataTableDeletedTestCase):
	def setUp(self):
		self.initWithDeiveAndSchema(testDeviceOfContacts.testDevice2)

class samsung_GT_i897or9000_2_3_4_TestCase(ContactsDataTableDeletedTestCase):
	def setUp(self):
		self.initWithDeiveAndSchema(testDeviceOfContacts.testDevice3)

class samsung_gt_i9003_2_3_5_TestCase(ContactsDataTableDeletedTestCase):
	def setUp(self):
		self.initWithDeiveAndSchema(testDeviceOfContacts.testDevice4)

class samsung_gt_i9300_4_1_2_TestCase(ContactsDataTableDeletedTestCase):
	def setUp(self):
		self.initWithDeiveAndSchema(testDeviceOfContacts.testDevice5)

class samsung_gt_n7000_4_0_3_TestCase(ContactsDataTableDeletedTestCase):
	def setUp(self):
		self.initWithDeiveAndSchema(testDeviceOfContacts.testDevice6)

class samsung_GT_N7000_4_0_4_TestCase(ContactsDataTableDeletedTestCase):
	def setUp(self):
		self.initWithDeiveAndSchema(testDeviceOfContacts.testDevice7)

class samsung_gt_n7100_4_1_1_TestCase(ContactsDataTableDeletedTestCase):
	def setUp(self):
		self.initWithDeiveAndSchema(testDeviceOfContacts.testDevice8)

class samsung_GT_N8000_4_1_1_TestCase(ContactsDataTableDeletedTestCase):
	def setUp(self):
		self.initWithDeiveAndSchema(testDeviceOfContacts.testDevice9)

class samsung_P5100_4_0_3_TestCase(ContactsDataTableDeletedTestCase):
	def setUp(self):
		self.initWithDeiveAndSchema(testDeviceOfContacts.testDevice10)

class samsung_SCH_I909_2_2_2_TestCase(ContactsDataTableDeletedTestCase):
	def setUp(self):
		self.initWithDeiveAndSchema(testDeviceOfContacts.testDevice11)

class samsung_SGH_I927_4_0_4_TestCase(ContactsDataTableDeletedTestCase):
	def setUp(self):
		self.initWithDeiveAndSchema(testDeviceOfContacts.testDevice12)

class Samsung_SGH_I997_2_2_1_TestCase(ContactsDataTableDeletedTestCase):
	def setUp(self):
		self.initWithDeiveAndSchema(testDeviceOfContacts.testDevice13)

class samsung_SGH_T759_2_3_3_TestCase(ContactsDataTableDeletedTestCase):
	def setUp(self):
		self.initWithDeiveAndSchema(testDeviceOfContacts.testDevice14)

class samsung_SPH_D710_4_0_4_TestCase(ContactsDataTableDeletedTestCase):
	def setUp(self):
		self.initWithDeiveAndSchema(testDeviceOfContacts.testDevice15)

class samsung_GT_9100_4_0_4_TestCase(ContactsDataTableDeletedTestCase):
	def setUp(self):
		self.initWithDeiveAndSchema(testDeviceOfContacts.testDevice16)

class samsung_GT_9250_4_2_2_TestCase(ContactsDataTableDeletedTestCase):
	def setUp(self):
		self.initWithDeiveAndSchema(testDeviceOfContacts.testDevice17)

class samsung_GT_I9000_2_3_4_TestCase(ContactsDataTableDeletedTestCase):
	def setUp(self):
		self.initWithDeiveAndSchema(testDeviceOfContacts.testDevice18)

class samsung_GT_I9100G_4_0_4_TestCase(ContactsDataTableDeletedTestCase):
	def setUp(self):
		self.initWithDeiveAndSchema(testDeviceOfContacts.testDevice19)

class samsung_GT_N8000_4_0_4TestCase(ContactsDataTableDeletedTestCase):
	def setUp(self):
		self.initWithDeiveAndSchema(testDeviceOfContacts.testDevice20)

class samsung_GT_P1000_2_2_1_TestCase(ContactsDataTableDeletedTestCase):
	def setUp(self):
		self.initWithDeiveAndSchema(testDeviceOfContacts.testDevice21)

class samsung_GT_P7500_4_0_4_TestCase(ContactsDataTableDeletedTestCase):
	def setUp(self):
		self.initWithDeiveAndSchema(testDeviceOfContacts.testDevice22)

class samsung_GT_S5670_2_2_1_TestCase(ContactsDataTableDeletedTestCase):
	def setUp(self):
		self.initWithDeiveAndSchema(testDeviceOfContacts.testDevice23)

class samsung_GT_S5830_2_3_4_TestCase(ContactsDataTableDeletedTestCase):
	def setUp(self):
		self.initWithDeiveAndSchema(testDeviceOfContacts.testDevice24)



if __name__ == '__main__':
	unittest.main()
