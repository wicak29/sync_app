'''
Converter untuk merubah sintaks UPDATE menjadi UPSERT

INPUT : "UPDATE routes SET src_airport = 'ACE' WHERE id_src_airport='1965'"
OUTPUT :to_str = "UPSERT INTO routes (id_route, src_airport, id_src_airport) SELECT id_route,'KZN','2990' FROM routes WHERE id_src_airport='2965'"
	
'''

import re
from ConfigParser import SafeConfigParser

def getPrimaryKey():
	parser = SafeConfigParser()
	parser.read('configuration.ini')

	conf_list = {
		'table' : parser.get('mysql_table', 'table'),
		'primary_key' : parser.get('mysql_table', 'primary_key')
	}
	return conf_list

def update_to_upsert(val) :
	update_str = val
	update_split = update_str.split()

	# Get table name
	tabel = update_split[1]

	kolom = [None]*50
	value = [None]*50

	# Get nama table
	table_name = re.findall(r'UPDATE(.*?)SET', update_str)[0].replace(" ", "")
	print "nama tabel: ", table_name

	# Mencari Primary Key Table
	get_list_tabel = getPrimaryKey()
	list_table = get_list_tabel['table'].split(',')
	list_pk = get_list_tabel['primary_key'].split(',')
	if (table_name in list_table):
		pos = list_table.index(table_name)
		pk = list_pk[pos]
		print "PK: ", pk
	else:
		return 0

	# get kolom and value betwen SET and WHERE
	fields = re.findall(r'SET(.*?)WHERE', update_str)
	kol_val = fields[0].split(',')
	list_kolom = "({0},".format(pk)
	list_value = " SELECT {0},".format(pk)
	for i in range(len(kol_val)):
		tmp = kol_val[i]
		# tmp_rmv_space = tmp.replace(" ","")
		tmp_split = tmp.split('=')
		kolom[i] = tmp_split[0]
		value[i] = tmp_split[1]
		if (i==(len(kol_val)-1)):
			list_kolom += kolom[i] + ")"
			list_value += value[i]
		else :
			list_kolom += kolom[i] + ","
			list_value += value[i] + ","


	# get kolom and value after WHERE
	last_pos = len(kol_val)
	split_where = update_str.split('WHERE')[1]

	final_string = "UPSERT INTO {0} {1} {2} FROM {0} WHERE {3};\n".format(table_name, list_kolom, list_value, split_where)
	return final_string

# x = "UPDATE airline2 SET iata='PR', callsign='PRIVATE', country='Unknown' WHERE id_airline=1"
# result = update_to_upsert(x)
# print result