# -*- coding: UTF-8 -*-

raw_contacts_table_1 = """CREATE TABLE raw_contacts
(_id INTEGER PRIMARY KEY AUTOINCREMENT,is_restricted INTEGER DEFAULT 0,
account_name STRING DEFAULT NULL, account_type STRING DEFAULT NULL,
sourceid TEXT,version INTEGER NOT NULL DEFAULT 1,
dirty INTEGER NOT NULL DEFAULT 0,deleted INTEGER NOT NULL DEFAULT 0,
contact_id INTEGER REFERENCES contacts(_id),
aggregation_mode INTEGER NOT NULL DEFAULT 0,
aggregation_needed INTEGER NOT NULL DEFAULT 1,custom_ringtone TEXT,
send_to_voicemail INTEGER NOT NULL DEFAULT 0,
times_contacted INTEGER NOT NULL DEFAULT 0,last_time_contacted INTEGER,
starred INTEGER NOT NULL DEFAULT 0,display_name TEXT,display_name_alt TEXT,
display_name_source INTEGER NOT NULL DEFAULT 0,phonetic_name TEXT,
phonetic_name_style TEXT,sort_key TEXT COLLATE PHONEBOOK,
sort_key_alt TEXT COLLATE PHONEBOOK,name_verified INTEGER NOT NULL DEFAULT 0,
contact_in_visible_group INTEGER NOT NULL DEFAULT 0,
sync1 TEXT, sync2 TEXT, sync3 TEXT, sync4 TEXT,
sns_id STRING DEFAULT NULL, sp INTEGER, is_sim INTEGER DEFAULT 0,
sort_priority INTEGER NOT NULL DEFAULT 0,
sort_priority_alt INTEGER NOT NULL DEFAULT 0,
sort_locale INTEGER NOT NULL DEFAULT 0,
sort_locale_alt INTEGER NOT NULL DEFAULT 0 );"""

data_1 = """CREATE TABLE data
(_id INTEGER PRIMARY KEY AUTOINCREMENT,
package_id INTEGER,
mimetype_id INTEGER  NOT NULL,
raw_contact_id INTEGER  NOT NULL,
is_primary INTEGER  NOT NULL DEFAULT 0,
is_super_primary INTEGER  NOT NULL DEFAULT 0,
data_version INTEGER  NOT NULL DEFAULT 0,
data1 TEXT,data2 TEXT,data3 TEXT,data4 TEXT,data5 TEXT,data6 TEXT,data7 TEXT,
data8 TEXT,data9 TEXT,data10 TEXT,data11 TEXT,data12 TEXT,data13 TEXT,
data14 TEXT,data15 TEXT,
data_sync1 TEXT, data_sync2 TEXT, data_sync3 TEXT, data_sync4 TEXT );"""


data_1_ori = """CREATE TABLE data
(_id INTEGER PRIMARY KEY AUTOINCREMENT,
package_id INTEGER REFERENCES package(_id),
mimetype_id INTEGER REFERENCES mimetype(_id) NOT NULL,
raw_contact_id INTEGER REFERENCES raw_contacts(_id) NOT NULL,
is_primary INTEGER NOT NULL DEFAULT 0,
is_super_primary INTEGER NOT NULL DEFAULT 0,
data_version INTEGER NOT NULL DEFAULT 0,
data1 TEXT,data2 TEXT,data3 TEXT,data4 TEXT,data5 TEXT,data6 TEXT,data7 TEXT,
data8 TEXT,data9 TEXT,data10 TEXT,data11 TEXT,data12 TEXT,data13 TEXT,
data14 TEXT,data15 TEXT,
data_sync1 TEXT, data_sync2 TEXT, data_sync3 TEXT, data_sync4 TEXT );"""
