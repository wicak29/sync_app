import phoenixdb

database_url = 'http://localhost:8765/'
conn = phoenixdb.connect(database_url, autocommit=True)

cursor = conn.cursor()
# cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username VARCHAR)")
# cursor.execute("UPSERT INTO routes VALUES (65000, 'WU', '13757', 'IEV', '2944', 'GRO', '1222','',0,'320')")
a = cursor.execute("SELECT * FROM ROUTES2")
# print cursor.fetchall()
a = cursor.fetchall()
for i in a:
	print i
	# print 'id_route: ', i[0]
	# print 'airline: ', i[1]
	# print 'id_airline: ', i[2]