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

class MotionAction:
    def __init__(self, 
            percentOn:float=100.0, 
            timeOutSeconds:int=299, 
            sensorInPin:int=23, 
            onMotionCallBack = None,
            onMotionTimeOutCallBack = None,
            logger=None) -> None:
        self.onMotionCallBack = onMotionCallBack
        self.onMotionTimeOutCallBack = onMotionTimeOutCallBack
        self.isMotionDetected = True
        self.deltaTime = None
        self.startTime = datetime.datetime.now()  
        self.onCounter = 0  # number of times the motion detector has come before time out
        self.percentToOn = percentOn # ratio of motion events to possible motion events
        self.logger = logger
        self.sensorInPin = sensorInPin
        self.timeOutSeconds = timeOutSeconds
        self.bounceTime_ms = (timeOutSeconds+1)*1000
        GPIO.setup(self.sensorInPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.sensorInPin, GPIO.RISING, callback=self.motionAction, bouncetime=self.bounceTime_ms)

    def setTimerValue(self, timeOutSeconds:int):
        self.timeOutSeconds = timeOutSeconds
        self.bounceTime_ms = (timeOutSeconds+1)*1000
        self.deltaTime = 0
        self.isMotionDetected = True
        self.deltaTime = None
        self.startTime = datetime.datetime.now()  
        GPIO.remove_event_detect(self.sensorInPin)
        GPIO.add_event_detect(self.sensorInPin, GPIO.RISING, callback=self.motionAction, bouncetime=self.bounceTime_ms)
        self.logger.info('Timer values reset to {} seconds and debounce {} ms'.format(self.timeOutSeconds, self.bounceTime_ms))
    
    # This method is called when the motion detector activates for at least self.bounceTime_ms.
    # It also calls the motion action function that was registered.
    def motionAction(self, channel):
        self.logger.info("-------->> Motion detected! <<------------")
        self.logger.debug('Motion on channel {}'.format(channel))
        self.startTime = datetime.datetime.now()
        self.deltaTime = 0
        self.isMotionDetected = True
        self.onCounter += 1
        if self.onMotionCallBack != None:
            self.onMotionCallBack()
        
    def checkForTimeOut(self):
        self.deltaTime = (datetime.datetime.now()-self.startTime).total_seconds()
        if self.deltaTime > self.timeOutSeconds:
            self.isMotionDetected = False
            self.startTime = datetime.datetime.now()
            self.deltaTime = 0
            self.onCounter = 0
            self.logger.info('Motion time out of {} seconds hit'.format(self.timeOutSeconds))
            if self.onMotionTimeOutCallBack != None:
                self.onMotionTimeOutCallBack()
    
    def checkForPercent(self):
        percentTarget = float(self.timeOutSeconds/self.onCounter)
        if percentTarget >= self.percentToOn:
            self.isMotionDetected = False
    
    # Only used for testing & dev.
    # def waitForMotion(self):
    #     testCounter = 0
    #     while True:
    #         sleep(1)
    #         self.checkForTimeOut()
    #         testCounter += 1
    #         if testCounter >= 100:
    #             self.setTimerValue(timeOutSeconds = 15, bounceTime_ms = 15100)

#-------------- End of class definition, start of test harness.

# def timeOutCallBack():
#     print('Motion timed out callback')

# def motionSensedCallBack():
#     print('Motion event call back!')

# parser = argparse.ArgumentParser()
# parser.add_argument("--log_level", 
#                     help="The level of log messages to log", 
#                     default="INFO", 
#                     choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'])
# parser.add_argument("--motionTimeOutSeconds",
#                     help="The number of seconds to wait before logging no motion", 
#                     default=900 )
# parser.add_argument("--percentToOn",
#                     help="The ration of on to off within the motion time out value to turn on.", 
#                     default=1000 )
# parser.add_argument("--motionSensorPin",
#                     help="The GPIO pin the motion sensor is wired to.", 
#                     default=23 )
# args = parser.parse_args()

# # load the kernel modules needed to handle the sensor
# os.system('modprobe w1-gpio')
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# LOG_FILENAME = 'motionSensorTest.log'
# eventLogger = logging.getLogger('EventLogger')
# eventLogger.setLevel(level = args.log_level)
# logFormatter = logging.Formatter('%(levelname)s\t%(asctime)s\t%(message)s')
# logHandler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=20000000, backupCount=2 )
# logHandler.setFormatter(logFormatter)
# eventLogger.addHandler(logHandler)

# mac = MotionAction(timeOutSeconds=int(args.motionTimeOutSeconds),
#     sensorInPin=int(args.motionSensorPin),
#     onMotionCallBack = motionSensedCallBack,
#     onMotionTimeOutCallBack = timeOutCallBack,
#     logger=eventLogger)
# print('Running motion class')
# startTime = datetime.datetime.now()
# halfHour = 60*60/2
# currentTimeOut = int(args.motionTimeOutSeconds)
# while True:
#     mac.checkForTimeOut()
#     sleep(2)
#     secondsRun = (datetime.datetime.now()-startTime).total_seconds()
#     if secondsRun > halfHour:
#         startTime = datetime.datetime.now()
#         currentTimeOut -= 1
#         eventLogger.info('Reseting timeout to {}'.format(currentTimeOut))
#         mac.setTimerValue(currentTimeOut)
