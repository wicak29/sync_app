import MySQLdb
import phoenixdb
from flask import Flask, request
from flask import jsonify, Response
import mysql_kueri
import json, urllib2
import c_db
import time
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
	database_url = 'http://{}:8765/'.format(data_hbase['host'])
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
	db.close()
	return (result[0] if result else None) if one else result

def query_db_insert_update(query, db=0):
	# 1 : MySQL
	# 0 : HBase
	if (db==1):
		db = connect_db_mysql(data_mysql)
	else :
		db = connect_db_hbase(data_hbase)

	cursor = db.cursor()
	result = cursor.execute(query)
	db.commit()
	db.close()

	if result:
		return 1
	else :
		return 0

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

# ROUTES ---------------------------------------------------------------------------------------
@app.route('/insert_routes', methods=['POST'])
def insert_routes():
	start_time = time.time()
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
				'type': 'int',
				'value': request.form['id_airline']
			},
			{
				'nama': 'src_airport',
				'type': 'varchar',
				'value': request.form['src_airport']
			},
			{
				'nama': 'id_src_airport',
				'type': 'int',
				'value': request.form['id_src_airport']
			},
			{
				'nama': 'dst_airport',
				'type': 'varchar',
				'value': request.form['dst_airport']
			},
			{
				'nama': 'id_dst_airport',
				'type': 'int',
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

		duration = time.time() - start_time
		print "Durasi waktu : ", duration
		result = {
			"Status" : do_insert,
			"Message" : msg
		}

		return jsonify(result)

@app.route("/delete_routes_by_id", methods=['POST'])
def delete_routes_by_id():
	start_time = time.time()
	do_delete = ''
	msg = ''

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
	
	duration = time.time() - start_time
	print "Durasi waktu : ", duration

	result = {
		"Status" : do_delete,
		"Message" : msg
	}

	return jsonify(result)

@app.route('/select_all_routes')
def select_all_routes():
	start_time = time.time()
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

	duration = time.time() - start_time
	print "Durasi waktu : ", duration

	result = { 
		"Host" : db_data['host'],
		"Database" : db_data['name'],
		"Rows" : data_numrows
		#"Flight_Routes" : routes_list
		}

	return jsonify(result)

@app.route('/select_route_by_id/<id_route>')
def select_route_by_id(id_route):
	start_time = time.time()
	print "[log] Select route by route's ID"	

	last = getLastSync(data_sync_db)
	
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

	kueri = "SELECT * FROM routes2 WHERE id_route = {0}".format(id_route)
	data = query_db(kueri,[],True,get_from)
	
	if (data==None) :
		route = "No data selected"
	else:
		route = {
			'id_route' : data[0],
			'airline' : data[1],
			'id_airline' : data[2],
			'src_airport' : data[3],
			'id_src_airport' : data[4],
			'dst_airport' : data[5],
			'id_dst_airport' : data[6],
			'codeshare' : data[7],
			'stop_val' : data[8],
			'equipment' : data[9],
			'log_date' : data[10]
		}

	duration = time.time() - start_time
	print "Durasi waktu : ", duration

	result = { 
		"host" : db_data['host'],
		"database" : db_data['name'],
		"route" : route
	}

	return jsonify(result)
	# return Response(json.dumps(data, encoding='latin1'), mimetype='application/json')

@app.route('/update_route_by_id', methods=['POST'])
def update_route_by_id():
	start_time = time.time()
	print "[log] UPDATE ROUTES data by routes's ID"
	# Cek status Sinkronisasi

	if request.method == 'POST':
		id_route = request.form['id_route']
		airline = request.form['airline']
		id_airline = request.form['id_airline']
		src_airport = request.form['src_airport']
		id_src_airport = request.form['id_src_airport']
		dst_airport = request.form['dst_airport']
		id_dst_airport = request.form['id_dst_airport']
		codeshare = request.form['codeshare']
		stop_val = request.form['stop_val']
		equipment = request.form['equipment']
		log_date = request.form['log_date']
		
		kueri = ("UPDATE routes2 "
			"SET airline='{0}', "
			"id_airline={1}, "
			"src_airport='{2}', "
			"id_src_airport={3}, "
			"dst_airport='{4}', "
			"id_dst_airport={5}, "
			"codeshare='{6}', "
			"stop_val={7}, "
			"equipment='{8}', "
			"log_date='{9}' "
			"WHERE id_route={10}").format(airline, id_airline, src_airport, id_src_airport, dst_airport, id_dst_airport, codeshare, stop_val, equipment, log_date, id_route)

		print kueri
		do_update = query_db_insert_update(kueri,1)

		if do_update :
			msg = 'Successed to UPDATE table routes'
		else :
			msg = "Failed to UPDATE table routes"

		duration = time.time() - start_time
		print "Durasi waktu : ", duration

		result = {
			"Status" : do_update,
			"Message" : msg
		}

	return jsonify(result)

# AIRLINE ---------------------------------------------------------------------------------------
@app.route('/insert_airline', methods=['POST'])
def insert_airline():
	start_time = time.time()
	if request.method == 'POST' :
		data = [ {
				'nama': 'id_airline',
				'type': 'int',
				'value': request.form['id_airline']
			},
			{
				'nama': 'name',
				'type': 'varchar',
				'value': request.form['name']
			},
			{
				'nama': 'alias',
				'type': 'varchar',
				'value': request.form['alias']
			},
			{
				'nama': 'iata',
				'type': 'varchar',
				'value': request.form['iata']
			},
			{
				'nama': 'icao',
				'type': 'varchar',
				'value': request.form['icao']
			},
			{
				'nama': 'callsign',
				'type': 'varchar',
				'value': request.form['callsign']
			},
			{
				'nama': 'country',
				'type': 'varchar',
				'value': request.form['country']
			},
			{
				'nama': 'active_stat',
				'type': 'varchar',
				'value': request.form['active_stat']
			}
		]

		do_insert = insert_into('airline2', data)
		if do_insert :
			msg = 'Successed INSERT to airline2'
		else :
			msg = "Failed INSERT to airline2"

		duration = time.time() - start_time
		print "Durasi waktu : ", duration

		result = {
			"Status" : do_insert,
			"Message" : msg
		}

		return jsonify(result)

@app.route("/delete_airline_by_id", methods=['POST'])
def delete_airline_by_id():
	start_time = time.time()
	do_delete = ''
	msg = ''

	if request.method == 'POST':
		data = { 'name': 'id_airline',
			'type' : 'int',
			'value' : request.form['id_airline']
		}

		try :
			do_delete = hapus_rute('airline2', data)
			if do_delete :
				msg = "Successed to DELETE"
			else:
				msg = "Failed to DELETE"
		except Exception, e:
				print str(e)

	duration = time.time() - start_time
	print "Durasi waktu : ", duration

	result = {
		"Status" : do_delete,
		"Message" : msg
	}

	return jsonify(result)

@app.route('/select_all_airline')
def select_all_airline():
	start_time = time.time()
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

	airline_list = []
	data = query_db("SELECT * FROM airline2",[],False,get_from)
	data_numrows = len(data)
	for row in data :
		airline = {
			'id_airline' : row[0],
			'name' : row[1],
			'alias' : row[2],
			'iata' : row[3],
			'icao' : row[4],
			'callsign' : row[5],
			'country' : row[6],
			'active_stat' : row[7]
		}
		airline_list.append(airline)

	duration = time.time() - start_time
	print "Durasi waktu : ", duration

	result = { 
		"Host" : db_data['host'],
		"Database" : db_data['name'],
		"Rows" : data_numrows,
		"Airlines" : airline_list
		}

	return Response(json.dumps(result, encoding='latin1'), mimetype='application/json')

@app.route('/select_airline/<id_airline>')
def select_airline(id_airline):
	start_time = time.time()
	print "[log] Select airline by airline's ID"
	# Cek status Sinkronisasi
	# id_airline = int(id_airline)
	print id_airline

	last = getLastSync(data_sync_db)
	
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

	kueri = "SELECT * FROM airline2 WHERE id_airline = {0}".format(id_airline)
	data = query_db(kueri,[],True,get_from)

	if (data==None) : 
		airline = "No data selected"
	else :
		airline = {
			'id_airline' : data[0],
			'name' : data[1],
			'alias' : data[2],
			'iata' : data[3],
			'icao' : data[4],
			'callsign' : data[5],
			'country' : data[6],
			'active_stat' : data[7]
		}

	duration = time.time() - start_time
	print "Durasi waktu : ", duration	

	result = { 
		"host" : db_data['host'],
		"database" : db_data['name'],
		"airline" : airline
	}

	return jsonify(result)
	# return Response(json.dumps(data, encoding='latin1'), mimetype='application/json')

@app.route('/update_airline_by_id', methods=['POST'])
def update_airline():
	start_time = time.time()
	print "[log] UPDATE airline data by airline's ID"
	# Cek status Sinkronisasi

	if request.method == 'POST':
		id_airline = request.form['id_airline']
		name = request.form['name']
		alias = request.form['alias']
		iata = request.form['iata']
		icao = request.form['icao']
		callsign = request.form['callsign']
		country = request.form['country']
		active_stat = request.form['active_stat']
		
		kueri = ("UPDATE airline2 "
			"SET name='{0}', "
			"alias='{1}', "
			"iata='{2}', "
			"icao='{3}', "
			"callsign='{4}', "
			"country='{5}', "
			"active_stat='{6}' "
			"WHERE id_airline={7}").format(name, alias, iata, icao, callsign, country, active_stat, id_airline)

		# pasti 1 karen aksi dilakukan ke db MySQL
		do_update = query_db_insert_update(kueri,1)

		if do_update :
			msg = 'Successed to UPDATE table airline'
		else :
			msg = "Failed to UPDATE table airline"

		duration = time.time() - start_time
		print "Durasi waktu : ", duration

		result = {
			"Status" : do_update,
			"Message" : msg
		}

	return jsonify(result)

# AIRLINE ---------------------------------------------------------------------------------------
@app.route('/insert_airport', methods=['POST'])
def insert_airport():
	start_time = time.time()
	if request.method == 'POST' :
		data = [ {
				'nama': 'airport_id',
				'type': 'int',
				'value': request.form['airport_id']
			},
			{
				'nama': 'name_airport',
				'type': 'varchar',
				'value': request.form['name_airport']
			},
			{
				'nama': 'city',
				'type': 'varchar',
				'value': request.form['city']
			},
			{
				'nama': 'country',
				'type': 'varchar',
				'value': request.form['country']
			},
			{
				'nama': 'iata',
				'type': 'varchar',
				'value': request.form['iata']
			},
			{
				'nama': 'icao',
				'type': 'varchar',
				'value': request.form['icao']
			},
			{
				'nama': 'latitude',
				'type': 'varchar',
				'value': request.form['latitude']
			},
			{
				'nama': 'longitude',
				'type': 'varchar',
				'value': request.form['longitude']
			},
			{
				'nama': 'altitude',
				'type': 'varchar',
				'value': request.form['altitude']
			},
			{
				'nama': 'timezone',
				'type': 'varchar',
				'value': request.form['timezone']
			},
			{
				'nama': 'dst',
				'type': 'varchar',
				'value': request.form['dst']
			},
			{
				'nama': 'tz_db',
				'type': 'varchar',
				'value': request.form['tz_db']
			},
			{
				'nama': 'type_airport',
				'type': 'varchar',
				'value': request.form['type_airport']
			},
			{
				'nama': 'source',
				'type': 'varchar',
				'value': request.form['source']
			}
		]

		do_insert = insert_into('airport2', data)
		if do_insert :
			msg = 'Successed INSERT to airport2'
		else :
			msg = "Failed INSERT to airport2"

		duration = time.time() - start_time
		print "Durasi waktu : ", duration

		result = {
			"Status" : do_insert,
			"Message" : msg
		}
		return jsonify(result)

@app.route("/delete_airport_by_id", methods=['POST'])
def delete_airport_by_id():
	start_time = time.time()
	do_delete = ''
	msg = ''

	if request.method == 'POST':
		data = { 'name': 'airport_id',
			'type' : 'int',
			'value' : request.form['airport_id']
		}

		try :
			do_delete = hapus_rute('airport2', data)
			if do_delete :
				msg = "Successed to DELETE"
			else:
				msg = "Failed to DELETE"
		except Exception, e:
				print str(e)

	duration = time.time() - start_time
	print "Durasi waktu : ", duration

	result = {
		"Status" : do_delete,
		"Message" : msg
	}

	return jsonify(result)

@app.route('/select_all_airport')
def select_all_airport():
	start_time = time.time()
	print "[log] Select all from table airport"
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

	airport_list = []
	data = query_db("SELECT * FROM airport2",[],False,get_from)
	data_numrows = len(data)
	for row in data :
		airport = {
			'airport_id' : row[0],
			'name_airport' : row[1],
			'city' : row[2],
			'country' : row[3],
			'iata' : row[4],
			'icao' : row[5],
			'latitude' : row[6],
			'longitude' : row[7],
			'altitude' : row[8],
			'timezone': row[9],
			'dst' : row[10],
			'tz_db' : row[11],
			'type_airport' : row[12],
			'source' : row[13]
		}
		airport_list.append(airport)

	duration = time.time() - start_time
	print "Durasi waktu : ", duration

	result = { 
		"Host" : db_data['host'],
		"Database" : db_data['name'],
		"Rows" : data_numrows,
		"Airport" : airport_list
		}

	return Response(json.dumps(result, encoding='latin1'), mimetype='application/json')

@app.route('/select_airport/<airport_id>')
def select_airport(airport_id):
	start_time = time.time()
	print "[log] Select airport by airport's ID"

	last = getLastSync(data_sync_db)
	
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

	kueri = "SELECT * FROM airport2 WHERE airport_id = {0}".format(airport_id)
	data = query_db(kueri,[],True,get_from)

	if (data==None) : 
		airport = "No data selected"
	else :
		airport = {
			'airport_id' : data[0],
			'name_airport' : data[1],
			'city' : data[2],
			'country' : data[3],
			'iata' : data[4],
			'icao' : data[5],
			'latitude' : data[6],
			'longitude' : data[7],
			'altitude' : data[8],
			'timezone': data[9],
			'dst' : data[10],
			'tz_db' : data[11],
			'type_airport' : data[12],
			'source' : data[13]
		}

	duration = time.time() - start_time
	print "Durasi waktu : ", duration

	result = { 
		"host" : db_data['host'],
		"database" : db_data['name'],
		"airport" : airport
	}

	return jsonify(result)
	# return Response(json.dumps(data, encoding='latin1'), mimetype='application/json')

@app.route('/update_airport', methods=['POST'])
def update_airport():
	start_time = time.time()
	print "[log] UPDATE airport data by airport's ID"
	# Cek status Sinkronisasi

	if request.method == 'POST':
		airport_id = request.form['airport_id']
		name_airport = request.form['name_airport']
		city = request.form['city']
		country = request.form['country']
		iata = request.form['iata']
		icao = request.form['icao']
		latitude = request.form['latitude']
		longitude = request.form['longitude']
		altitude = request.form['altitude']
		timezone = request.form['timezone']
		dst = request.form['dst']
		tz_db = request.form['tz_db']
		type_airport = request.form['type_airport']
		source =  request.form['source']
		
		kueri = ("UPDATE airport2 "
			"SET name_airport='{0}', "
			"city='{1}', "
			"country='{2}', "
			"iata='{3}', "
			"icao='{4}', "
			"latitude='{5}', "
			"longitude='{6}', "
			"altitude='{7}', "
			"timezone='{8}', "
			"dst='{9}', "
			"tz_db='{10}', "
			"type_airport='{11}', "
			"source='{12}' "
			"WHERE airport_id={13}").format(name_airport, city, country, iata, icao, latitude, longitude, altitude, timezone, dst, tz_db, type_airport, source, airport_id)

		# pasti 1 karen aksi dilakukan ke db MySQL
		print kueri
		do_update = query_db_insert_update(kueri,1)

		if do_update :
			msg = 'Successed to UPDATE table airport'
		else :
			msg = "Failed to UPDATE table airport"

		duration = time.time() - start_time
		print "Durasi waktu : ", duration
		
		result = {
			"Status" : do_update,
			"Message" : msg
		}

	return jsonify(result)

# KOMPLEKS SELECT -------------------------------------------------------------------------------
@app.route('/select_routes_country/<id_route>')
def select_routes_country(id_route):
	start_time = time.time()
	print "[log] SELECT Join routes with airline country"

	last = getLastSync(data_sync_db)
	
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

	kueri = "SELECT a.*,b.name,b.country  FROM routes2 a JOIN airline2 b ON a.id_airline = b.id_airline WHERE a.id_route = {0}".format(id_route)
	data = query_db(kueri,[],True,get_from)

	if (data==None) : 
		route = "No data selected"
	else :
		route = {
			'id_route' : data[0],
			'airline' : data[1],
			'id_airline' : data[2],
			'src_airport' : data[3],
			'id_src_airport' : data[4],
			'dst_airport' : data[5],
			'id_dst_airport' : data[6],
			'codeshare' : data[7],
			'stop_val' : data[8],
			'equipment' : data[9],
			'log_date' : data[10],
			'name' : data[11],
			'country': data[12]
		}

	duration = time.time() - start_time
	print "Durasi waktu : ", duration

	result = { 
		"host" : db_data['host'],
		"database" : db_data['name'],
		"route" : route
	}

	return jsonify(result)
	# return Response(json.dumps(data, encoding='latin1'), mimetype='application/json')

@app.route('/select_all_number_routes_by_airline')
def select_all_number_routes_by_airline():
	start_time = time.time()
	print "[log] Select all number routes by airline"
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

	airline_list = []
	data = query_db("SELECT a.id_airline,b.name,count(id_route) FROM routes2 a JOIN airline2 b ON a.id_airline = b.id_airline GROUP BY a.id_airline,b.name",[],False,get_from)
	data_numrows = len(data)
	for row in data :
		route = {
			'id_airline' : row[0],
			'airline_name' : row[1],
			'number_routes' : row[2]
		}
		airline_list.append(route)

	duration = time.time() - start_time
	print "Durasi waktu : ", duration

	result = { 
		"Host" : db_data['host'],
		"Database" : db_data['name'],
		"Rows" : data_numrows,
		"Routes" : airline_list
		}

	return Response(json.dumps(result, encoding='latin1'), mimetype='application/json')

@app.route('/select_all_number_routes_more_than/<number>')
def select_all_number_routes_more_than(number):
	start_time = time.time()
	print "[log] Select all number routes more than x"
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

	airline_list = []
	kueri = "SELECT id_airline, count(id_route) FROM routes2 GROUP BY id_airline HAVING COUNT(*) > {0}".format(number)
	data = query_db(kueri,[],False,get_from)
	data_numrows = len(data)
	for row in data :
		route = {
			'id_airline' : row[0],
			'number_routes' : row[1]
		}
		airline_list.append(route)

	duration = time.time() - start_time
	print "Durasi waktu : ", duration

	result = { 
		"Host" : db_data['host'],
		"Database" : db_data['name'],
		"Rows" : data_numrows,
		"Routes" : airline_list
		}

	return Response(json.dumps(result, encoding='latin1'), mimetype='application/json')

@app.route('/select_all_airline_in_routes')
def select_all_airline_in_routes():
	start_time = time.time()
	print "[log] Select all airline in routes"
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

	airline_list = []
	kueri = "SELECT DISTINCT id_airline from routes2"
	data = query_db(kueri,[],False,get_from)
	data_numrows = len(data)
	for row in data :
		route = {
			'id_airline' : row[0]
		}
		airline_list.append(route)

	duration = time.time() - start_time
	print "Durasi waktu : ", duration

	result = { 
		"Host" : db_data['host'],
		"Database" : db_data['name'],
		"Rows" : data_numrows,
		"Routes" : airline_list
		}

	return Response(json.dumps(result, encoding='latin1'), mimetype='application/json')

# SINKRONISASI ----------------------------------------------------------------------------------
@app.route("/sinkron")
def sinkron():
	response = urllib2.urlopen('http://10.151.36.29:5001')
	print "[log] Melakukan sinkronisasi .."
	data = json.load(response)   
	# print data
	return jsonify(data)

# ------------------------------------------------------------------------------------- #
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

# ------------------------------------------------------------------------------------- #

if __name__ == "__main__":
	app.run(host='0.0.0.0')
	app.config['JSON_AS_ASCII'] = False
