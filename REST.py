#!/usr/bin/env python
''' 
    Functions:
		- '/api/v1.0/hostinfo'
		- '/api/v1.0/func'
		- '/api/v1.0/func/<Param>'

'''
__author__ = "JM <chogeha@gmail.com>"
__date__ = "10 Oct. 2018"

# Known bugs that can't be fixed here:
#   - TBD

from flask import Flask, request, redirect, url_for
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify
from werkzeug import secure_filename
import requests

import os
import json
import time
import pdb
import socket
import platform

def _mf_QueryUploadPath():
	strPlatform = platform.architecture()[0]
	strOS = platform.architecture()[1]     

	if "Win" in strOS: # Windows
		return "C:\\PyTestUploadTest"
		
		if '32' in strPlatform:
			print("System is Windows 32Bits")
		else:
			print("System is Windows 64Bits")
	else: # Linux
		return "//opt//PyTestUploadTest"
		
		if '32' in self.strPlatform:
			print("System is Linux 32Bits")
		else:
			print("System is Linux 64Bits")
			
UPLOAD_FOLDER = _mf_QueryUploadPath()
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)

hostname = ""
localip = ""


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class HostInfo(Resource):
	def __init__(self):
		self.hostname = "-1"
		self.localip = "-1.-1.-1.-1"
		self.macaddr = "-1.-1.-1.-1.-1.-1"
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.connect(('8.8.8.8', 80))
			self.hostname = socket.gethostname()
			self.localip = s.getsockname()[0]
			self.localip = s.getsockname()[0]
		finally:
			s.close()
			
	def get(self):
		return jsonify({'HostName': self.hostname, 'IP Address': self.localip})
		
class Function(Resource):
	def get(self):
		#usr = request.get_json()
		header = request.headers		
		print('Get header = ',header)
		for var in header:
			#print('var = ', var, 'index =')
			if 'Model' in var:
				print("Print Model = ", header['Model'])
			elif 'Apikey' in var:
				print("Print APIKey = ", header['Apikey'])
			

		#print('Get username = ', header['username'])
		return jsonify({'message': 'API Test GET!'})
	
	def put(self):
		return jsonify({'message': 'API Test PUT!'})

	#def allowed_file(self, filename):
    #	return '.' in filename and \
	#		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
	
	def post(self):
		header = request.headers
		data = request.data		
		print('Post header = ',header)
		print('Post data =', data, 'type = ',type(data))
		print('Post arge = ', request.args)
		print('Post form = ', request.form)
		print('Post files = ', request.files, ' type = ', type(request.files))
		print('Post values = ', request.values)
		print('Post stream = ', request.stream.read())

		print('Test')
		file = request.files['file']
		if file:
			filename = secure_filename(file.filename)		
			
			if not os.path.exists(app.config['UPLOAD_FOLDER']):
				os.makedirs(app.config['UPLOAD_FOLDER'])
				
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('Upload_File', fn = filename))
		
		return jsonify({'message': 'API Test POST!'})

class FunctionParam(Resource):
    def get(self, Param):
        return jsonify({'Param = ': Param})

# Redirection purpose
@app.route('/api/v1.0/<fn>')
def Upload_File(fn):
	return jsonify({'message': fn})

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response	
	
api.add_resource(HostInfo, '/api/v1.0/hostinfo')
api.add_resource(Function, '/api/v1.0/func')
api.add_resource(FunctionParam, '/api/v1.0/func/<Param>')

if __name__ == '__main__':
     app.run(host='0.0.0.0',port='5000')
