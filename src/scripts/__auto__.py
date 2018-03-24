'''
Autorun Module
--------------

Load all modules and execute boot sequence.

'''

import os
import wx
import adata
from adata import echo, publish



       
class Command(adata.Commands):

    def do_stop(self, e):
        publish("app.stop")
    




class Define(adata.Module):
    


    def run(self):

        app = self.app

       
        # Create a interpreter and bind console input to it
        app.cmd = Command(app).Prompt(app.win.console)

        #echo("Autorun: Loading", marker="autorun", icon='blue_arrow')

        self.menuitems([
            ("File", [
                {          
                    'name': "New", 
                    'call': app.run_explorer(app.system["FILES"]), 
                    'icon': "folder_explore.png", 
                },
            ])
        ])

        # Search custom modules app.Run()
        app.load_module("plugin.mqtt_channels")
        app.load_module("plugin.websocket_client")
        app.load_module("plugin.websocket_server")
        app.load_module("plugin.mqtt_channels_bbc")

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
                    'name': "About Adata...", 
                    'call': app.OnAbout, 
                    'icon': "help.png", 
                    'help': "Automation Framework"
                }
            ])
        ])

       
        


