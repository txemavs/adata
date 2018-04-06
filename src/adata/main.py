# adata.main
''' Main Adata application initialize
'''

from .window.main import *


class App(Application):
    ''' The Adata main application is a text console window.
    '''
    Name = "Adata"
    Title = "Adata Automation Framework"
    Version = "0.0.1"
    WebSite = "http://www.nabla.net/adata"
    Copyright = u"(c)2018 Nabla.net"
    
    Developer = "Txema Vicente Segura <txema@nabla.net>"
    
    Description = '''
A portable IFTTT event handling framework to run your python scripts.

Twisted Internet Reactor + WX Python application.'''
    
    License = '''
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
    
    win = None


    def OnPreInit(self):
        ''' Configure the application basics.
        
            - Create the top Window             
            - Prepare local file database

        '''

        self.win = Window(self)
        self.SetTopWindow(self.win) 
        
        self.InitSystem()
        self.win.SetIcon(self.icon)

        # Welcome message directly to console
        self.win.console.echo(" ")
        self.win.console.echo(" "+self.Title+": "+self.info["host"],  "fore:#CCEEFF") 
        self.win.console.echo(" ")
        for line in range(0,3): 
            self.win.console.Mark(line, 'blue_back')


        self.InitConfig() 
        
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        if not self.debug:
            sys.stdout = self.win.console
            sys.stderr = self.win.console

        self.InitDataBase()

       




    def InitConfig(self):
        '''Load application initial configuration.
        '''
        path = os.path.join(self.path["root"],"config.ini")
        self.path["config"] = path
        self.config = self.ConfigParser( path )    
        self.system = self.ConfigDict(self.config, "SYSTEM")
        self.language = self.config.get("SYSTEM", "language")
        self.database = self.config.get("SYSTEM", "database")
    
        if "DEBUG" in self.system:  
            self.debug = self.system["DEBUG"] 



    def InitDataBase(self):
        '''Create the local sqlite3 database for local user data.
        '''
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




    
    def OnInit(self): 
        '''Ready to go, twisted reactor manages the main loop.
        
        Must return True if OK
        '''
        self.win.Show() 
        echo("")
        #self.cmd = Command(self).Prompt(self.win.console)
        echo(self.info["python"])
        pub.subscribe(self.OnTask, 'app.task')
        return True 

        
    def OnTask(self, name="?"): 
        '''Subscribed to app.task, shows message at status
        '''
        self.win.Status("OnTask %s" % name, echo=False)



    def OnExit(self):
        '''Wait if threads running and close log file.
        '''
        
        # Wait for threads    
        while True:
            threads = self.threads()
            if len(threads)<=1:
                break
            echo("Waiting for %s threads..." % len(threads))
            time.sleep(1)

        self.file_log.write("THREAD ALIVE "+str(threads)+"\n")
            
        if os.path.exists(self.file_log_name):
            if os.stat(self.file_log_name).st_size == self.file_log_size:
                sys.stderr = self.stderr
                self.file_log.close()
                #os.remove(self.file_log_name)
        
        return True



    def Documentation(self, event=None):
        '''See HTML documentation.
        '''
        uri = "file:///"+os.path.join(self.path["www"], "documentation", "index.html")
        echo(uri)
        webbrowser.open(uri) 






def excepthook (etype, value, tb) :
    '''The application error handler.
    
    Send error details to subscribed consoles.

        :param etype: Exception type
        :type etype: type
        :param value: Exception value
        :type value: Exception
        :param tb: Traceback
        :type tb: ``traceback``
    '''
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








# db   d8b   db d888888b d8b   db d8888b.  .d88b.  db   d8b   db 
# 88   I8I   88   `88'   888o  88 88  `8D .8P  Y8. 88   I8I   88 
# 88   I8I   88    88    88V8o 88 88   88 88    88 88   I8I   88 
# Y8   I8I   88    88    88 V8o88 88   88 88    88 Y8   I8I   88 
# `8b d8'8b d8'   .88.   88  V888 88  .8D `8b  d8' `8b d8'8b d8' 
#  `8b8' `8d8'  Y888888P VP   V8P Y8888D'  `Y88P'   `8b8' `8d8'  
#------------------------------------------------------------------------------


class Window(TopWindow):
    ''' The main top window
    '''

    def Initialize(self):
        """ Create the UI and susbcribe to app.echo pubsub channel
        """
        # Events        
        EVT_TASK(self, self.OnTaskEvent)


    def OnClose(self, event=None):
        """ Stop all threads before exit
        """

        if len(self.app.threads())>1:
            if event and event.CanVeto(): 
                event.Veto()
            echo("Closing...", marker="OnClose", icon="red_circle")
            publish("app.stop")
            self.app.reactor.stop()        
            return


    def Status(self, text=None, console=False, mode=None):
        """ Update the status bar
        """
        if text is not None: self.sb.SetStatusText(text)
        if mode is not None: self.sb.SetStatusText(mode, 2)
        else:
            if console: self.console.echo(text+"\n")









