#!/usr/bin/env python

import os
#import glob
import time
from time import sleep, strftime
import re
import ConfigParser
import json
import RPi.GPIO as GPIO
import logging
import logging.handlers
from ThermalPrediction import PredictDeltaTemp

# load the kernel modules needed to handle the sensor
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
LOG_FILENAME = 'themeralController.log'
eventLogger = logging.getLogger('EventLogger')
eventLogger.setLevel(logging.DEBUG)
logFormatter = logging.Formatter('%(levelname)s\t%(asctime)s\t%(message)s')
logHandler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=20000000, backupCount=2 )
logHandler.setFormatter(logFormatter)
eventLogger.addHandler(logHandler)

def getTimeToTemp():
    #the following is wrong:
    uot = PredictDeltaTemp.thermalCalculations
    return uot.deltaTemp(self, 1000)
    
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
        eventLogger.info("Temperature\t " + str(tempVal))
        tempRetVal = tempVal
    else:
        tempRetVal = 0
        eventLogger.warn("Got bad crc reading temperture sensor")
    return tempRetVal;

def getSetTemp(eventsJsonFile):
    # read the settings json file
    try:
        with open(eventsJsonFile) as json_data_file:
            data = json.load(json_data_file)
        json_data_file.close()
    except:
        e = sys.exc_info()[0]
        eventLogger.warn("Unable to open events file w/ setpoints with exception " + str(e))
    now = time.localtime()
#    print "Current time is: " + strftime("%B %d, %Y %H:%M:%S", now)
    for e in data:
        setTemp = -40
        onDate = time.strptime(str(e['on']['when']), "%Y-%m-%d %H:%M")
        offDate = time.strptime(str(e['off']['when']), "%Y-%m-%d %H:%M")
        setTempOn = float(e['on']['temperature'])
        setTempOff = float(e['off']['temperature'])
#TODO:  check how much time is needed to get to the specified temp
# and add it to the onDate

#TODO:  Use the motion sensor to check if anyone is in the building
# Wait for a configurable number of minutes before shutting down.
        if (now >= onDate) and (now <= offDate):
            eventLogger.info("Set on temp to: " + str(setTempOn))
            setTemp = setTempOn
            return setTempOn
        if offDate <= now:
            eventLogger.info("Set off temp to: " + str(setTempOff))
            setTemp = setTempOff
    return setTemp;

Config = ConfigParser.ConfigParser()
Config.read("config.ini")
relay1 = 17
relay2 = 27
relay3 = 22
relay4 = 10
statusLight = 18

# The script as below using BCM GPIO 00..nn numbers
GPIO.setmode(GPIO.BCM)

# Set relay pins as output
GPIO.setup(relay1, GPIO.OUT)
GPIO.setup(relay2, GPIO.OUT)
GPIO.setup(relay3, GPIO.OUT)
GPIO.setup(relay4, GPIO.OUT)
GPIO.setup(statusLight, GPIO.OUT)

#initialize to off
GPIO.output(relay1, GPIO.HIGH)
GPIO.output(relay2, GPIO.HIGH)
GPIO.output(relay3, GPIO.HIGH)
GPIO.output(relay4, GPIO.HIGH)
GPIO.output(statusLight, GPIO.LOW)

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
    eventLogger.info("Temperature settings\t" + str(onTemp))
    if tempVal < onTemp: 
        FurnaceState = True
    else:
        FurnaceState = False
    if tempVal >= maxTemp:
        FurnaceState = False
        eventLogger.warn("Max temperature exceded!")
    if FurnaceState:
        eventLogger.info("Furnance ON")
        GPIO.output(relay1, GPIO.LOW)
        GPIO.output(statusLight, GPIO.LOW)
    else:
        eventLogger.debug("Furnance off")
        GPIO.output(relay1, GPIO.HIGH)
        GPIO.output(statusLight, GPIO.HIGH)
    sleep(DelayTime)
        
