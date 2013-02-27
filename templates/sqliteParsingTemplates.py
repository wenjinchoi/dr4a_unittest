# -*- coding: UTF-8 -*-

SQL_TYPE_INT = 1
SQL_TYPE_TEXT = 2
SQL_TYPE_LONG = 4
SQL_TYPE_FLOAT = 4
SQL_TYPE_BLOB = 8
SQL_TYPE_NULL = 16

# HTC 4.1.2
smsTemplate = (("_id", SQL_TYPE_NULL),
			   ("Thread_id", SQL_TYPE_INT ),
			   ("Address", SQL_TYPE_TEXT | SQL_TYPE_NULL),
			   ("Person", SQL_TYPE_INT | SQL_TYPE_NULL),
			   ("Date", SQL_TYPE_INT),
			   ("date_sent", SQL_TYPE_INT),
			   ("Protocol", SQL_TYPE_INT | SQL_TYPE_NULL),
			   ("Read", SQL_TYPE_INT),
			   ("status", SQL_TYPE_INT),
			   ("type", SQL_TYPE_INT),
			   ("Reply_path_present", SQL_TYPE_INT | SQL_TYPE_NULL),
			   ("subject", SQL_TYPE_TEXT | SQL_TYPE_NULL),
			   ("body", SQL_TYPE_TEXT | SQL_TYPE_NULL),
			   ("service_center", SQL_TYPE_TEXT | SQL_TYPE_NULL),
			   ("locked",  SQL_TYPE_INT),
			   ("error_code", SQL_TYPE_INT),
			   ("seen", SQL_TYPE_INT))
