import json
import datetime
import requests
from requests.auth import HTTPBasicAuth
import ssl
import jwt
import time
import paho.mqtt.client as mqtt
import logging
import re
from Config import *

'''
A class to enable a bridge between MQTT topics hosted in GCP core IoT and a REST API hosted elsewhere

Fred T. Dunaway
2020-01-08
'''
class GCP_Bridge():
       
    def __init__(self, *args, **kwargs):       
        self.blogger = logging.getLogger(__name__)
        self.mqttHost = host
        self.mqttPort = port
        self.QoS = QoS
        self.keyDir = certDir
        self.localUser = localApiUser
        self.localPass = localApiPass
        self.projectId = project_id
        self.cloudRegion = cloud_region
        self.registryId = registry_id
        self.gatewayId = gateway_id
        self.deviceId = device_id
        self.tempertureURI = tempertureURI
        self.eventURI = eventURI
        self.runningURI = runningURI
                
        self.privateKeyFile = self.keyDir + '/rsa_private.pem'
        self.caCert = self.keyDir + '/roots.pem'
        self.algorithm = 'RS256'        
        self.configTopic = '/devices/{}/config'.format(self.deviceId)
        self.commandTopic = '/devices/{}/commands/#'.format(self.deviceId)
        self.eventTopic = '/devices/{}/events'.format(self.deviceId)
        self.jwtTime = datetime.datetime.utcnow()
        self.blogger.debug('JWT creation time: {}'.format(self.jwtTime))
        self.mqttc = self.mqttConnect()
        self.messageToPublish = None

    def mqttConnect(self):
        """Create our MQTT client. The client_id is a unique string that identifies
            this device. For Google Cloud IoT Core, it must be in the format below."""
        clientId = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(self.projectId, 
                                                                               self.cloudRegion, 
                                                                               self.registryId, 
                                                                               self.deviceId)
        mqttc = mqtt.Client(client_id = clientId)
        
        # With Google Cloud IoT Core, the username field is ignored, and the
        # password field is used to transmit a JWT to authorize the device.
        mqttc.username_pw_set(
                username='unused',
                password=self.create_jwt())

        # Enable SSL/TLS support.
        mqttc.tls_set(ca_certs=self.caCert, tls_version=ssl.PROTOCOL_TLSv1_2)    
        self.blogger.info('Starting connection to: {0}:{1}'.format(self.mqttHost, self.mqttPort))
        mqttc.on_connect = self.connectCallBack
        mqttc.on_message = self.processMessage
        mqttc.on_publish = self.publishedMessageCallBack
        mqttc.connect(self.mqttHost, port=self.mqttPort, keepalive=60)
        try:
            mqttc.subscribe(self.configTopic, qos=self.QoS)
            self.blogger.debug('Subscribed to config topic: {}'.format(self.configTopic))
            mqttc.subscribe(self.commandTopic, qos=self.QoS)
            self.blogger.debug('Subscribed to command topic: {}'.format(self.commandTopic))
            mqttc.subscribe(self.eventTopic, qos=self.QoS)
            self.blogger.debug('Subscribed to event topic: {}'.format(self.eventTopic))
            self.messageToPublish = '{"thingy":"ready"}'
#            self.publishMessage(self.eventTopic, QoS)
        except Exception as e:
            self.blogger.error('subscription failed for reason: {0}'.format(e))

        return mqttc
            
    def create_jwt(self):
        """Creates a JWT (https://jwt.io) to establish an MQTT connection.
            Returns:
                A JWT generated from the given project_id and private key, which
                expires in 20 minutes. After 20 minutes, your client will be
                disconnected, and a new JWT will have to be generated.
            Raises:
                ValueError: If the private_key_file does not contain a known key.
            """
    
        token = {
                # The time that the token was issued at
                'iat': datetime.datetime.utcnow(),
                # The time the token expires.
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=19),
                # The audience field should always be set to the GCP project id.
                'aud': self.projectId
        }
    
        # Read the private key file.
        with open(self.privateKeyFile, 'r') as f:
            private_key = f.read()
        return jwt.encode(token, private_key, algorithm=self.algorithm)

    def publishMessage(self, topic, QoS=0):
        client = self.mqttConnect
        mqInfo = client.publish(topic, self.messageToPublish, qos=QoS)
        if mqInfo.is_published():
            self.blogger.debug('publish returned rc: {0}'.format(mqInfo.rc))
            self.messageToPublish = None
        else:
            print('Failed to publish message!')
            
    def processMessage(self, client, userdata, msg):
        if msg is not None:
            req = str(msg.payload.decode('utf-8'))
            self.blogger.debug('Message received: {0}'.format(req))
            try:
                action = json.loads(req.strip())
                if action['ActionRequests']['actionType']['verb']:
                    if action['ActionRequests']['actionType']['verb'] == 'heat':
                        onTime = str(action['actionValue']['on'])
                        onTemp = action['actionValue']['temp']
                        mds = action['actionValue']['motion_delay_seconds']
                        events = [{
                            'on':
                            {
                                'when': onTime,
                                 'temperature': onTemp,
                                 'motion_delay_seconds': mds
                             },
                             'off':{
                                'when':u'2999-03-12 18:00',
                                 'temperature':-42
                             },
                         }]
                        msg = json.dumps(events)
                        self.blogger.debug('JSON request to controller: {0}'.format(msg))
                        self.sendEvent(msg)
                            
                    if action['ActionRequests']['actionType']['verb'] == 'read':
                        sensor = action['ActionRequests']['actionType']['adjective']
                        val = self.getSensorReading(sensor)
                        self.publishMessaage(self.mqttc, val, self.eventTopic)                    
                else:
                    self.blogger.error('No action request in message?\n {}'.format(reg))
            except Exception as e:
                self.blogger.error('Error {0}\n attempting to process JSON message: \n{1}'.format(e, req))                     
        else:
            self.blogger.info('Empty message received.')
    
    def publishedMessageCallBack(self, client, data, mid):
        self.blogger.debug('Published message id {0}'.format(mid))
            
    def connectCallBack(self, client, userdata, flags, rc):
        self.blogger.debug('Connect call back function called.')
    
    #TODO:  Check the sensor for what type of sensor and format the URL accordingly.
    #Currently hard coded to read temperature sensor.
    def getSensorReading(self, sensor):
        url = baseURL + tempertureURI
        res = requests.get(url, auth=HTTPBasicAuth(self.localUser, self.localPass), verify=True)
        if re.search(r'4\d+', str(res.status_code)):
            raise Exception('Unable to get sensor reading with HTTP return code of {}'.format(res.status_code))
        reading = res.json()
        self.blogger.debug('Sensor reading: {}'.format(reading))
        self.publishMessage(self.eventTopic, reading, 1)

    def sendEvent(self, event):
        try:
            url = baseURL + eventURI
            if isinstance(event, dict):
                event = json.dumps(event)
            if not isinstance(event, str):
                raise TypeError('Event is not of type string, but of type {0}'.format(type(event)))         
            resp = requests.post(url, json=event, auth=HTTPBasicAuth(self.localUser, self.localPass), verify=True)
            if re.search(r'4\d+', str(resp.status_code)):
                raise Exception('Unable to send event.  HTTP return code: {}'.format(resp.status_code))
            return True
        except Exception as e:
            self.blogger.error('Unable to send event for reason: {}'.format(e))
            
        return False
    
    def run(self, loopDelay=5):
        while True:
            time.sleep(loopDelay)
            if datetime.datetime.utcnow() >= self.jwtTime + datetime.timedelta(minutes=10):
                self.mqttc = self.mqttConnect()
                
            self.mqttc.loop()

        