'''Objectives:
* Connect to GCP pub-sub for IoT Core
* Subscribe to a topic
* Publish events to a topic

Fred T. Dunaway
Jan 3, 2020

Source:  https://cloud.google.com/iot/docs/how-tos/mqtt-bridge
'''
import ssl
import jwt
import datetime
import time
import paho.mqtt.client as mqtt

# Variables that should be move to a configuration...
host = 'mqtt.googleapis.com'
port = 8883
QoS = 0
project_id = 'iotsmartcontroller'
cloud_region = 'us-central1'
registry_id = 'TestMooseIoTRegistry'
gateway_id = 'MooseIoTGateway'
device_id = 'led-light'
#device_id = 'smart-tstat-test'
certDir = 'certs'
privateKeyFile = certDir + '/rsa_private.pem'
ca_certs = certDir + '/roots.pem'
algorithm = 'RS256'
isConnected = False

defaultTopic ='projects/iotsmartcontroller/topics/default'

configTopic = '/devices/{}/config'.format(device_id)
commandTopic = '/devices/{}/commands/#'.format(device_id)
commandPublishTopic = '/devices/{}/commands/'.format(device_id)
eventTopic = '/devices/{}/events'.format(device_id)

def create_jwt(project_id, private_key_file, algorithm):
    """Creates a JWT (https://jwt.io) to establish an MQTT connection.
        Args:
         project_id: The cloud project ID this device belongs to
         private_key_file: A path to a file containing either an RSA256 or
                 ES256 private key.
         algorithm: The encryption algorithm to use. Either 'RS256' or 'ES256'
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
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            # The audience field should always be set to the GCP project id.
            'aud': project_id
    }

    # Read the private key file.
    with open(private_key_file, 'r') as f:
        private_key = f.read()

    print('Creating JWT using {} from private key file {}'.format(
            algorithm, private_key_file))

    x = jwt.encode(token, private_key, algorithm=algorithm)
    #print("Generated, encoded jwt: {}".format(x))
    return x

def publishMessage(client, data, topic, qos=0):
#    if not isConnected:
#         print('Not currently connected.  Trying again in 1 second')
#         client.connect(host, port=port, keepalive=60)
#         time.sleep(1)        
#         #publishMessage(client=client, data=data, topic=topic, qos=qos)
#         print('Attempting to publish message anyway.  Client may not be connected.')
        
    mqInfo = client.publish(topic, data, qos=qos)
    if mqInfo.is_published():
        print('publish returned rc: {0}'.format(mqInfo.rc))
        isConnected = True
    else:
        print('Failed to publish message with reason code: {0}'.format(mqInfo.rc))

def publishedMessageCallBack(client, data, mid):
    print('Published message {0}\n with id {1}'.format(data, mid))
        
def connectCallBack(client, userdata, flags, rc):
    print('Connection made with result code: {}'.format(str(rc)))
    try:
        client.subscribe(configTopic, qos=0)
        print('Subscribed to config topic')
        client.subscribe(commandTopic, qos=0)
        print('Subscribed to command topic: {0}'.format(commandTopic))
#         client.subscribe(eventTopic, qos=0)
#         print('Subscribed to event topic: {0}'.format(eventTopic))
        isConnected = True
    except Exception as e:
        print('subscription failed for reason: {0}'.format(e))

def processMessage(client, userdata, msg):
    if msg is not None:
        print('Message received: {0}'.format(str(msg.payload.decode('utf-8'))))
        msg.ack()
    else:
        print('Empty message received.')
        
def onDisconnectCallBack(client, userdata, flags, rc):
    isConnected = False
    print('Disconnected from broker')
    
"""Create our MQTT client. The client_id is a unique string that identifies
    this device. For Google Cloud IoT Core, it must be in the format below."""
client_id = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(project_id, cloud_region, registry_id, device_id)
mqttc = mqtt.Client(client_id = client_id)

# print('Device client_id is \'{}\''.format(client_id))
# With Google Cloud IoT Core, the username field is ignored, and the
# password field is used to transmit a JWT to authorize the device.
mqttc.username_pw_set(
        username='unused',
        password=create_jwt(
                project_id, privateKeyFile, algorithm))

# Enable SSL/TLS support.
mqttc.tls_set(ca_certs=ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)
    
print('Starting connection to: {0}:{1}'.format(host, port))
mqttc.on_connect = connectCallBack
mqttc.on_message = processMessage
mqttc.on_publish = publishedMessageCallBack
mqttc.connect(host, port=port, keepalive=60)
mqttc.on_disconnect= onDisconnectCallBack

# topic = eventTopic
# publishMessage(mqttc, '{"temp":42}', topic, 1)
# time.sleep(1)
# publishMessage(mqttc, '{"temp":43}', topic, 0)

if not mqttc.is_connected():
    print('Not connected yet?')
    time.sleep(5)
# Send request for current temperature
tempRequestMessage = '{"temperature": 24}'
for i in range(0, 100):
    time.sleep(10)
    publishMessage(mqttc, tempRequestMessage, eventTopic, 0)

# print('Published temperature message to topic {}.'.format(client_id))
# time.sleep(10)
#mqttc.loop()
mqttc.loop_forever()
