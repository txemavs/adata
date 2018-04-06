'''
Simple Websockets and pubsub example

'''

import webbrowser
import adata
from adata import service, echo, pub



class Protocol(service.WebSocketProtocol):
    ''' 
    Custom protocol
    Every client has one protocol instance
    
    If a event handler returns true, publish it
    '''
    def OnClientMessage(self, data, isBinary):
        ''' New message event received
        '''        
        response = Protocol.JSON({
                "msg": "reply",
                "type":"protocol"
            })
        self.sendMessage(response)
        return True





class Listener(object):
    ''' Uses pubsub to propagate events
    '''
    def Subscribe(self, topic):
        pub.subscribe(self.OnConn, topic+".conn")
        pub.subscribe(self.OnMessage, topic+".msg")
        return self

    def OnMessage(self, data=None):

        key = data['key']
        number = Protocol.keys.index(key)
        #conn = Protocol.connections[number]

        echo("client.%s: " % number, "FF8800", lf=False, icon="dots")
        echo("%s" % data['data'])



        
        if type(data)==type(b''):
            Protocol.Broadcast({
                  "data": str(data),
            })

        else:    
            Protocol.Broadcast({
                "data": data,
            })

    def OnConn(self, request=None, data=None):
       
        Protocol.Broadcast({
            "msg":"Connection",
            "data": data,
         #   "peer": request.peer
        })





class Service(service.WebSocketServer):
    ''' Creates the WS server
    '''

    def GetTopic(self):
        return "ws.server"

    def Broadcast(self, data):
        Protocol.Broadcast(data)


    def Initialize(self):
        echo("Web Server: Starting at %s" % self.root)
        echo("Websockets Server: Starting at %s" % self.url)
        self.Logger()
        self.SetTopic(self.GetTopic())
        
        # Keep a reference or it goes away
        self.listener = Listener().Subscribe( self.GetTopic() )
        pub.subscribe(self.Broadcast, self.GetTopic()+".echo")










class Define(adata.Module):
    ''' This module creates an example Websocket Service
    '''
    name = "websocket_server"
    menu = "Service"
    port = 8080

    def run(self):

        try:
            self.app.ws = Service(self.app, protocol=Protocol)
        except Exception as error:
            if "WinError 10048" in "%s" % error: #idk better
                echo("Websockets: Port %s is not available" % (self.port), "ff0000", marker="websocket_server",icon='red_circle')
            else:
                raise error

    def menuitem(self):

        # Add another menuitem before
        self.app.win.AddMenu(self.menu, {
            'name': "Local WebSockets server", 
            'call': self.call(),
        })

        try: 
            ip = self.app.IP
        except: 
            ip = "127.0.0.1"

        return {
            'name': "Local WebSockets client", 
            'call': lambda e: webbrowser.open("http://%s:%s" % (ip, self.port)),
        }

















def WSECHO( text, style="default", lf=True, marker=None, icon=None ):
    Protocol.Broadcast({"text":text})
    

