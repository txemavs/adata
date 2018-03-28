#!/usr/bin/python
"""
ADATA Main Script

Adata is a frozen framework module

"""

import sys
import adata.main

try:
    import win32api
    import win32com.client as win32
except:
    pass



def run(service=True):

    # The one WX application instance
    app = adata.main.App(
        redirect = False,
        filename = None,
        useBestVisual = True,
        clearSigInt = True
    )
    
    # Redirect errors to Console
    sys.excepthook = adata.excepthook
    
    # Execute script/__auto__ 
    app.Run("__auto__")
    
    if service: 
        app.ReactorLoop()
    else:   
        app.MainLoop() 


if __name__ == '__main__': 
    run()



