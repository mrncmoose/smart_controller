'''
Configuration variables for the Flask Web App
FTD 2019-10-16
'''

OnTempAdder= 0.5

# The number of seconds to wait between temperature readings.
# Must be less than 6 for the motion sensor to get reasonable readings
DelayTime= 2
MaxTemp= 30

# Temperature control within +/-
TempWindow= 1.0

#The number of seconds of no motion detected after the set start time to shut the furnace down.
# will want 900 (15 minutes) in prod.  Test much shorter
#FTD 2019-10-23, moved to JSON event message
#motionTimeOutSeconds = 45

#The number of hours for a given pre-heat window.  
#The predicted start time + this value is allowed before a motion must be sensed.
#If not, shut down & wait for another request to heat up.
PreHeatHours = 2

#TempSensorId= '/sys/bus/w1/devices/28-04167527baff'
# TempSensorId = '/sys/bus/w1/devices/28-0118410e8eff'
TempSensorId = '/sys/bus/w1/devices/28-0118410baaff'
# TempSensorId: /home/pi/thermal_controller/temp

#TODO:  Add sensor calibration values

relay1 = 17
relay2 = 27
relay3 = 22
relay4 = 10
statusLight = 18
motionSensorInPin = 23

# GCP IoT core MQTT messaging items
host = 'mqtt.googleapis.com'
port = 8883
QoS = 0
project_id = 'iotsmartcontroller'
cloud_region = 'us-central1'
registry_id = 'TestMooseIoTRegistry'
gateway_id = 'MooseIoTGateway'
device_id = 'smart-tstat-test'
certDir = 'certs'
privateKeyFile = certDir + '/rsa_private.pem'
ca_certs = certDir + '/roots.pem'
algorithm = 'RS256'
#The id/key assigned to this thing via the central server.  Each thing Id is unique.
#ourThingId = 2   #Training building is id = 2
ourThingId = 3    #Marie thing for test.

#API URI's for local API
localApiUser = 'admin'
localApiPass = 'secret'
baseURL = 'http://127.0.0.1:5001'
tempertureURI = '/thermal/api/v1.0/current_temp'
eventURI = '/thermal/api/v1.0/events'
runningURI = '/thermal/api/v1.0/isFurnaceOn'

#The server the 'world' will interact with via it's API's.
#Polling isn't the best way to do this, but HTTP is currently the only protocol working.
centralServer = { 'baseURL': 'https://iotsmartcontroller.appspot.com',
                 'eventURI': '/iot/api/thermal-events/',
                 'currentReadingURI': '/iot/api/thing-data/',
                 'thingsURI': '/iot/api/things/'
                 }
# centralServer = { 'baseURL': 'http://10.0.0.9:8000',
#                  'eventURI': '/iot/api/thermal-events/',
#                  'currentReadingURI': '/iot/api/thing-data/',
#                  'thingsURI': '/iot/api/things/'
#                  }
