'''
Autorun Module
--------------

Load all modules and execute boot sequence.

'''

import os
import wx
import adata
from adata import echo, publish
from adata.mqtt import Broker
from adata.cmd import argparse, with_argparser
       
class Command(adata.Commands):

    __doc__ = adata.Commands.__doc__
    

    def do_stop(self, e):
        publish("app.stop")

    
    mqtt_parser = argparse.ArgumentParser( description='Send MQTT message', add_help=False )
    mqtt_parser.add_argument('-h', '--host',  help='Broker' ) 
    mqtt_parser.add_argument('-t', '--topic',  help='Topic' ) 
    mqtt_parser.add_argument('-p', '--port',  nargs='?', default=1883, help='port number' )
    mqtt_parser.add_argument('message', help='payload' )
    @with_argparser( mqtt_parser )
    def do_mqtt(self, args ):
        '''Send MQTT message
        '''
        broker = Broker(args.host, args.port)
        broker.publish(args.topic, args.message)



class Define(adata.Module):

    def run(self):

        app = self.app
        #echo("Autorun: Loading", marker="autorun", icon='blue_arrow')

        # Create a interpreter and bind console input to it
        app.cmd = Command(app).Prompt(app.win.console)

        
        self.menuitems([
            ("File", [
                {          
                    'name': "Open", 
                    'call': app.run_explorer(app.system["FILES"]), 
                    'icon': "folder_explore.png", 
                },
            ])
        ])

        # Search custom modules app.Run()
        
        #app.load_module("flask_server")
        app.load_module("plugin.mqtt_subscription")
        app.load_module("plugin.flask_ws_server")
        app.load_module("plugin.flask_ws_client")
        
        try:
            app.run_module( "__load__" )(app)

        except ModuleNotFoundError:
            echo("No custom module loader.")
            pass


        self.menuitems([
            ("File", [
                {
                    'name': "", 
                },{
                    'name': "Exit", 
                    'call': app.win.OnExit, 
                }
            ]),
            ("Tools",[
                {          
                    'name': "Configuration File", 
                    'call': app.run_file(app.path["config"]), 
                    'icon': "book.png", 
                },{          
                    'name': "User data folder", 
                    'call': app.run_explorer(app.path["user"]), 
                    'icon': "folder_explore.png", 
                },
            ]),
            ("Help",[
                {          
                    'name': "Documentation", 
                    'call': app.Documentation, 
                    'icon': "help.png", 
                },{
                    'name': "About Adata...", 
                    'call': app.About, 
                    'help': "Automation Framework"
                }
            ])
        ])

       
        


