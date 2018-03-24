# adata.cmd

'''
Interactive Interpreter using CMD2 first

'''
import os
import sys
import code
import pprint
import importlib
import argparse
from .pubsub import *
from cmd2 import Cmd, with_argparser
from prettytable import PrettyTable



def prettydir(var):

    pretty = PrettyTable(["Item", "Doc",  "type"]) 
    pretty.align["Item"] = "l" 
    pretty.align["Doc"] = "l" 
    pretty.align["type"] = "l"

    for item in dir(var):     
        if "__" in item: continue
        obj = getattr(var, item)
        typ = type(obj).__name__

        if obj.__doc__ is None:
            doc = ""
        else:
            doc = obj.__doc__.split('\n')[0]
        if len(doc)>40:
            doc = doc[0:40]
        pretty.add_row(["%s" % item,  doc , typ ])
    echo(var.__doc__, "ffffff")
    echo(pretty.get_string())






class Interpreter(code.InteractiveInterpreter):
    def write(self, data):
        echo(data)


 
#  .o88b. .88b  d88. d8888b. 
# d8P  Y8 88'YbdP`88 88  `8D 
# 8P      88  88  88 88   88 
# 8b      88  88  88 88   88 
# Y8b  d8 88  88  88 88  .8D 
#  `Y88P' YP  YP  YP Y8888D' 
                            
                           


#https://cmd2.readthedocs.io/en/latest/unfreefeatures.html#poutput-pfeedback-perror-ppaged

class Commands(Cmd):
    """ Example cmd2 application. 
    """

    default_to_shell = False
    __script = {}
    __module = {}
    stdout = Output()

    def is_command(self, name):
        return ('do_' + name) in dir(self)
          
    def __init__(self, app):

        self.app = app
        
        self.multilineCommands = ['orate']
        self.maxrepeats = 3
        
        # Add stuff to settable and shortcuts before calling base class initializer
        self.settable['maxrepeats'] = 'max repetitions for speak command'
        self.shortcuts.update({'&': 'speak'})
        env = {
            'app': app,
            'pretty': pprint.PrettyPrinter(indent=4),
            '__doc__': 'Adata Command Interpreter',
            '__name__':'__console__'
        }
        self.code = Interpreter( locals= dict(globals(), **env) )
        Cmd.__init__(self, use_ipython=True)


    def DirScripts(self):
        return [ os.path.splitext(x)[0] for x in os.listdir(self.app.path["scripts"]) ]


    def Prompt(self, console):
        ''' Attach a interactive input handler
        '''
        def handler(cmd): 
            if self.is_command(cmd.split(' ')[0]):
                self.runcmds_plus_hooks(cmd.split('\n'))
                return

            if cmd in self.DirScripts():
                
                if cmd in self.__script.keys():
                    importlib.reload(self.__script[cmd])
                else:
                    module = importlib.import_module(cmd, package=None)
                    self.__script[cmd] = module
                return
             
            self.code.runsource(cmd)
                
        console.Enter = handler


    def do_dir(self, source):
       
        if source=="":
            scripts = self.DirScripts()
            print(scripts)
        else:
            self.code.runsource('prettydir(%s)' % source )






        

    def do_module(self, name):
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


    def poutput(self, msg, end='\n'):
        """Convenient shortcut for self.stdout.write(); by default adds newline to end if not already present.
        Also handles BrokenPipeError exceptions for when a commands's output has been piped to another process and
        that process terminates before the cmd2 command is finished executing.
        :param msg: str - message to print to current stdout - anything convertible to a str with '{}'.format() is OK
        :param end: str - string appended after the end of the message if not already present, default a newline
        """
        if msg is not None and msg != '':
            try:
                msg_str = '{}'.format(msg)
                first=True
                for line in msg_str.split('\n'):
                    echo(line, 
                        color="ffffff", 
                        marker="cmd_last" if first else None, 
                        icon='blue_arrow' if first else 'dots'
                    )
                    first=False
                #if not msg_str.endswith(end): echo(end)
            except IOError:
                # This occurs if a command's output is being piped to another process and that process closes before the
                # command is finished. If you would like your application to print a warning message, then set the
                # broken_pipe_warning attribute to the message you want printed.
                if self.broken_pipe_warning:
                    sys.stderr.write(self.broken_pipe_warning)



    speak_parser = argparse.ArgumentParser()
    speak_parser.add_argument('-p', '--piglatin', action='store_true', help='atinLay')
    speak_parser.add_argument('-s', '--shout', action='store_true', help='N00B EMULATION MODE')
    speak_parser.add_argument('-r', '--repeat', type=int, help='output [n] times')
    speak_parser.add_argument('words', nargs='+', help='words to say')
    @with_argparser(speak_parser)
    def do_speak(self, args):
        """Repeats what you tell me to."""
        words = []
        for word in args.words:
            if args.piglatin:
                word = '%s%say' % (word[1:], word[0])
            if args.shout:
                word = word.upper()
            words.append(word)
        repetitions = args.repeat or 1
        for i in range(min(repetitions, self.maxrepeats)):
            # .poutput handles newlines, and accommodates output redirection too
            self.poutput(' '.join(words))

    do_say = do_speak  # now "say" is a synonym for "speak"
    do_orate = do_speak  # another synonym, but this one takes multi-line input




