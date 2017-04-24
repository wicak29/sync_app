'''
Script Python untuk melakukan sinkronisasi MySQL dan HBase

'''
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
import conv_phoenix
from ConfigParser import SafeConfigParser

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

def initiateDBtoHBase(data):
	host = data['host']
	username = data['username']
	password = data['password']
	db_name = data['db_name']
	# dump dari MySQL ke csv
	db = MySQLdb.connect(host=host, user=username, passwd=password, db=db_name)
	cursor = db.cursor()
	sql = "SELECT * FROM routes2"
	try :
		cursor.execute(sql)
		result = cursor.fetchall()
		c = csv.writer(open("file/fetchallmysql.csv", "wb"))
		for row in result:
			c.writerow(row)
		return 1
	except :
		print "Error, unable to fetch data from MySQL (",host,")"
		return 0
	db.close()

def getDataAfterLastSync(last_sync):
	data = getConfMysqlDb()
	host = data['host']
	username = data['username']
	password = data['password']
	db_name = data['db_name']
	db = MySQLdb.connect(host=host, user=username, passwd=password, db=db_name)
	cursor = db.cursor()
	sql = "SELECT * FROM routes2 WHERE date_change > '{0}'".format(last_sync)

	try :
		cursor.execute(sql)
		result = cursor.fetchall()
		c = csv.writer(open("file/fetchnewtosync.csv", "wb"))
		for row in result:
			c.writerow(row)
		return 1
	except :
		print "Error, unable to fetch data from MySQL (",host,")"
		return 0
	db.close()


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

def getConfMysqlDb():
	parser = SafeConfigParser()
	parser.read('configuration.ini')

	conf_list = {
		'host' : parser.get('mysql_db', 'host'),
		'username' : parser.get('mysql_db', 'username'),
		'password' : parser.get('mysql_db', 'password'),
		'db_name' : parser.get('mysql_db', 'db_name')
	}
	return conf_list

def getConfHbaseDb():
	parser = SafeConfigParser()
	parser.read('configuration.ini')

	conf_list = {
		'host' : parser.get('hbase_db', 'host')
	}
	return conf_list

def getConfSyncLogDb():
	parser = SafeConfigParser()
	parser.read('configuration.ini')

	conf_list = {
		'host' : parser.get('sync_log_db', 'host'),
		'username' : parser.get('sync_log_db', 'username'),
		'password' : parser.get('sync_log_db', 'password'),
		'db_name' : parser.get('sync_log_db', 'db_name')
	}
	return conf_list

def getSshAccess():
	parser = SafeConfigParser()
	parser.read('configuration.ini')

	conf_list = {
		'host' : parser.get('ssh_access', 'host'),
		'username' : parser.get('ssh_access', 'username'),
		'password' : parser.get('ssh_access', 'password')
	}
	return conf_list

def remoteServerMysqlDb():
	data = getSshAccess()
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
		create_tabel = "psql.py file/routes_create_2.sql" 
		phoenix_cmd = "psql.py -t ROUTES2 file/fetchallmysql.csv"

		try :
			result_create_tabel = subprocess.check_output([create_tabel], shell=True)
			if (result_create_tabel):
				print "Tabel berhasil dibuat di HBase"
				try : 
					result_phoenix = subprocess.check_output([phoenix_cmd], shell=True)
					if (result_phoenix):
						insert_time = insertNewSync(sync_db, mysql_db, hbase_db)
						if (insert_time) :
							print 'Inisialisasi berhasil dilakukan, last insert id: ', insert_time
				except Exception as e:
					print(e)			
		except Exception as e:
			print(e)

allow_q = ["insert", "delete", "update"]

if __name__ == '__main__':
	data_mysql = getConfMysqlDb()
	data_hbase = getConfHbaseDb()
	data_sync_db = getConfSyncLogDb()
	data_ssh = getSshAccess()

	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())	
	ssh.connect(data_ssh['host'], username=data_ssh['username'], password=data_ssh['password'])
	
	print "1: get file log"
	print "2: print contents of file"
	c = input('Masukan pilihan :')

	if c==1 :
		mainGetFile()
	if c==2 :
		last_sync = getLastSync(data_sync_db)
		present = datetime.now()
		print 'sinkron terakhir: ',last_sync
		print 'waktu sekarang: ', present

		if (not last_sync) :
			initiateTransformMysqlToHbase(data_mysql, data_hbase, data_sync_db)
			# print "Belum pernah sinkronisasi"
			# init = initiateDBtoHBase(data_mysql)
			# if (init) :
			# 	print "Data berhasil di export!"
			# 	print "Inisialisasi data awal.."
			# 	print "Mmentransformasi data ke HBase..."
			# 	create_tabel = "psql.py file/routes_create_2.sql" 
			# 	phoenix_cmd = "psql.py -t ROUTES2 file/fetchallmysql.csv"

			# 	try :
			# 		result_create_tabel = subprocess.check_output([create_tabel], shell=True)
			# 		if (result_create_tabel):
			# 			try : 
			# 				result_phoenix = subprocess.check_output([phoenix_cmd], shell=True)
			# 				if (result_phoenix):
			# 					insert_time = insertNewSync(data_sync_db)
			# 					if (insert_time) :
			# 						print 'Inisialisasi berhasil dilakukan, last insert id: ', insert_time
			# 			except Exception as e:
			# 				print(e)			
			# 	except Exception as e:
			# 		print(e)

		elif (last_sync) :
			print "Sinkronisasi terakhir: ", last_sync
			print last_sync > present
			do_patching = False

			'''
			# Mengambil data INSERT dan UPDATE -> bulk ke .csv
			# Kemudian di jalankan dengan Phoenix
			data_in_up = getDataAfterLastSync(last_sync)
			if (data_in_up):
				print "Sinkronisasi terakhir: ", last_sync
				print "Data insert dan update didapat"
				print "Mentransform ke HBase..."
				phoenix_cmd = "psql.py -t ROUTES file/fetchnewtosync.csv"

				try : 
					result_phoenix = subprocess.check_output([phoenix_cmd], shell=True)
				except Exception as e:
					print(e)

				if (result_phoenix) :
					print 'Sync berhasil dilakukan'
			'''

			# Mengambil data DELETE dari remote server, kemudian di simpan di file local
			print "Mengambil data Query dari log ..."
			ftp = ssh.open_sftp()
			file = ftp.file('/var/log/mysql/log_query.log', 'r')
			f_list_query = open('file/list_all_query.sql', 'w')
			date_tmp = ''

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
					insert_time = insertNewSync(data_sync_db, data_mysql, data_hbase)
					if (insert_time) :
						print 'Sync telah dilakukan, last insert id: ', insert_time
					print 'Sync berhasil dilakukan'

		print "Selesai"
	if c==3 :
		print "Key terlarang!"
		getconf = getConfMysqlDb()
		print getconf	
		print getconf['host']
	else :
		print "EXIT!";
	ssh.close()
