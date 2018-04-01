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




class StyledText(stc.StyledTextCtrl):
    ''' 
    Basic scintilla text control with styles, write and echo methods 

    See https://docs.wxpython.org/wx.stc.StyledTextCtrl.html
    '''

    _style_cache = [None]



    def echo(self, text=None, style=None, lf=True, marker=None, icon=None):
        ''' The print method
        '''
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
            #TODO: Modify a previously marked line (EX: Task... [OK-1:21] )
 
        self.EnsureCaretVisible()

        

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



    def __init__(self, *args, **kwargs):
        '''Initialize stc.StyledTextCtrl and set marker and style specs.

        See stc.StyledTextCtrl documentation.
        '''
        stc.StyledTextCtrl.__init__(self, *args, **kwargs)

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
        





#  .o88b.  .d88b.  d8b   db .d8888.  .d88b.  db      d88888b 
# d8P  Y8 .8P  Y8. 888o  88 88'  YP .8P  Y8. 88      88'     
# 8P      88    88 88V8o 88 `8bo.   88    88 88      88ooooo 
# 8b      88    88 88 V8o88   `Y8b. 88    88 88      88~~~~~ 
# Y8b  d8 `8b  d8' 88  V888 db   8D `8b  d8' 88booo. 88.     
#  `Y88P'  `Y88P'  VP   V8P `8888Y'  `Y88P'  Y88888P Y88888P 


class Console(StyledText):
    '''stc.StyledTextCtrl Styled text window with an input prompt.

        :param args: ``wx.stc.StyledTextCtrl``
        :type args: parameters

    '''

    __history = []
    __history_index = -1
    __zoom = 0
    __find = ""

    __special_keys = [
        wx.WXK_LEFT, 
        wx.WXK_UP, 
        wx.WXK_RIGHT, 
        wx.WXK_DOWN,
        wx.WXK_RETURN, 
        wx.WXK_TAB, 
        wx.WXK_BACK, 
        wx.WXK_DELETE
    ]


    def __init__(self, *args, **kwargs):
        StyledText.__init__(self, *args, **kwargs)

        self.SetMarginType(1, stc.STC_MARGIN_SYMBOL)
        self.SetMarginWidth(1, 20)
        self.SetCaretStyle(2)
        self.SetCaretForeground(wx.Colour(0, 255, 0))

        self.AddText("\n")  # A blank line before prompt, echo always writes here
        
        try:
            self.prompt = sys.ps1 # Create a prompt 
        except AttributeError:
            self.prompt = ">>> "

        self.AddText(self.prompt)
        self.marker["prompt"] = self.MarkerAdd(1, self.mark_number["prompt"])
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)



    def GoPrompt(self, text=None):
        '''Move cursor to propmt and optionally set the command text
        
        :param text: Optional command
        :type text: string
        '''
        line = self.MarkerLineFromHandle(self.marker["prompt"])
        pos = self.GetLineIndentPosition(line)+len(self.prompt)
        self.GotoPos( pos )
        if text is not None:
            self.DeleteRange(pos, self.GetLength()-pos)
            if text!="": 
                self.AddText(text)



    def Enter(self, cmd):
        '''Override to send code somewhere 
        
        :param cmd:  A command line.
        :type cmd: string
        ''' 
        raise Exception("Not implemented - You must override me")



    def OnKeyDown(self, event):
        '''Key pressed event handler

        If line is not prompt, does nothing. Else:

            - Avoid prompt symbol modification
            - Up / Down to navigate history
            - Send code on Enter

        :param event:  Required event information.
        :type event: ``wx.Event``
        '''
        line_current = self.GetCurrentLine()
        line_prompt = self.MarkerLineFromHandle(self.marker["prompt"])

        if line_current!=line_prompt: 
            return event.Skip()

        pos_prompt = self.GetLineIndentPosition(line_prompt)
        pos = self.GetCurrentPos()

        if pos-pos_prompt<len(self.prompt): # U can't touch this
            self.GoPrompt()
            return 

        keycode = event.GetKeyCode()
        if not keycode in self.__special_keys:  # Not interested
            return event.Skip()
        
        if keycode in [wx.WXK_LEFT, wx.WXK_BACK]:
            if (pos-pos_prompt)==len(self.prompt): # Don't go there
                return  

        if keycode==wx.WXK_RETURN:    
            # Command
            cmd = self.GetLine(line_prompt)[len(self.prompt):].strip()
            if cmd=="": return
            
            self.echo()
            self.echo(self.prompt+cmd,"fore:#ffff00,bold")
            self.GoPrompt('')
            self.__history.insert(0, cmd)
            self.__history_index = -1
            self.Enter(cmd)
            return

        # Command history
        if keycode in [wx.WXK_UP, wx.WXK_DOWN]:
            
            if keycode==wx.WXK_UP and self.__history_index<len(self.__history)-1: 
                self.__history_index+=1
            
            if keycode==wx.WXK_DOWN and self.__history_index>0: 
                self.__history_index-=1
            
            if self.__history_index<0: return

            self.GoPrompt( self.__history[self.__history_index] )
            return

        event.Skip()
            






    def ToggleWrapMode(self, event=None):
        '''Toggle text wrap mode

        :param event: Optional
        :type event: ``wx.Event``
        :return: self.GetWrapMode
        :rtype: boolean
        '''
        state = not self.GetWrapMode()
        self.SetWrapMode( state )
        return state


    def FontSmaller(self, e=None): 
        '''Toggle text wrap mode

        :param event: Optional
        :type event: ``wx.Event``
        :return: zoom level
        :rtype: int
        '''
        self.__zoom -= 1
        self.SetZoom( self.__zoom )
        return self.__zoom

    def FontBigger(self, e=None): 
        '''Toggle text wrap mode

        :param event: Optional
        :type event: ``wx.Event``
        :return: zoom level
        :rtype: int
        '''
        self.__zoom += 1
        self.SetZoom( self.__zoom )
        return self.__zoom


    def GoPreviousMarker(self, e=None): 
        '''Go to previous marker

        :param event: Optional
        :type event: ``wx.Event``
        :return: zoom level
        :rtype: int
        '''
        self.GotoLine( self.MarkerPrevious( self.GetCurrentLine()-1, 0xFF ) )


    def GoPromptHandler(self, e):
        '''Go to prompt *****

        :param event: Optional
        :type event: ``wx.Event``
        :return: line
        :rtype: int
        '''
        line = self.MarkerLineFromHandle( self.marker["prompt"] )
        self.GotoLine( line )
        self.LineEnd()
        return line


    def SearchBox(self, e=None):
        '''Find text

        :param event: Optional
        :type event: ``wx.Event``
        '''
        dialog = wx.TextEntryDialog( None, "Search", "Find", self.__find )
        dialog.ShowModal()
        value = dialog.GetValue()
        if value=="": return
        self.__find = value
        self.CharRight()
        self.SearchAnchor()
        self.SearchNext(0xFF, value)


    def SearchPreviousHandler(self, e=None): 
        '''Search previous occurence

        :param event: Optional
        :type event: ``wx.Event``
        '''
        if self.__find=="": return
        self.CharLeft()
        self.SearchAnchor()
        self.SearchPrev(0xFF, self.__find)
        self.EnsureCaretVisible()



    def SearchNextHandler(self, e=None):
        '''Search next occurence

        :param event: Optional
        :type event: ``wx.Event``
        '''
        if self.__find=="": return
        self.CharRight()
        self.SearchAnchor()
        self.SearchNext(0xFF, self.__find)
        self.EnsureCaretVisible()

  

    def Mark(self, line, icon):
        '''Set marker 

        :param line: Line number
        :type line: int
        :param icon: mark_number dictionary key
        :type icon: string
        :return: Marker ID
        :rtype: int
        '''        
        if not icon in self.mark_number.keys(): return
        return self.MarkerAdd(line, self.mark_number[icon])
    



