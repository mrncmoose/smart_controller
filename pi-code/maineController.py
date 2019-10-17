#!/usr/bin/env python

import os
#import glob
import time
import datetime
from time import sleep, strftime
import re
import json
import RPi.GPIO as GPIO
import logging
import logging.handlers

from ThermalPrediction.PredictDeltaTemp import thermalCalculations
from Config import *

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
startTime = datetime.datetime.now()
isMotionDetected = False
isMotionTimedOut = False
isHeating = False
isPreHeating = False
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# Set relay pins as output
GPIO.setup(relay1, GPIO.OUT)
GPIO.setup(relay2, GPIO.OUT)
GPIO.setup(relay3, GPIO.OUT)
GPIO.setup(relay4, GPIO.OUT)
GPIO.setup(statusLight, GPIO.OUT)
GPIO.setup(motionSensorInPin, GPIO.IN)
 
#initialize to off
GPIO.output(relay1, GPIO.HIGH)
GPIO.output(relay2, GPIO.HIGH)
GPIO.output(relay3, GPIO.HIGH)
GPIO.output(relay4, GPIO.HIGH)
GPIO.output(statusLight, GPIO.LOW)

maxTemp = MaxTemp

# A boolean of if the Furnace should be turned on/off.  False -->  off
FurnaceState = False
isMotionDetected = False
deltaTime = 0

def preHeatCheck(targetTime, setTemp):
    secondsToTemp = getSecondsToTemp(setTemp, getCurrentTemp(TempSensorId))
    timeToTemp = datetime.datetime.now() - datetime.timedelta(seconds=secondsToTemp)
    if timeToTemp <= datetime.datetime.now() and setTemp < getCurrentTemp(TempSensorId):
        isPreHeating = True
    else:
        isPreHeating = False

def motionAction(motionStartTime):
    deltaTime = 0
    if GPIO.input(motionSensorInPin)==1:
        eventLogger.debug("-------->> Motion detected! <<------------")
        GPIO.output(statusLight, GPIO.HIGH)
        deltaTime = (datetime.datetime.now()-motionStartTime).total_seconds()
        eventLogger.debug("Seconds between motion: {0}".format(deltaTime))
        GPIO.output(statusLight, 1)
    if(deltaTime < motionTimeOutSeconds):
        motionStartTime = datetime.datetime.now()
        isMotionDetected = True
    else:
        GPIO.output(statusLight, 0)
        isMotionDetected = False
        eventLogger.debug('No motion in {0} seconds.'.format(deltaTime))         
    return motionStartTime

def getSecondsToTemp(setTemp, currentTemp):
    # updating to correct method
    dT = setTemp - currentTemp
    return thermalCalculations.secondsToTemp(dTemp=dT)
    
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
    tempRetVal = 30
    if "YES" in crc:
        eventLogger.info("Temperature\t " + str(tempVal))
        tempRetVal = tempVal
    else:
        eventLogger.warn("Got bad crc reading temperature sensor")
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
    now = datetime.datetime.now()   
    for e in data:
        setTemp = -40
        onDate = datetime.datetime.strptime(str(e['on']['when']), "%Y-%m-%d %H:%M")
#        offDate = time.strptime(str(e['off']['when']), "%Y-%m-%d %H:%M")
        setTempOn = float(e['on']['temperature'])
        setTempOff = float(e['off']['temperature'])
        secondsToTemp = getSecondsToTemp(setTempOn, getCurrentTemp(TempSensorId))
        onDate = onDate - datetime.timedelta(seconds=secondsToTemp)
        eventLogger.info("Updated datetime to get to temperature: " + onDate.strftime("%Y-%m-%d %H:%M:%S"))
# Check for motion only after the onDate + MotionDelayTime
        if (now >= onDate and isMotionDetected):
            eventLogger.info("Set on temp to: " + str(setTempOn))
            setTemp = setTempOn
            return setTempOn
        else:
            eventLogger.info("Set off temp to: " + str(setTempOff))
            setTemp = setTempOff
    return setTemp
    
 
while (True):
    tempVal = getCurrentTemp(TempSensorId)
    startTime = motionAction(startTime)    
    onTemp = getSetTemp("furnanceEvent.json")
    eventLogger.info("Temperature settings\t{0{".format(onTemp))
    eventLogger .info("Seconds since last motion {0} and timeout value of {1}".format(deltaTime, motionTimeOutSeconds))
    if (tempVal < (onTemp - TempWindow)): 
        FurnaceState = True
    if tempVal > (onTemp + TempWindow):
        FurnaceState = False
    if tempVal >= maxTemp:
        FurnaceState = False
        eventLogger.warn("Max temperature exceeded!")
    #If the current temperature is at or above the set temperature
    # and there has not been any motion in motionTimeOutSeconds
    # turn furnace off.
    eventLogger.debug("Motion detected flag: {0}".format(isMotionDetected))
        
    if FurnaceState:
        eventLogger.info("Furnace ON")
        GPIO.output(relay1, GPIO.LOW)
#         GPIO.output(statusLight, GPIO.LOW)
    else:
        eventLogger.debug("Furnace off")
        GPIO.output(relay1, GPIO.HIGH)

    sleep(DelayTime)
