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



# htc_2_2_1
sms_htc_2_2_1 = '''CREATE TABLE sms
(_id INTEGER PRIMARY KEY,
thread_id INTEGER,
toa INTEGER DEFAULT 0,
address TEXT,
person INTEGER,
date INTEGER,
protocol INTEGER,
read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,
type INTEGER,
reply_path_present INTEGER,
subject TEXT,
body TEXT,
sc_toa INTEGER DEFAULT 0,
report_date INTEGER,
service_center TEXT,
locked INTEGER DEFAULT 0,
index_on_sim TEXT,
callback_number TEXT,
priority INTEGER DEFAULT 0,
htc_category INTEGER DEFAULT 0,
cs_timestamp LONG DEFAULT -1,
cs_id TEXT,
cs_synced INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,
seen INTEGER DEFAULT 0,
is_cdma_format INTEGER DEFAULT 1,
is_evdo INTEGER DEFAULT 0 );
'''

#
sms_ = '''CREATE TABLE sms
(_id INTEGER PRIMARY KEY AUTOINCREMENT,
thread_id INTEGER,
address TEXT,
person INTEGER,
date INTEGER,
protocol INTEGER,
read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,
type INTEGER,
reply_path_present INTEGER,
subject TEXT,
body TEXT,
service_center TEXT,
locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,
seen INTEGER DEFAULT 0,
deletable INTEGER DEFAULT 0,
delivery_date INTEGER);
'''

# samsung_GT_i897or9000_2_3_4
sms_samsung_GT_i897or9000_2_3_4 = '''CREATE TABLE sms
(_id INTEGER PRIMARY KEY AUTOINCREMENT,
thread_id INTEGER,
address TEXT,
person INTEGER,
date INTEGER,
protocol INTEGER,
read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,
type INTEGER,
reply_path_present INTEGER,
subject TEXT,
body TEXT,
service_center TEXT,
locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,
seen INTEGER DEFAULT 0,
deletable INTEGER DEFAULT 0);
'''

# samsung_gt_i9001_2_3_6
sms_samsung_gt_i9001_2_3_6 = '''CREATE TABLE sms
(_id INTEGER PRIMARY KEY AUTOINCREMENT,
thread_id INTEGER,
address TEXT,
person INTEGER,
date INTEGER,
protocol INTEGER,
read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,
type INTEGER,
reply_path_present INTEGER,
subject TEXT,
body TEXT,
service_center TEXT,
locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,
seen INTEGER DEFAULT 0,
deletable INTEGER DEFAULT 0,
delivery_date INTEGER);
'''

# samsung_gt_i9003_2_3_5
sms_samsung_gt_i9003_2_3_5 = '''CREATE TABLE sms
(_id INTEGER PRIMARY KEY AUTOINCREMENT,
thread_id INTEGER,
address TEXT,
person INTEGER,
date INTEGER,
protocol INTEGER,
read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,
type INTEGER,
reply_path_present INTEGER,
subject TEXT,
body TEXT,
service_center TEXT,
locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,
seen INTEGER DEFAULT 0,
deletable INTEGER DEFAULT 0);
'''

# samsung_gt_i9300_4_1_2
sms_samsung_gt_i9300_4_1_2 = '''CREATE TABLE sms
(_id INTEGER PRIMARY KEY AUTOINCREMENT,
thread_id INTEGER,
address TEXT,
person INTEGER,
date INTEGER,
date_sent INTEGER DEFAULT 0,
protocol INTEGER,
read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,
type INTEGER,
reply_path_present INTEGER,
subject TEXT,
body TEXT,
service_center TEXT,
locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,
seen INTEGER DEFAULT 0,
deletable INTEGER DEFAULT 0,
hidden INTEGER DEFAULT 0,
group_id INTEGER,
group_type INTEGER,
delivery_date INTEGER,
app_id INTEGER DEFAULT 0,
msg_id INTEGER DEFAULT 0,
callback_number TEXT,
reserved INTEGER DEFAULT 0,
pri INTEGER DEFAULT 0,
teleservice_id INTEGER DEFAULT 0,
link_url TEXT);
'''

# samsung_gt_n7000_4_0_3
sms_samsung_gt_n7000_4_0_3 = '''CREATE TABLE sms
(_id INTEGER PRIMARY KEY AUTOINCREMENT,
thread_id INTEGER,
address TEXT,
person INTEGER,
date INTEGER,
date_sent INTEGER DEFAULT 0,
protocol INTEGER,
read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,
type INTEGER,
reply_path_present INTEGER,
subject TEXT,
body TEXT,
service_center TEXT,
locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,
seen INTEGER DEFAULT 0,
deletable INTEGER DEFAULT 0,
hidden INTEGER DEFAULT 0,
group_id INTEGER,
group_type INTEGER,
delivery_date INTEGER);
'''

# samsung_GT_N7000_4_0_4
sms_samsung_GT_N7000_4_0_4 = '''CREATE TABLE sms
(_id INTEGER PRIMARY KEY AUTOINCREMENT,
thread_id INTEGER,
address TEXT,
person INTEGER,
date INTEGER,
date_sent INTEGER DEFAULT 0,
protocol INTEGER,
read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,
type INTEGER,
reply_path_present INTEGER,
subject TEXT,
body TEXT,
service_center TEXT,
locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,
seen INTEGER DEFAULT 0,
deletable INTEGER DEFAULT 0,
hidden INTEGER DEFAULT 0,
group_id INTEGER,
group_type INTEGER,
delivery_date INTEGER,
reserved INTEGER DEFAULT 0,
pri INTEGER DEFAULT 0);
'''

# samsung_gt_n7100_4_1_1
sms_samsung_gt_n7100_4_1_1 = '''CREATE TABLE sms
(_id INTEGER PRIMARY KEY AUTOINCREMENT,
thread_id INTEGER,
address TEXT,
person INTEGER,
date INTEGER,
date_sent INTEGER DEFAULT 0,
protocol INTEGER,
read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,
type INTEGER,
reply_path_present INTEGER,
subject TEXT,
body TEXT,
service_center TEXT,
locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,
seen INTEGER DEFAULT 0,
deletable INTEGER DEFAULT 0,
hidden INTEGER DEFAULT 0,
group_id INTEGER,
group_type INTEGER,
delivery_date INTEGER,
app_id INTEGER DEFAULT 0,
msg_id INTEGER DEFAULT 0,
callback_number TEXT,
reserved INTEGER DEFAULT 0,
pri INTEGER DEFAULT 0,
teleservice_id INTEGER DEFAULT 0,
link_url TEXT);
'''

# samsung_gt_n8000_4_1_1
sms_samsung_gt_n8000_4_1_1 = '''CREATE TABLE sms
(_id INTEGER PRIMARY KEY AUTOINCREMENT,
thread_id INTEGER,
address TEXT,
person INTEGER,
date INTEGER,
date_sent INTEGER DEFAULT 0,
protocol INTEGER,
read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,
type INTEGER,
reply_path_present INTEGER,
subject TEXT,
body TEXT,
service_center TEXT,
locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,
seen INTEGER DEFAULT 0,
deletable INTEGER DEFAULT 0,
hidden INTEGER DEFAULT 0,
group_id INTEGER,
group_type INTEGER,
delivery_date INTEGER,
app_id INTEGER DEFAULT 0,
msg_id INTEGER DEFAULT 0,
callback_number TEXT,
reserved INTEGER DEFAULT 0,
pri INTEGER DEFAULT 0,
teleservice_id INTEGER DEFAULT 0,
link_url TEXT);
'''

# samsung_gt_p1000_2_2_1
sms_samsung_gt_p1000_2_2_1 = '''CREATE TABLE sms
(_id INTEGER PRIMARY KEY AUTOINCREMENT,
thread_id INTEGER,
address TEXT,
person INTEGER,
date INTEGER,
protocol INTEGER,
read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,
type INTEGER,
reply_path_present INTEGER,
subject TEXT,
body TEXT,
service_center TEXT,
locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,
seen INTEGER DEFAULT 0);
'''

# samsung_gt_p7500_4_0_4
sms_samsung_gt_p7500_4_0_4 = '''CREATE TABLE sms
(_id INTEGER PRIMARY KEY AUTOINCREMENT,
thread_id INTEGER,
address TEXT,
person INTEGER,
date INTEGER,
protocol INTEGER,
read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,
type INTEGER,
reply_path_present INTEGER,
subject TEXT,
body TEXT,
service_center TEXT,
locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,
seen INTEGER DEFAULT 0,
hidden INTEGER DEFAULT 0,
group_id INTEGER,
group_type INTEGER,
date_sent INTEGER DEFAULT 0,
delivery_date INTEGER,
app_id INTEGER DEFAULT 0,
msg_id INTEGER DEFAULT 0,
callback_number TEXT,
deletable INTEGER DEFAULT 0,
priority INTEGER DEFAULT 0,
reserved INTEGER DEFAULT 0,
teleservice_id INTEGER DEFAULT 0,
link_url TEXT);
'''

# samsung_gt_s5570_2_2_1
sms_samsung_gt_s5570_2_2_1 = '''CREATE TABLE sms
(_id INTEGER PRIMARY KEY AUTOINCREMENT,
thread_id INTEGER,
address TEXT,
person INTEGER,
date INTEGER,
protocol INTEGER,
read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,
type INTEGER,
reply_path_present INTEGER,
subject TEXT,
body TEXT,
service_center TEXT,
locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,
seen INTEGER DEFAULT 0,
deletable INTEGER DEFAULT 0);
'''

# samsung_P1500_4_0_3
sms_samsung_P1500_4_0_3 = '''CREATE TABLE sms
(_id INTEGER PRIMARY KEY AUTOINCREMENT,
thread_id INTEGER,
address TEXT,
person INTEGER,
date INTEGER,
date_sent INTEGER DEFAULT 0,
protocol INTEGER,
read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,
type INTEGER,
reply_path_present INTEGER,
subject TEXT,
body TEXT,
service_center TEXT,
locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,
seen INTEGER DEFAULT 0,
deletable INTEGER DEFAULT 0,
hidden INTEGER DEFAULT 0,
group_id INTEGER,
group_type INTEGER,
delivery_date INTEGER,
app_id INTEGER DEFAULT 0,
msg_id INTEGER DEFAULT 0,
callback_number TEXT,
reserved INTEGER DEFAULT 0);
'''

# samsung_s5670_2_2_1
sms_samsung_s5670_2_2_1 = '''CREATE TABLE sms
(_id INTEGER PRIMARY KEY AUTOINCREMENT,
thread_id INTEGER,
address TEXT,
person INTEGER,
date INTEGER,
protocol INTEGER,
read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,
type INTEGER,
reply_path_present INTEGER,
subject TEXT,
body TEXT,
service_center TEXT,
locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,
seen INTEGER DEFAULT 0,
deletable INTEGER DEFAULT 0);
'''

# samsung_s5830_2_3_4
sms_samsung_s5830_2_3_4 = '''CREATE TABLE sms
(_id INTEGER PRIMARY KEY AUTOINCREMENT,
thread_id INTEGER,
address TEXT,
person INTEGER,
date INTEGER,
protocol INTEGER,
read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,
type INTEGER,
reply_path_present INTEGER,
subject TEXT,
body TEXT,
service_center TEXT,
locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,
seen INTEGER DEFAULT 0,
deletable INTEGER DEFAULT 0,
delivery_date INTEGER);
'''

# samsung_SCH_I909_2_2_2
sms_samsung_SCH_I909_2_2_2 = '''CREATE TABLE sms
(_id INTEGER PRIMARY KEY AUTOINCREMENT,
thread_id INTEGER,
address TEXT,
person INTEGER,
date INTEGER,
protocol INTEGER,
read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,
type INTEGER,
reply_path_present INTEGER,
subject TEXT,
body TEXT,
service_center TEXT,
locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,
seen INTEGER DEFAULT 0,
deletable INTEGER DEFAULT 0,
band INTEGER DEFAULT -1);
'''

# samsung_sgh_i927_4_0_4
sms_samsung_sgh_i927_4_0_4 = '''CREATE TABLE sms
(_id INTEGER PRIMARY KEY AUTOINCREMENT,
thread_id INTEGER,
address TEXT,
person INTEGER,
date INTEGER,
date_sent INTEGER DEFAULT 0,
protocol INTEGER,
read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,
type INTEGER,
reply_path_present INTEGER,
subject TEXT,
body TEXT,
service_center TEXT,
locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,
seen INTEGER DEFAULT 0,
deletable INTEGER DEFAULT 0,
hidden INTEGER DEFAULT 0,
group_id INTEGER,
group_type INTEGER,
delivery_date INTEGER);
'''

# samsung_sgh_i9970_2_2_1
sms_samsung_sgh_i9970_2_2_1 = '''CREATE TABLE sms
(_id INTEGER PRIMARY KEY AUTOINCREMENT,
thread_id INTEGER,
address TEXT,
person INTEGER,
date INTEGER,
protocol INTEGER,
read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,
type INTEGER,
reply_path_present INTEGER,
subject TEXT,
body TEXT,
service_center TEXT,
locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,
seen INTEGER DEFAULT 0,
deletable INTEGER DEFAULT 0);
'''

# samsung_sph_d710_4_0_4
sms_samsung_sph_d710_4_0_4 = '''CREATE TABLE sms
(_id INTEGER PRIMARY KEY AUTOINCREMENT,
thread_id INTEGER,
address TEXT,
person INTEGER,
date INTEGER,
protocol INTEGER,
read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,
type INTEGER,
reply_path_present INTEGER,
subject TEXT,
body TEXT,
service_center TEXT,
locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,
seen INTEGER DEFAULT 0,
deletable INTEGER DEFAULT 0,
hidden INTEGER DEFAULT 0,
group_id INTEGER,
group_type INTEGER,
delivery_date INTEGER,
service_category INTEGER,
category INTEGER,
response_type INTEGER,
severity INTEGER,
urgency INTEGER,
certainty INTEGER,
identifier INTEGER,
alert_handling INTEGER,
expires INTEGER,
language INTEGER,
cmas_sms_expired INTEGER DEFAULT 1);
'''

# samsung_GT_9100_4_0_4
sms_samsung_GT_9100_4_0_4 = '''CREATE TABLE sms
(_id INTEGER PRIMARY KEY AUTOINCREMENT,
thread_id INTEGER,
address TEXT,
person INTEGER,
date INTEGER,
date_sent INTEGER DEFAULT 0,
protocol INTEGER,
read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,
type INTEGER,
reply_path_present INTEGER,
subject TEXT,
body TEXT,
service_center TEXT,
locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,
seen INTEGER DEFAULT 0,
deletable INTEGER DEFAULT 0,
hidden INTEGER DEFAULT 0,
group_id INTEGER,
group_type INTEGER,
delivery_date INTEGER);
'''

# samsung_GT_9250_4_2_2
sms_samsung_GT_9250_4_2_2 = '''CREATE TABLE sms
(_id INTEGER PRIMARY KEY,
thread_id INTEGER,
address TEXT,
person INTEGER,
date INTEGER,
date_sent INTEGER DEFAULT 0,
protocol INTEGER,
read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,
type INTEGER,
reply_path_present INTEGER,
subject TEXT,
body TEXT,
service_center TEXT,
locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,
seen INTEGER DEFAULT 0);
'''

# sansung_5580_2_3_4
sms_sansung_5580_2_3_4 = '''CREATE TABLE sms
(_id INTEGER PRIMARY KEY AUTOINCREMENT,
thread_id INTEGER,
address TEXT,
person INTEGER,
date INTEGER,
protocol INTEGER,
read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,
type INTEGER,
reply_path_present INTEGER,
subject TEXT,
body TEXT,
service_center TEXT,
locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,
seen INTEGER DEFAULT 0,
deletable INTEGER DEFAULT 0,
delivery_date INTEGER);
'''

# sansung_GT_I9000_2_3_4
sms_sansung_GT_I9000_2_3_4 = '''CREATE TABLE sms
(_id INTEGER PRIMARY KEY AUTOINCREMENT,
thread_id INTEGER,
address TEXT,
person INTEGER,
date INTEGER,
protocol INTEGER,
read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,
type INTEGER,
reply_path_present INTEGER,
subject TEXT,
body TEXT,
service_center TEXT,
locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,
seen INTEGER DEFAULT 0,
deletable INTEGER DEFAULT 0);
'''

# sansung_GT_I9100G_4_0_4
sms_sansung_GT_I9100G_4_0_4 = '''CREATE TABLE sms
(_id INTEGER PRIMARY KEY AUTOINCREMENT,
thread_id INTEGER,
address TEXT,
person INTEGER,
date INTEGER,
date_sent INTEGER DEFAULT 0,
protocol INTEGER,
read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,
type INTEGER,
reply_path_present INTEGER,
subject TEXT,
body TEXT,
service_center TEXT,
locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,
seen INTEGER DEFAULT 0,
deletable INTEGER DEFAULT 0,
hidden INTEGER DEFAULT 0,
group_id INTEGER,
group_type INTEGER,
delivery_date INTEGER);
'''

# sansung_SGH_I997_2_2_1
sms_sansung_SGH_I997_2_2_1 = '''CREATE TABLE sms
(_id INTEGER PRIMARY KEY AUTOINCREMENT,
thread_id INTEGER,
address TEXT,
person INTEGER,
date INTEGER,
protocol INTEGER,
read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,
type INTEGER,
reply_path_present INTEGER,
subject TEXT,
body TEXT,
service_center TEXT,
locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,
seen INTEGER DEFAULT 0,
deletable INTEGER DEFAULT 0);
'''

# sansung_SGH_T759_2_3_3
sms_sansung_SGH_T759_2_3_3 = '''CREATE TABLE sms
(_id INTEGER PRIMARY KEY AUTOINCREMENT,
thread_id INTEGER,
address TEXT,
person INTEGER,
date INTEGER,
protocol INTEGER,
read INTEGER DEFAULT 0,
status INTEGER DEFAULT -1,
type INTEGER,
reply_path_present INTEGER,
subject TEXT,
body TEXT,
service_center TEXT,
locked INTEGER DEFAULT 0,
error_code INTEGER DEFAULT 0,
seen INTEGER DEFAULT 0,
deletable INTEGER DEFAULT 0);
'''

sms_device_schemas = {
  "htc_2_2_1" : sms_htc_2_2_1,
  "" : sms_,
  "samsung_GT_i897or9000_2_3_4" : sms_samsung_GT_i897or9000_2_3_4,
  "samsung_gt_i9001_2_3_6" : sms_samsung_gt_i9001_2_3_6,
  "samsung_gt_i9003_2_3_5" : sms_samsung_gt_i9003_2_3_5,
  "samsung_gt_i9300_4_1_2" : sms_samsung_gt_i9300_4_1_2,
  "samsung_gt_n7000_4_0_3" : sms_samsung_gt_n7000_4_0_3,
  "samsung_GT_N7000_4_0_4" : sms_samsung_GT_N7000_4_0_4,
  "samsung_gt_n7100_4_1_1" : sms_samsung_gt_n7100_4_1_1,
  "samsung_gt_n8000_4_1_1" : sms_samsung_gt_n8000_4_1_1,
  "samsung_gt_p1000_2_2_1" : sms_samsung_gt_p1000_2_2_1,
  "samsung_gt_p7500_4_0_4" : sms_samsung_gt_p7500_4_0_4,
  "samsung_gt_s5570_2_2_1" : sms_samsung_gt_s5570_2_2_1,
  "samsung_P1500_4_0_3" : sms_samsung_P1500_4_0_3,
  "samsung_s5670_2_2_1" : sms_samsung_s5670_2_2_1,
  "samsung_s5830_2_3_4" : sms_samsung_s5830_2_3_4,
  "samsung_SCH_I909_2_2_2" : sms_samsung_SCH_I909_2_2_2,
  "samsung_sgh_i927_4_0_4" : sms_samsung_sgh_i927_4_0_4,
  "samsung_sgh_i9970_2_2_1" : sms_samsung_sgh_i9970_2_2_1,
  "samsung_sph_d710_4_0_4" : sms_samsung_sph_d710_4_0_4,
  "samsung_GT_9100_4_0_4" : sms_samsung_GT_9100_4_0_4,
  "samsung_GT_9250_4_2_2" : sms_samsung_GT_9250_4_2_2,
  "sansung_5580_2_3_4" : sms_sansung_5580_2_3_4,
  "sansung_GT_I9000_2_3_4" : sms_sansung_GT_I9000_2_3_4,
  "sansung_GT_I9100G_4_0_4" : sms_sansung_GT_I9100G_4_0_4,
  "sansung_SGH_I997_2_2_1" : sms_sansung_SGH_I997_2_2_1,
  "sansung_SGH_T759_2_3_3" : sms_sansung_SGH_T759_2_3_3 }

