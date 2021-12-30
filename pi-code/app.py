#!flask/bin/python
from flask import Flask, jsonify, request, Response, abort
from functools import wraps
import re
import os
import RPi.GPIO as GPIO
import json
import datetime
import logging
import logging.handlers
#import dumper
from ThermalPrediction import PredictDeltaTemp

from Config import *

# TODO:  Include temperature calibration & other config items found in Config.py
# TODO:  figure out better way to get isMotion and furnanceState instaead of attempting to read values from GPIO.

# load the kernel modules needed to handle the sensor
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
# The script as below using BCM GPIO 00..nn numbers
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay1, GPIO.OUT)
GPIO.setup(statusLight, GPIO.OUT)
GPIO.setup(motionSensorInPin, GPIO.IN)

apiKey = os.environ['API_KEY']

lg = logging.getLogger(__name__)
lg.setLevel(level = 'INFO')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

LOG_FILENAME = 'webAPI.log'
eventLogger = logging.getLogger('EventLogger')
eventLogger.setLevel(level = 'INFO')
logFormatter = logging.Formatter('%(levelname)s\t%(asctime)s\t%(message)s')
logHandler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=20000000, backupCount=2 )
logHandler.setFormatter(logFormatter)
lg.addHandler(logHandler)

lg.info("Starting web API server...")

app = Flask(__name__)

eventsFileName = "furnanceEvent.json"
events = [
	{
		'on':
		{
			'when':u'2017-03-12 18:00',
 			'temperature':20,
 			'motion_delay_seconds':120
 		},
 	    'off':{
			'when':u'2017-03-12 18:00',
 			'temperature':-42
 		},
    'current_timestamp':u'2017-03-27 14:41:00'
 	},
 	{
 		'on':
 		{
 			'when':u'2017-03-13 06:00',
 			'temperature':21,
 			'motion_timeout_seconds':120
 		},
 	    'off':{
 			'when':u'2017-03-13 11:00',
 			'temperature':-40
 			},
        'current_timestamp':u'2017-03-27 14:41:00'
 	}
]
def cToF(tempVal):
    return tempVal * 1.8 +32

def fToC(tempVal):    
    return (tempVal - 32)/1.8

def check_api_key(key):
# FTD 2020-01-12  Removing API key check because the api will only be exposed on localhost, which is trusted.
# Communications with the outside world will be handled via MQTT & GCP ore IoT.
	return True
#	print('Checking api key of {0} against env value of {1}'.format(key, apiKey))
# 	if key is not None and key == apiKey:
# 		return True
# 	else:
# 		return Response(	'Could not verify your access level for that URL.\n'
# 	'You have to login with proper credentials', 401,
# 	{'WWW-Authenticate': 'Basic realm="I dont like you"'})
		
def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def getCurrentTemp(sensorPath):
    # append the device file name to get the absolute path of the sensor
    devicefile = sensorPath + '/w1_slave'
    # open the file representing the sensor.
    fileobj = open(devicefile,'r')
    lines = fileobj.readlines()
    fileobj.close()
    myRegex = re.compile(r"=")
    crc = myRegex.split(lines[0])
    crc = crc[1][3:-1]
    tempStr = myRegex.split(lines[1])
    tempVal = round(((float(tempStr[1])/1000) * tempSensorSlope) + tempSensorOffset, 1) 
    tempRetVal = 0
    if "YES" in crc:
        lg.debug("Temperature: " + str(tempVal) + " C")
        tempRetVal = tempVal
    else:
        tempRetVal = -99
        lg.error("Got bad crc reading temperture sensor")
    return tempRetVal;

@app.route('/thermal/api/v1.0/time_to_temp', methods=['GET'])
# @requires_auth
def get_time_to_temp():
	api_key = request.args.get("api_id")
	res = check_api_key(api_key)
	if res == True:
		tCalc = PredictDeltaTemp.thermalCalculations
		tempPath = TempSensorId
		setTemp = events[0]['on']['temperature']
		currentTemp = getCurrentTemp(tempPath)
		dT =  setTemp - currentTemp
		secondsToTemp = tCalc.secondsToTemp(dT)
		return jsonify({'seconds_to_temp': secondsToTemp, 'temperature set point': setTemp, 'current temp': currentTemp})
	return res

@app.route('/thermal/api/v1.0/events', methods=['GET'])
#@requires_auth
def get_events():
	api_key = request.args.get("api_id")
	res = check_api_key(api_key)
	if res == True:
		with open(eventsFileName) as json_data_file:
	            events = json.load(json_data_file)
		json_data_file.close()
		return jsonify({'events': events})
	return res

@app.route('/thermal/api/v1.0/current_temp', methods=['GET'])
# @requires_auth
def get_current_temp():
	try:
		api_key = request.args.get("api_id")
		res = check_api_key(api_key)
		if res == True:
			tempPath = TempSensorId
			current_temp = getCurrentTemp(tempPath)
			return jsonify({'current_temp': current_temp})
	except Exception as e:
		lg.error('Unable to get current temperature for reason: {}'.format(e))
		return Response('Unable to get current temperature for reason {}'.format(e), 501)
	
	return res

@app.route('/thermal/api/v1.0/events', methods=['POST'])
# @requires_auth
def create_events():
	api_key = request.args.get("api_id")
	res = check_api_key(api_key)
	if res == True:
		if not request.json:
		    abort(400)
		events = None
		if isinstance(request.json, str):
			events = json.loads(request.json)
		else:
			raise TypeError('Error working with requested JSON of type {0}'.format(type(request.json)))
		for event in events:
			try:
				try:
					onDate = datetime.datetime.strptime(str(event['on']['when']), "%Y-%m-%dT%H:%M:%S")
					# onDate = datetime.datetime.strptime(str(event['on']['when']), "%Y-%m-%dT%H:%M:%SZ")
				except ValueError:
 					onDate = datetime.datetime.strptime(str(event['on']['when']), "%Y-%m-%d %H:%M")
				onTemp = float(event['on']['temperature'])
				offTemp = float(event['off']['temperature'])
				motionDelaySecs = int(event['on']['motion_delay_seconds'])			
			except:
				lg.error('Data type problem with json message: \n{0}\n\n'.format(json.dumps(event)))
				abort(410)
		with open(eventsFileName, 'w') as json_data_file:
	            try:
	                json.dump(events, json_data_file, ensure_ascii=False)
	            except Exception as e:
	            	lg.error('Error reading events filename {} with error: {}'.format(eventsFileName, e))
	            	abort(500)
		json_data_file.close()
	#	currentTimeStamp = events[0]['current_timestamp']
	#	print("Setting date to: " + currentTimeStamp)
	#	os.system('sudo date --set=\'' + currentTimeStamp + '\'')
		return jsonify({'events': events});
	return res

@app.route('/thermal/api/v1.0/isFurnaceOn', methods=['GET'])
# @requires_auth
def get_furnance_on():
	api_key = request.args.get("api_id")
	res = check_api_key(api_key)
	if res == True:
		if GPIO.input(relay1) == 1:
			return jsonify({'isFurnanceOn': 'False'})
		return jsonify({'isFurnanceOn': 'True'})
	return res

@app.route('/thermal/api/v1.0/isMotion', methods=['GET'])
# @requires_auth
def get_motion():
	api_key = request.args.get("api_id")
	res = check_api_key(api_key)
	if res == True:
		if GPIO.input(motionSensorInPin) == 1:
			return jsonify({'isMotion': 'False'})
		return jsonify({'isMotion': 'True'})
	return res

if __name__ == '__main__':
#	app.debug = True
	app.run(host='127.0.0.1', port=5001)
