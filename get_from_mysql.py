import MySQLdb

def get_select_all_routes():
	db = MySQLdb.connect(host='10.151.36.129', user='wicak', passwd='m3l0dy!', db='emp')
	cursor = db.cursor()

	sql = "SELECT * FROM routes2"

	try :
		cursor.execute(sql)
		result = cursor.fetchall()
		for row in result :
			print row
	except :
		print "Error, unable to fetch Last Sync data"
		return 0		
	db.close()

if __name__ == '__main__':
	get_select_all_routes()