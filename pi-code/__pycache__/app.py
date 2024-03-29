#!flask/bin/python
from flask import Flask, jsonify, request
import re
import os
import RPi.GPIO as GPIO
import json
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
app = Flask(__name__)

eventsFileName = "furnanceEvent.json"
events = [
	{
		'on':
		{
			'when':u'2017-03-12 18:00',
 			'temperature':20
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
 			'temperature':21
 		},
 	    'off':{
 			'when':u'2017-03-13 11:00',
 			'temperature':-40
 			},
        'current_timestamp':u'2017-03-27 14:41:00'
 	}
]

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
        # print("Temperature: " + str(tempVal) + " C")
        tempRetVal = tempVal
    else:
        tempRetVal = -99
        print("Got bad crc reading temperture sensor")
    return tempRetVal;

@app.route('/thermal/api/v1.0/time_to_temp', methods=['GET'])
def get_time_to_temp():
	tCalc = PredictDeltaTemp.thermalCalculations
	tempPath = TempSensorId
	dT = events[0]['on']['temperature'] - getCurrentTemp(tempPath)
	secondsToTemp = tCalc.secondsToTemp(dT)
	return jsonify({'seconds_to_temp': 42})

@app.route('/thermal/api/v1.0/events', methods=['GET'])
def get_events():
	with open(eventsFileName) as json_data_file:
            events = json.load(json_data_file)
	json_data_file.close()
	return jsonify({'events': events})

@app.route('/thermal/api/v1.0/current_temp', methods=['GET'])
def get_current_temp():
#    current_temp = getCurrentTemp('/sys/bus/w1/devices/28-04167527baff')
	tempPath = TempSensorId
	current_temp = getCurrentTemp(tempPath)
	return jsonify({'current_temp': current_temp})

@app.route('/thermal/api/v1.0/events', methods=['POST'])
def create_events():
	if not request.json:
	    abort(400)
	events = request.json['events']
	with open(eventsFileName, 'w') as json_data_file:
            try:
                json.dump(events, json_data_file, ensure_ascii=False)
            except:
                abort(500)
	json_data_file.close()
	# FTD 20211230  Current time is no longer sent in the message.  Use internet time.
	# currentTimeStamp = events[0]['current_timestamp']
	# print("Setting date to: " + currentTimeStamp)
	# os.system('sudo date --set=\'' + currentTimeStamp + '\'')
	return jsonify({'events': events});

@app.route('/thermal/api/v1.0/isFurnaceOn', methods=['GET'])
def get_furnance_status():
	furnanceOn =  GPIO.input(relay1)
	if furnanceOn == 0:
		return jsonify({'isFurnanceOn': 'False'})
	return jsonify({'isFurnanceOn': 'True'})

@app.route('/thermal/api/v1.0/isMotionDetected', methods=['GET'])
def get_motion_status():
	if GPIO.input(motionSensorInPin) == 1:
		return jsonify({'isMotionDetected': 'False'})
	return jsonify({'isMotionDetected': 'True'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
