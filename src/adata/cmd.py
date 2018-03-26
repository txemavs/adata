# adata.cmd

'''
Interactive Interpreter

.. seealso:: `cmd2 <https://cmd2.readthedocs.io/en/latest/unfreefeatures.html>`_



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
    __doc__ = code.InteractiveInterpreter.__doc__
    
    def write(self, text):
        '''Adata override: pubsub event send.
        
        :parameters:
            `text` : string
                Output.
        '''
        echo(text)
                     



class Commands(Cmd):
    '''Adata interactive interpreter: execute command, script or code.
    
    '''
    
    __script = {}
    __module = {}
    stdout = Output()
    default_to_shell = False

 
    def __init__(self, app):
        '''Create a cmd2 interpreter.

        :parameters:
            `app` : ``adata.core.Application``
                The main application.
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
        '''Adata override of cmd2.Cmd.poutput method: print to console.
            
        '''
        #poutput-pfeedback-perror-ppaged

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
        '''Attach a interactive input handler to a Console instance.

        Try:
         - 1. first word is cmd2: This interpreter - see help 
         - 2. first word is a script: run the module
         - 3. code: code.InteractiveInterpreter: python
        
        :parameters:
            `console` : ``adata.gui.text.Console``
                The console.
        
        :return: self
        :rtype: `Commands`
        '''

        def handler(cmd): 
            ''' 
            Console.Enter handler (Commands class overriden)
            
            :parameters:
                `cmd` : string
                    A command line.
            '''

            if cmd=="help()": cmd = "import this" 
            # help() fails at , why?

            # Rules
            if self.is_command(cmd.split(' ')[0]): # Mine
                self.runcmds_plus_hooks(cmd.split('\n'))
                return 

            if cmd in self.iter_scripts(): # Import or reload
                
                if cmd in self.__script.keys():
                    importlib.reload(self.__script[cmd])
                else:
                    module = importlib.import_module(cmd, package=None)
                    self.__script[cmd] = module
                return
            
            # InteractiveInterpreter
            self.code.runsource(cmd) # Are you sure?
                
        console.Enter = handler # Take input method
        return self


    def iter_scripts(self):
        '''List file names in the /scripts folder.
        '''
        for x in os.listdir(self.app.path["scripts"]):
            name = os.path.splitext(x)[0]
            if name[0]=="_": continue
            yield name

     




    # Commands
    # --------
    # https://docs.python.org/3/library/argparse.html#the-add-argument-method

    def is_command(self, keyword):
        ''' Does a do_name method exist?
        
        :return: Attribute exists.
        :rtype: bool
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
            print( '\n'.join( self.iter_scripts() ))
            

    
    def do_module(self, name):
        '''Load or reload a module.

        :parameters:
            `name` : string
                Module name

        :return: Module imported without errors
        :rtype: bool

        '''
        try:        
            if name in self.__module.keys():
                importlib.reload(self.__module[name])
                echo("OK")
            else:
                module = importlib.import_module(name, package=None)
                self.__module[name] = module
                echo("OK")
            return True
        
        except Exception as error:
            echo("%s" % error)
            # Clean module to reload
            return False

# Add original documentation
Commands.__doc__ += Cmd.__doc__      
            
            
            
def visit(url):
    ''' Test web page text - locals() available 
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

def read_file(path, encoding="utf-8"):
    ''' Prints a text file
    '''
    with open(path, "rt", encoding=encoding) as f: 
        print(f.read())


def dir_pretty(var, grep=None):
    ''' Pretty dir command 
    '''
    pretty = PrettyTable([ "__name__", "type", "__doc__"]) 
    pretty.align["__name__"] = "l" 
    pretty.align["type"] = "l" 
    pretty.align["__doc__"] = "l"

    for item in dir(var):     
        if item[0]=="_": continue
        if grep is not None and not grep in item: continue

        obj = getattr(var, item)
        obj_type = type(obj).__name__
        
        if obj.__doc__ is None:
            doc = ""
        else:
            doc = obj.__doc__.split('\n')[0]
        if len(doc)>80:
            doc = doc[0:40]
        pretty.add_row([ "%s" % item, obj_type, doc ])
    echo(var.__doc__, "ffffff")
    echo(pretty.get_string())

