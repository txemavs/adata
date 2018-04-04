''' Example MQTT client
'''

from adata import echo, Module
from adata.mqtt import Broker
   
class Define(Module):

    name = "mqtt_bbc_one"
    menu = "Service"

    def task(self):
        broker = Broker("test.mosquitto.org", 1883)
        broker.app = self.app
        broker.subscribe("bbc/subtitles/bbc_one_london/#")
        
    def menuitem(self):
        return {
            'name': "MQTT Example - BBC1", 
        }

    



