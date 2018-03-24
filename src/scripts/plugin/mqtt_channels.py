


from adata import echo, Module
from adata.mqtt import Broker

    
class Define(Module):

    name = "mqtt_channels"
    menu = "Service"

    def task(self):
        #broker = Broker("gps.gglas.com", 1883)
        #broker.auth("glas","jmve")
        broker = ScanTopics("test.mosquitto.org", 1883)
        broker.app = self.app
        broker.subscribe("adata/#")

    def menuitem(self):
        return {
            'name': "Connect MQTT - test.mosquitto.org", 
        }






    

class ScanTopics(Broker):




    def on_message(self, client, userdata, msg):
        try:
            echo("%s: " % msg.topic, "FFFF00", lf=False)
            echo("%s" % msg.payload)
            #print("%s %s" % (msg.topic, repr()))
        except Exception as e:
            echo("Error: %s" % e)

    
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



