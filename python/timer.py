#!/usr/bin/python

import wx

# User-defined modules here
import taskicon

TIMER_INTERVAL = 100 # Interval should be less than 1000 but not be too small in order to save resource

class timer(wx.Timer):
    def __init__(self, cf, taskicon):
        super(timer, self).__init__()
        self.__config__ = cf
        self.__taskicon__ = taskicon

        # A temporary list storing the message that is disabled temporarily
        self.__paused__ = []

    def Notify(self):
        messages = self.__config__.findMessageByCondition()
        if len(messages) > 0:
            for msg in messages:
                if not msg in self.__paused__:
                    self.__taskicon__.show(msg.chooseMessage())
                    self.__paused__.append(msg) # Put this message in list temporarily
        else:
            self.__paused__ = [] # Once no messages should be triggered, clear list

    def start(self):
        self.Start(TIMER_INTERVAL)

    def stop(self):
        self.Stop()
