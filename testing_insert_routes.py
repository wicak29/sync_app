import MySQLdb

def do_insert():
	db = MySQLdb.connect(host='10.151.36.129', user='wicak', passwd='m3l0dy!', db='emp')
	cursor = db.cursor()

	for i in range(114, 300):
		id_route = i+1
		kueri = "INSERT INTO routes2 (id_route, airline, id_airline, src_airport, id_src_airport, dst_airport, id_dst_airport, codeshare, stop_val, equipment, log_date) VALUES ({0},'QG','19305','CGK','3275','SUB','3928','',0,'320', '2017-05-05 07:00:00');".format(id_route)

		try :
			cursor.execute(kueri)
			db.commit()
			if cursor.lastrowid :
				print "row id: ", cursor.lastrowid
			else :
				print "id_route: ", id_route
		except :
			db.rollback() 
			print "Error, unable to record current sync time!"
			return 0
		finally :
			db.close

if __name__ == '__main__':
	do_insert()

