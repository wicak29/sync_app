'''
Converter untuk merubah sintaks UPDATE menjadi UPSERT

INPUT : "UPDATE routes SET src_airport = 'ACE' WHERE id_src_airport='1965'"
OUTPUT :to_str = "UPSERT INTO routes (id_route, src_airport, id_src_airport) SELECT id_route,'KZN','2990' FROM routes WHERE id_src_airport='2965'"
	
'''

import re

def update_to_upsert(val) :
	update_str = val
	update_split = update_str.split()

	# Get table name
	tabel = update_split[1]

	kolom = [None]*10
	value = [None]*10

	# get kolom and value betwen SET and WHERE
	fields = re.findall(r'SET(.*?)WHERE', update_str)
	kol_val = fields[0].split(',')
	list_kolom = "(id_route,"
	list_value = " SELECT id_route,"
	for i in range(len(kol_val)):
		tmp = kol_val[i]
		tmp_rmv_space = tmp.replace(" ","")
		tmp_split = tmp_rmv_space.split('=')
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

	final_string = "UPSERT INTO routes2 " + list_kolom + list_value + " FROM routes2 WHERE " + split_where + ";\n"
	return final_string

# x = "update routes2 set codeshare='Y' WHERE id_route=1"
# result = update_to_upsert(x)
# print result