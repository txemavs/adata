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

    :param host: IP or DNS name of the broker.
    :type host: string 
    :param port: Optional port - default 8080
    :type port: int 
    '''


    def __init__(self, host, port=1883):
        '''
        '''
        self.host = host
        self.port = port
        self.client = mqtt.Client()




    def auth(self, user, password):
        '''Set credentials before connect.

        :param user: user
        :type user: string
        :param password: password
        :type password: string
        '''
        self.client.username_pw_set(user, password)




    def connect(self, on_connect=None, on_message=None):
        '''Connect to the service.

        :param on_connect: connection handler
        :type on_connect: function
        :param on_message: message handler
        :type on_message: function
        
        '''
        def on_disconnect(client, userdata, rc):
            if rc != 0: print("Error: %s" % rc)

        self.client.on_disconnect = on_disconnect

        if on_connect: self.client.on_connect = on_connect
        if on_message: self.client.on_message = on_message

        self.client.connect(self.host, self.port, 60)

        

        
    def publish(self, topic, payload):
        '''Send one MQTT message.
        '''
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




    def subscribe(self, topic="#"):
        '''Subscribe to a topic and echo received messages.

        Blocks this thread until app.stop signal to disconnect.
        '''

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
        ''' Stop any running loop.
        '''
        self.running = False

    
