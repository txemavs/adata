#adata.pubsub
''' 
Publisher Subscriber framework
'''
import wx
import traceback
from wx.lib.pubsub import pub


'''Send message alias 
'''
publish = pub.sendMessage


def echo(text, color=None, lf=True, marker=None, icon=None): # no optional **kwargs
    '''The Adata console print function sends a pubsub:app.echo message.

    Top window's OnEcho method is suscribed to the channel. 
    '''
    style = None
    if color is not None:
        style = "fore:#%s,bold" % color

    pub.sendMessage('app.echo', 
        text = text, 
        style = style, 
        lf = lf, 
        marker = marker, 
        icon = icon
    )




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




class Output():
    '''Standard output like class using echo.
    '''
    def write(self, line): echo(line)
    def flush(self): pass



    
def subscribe(topic):
    ''' TODO: Create a subscription decorator for this topic
    '''
    app = wx.GetApp()
    def subscribe_decorator(function):
        ''' Subscribe to the topic. Beware args
        '''
        pub.subscribe(function, topic)
        return function

    return subscribe_decorator



