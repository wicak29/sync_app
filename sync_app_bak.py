import paramiko
import string
import webbrowser
import time, os
import re
from datetime import datetime
import MySQLdb
import csv
import sys
import subprocess

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
		print "Error, unable to fetch Last Sync data"
		return 0		
	db.close()

def initiateDBtoHBase():
	# dump MySQL ke csv
	db = MySQLdb.connect(host='10.151.36.129', user='wicak', passwd='m3l0dy!', db='emp')
	cursor = db.cursor()
	sql = "SELECT * FROM daerah"
	try :
		cursor.execute(sql)
		result = cursor.fetchall()
		c = csv.writer(open("file/fetchallmysql.csv", "wb"))
		for row in result:
			c.writerow(row)
		return 1
	except :
		print "Error, unable to fetch data from MySQL (10.151.36.129)"
		return 0
	db.close()

def getDataAfterLastSync(last_sync):
	db = MySQLdb.connect(host='10.151.36.129', user='wicak', passwd='m3l0dy!', db='emp')
	cursor = db.cursor()
	sql = "SELECT * FROM daerah WHERE date_change > '{0}'".format(last_sync)

	try :
		cursor.execute(sql)
		result = cursor.fetchall()
		c = csv.writer(open("file/fetchnewtosync.csv", "wb"))
		for row in result:
			c.writerow(row)
		return 1
	except :
		print "Error, unable to fetch data from MySQL (10.151.36.129)"
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

allow_q = ["delete"]

print "1: get file"
print "2: print contents of file"
c = input('Masukan pilihan :')

if c==1 :
	mainGetFile()
if c==2 :
	last_sync = getLastSync()
	present = datetime.now()
	print 'sinkron terakhir: ',last_sync
	print 'waktu sekarang: ', present

	if (not last_sync) :
		print "Belum pernah sinkronisasi"
		init = initiateDBtoHBase()
		if (init) :
			print "Data berhasil di export!"
			print "Inisialisasi data awal.."
			print "Sedang mentransformasi data ke HBase..."
			phoenix_cmd = "psql.py -t DAERAH3 file/fetchallmysql.csv"

			try : 
				result_phoenix = subprocess.check_output([phoenix_cmd], shell=True)
			except Exception as e:
				print(e)

			insert_time = insertNewSync()
			if (insert_time) :
				print 'Sync telah dilakukan, last insert id: ', insert_time

	elif (last_sync) :
		print last_sync > present
		do_delete = False

		# Mengambil data INSERT dan UPDATE -> bulk ke .csv
		# Kemudian di jalankan dengan Phoenix
		data_in_up = getDataAfterLastSync(last_sync)
		if (data_in_up):
			print "Data insert dan update didapat"
			print "Mentransform ke HBase..."
			phoenix_cmd = "psql.py -t DAERAH3 file/fetchnewtosync.csv"

			try : 
				result_phoenix = subprocess.check_output([phoenix_cmd], shell=True)
			except Exception as e:
				print(e)

			if (result_phoenix) :
				print 'Sync berhasil dilakukan'

		# Mengambil data DELETE dari remote server, kemudian di simpan di file local
		ftp = ssh.open_sftp()
		file = ftp.file('/var/log/mysql/log_query.log', 'r')
		f_list_query = open('file/list_query_delete.sql', 'w')
		date_tmp = ''

		print "Cek aksi DELETE pada log..."
		for line in file :
			kueri_line = line

			get_waktu = kueri_line.split()
			tgl = str(get_waktu[0])
			wkt = str(get_waktu[1])
			if (isDateFormat(tgl)) :
				if (isTimeFormat(wkt)) :
					date_time_join = tgl + ' ' + wkt
					date_tmp = convertDateTimeFormat(date_time_join)

			# print 'date_tmp: ', date_tmp
			# print 'last_sync: ', last_sync
			# print 'date tmp > last_sync :', date_tmp > last_sync
			if (date_tmp > last_sync) :
				print 'sinkronkan'
				if 'Query' in line : 
					for a_q in allow_q :
						q = re.split(r'\t+', kueri_line)
						if (a_q in q[2]) or (a_q.upper() in q[2]) :
							kueri = q[2]
							# print 'kueri: ', kueri
							f_list_query.write(kueri)
							do_delete = True
		f_list_query.close()
		ftp.close()

		# Menjalankan DELETE
		if (do_delete):
			print "Sinkronisasi, DELETE file on progress sync to HBase..."
			phoenix_delete_cmd = "psql.py -t ROUTES file/list_query_delete.sql"

			try : 
				res_phoenix_del = subprocess.check_output([phoenix_cmd], shell=True)
			except Exception as e:
				print(e)

			if (res_phoenix_del) :
				print 'Sync berhasil dilakukan'

		insert_time = insertNewSync()
		if (insert_time) :
			print 'Sync telah dilakukan, last insert id: ', insert_time

	print "DONE!"	
else :
	print "EXIT!";
ssh.close()
