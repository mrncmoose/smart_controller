'''
A base class to hold all of the MQTT definitions and setups.
Fred T. Dunaway April 16, 2021
'''
import pika
import time
import logging
from Config import mqttConfig

class MqttBase(object): 
    def __init__(self):
        self.conn = None
        self.channel = None
        self.mqttConnect()
        #Per best practice, define everything in all programs
        for t in mqttConfig['ques']:
            self.channel.queue_declare(queue=mqttConfig['ques'][t]['qName']) 
            self.channel.exchange_declare(exchange=mqttConfig['ques'][t]['exchange'], exchange_type='topic')
            self.channel.queue_bind(exchange=mqttConfig['ques'][t]['exchange'], queue=mqttConfig['ques'][t]['qName'], routing_key=mqttConfig['ques'][t]['routingKey'])
            self.channel.queue_purge(queue=mqttConfig['ques'][t]['qName'])  
                  
    def mqttConnect(self):
        if not self.conn or self.conn.is_closed:
            try:
                credentials = pika.PlainCredentials(mqttConfig['user'], mqttConfig['passWd'])
                self.conn = pika.BlockingConnection(pika.ConnectionParameters(credentials=credentials, 
                    host=mqttConfig['mqttServer'],
                    heartbeat=300,
                    blocked_connection_timeout=300))
                self.channel = self.conn.channel()
                logging.info('Connected to mqtt server')
            except Exception as e:
               logging.error('Unable to connect to mqtt server {} for reason {}!'.format(mqttConfig['mqttServer'], e))

    def getFloatVal(self, val: dict, key):
        if key not in val or val[key] is None:
            return 0.0
        return float(val.get(key, 0.0))
        