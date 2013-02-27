# -*- coding: UTF-8 -*-

import sqlite3
import os
import unittest

from sqlite_utils import *
from loadFunction import parsingMmssmsByLoadLibrary
from templates import mmssms_db_tmpl

faked = True

def fetchSMSNormalData(sqlite_file_path):
	with sqlite3.connect(sqlite_file_path) as conn:
		conn.text_factory = str
		curs = conn.cursor()
		curs.execute('''select address, thread_id, date, type, body
			from sms''')
		results = curs.fetchall()
		return results

class SMSTestCase(unittest.TestCase):

	def setUp(self):
		""" unittest 的初始化方法
		在继承类中，需要覆盖此方法以构建针对不同测试设备的 TestCase
		建议直接调用 initWithDeviceAndSchema 初始化方法
		"""
		self.initWithDeviceAndSchema(mmssms_db_tmpl.testDevice9)

	def tearDown(self):
		pass

	def initWithDeviceAndSchema(self, dictOfDeviceAndSchema):
		""" 通用的初始化函数，需要传入关于设备测试信息的dict:
					{"deviceInfo": ,
					 "schema": }
				deviceInfo 是根据设备型号信息，用于匹配解析规则，定义在 WSDBRecovery.dll 的
				头文件，在 loadFunction.py 中实现了替换类 |class DeviceInfo|, 需通过构建该类
				的对象作为此处的参数
				schema 是用于创建Table的 schema, sms 的测试至少包含 sms 和 threads Table，
				定义在 mmssms_db_tmpl
		"""
		self.faked = False

		self.deviceInfo = dictOfDeviceAndSchema["deviceInfo"]
		self.smsSchema = dictOfDeviceAndSchema["schema"]

		if not os.path.exists('./src_db'): os.mkdir('./src_db')
		if not os.path.exists('./rec_db'): os.mkdir('./rec_db')

		self.tmpdb_path = './src_db/mmssms.db'
		self.output_db_filepath = './rec_db/mmssms.db'

		createDB(self.tmpdb_path, self.smsSchema)

	def set_faked(self, isFaked):
		self.faked = isFaked

	def parsing_db(self, intput_db_file, output_db_file):
		""" 此处为实际调用程序功能的函数，若被测程序接口有变，则通过改动此函数来实现
		"""
		parsingMmssmsByLoadLibrary(self.deviceInfo,
												 			 self.tmpdb_path,
												 			 self.output_db_filepath)

	def insertAndDeleteLeftTheFirstOne(self, db_file, testData):
		""" Use for fill the database |db_file| with |testData|,
		and delete the them except the first record.
		"""
		with sqlite3.connect(db_file) as conn:
			c = conn.cursor()
			insertSQL = '''insert into sms(address, thread_id, date, type, body)
			 values (?, ?, ?, ?, ?)'''
			for n in xrange(len(testData)):
				c.execute(insertSQL, testData[n])
			c.execute('''delete from sms where _id > 1''')
			conn.commit()

	def checkAllTestData(self, db_file, testData):
		self.assertTrue(isTableExists(db_file, "sms"),
			"the sms table does not exists in recovery file")

		results = fetchSMSNormalData(db_file)

		for n in xrange(1, len(testData)):
			self.assertTrue(testData[n] in results,
				"could not find the deleted record at testData[%d]" % n)

	def setData_Process_And_Check(self, testData):
		self.insertAndDeleteLeftTheFirstOne(self.tmpdb_path, testData)
		self.parsing_db(self.tmpdb_path, self.output_db_filepath)
		self.checkAllTestData(self.output_db_filepath, testData)

	def testBase(self):
		testData = (
			('10086', 1, 1357005600, 1, 'Record 1'),
			('10086', 2, 1357005601, 1, 'Record 2'))

		self.insertAndDeleteLeftTheFirstOne(self.tmpdb_path, testData)

		#  -----  faked  -----
		def faked_process(db_file):
			createDB(db_file, self.smsSchema)
			with sqlite3.connect(db_file) as conn:
				curs = conn.cursor()
				insertSQL = '''insert into sms(address, thread_id, date, type, body)
			 		values (?, ?, ?, ?, ?)'''
				for n in xrange(len(testData)):
					curs.execute(insertSQL, testData[n])
				conn.commit()
		#  -----  faked  -----

		if not faked:
			self.parsing_db(self.tmpdb_path, self.output_db_filepath)
		else:
			faked_process(self.output_db_filepath)

		self.checkAllTestData(self.output_db_filepath, testData)

	def testOneRecordInFreeBlock(self):
		testData = (
			('10086', 1, 1357005600, 1, 'Record 1'),
			('10086', 1, 1357005601, 1, 100 * 'a'),
			('10086', 1, 1357005602, 1, 'Record 3'),
			('10086', 1, 1357005603, 1, 'Record 4'))

		with sqlite3.connect(self.tmpdb_path) as conn:
			c = conn.cursor()
			insertSQL = '''insert into sms(address, thread_id, date, type, body)
			 values (?, ?, ?, ?, ?)'''

			c.execute(insertSQL, testData[0])
			c.execute(insertSQL, testData[1])
			c.execute(insertSQL, testData[2])
			c.execute('''delete from sms where _id = 2''')
			c.execute(insertSQL, testData[3])
			conn.commit()

		lastRecordSize = lastSmsRecordSize(self.tmpdb_path)

		self.parsing_db(self.tmpdb_path, self.output_db_filepath)
		self.assertTrue(isTableExists(self.output_db_filepath, "sms"),
			"the sms table does not exists in recovery file")
		results = fetchSMSNormalData(self.output_db_filepath)

		leave_times = 100 - lastRecordSize
		self.assertTrue(
			('10086', 1, 112141782847, 5, leave_times * 'a') in results,
			"could not find the correct deleted record")

		for n in xrange(len(testData)):
			if n == 1: continue
			self.assertTrue(testData[n] in results,
				"could not find the exists record at testData[%d]" % n)

	def testTwoRecordInFreeBlock(self):
		testData = (
			('10086', 1, 1357005600, 1, 'Record 1'),
			('10086', 1, 1357005601, 1, 100 * 'a'),
			('10086', 1, 1357005602, 1, 'Record 3'),
			('10086', 1, 1357005603, 1, 'Record 4'),
			('10086', 1, 1357005604, 1, 'Record 5'))

		with sqlite3.connect(self.tmpdb_path) as conn:
			c = conn.cursor()
			insertSQL = '''insert into sms(address, thread_id, date, type, body)
			 values (?, ?, ?, ?, ?)'''

			c.execute(insertSQL, testData[0])
			c.execute(insertSQL, testData[1])
			c.execute(insertSQL, testData[2])
			c.execute('''delete from sms where _id = 2''')
			c.execute(insertSQL, testData[3])
			conn.commit()
			record_size_4 = lastSmsRecordSize(self.tmpdb_path)
			c.execute(insertSQL, testData[4])
			conn.commit()
			record_size_5 = lastSmsRecordSize(self.tmpdb_path)

		self.parsing_db(self.tmpdb_path, self.output_db_filepath)
		self.assertTrue(isTableExists(self.output_db_filepath, "sms"),
			"the sms table does not exists in recovery file")
		results = fetchSMSNormalData(self.output_db_filepath)

		times = 100 - record_size_4 - record_size_5
		self.assertTrue(('10086', 1, 112141782847, 5, times * 'a') in results)

		for n in xrange(len(testData)):
			if n == 1: continue
			self.assertTrue(testData[n] in results)

	def testDeletedRecordBeforeValidCells(self):
		testDataFirst = (
			('10086', 1, 1357005600, 1, 'Record 1'),
			('10086', 1, 1357005601, 1, 'Record 2'),
			('10086', 1, 1357005602, 1, 'Record 3'),
			('10086', 1, 1357005603, 1, 'Record 4'),
			('10086', 1, 1357005604, 1, 'Record 5'))

		testDataSecond = (
			('21197', 2, 1357005701, 1, 'New 1'),
			('21197', 2, 1357005602, 1, 'New 2'))

		with sqlite3.connect(self.tmpdb_path) as conn:
			c = conn.cursor()
			insertSQL = '''insert into sms(address, thread_id, date, type, body)
			 values (?, ?, ?, ?, ?)'''

			c.execute(insertSQL, testDataFirst[0])  # keep this
			c.execute(insertSQL, testDataFirst[1])  # delete and overwrite
			c.execute(insertSQL, testDataFirst[2])  # delete and overwrite
			c.execute(insertSQL, testDataFirst[3])  # delete, not overwrite
			c.execute(insertSQL, testDataFirst[4])  # delete, not overwrite
			c.execute('''delete from sms where _id > 1''')
			c.execute(insertSQL, testDataSecond[0]) # almost overwrite testDataFirst[1]
			c.execute(insertSQL, testDataSecond[1]) # almost overwrite testDataFirst[2]
			conn.commit()

		self.parsing_db(self.tmpdb_path, self.output_db_filepath)
		self.assertTrue(isTableExists(self.output_db_filepath, "sms"),
			"the sms table does not exists in recovery file")

		results = fetchSMSNormalData(self.output_db_filepath)

		self.assertTrue(testDataFirst[3] in results)
		self.assertTrue(testDataFirst[4] in results)



	def templateTestAddressWithLengthAndChar(self, lengthOfAddress, char):
		testData = (
			('0000',  1, 1357005600, 1, 'Record 0'),
			(lengthOfAddress * char, 2, 1357005601, 1, 'Record 2'))

		self.insertAndDeleteLeftTheFirstOne(self.tmpdb_path, testData)
		self.parsing_db(self.tmpdb_path, self.output_db_filepath)

		self.assertTrue(isTableExists(self.output_db_filepath, "sms"),
			"the sms table does not exists in recovery file")

		results = fetchSMSNormalData(self.output_db_filepath)

		for n in xrange(1, len(testData)):
			self.assertTrue(testData[n] in results,
				"Failed with %d character Test, " % lengthOfAddress \
				+"could not find the deleted record at "\
				+"testData[%d]" % n)

	def testAddressWith1to101LengthBy10Increment(self):
		for n in xrange(1, 101, 10):
			self.templateTestAddressWithLengthAndChar(n, "1")

	def testAddressWith500char(self):
		self.templateTestAddressWithLengthAndChar(500, "a")

	def testAddressWithDeleting10Record(self):
		testData = (
			('0000',  1, 1357005600, 1, 'Record 0'),
			('1', 1, 1357005601, 1, 'Record 1'),
			('a', 2, 1357005602, 1, 'Record 2'),
			('86543',  3, 1357005603, 1, 'Record 3'),
			('1-800-MY-APPLE', 4, 1357005604, 1, 'Record 4'),
			('+8613800138000', 5, 1357005605, 1, 'Record 5'),
			('+861237513800138000', 6, 1357005606, 1, 'Record 6'),
			('1-(800)-(12345)', 7, 1357005607, 1, 'Record 7'),
			('0755-10086', 8, 1357005608, 1, 'Record 8'),
			('test@gmail.com',  9, 1357005609, 1, 'Record 9'),
			('thisisalonglonglonglonglonglongAddress@canyouseeme.com',
				10, 1357005610, 1, 'Record 10'))

		self.setData_Process_And_Check(testData)

	def testAddressWithANumber(self):
		testData = (
			('0000',  1, 1357005600, 1, 'Record 0'),
			('1', 2, 1357005601, 1, 'Record 2'))

		self.setData_Process_And_Check(testData)

	def testAddressWithAChar(self):
		testData = (
			('0000',  1, 1357005600, 1, 'Record 0'),
			('a', 2, 1357005602, 1, 'Record 2'))

		self.setData_Process_And_Check(testData)

	def testAddressWithShortNumber(self):
		testData = (
			('0000',  1, 1357005600, 1, 'Record 0'),
			('86543',  3, 1357005603, 1, 'Record 3'))

		self.setData_Process_And_Check(testData)

	def testAddressWithNumberAndChar(self):
		testData = (
			('0000',  1, 1357005600, 1, 'Record 0'),
			('1-800-MY-APPLE', 4, 1357005604, 1, 'Record 4'))

		self.setData_Process_And_Check(testData)

	def testAddressWithPrefix(self):
		testData = (
			('0000',  1, 1357005600, 1, 'Record 0'),
			('+861237513800138000', 6, 1357005606, 1, 'Record 6'))

		self.setData_Process_And_Check(testData)

	def testAddressWithParenthesis(self):
		testData = (
			('0000',  1, 1357005600, 1, 'Record 0'),
			('1-(800)-(12345)', 7, 1357005607, 1, 'Record 7'))

		self.setData_Process_And_Check(testData)

	def testAddressWithEmail(self):
		testData = (
			('0000',  1, 1357005600, 1, 'Record 0'),
			('test@gmail.com',  9, 1357005609, 1, 'Record 9'))

		self.setData_Process_And_Check(testData)

	def testAddressWithLongEmail(self):
		testData = (
			('0000',  1, 1357005600, 1, 'Record 0'),
			('thisisalonglonglonglonglonglongAddress@canyouseeme.com',
				10, 1357005610, 1, 'Record 10'))

		self.setData_Process_And_Check(testData)

	def templateTestAddressWithMultiLanguageString(self, aString):
		testData = (
			('0000',  1, 1357005600, 1, 'Record 0'),
			(aString, 13, 1357005610, 1, 'Record 10'))

		with sqlite3.connect(self.tmpdb_path) as conn:
			c = conn.cursor()
			# ignore Unicode characters that cannot be decode from UTF-8
			conn.text_factory = lambda x: unicode(x, "UTF-8", "ignore")
			insertSQL = '''insert into sms(address, thread_id, date, type, body)
			 values (?, ?, ?, ?, ?)'''
			for n in xrange(len(testData)):
				c.execute(insertSQL, testData[n])
			c.execute('''delete from sms where _id > 1''')
			conn.commit()

		self.parsing_db(self.tmpdb_path, self.output_db_filepath)
		self.checkAllTestData(self.output_db_filepath, testData)

	def testAddressWithChinese(self):
		self.templateTestAddressWithMultiLanguageString('中文地址测试')

	def testAddressWithJanpanese(self):
		self.templateTestAddressWithMultiLanguageString('テスト')

	def testAddressWithKorean(self):
		self.templateTestAddressWithMultiLanguageString('한국어')

	def testAddressWithOverflow(self):
		# TODO: need to finish
		self.assertTrue(False)

	def testThreadIDSimple(self):
		testData = (
			('0000',  1, 1357005600, 1, 'Record 0'),
			('10086', 2, 1357005601, 1, 'Record 1'))

		self.setData_Process_And_Check(testData)

	def testThreadIDSameWithPrev(self):
		testData = (
			('0000',  1, 1357005600, 1, 'Record 0'),
			('10086', 1, 1357005601, 1, 'Record 1'),
			('10086', 1, 1357005601, 1, 'Record 1'))

		self.setData_Process_And_Check(testData)

	def testThreadIDIs0(self):
		testData = (
			('0000',  1, 1357005600, 1, 'Record 0'),
			('10086', 0, 1357005601, 1, 'Record 1'))

	def testThreadIDIs10(self):
		testData = (
			('0000',  1, 1357005600, 1, 'Record 0'),
			('10086', 10, 1357005601, 1, 'Record 1'))

		self.setData_Process_And_Check(testData)

	def testThreadIDIs1000(self):
		testData = (
			('0000',  1, 1357005600, 1, 'Record 0'),
			('10086', 1000, 1357005601, 1, 'Record 1'))

		self.setData_Process_And_Check(testData)

	def testThreadIDHas3ID(self):
		testData = (
			('0000',  1, 1357005600, 1, 'Record 0'),
			('10086', 1, 1357005601, 2, 'Record 1'),
			('10086', 2, 1357005601, 1, 'Record 2'),
			('10086', 2, 1357005601, 2, 'Record 3'),
			('10086', 3, 1357005601, 1, 'Record 4'),
			('10086', 1, 1357005601, 1, 'Record 5'))

		self.setData_Process_And_Check(testData)

	def templateTestDataWithNumber(self, num):
		testData = (
			('0000',  1, 1357005600 * 1000, 1, 'Record 0'),
			('10086', 1, num, 1, 'Record 1'))
		self.setData_Process_And_Check(testData)

	def testDateIs0(self):
		self.templateTestDataWithNumber(0)

	def testDateIs1(self):
		self.templateTestDataWithNumber(1)

	def testDateIs10(self):
		self.templateTestDataWithNumber(10)

	def testDateIs1000(self):
		self.templateTestDataWithNumber(1000)

	def testDateInYear2036(self):
		"""
		Test Date: 1/1/2036 12:00:00 AM
		"""
		self.templateTestDataWithNumber(2082729600 * 1000)

	def testDateIsNow(self):
		from time import time
		self.templateTestDataWithNumber(int(time()) * 1000)

	def testDate(self):
		testData = (
			('0000',  1, 1357005600, 1, 'Record 0'),
			('10086', 1, 0, 1, 'Record 1'),
			('10086', 2, 1, 1, 'Record 2'),
			('10086', 3, 10, 1, 'Record 3'),
			('10086', 4, 100, 1, 'Record 4'),
			('10086', 5, 1000, 1, 'Record 5'),
			('10086', 6, 10000, 1, 'Record 6'),
			('10086', 7, 100000, 1, 'Record 7'),
			('10086', 8, 1000000, 1, 'Record 8'),
			('10086', 8, 10000000, 1, 'Record 9'),
			('10086', 8, 100000000, 1, 'Record 10'),
			('10086', 8, 2000000000, 1, 'Record 11'))

		self.setData_Process_And_Check(testData)

	def templateTestTypeWithNumber(self, num):
		testData = (
			('0000',  1, 1357005600, 1, 'Record 0'),
			('10086', 1, 1357005601, num, 'Record 1'))
		self.setData_Process_And_Check(testData)

	def testTypeIsIn(self):
		self.templateTestTypeWithNumber(1)

	def testTypeIsOut(self):
		self.templateTestTypeWithNumber(2)

	def testTypeIsDraft(self):
		self.templateTestTypeWithNumber(3)

	def testTypeIsPending(self):
		self.templateTestTypeWithNumber(4)

	def testTypeIs5(self):
		self.templateTestTypeWithNumber(5)

	def testTypeIs6(self):
		self.templateTestTypeWithNumber(6)

	def testTypeIs0(self):
		self.templateTestTypeWithNumber(0)

	def testTypeHas4Type(self):
		testData = (
			('0000',  1, 1357005600, 1, 'Record 0'),
			('10086', 1, 1357005601, 1, 'Record 1'),  # in
			('10086', 1, 1357005602, 2, 'Record 2'),  # out
			('10086', 1, 1357005603, 3, 'Record 3'),  # draft
			('10086', 1, 1357005604, 4, 'Record 5'))  # pending
		self.setData_Process_And_Check(testData)

	def templateTestBodyWithString(self, aString):
		testData = (
			('0000',  1, 1357005600, 1, 'Record 0'),
			('10086', 1, 1357005601, 1, aString))
		self.setData_Process_And_Check(testData)

	def testBodyWithAChar(self):
		self.templateTestBodyWithString('a')

	def testBodyWithANumber(self):
		self.templateTestBodyWithString('2')

	def testBodyWithAExclamatoryMark(self):
		self.templateTestBodyWithString('!')

	def testBodyWithBlank(self):
		self.templateTestBodyWithString(' ')

	def testBodyWith0000(self):
		self.templateTestBodyWithString('0000')

	def testBodyWith20chars(self):
		self.templateTestBodyWithString(20 * 'a')

	def testBodyWith140chars(self):
		self.templateTestBodyWithString(140 * 't')

	def testBodyWith500chars(self):
		self.templateTestBodyWithString(500 * 'z')

	def testBodyWithDeleting2Record(self):
		testData = (
			('0000',  1, 1357005600, 1, 'Record 0'),
			('10086', 2, 1357005611, 1, 'Record 1'),
			('10086', 2, 1357005612, 2, 'Record 2'))

		self.setData_Process_And_Check(testData)

	def templateTestBodyMultiLanguage(self, aString):
		testData = (
			('0000',  1, 1357005600, 1, 'Record 0'),
			('10086', 13, 1357005610, 1, aString))

		with sqlite3.connect(self.tmpdb_path) as conn:
			c = conn.cursor()
			# ignore Unicode characters that cannot be decode from UTF-8
			conn.text_factory = lambda x: unicode(x, "UTF-8", "ignore")
			insertSQL = '''insert into sms(address, thread_id, date, type, body)
			 values (?, ?, ?, ?, ?)'''
			for n in xrange(len(testData)):
				c.execute(insertSQL, testData[n])
			c.execute('''delete from sms where _id > 1''')
			conn.commit()

		self.parsing_db(self.tmpdb_path, self.output_db_filepath)
		self.checkAllTestData(self.output_db_filepath, testData)

	def testBodyWithChinese(self):
		self.templateTestBodyMultiLanguage('中文地址测试')

	def testBodyWith70ChineseChars(self):
		self.templateTestBodyMultiLanguage(70 * '中')

	def testBodyWithJanpanese(self):
		self.templateTestBodyMultiLanguage('テスト')

	def testBodyWithKorean(self):
		self.templateTestBodyMultiLanguage('한국어')

	def testOtherValue(self):
		pass

	# Scenario simulation
	def testRandomDelete(self):
		""" 插入一批数据，随机删除其中的若干条
		"""
		pass

	def testDeleteAllReordOfAThreadID(self):
		""" 删除同一 thread_id 的记录，即删除整个对话
		"""
		pass

	def testDeleteAllReordOfSeveralThreadID(self):
		""" 删除若干各 thread_id 的记录，即删除若干个个对话
		"""
		pass

	def testDeleteRecordsGreaterThanAPage(self):
		""" 删除一批记录，该批记录的长度大于一个PageSize的大小，使得 Sqlite 发生自收缩
		（该db文件需开启 auto_vacuum ）
		"""
		pass

class HTC_G10_TestCase(SMSTestCase):
	def setUp(self):
		self.initWithDeviceAndSchema(mmssms_db_tmpl.testDevice2)

class HTC_G12_TestCase(SMSTestCase):
	def setUp(self):
		self.initWithDeviceAndSchema(mmssms_db_tmpl.testDevice3)

class Samsung_S5830__TestCase(SMSTestCase):
	def setUp(self):
		self.initWithDeviceAndSchema(mmssms_db_tmpl.testDevice4)

class Motorola_XT883_TestCase(SMSTestCase):
	def setUp(self):
		self.initWithDeviceAndSchema(mmssms_db_tmpl.testDevice5)

class MMotorola_ME722_TestCase(SMSTestCase):
	def setUp(self):
		self.initWithDeviceAndSchema(mmssms_db_tmpl.testDevice6)

class LG_P990_TestCase(SMSTestCase):
	def setUp(self):
		self.initWithDeviceAndSchema(mmssms_db_tmpl.testDevice7)

class Samsung_Note_GT_I9220_TestCase(SMSTestCase):
	def setUp(self):
		self.initWithDeviceAndSchema(mmssms_db_tmpl.testDevice8)

class Samsung_Samsung_S5880_TestCase(SMSTestCase):
	def setUp(self):
		self.initWithDeviceAndSchema(mmssms_db_tmpl.testDevice9)

if __name__ == '__main__':
	unittest.main()




