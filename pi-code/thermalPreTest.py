from time import sleep
import time
import datetime
from datetime import timedelta
from time import sleep, strftime

motionTimeOutSeconds = 5
lastMotionTime = datetime.datetime.now()

def motionTimedOut():
    myNow = datetime.datetime.now()
    deltaTime = (myNow - lastMotionTime).total_seconds()
    if deltaTime > motionTimeOutSeconds:
        print('Motion timed out after {0} seconds'.format(deltaTime))
        return True
    return False

sleep(2)
# bTime = datetime.datetime.now()
# deltaT = (bTime-lastMotionTime).total_seconds()
# print(deltaT)
if motionTimedOut():
    print('Motion timeout test of 2 seconds failed!')
    exit(-1)
print('No timeout after 2 seconds.')
lastMotionTime = datetime.datetime.now()
sleep(6)
if motionTimedOut():
    print('Motion timeout test is working after 6 seconds')
    