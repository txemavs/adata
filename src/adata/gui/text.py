# adata.gui.text
''' 
Console emulation using scintilla
'''

from .basic import *
from wx import stc
import json
import keyword

RGB = wx.Colour
SYS_COLOUR = wx.SystemSettings.GetColour

#self.GetEOLMode()

#See http://proton-ce.sourceforge.net/rc/scintilla/pyframe/www.pyframe.com/stc/markers.html
MARKERS = {
    'prompt':       (stc.STC_MARK_SHORTARROW,   RGB(0, 0, 0),       RGB(0, 255, 0)      ),
    'blue_arrow':   (stc.STC_MARK_ARROW,        RGB(0, 0, 0),       RGB(0, 0, 255)      ),
    'blue_circle':  (stc.STC_MARK_CIRCLE,       RGB(0, 0, 0),       RGB(0, 0, 255)      ),
    'red_arrow':    (stc.STC_MARK_ARROW,        RGB(0, 0, 0),       RGB(255, 0, 0)      ),
    'red_rect':     (stc.STC_MARK_SMALLRECT,    RGB(0, 0, 0),       RGB(255, 0, 0)      ),
    'red_back':     (stc.STC_MARK_BACKGROUND,   RGB(255, 255, 0),   RGB(32, 0, 0)       ),
    'green_back':   (stc.STC_MARK_BACKGROUND,   RGB(255, 255, 0),   RGB(0, 32, 0)       ),
    'blue_back':    (stc.STC_MARK_BACKGROUND,   RGB(255, 255, 0),   RGB(0, 0, 32)       ),
    'red_circle':   (stc.STC_MARK_CIRCLE,       RGB(0, 0, 0),       RGB(255, 64, 64)    ),
    'orange_arrow': (stc.STC_MARK_ARROW,        RGB(0, 0, 0),       RGB(255, 128, 0)    ),
    'green_arrow':  (stc.STC_MARK_ARROW,        RGB(0, 0, 0),       RGB(32, 255, 32)    ),
    'dots':         (stc.STC_MARK_DOTDOTDOT,       )}





# .d8888. d888888b db    db db      d88888b d8888b. d888888b d88888b db    db d888888b 
# 88'  YP `~~88~~' `8b  d8' 88      88'     88  `8D `~~88~~' 88'     `8b  d8' `~~88~~' 
# `8bo.      88     `8bd8'  88      88ooooo 88   88    88    88ooooo  `8bd8'     88    
#   `Y8b.    88       88    88      88~~~~~ 88   88    88    88~~~~~  .dPYb.     88    
# db   8D    88       88    88booo. 88.     88  .8D    88    88.     .8P  Y8.    88    
# `8888Y'    YP       YP    Y88888P Y88888P Y8888D'    YP    Y88888P YP    YP    YP    


class StyledText(stc.StyledTextCtrl):

    _style_cache = [None]



    def __init__(self, *args, **kwargs):
        stc.StyledTextCtrl.__init__(self, *args, **kwargs)

        #self.SetScrollWidth(800)
        self.SetScrollWidthTracking(True)

        self._styles = PlatformStyle()
        self._styles.update({
            'fore'   : '#ffffff',
            'back'   : '#000002',
            'calltip' : '#FFFF00',
            'calltipback' : '#004000',
        })

        self.StyleSetSpec(
            stc.STC_STYLE_DEFAULT,
            "face:%(mono)s,size:%(size)d,fore:%(fore)s,back:%(back)s" % self._styles
        )
        self.StyleClearAll()
        self.SetSelForeground(True, SYS_COLOUR(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.SetSelBackground(True, SYS_COLOUR(wx.SYS_COLOUR_HIGHLIGHT))


        # Define markers
        self.marker = {}        
        self.mark_number = {}
        number = 0
        for name, params in MARKERS.items():
            number+=1
            self.MarkerDefine(number, *params)
            self.mark_number[name] = number
        

    def write(self, text):
        if len(text)>80:

            if text[0] in ("(","[","{"):
                text = ',\n'.join(text.split(','))

                #o = json.loads(text)
                #text = json.dumps(o, indent=4, sort_keys=True)

        wx.CallAfter(self.echo, 
            text = text, 
            lf = False, 
        )



    # d88888b  .o88b. db   db  .d88b.  
    # 88'     d8P  Y8 88   88 .8P  Y8. 
    # 88ooooo 8P      88ooo88 88    88 
    # 88~~~~~ 8b      88~~~88 88    88 
    # 88.     Y8b  d8 88   88 `8b  d8' 
    # Y88888P  `Y88P' YP   YP  `Y88P'


    def echo(self, text=None, style=None, lf=True, marker=None, icon=None):
        
        if not style in self._style_cache:
            self._style_cache.append(style)
            self.StyleSetSpec(len(self._style_cache)-1, style)

        if text is None: text=""

        line = self.MarkerLineFromHandle(self.marker["prompt"])-1
        pos = self.GetLineEndPosition(line)

        self.InsertText(pos, '%s%s' % (text,'\n' if lf else '') )

        if style is not None:
            length = len(text)
            self.StartStyling(pos=pos, mask=0xFF)
            self.SetStyling(length=length, style=self._style_cache.index(style))




       
        mark = None        
        if icon is not None:
            if icon in self.mark_number.keys():
                markerNumber = self.mark_number[icon]
            else:
                markerNumber = 0
            mark = self.MarkerAdd(line, markerNumber)

        if marker is not None:
            self.marker[marker] = self.MarkerAdd(line) if mark is None else mark            
            
            #Si ya existe modificar linea



        
        #if br: 
        #    line = self.MarkerLineFromHandle(self.marker["prompt"])
        #    pos = self.GetLineIndentPosition(line)
        #    self.InsertText(pos, '\r\n' )
        
        self.EnsureCaretVisible()

        








class Console(StyledText):
    ''' See https://docs.wxpython.org/wx.stc.StyledTextCtrl.html
    '''

    __zoom = 0
    __find = ""



    def OnWrap(self, e):
        self.SetWrapMode( not self.GetWrapMode() )


    def OnSmaller(self, e): 
        self.__zoom-=1
        self.SetZoom(self.__zoom)


    def OnBigger(self, e): 
        self.__zoom+=1
        self.SetZoom(self.__zoom)


    def OnGoUp(self, e): 
        self.GotoLine( self.MarkerPrevious( self.GetCurrentLine()-1, 0xFF ) )


    def OnGoDown(self, e):
        self.GotoLine( self.MarkerLineFromHandle( self.marker["prompt"] ) )
        self.LineEnd()

    def OnFind(self, e):
        dialog = wx.TextEntryDialog( None, "Search", "Find", self.__find )
        dialog.ShowModal()
        value = dialog.GetValue()
        if value=="": return
        self.__find = value
        self.CharRight()
        self.SearchAnchor()
        self.SearchNext(0xFF, value)


    def OnGoBack(self, e): 
        if self.__find=="": return
        self.CharLeft()
        self.SearchAnchor()
        self.SearchPrev(0xFF, self.__find)
        self.EnsureCaretVisible()

    def OnGoForward(self, e):
        if self.__find=="": return
        self.CharRight()
        self.SearchAnchor()
        self.SearchNext(0xFF, self.__find)
        self.EnsureCaretVisible()
  

    def Mark(self, line, icon):
        if not icon in self.mark_number.keys(): return
        return self.MarkerAdd(line, self.mark_number[icon])
    


    def __init__(self, *args, **kwargs):
        StyledText.__init__(self, *args, **kwargs)

        self.SetMarginType(1, stc.STC_MARGIN_SYMBOL)
        self.SetMarginWidth(1, 20)
        self.SetCaretStyle(2)
        self.SetCaretForeground(wx.Colour(0, 255, 0))


        # A blank line before prompt, echo writes here
        self.AddText("\n")
        
        # Create a propmt line
        try:
            self.prompt = sys.ps1
        except AttributeError:
            self.prompt = ">>> "
        self.AddText(self.prompt)
        self.marker["prompt"] = self.MarkerAdd(1, self.mark_number["prompt"])
        
        #https://wxpython.org/Phoenix/docs/html/wx.stc.StyledTextEvent.html#wx-stc-styledtextevent
       
        #Check if enter pressed
        self.Bind(stc.EVT_STC_CHARADDED, self.OnLine)

        self.Bind(stc.EVT_STC_UPDATEUI, self.OnUpdateUI)
        #self.Bind(stc.EVT_STC_DWELLEND, self.OnKey)
        #self.Bind(stc.EVT_STC_HOTSPOT_CLICK, self.OnKey)
        #self.Bind(stc.EVT_STC_INDICATOR_CLICK, self.OnKey)
        

        #self.Bind(stc.EVT_STC_KEY, self.OnKey)
        self.Bind(stc.EVT_STC_MODIFIED, self.OnModified)

        self._correcting = False

    def GotoPrompt(self):
        line = self.MarkerLineFromHandle(self.marker["prompt"])
        self.GotoPos( self.GetLineIndentPosition(line)+len(self.prompt))



    def OnModified(self, event):
        prompt = self.MarkerLineFromHandle(self.marker["prompt"])
        modification = event.GetModificationType()

        # ugly _correcting trick breaks vicius circle
        if self._correcting and modification in [18, 8209, 8210]: 
            self._correcting=False
            wx.CallAfter(self.GotoPos, self.GetLineIndentPosition(prompt)+len(self.prompt) )
            return

        pos = self.GetLineEndPosition(prompt-1)
        mod = event.GetPosition()

        if mod>pos and mod<=(pos+len(self.prompt)):
            
            if modification in [18, 8210]: 
                self._correcting=True
                wx.CallAfter( self.AddText, event.GetText() )
            
            if event.GetModificationType() in [8209]:
                self._correcting=True
                wx.CallAfter( self.DeleteBackNotLine )
            
                

       



    # d88888b d8b   db d888888b d88888b d8888b. 
    # 88'     888o  88 `~~88~~' 88'     88  `8D 
    # 88ooooo 88V8o 88    88    88ooooo 88oobY' 
    # 88~~~~~ 88 V8o88    88    88~~~~~ 88`8b   
    # 88.     88  V888    88    88.     88 `88. 
    # Y88888P VP   V8P    YP    Y88888P 88   YD 


    def Enter1(self, cmd):
        ''' Send code to interpreter  
        ''' 
        raise Exception("Not implemented - Must override")



    def OnLine(self, event):

        """ Falta borrar resto y limpiar bien \r\n
        """

        if event.GetKey() == 13:
            last = self.GetCurrentLine()-1
            cmd = self.GetLine(last).strip()
            
            if cmd[0:len(self.prompt)]!=self.prompt: 
                return event.Skip()
            
            self.DeleteBack()
            cmd = self.GetLine(self.GetCurrentLine()).strip()[len(self.prompt):]
            self.echo('\n'+self.prompt+cmd,"fore:#ffff00,bold")
            self.GotoPrompt()
            #self.DelLineRight()
            pos = self.GetCurrentPos()
            self.DeleteRange(pos, self.GetLength()-pos)
            self.Enter(cmd)
            



    def OnUpdateUI(self, event):
        ''' TODO: Detect UP Key
        '''
        return
        for prop in dir(event):
            if len(prop)<3: continue
            if prop[0:3]!="Get": continue
            print("%s %s " % (prop, getattr(event, prop)() ))
        print("***")
