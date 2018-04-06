''' Example: A Flask / static files / ws server
'''
import os
import wx
import webbrowser
import jinja2
from adata.core import Module
from adata.pubsub import echo, pub, publish
from adata.service import WSGIServer, WebSocketProtocol
from flask import Flask, session, redirect, url_for, escape, request, render_template


PORT = 8080



class Define(Module):
    '''A web remote control
    '''
    name = "flask_ws_example"
    menu = "Service"

    def run(self):
        try:
            templates = os.path.join(self.app.path['data'], 'templates')
            ws = Server(webapp(templates = templates ), Protocol, port=8080 )
        except Exception as error:
            if "WinError 10048" in "%s" % error: #idk better
                echo("Websockets: Port %s is not available" % (PORT), 
                    "ff0000", marker="websocket_server", icon='red_circle')
            else:
                raise error

    def menuitem(self):
        return {
                'name': "Flask web server", 
                'help': "Port %s" % PORT
            }





class Server(WSGIServer):

    def Initialize(self):
        pub.subscribe(self.Broadcast, self.topic+".broadcast")
        pub.subscribe(self.Receive, self.topic)
        echo("pubsub: listening %s" % self.topic, "ff8800")

    def Receive(self, data=None):
        key = data['key']
        number = Protocol.keys.index(key)
        #conn = Protocol.connections[number]

        echo("client.%s: " % number, "FF8800", lf=False, icon="dots")
        echo("%s" % data['data'])






class Protocol(WebSocketProtocol):
    ''' 
    Custom protocol
    Every client has one protocol instance
    
    If a event handler returns true, publish it
    '''
    status = {}


    def status_update(self):
        self.status["clients"]=len(self.connections)
        return self.status

    def OnClientMessage(self, data, isBinary):
        ''' New message event received
        '''        

        number = self.connections.index(self)
        
        echo("client.%s: " % (number), "0088ff", lf=False, icon="blue_arrow")
        echo("%s" % ( data.decode('utf-8')) )

        reply = {
            "conn": number,
            "type":"protocol"
        }
        
        # Update request response for one client
        if data==b'update':
            reply["status"] = self.status_update()
            echo("update: %s" % reply )
            response = Protocol.JSON(reply)
            self.sendMessage(response)
            return

        # Set a status key value pair
        word = data.split(b' ')
        if len(word)>2 and word[0]==b'set':
            key = word[1].decode('utf-8')
            val = word[2].decode('utf-8')
            self.status[ key ] = val
            echo(repr(self.status))
            Protocol.Broadcast({
                "status": self.status_update(),
                "type": "update"
            })
            return
        
        # Else is a chat message
        response = Protocol.JSON(reply)
        self.sendMessage(response)

        
        Protocol.Broadcast({
            "conn": number,
            "msg": data.decode('utf-8'),
            "type": "chat"
        })
    

        # Local
        publish(self.topic, data=response)
        return True





def webapp(templates):
    ''' Create a WSGI Flask app
    '''

    app = Flask("Adata")
    app.secret_key = os.urandom(24)

    #Set custom templates folder
    loader = jinja2.ChoiceLoader([
        jinja2.FileSystemLoader([templates]),
        app.jinja_loader,
    ])
    app.jinja_loader = loader


    @app.route('/')
    def index():
        echo("Request index")
        name = escape(session['username']) if 'username' in session else "?" 
        return render_template('index.html', name=name)


    @app.route('/remote')
    @app.route('/remote/<name>')
    def remote(name=None):
        echo("Request remote")
        title="Adata remote"
        return render_template('remote.html', title = title)


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        return '''
            <form method="post">
                <p><input type=text name=username>
                <p><input type=submit value=Login>
            </form>
        '''


    @app.route('/logout')
    def logout():
        # remove the username from the session if it's there
        session.pop('username', None)
        return redirect(url_for('index'))



    return app



