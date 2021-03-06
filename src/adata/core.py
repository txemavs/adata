# adata.core
'''
Helpers and base class for WX applications.

    - Module: a base class to allow scripts to be loaded.
    - Application: a WX App running in a Twisted event loop

'''
import re 
import sys
import locale
import time
import datetime
import socket
import shutil
import threading
import configparser
import importlib
import traceback
import twisted
import subprocess
import webbrowser
from wx import adv 
from .cmd import *
from .functions import *
from .gui import *
from .tasks import *
from .pubsub import *
from .sqlite import *
from twisted.internet import wxreactor
from twisted.internet.error import ReactorAlreadyInstalledError
try:
    wxreactor.install()
except ReactorAlreadyInstalledError:
    pass
from twisted.internet import reactor






class Module(object):
    '''Every pluggable module should have a Define(Module) subclass 

    TODO: "Define" convention -> dir module classes issubclass(cls, Module)

    '''
    
    run = None
    task = None
    name = None

    def __init__(self, app):
        '''Define the module

        :param app: The main application
        :type app: ``adata.core.Application``
        '''
        self.app = app


    def call(self):
        '''Function to execute this module

        :return: Callable handler
        :rtype: function
        '''
        def call(e=None):
            self.execute()
        return call        


    def execute(self, event=None):
        '''Call the run and task methods if defined
        
        :param event: optional
        :type event: ``wx.Event`` or None.
        '''        
        if self.run is not None: 
            if self.name is not None:
                echo("Run %s " % self.name, color="ff8800", marker=self.name, icon='orange_arrow')
            self.run()

        if self.task is not None:
            def task(): self.task()
            Task(self.app, task, name=self.name)
    

    def menuitems(self, menu):
        '''Create menuitems
        '''
        for title, items in menu:
            for item in items:
                self.app.win.AddMenu(title, item)






def check_module(name):
    '''Try to Import the module and show errors

    :param name: Module name.
    :type name: string 
    :return: Module imported without errors
    :rtype: bool
    '''
    try:
        module = importlib.import_module(name, package=None)
        return True
    except Exception as error:
        echo(name)
        echo("Module '%s' %s: %s" % (name, error.__class__.__name__, error), 
            "ff5555", 
            marker="error", icon='red_circle')
        return False


def check_modules(folder):
    '''Check all modules in a folder.

    A module should not do anything when imported.
    But a script does: try check_modules(app.path["scripts"])

    :param folder: Module folder path.
    :type folder: string 
    '''
    errors = 0
    passed = 0
    for filename in os.listdir(folder):
        name, ext = os.path.splitext(filename)
        if name[0:2]=="__": continue
        if ext==".py": 
            if check_module(name): passed+=1
            else: errors+=1
    echo("%s %s/%s OK" % (folder, passed,passed+errors), 
        icon="orange_arrow" if errors else "green_arrow")








class Custom(object): 
    '''A custom global configuration placeholder for modules

        Common custom configuration options storage convention. 
        at wx.GetApp().custom.module_name
    '''
    pass                                                                                             







class Application(wx.App): 
    '''The minimal Adata wx application class.
    
    Here goes anything common to every concrete app
    
    '''

    custom = Custom
    module = {}
    loaded = []


    @staticmethod
    def pub(channel, **kwargs):
        '''Publish a pubsub message. 

        Keyword arguments should follow the spec.
        '''
        pub.sendMessage(channel, **kwargs)
        

    def ReactorLoop(self):
        '''Run wxpython in a Twisted event loop.
        '''
        self.reactor = reactor
        reactor.registerWxApp(self)
        reactor.run()


    def InitSystem(self):
        '''Configure system paths before UI creation
        '''
        self.info = {}
        self.info["python"] = "Python %s %s (%s) " % (
            sys.version[0:sys.version.index("(")], 
            platform.system(), 
            platform.version()
        ) 
        self.info["host"] = platform.node() 
        self.info["wx"] = wx.version()

        self.encoding = locale.getpreferredencoding()


        sp = wx.StandardPaths.Get()
        cwd = os.getcwd()        
        
        self.path = {
            "main": cwd,
            "data": os.path.join(cwd, 'data'),
            "icon": os.path.join(cwd, 'data', 'image', 'icon'),
            "image": os.path.join(cwd, 'data', 'image'),
            "audio": os.path.join(cwd, 'data', 'audio'),            
            "www": os.path.join(cwd, 'data', 'www'),            
        }
        
        path_user = getattr(sp,'GetUserLocalDataDir')()
        self.path["user"] = path_user
        self.path["exe"] = sp.ExecutablePath
        self.path["log"] = folder(os.path.join(path_user,"log"))
        self.path["db"] = os.path.join(path_user,"base.s3db")
        self.path["WebServer"] = os.path.join(self.path["data"],"web")

        favicon = os.path.join(self.path["www"],"favicon.ico")
        self.icon = wx.Icon(favicon,  wx.BITMAP_TYPE_ICO)
        
        self.file_log_name = os.path.join(self.path["log"], filestamp()+".txt")
        #self.echo("Log %s" % self.file_log_name)
        self.file_log = open(self.file_log_name,"a")
        self.file_log_size = os.stat(self.file_log_name).st_size
        self.file_log.write(self.info["python"])
        self.file_log.write(self.info["host"])
        for name,path in self.path.items():
            self.file_log.write("%s: %s\n" % (name,path) )
            
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        self.IP = s.getsockname()[0]
        s.close()
        self.info["host"]+=" - %s" % self.IP
        
        root = self.path["main"]
        while not "scripts" in os.listdir(root):
            root = os.path.dirname(root)
            if root is None: 
                break

        if root is not None:
            self.path["root"] = root
            self.path["modules"] = os.path.join(root, "modules")
            self.path["scripts"] = os.path.join(root, "scripts")
            sys.path.insert(0, self.path["modules"]) 
            sys.path.insert(0, self.path["scripts"]) 

       
        sys.path.append(self.path["main"]) 
        importlib.invalidate_caches()

        #echo("Path: %s " % self.path["modules"])


    def ConfigParser(self, filepath):
        '''Create a Windows style ini file parser
        
        :param filepath: File path.
        :type filepath: string
        :return: ConfigParser instance
        :rtype: ``configparser.ConfigParser``
        '''
        config = configparser.ConfigParser()
        config.read_file( open(filepath, "rt", encoding="utf-8-sig")) #sig: notepad BOM
        return config


    def ConfigDict(self, config, section):
        '''Read a configuration section.

        :param config: File path
        :type `config`: ``configparser.ConfigParser``
        :param section: [Section] title
        :type `section`: string
        :rtype: dict
        '''
        data = {}        
        for name, value in config.items(section):
            if value.lower()=="true": v = True
            elif value.lower()=="false": v = False
            else:
                try: v = int(value)
                except: v = value
            data[name.upper()] = v
        return data


    def About(self, evt):
        '''Display the About box
        '''
        info = adv.AboutDialogInfo()
        info.SetName(self.Title)
        info.SetVersion(self.Version)
        info.SetCopyright(self.Copyright)
        #info.Description = wordwrap(self.Description, 350, wx.ClientDC(self.TopWindow))
                
        x = '\n'.join([
            self.info["python"],
            "Twisted Internet " + twisted.version.short(),
            "User Interface: WX Phoenix " + self.info["wx"] + "\n",
            "- "*80,
            "\n",
        ])
        x+= '\n'.join([ "%s > %s (%s)" % m for m in self.loaded ])
        info.SetDescription(self.Description+'\n\n'+x)
        info.SetWebSite(self.WebSite)
        info.AddDeveloper(self.Developer)
        #info.SetLicence(wordwrap(self.License, 600, wx.ClientDC(self.TopWindow)))
        info.SetLicence(self.License)
        adv.AboutBox(info)



    def threads(self):
        '''Get all runing threads.
        '''
        threads = threading.enumerate()
        for thread in threads:
            if hasattr(thread, "app") and thread.app==self.app:
                color="00ff00"
            else:
                color="ff8800"
            echo("%s <%s>" % (thread.getName(), thread.__class__.__name__), color=color )
        return threads


        
    def Run(self, module="__auto__"):
        '''Execute the module.

        Calls the function returned by the defined call method.

        :param module: Module name.
        :type module: string 
        :return: 
        :rtype: ``Unknown``

        '''
        try:
            return self.run_module( module )(self)

        except Exception as error:
            echo("Error: %s" % error, "ff5555", marker="error", icon='dots')
            echo("%s" % traceback.format_exc(), "dddddd")
            echo("Run __auto__ failed!","ff5555", marker="error", icon='red_circle')
        
        #adata.traceback.print_tb(error.tb, file = sys.stderr)




    def load_module(self, name):
        ''' Custom modules loader

        Configures the module definition and creates custom GUI elements.    
        '''
        
        module = importlib.import_module(name, package=None)
        
        if hasattr(module, "Define"):
            define = module.Define(self)
            if hasattr(define, "menu"):
                menu = define.menu
                menuitem = define.menuitem()
                if not "call" in menuitem.keys():
                    menuitem["call"] = define.call()
                self.win.AddMenu( define.menu, menuitem )
                self.loaded.append(( menu, menuitem["name"], name))
            else:
                echo("Load: %s" % name)
                
            return define.call()

        else:
            echo("Module Define not found: %s" % name)
            return None


    def run_module(self, name):
        '''Get the defined execution call. 

        The default method returns a function that calls if found:

        - 1. the run method: Code executed in main thread 
        - 2. the task method: Start a new background task 

        TODO: use a loaded module cache 
        '''
        
        define = None
        module = importlib.import_module(name, package=None)
        if hasattr(module, "Define"):
            define = module.Define(self)
            return define.call()

        else:
            echo("Module %s is not defined" % name)

        return run




    def run_process_module(self, name):
        ''' TODO: multiprocessing modules
        '''
        def run(e):
            module = importlib.import_module(name, package=None)
            
            if hasattr(module, "RUN") and module.RUN:
                module.run(self)
            else:
                def task(): module.run(self)
                #Task(self, task, name=name)

                q = mp.Queue()
                p = mp.Process(target=module.run, args=(self,))
                p.start()
                print(q.get())
                p.join()

        return run




    def run_explorer(self, folder):
        '''Open a new Windows Explorer. 
        '''
        def run(e):
            fn = 'explorer.exe "%s"' % (folder)
            subprocess.Popen( fn , shell=True)
            self.win.Status("Explore "+fn)
        return run


    def run_file(self, path):
        '''Run default application to open a file.
        '''
        def run(e): 
            os.startfile(path) 
            self.win.Status("Open "+path)
        return run





