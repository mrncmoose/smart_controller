import logging
import requests
import os
import time
import re
import json
import datetime

from requests.auth import HTTPBasicAuth

from Config import *


def getEvents():
    try:
        url = centralServer['baseURL'] + centralServer['eventURI']
        res = requests.get(url, auth=HTTPBasicAuth('Marie', 'Mo%902ose'), verify=True)
        if re.search(r'4\d+|5\d+', str(res.status_code)):
            raise Exception('Unable to get events from central server with HTTP return code of {}'.format(res.status_code))
        events = res.json()
        logging.info('Got events from central server: {}'.format(events))
        if len(events) > 0:
            url = baseURL + eventURI
            localEvents = []
            for ev in events:
                evDateTime = datetime.datetime.strptime(ev['on_when'], "%Y-%m-%dT%H:%M:%SZ")
                if evDateTime >= datetime.datetime.now():
                    lEv = {'on':{
                              'motion_delay_seconds':ev['on_motion_delay_seconds'],
                              'when': ev['on_when'],
                              'temperature': ev['on_temperature']                              
                              },
                             'off': {'temperature': ev['off_temperature']}
                        }
                else:
                    lEv = {'on':{
                              'motion_delay_seconds':ev['on_motion_delay_seconds'],
                              'when': ev['on_when'],
                              'temperature': -42.0                             
                              },
                             'off': {'temperature': ev['off_temperature']}
                        }                        
                localEvents.append(lEv)
            jsonMess = json.dumps(localEvents)
        else:
            logging.info('No events fetched from central server at URL: {}'.format(url))
    except Exception as e:
        logging.error('Unable to send event for reason: {}'.format(e))
        
    return False

getEvents()
