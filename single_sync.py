from flask import Flask, request
from flask import jsonify, Response
import mysql_kueri
import json, urllib2
import c_db
import time
from ConfigParser import SafeConfigParser
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
	return "Tugas Akhir, Sync app"

# SINKRONISASI ----------------------------------------------------------------------------------
@app.route("/sinkron")
def sinkron():
	response = urllib2.urlopen('http://10.151.36.29:5001')
	print "[log] Melakukan sinkronisasi .."
	data = json.load(response)   
	# print data
	return jsonify(data)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port='5002')
	app.config['JSON_AS_ASCII'] = False