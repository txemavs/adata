# adata.gui.basic

''' 
My WX helpers - old 2006 code - needs cleaning
'''

#__all__ = ['app','sizer','panel']

import os
import sys
import time
import datetime
import platform
import datetime, time, zipfile
import xml.etree.ElementTree as etree
import wx
import wx.lib.buttons as buttons
import wx.lib.masked as masked
from wx import adv 
from wx.lib.wordwrap import wordwrap
from urllib.request import urlopen
from urllib.error import URLError




class Dictionary(dict):
    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            return key

class DictionaryDefault(dict):
    def __init__(self, default=None):
        dict.__init__(self)
        self.default = default

    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            return self.default



PATH = os.path.dirname(os.path.dirname(__file__))
PATH_IMAGE = os.path.join(PATH, 'data', 'image')
PATH_ICON = os.path.join(PATH_IMAGE, 'icon')
BRD = 8
BRB = 5
EXA = wx.EXPAND|wx.ALL
POS = wx.DefaultPosition
SIZE = wx.DefaultSize

TEXT = Dictionary()
TEXT_DB = Dictionary()
HELP = Dictionary()
MSG = Dictionary()
ERROR = Dictionary()
IMAGE = DictionaryDefault("missing.png")
ICON = DictionaryDefault("missing.png")




def PlatformStyle():
    if 'wxMSW' in wx.PlatformInfo: return { 
        'times'     : 'Times New Roman',
        'mono'      : 'Courier New',
        'sans'      : 'Arial',
        'size'      : 11,
    }

    if 'wxMac' in wx.PlatformInfo: return { 
        'times'     : 'Lucida Grande',
        'mono'      : 'Monaco',
        'sans'      : 'Geneva',
        'size'      : 12,
    }
    
    if 'gtk2' in wx.PlatformInfo or 'gtk3' in wx.PlatformInfo: return { 
        'times'     : 'Serif',
        'mono'      : 'Monospace',
        'sans'      : 'Sans',
        'size'      : 10,
    }

    return { 
        'times'     : 'Times',
        'mono'      : 'Courier',
        'sans'      : 'Helvetica',
        'size'      : 12,
    }
                                                                    
                  




def ImageLoad(name):
    path = os.path.join(PATH_IMAGE, name)
    return wx.Image(path, wx.BITMAP_TYPE_JPEG)


def Icon(name):
    filename = os.path.join(PATH_ICON, ICON[name])
    return wx.Icon(filename, wx.BITMAP_TYPE_PNG)


def SetValues(data, controls):
    for i in controls.keys():
        d = data[i]
        if d is None: value = ""
        elif type(d)==type(0) or type(d)==type(0.0): value=str(d)
        else: value = d 
        controls[i].SetValue(value)



def binary(i):
    b = ''
    while i > 0:
        j = i & 1
        b = str(j) + b
        i >>= 1
    return b


def xml_code(node, cmd=False):
    tab=0
    CR=u'\u0010'+u'\u2028'
    code=""
    text=etree.tostring(node)
    for elem in text.split("<"):
        if elem!="":
            if elem[0]=="/": tab-=2
            if cmd: code+= ("".rjust(tab)+"<"+elem)[0:79]+"\n"
            else: code+= ("".rjust(tab)+"<"+elem)+CR
            if elem[0]!="/" and not "/>" in elem: tab+=2
    return code

def strtime(tt):
    if tt is None: tt=0
    mm=int(tt//(60))
    tt=tt-mm*60
    ss=int(tt)
    tt=tt-ss
    cc=int(tt*100)
    #ff=int(tt*25)*4
    return str(mm).zfill(2)+"-"+str(ss).zfill(2)+"-"+str(cc).zfill(2)


#def timestamp():
#    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def timestamp(timer=None):
    if timer is None: timer = time.time()
    dt_obj = datetime.datetime.fromtimestamp(timer)
    return dt_obj.strftime("%Y-%m-%d %H:%M:%S")





def filestamp(timer=None):
    if timer is None: timer = time.time()
    dt_obj = datetime.datetime.fromtimestamp(timer)
    return dt_obj.strftime("%Y%m%d-%H%M%S")

def zip_extract(path, dest):
    try:
        zip = zipfile.ZipFile(path, 'r')
    except:
        return 0
    if zip.testzip() is not None: 
        print("ZIP CORRUPT: "+path)
        return 0
    n=0
    #try:
    if True:
        for archive in zip.namelist():
            #print os.path.join(dest, archive)
            zip.extract(archive, dest)
            n+=1
        print(str(n)+" files extracted")
        return n
    #except:
    #    raise Exception()
    #    print "ZIP ERROR: "+path
    #    return 0






def folder(path):
    if not os.path.exists(path): 
        os.makedirs(path)
    return path

def htmlchars(text): 
    return text.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")




def ping(host):
    """
    Returns True if host responds to a ping request
    """
    
    ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"

    # Ping
    return os.system("ping " + ping_str + " " + host) == 0

def internet_on():
    try:
        response=urlopen('http://google.com',timeout=1)
        return True
    except URLError as err: pass
    return False




#  .d8888. d888888b d88888D d88888b d8888b. .d8888. 
#  88'  YP   `88'   YP  d8' 88'     88  `8D 88'  YP 
#  `8bo.      88       d8'  88ooooo 88oobY' `8bo.   
#    `Y8b.    88      d8'   88~~~~~ 88`8b     `Y8b. 
#  db   8D   .88.    d8' db 88.     88 `88. db   8D 
#  `8888Y' Y888888P d88888P Y88888P 88   YD `8888Y'



def Border(sizer, border):
    s = SizerV()
    s.Add(sizer, 1, wx.EXPAND|wx.ALL, border)
    return s
        
class SizerV(wx.BoxSizer):
    def __init__(self):
        super(SizerV, self).__init__(wx.VERTICAL)
        
        
class SizerH(wx.BoxSizer):
    def __init__(self):
        super(SizerH, self).__init__(wx.HORIZONTAL)


class SizerVB(wx.BoxSizer):
    def __init__(self, items, border=8):
        super(SizerVB, self).__init__(wx.VERTICAL)
        style = EXA
        style_first = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP
        style_last = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM
        if len(items)==1:
            self.Add(items[0][0], items[0][1], style, border)
            return
        last = len(items)-1
        self.Add(items[0][0], items[0][1], style_first, border)
        for i in range(1, last):
            self.Add(items[i][0], items[i][1], style, border)
        self.Add(items[last][0], items[last][1], style_last, border)


class SizerBox(wx.StaticBoxSizer):
    def __init__(self, parent, title):
        box = wx.StaticBox(parent, -1, title)
        super(SizerBox, self).__init__(box, wx.VERTICAL)



class SizerRow(wx.FlexGridSizer):
    def __init__(self, items):
        super(SizerRow, self).__init__(1, len(items), 0, 0)
        self.AddGrowableCol(0)
        prop = 1
        for item in items:
            self.Add(item, prop, wx.EXPAND)
            if prop==1: prop=0

class SizerTable(wx.FlexGridSizer):
    def __init__(self, parent, items, expand=[]):
        super(SizerTable, self).__init__(len(items), 2, 5, 5)
        self.AddGrowableCol(1)
        for row in expand:
            self.AddGrowableRow(row)
        for label, widget in items:
            self.Add(wx.StaticText(parent, -1, label+":"), 0, wx.ALL, 4) #wx.ALIGN_CENTER_VERTICAL
            self.Add(widget, 0, wx.EXPAND)        










#  d8888b.  .d8b.  d8b   db d88888b db      .d8888. 
#  88  `8D d8' `8b 888o  88 88'     88      88'  YP 
#  88oodD' 88ooo88 88V8o 88 88ooooo 88      `8bo.   
#  88~~~   88~~~88 88 V8o88 88~~~~~ 88        `Y8b. 
#  88      88   88 88  V888 88.     88booo. db   8D 
#  88      YP   YP VP   V8P Y88888P Y88888P `8888Y' 



class BasePanel(wx.Panel):
    """ REVISAR SMC
    """
    def __init__(self, parent, win, frame=None):
        
        self.pan = {}
        self.but = {}
        self.box, self.original = {}, {}        
        self.win = win
        if frame is None: self.frame = win
        else: self.frame = frame
        wx.Panel.__init__(self, parent, style=wx.BORDER_NONE)
        self.ready = False
        self.init()
        self.ready = True
        self.parent = parent

    def Question(self, title, text):
        res = self.win.Question(text, title)
        return res == wx.YES

    def Status(self, text):
        if self.ready: self.win.Status(text)

    def PanButtonsH(self, parent, buttons):
        p = Panel(parent)
        s = SizerH()
        s.Add(wx.Window(p, -1), 1, wx.ALL , BRB)
        for name, image, call in buttons:
            img = self.win.image[image]
            self.but[name] = Button(p, TEXT[name], call, img)
            s.Add(self.but[name], 0, wx.ALL , BRB)
        p.SetSizer(s)
        return p

    def PanButtonsV(self, parent, buttons):
        p = Panel(parent)
        s = SizerV()
        for name, image, call in buttons:
            img = self.win.image[image]
            self.but[name] = Button(p, TEXT[name], call, img, size=(128,32))
            s.Add(self.but[name], 0, wx.ALL , BRB)
        s.Add(wx.Window(p, -1), 1, wx.ALL , BRB)
        p.SetSizer(Border(s, BRD))
        return p

    def OnButtonCancel(self, event):
        if self.frame is not None:
            self.frame.Close()

    def DataGet(self):
        for name in self.box:
            if hasattr(self.box[name], "GetValue"):
                self.original[name] = self.box[name].GetValue()

    def DataModified(self):
        for name in self.box:
            if name in self.original:
                if hasattr(self.box[name], "GetValue"):
                    if self.original[name]!=self.box[name].GetValue(): 
                        return True
        return False    

    def DataCheck(self, event=None):    
        self.but["UPDATE"].Enable(self.DataModified())
        print("DataCheck %s" % str(self.DataModified()))

#def Panel(parent):
#    return wx.Panel(parent, -1, style=wx.BORDER_NONE|wx.TAB_TRAVERSAL)

class PanelBox(wx.Panel):
    def __init__(self, parent):
        super(PanelBox, self).__init__(parent, -1, style=wx.BORDER_NONE)
        self.sizer = SizerV()

    def Contains(self, panel):
        self.sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.GetParent().Layout()
        return self



class Panel(wx.Panel):
    def __init__(self, parent):
        super(Panel, self).__init__(parent, -1, 
                            style=wx.BORDER_NONE|wx.TAB_TRAVERSAL)

    def Visible(self, value=True):
        if value:
            self.Show()
            self.GetParent().Layout()
        else:
            self.Hide()





class DateTimePicker(wx.Panel):
    def __init__(self, parent, call=None, *args,**kwargs):
        super(DateTimePicker, self).__init__(parent, *args, **kwargs)
        self.box_date = DatePicker(self)
        self.box_time = TimePicker(self)
        self.box_time.Now()
        s = SizerH()
        s.Add(self.box_date,1,wx.EXPAND)
        s.Add(self.box_time,0,wx.EXPAND)
        self.SetSizer(s)
        if call is not None: 
            self.box_time.Bind(masked.EVT_TIMEUPDATE, call)
            self.box_date.Bind(wx.EVT_DATE_CHANGED, call)

        
    def SetValue(self,value):
        pass
    
    def GetValue(self):
        date = self.box_date.GetValue()
        time = self.box_time.GetValue()
        return datetime.datetime(date.year, date.month, date.day, 
                                 int(time[0:2]), int(time[3:5]))
        



class Image(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        self.image = None  # wxPython image
        wx.EVT_SIZE(self,self.OnSize)
        wx.EVT_PAINT(self, self.OnPaint)

    def display(self, path):
        print("Image display",path)
        if os.path.exists(path):
            self.image = wx.Image(path, wx.BITMAP_TYPE_ANY)
        else:
            self.image = None
        self.Refresh(True)

    def OnSize(self, event):
        self.Width, self.Height = self.GetClientSizeTuple()

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        if not self.image: 
            return
        W, H = self.Width, self.Height
        w, h = self.image.GetWidth(), self.image.GetHeight()
        A, a = W/float(H), w/float(h)
        if A < a:
            sw, sh = W, W/a
            ow, oh = 0, (H-sh)/2
        else:
            sw, sh = H*a, H
            ow, oh = (W-sw)/2, 0
        scaled = self.image.Scale(sw, sh, wx.IMAGE_QUALITY_HIGH)
        dc.DrawBitmap(scaled.ConvertToBitmap(), ow, oh)




class ProgressBar(wx.Panel):
    def __init__(self, parent, color=(255,255,255), bgcolor=(0,0,0)):
        wx.Panel.__init__(self, parent, 
                          style=wx.BORDER_NONE | wx.NO_FULL_REPAINT_ON_RESIZE)
        wx.EVT_SIZE(self,self.OnSize)
        wx.EVT_PAINT(self,self.OnPaint)
        #self.SetDoubleBuffered(True)
        self.SetBackgroundColour(bgcolor)
        self.SetForegroundColour(color)
        self.value = 0
        self.color = color
        self.OnSize(None)
        
    def SetValue(self, value):
        self.value = value
        self.UpdateDrawing()
        
    def OnSize(self, event=None):
        self.Width, self.Height = self.GetClientSizeTuple()
        self._Buffer = wx.EmptyBitmap(self.Width, self.Height)
        self.Draw()
        
    def OnPaint(self,event):
        event.Skip()
        self.Draw()
        
    def UpdateDrawing(self):
        dc = wx.BufferedDC(wx.ClientDC(self), self._Buffer)
        self.Draw(dc)
        
    def Draw(self, dc=None):
        if dc is None: dc = wx.ClientDC(self)
        width,height = self.Width, self.Height#self.GetSize()
        w=int(width*self.value)
        if w<8:w=8
        h=height
        x=(width-w)/2
        y=0
        dc.BeginDrawing()
        dc.Clear()
        dc.SetBrush(wx.Brush((0,0,0)))
        dc.DrawRectangle(0,0,width,height)
        dc.SetBrush(wx.Brush(self.color))
        
        dc.DrawRoundedRectangle(0,0,width,height,4)
        dc.SetBrush(wx.Brush((0,0,0)))
        dc.DrawRoundedRectangle(4,4,width-8,height-8,4)
        dc.SetBrush(wx.Brush(self.color))
        dc.DrawRoundedRectangle(6,6,int(self.value*(width-12)),height-12,4)
        #dc.SetPen(wx.Pen((255,255,255), 12, wx.SOLID))        
        #dc.DrawText(str(int(self.value*100))+"%",0,0)
        dc.EndDrawing()





#   .o88b.  .d88b.  d8b   db d888888b d8888b.  .d88b.  db      .d8888. 
#  d8P  Y8 .8P  Y8. 888o  88 `~~88~~' 88  `8D .8P  Y8. 88      88'  YP 
#  8P      88    88 88V8o 88    88    88oobY' 88    88 88      `8bo.   
#  8b      88    88 88 V8o88    88    88`8b   88    88 88        `Y8b. 
#  Y8b  d8 `8b  d8' 88  V888    88    88 `88. `8b  d8' 88booo. db   8D 
#   `Y88P'  `Y88P'  VP   V8P    YP    88   YD  `Y88P'  Y88888P `8888Y' 
                                                                    
                                                                    
                                                                    
                                                                    
                                                                    
                                                                    
                                                                    
                                                                    

class Text(wx.TextCtrl):
    def __init__(self, parent, edit=True, multiline=False, value="", 
                 change=None, key=None, font=None, size=(32,24), style=None):
        if style is None:
            if edit: style = wx.BORDER_SUNKEN
            else: style = wx.TE_READONLY | wx.SIMPLE_BORDER
        if multiline: style = style | wx.TE_MULTILINE     
        style = style | wx.TE_RICH | wx.TE_RICH2   
        #super(Text, self).__init__(parent, -1, value, style=style, size=size)    
        super(Text, self).__init__(parent, -1, style=style, size=size)    
        if change is not None: self.Bind(wx.EVT_KILL_FOCUS, change)
        if key is not None: self.Bind(wx.EVT_TEXT, key)
        if font is not None: self.SetFont(font)


class Button(buttons.GenBitmapTextButton):
    """ Image button
    """
    def __init__(self, parent, caption, call, image=None, size=(100,32)):
        #x = wx.Button(parent, -1, caption)
        if image is not None: caption="  "+caption
        if size[0]>100: self.DrawLabel = self.DrawLabelRight
        super(Button, self).__init__(parent, -1, None, caption, size=size)
        if image is not None: self.SetBitmapLabel(image)
        self.Bind(wx.EVT_BUTTON, call)
    

    def DrawLabelRight(self, dc, width, height, dx=0, dy=0):
        bmp = self.bmpLabel
        if bmp is not None:     # if the bitmap is used
            if self.bmpDisabled and not self.IsEnabled():
                bmp = self.bmpDisabled
            if self.bmpFocus and self.hasFocus:
                bmp = self.bmpFocus
            if self.bmpSelected and not self.up:
                bmp = self.bmpSelected
            bw,bh = bmp.GetWidth(), bmp.GetHeight()
            if not self.up:
                dx = dy = self.labelDelta
            hasMask = bmp.GetMask() is not None
        else:
            bw = bh = 0     # no bitmap -> size is zero

        dc.SetFont(self.GetFont())
        if self.IsEnabled():
            dc.SetTextForeground(self.GetForegroundColour())
        else:
            dc.SetTextForeground(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT))

        label = self.GetLabel()
        tw, th = dc.GetTextExtent(label)        # size of text
        if not self.up:
            dx = dy = self.labelDelta

        #pos_x = (width-bw-tw)/2+dx      # adjust for bitmap and text to centre
        pos_x = 8
        if bmp is not None:
            dc.DrawBitmap(bmp, pos_x, (height-bh)/2+dy, hasMask) # draw bitmap if available
            pos_x = pos_x + 2   # extra spacing from bitmap

        dc.DrawText(label, pos_x + dx+bw, (height-th)/2+dy)      # draw the text



class CheckBox(wx.CheckBox):       
    def __init__(self, parent, caption, call):
        super(CheckBox, self).__init__(parent, -1, caption)
        self.Bind(wx.EVT_CHECKBOX, call)



class ListBox(wx.ListBox): 
    def __init__(self, parent, call=None, double=None):
        self.key={}
        super(ListBox, self).__init__(parent, -1, size=(80,80), style=wx.LB_SINGLE)
        if call is not None: 
            self.Bind(wx.EVT_LISTBOX, call)
        if double is not None:     
            self.Bind(wx.EVT_LISTBOX_DCLICK, double)

    def GetKey(self):
        value = self.GetStringSelection()
        if value in self.key: 
            return self.key[value] 

    def GetItemsFromData(self, data):
        l, self.key = [], {}
        selected = self.GetStringSelection()
        if len(data)>0:
            if len(data[0])>1:
                for result in data: 
                    value = result[1]
                    if len(result)>2:
                        for i in range(2,len(result)): value+=","+result[i]
                    self.key[value]=result[0]
                    l.append(value)
            else: 
                for result in data: l.append(result[0])
        if self.GetItems()!=l: 
            self.SetItems(l)
        if selected in l:
            self.SetSelection(l.index(selected))
        return l

class ComboBox(wx.ComboBox):       
    """ Una lista de opciones
    """
    def __init__(self, parent, choices=None, call=None, edit=True, 
                 sort=False, first=None):
        if sort: style = wx.CB_SORT
        else: style = 0
        if not edit: style = style | wx.CB_READONLY
        self.first = first
        if first is not None: 
            if choices is None: choices=[first]
            else: choices=[first]+choices
        if choices is None: choices=[]
        super(ComboBox, self).__init__(parent, -1, "", style=style , 
                                       choices=choices)
        if call is not None: 
            self.Bind(wx.EVT_KILL_FOCUS, call)
            self.Bind(wx.EVT_COMBOBOX, call)
        self.key = {}

    def GetKey(self):
        value = self.GetValue()
        if value in self.key: 
            return self.key[value] 
        else:
            return value

    def GetItemsFromData(self, data):
        #data = self.DB.result("SELECT DISTINCT type FROM sequences ORDER BY type")
        selected = self.GetValue()
        
        if self.first is None: 
            l=[]
            self.key={}
        else: 
            l = [self.first]
            self.key={self.first:None}
        if len(data)>0:
            if len(data[0])>1:
                for result in data: 
                    value = result[1]
                    if len(result)>2:
                        for i in range(2,len(result)): 
                            value+=", "+result[i]
                    self.key[value]=result[0]
                    l.append(value)
            else: 
                for result in data: l.append(result[0])
                
        if "" in l: l.remove("")
        if self.GetItems()!=l: self.SetItems(l)
        if selected in l:
            self.SetSelection(l.index(selected))
        else:
            if self.first is not None:
                self.selected = l[0]
                self.SetSelection(0)
        return l
        
        

    
            
#def DatePicker(parent, call):
#    x = MyDatePickerCtrl(parent, style = wx.DP_DROPDOWN)
#    x.Bind(wx.EVT_DATE_CHANGED, call)
#    return x 

class TimePicker(masked.TimeCtrl):
    def __init__(self, parent, call=None, *args,**kwargs):
        #wx.DatePickerCtrl.__init__(self, parent, *args,**kwargs)
        super(TimePicker, self).__init__(parent, style=adv.DP_DROPDOWN, 
                                         *args, **kwargs)
        if call is not None: 
            self.Bind(masked.EVT_TIMEUPDATE, call)


    def Now(self):
        t = datetime.datetime(2000,1,1).today()
        wxvalue=wx.DateTime()
        wxvalue.Set(year=t.year, month=t.month-1, day=t.day, 
                    hour=t.hour, minute=t.minute)
        self.SetValue(wxvalue)
 
class DatePicker(adv.DatePickerCtrl):
    def __init__(self, parent, call=None, *args,**kwargs):
        #wx.DatePickerCtrl.__init__(self, parent, *args,**kwargs)
        super(DatePicker, self).__init__(parent, style=adv.DP_DROPDOWN, 
                                         *args, **kwargs)
        if call is not None: 
            self.Bind(wx.EVT_DATE_CHANGED, call)
        
    def SetValue(self,value):
        """Set either datetime.datetime or wx.DateTime"""
        if isinstance(value,(datetime.date,datetime.datetime)):
            wxvalue=wx.DateTime()
            wxvalue.Set(year=value.year,month=value.month-1,day=value.day)
            value=wxvalue
        elif value is None:
            value=wx.DateTime()
        wx.DatePickerCtrl.SetValue(self,value)
        
    def GetValue(self):
        """Returns datetime.datetime values"""
        value=wx.DatePickerCtrl.GetValue(self)
        if not value.IsValid():    #Manage null dates (useful when wx.DP_ALLOWNONE is set)
            return None
        else:
            return datetime.datetime(value.GetYear(),value.GetMonth()+1,value.GetDay())



                                                  



# d88888b d8888b. d8888b.  .d88b.  d8888b. .d8888. 
# 88'     88  `8D 88  `8D .8P  Y8. 88  `8D 88'  YP 
# 88ooooo 88oobY' 88oobY' 88    88 88oobY' `8bo.   
# 88~~~~~ 88`8b   88`8b   88    88 88`8b     `Y8b. 
# 88.     88 `88. 88 `88. `8b  d8' 88 `88. db   8D 
# Y88888P 88   YD 88   YD  `Y88P'  88   YD `8888Y'            

class ErrorWindow(wx.Frame):
    def __init__(self, value, tb):
        # based on a frame, so set up the frame
        print("ERROR: %s" % value)
        #print(dir(value))

        title=value.__class__.__name__

        if hasattr(value, "filename"): title += " %s" % value.filename
        if hasattr(value, "lineno"):   title += " #%s" % value.lineno

        wx.Frame.__init__(self, None, -1, title, size=(720, 480))
        font = wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.NORMAL)



        self.text = Text(self, multiline=True, font=font)
        #self.text = StyledText(self)
        self.text.SetBackgroundColour((255,255,255))
        self.text.SetForegroundColour((255,0,0))
        #self.text.echo("%s\n" % value)
        #self.text.echo("\n\nTraceback:\n\n", "fore:#FF0F0F,back:#0F0000,bold")
        self.text.write("%s\n" % value)
        self.text.write("\n\nTraceback:\n\n")
        #self.text.SetForegroundColour((0,0,0))
        
        traceback.print_tb(tb, file = self.text)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.text,1,wx.EXPAND)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        #self.sizer.Fit(self)
        self.Show()









ART = [
    "ART_ERROR",
    "ART_GOTO_LAST",
    "ART_FILE_SAVE_AS",
    "ART_QUESTION",
    "ART_PRINT",
    "ART_DELETE",
    "ART_WARNING",
    "ART_HELP",
    "ART_COPY",
    "ART_INFORMATION",
    "ART_TIP",
    "ART_CUT",
    "ART_ADD_BOOKMARK",
    "ART_REPORT_VIEW",
    "ART_PASTE",
    "ART_DEL_BOOKMARK",
    "ART_LIST_VIEW",
    "ART_UNDO",
    "ART_HELP_SIDE_PANEL",
    "ART_NEW_DIR",
    "ART_REDO",
    "ART_HELP_SETTINGS",
    "ART_FOLDER",
    "ART_PLUS",
    "ART_HELP_BOOK",
    "ART_FOLDER_OPEN",
    "ART_MINUS",
    "ART_HELP_FOLDER",
    "ART_GO_DIR_UP",
    "ART_CLOSE",
    "ART_HELP_PAGE",
    "ART_EXECUTABLE_FILE",
    "ART_QUIT",
    "ART_GO_BACK",
    "ART_NORMAL_FILE",
    "ART_FIND",
    "ART_GO_FORWARD",
    "ART_TICK_MARK",
    "ART_FIND_AND_REPLACE",
    "ART_GO_UP",
    "ART_CROSS_MARK",
    "ART_HARDDISK",
    "ART_GO_DOWN",
    "ART_MISSING_IMAGE",
    "ART_FLOPPY",
    "ART_GO_TO_PARENT",
    "ART_NEW",
    "ART_CDROM",
    "ART_GO_HOME",
    "ART_FILE_OPEN",
    "ART_GOTO_FIRST",
    "ART_FILE_SAVE"
]
