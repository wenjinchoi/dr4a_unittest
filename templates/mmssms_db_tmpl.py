# -*- coding: UTF-8 -*-

# Base Test
smsSchema1 = '''CREATE TABLE sms
	(_id INTEGER PRIMARY KEY AUTOINCREMENT, thread_id INTEGER,
	address TEXT, person INTEGER, date INTEGER, date_sent INTEGER,
	protocol INTEGER, read INTEGER DEFAULT 0, status INTEGER DEFAULT -1,
	type INTEGER, reply_path_present INTEGER, subject TEXT, body TEXT)'''

# HTC_G10_4.1.2
smsSchema2 = '''CREATE TABLE sms
	(_id INTEGER PRIMARY KEY AUTOINCREMENT, thread_id INTEGER,
	address TEXT, person INTEGER, date INTEGER, date_sent INTEGER,
	protocol INTEGER, read INTEGER DEFAULT 0, status INTEGER DEFAULT -1,
	type INTEGER, reply_path_present INTEGER, subject TEXT, body TEXT,
	service_center TEXT, locked INTEGER, error_code INTEGER, seen INTEGER)'''

# HTC_G12_2.3.3
smsSchema3 = '''CREATE TABLE sms
	(_id INTEGER PRIMARY KEY,thread_id INTEGER,toa INTEGER DEFAULT 0,
	address TEXT,person INTEGER,date INTEGER,protocol INTEGER,
	read INTEGER DEFAULT 0,status INTEGER DEFAULT -1,type INTEGER,
	reply_path_present INTEGER,subject TEXT,body TEXT,
	sc_toa INTEGER DEFAULT 0,report_date INTEGER,service_center TEXT,
	locked INTEGER DEFAULT 0,index_on_sim TEXT,callback_number TEXT,
	priority INTEGER DEFAULT 0,htc_category INTEGER DEFAULT 0,
	cs_timestamp LONG DEFAULT -1, cs_id TEXT, cs_synced INTEGER DEFAULT 0,
	error_code INTEGER DEFAULT 0,seen INTEGER DEFAULT 0,
	is_cdma_format INTEGER DEFAULT 0, is_evdo INTEGER DEFAULT 0,
	c_type INTEGER DEFAULT 0, exp INTEGER DEFAULT 0 )'''

# Samsung_S5830_2.3.4
smsSchema4 = '''CREATE TABLE sms
	(_id INTEGER PRIMARY KEY AUTOINCREMENT,thread_id INTEGER,address TEXT,
	person INTEGER,date INTEGER,protocol INTEGER,read INTEGER DEFAULT 0,
	status INTEGER DEFAULT -1,type INTEGER,reply_path_present INTEGER,
	subject TEXT,body TEXT,service_center TEXT,locked INTEGER DEFAULT 0,
	error_code INTEGER DEFAULT 0,seen INTEGER DEFAULT 0,
	deletable INTEGER DEFAULT 0,delivery_date INTEGER)'''

# Motorola_XT883_2.3.6
smsSchema5 = '''CREATE TABLE sms
	(_id INTEGER PRIMARY KEY,thread_id INTEGER,address TEXT,person INTEGER,
	date INTEGER,protocol INTEGER,read INTEGER DEFAULT 0,
	priority INTEGER DEFAULT 0,status INTEGER DEFAULT -1,type INTEGER,
	callback_number TEXT,reply_path_present INTEGER,subject TEXT,body TEXT,
	service_center TEXT,failure_cause INTEGER DEFAULT -1,
	locked INTEGER DEFAULT 0,error_code INTEGER DEFAULT -33001,
	stack_type INTEGER DEFAULT 0,seen INTEGER DEFAULT 0,
	sort_index INTEGER DEFAULT 0 )'''

# MMotorola_ME722_2.2.2
smsSchema6 = '''CREATE TABLE sms
	(_id INTEGER PRIMARY KEY,thread_id INTEGER,address TEXT,person INTEGER,
	date INTEGER,protocol INTEGER,read INTEGER DEFAULT 0,
	priority INTEGER DEFAULT 0,status INTEGER DEFAULT -1,type INTEGER,
	callback_number TEXT,reply_path_present INTEGER,subject TEXT,
	body TEXT,service_center TEXT,failure_cause INTEGER DEFAULT -1,
	locked INTEGER DEFAULT 0,error_code INTEGER DEFAULT -33001,
	seen INTEGER DEFAULT 0,sort_index INTEGER DEFAULT 0 )'''

# LG_P990_2.3.4
smsSchema7 = '''CREATE TABLE sms
	(_id INTEGER PRIMARY KEY,thread_id INTEGER,address TEXT,person INTEGER,
		date INTEGER,protocol INTEGER,read INTEGER DEFAULT 0,
		status INTEGER DEFAULT -1,type INTEGER,reply_path_present INTEGER,
		subject TEXT,body TEXT,service_center TEXT,locked INTEGER DEFAULT 0,
		error_code INTEGER DEFAULT 0,seen INTEGER DEFAULT 0,
		lgeMsgType INTEGER DEFAULT 0,lgeSiid INTEGER,lgeCreated INTEGER,
		lgeExpires INTEGER,lgeReceived INTEGER,lgeAction TEXT,lgeSec TEXT,
		lgeMac TEXT,lgeDoc TEXT,doInstalled INTEGER DEFAULT 0,
		modified INTEGER NOT NULL DEFAULT 1,modified_time INTEGER,
		index_on_icc INTEGER,service_msg_sender_address TEXT)'''

# Samsung_Note_GT_I9220_4.0.4
smsSchema8 = '''CREATE TABLE sms
	(_id INTEGER PRIMARY KEY AUTOINCREMENT,thread_id INTEGER,address TEXT,
		person INTEGER,date INTEGER,date_sent INTEGER DEFAULT 0,
		protocol INTEGER,read INTEGER DEFAULT 0,status INTEGER DEFAULT -1,
		type INTEGER,reply_path_present INTEGER,subject TEXT,body TEXT,
		service_center TEXT,locked INTEGER DEFAULT 0,
		error_code INTEGER DEFAULT 0,seen INTEGER DEFAULT 0,
		deletable INTEGER DEFAULT 0,hidden INTEGER DEFAULT 0,
		roup_id INTEGER,group_type INTEGER,delivery_date INTEGER)'''

# Samsung_S5880_2.3.4
smsSchema9 = '''CREATE TABLE sms
	(_id INTEGER PRIMARY KEY AUTOINCREMENT,thread_id INTEGER,address TEXT,
	person INTEGER,date INTEGER,protocol INTEGER,read INTEGER DEFAULT 0,
	status INTEGER DEFAULT -1,type INTEGER,reply_path_present INTEGER,
	subject TEXT,body TEXT,service_center TEXT,locked INTEGER DEFAULT 0,
	error_code INTEGER DEFAULT 0,seen INTEGER DEFAULT 0,
	deletable INTEGER DEFAULT 0,delivery_date INTEGER)'''

threadSchema9 = """CREATE TABLE threads (_id INTEGER PRIMARY KEY,
	date INTEGER DEFAULT 0,message_count INTEGER DEFAULT 0,recipient_ids TEXT,
	snippet TEXT,snippet_cs INTEGER DEFAULT 0,read INTEGER DEFAULT 1,
	type INTEGER DEFAULT 0,error INTEGER DEFAULT 0,
	has_attachment INTEGER DEFAULT 0,unread_count INTEGER DEFAULT 0)"""


sms_update_thread_on_insert = '''CREATE TRIGGER sms_update_thread_on_insert
AFTER INSERT ON sms BEGIN  UPDATE threads
SET date = (strftime('%s','now') * 1000),
snippet = new.body,
snippet_cs = 0  WHERE threads._id = new.thread_id;
UPDATE threads SET message_count =
(SELECT COUNT(sms._id) FROM sms LEFT JOIN threads ON threads._id = thread_id
WHERE thread_id = new.thread_id AND sms.type != 3),
unread_count =
(SELECT count(*) FROM sms LEFT JOIN threads
ON threads._id = thread_id
WHERE thread_id = new.thread_id
AND sms.read = 0 AND sms.type != 3);
UPDATE threads SET read = CASE (SELECT COUNT(*)
FROM sms
WHERE read = 0
AND thread_id = threads._id)
WHEN 0 THEN 1      ELSE 0    END
WHERE threads._id = new.thread_id; END;'''

index = "CREATE INDEX typeThreadIdIndex ON sms (type, thread_id)"

sms_update_thread_on_insert_ori = '''CREATE TRIGGER sms_update_thread_on_insert
AFTER INSERT ON sms BEGIN  UPDATE threads
SET    date = (strftime('%s','now') * 1000),
snippet = new.body,
snippet_cs = 0  WHERE threads._id = new.thread_id;
UPDATE threads SET message_count =
(SELECT COUNT(sms._id) FROM sms LEFT JOIN threads
ON threads._id = thread_id
WHERE thread_id = new.thread_id
AND sms.type != 3) +
(SELECT COUNT(pdu._id) FROM pdu LEFT JOIN threads
ON threads._id = thread_id
WHERE thread_id = new.thread_id
AND (m_type=132 OR m_type=130 OR m_type=128)
AND msg_box != 3) 		,
unread_count =
(SELECT count(*) FROM sms LEFT JOIN threads
ON threads._id = thread_id
WHERE thread_id = new.thread_id
AND sms.read = 0 AND sms.type != 3) +
(SELECT count(*) FROM pdu LEFT JOIN threads
ON threads._id = thread_id
WHERE thread_id = new.thread_id
AND pdu.read = 0
AND (m_type = 128 OR m_type = 132 OR m_type = 130)
AND msg_box != 3)   WHERE threads._id = new.thread_id;
UPDATE threads SET read =     CASE (SELECT COUNT(*)
FROM sms
WHERE read = 0
AND thread_id = threads._id)
WHEN 0 THEN 1      ELSE 0    END
WHERE threads._id = new.thread_id; END;'''


samsung_gts5570_2_2_1_sms = """CREATE TABLE sms (
_id INTEGER PRIMARY KEY AUTOINCREMENT,thread_id INTEGER,address TEXT,
person INTEGER,date INTEGER,protocol INTEGER,read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,type INTEGER,reply_path_present INTEGER,
subject TEXT,body TEXT,service_center TEXT,locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,seen INTEGER DEFAULT 0,
deletable INTEGER DEFAULT 0);"""

samsung_gti9000_2_3_4_sms = """CREATE TABLE sms (
_id INTEGER PRIMARY KEY AUTOINCREMENT,thread_id INTEGER,address TEXT,
person INTEGER,date INTEGER,protocol INTEGER,read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,type INTEGER,reply_path_present INTEGER,
subject TEXT,body TEXT,service_center TEXT,locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,seen INTEGER DEFAULT 0,
deletable INTEGER DEFAULT 0);"""

samsung_gtn7000_4_0_4_sms = """CREATE TABLE sms (
_id INTEGER PRIMARY KEY AUTOINCREMENT,thread_id INTEGER,address TEXT,
person INTEGER,date INTEGER,date_sent INTEGER DEFAULT 0,protocol INTEGER,
read INTEGER DEFAULT 0,status INTEGER DEFAULT -1,type INTEGER,
reply_path_present INTEGER,subject TEXT,body TEXT,service_center TEXT,
locked INTEGER DEFAULT 0,error_code INTEGER DEFAULT 0,seen INTEGER DEFAULT 0,
deletable INTEGER DEFAULT 0,hidden INTEGER DEFAULT 0,group_id INTEGER,
group_type INTEGER,delivery_date INTEGER, reserved INTEGER DEFAULT 0,
pri INTEGER DEFAULT 0);"""

samsung_sghi997_2_2_1_sms = """CREATE TABLE sms (
_id INTEGER PRIMARY KEY AUTOINCREMENT,thread_id INTEGER,address TEXT,
person INTEGER,date INTEGER,protocol INTEGER,read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,type INTEGER,reply_path_present INTEGER,
subject TEXT,body TEXT,service_center TEXT,locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,seen INTEGER DEFAULT 0,
deletable INTEGER DEFAULT 0);"""

samsung_gts5830_2_3_4_sms = """CREATE TABLE sms (
_id INTEGER PRIMARY KEY AUTOINCREMENT,thread_id INTEGER,address TEXT,
person INTEGER,date INTEGER,protocol INTEGER,read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,type INTEGER,reply_path_present INTEGER,
subject TEXT,body TEXT,service_center TEXT,locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,seen INTEGER DEFAULT 0,
deletable INTEGER DEFAULT 0,delivery_date INTEGER);"""

samsung_gts5670_2_2_1_sms = """CREATE TABLE sms (
_id INTEGER PRIMARY KEY AUTOINCREMENT,thread_id INTEGER,address TEXT,
person INTEGER,date INTEGER,protocol INTEGER,read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,type INTEGER,reply_path_present INTEGER,
subject TEXT,body TEXT,service_center TEXT,locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,seen INTEGER DEFAULT 0,
deletable INTEGER DEFAULT 0);"""


