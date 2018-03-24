# adata.reactor

'''
Twisted Internet Reactor initialization.
'''

from twisted.internet import wxreactor
from twisted.internet.error import ReactorAlreadyInstalledError
try:
    wxreactor.install()
except ReactorAlreadyInstalledError:
    pass
from twisted.internet import reactor




class ReactorMixin(object):
    
    def ReactorLoop(self):
        ''' Run wxpython in a twisted event loop.
        '''
        self.reactor = reactor
        reactor.registerWxApp(self)
        reactor.run()
