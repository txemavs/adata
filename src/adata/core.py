# adata.core
'''
Base class for adata applications.

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
import subprocess


from wx import adv 
from .cmd import *
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



def check_module(name):
    ''' A module should not do anything when imported.
        But a script does. Try check_modules(app.path["scripts"])
    '''
    try:
        module = importlib.import_module(name, package=None)
        return True
    except Exception as error:
        echo(name)
        echo("Module '%s' %s: %s" % (name, error.__class__.__name__, error), "ff5555", marker="error", icon='red_circle')
        return False


def check_modules(folder):
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



class Module(object):
    """ Every pluggable module should define a Define subclass 
    """
    
    run = None
    task = None
    name = None

    def __init__(self, app):
        self.app = app

    def call(self):
        def call(e=None):
            self.execute()
        return call        

    def execute(self, e=None):
        
        if self.run is not None: 
            if self.name is not None:
                echo("Run %s " % self.name, color="ff8800", marker=self.name, icon='orange_arrow')
            self.run()

        if self.task is not None:
            def task(): self.task()
            Task(self, task, name=self.name)
    

    def menuitems(self, menu):
        # Create menuitems
        for title, items in menu:
            for item in items:
                self.app.win.AddMenu(title, item)



class Custom(object): 
    ''' A custom global configuration placeholder 
    '''
    pass                                                                                             



def excepthook (etype, value, tb) :
    echo(" %s: %s" % (value.__class__.__name__, value), "ff5555", lf=False, marker="error", icon='red_arrow')
    echo("", icon='red_back')
    for x in traceback.format_tb(tb):
        if "code.py" in x: continue  
        if "codeop.py" in x: continue  
        if 'File "<input>"' in x: continue  
        echo( x , "dddddd", lf=False, icon='dots')
    where=""
    if hasattr(value, "filename"): where += " %s" % value.filename
    if hasattr(value, "lineno"):   where += " #%s" % value.lineno
    if where!="": echo("%s" % where,"888888")



#  .d8b.  d8888b. d8888b. db      d888888b  .o88b.  .d8b.  d888888b d888888b  .d88b.  d8b   db 
# d8' `8b 88  `8D 88  `8D 88        `88'   d8P  Y8 d8' `8b `~~88~~'   `88'   .8P  Y8. 888o  88 
# 88ooo88 88oodD' 88oodD' 88         88    8P      88ooo88    88       88    88    88 88V8o 88 
# 88~~~88 88~~~   88~~~   88         88    8b      88~~~88    88       88    88    88 88 V8o88 
# 88   88 88      88      88booo.   .88.   Y8b  d8 88   88    88      .88.   `8b  d8' 88  V888 
# YP   YP 88      88      Y88888P Y888888P  `Y88P' YP   YP    YP    Y888888P  `Y88P'  VP   V8P 

class Application(wx.App): 
    """ Bootstrap the wxPython system and initialize properties.
        Here goes anything common to every concrete app
    """

    custom = Custom
    module = {}
    loaded = []


    @staticmethod
    def pub(channel, **kwargs):
        ''' Publish a message 
        '''
        pub.sendMessage(channel, **kwargs)
        

    def ReactorLoop(self):
        ''' Run wxpython in a twisted event loop.
        '''
        self.reactor = reactor
        reactor.registerWxApp(self)
        reactor.run()


    def InitSystem(self):

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
        
        self.file_log_name = os.path.join(self.path["log"],filestamp()+".txt")
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
        config = configparser.ConfigParser()
        config.read_file( open(filepath, "rt", encoding="utf-8-sig")) #sig: notepad BOM
        return config


    def ConfigDict(self, config, section):
        data = {}        
        for name, value in config.items(section):
            if value.lower()=="true": v = True
            elif value.lower()=="false": v = False
            else:
                try: v = int(value)
                except: v = value
            data[name.upper()] = v
        return data


    def InitConfig(self):

        self.path["config"] = os.path.join(self.path["root"],"config.ini")
        #echo("Config: %s" % self.path["config"])
        #with open(self.path["config"], "rt", encoding="utf-8") as f: print(f.read())

        self.config = self.ConfigParser( self.path["config"] )
        self.language = self.config.get("SYSTEM", "language")
        self.database = self.config.get("SYSTEM", "database")
    
        self.system = self.ConfigDict(self.config, "SYSTEM")

        if "DEBUG" in self.system:  
            self.debug = self.system["DEBUG"] 






    def InitDataBase(self):
        
        self.path["db"] = os.path.join(self.path["user"], self.database)
        self.DB = DataBase(self.path["db"])
        if len(self.DB.tables())==0: 
            print("Creating new SQLite file: %s" % self.path["db"])
            sql_start = os.path.join(self.path["data"],"database.sql")
            with open(sql_start) as file:
                structure = file.read()
            for query in structure.split(";"): 
                sql=""
                for line in query.splitlines(): sql+=line
                self.DB.query(sql)
        #print(self.DB.info())
        #self.DB.types("type") 



    def InitLanguage(self):
        return
        
        file=os.path.join(PATH_DATA,"language",self.language+".ini")
        config = configparser.RawConfigParser()
        config.read(file)
        self.language_name = config.get("LANGUAGE", "name")
        self.date={}
        for name, value in config.items("DATA"): TEXT_DB[name.upper()]=value
        for name, value in config.items("TEXT"): TEXT[name.upper()]=value
        for name, value in config.items("HELP"): HELP[name.upper()]=value
        for name, value in config.items("ERROR"): ERROR[name.upper()]=value
        for name, value in config.items("DATE"): self.date[name]=value
        
        if "APP_DESC" in HELP: App.Description = HELP["APP_DESC"]
        if "APP_LICENSE" in HELP: App.License = HELP["APP_LICENSE"]

        
    def InitInstall(self):
        
        #print TEXT["PATH_HOME"]+":", PATH_HOME
        #print TEXT["PATH_DATA"]+":", self.path_user
        #print TEXT["LANGUAGE"]+": " + self.language_name
        
        # Return if log file exists
        log = os.path.join(self.path["user"], "install.log")
        marker = "Installation: %s\n" % self.path["main"]
        if os.path.exists(log): 
            with open(log) as f: txt = f.read()
            if marker in txt: return
        

        print("")
        print(TEXT["INSTALLING"])
        print("-"*79)

        
        #Create log file
        with open(log, "w") as f:            
            f.write(marker)
            f.write("Timestamp: %s" % timestamp())


        #Extract local.zip if exists
        data = os.path.join(self.path["main"], "local.zip")
        if not os.path.exists(data):
            print(HELP["LOCAL_DATA_NOT_FOUND"])
            return
        n = zip_extract(data, self.path["user"])
        if n == 0: 
            self.Error(ERROR["USER_DATA_NOT_INSTALLED"])
        
        print("-"*79)
        print("")

        #Backup existing database on every install
        print("SQLite file: %s" % self.path["db"])
        copy = ""
        if os.path.exists(self.path["db"]):
            copy = "base_"+filestamp()+".s3db"
            print("Backup %s" % copy) 
            shutil.copy2(self.path["db"], os.path.join(self.path["user"], copy))
            #delete original database?


    def InitResources(self):
        
        for name, value in self.config.items("ICON"): 
            if not ".png" in value: value+=".png"
            ICON[name.upper()] = value

        for name, value in self.config.items("IMAGE"): 
            if (not ".png" in value) and (not ".jpg" in value): value+=".png"
            IMAGE[name.upper()] = value




    def OnAbout(self, evt):
        """ Display the wx.adv.AboutBox
        """
        info = adv.AboutDialogInfo()
        info.SetName(self.Title)
        info.SetVersion(self.Version)
        info.SetCopyright(self.Copyright)
        #info.Description = wordwrap(self.Description, 350, wx.ClientDC(self.TopWindow))
                

        x = '\n'.join([
            self.info["python"],
            "WX Phoenix "+self.info["wx"]+"\n",
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
        return threading.enumerate()


        
    def Run(self, module="__auto__"):
        try:
            return self.run_module( module )(self)

        except Exception as error:
            echo("Error: %s" % error, "ff5555", marker="error", icon='dots')
            echo("%s" % traceback.format_exc(), "dddddd")
            echo("Run __auto__ failed!","ff5555", marker="error", icon='red_circle')
        
        #adata.traceback.print_tb(error.tb, file = sys.stderr)




    def load_module(self, name):
        """ Loads the module 
            Creates menuitem
            
        """
        
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
        """ Returns the function that calls a new Task on the module's run function 

            Define.run
            Define.task

        """
        
        define = None
        module = importlib.import_module(name, package=None)
        if hasattr(module, "Define"):
            define = module.Define(self)
            return define.call()

        else:
            echo("Module %s is not defined" % name)

        return run




    def run_process_module(self, name):
        """ Returns the function that calls a new Task on the module's run function 
        """
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
        def run(e):
            fn = 'explorer.exe "%s"' % (folder)
            subprocess.Popen( fn , shell=True)
            self.win.Status("Explore "+fn)
        return run


    def run_file(self, path):
        def run(e): 
            os.startfile(path) 
            self.win.Status("Open "+path)
        return run





