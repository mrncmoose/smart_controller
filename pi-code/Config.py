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

#The number of hours for a given pre-heat window.  
#The predicted start time + this value is allowed before a motion must be sensed.
#If not, shut down & wait for another request to heat up.
PreHeatHours = 2

#TempSensorId: /sys/bus/w1/devices/28-04167527baff
TempSensorId = '/sys/bus/w1/devices/28-0118410e8eff'
# TempSensorId: /home/pi/thermal_controller/temp

relay1 = 17
relay2 = 27
relay3 = 22
relay4 = 10
statusLight = 18
motionSensorInPin = 23

eventsFileName = "furnanceEvent.json"

#------------------------------
# Items needed for AWS IoT MQTT
#------------------------------
awsEndpoint = 'a2vbde4oiektna-ats.iot.us-east-2.amazonaws.com'
awsRootCert = '/home/pi/AWS/root-CA.crt'
awsThingCert = '/home/pi/AWS/7bcc9d228c-certificate.pem.crt'
awsThingKey = '/home/pi/AWS/7bcc9d228c-private.pem.key'
awsThingName = 'SmartThermalController-Test'
awsClientId = awsThingName
awsPort = 8883
awsResponseTopic = awsThingName + '/request/response'
awsRequestTopic = awsThingName + '/request'
