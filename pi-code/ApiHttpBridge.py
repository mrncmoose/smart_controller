# TODO:  Date time values are way off.  Time zone issue?
# Convert everything to use aware date time.
import logging
import requests
import os
import time
import re
import json
import datetime
from requests.auth import HTTPBasicAuth

from Config import *

class HttpBridge(object):
    
    def __init__(self, *args, **kwargs):       
        self.blogger = logging.getLogger(__name__)
        self.currentTemp = -42.0
        self.isMotion = False
        self.isFurnanceOn = False
        
    def getIsMotion(self):
        res = None
        try:
            url = baseURL + motionURI
            res = requests.get(url, auth=HTTPBasicAuth(localApiUser, localApiPass), verify=True)
            if re.search(r'4\d+|5\d+', str(res.status_code)):
                raise Exception('Unable to get motion from controller with HTTP return code of {}'.format(res.status_code))
            reading = res.json()
            self.isMotion = reading['isMotion']
        except Exception as e:
            self.blogger.error('Unable to get reading from local controller for reason: {}'.format(e))
            return False        
        return True
    
    def getIsFurnanceOn(self):
        res = None
        try:
            url = baseURL + runningURI
            res = requests.get(url, auth=HTTPBasicAuth(localApiUser, localApiPass), verify=True)
            if re.search(r'4\d+|5\d+', str(res.status_code)):
                raise Exception('Unable to get furnance running from controller with HTTP return code of {}'.format(res.status_code))
            reading = res.json()
            self.isFurnanceOn = reading['isFurnanceOn']
        except Exception as e:
            self.blogger.error('Unable to get reading from local controller for reason: {}'.format(e))
            return False        
        return True               
    
    def getTemperature(self):
        url = baseURL + tempertureURI
        try:
            res = requests.get(url, auth=HTTPBasicAuth(localApiUser, localApiPass), verify=True)
            if re.search(r'4\d+|5\d+', str(res.status_code)):
                raise Exception('Unable to get temperature from controller with HTTP return code of {}'.format(res.status_code))        
            reading = res.json()
            self.currentTemp = reading['current_temp']
            return self.currentTemp
        except Exception as e:
            self.blogger.error('Unable to get tempature reading from local controller for reason: {}'.format(e))
        return -42.0
    
    def putReadings(self):
        res = None
        try:
            temp = self.getTemperature()
            motion = self.getIsMotion()
            isHeating = self.getIsFurnanceOn()
        except Exception as e:
            self.blogger.error('Unable to get readings from local controller for reason: {}'.format(e))
            return False
        try:
            url = centralServer['baseURL'] + centralServer['currentReadingURI']
            d = datetime.datetime.now()
            thingOwner = os.environ['THING_OWNER']
            thingPass = os.environ['THING_PASSWORD']
            reading =[
                        {
                            'ttReadTime': '{}'.format(d.strftime('%Y-%m-%dT%H:%M:%S')),
                            'sensorType': sensorTypes['temperature'],
                            'dataValue': '{}'.format(temp),
                            'thing': ourThingId
                        },
                        {
                            'ttReadTime': '{}'.format(d.strftime('%Y-%m-%dT%H:%M:%S')),
                            'sensorType': sensorTypes['motion'],
                            'dataValue': '{}'.format(motion),
                            'thing': ourThingId                            
                        },
                        {
                            'ttReadTime': '{}'.format(d.strftime('%Y-%m-%dT%H:%M:%S')),
                            'sensorType': sensorTypes['furnance'],
                            'dataValue': '{}'.format(isHeating),
                            'thing': ourThingId                                 
                        }
            ]
            mes = json.dumps(reading)
            res = requests.post(url, json=reading, auth=HTTPBasicAuth(thingOwner, thingPass), verify=True)
            self.blogger.debug('Post current reading status code: {0}\n for message: {1}\nTo URL: {2}'.format(res.status_code, mes, url))
            if re.search(r'4\d+|5\d+', str(res.status_code)):
                raise Exception('Unable to send data to central server with HTTP return code of {}'.format(res.status_code))

        except Exception as e:
            self.blogger.error('Unable to put readings to central server for reason: {}'.format(e))
            return False
        self.blogger.debug('Successfully posted device reading to central server.') 
        return True
    
    def getEvents(self):
        try:
            url = centralServer['baseURL'] + centralServer['eventURI']
            isEventInPast = False
            res = requests.get(url, auth=HTTPBasicAuth(os.environ['THING_OWNER'], os.environ['THING_PASSWORD']), verify=True)
            if re.search(r'4\d+|5\d+', str(res.status_code)):
                raise Exception('Unable to get events from central server with HTTP return code of {}'.format(res.status_code))
            events = res.json()
            self.blogger.debug('Got events from central server: {}'.format(events))
            if len(events) > 0:
                url = baseURL + eventURI
                localEvents = []
                for ev in events:
                    now = datetime.datetime.now()
                    setDate = datetime.datetime.strptime(ev['on_when'], "%Y-%m-%dT%H:%M:%S")
                    if setDate >= now:
                        lEv = {'on':{
                                  'motion_delay_seconds':ev['on_motion_delay_seconds'],
                                  'when': ev['on_when'],
                                  'temperature': ev['on_temperature']                              
                                  },
                                 'off': {'temperature': ev['off_temperature']}
                            }
                        localEvents.append(lEv)
                    else:
                        self.blogger.warn('Set point datetime is in the past.  Current date: {}\tSetpoint date: {}'.format(now, setDate))
                        isEventInPast = True
                if not isEventInPast:
                    jsonMess = json.dumps(localEvents)
                    resp = requests.post(url, json=jsonMess, auth=HTTPBasicAuth(localApiUser, localApiPass), verify=True)
                    if re.search(r'4\d+|5\d+', str(resp.status_code)):
                        raise Exception('Unable to send event to local server.  HTTP return code: {}'.format(resp.status_code))
                return True
            else:
                self.blogger.debug('No events fetched from central server at URL: {}'.format(url))
        except Exception as e:
            self.blogger.error('Unable to send event for reason: {}'.format(e))
            
        return False
            
    def run(self, loopDelay=600):
        while True:
            time.sleep(loopDelay)
            self.getEvents()
            self.putReadings()
            