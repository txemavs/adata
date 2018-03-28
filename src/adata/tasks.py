#adata.tasks

'''
Threads

TODO: Subprocesses
'''

import wx
import time
import threading
from .pubsub import echo
#import multiprocessing as mp



 
#------------------------------------------------------------------------------
# d888888b  .d8b.  .d8888. db   dD 
# `~~88~~' d8' `8b 88'  YP 88 ,8P' 
#    88    88ooo88 `8bo.   88,8P   
#    88    88~~~88   `Y8b. 88`8b   
#    88    88   88 db   8D 88 `88. 
#    YP    YP   YP `8888Y' YP   YD 
#------------------------------------------------------------------------------

                                 

class Task(threading.Thread):
    ''' Create a new thread and execute the task.
    '''

    def __init__(self, app, task, name=""):
        threading.Thread.__init__(self)
        self.app = app
        self.task = task
        self.name = name
        echo(
            "Task %s starts..." % self.name, 
            "8888ff", 
            marker = self.name, icon = 'blue_arrow')
        self.start()


    def run(self):
        self.task()
        echo(
            "Task %s ends." % self.name, 
            "88ff88", 
            marker = self.name, icon = 'green_arrow')
        



# Define custom wx event for tasks 

EVT_TASK_ID = wx.NewId()

def EVT_TASK(win, func):
    win.Connect(-1, -1, EVT_TASK_ID, func)


class TaskEvent(wx.PyEvent):
    """ Simple event to carry result data.
    """
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_TASK_ID)
        self.data = data









class Watcher(threading.Thread):
    ''' CThread to call a function in a loop
    '''
    def __init__(self, function, period=0.2):
        self.function = function
        self.sleep = period
        threading.Thread.__init__(self)
        self.running = True
        self.start()

    def run(self):
        self.loop()

    def stop(self):
        self.running = False
        
    def loop(self):
        while self.running:
            self.function()
            time.sleep(self.sleep)