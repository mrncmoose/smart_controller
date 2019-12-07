import json
#from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from Config import *
import logging
import logging.handlers

class baseAWSmqClient:
    
    def __init__(self, base_dir='/Users/moose/Documents/IoT-stuff/AWS/test-pi/client/'):
        self.myAWSIoTMQTTClient = None
        baseDir = base_dir
        self.awsRootCert = baseDir + 'AmazonRootCA1.pem'
        self.awsThingCert = baseDir + 'b3e88e24a4-certificate.pem.crt'
        self.awsThingKey = baseDir + 'b3e88e24a4-private.pem.key'
        self.currentTemp = None
        self.motionTime = None
        self.thermalEvents = None
        self.isThermalEventsAccepted = None

    '''
    AWS IoT message queuing calls
    '''
    def customCallback(self, client, userdata, message):
        try:
            response = json.loads(message.payload)
            if 'current_temp' in response:
                self.currentTemp = '{0} C'.format(response['current_temp'])
            if 'accepted' in response:
                self.isThermalEventsAccepted = response['accepted']
        except Exception as e:
            print('Error on response message: {0}'.format(e))
            raise e
    
    # Function called when a shadow is updated
    def customShadowCallback_Update(self, payload, responseStatus, token):
    
        # Display status and data from update request
        if responseStatus == "timeout":
            print("Update request " + token + " time out!")
    
        if responseStatus == "accepted":
            payloadDict = json.loads(payload)
            print("~~~~~~~~~~~~~~~~~~~~~~~")
            print('Callback_Update JSON: {0}'.format(payload))
            print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    
        if responseStatus == "rejected":
            print("Update request " + token + " rejected!")
    
    # Function called when a shadow is deleted
    def customShadowCallback_Delete(self, payload, responseStatus, token):
    
         # Display status and data from delete request
        if responseStatus == "timeout":
            print("Delete request " + token + " time out!")
    
        if responseStatus == "accepted":
            print("~~~~~~~~~~~~~~~~~~~~~~~")
            print("Delete request with token: " + token + " accepted!")
            print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    
        if responseStatus == "rejected":
            print("Delete request " + token + " rejected!")
        
    def connect(self):
        self.myAWSIoTMQTTClient = AWSIoTMQTTClient('webClient')
        self.myAWSIoTMQTTClient.configureEndpoint(awsEndpoint, awsPort)
        self.myAWSIoTMQTTClient.configureCredentials(self.awsRootCert, self.awsThingKey, self.awsThingCert)
        
        # AWSIoTMQTTClient connection configuration
        self.myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
        self.myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        self.myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
        
        # Connect and subscribe to AWS IoT
        self.myAWSIoTMQTTClient.connect()
        print('Connected to AWS IoT via MQTT')
        self.myAWSIoTMQTTClient.subscribe(awsResponseTopic, 1, self.customCallback)
        print('Subscribed to topic {0}'.format(awsResponseTopic))

    def makeRequest(self, requestItem):
        request = None
        if requestItem == 'temperature':
            request = {'request': 'temperature'}
            self.sendRequest(json.dumps(request))
    
    def sendRequest(self, requestJson):
        self.myAWSIoTMQTTClient.publish(awsRequestTopic, requestJson, 0)
        print('Sent request to topic {0}'.format(awsRequestTopic))