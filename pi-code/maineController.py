#!/usr/bin/env python

import os
import sys
import time
import datetime
from time import sleep, strftime
import re
import json
import RPi.GPIO as GPIO
import argparse
import logging
import logging.handlers

from ThermalPrediction.PredictDeltaTemp import thermalCalculations
from Config import *
from StateKlass import MachineState

parser = argparse.ArgumentParser()
parser.add_argument("--log_level", 
                    help="The level of log messages to log", 
                    default="INFO", 
                    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'])
args = parser.parse_args()
print('Arg passed in: {0}'.format(args.log_level))

# load the kernel modules needed to handle the sensor
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
LOG_FILENAME = 'themeralController.log'
eventLogger = logging.getLogger('EventLogger')
eventLogger.setLevel(level = args.log_level)
logFormatter = logging.Formatter('%(levelname)s\t%(asctime)s\t%(message)s')
logHandler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=20000000, backupCount=2 )
logHandler.setFormatter(logFormatter)
eventLogger.addHandler(logHandler)
startTime = datetime.datetime.now()
isMotionDetected = False
isMotionTimedOut = False
machineState = MachineState()
machineState.changeState('Off')
# A boolean of if the Furnace should be turned on/off.  False -->  off
FurnaceState = False
deltaTime = 0
motionTimeOutSeconds = 900

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

'''
Determines if we are in pre-heat mode.
targetTime is when the system is expected to be at the set temperature
setTemp is the targeted temperature.
'''
def preHeatCheck(targetTime, setTemp):
    global PreHeatHours
    now = datetime.datetime.now()
    secondsToTemp = getSecondsToTemp(setTemp, getCurrentTemp(TempSensorId))
    timeToTemp = targetTime - datetime.timedelta(seconds=secondsToTemp)
    lowerTimeLimit = now - datetime.timedelta(hours=PreHeatHours)
    eventLogger.debug("lower time limit: {0}".format(lowerTimeLimit.strftime("%Y-%m-%d %H:%M:%S")))
    eventLogger.debug('target time now: {0}'.format(timeToTemp))
    
    if targetTime >= lowerTimeLimit and timeToTemp < now:
        eventLogger.debug('Preheat zone reached with time to temp: {0}'.format(timeToTemp))
        return timeToTemp

    return now + datetime.timedelta(hours=12)

def motionAction(motionStartTime):
    global isMotionDetected
    global deltaTime
    global machineState
    global motionTimeOutSeconds
    
    if GPIO.input(motionSensorInPin)==1:
        eventLogger.info("-------->> Motion detected! <<------------")
        motionStartTime = datetime.datetime.now()
        deltaTime = 0
        isMotionDetected = True
        GPIO.output(statusLight, GPIO.HIGH)
    else:
        deltaTime = (datetime.datetime.now()-motionStartTime).total_seconds()
        eventLogger.info("Seconds between motion: {0} with timeout of {1} seconds".format(deltaTime, motionTimeOutSeconds))
            
    if deltaTime >= motionTimeOutSeconds:
        GPIO.output(statusLight, GPIO.LOW)
        isMotionDetected = False
    #If preheating, always show motion.
    if machineState.getCurrentState() == 'Preheating':
        isMotionDetected = True
        deltaTime = 0
        motionStartTime = datetime.datetime.now()        

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

def resetEvents():
    eventsFileName = "furnanceEvent.json"
    events = [
        {
            'on':
            {
                'when':u'1999-04-01 18:00',
                 'temperature':-42,
                 'motion_delay_seconds':30
             },
             'off':{
                'when':u'2017-04-01 18:00',
                 'temperature':-42
             },
        'current_timestamp':u'2020-03-27 14:41:00'
         },
    ]
    try:
        with open(eventsFileName, 'w') as json_data_file:
            json.dump(events, json_data_file)
            json_data_file.close()
    except Exception as e:
        eventLogger.error('Unable to update the events file with error: {0}'.format(e))
        raise Exception(e)
        
def getSetTemp(eventsJsonFile):
    global isMotionDetected
    global machineState
    global motionTimeOutSeconds
    
    try:
        with open(eventsJsonFile) as json_data_file:
            data = json.load(json_data_file)
        json_data_file.close()
    except:
        GPIO.output(relay1, GPIO.HIGH)
        e = sys.exc_info()[0]
        eventLogger.error("Unable to open events file w/ setpoints with exception " + str(e))
    now = datetime.datetime.now()
    for e in data:
        onDate = datetime.datetime.strptime(str(e['on']['when']), "%Y-%m-%d %H:%M")
        setTempOn = float(e['on']['temperature'])
        setTempOff = float(e['off']['temperature'])
        try:
            motionTimeOutSeconds = int(e['on']['motion_delay_seconds'])
        except:
            eventLogger.error('Unable to read motion time out seconds value.  Using value of 300.')
            motionTimeOutSeconds = 300
        setTemp = setTempOff        
        targetOnTime = preHeatCheck(onDate, setTempOn)
        currentState = machineState.getCurrentState()

        eventLogger.debug("on temp: {0}C\t On time: {1}\t Target Time: {2}".format(setTemp, setTempOn, onDate, targetOnTime))
        eventLogger.debug("Current machine state: {0}".format(currentState))
        
        if currentState == 'Heating' and not isMotionDetected:
            resetEvents()
            machineState.changeState("Off")
            eventLogger.info("Machine state to off")
            return setTempOff

        if currentState == 'Off' and targetOnTime <= now:
            machineState.changeState('Preheating')
            eventLogger.info("Machine state change to preheating")
            return setTempOn
        
        if currentState == 'Preheating' and now >= onDate:
            machineState.changeState('Heating')
            eventLogger.info("Machine state change to heating")
            return setTempOn
        if currentState == 'Preheating' or currentState == 'Heating':
            return setTempOn
                 
    return setTemp
        
 
while (True):
    tempVal = getCurrentTemp(TempSensorId)
    startTime = motionAction(startTime)    
    onTemp = getSetTemp("furnanceEvent.json")
    eventLogger.info("Temperature set point\t{0}".format(onTemp))
    if (tempVal < (onTemp - TempWindow)): 
        FurnaceState = True
    if tempVal > (onTemp + TempWindow):
        FurnaceState = False
    if tempVal >= MaxTemp:
        FurnaceState = False
        eventLogger.warn("Max temperature exceeded!")
#    eventLogger.debug("Motion detected flag: {0}".format(isMotionDetected))
        
    if FurnaceState:
        eventLogger.info("Furnace ON")
        GPIO.output(relay1, GPIO.LOW)
#         GPIO.output(statusLight, GPIO.LOW)
    else:
        eventLogger.debug("Furnace off")
        GPIO.output(relay1, GPIO.HIGH)

    sleep(DelayTime)
