'''
MQTT Client

Machine Queue Telemetry Transport
'''

import sys
import time
import paho.mqtt.client as mqtt
from .pubsub import pub, echo


class Broker(object):
    ''' A MQTT broker connection
    '''
    def __init__(self, host, port=1883):
        '''
        '''
        self.host = host
        self.port = port
        self.client = mqtt.Client()

    def auth(self, user, password):
        ''' Set credentials.

        :param user: user
        :type user: string
        
        :param password: password
        :type password: string

        '''
        self.client.username_pw_set(user, password)


    def connect(self, on_connect=None, on_message=None):

        def on_disconnect(client, userdata, rc):
            if rc != 0: print("Error: %s" % rc)

        self.client.on_disconnect = on_disconnect

        if on_connect: self.client.on_connect = on_connect
        if on_message: self.client.on_message = on_message

        self.client.connect(self.host, self.port, 60)
        
        
    def subscribe(self, topic="#"):


        def on_connect(client, userdata, flags, rc):
            
            if rc==0:
                echo("Connected to %s:%s/%s\n" % (self.host, self.port, topic), "00FF00")
            else:
                echo("Error %s" % rc)
            self.client.subscribe(topic)


        def on_message(client, userdata, msg):
            
            try:
                echo("%s: " % msg.topic, "FFFF00", lf=False)
                echo("%s" % msg.payload)
                #print("%s %s" % (msg.topic, repr()))
            except Exception as e:
                echo("Error: %s" % e)
        
        echo("Connecting to MQTT server...", "88aaff")
        self.connect(on_connect, on_message)
        pub.subscribe(self.StopHandler, "app.stop")
        self.client.loop_start()
        self.running = True
        while self.running:
            time.sleep(1)

        echo("Disconnecting from MQTT server...", "FF0000")
        self.client.loop_stop()
        self.client.disconnect() 
        echo("Disconnected")

    def StopHandler(self):
        self.running = False

    
    def publish(self, topic, payload):

        def on_connect(client, userdata, flags, rc):
            if rc!=0:
                print("Error %s" % rc)
                sys.exit(rc)
            client.publish(topic, payload=payload)
            self.sent = True

        self.sent = False
        self.connect(on_connect)
        while not self.sent: self.client.loop()
        self.client.disconnect()

