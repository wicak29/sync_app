import MySQLdb
import phoenixdb
from flask import Flask, request
from flask import jsonify
import mysql_kueri
import c_db
from ConfigParser import SafeConfigParser

app = Flask(__name__)

data_mysql = c_db.getConfMysqlDb()
data_hbase = c_db.getConfHbaseDb()
data_sync_db = c_db.getConfSyncLogDb()
data_ssh = c_db.getSshAccess()

def connect_db_mysql(data):
	host = data['host']
	username = data['username']
	password = data['password']
	db_name = data['db_name']

	db = MySQLdb.connect(host=host, user=username, passwd=password, db=db_name)
	return db

def connect_db_hbase(data):
	database_url = 'http://localhost:8765/'
	conn = phoenixdb.connect(database_url, autocommit=True)

	return conn

# Insert pasti dilakukan di MySQL database
def insert_into(table, data):
	db = connect_db_mysql(data_mysql)
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
	db = connect_db_mysql(data_mysql)
	cursor = db.cursor()

	kueri = mysql_kueri.delete_routes_by_id(table, data)
	print "kueri: ", kueri
	result = cursor.execute(kueri)
	db.commit()
	db.close()

	if result:
		return 1
	else:
		return 0

def query_db(query, args=(), one=False, db=0):
	# 1 : MySQL
	# 0 : HBase
	if (db==1):
		db = connect_db_mysql(data_mysql)
	else :
		db = connect_db_hbase(data_hbase)

	cursor = db.cursor()
	cursor.execute(query, args)
	result = cursor.fetchall()
	db.close
	return (result[0] if result else None) if one else result

def select_all_routes_mysql():
	routes_list = []
	data = query_db("SELECT * FROM routes2",'',False,0)
	data_numrows = len(data)
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
			'log_date': row[10]
		}
		routes_list.append(route_temp)

	result = { 
		"Host" : "10.151.36.129",
		"Database" : "MySQL",
		"Flight_Rows" : data_numrows,
		"Flight_Routes" : routes_list
		}
	return result

def select_all_routes_hbase():
	database_url = 'http://localhost:8765/'
	conn = phoenixdb.connect(database_url, autocommit=True)

	cursor = conn.cursor()
	cursor.execute("SELECT * FROM ROUTES2")
	
	routes_list = []
	data = cursor.fetchall()
	data_numrows = len(data)
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
			'log_date': row[10]
		}
		routes_list.append(route_temp)

	result = { 
		"Host" : "10.151.36.29",
		"Database" : "HBase",
		"Flight_Rows" : data_numrows,
		"Flight_Routes" : routes_list
		}
	return result

def getLastSync(data):
	host = data['host']
	username = data['username']
	password = data['password']
	db_name = data['db_name']

	db = MySQLdb.connect(host=host, user=username, passwd=password, db=db_name)
	cursor = db.cursor()

	sql = "SELECT * FROM log_sinkronisasi ORDER BY waktu DESC LIMIT 1"
	try :
		cursor.execute(sql)
		row = cursor.fetchone()
		return row
	except :
		print "Error, unable to fetch Last Sync data"
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

# Melakukan SELECT ALL pada tabel ROUTES
@app.route('/select_all_routes')
def select_all_routes():
	print "[log] Select all from table route"
	# Cek status Sinkronisasi
	last = getLastSync(data_sync_db)
	
	# 1 : MySQL
	# 0 : HBase
	if (last[4]==1):
		print "Proses sinkronisasi sedang TIDAK BERLANGSUNG"
		print "Mengambil data dari HBase.."
		get_from = 0
		db_data = data_hbase
	else:
		print "Proses sinkronisasi sedang BERLANGSUNG"
		print "Mengambil data dari MySQL.."
		get_from = 1
		db_data = data_mysql

	print db_data

	routes_list = []
	data = query_db("SELECT * FROM routes2",[],False,get_from)
	data_numrows = len(data)
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
			'log_date': row[10]
		}
		routes_list.append(route_temp)

	result = { 
		"Host" : db_data['host'],
		"Database" : db_data['name'],
		"Flight_Rows" : data_numrows,
		"Flight_Routes" : routes_list
		}

	return jsonify(result)

@app.route('/select_all_airport')
def select_all_airport():
	print "[log] Select all from table airport"

	# Cek status Sinkronisasi
	db = connect_db_mysql(data_sync_db)
	cursor = db.cursor()

	last = getLastSync(data_sync_db)
	# print last
	if (last[4]==1):
		print "Proses sinkronisasi sedang TIDAK BERLANGSUNG"
		result = select_all_routes_mysql()
	else:
		print "Proses sinkronisasi sedang BERLANGSUNG"
		result = select_all_routes_hbase()

	return jsonify(result)

@app.route('/select_all_mysql')
def select_all_mysql():	
	result = select_all_routes_mysql()
	return jsonify(result)

@app.route("/select_all_hbase")
def select_all_hbase():
	result = select_all_routes_hbase()
	return jsonify(result)

@app.route("/")
def hello():
	return "Tugas Akhir, Sync app"

if __name__ == "__main__":
	app.run(host='0.0.0.0')