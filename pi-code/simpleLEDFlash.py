'''
Created on Jan 1, 2019

@author: Fred T. Dunaway
'''
import RPi.GPIO as GPIO
import time
import datetime

statusLedPin = 18
motionSensorInPin = 23
heatRelay1 = 17
motionTimeOutSeconds = 15
heatOnFlag = False
preHeatFlag = False
heatOnDate = time.strptime('2019-01-13 13:20', "%Y-%m-%d %H:%M")
tempSetpoint = 20.0
tempWindow = 3
GPIO.setmode(GPIO.BCM)
# (GPIO.BOARD) is physical pin
GPIO.setwarnings(False)
GPIO.setup(statusLedPin, GPIO.OUT)
GPIO.setup(heatRelay1, GPIO.OUT)
GPIO.setup(motionSensorInPin, GPIO.IN)
GPIO.setup(statusLedPin, GPIO.LOW)
GPIO.setup(heatRelay1, GPIO.LOW)
startTime = datetime.datetime.now()
deltaTime = startTime

def heatOnOff(tempSetPoint, tempWindow):
    pass
    
def motionAction(startTime):
    deltaTime = (datetime.datetime.now()-startTime).total_seconds()
    print("Seconds between motion: {0}".format(deltaTime))
    GPIO.output(statusLedPin, 1)
    if(deltaTime < motionTimeOutSeconds):
        startTime = datetime.datetime.now()
    else:
        GPIO.output(statusLedPin, 0)
        print('No motion in {0} seconds.'.format(deltaTime))          
    return startTime
        
if __name__ == '__main__':
    print('Setting up')
    GPIO.output(statusLedPin, 0)
    while True:
        time.sleep(2)
        motionState = GPIO.input(motionSensorInPin)
        print('Motion state is: {0}'.format(motionState))
        if motionState==1:
            startTime = motionAction(startTime)  
