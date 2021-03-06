#!flask/bin/python
from flask import Flask, jsonify, request, Response, abort
from functools import wraps
import re
import os
import RPi.GPIO as GPIO
import json
import datetime
from ThermalPrediction import PredictDeltaTemp

from Config import *

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
#	print('Checking api key of {0} against env value of {1}'.format(key, apiKey))
	if key is not None and key == apiKey:
		return True
	else:
		return Response(	'Could not verify your access level for that URL.\n'
	'You have to login with proper credentials', 401,
	{'WWW-Authenticate': 'Basic realm="I dont like you"'})
		
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
    tempVal = round(float(tempStr[1])/1000, 1)
    tempRetVal = 0
    if "YES" in crc:
        print("Temperature: " + str(tempVal) + " C")
        tempRetVal = tempVal
    else:
        tempRetVal = -99
        print("Got bad crc reading temperture sensor")
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
#    current_temp = getCurrentTemp('/sys/bus/w1/devices/28-04167527baff')
	api_key = request.args.get("api_id")
	res = check_api_key(api_key)
	if res == True:
		tempPath = TempSensorId
		current_temp = getCurrentTemp(tempPath)
		return jsonify({'current_temp': current_temp})
	return res

@app.route('/thermal/api/v1.0/events', methods=['POST'])
# @requires_auth
def create_events():
	api_key = request.args.get("api_id")
	res = check_api_key(api_key)
	if res == True:
		if not request.json:
		    abort(400)
		events = request.json['events']
		for event in events:
			try:
				onDate = datetime.datetime.strptime(str(event['on']['when']), "%Y-%m-%d %H:%M")
				onTemp = float(event['on']['temperature'])
				offTemp = float(event['off']['temperature'])
				motionDelaySecs = int(event['on']['motion_delay_seconds'])			
			except:
				print('Data type problem with json message.')
				abort(410)
		with open(eventsFileName, 'w') as json_data_file:
	            try:
	                json.dump(events, json_data_file, ensure_ascii=False)
	            except:
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
	app.run(host='0.0.0.0', port=5001)
