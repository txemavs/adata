import wx
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import adata





#----------------------------------------------------------------------------
#--- Base      self.win  

class Window(wx.Frame):
    size = (640, 480)
    style = None
    def __init__(self, win, key=None, *args, **kwargs):
        self.win = win
        #for key in kwargs:
        #    setattr(self, key, kwargs[key])
        self.key = key
        self.name = self.__class__.__name__
        if key is not None:
            self.name += ":"+str(key)
        if self.name!="Window": 
            if self.name in self.win.wins:
                self.win.wins[self.name].Show()
                print("EXISTE")
                del self
                return 
            self.win.wins[self.name]=self
        if self.style is None: style = wx.DEFAULT_FRAME_STYLE
        elif self.style == "dialog": style = wx.CAPTION | wx.CLOSE_BOX 
        elif self.style == "close": 
            style = wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN
            style = style | wx.FRAME_FLOAT_ON_PARENT|wx.FRAME_NO_TASKBAR
            #| wx.FRAME_TOOL_WINDOW 
        
        wx.Frame.__init__(self, self.win, -1, 'SMC', size=self.size, style=style)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.SetTitle('Ventana')
     
     
        self.panel = wx.Panel(self, -1) #, style=wx.RAISED_BORDER)
        sizer = SizerV()
        sizer.Add(self.panel, proportion=1, flag=wx.EXPAND)
        
        if self.style is None:
            self.sb = wx.StatusBar(self)
            self.SetStatusBar(self.sb)
            self.sb.SetStatusText("OK")
        else:
            self.sb = None
        self.SetSizer(sizer)
        self.init()
        self.Show()

    def Question(self, message, title="Pregunta"):
        return wx.MessageBox(message, title , wx.YES_NO, self)
        
    def Status(self,text, console=True):
        if console: self.win.console.write(text+"\n")
        if self.sb is not None: self.sb.SetStatusText(text)

    def OnClose(self, event=None):
        if self.name!="Window": 
            if self.name in self.win.wins: self.win.wins.pop(self.name)
        #print "CLOSING", str(self.name)
        if event is not None: event.Skip()

        








class Empty(wx.Window):
    def __init__(self, parent):
        super(Empty, self).__init__(parent, -1, style=wx.BORDER_NONE)

    



  



