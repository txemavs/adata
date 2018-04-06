
from adata import echo
from twisted.internet import reactor, ssl
from autobahn.twisted.websocket import WebSocketClientProtocol, WebSocketClientFactory, connectWS


class ClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onOpen(self):
        print("WebSocket connection open.")

        def hello():
            echo("sending Hello")
            self.sendMessage(b"Hello, world!")
            self.sendMessage(b"\x00\x01\x03\x04", isBinary=True)
            self.factory.reactor.callLater(3, hello)

        # start sending messages every second ..
        hello()

    def onMessage(self, payload, isBinary):
        if isBinary:
            echo("Binary message received: {0} bytes".format(len(payload)))
        else:
            echo("Text message received: {0}".format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
        echo ("Closed %s %s %s" % (wasClean, code, reason))
        print("WebSocket connection closed: {0}".format(reason))



from adata import Module, echo


    
class Define(Module):

    name = "websocket_client"
    menu = "Service"

    def task(self):
        factory = WebSocketClientFactory("wss://gglas.eu/live/?key=ADATA")
        factory.protocol = ClientProtocol
        contextFactory = ssl.ClientContextFactory() if factory.isSecure else None
        connector = connectWS(factory, contextFactory)

        #factory = WebSocketClientFactory(u"ws://127.0.0.1:8080/ws")
        #factory.protocol = MyClientProtocol
        #reactor.connectTCP("gglas.eu", 443, factory)    


    def menuitem(self):
        return {
            'name': "Connect to WebSockets", 
            'call': self.call(),
        }





   

    