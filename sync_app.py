
import paramiko
import string
import webbrowser
import time, os
import re
from datetime import datetime
import MySQLdb

def getLastSync():
	db = MySQLdb.connect(host='localhost', user='root', passwd='root', db='sinkronisasi')
	cursor = db.cursor()

	sql = "SELECT * FROM waktu_sinkronisasi ORDER BY waktu DESC LIMIT 1"
	try :
		cursor.execute(sql)
		row = cursor.fetchone()
		get_date = row[1]
		return get_date
	except :
		print "Error, unable to fetch data"
		return 0		
	db.close()

def insertNewSync():
	ts = time.time()
	timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	print 'time stamp: ', timestamp
	db = MySQLdb.connect(host='localhost', user='root', passwd='root', db='sinkronisasi')	
	cursor = db.cursor()

	sql = "INSERT INTO waktu_sinkronisasi (waktu) VALUES ('{0}')".format(timestamp)
	print 'sql : ', sql

	try :
		cursor.execute(sql)
		db.commit()
		if cursor.lastrowid :
			return cursor.lastrowid
		else :
			return 0
	except :
		db.rollback() 
		print "Error, unable to record current sync time!"
		return 0

	finally :
		db.close


def isDateFormat(input):
    try:
        time.strptime(input, '%y%m%d')
        return True	
    except ValueError:
        return False

def isTimeFormat(input):
    try:
        time.strptime(input, '%H:%M:%S')	
        return True	
    except ValueError:
        return False  

def convertDateTimeFormat(input):
	result = datetime.strptime(input, '%y%m%d %H:%M:%S')
	return result

def mainGetFile() :
	ftp = ssh.open_sftp()
	ftp.get('/var/log/mysql/log_query.log', 'file/get_log_query.log')
	ftp.close()
	# webbrowser.open_new(os.getcwd()+'/get_log_query.log')
	print ("FILE GOT!")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())	
ssh.connect('10.151.36.129', username='administrator', password='m3l0dy!')

allow_q = ["insert", "update", "delete"]

print "1: get file"
print "2: print contents of file"
c = input('Masukan pilihan :')

last_sync = getLastSync()
present = datetime.now()
print 'sinkron terakhir: ',last_sync
print 'waktu sekarang: ', present
print last_sync > present

if c==1 :
	mainGetFile()
if c==2 :
	ftp = ssh.open_sftp()
	file = ftp.file('/var/log/mysql/log_query.log', 'r')
	
	f_list_query = open('file/list_query.txt', 'w')
	for line in file :
		kueri_line = line

		get_waktu = kueri_line.split()
		tgl = str(get_waktu[0])
		wkt = str(get_waktu[1])
		if (isDateFormat(tgl)) :
			# print 'tgl: ',tgl
			if (isTimeFormat(wkt)) :
				# print 'waktu: ',wkt
				date_time_join = tgl + ' ' + wkt
				date_tmp = convertDateTimeFormat(date_time_join)

				print 'date tmp: ', date_tmp
				if (date_tmp > last_sync) :
					print 'sinkronkan'
					if 'Query' in line : 
						for a_q in allow_q :
							q = re.split(r'\t+', kueri_line)
							if (a_q in q[2]) or (a_q.upper() in q[2]) :
								kueri = q[2]
								# print 'kueri: ', kueri
								f_list_query.write(kueri)
	f_list_query.close()
	ftp.close()

	insert_time = insertNewSync()
	if (insert_time) :
		print 'Sync telah dilakukan, last insert id: ', insert_time

	print "DONE!"	
else :
	print "EXIT!";
ssh.close()
