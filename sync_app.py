'''
Script Python untuk melakukan sinkronisasi MySQL dan HBase

'''
import paramiko
import string
import webbrowser
import time, os, re
from datetime import datetime
import MySQLdb
import csv, sys
import subprocess
import conv_phoenix
import c_db
from ConfigParser import SafeConfigParser

sync_time_init=0
allow_q = ["insert", "delete", "update"]

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
		get_date = row[1]
		return get_date
	except :
		print "Error, unable to fetch Last Sync data"
		return 0		
	db.close()

def dumpMysqlTableToCsv(db_data, tabel_name):
	data = db_data
	host = data['host']
	username = data['username']
	password = data['password']
	db_name = data['db_name']
	# dump dari MySQL ke csv
	db = MySQLdb.connect(host=host, user=username, passwd=password, db=db_name)
	cursor = db.cursor()
	sql = "SELECT * FROM {0}".format(tabel_name)
	file_output = "file/csv/fetch_all_{0}.csv".format(tabel_name)

	print "sql: ", sql
	print "file_output: ", file_output

	try :
		cursor.execute(sql)
		result = cursor.fetchall()
		c = csv.writer(open(file_output, "wb"))
		for row in result:
			c.writerow(row)
		return 1
	except :
		print "Error, unable to fetch data from MySQL (",host,")"
		return 0
	finally:
		db.close()

def initiateDBtoHBase(data_db):
	get_table = c_db.getTableToSync()
	list_table = get_table['table'].replace(" ", "").split(',')
	for table in list_table:
		d = dumpMysqlTableToCsv(data_db, table)
		if (d) :
			print "Berhasil, tabel ", table," berhasil di dump ke fetch_all_",table,".csv"
	return list_table


def insertNewSync(sync_db, mysql_db, hbase_db):
	# DB Log sinkronisasi
	host = sync_db['host']
	username = sync_db['username']
	password = sync_db['password']
	db_name = sync_db['db_name']

	# DB MySQL
	host_mysql = mysql_db['host']

	# DB HBase
	host_hbase = hbase_db['host']

	ts = time.time()
	timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	print 'time stamp: ', timestamp
	db = MySQLdb.connect(host=host, user=username, passwd=password, db=db_name)	
	cursor = db.cursor()

	sql = "INSERT INTO log_sinkronisasi (waktu, ip_src, ip_dst, status) VALUES ('{0}', '{1}', '{2}', '{3}')".format(timestamp,host_mysql,host_hbase,0)
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

def updateStatusSinkronisasi(sync_db, id_log, status):
	# DB Log sinkronisasi
	host = sync_db['host']
	username = sync_db['username']
	password = sync_db['password']
	db_name = sync_db['db_name']

	db = MySQLdb.connect(host=host, user=username, passwd=password, db=db_name)	
	cursor = db.cursor()
	sql = "UPDATE log_sinkronisasi SET status='{0}' WHERE id_log={1}".format(status, id_log)

	try :
		cursor.execute(sql)
		db.commit()
		return 1
	except :
		db.rollback() 
		print "Error, unable to update log status!"
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

def remoteServerMysqlDb():
	data = c_db.getSshAccess()
	host = data['host']
	username = data['username']
	password = data['password']

	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())	
	ssh.connect(host, username=username, password=password)
	return ssh

def mainGetFile() :
	ftp = ssh.open_sftp()
	ftp.get('/var/log/mysql/log_query.log', 'file/get_log_query.log')
	ftp.close()
	# webbrowser.open_new(os.getcwd()+'/get_log_query.log')
	print ("FILE GOT!")

def initiateTransformMysqlToHbase(mysql_db, hbase_db, sync_db):
	print "Belum pernah sinkronisasi"
	init = initiateDBtoHBase(mysql_db)

	if (init) :
		print "Data berhasil di export!"
		print "Inisialisasi data awal.."
		print "Mmentransformasi data ke HBase..."
		create_tabel = "psql.py file/flight_create_2.sql" 

		try :
			result_create_tabel = subprocess.check_output([create_tabel], shell=True)
			if (result_create_tabel):
				print "Tabel berhasil dibuat di HBase"
				for table in init:
					hbase_table = table.upper()
					phoenix_cmd = "psql.py -t {0} file/csv/fetch_all_{1}.csv".format(hbase_table, table)

					try : 
						result_phoenix = subprocess.check_output([phoenix_cmd], shell=True)
						if (result_phoenix):
							print "Tabel {0} berhasil diimport ke HBase...".format(table)
						else :
							print "Tabel {0} gagal diimport ke HBase..".format(table)
					except Exception as e:
						print(e)
			else:
				print "Gagal membuat tabel di HBase.. "			
				
		except Exception as e:
			print(e)

	update_status_sync = updateStatusSinkronisasi(sync_db, sync_time_init, 1)
	if (update_status_sync) :
		print 'Proses inisialisasi selesai..'

if __name__ == '__main__':
	data_mysql = c_db.getConfMysqlDb()
	data_hbase = c_db.getConfHbaseDb()
	data_sync_db = c_db.getConfSyncLogDb()
	data_ssh = c_db.getSshAccess()

	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())	
	ssh.connect(data_ssh['host'], username=data_ssh['username'], password=data_ssh['password'])
	
	# print "1: get file log"
	# print "2: Syncronize MySQL to HBase"
	# c = input('Select an option :')
	
	try : 
		act = int(sys.argv[1])

		if (act==1):
			c = 1
		elif (act==2):
			c = 2
		else :
			c = -1
			print "Parameter salah ..."
			print ">> 1: get file log"
			print ">> 2: Syncronize MySQL to HBase"
	except :
		print "Sintaks salah!"
		c = -1



	if c==1 :
		mainGetFile()
	if c==2 :
		start_time = time.time()
		last_sync = getLastSync(data_sync_db)
		present = datetime.now()
		print 'sinkron terakhir: ',last_sync
		print 'waktu sekarang: ', present

		sync_time_init = insertNewSync(data_sync_db, data_mysql, data_hbase)

		if (not last_sync) :
			initiateTransformMysqlToHbase(data_mysql, data_hbase, data_sync_db)

		elif (last_sync) :
			print "Sinkronisasi terakhir: ", last_sync
			# print last_sync > present
			do_patching = False

			# Mengambil data DELETE dari remote server, kemudian di simpan di file local
			print "Mengambil data Query dari log ..."
			ftp = ssh.open_sftp()
			file = ftp.file('/var/log/mysql/log_query.log', 'r')
			f_list_query = open('file/list_all_query.sql', 'w')
			date_tmp = ''

			count_kueri = 0

			print "Cek aksi INSERT, UPDATE, DELETE pada log..."
			for line in file :
				kueri_line = line

				get_waktu = kueri_line.split()
				
				tgl = str(get_waktu[0])
				if (len(get_waktu)>1):
					wkt = str(get_waktu[1])
				if (isDateFormat(tgl)) :
					if (isTimeFormat(wkt)) :
						date_time_join = tgl + ' ' + wkt
						date_tmp = convertDateTimeFormat(date_time_join)

				if (date_tmp > last_sync) :
					if 'Query' in line : 
						for a_q in allow_q :
							q = re.split(r'\t+', kueri_line)
							if (a_q in q[2]) or (a_q.upper() in q[2]) :
								kueri = q[2].replace("\n", "")
								split_kueri = kueri.split()

								count_kueri+=1
								# Cek jika sintaks adalah UPDATE
								if (split_kueri[0].upper()=="INSERT"):
									print "[sync] INSERT"
									new_kueri = kueri.replace("INSERT", "UPSERT").replace("insert", "UPSERT") + ";\n";
								if (split_kueri[0].upper()=="UPDATE"):
									print "[sync] UPDATE"
									new_kueri = conv_phoenix.update_to_upsert(kueri)
								if (split_kueri[0].upper()=="DELETE") :
									print "[sync] DELETE"
									new_kueri = kueri.replace("INSERT", "UPSERT").replace("insert", "UPSERT") + ";\n";
									
								f_list_query.write(new_kueri)
								do_patching = True
			if (count_kueri ==0) : 
				print "Tidak ada data yang transformasikan!"
				updateStatusSinkronisasi(data_sync_db, sync_time_init, 1)

			f_list_query.close()
			ftp.close()

			# Menjalankan DELETE, INSERT, dan UPDATE
			if (do_patching):
				print "Sinkronisasi, DELETE, INSERT dan UPDATE file on progress sync to HBase..."
				phoenix_cmd = "psql.py -t ROUTES2 file/list_all_query.sql"
				res_phoenix =''

				try : 
					res_phoenix = subprocess.check_output([phoenix_cmd], shell=True)
				except Exception as e:
					print(e)

				if (res_phoenix) :
					insert_time = updateStatusSinkronisasi(data_sync_db, sync_time_init, 1)
					if (insert_time) :
						print 'Update status sinkronisasi berhasil'
					print 'Sync berhasil dilakukan.'

		duration = time.time() - start_time

		print "Durasi sinkronisai : %s seconds" % (duration)
		print "Done"
	if c==3 :
		print "Key terlarang!"
		getconf = c_db.getConfMysqlDb()
		print getconf	
	else :
		print "EXIT!";
	ssh.close()
