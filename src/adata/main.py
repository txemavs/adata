# adata.main
''' Main adata application and console window
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

    def OnOpen(self, e):
        print("TODO: Open a script")


    def OnPreInit(self):
        ''' Create the top window and configure the application basics.
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

        # Create the Toolbar
        self.tb = wx.ToolBar(self.win, -1, wx.DefaultPosition, wx.DefaultSize,
                           wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)

        self.win.SetToolBar(self.tb)
        
        i=10
        size = (24,24)
        handler = {}
        for bmp, label, call in [
            ("ART_GO_DOWN","Forward",   self.win.console.OnGoDown),
            ("ART_GO_UP","Back",        self.win.console.OnGoUp),
            ("ART_MINUS","Smaller",     self.win.console.OnSmaller),
            ("ART_PLUS","Bigger",       self.win.console.OnBigger),
            ("ART_NORMAL_FILE","Wrap",  self.win.console.OnWrap),
            (None, None, None),
            ("ART_FOLDER","Open",       self.OnOpen),
            (None, None, None),
            ("ART_FIND","Search",       self.win.console.OnFind),
            ("ART_GO_BACK","Back",      self.win.console.OnGoBack),
            ("ART_GO_FORWARD","Forward",self.win.console.OnGoForward),   
        ]:
            if bmp is None:
                self.tb.AddSeparator()
                continue
            art =  wx.ArtProvider.GetBitmap(getattr(wx, bmp), wx.ART_TOOLBAR, size)
            self.tb.AddTool(i, label, art, shortHelp=label)
            handler[i]=call
            i+=1

        def onTool(event):
            handler[event.GetId()](event)

        self.tb.Bind(wx.EVT_TOOL, onTool)
        self.tb.Realize()
        self.InitConfig() 
        
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        if not self.debug:
            sys.stdout = self.win.console
            sys.stderr = self.win.console

        self.InitDataBase()

       

    
    def OnInit(self): 
        """ Ready to go, twisted reactor manages the main loop.
            Must return True if OK
        """
        self.win.Show() 
        echo("")
        #self.cmd = Command(self)
        #self.cmd.Prompt(self.win.console)
        echo(self.info["python"])
        pub.subscribe(self.OnTask, 'app.task')
        return True 

        
    def OnTask(self, name="?"): 
        self.win.Status("OnTask %s" % name, echo=False)



    def OnExit(self):
        print("OnExit")
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
        uri = "file:///"+os.path.join(self.path["www"], "documentation", "index.html")
        echo(uri)
        webbrowser.open(uri) 





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

