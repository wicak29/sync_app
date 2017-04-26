import MySQLdb
import phoenixdb
from flask import Flask, request
from flask import jsonify
import mysql_kueri

app = Flask(__name__)

def insert_into(table, data):
	db = MySQLdb.connect("10.151.36.129","wicak","m3l0dy!","emp" )
	cursor = db.cursor()

	kueri = mysql_kueri.insert_into_routes(table, data)
	print "kueri: ", kueri
	cursor.execute(kueri)
	db.commit()
	db.close()

	if kueri:
		return 1
	else:
		return 0

def hapus_rute(table, data):
	db = MySQLdb.connect("10.151.36.129","wicak","m3l0dy!","emp" )
	cursor = db.cursor()
	print data
	print table

	kueri = mysql_kueri.delete_routes_by_id(table, data)
	print "kueri: ", kueri
	result = cursor.execute(kueri)
	db.commit()
	db.close()

	if result:
		return 1
	else:
		return 0

@app.route('/insert_routes', methods=['POST'])
def insert_routes():
	if request.method == 'POST' :
		data = [ {
				'nama': 'id_route',
				'type': 'int',
				'value': request.form['id_route']
			},
			{
				'nama': 'airline',
				'type': 'varchar',
				'value': request.form['airline']
			},
			{
				'nama': 'id_airline',
				'type': 'varchar',
				'value': request.form['id_airline']
			},
			{
				'nama': 'src_airport',
				'type': 'varchar',
				'value': request.form['src_airport']
			},
			{
				'nama': 'id_src_airport',
				'type': 'varchar',
				'value': request.form['id_src_airport']
			},
			{
				'nama': 'dst_airport',
				'type': 'varchar',
				'value': request.form['dst_airport']
			},
			{
				'nama': 'id_dst_airport',
				'type': 'varchar',
				'value': request.form['id_dst_airport']
			},
			{
				'nama': 'codeshare',
				'type': 'varchar',
				'value': request.form['codeshare']
			},
			{
				'nama': 'stop_val',
				'type': 'int',
				'value': request.form['stop_val']
			},
			{
				'nama': 'equipment',
				'type': 'varchar',
				'value': request.form['equipment']
			},
			{
				'nama': 'log_date',
				'type': 'varchar',
				'value': request.form['log_date']
			}
		]

		do_insert = insert_into('routes2', data)
		if do_insert :
			msg = 'Successed to INSERT'
		else :
			msg = "Failed to INSERT"

		result = {
			"Status" : do_insert,
			"Message" : msg
		}

		return jsonify(result)

@app.route("/delete_routes_by_id", methods=['POST'])
def delete_routes_by_id():
	if request.method == 'POST':
		id_route = request.form['id_route']
		data = { 'name': 'id_route',
			'type' : 'int',
			'value' : request.form['id_route']
		}

		try :
			do_delete = hapus_rute('routes2', data)
			if do_delete :
				msg = "Successed to DELETE"
			else:
				msg = "Failed to DELETE"
		except Exception, e:
				print str(e)

		result = {
			"Status" : do_delete,
			"Message" : msg
		}

		return jsonify(result)

@app.route('/select_all_mysql')
def select_all_mysql():	
	db = MySQLdb.connect("10.151.36.129","wicak","m3l0dy!","emp" )
	cursor = db.cursor()

	query_string = "SELECT * FROM routes2"
	cursor.execute(query_string)

	routes_list = []
	data = cursor.fetchall()
	data_numrows = int(cursor.rowcount)
	for row in data :
		route_temp = {
			'id_route': row[0],
			'airline': row[1],
			'id_airline': row[2],
			'src_airport': row[3],
			'id_src_airport': row[4],
			'dst_airport': row[5],
			'id_dst_airport': row[6],
			'codeshare': row[7],
			'stop_val': row[8],
			'equipment': row[9],
			'date_change': row[10]
		}
		routes_list.append(route_temp)

	db.close()
	result = { 
		"Flight_Rows" : data_numrows,
		"Flight_Routes" : routes_list
		}

	return jsonify(result)

@app.route("/select_all_hbase")
def select_all_hbase():
	database_url = 'http://localhost:8765/'
	conn = phoenixdb.connect(database_url, autocommit=True)

	cursor = conn.cursor()
	a = cursor.execute("SELECT * FROM ROUTES2")
	
	routes_list = []
	data = cursor.fetchall()
	data_numrows = int(cursor.rowcount)
	print "[log] jumlah baris: ", len(data)
	for row in data :
		route_temp = {
			'id_route': row[0],
			'airline': row[1],
			'id_airline': row[2],
			'src_airport': row[3],
			'id_src_airport': row[4],
			'dst_airport': row[5],
			'id_dst_airport': row[6],
			'codeshare': row[7],
			'stop_val': row[8],
			'equipment': row[9],
			'date_change': row[10]
		}
		routes_list.append(route_temp)

	result = { 
		"Flight_Rows" : data_numrows,
		"Flight_Routes" : routes_list
		}

	return jsonify(result)

@app.route("/")
def hello():
	return "Hello World!"

if __name__ == "__main__":
	app.run(host='0.0.0.0')