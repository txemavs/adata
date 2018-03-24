''' Publish a MQTT message 
'''
import wx
from adata.mqtt import Broker

broker = Broker("test.mosquitto.org", 1883)
broker.app = wx.GetApp()

#broker.subscribe("adata/testing/#")
broker.publish("adata/testing", "TEST 1")
