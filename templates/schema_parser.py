# -*- coding: UTF-8 -*-

import os
from pprint import pprint

def process_device_name(device_name):
	device = device_name
	device = device.rstrip("-")
	device = device.rstrip("_")
	device = device.replace("-", "_")
	device = device.replace("(", "or")
	device = device.replace(")", "")
	device = device.replace(".", "_")
	return device

def process_data_schema(schema):
	tmp_schema = schema
	tmp_schema = tmp_schema.replace("REFERENCES package(_id)", "")
	tmp_schema = tmp_schema.replace("REFERENCES mimetype(_id) ", "")
	tmp_schema = tmp_schema.replace("REFERENCES raw_contacts(_id) ", "")
	tmp_schema = tmp_schema.replace("CREATE TABLE data ", "CREATE TABLE data \n")
	tmp_schema = tmp_schema.replace("AUTOINCREMENT," ,"AUTOINCREMENT,\n")
	tmp_schema = tmp_schema.replace(",mimetype_id", ",\nmimetype_id")
	tmp_schema = tmp_schema.replace(",raw_contact_id", ",\nraw_contact_id")
	tmp_schema = tmp_schema.replace(",is_read_only", ",\nis_read_only")
	tmp_schema = tmp_schema.replace(",is_primary", ",\nis_primary")
	tmp_schema = tmp_schema.replace(",is_super_primary", ",\nis_super_primary")
	tmp_schema = tmp_schema.replace(",data_version", ",\ndata_version")
	tmp_schema = tmp_schema.replace(",data1 ", ",\ndata1 ")
	tmp_schema = tmp_schema.replace(",data8", ",\ndata8")
	tmp_schema = tmp_schema.replace(",data14", ",\ndata14")
	tmp_schema = tmp_schema.replace(",data_sync1", ",\ndata_sync1")
	return tmp_schema

def process_raw_contacts_schema(schema):
	tmp_schema = schema
	tmp_schema = tmp_schema.replace("CREATE TABLE raw_contacts ",
																	"CREATE TABLE raw_contacts \n")
	tmp_schema = tmp_schema.replace("REFERENCES package(_id)", "")
	tmp_schema = tmp_schema.replace(" REFERENCES accounts(_id)", "")
	tmp_schema = tmp_schema.replace(" REFERENCES contacts(_id)", "")
	tmp_schema = tmp_schema.replace(" ,", ",")
	tmp_schema = tmp_schema.replace(", ", ",")
	tmp_schema = tmp_schema.replace(",", ",\n")
	return tmp_schema


def parse_schema(parsed_path, output_path, split_chars, table_name,
	fprocess_schema):
	with open(output_path, "w") as fw:
		fw.write("# -*- coding: UTF-8 -*-\n\n")

		devices = []
		for d in os.walk(parsed_path):
			for f in d[2]:
				# pprint(os.path.join(d[0], f))
				device = f.split(split_chars)[0]
				device = process_device_name(device)
				devices.append(device)

				file_path = os.path.join(d[0], f)
				cmd = 'sqlite3 "%s" .schema | grep "CREATE TABLE %s "' \
					% (file_path, table_name)
				schema = os.popen(cmd).readline()
				schema = fprocess_schema(schema)

				line1 = "# %s\n" % device
				line2 = "data_%s = '''%s'''\n\n" % (device, schema)

				fw.write(line1)
				fw.write(line2)

			break

		device_schemas_dict = "%s_device_schemas = {\n" % table_name
		for d in devices:
			device_schemas_dict += '  "%s" : data_%s,\n' % (d, d)
		device_schemas_dict = device_schemas_dict.rstrip("\n")
		device_schemas_dict = device_schemas_dict.rstrip(",")
		device_schemas_dict += " }\n"

		fw.write(device_schemas_dict)


if __name__ == '__main__':
	parsed_path = "../TestResource/contact"

	# parse_schema(parsed_path, output, split_chars, table_name, fprocess_schema)
	parse_schema(parsed_path,
							 "./schema_for_data.py",
							 "contacts2.db",
							 "data",
							 process_data_schema)

	parse_schema(parsed_path,
							 "./schema_for_raw_contacts.py",
							 "contacts2.db",
							 "raw_contacts",
							 process_raw_contacts_schema)

