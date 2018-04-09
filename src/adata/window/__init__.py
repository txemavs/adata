
import wx.html2
from ..core import *
from ..gui.text import TextEditor


class TextWindow(wx.Frame):
    '''A text editor window
    '''
    def __init__(self, filepath=None):
        wx.Frame.__init__(self, None, -1, filepath, size=(800, 600))
        self.text = TextEditor(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.text,1,wx.EXPAND)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.Show()
        with open(filepath, "rt", encoding="utf-8") as f: 
            self.text.AddText(f.read())
        




class Browser(wx.Frame):
    '''A web browser window
    '''
    def __init__(self, *args, **kwargs): 
        wx.Frame.__init__(self, *args, **kwargs) 
        self.browser = wx.html2.WebView.New(self) 
        sizer = wx.BoxSizer(wx.VERTICAL) 
        sizer.Add(self.browser, 1, wx.EXPAND, 10) 
        self.SetSizer(sizer) 
        self.SetSize((800, 600)) 
        self.Show()


    def Go(self, url):
        self.browser.LoadURL(url)



