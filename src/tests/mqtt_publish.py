import wx
from adata.mqtt import Broker

    

broker = Broker("test.mosquitto.org", 1883)
broker.app = wx.GetApp()

#broker.subscribe("bbc/subtitles/bbc_one_london/#")
broker.publish("adata/testing", "TEST 1")