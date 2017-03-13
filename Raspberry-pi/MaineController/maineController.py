#!/usr/bin/env python

#import os
#import glob
import time
from time import sleep, strftime
import re
import ConfigParser
import json

# load the kernel modules needed to handle the sensor
#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')
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
        print "Temperature: " + str(tempVal) + " C"
        tempRetVal = tempVal
    else:
        tempRetVal = 0
        print "Got bad crc reading temperture sensor"
    return tempRetVal;

def getSetTemp(eventsJsonFile):
    # read the settings json file
    with open(eventsJsonFile) as json_data_file:
        data = json.load(json_data_file)    
    json_data_file.close()
    now = time.localtime()
    print "Current time is: " + strftime("%B %d, %Y %H:%M:%S", now)
    for e in data['events']:
        setTemp = -40
        onDate = time.strptime(str(e['on']['when']), "%Y-%m-%d %H:%M")
        offDate = time.strptime(str(e['off']['when']), "%Y-%m-%d %H:%M")
        setTempOn = float(e['on']['temperature'])
        setTempOff = float(e['off']['temperature'])
        if (now >= onDate) and (now <= offDate):
#            print "Set on temp to: " + str(setTempOn)
            setTemp = setTempOn
        if offDate <= now:
#            print "Set off temp to: " + str(setTempOff)
            setTemp = setTempOff
    return setTemp;

Config = ConfigParser.ConfigParser()
Config.read("config.ini")

TempWindow = Config.getfloat("ControlVars", "TempWindow")
OnTempAdder = Config.getfloat("ControlVars", "OnTempAdder")
DelayTime = Config.getint("ControlVars", "DelayTime")
maxTemp = Config.getfloat("ControlVars","MaxTemp")
SensorPath = Config.get("ControlVars","TempSensorId")
# A boolean of if the furnance should be turned on/off.  False -->  off
FurnaceState = False

# V1.0:  Only use one thermal sensor.
devicePath = Config.get("ControlVars", "TempSensorId")
while (True):
    tempVal = getCurrentTemp(SensorPath)
    onTemp = getSetTemp("furnanceEvent.json")
    print "Temperature settings: " + str(onTemp)
    if tempVal < onTemp: 
        FurnaceState = True
    else:
        FurnaceState = False
    if tempVal >= maxTemp:
        FurnaceState = False
        print "Max temperature exceded!"
    if FurnaceState:
        print "Furnance ON"
    else:
        print "Furnance off"
    sleep(DelayTime)
        
