import time
import datetime
from time import sleep, strftime

offTime = datetime.datetime.now() + datetime.timedelta(seconds=30) 
now = datetime.datetime.now()
adjustedOnDate = datetime.datetime.strptime('2019-10-17 21:17:40', "%Y-%m-%d %H:%M:%S")
adjustCheckDate = datetime.datetime.strptime('2019-10-17 22:27:06', "%Y-%m-%d %H:%M:%S")
PreHeatHours = 6
lowerTimeLimit = now - datetime.timedelta(hours=PreHeatHours)
print('Lower time limit:\t{0}'.format(lowerTimeLimit.strftime("%Y-%m-%d %H:%M:%S")))

print('Offtime is:\t{0}'.format(offTime.strftime("%Y-%m-%d %H:%M:%S")))
print('Now is:\t\t{0}'.format(now.strftime("%Y-%m-%d %H:%M:%S")))

# should not hit
if now >= offTime:
    print('now is >= offTime')

#should be same as above
if offTime <= now:
    print('offTime is <= now')

# offTime is 30 seconds in the future, therefore this should hit
if now <= offTime:
    print('now is <= offTime')

# should hit
if adjustedOnDate <= adjustCheckDate:
    print('Turn on!')
    