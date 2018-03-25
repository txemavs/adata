# adata.cmd

'''
Interactive Interpreter

'''
import os
import sys
import code
import pprint
import requests
import html2text
import importlib
import argparse
from .pubsub import *
from lxml import html
from cmd2 import Cmd, with_argparser
from prettytable import PrettyTable



class Interpreter(code.InteractiveInterpreter):
    def write(self, data):
        echo(data)


def visit(url):
    ''' Text web page text - locals() available 
    '''
    source = requests.get(url) #headers=headers
    print(html2text.html2text(source.text))
    print("* Info %s" % url)
    page = html.fromstring(source.text)
    for meta in page.xpath("//meta"):
        name = meta.get("name")
        if name is None:
            name = meta.get("property")
        print(" -- %s -> %s" % (name, meta.get("content")))


def dir_pretty(var, grep=None):
    ''' Pretty dir command 
    '''
    pretty = PrettyTable(["type", "__name__", "__doc__"]) 
    pretty.align["type"] = "l" 
    pretty.align["__name__"] = "l" 
    pretty.align["__doc__"] = "l"

    for item in dir(var):     
        if "__" in item: continue
        if grep is not None and not grep in item: continue

        obj = getattr(var, item)
        typ = type(obj).__name__

        if obj.__doc__ is None:
            doc = ""
        else:
            doc = obj.__doc__.split('\n')[0]
        if len(doc)>80:
            doc = doc[0:40]
        pretty.add_row([ typ, "%s" % item,  doc  ])
    echo(var.__doc__, "ffffff")
    echo(pretty.get_string())








 
#  .o88b. .88b  d88. d8888b. 
# d8P  Y8 88'YbdP`88 88  `8D 
# 8P      88  88  88 88   88 
# 8b      88  88  88 88   88 
# Y8b  d8 88  88  88 88  .8D 
#  `Y88P' YP  YP  YP Y8888D'                           

# https://cmd2.readthedocs.io/en/latest/unfreefeatures.html#poutput-pfeedback-perror-ppaged

class Commands(Cmd):
    ''' Interactive interpreter . 
    '''

    __script = {}
    __module = {}
    stdout = Output()
    default_to_shell = False

 
    def __init__(self, app):
        '''
        A cmd2 interpreter

        :param app: the main app
        :type app: adata.core.Application
        '''
        env = {
            'app': app,
            'pretty': pprint.PrettyPrinter(indent=4),
            '__doc__': 'Adata Command Interpreter',
            '__name__':'__console__'
        }
        self.code = Interpreter( locals= dict(globals(), **env) )
        
        self.app = app
        self.multilineCommands = ['for']

        return Cmd.__init__(self, use_ipython=False)


    def poutput(self, msg, end='\n'):
        ''' Overriden Cmd.poutput direct to console
        '''
        if msg is not None and msg != '':
            try:
                msg_str = '{}'.format(msg)
                first=True
                for line in msg_str.split('\n'):
                    self.app.win.console.echo(line, #or pubsub echo 
                        #color="ffffff", 
                        style="fore:f5f5f5", 
                        marker="cmd_last" if first else None, 
                        icon='blue_arrow' if first else 'dots'
                    )
                    first=False
                #if not msg_str.endswith(end): echo(end)
            except IOError:
                if self.broken_pipe_warning:
                    sys.stderr.write(self.broken_pipe_warning)



    def Prompt(self, console):
        ''' 
        Attach a interactive input handler to a console

        Try:
         - 1. first word is cmd2: This interpreter - see help 
         - 2. first word is a script: run the module
         - 3. code: code.InteractiveInterpreter: python
        
        :param console: the console
        :type console: adata.gui.text.Console

        '''

        def handler(cmd): 
            ''' 
            Console.Enter handler (Commands class overriden)

            :param cmd: command line
            :type cmd: string
            '''

            if cmd=="help()": cmd="import this" 
            # help() fails at , why?

            # Rules
            if self.is_command(cmd.split(' ')[0]): # Mine
                self.runcmds_plus_hooks(cmd.split('\n'))
                return 

            if cmd in self.list_scripts(): # Import or reload
                
                if cmd in self.__script.keys():
                    importlib.reload(self.__script[cmd])
                else:
                    module = importlib.import_module(cmd, package=None)
                    self.__script[cmd] = module
                return
            
            # InteractiveInterpreter
            self.code.runsource(cmd) # Are you sure?
                
        console.Enter = handler # Take input method



    def list_scripts(self):
        ''' List file names in /scripts folder
        '''
        path = self.app.path["scripts"]
        return [ os.path.splitext(x)[0] for x in os.listdir(path) ]
        




    # Commands
    # --------
    # https://docs.python.org/3/library/argparse.html#the-add-argument-method

    def is_command(self, keyword):
        ''' Does a do_name method exist?
        '''
        return ('do_' + keyword) in dir(self)




    dir_parser = argparse.ArgumentParser( description='Attributes table.' )
    dir_parser.add_argument('-f', '--filter',  nargs='?', help='Grep' ) # default='',
    dir_parser.add_argument('something', nargs='?', help='what to inspect' )
    
    @with_argparser( dir_parser )
    def do_dir(self, args ):
        ''' Shows all the attributes
        '''
        #print(args.filter)
        #source = ' '.join(args.something)
        source = args.something

        if args.something:
            self.code.runsource('dir_pretty(%s)' % source )
        else:
            print(self.list_scripts() )
            

    
    def do_module(self, name):
        ''' Load or reload a module.
        '''
        try:        
            if name in self.__module.keys():
                importlib.reload(self.__module[name])
                echo("OK")
            else:
                module = importlib.import_module(name, package=None)
                self.__module[name] = module
                echo("OK")

        except Exception as error:
            echo("%s" % error)
            # Clean module

