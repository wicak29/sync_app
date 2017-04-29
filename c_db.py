import MySQLdb
from ConfigParser import SafeConfigParser

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
