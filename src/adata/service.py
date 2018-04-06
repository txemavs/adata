# adata.service

''' Basic servers

    Define the protocol over WebSocketProtocol, 

    Create a Server with a protocol factory

'''
import wx
import os
import sys
import json
from twisted.python import log
from twisted.internet import reactor
from twisted.web.static import File
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.web.wsgi import WSGIResource
from autobahn.twisted import websocket, resource

from adata import echo, publish



class WSGIRoot( Resource ):
    ''' Fallback root to Flask
    '''
    WSGI = None
    
    def getChild( self, child, request ):
        request.prepath.pop()
        request.postpath.insert(0,child)
        return self.WSGI
    
    def render( self, request ):
        return self.WSGI.render( request )




PORT = 8080




#  db   d8b   db d88888b d8888b. .d8888.  .d88b.   .o88b. db   dD d88888b d888888b 
#  88   I8I   88 88'     88  `8D 88'  YP .8P  Y8. d8P  Y8 88 ,8P' 88'     `~~88~~' 
#  88   I8I   88 88ooooo 88oooY' `8bo.   88    88 8P      88,8P   88ooooo    88    
#  Y8   I8I   88 88~~~~~ 88~~~b.   `Y8b. 88    88 8b      88`8b   88~~~~~    88    
#  `8b d8'8b d8' 88.     88   8D db   8D `8b  d8' Y8b  d8 88 `88. 88.        88    
#   `8b8' `8d8'  Y88888P Y8888P' `8888Y'  `Y88P'   `Y88P' YP   YD Y88888P    YP    

                                                                                

class WebSocketProtocol(websocket.WebSocketServerProtocol):
    ''' One websocket connection, a instance for each connected client
    '''
    topic = "ws.server"
    keys = list()
    clients = dict()
    connections = list()


    @staticmethod
    def JSON(data):
        '''
        :returns: JSON
        :rtype: bytes
        '''
        return json.dumps(data, ensure_ascii = False).encode('utf8')

    @classmethod
    def Broadcast(cls, data):
        ''' Send JSON data to all connected clients
        '''
        payload = WebSocketProtocol.JSON(data)
        #data["type"] = "broadcast"
        clients = set(cls.connections)
        #echo("WebSockets: Broadcast for {} clients = {}".format(len(clients), payload))
        for conn in clients:
            reactor.callFromThread(cls.sendMessage, conn, payload)


    def GetKey(self):
        return self.keys[self.connections.index(self)]

    def GetIP(self):
        return self.clients[self.GetKey()].origin


    def OnClientConnects(self, request): 
        '''Pub if Hook returns true '''
        return True
    
    def OnClientDisconnects(self, wasClean, code, reason): 
        '''Hook'''
        return True
    
    def OnClientMessage(self, data, isBinary):
        '''Hook '''
        return True
    

    def onConnect(self, request):
        ''' Client connects (override)
        '''
        key = request.headers["sec-websocket-key"]
        self.clients[key] = request
        self.connections.append(self)
        self.keys.append(key)
        
        if self.OnClientConnects(request):
            publish(self.topic+'.conn', data={
                'event': 'onConnect',
                'key': key,
            })



    def onClose(self, wasClean, code, reason):
        ''' Client disconnects (override)
        '''        
        key = self.keys[self.connections.index(self)]
        self.connections.remove(self)
        self.keys.remove(key)
        if self.OnClientDisconnects(wasClean, code, reason):        
            publish(self.topic+'.conn', data={
                'event': 'onClose',
                'key': key,
                'wasClean': wasClean, 
                'code': code, 
                'reason': reason
            })
        del self.clients[key]



    def onMessage(self, data, isBinary):
        ''' Client message (override)
        '''
        key = self.GetKey()
        if self.OnClientMessage( data, isBinary):
            publish('ws.server.msg', data={
                'key': key,
                'data': u'%s' % data
            })    
                




# -----------------------------------------------------------------------------

#  .d8888. d88888b d8888b. db    db d88888b d8888b. 
#  88'  YP 88'     88  `8D 88    88 88'     88  `8D 
#  `8bo.   88ooooo 88oobY' Y8    8P 88ooooo 88oobY' 
#    `Y8b. 88~~~~~ 88`8b   `8b  d8' 88~~~~~ 88`8b   
#  db   8D 88.     88 `88.  `8bd8'  88.     88 `88. 
#  `8888Y' Y88888P 88   YD    YP    Y88888P 88   YD 
                                                 
                                                 


class WebSocketServer(object):
    ''' www server
    '''

    def SetTopic(self, topic):
        self.topic = topic
        self.factory.protocol.topic = topic




    def __init__(self, app, protocol=None, ip=None, port=PORT, path=b"ws", www=None):
        ''' Start protocol factory and reactor
        '''
        #self.io_control()
        
        self.app = app
        self.ip = "127.0.0.1" if ip is None else ip
        self.port = port
        self.url = "ws://%s:%s" % (self.ip, self.port)

        if protocol is None:
            protocol = WebSocketProtocol

        self.root = File(app.path['www'] if www is None else www)

        self.factory = websocket.WebSocketServerFactory(self.url)
        self.factory.protocol = protocol

        self.root.putChild(path, resource.WebSocketResource(self.factory))
        self.site = Site(self.root)

        # Use the existing reactor        
        reactor.listenTCP(self.port, self.site)
        
        self.Initialize()


    def Initialize(self):
        echo("Web Server: Starting at %s" % self.root)
        echo("Websockets Server: Starting at %s" % self.url)


    def Logger(self):
        log.startLogging(sys.stdout)






class WSGIServer(object):
    ''' Creates the WS server
    '''

    def __init__(self, wsgiapp,  wsprotocol, port=PORT):
        ''' Start protocol factory and reactor
        '''
        self.app = wx.GetApp()
        ip = self.app.IP
        self.ip = "127.0.0.1" if ip is None else ip
        self.port = port
        self.url = "ws://%s:%s" % (self.ip, self.port)

        # Set Protocol factory
        self.factory = websocket.WebSocketServerFactory(self.url)
        self.factory.protocol = wsprotocol
       
        self.root = WSGIRoot()
        self.root.WSGI = WSGIResource( 
            reactor, 
            reactor.getThreadPool(), 
            wsgiapp 
        )
        self.root.putChild(b"ws", resource.WebSocketResource(self.factory) )
        
        static = File( os.path.join(self.app.path['www'], 'static') )
        self.root.putChild(b"static", static )
        # Only one File
        #self.root.putChild(b"documentation", File( os.path.join(self.app.path['www'], 'documentation') ) )

        self.site = Site( self.root )

        # Use the existing reactor        
        reactor.listenTCP( self.port, self.site )
        
        echo("Web Server: Starting at %s" % self.root)
        echo("Websockets Server: Starting at %s" % self.url)
        
        topic = "ws.local"
        self.topic = topic
        self.factory.protocol.topic = topic
        self.Initialize()    

    def Initialize(self): pass



    def Broadcast(self, data):
        Protocol.Broadcast(data)




        
def htmlchars(text): 
    return text.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")
# -----------------------------------------------------------------------------

