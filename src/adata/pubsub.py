#adata.pubsub
''' 
Publisher Subscriber framework
'''
import wx
import traceback
from wx.lib.pubsub import pub


publish = pub.sendMessage


def echo(text, color=None, lf=True, marker=None, icon=None): # no optional **kwargs
    """ 
    This is the main print function for a adata application
    Top window's OnEcho is suscribed to the channel. 
    """
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


class Output():
    def write(self, line): echo(line)
    def flush(self): pass





    
def subscribe(topic):
    ''' Create a subscription decorator for this topic
    '''
    app = wx.GetApp()
    def subscribe_decorator(function):
        ''' Subscribe to the topic. Beware args
        '''
        

        pub.subscribe(function, topic)
        print("SUBBBBBBBBB")

        #def subscription():
        #    print("XXXXXXXXXXXXXXXXX")
        #    return "Subscription topic '%s' -> %s" % (topic, function.__name__)
        #print(subscription())
        
        return function

    return subscribe_decorator