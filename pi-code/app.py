#!flask/bin/python
from flask import Flask, jsonify, request
import re
import os
import json

# load the kernel modules needed to handle the sensor
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

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
 		}
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
 			}
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
        print("Temperature: " + str(tempVal) + " C")
        tempRetVal = tempVal
    else:
        tempRetVal = -99
        print("Got bad crc reading temperture sensor")
    return tempRetVal;

@app.route('/thermal/api/v1.0/events', methods=['GET'])
def get_events():
	with open(eventsFileName) as json_data_file:
            events = json.load(json_data_file)
	json_data_file.close()
	return jsonify({'events': events})

@app.route('/thermal/api/v1.0/current_temp', methods=['GET'])
def get_current_temp():
    current_temp = getCurrentTemp('/sys/bus/w1/devices/28-04167527baff')
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
	return jsonify({'events': events});

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
