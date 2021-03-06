'''
Configuration variables for the Flask Web App
FTD 2019-10-16
'''

OnTempAdder= 0.5

# The number of seconds to wait between temperature readings.
# Must be less than 6 for the motion sensor to get reasonable readings
DelayTime= 3
MaxTemp= 30

# Temperature control within +/-
TempWindow= 1.0

#The number of seconds of no motion detected after the set start time to shut the furnace down.
# will want 900 (15 minutes) in prod.  Test much shorter
MotionDelaySeconds= 10

#TempSensorId: /sys/bus/w1/devices/28-04167527baff
TempSensorId = '/sys/bus/w1/devices/28-0118410e8eff'
# TempSensorId: /home/pi/thermal_controller/temp

relay1 = 17
relay2 = 27
relay3 = 22
relay4 = 10
statusLight = 18
motionSensorInPin = 23
