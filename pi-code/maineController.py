#!/usr/bin/env python

# 20210126:  BUG  Unit not shutting down after people have left the building.
# conditions:  set temp is not reached.

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
from MotionSensorClass import MotionAction

parser = argparse.ArgumentParser()
parser.add_argument("--log_level", 
                    help="The level of log messages to log", 
                    default="INFO", 
                    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'])
args = parser.parse_args()

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

machineState = MachineState()
machineState.changeState('Off')
# A boolean of if the Furnace should be turned on/off.  False -->  off
FurnaceState = False
deltaTime = 0
motionTimeOutSeconds = 30

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# Set relay pins as output
GPIO.setup(relay1, GPIO.OUT)
GPIO.setup(relay2, GPIO.OUT)
GPIO.setup(relay3, GPIO.OUT)
GPIO.setup(relay4, GPIO.OUT)
GPIO.setup(statusLight, GPIO.OUT)
# GPIO.setup(motionSensorInPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Will be set up in the Motion sensor class.
 
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
    now = datetime.datetime.now()
    secondsToTemp = getSecondsToTemp(setTemp, getCurrentTemp(TempSensorId))
    timeToTemp = targetTime - datetime.timedelta(seconds=secondsToTemp)
    lowerTimeLimit = now - datetime.timedelta(hours=PreHeatHours)
    eventLogger.debug("lower time limit: {0}".format(lowerTimeLimit.strftime("%Y-%m-%d %H:%M:%S")))
    eventLogger.debug('target time now: {0}'.format(timeToTemp))
    
    if targetTime >= lowerTimeLimit and timeToTemp < now:
        eventLogger.debug('Preheat zone reached with time to temp: {0}'.format(timeToTemp))
    
    return timeToTemp

def timeoutAction():
    eventLogger.debug('Time out action called.')
    if machineState.getCurrentState() != 'Preheating':
        eventLogger.info('Motion time out changing state to Off from state of {}'.format(machineState.getCurrentState()))
        machineState.changeState('Off')
        GPIO.output(statusLight, GPIO.LOW)
    
def doMotionAction():
    eventLogger.debug('---> Motion action called')
    mac.isMotionDetected = True
    GPIO.output(statusLight, GPIO.HIGH)

def getSecondsToTemp(setTemp, currentTemp):
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
    tempVal = round(((float(tempStr[1])/1000) * tempSensorSlope) + tempSensorOffset, 1)
    tempRetVal = 30
    if "YES" in crc:
        eventLogger.info("Temperature\t " + str(tempVal))
        tempRetVal = tempVal
    else:
        eventLogger.warning("Got bad crc reading temperature sensor")
    return tempRetVal;

def resetEvents():
    eventsFileName = "furnanceEvent.json"
    events = [
        {
            'on':
            {
                'when':u'1999-04-01T18:00:00',
                 'temperature':-42,
                 'motion_delay_seconds':500
             },
             'off':{
                'when':u'2017-04-01T18:00:00',
                 'temperature':-42
             },
#        'current_timestamp':u'2020-03-27 14:42:00'
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
    retryCount = 0
    targetOnTime = None
    for i in range(0, 2):        
        try:
            with open(eventsJsonFile) as json_data_file:
                data = json.load(json_data_file)
            json_data_file.close()
            break
        except Exception as e:
            eventLogger.error("Unable to open events file w/ setpoints with exception " + str(e))
            eventLogger.error("Waiting 2 seconds to try again.")
            retryCount += 1
            time.sleep(2)   
    if retryCount > 1:
        GPIO.output(relay1, GPIO.HIGH)
        eventLogger.critical('Maximum number of retries to open the setpoints file exceeded!')

    now = datetime.datetime.now()
    for e in data:
        onDate = None
        try:
            onDate = datetime.datetime.strptime(str(e['on']['when']), "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            eventLogger.error('Unable to parse on Date of {} using template of %Y-%m-%dT%H:%M:%S'.format(e['on']['when']))
        if onDate == None:
            try:
                onDate = datetime.datetime.strptime(str(e['on']['when']), "%Y-%m-%d %H:%M:%S")
            except ValueError:
                eventLogger.error('Unable to parse on Date of {} using template of %Y-%m-%d %H:%M:%S'.format(e['on']['when']))
            
        setTempOn = float(e['on']['temperature'])
        setTempOff = float(e['off']['temperature'])
        try:
            newMotionDelay = int(e['on']['motion_delay_seconds'])
            eventLogger.debug('Motion Delay value: {}'.format(newMotionDelay))
            mac.setTimerValue(newMotionDelay)
        except:
            eventLogger.error('Unable to read motion time out seconds value.  Using value of 500.')
            mac.setTimerValue(500)
        setTemp = setTempOff
        if onDate != None:      
            targetOnTime = preHeatCheck(onDate, setTempOn)
            eventLogger.debug("Set on temp: {0}\t On time: {1}\t Target on time: {2}".format(setTempOn, onDate, targetOnTime))

    eventLogger.info("Current machine state: {0}".format(machineState.getCurrentState()))

    if machineState.getCurrentState() == 'Heating' and not mac.isMotionDetected:
        resetEvents()
        machineState.changeState("Off")
        eventLogger.info("Machine state to off")
        return setTempOff
    if targetOnTime is not None:
        if machineState.getCurrentState() == 'Off' and targetOnTime < now < onDate:
            machineState.changeState('Preheating')
            eventLogger.info("Machine state change to preheating")
            return setTempOn
    else:
        eventLogger.info('No target on time to enter preheat mode.')

    if machineState.getCurrentState() == 'Preheating' and onDate <= now:
        machineState.changeState('Heating')
        eventLogger.info("Machine state change to heating")
        return setTempOn
    if machineState.getCurrentState() == 'Preheating' or machineState.getCurrentState() == 'Heating':
        return setTempOn
                 
    return setTemp
        
motionStartTime = datetime.datetime.now()
mac = MotionAction(timeOutSeconds=int(motionTimeOutSeconds),
    sensorInPin=int(motionSensorInPin),
    onMotionCallBack = doMotionAction,
    onMotionTimeOutCallBack = timeoutAction,
    logger=eventLogger)
FurnaceState = False

while (True):
    tempVal = getCurrentTemp(TempSensorId)
    mac.checkForTimeOut()
    onTemp = getSetTemp("furnanceEvent.json")
    eventLogger.info("Temperature set point\t{0}".format(onTemp))
    if tempVal < (onTemp - TempWindow) and machineState.getCurrentState() != 'Off': 
        FurnaceState = True
    if tempVal > (onTemp + TempWindow):
        FurnaceState = False
    if tempVal >= MaxTemp:
        FurnaceState = False
        eventLogger.warning("Max temperature exceeded!")

    eventLogger.debug('Maine loop current state {} and furnance state {}'.format(machineState.getCurrentState(), FurnaceState))        
    if FurnaceState:
        eventLogger.info("Furnace ON")
        GPIO.output(relay1, GPIO.LOW)
    else:
        eventLogger.debug("Furnace off")
        GPIO.output(relay1, GPIO.HIGH)

    sleep(DelayTime)
