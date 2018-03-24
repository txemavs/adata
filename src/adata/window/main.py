# adata.window.main
""" 
The base class for the Adata top window.

A Frame with Menu, the console and a status bar.


"""

from ..core import *
from ..gui.text import Console


class TopWindow(wx.Frame):
    """ A wx frame with some helpers

        Events, 

        Menu, 

        Dialogs

    """

    _menu = {}


    def UserInterface(self):

        ''' The usual layout is one scintilla text window
        '''
        # Create the main STC widget
        self.console = Console(self, style=wx.NO_BORDER)
        self.app.echo = self.console.echo

        sizer = SizerH()
        sizer.Add(self.console, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(sizer)

        self.SetTitle("%s - %s" % (self.app.Name, platform.node() ))
        self.sb = StatusBar(self, self.app)
        self.SetStatusBar(self.sb)
        self.Status(self.app.Copyright, console=False)
        
        # Events
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        pub.subscribe(self.OnEcho, 'app.echo')


    def Initialize(self): pass


    def __init__(self, app):
        self.app = app
        super(TopWindow, self).__init__(parent=None, title='', size=(1024,600))
        self._nobitmap = wx.Bitmap.FromRGBA(16,16,1,0,0,1)

        self.UserInterface()
        self.Initialize()






    # d88888b db    db d88888b d8b   db d888888b .d8888. 
    # 88'     88    88 88'     888o  88 `~~88~~' 88'  YP 
    # 88ooooo Y8    8P 88ooooo 88V8o 88    88    `8bo.   
    # 88~~~~~ `8b  d8' 88~~~~~ 88 V8o88    88      `Y8b. 
    # 88.      `8bd8'  88.     88  V888    88    db   8D 
    # Y88888P    YP    Y88888P VP   V8P    YP    `8888Y'




    def OnEcho(self, text, style="default", lf=True, marker=None, icon=None):
        """ Handle a app.echo event at the main thread
            Do not use **kwargs because the spec check
        """
        wx.CallAfter(self.console.echo, 
            text = text, 
            style = style, 
            lf = lf, 
            marker = marker, 
            icon = icon
        )


    def OnSize(self, event=None):
        #w,h=self.pan["gallery"].GetClientSizeTuple()
        if event is not None: event.Skip()


    def OnClose(self, event=None):
        for win in self.wins.keys(): self.wins[win].Close()
        if event is not None: event.Skip() 
        self.app.OnExit()
        

    def OnCloseWindow(self, event):
        print("OnCloseWindow")
        self.Destroy()
        

    def OnExit(self, event=None):
        print("EXIT")
        self.OnClose()
        self.Close()  # Close the main window.


    def OnTimer(self, event):
        t = time.localtime(time.time())
        st = time.strftime("%H-%M-%S", t)
        self.crono.SetValue(st)
        #self.count = self.count + 0.001
        #if self.count > 1: self.count = 0
        #self.progress.SetValue(self.count)
        self.sb.UpdateDate()


    def OnTaskEvent(self, event):
        """Show Result status."""
        if event.data is None:
        # Thread aborted (using our convention of None return)
            self.Status('Task aborted')
        else:
            self.Status('TE %s' % event.data, console=False)
        

    def OnTaskInfo(self, text):
        wx.PostEvent(self, TaskEvent(text))




    # .88b  d88. d88888b d8b   db db    db 
    # 88'YbdP`88 88'     888o  88 88    88 
    # 88  88  88 88ooooo 88V8o 88 88    88 
    # 88  88  88 88~~~~~ 88 V8o88 88    88 
    # 88  88  88 88.     88  V888 88b  d88 
    # YP  YP  YP Y88888P VP   V8P ~Y8888P' 
                                     
        
    def AddMenuItem(self, menu, name="", call=None, help="", style=wx.ITEM_NORMAL, icon = None):
        if name=="": 
            item = menu.AppendSeparator()
            return item
        if name in TEXT: 
            key = name
            name = TEXT[key]
            if HELP.has_key(key):
                help = HELP[key]
            if ICON.has_key(key):
                icon = ICON[key]
        
        noicon = style==wx.ITEM_NORMAL
        item = wx.MenuItem(menu, wx.ID_ANY, name, help, style)
        if call is not None: self.Bind(wx.EVT_MENU, call, item)
        if icon is not None: 
            path = os.path.join(self.app.path["icon"], icon)

            if not os.path.exists(path):
                path = os.path.join(self.app.path["main"], icon)

            if os.path.exists(path):
                item.SetBitmap(wx.Bitmap(path, wx.BITMAP_TYPE_PNG))
                noicon = False
            else:
                print("Falta icono: ",path)
        if noicon: item.SetBitmap(self._nobitmap)
        menu.Append(item)
        return item


    
    def AddMenu(self, title, menuitem):
        ''' Create MenuBar and Menur if needed, and add a MenuItem.
        '''
        menuBar = self.GetMenuBar()
        if menuBar is None:
            menuBar = wx.MenuBar()
            self.SetMenuBar(menuBar)
        
        if not title in self._menu.keys():
            m = wx.Menu()
            self.GetMenuBar().Append(m, title)
            self._menu[title] = m


        self.AddMenuItem(self._menu[title],**menuitem)
                             



    # d8888b. d888888b  .d8b.  db       .d88b.   d888b  .d8888. 
    # 88  `8D   `88'   d8' `8b 88      .8P  Y8. 88' Y8b 88'  YP 
    # 88   88    88    88ooo88 88      88    88 88      `8bo.   
    # 88   88    88    88~~~88 88      88    88 88  ooo   `Y8b. 
    # 88  .8D   .88.   88   88 88booo. `8b  d8' 88. ~8~ db   8D 
    # Y8888D' Y888888P YP   YP Y88888P  `Y88P'   Y888P  `8888Y'


    def Question(self, message, title="Question"):
        dialog = wx.MessageBox(message, title , wx.ICON_QUESTION | wx.YES_NO)
        return dialog == wx.YES
        

    def Message(self, message, title="Message"):
        dialog = wx.MessageDialog(self, message, title, wx.OK)
        dialog.ShowModal()
        dialog.Destroy()


    def Error(self, message, title="Error"):
        dialog = wx.MessageDialog(self, message, title, wx.OK | wx.ICON_ERROR)
        dialog.ShowModal()
        dialog.Destroy()
                
        
    def DirDialog(self, message, defaultPath="C:"):
        ''' Returns path or None
        '''
        dialog = wx.DirDialog(self, 
            message = message, 
            defaultPath = defaultPath
        )
        if dialog.ShowModal() == wx.ID_OK:
            dirname = dialog.GetPath()
            dialog.Destroy()
            return dirname
        else:
            dialog.Destroy()
            return


    def FileDialog(self, message, defaultDir="C:", wildcard='*.*'):
        ''' Returns file path or None
        '''
        dialog = wx.FileDialog(self, 
            message = message, 
            defaultDir = defaultDir, 
            wildcard = wildcard
        )
        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetFilename()
            dirname = dialog.GetDirectory()
            dialog.Destroy()
            return os.path.join(dirname,filename)
        else:
            dialog.Destroy()
            return









# .d8888. d888888b  .d8b.  d888888b db    db .d8888. d8888b.  .d8b.  d8888b. 
# 88'  YP `~~88~~' d8' `8b `~~88~~' 88    88 88'  YP 88  `8D d8' `8b 88  `8D 
# `8bo.      88    88ooo88    88    88    88 `8bo.   88oooY' 88ooo88 88oobY' 
#   `Y8b.    88    88~~~88    88    88    88   `Y8b. 88~~~b. 88~~~88 88`8b   
# db   8D    88    88   88    88    88b  d88 db   8D 88   8D 88   88 88 `88. 
# `8888Y'    YP    YP   YP    YP    ~Y8888P' `8888Y' Y8888P' YP   YP 88   YD

class StatusBar(wx.StatusBar):
    def __init__(self, win, app):
        wx.StatusBar.__init__(self, win, -1)

        self.win = win
        self.app = app
        
        self.SetFieldsCount(3)
        self.SetStatusWidths([-1, 140, 140])
        
        self.SetStatusText("", 0)
        self.SetStatusText("", 1)
        
        self.timer = wx.PyTimer(self.Refresh)
        self.timer.Start(1000)
        self.Refresh()


    def Refresh(self, format="%s %s %s"):
 
        
        t = time.localtime(time.time())
        self.SetStatusText(time.strftime("%B %d %A %H:%M", t), 1)
        
        self.SetStatusText("%s Threads - Line %s/%s" % (
            len(self.app.threads()),
            self.win.console.GetCurrentLine(),
            self.win.console.GetLineCount()-1
        ), 2)
        

