import MySQLdb
import phoenixdb
from flask import Flask
from flask import jsonify

app = Flask(__name__)

@app.route('/select_all')
def select():	
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
	app.run()