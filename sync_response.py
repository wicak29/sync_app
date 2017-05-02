from flask import Flask, request
from flask import jsonify, Response
import os
import subprocess

app = Flask(__name__)

@app.route("/")
def do_syncronize():
	exec_bash = "bash do_sync.sh"

	try : 
		do_sync = subprocess.check_output([exec_bash], shell=True)
		print do_sync
		if do_sync:
			result = {
				"status" : 1,
				"msg" : "executing sync_app.py"
			}
		else :
			result = {
				"status" : 0,
				"msg" : "can not execute sync_app.py"
			}
	except Exception as e:
		print(e)
		result = {
			"status" : 0,
			"msg" : "failed"
		}

	return jsonify(result)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port='5001')
	app.config['JSON_AS_ASCII'] = False