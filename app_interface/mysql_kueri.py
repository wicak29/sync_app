
def insert_into_routes(table, data):
	print "jumlah kolom: ", len(data)
	str_kolom = ''
	str_values = ''
	for i in range(len(data)):
		str_kolom += str(data[i]['nama'])
		if (data[i]['type']=='int'):
			str_values += "{}".format(str(data[i]['value']))
		else:
			str_values += "'{}'".format(str(data[i]['value']))

		if (i!=len(data)-1):
			str_kolom += ', '
			str_values += ','


	query_string = "INSERT INTO {0} ({1}) VALUES ({2})".format(table, str_kolom, str_values);

	return query_string

def delete_routes_by_id(table, data):
	query_string = "DELETE FROM {0} WHERE {1}={2}".format(table, data['name'], data['value'])

	return query_string