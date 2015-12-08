#!/usr/bin/python

import wx
import os
import random

# User-defined modules here
import config
import timer

class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self, cf, icon = None):
        super(TaskBarIcon, self).__init__()
        self.__config__ = cf
        if(icon != None):
            if(os.path.isfile(icon)): # Icon file
                try:
                    self.SetIcon(wx.IconFromBitmap(wx.Bitmap(icon)), self.__config__.result['name']) # Set icon
                    # Otherwise, set an empty icon
                except:
                    self.SetIcon(wx.EmptyIcon(), self.__config__.result['name'])
            else:
                self.SetIcon(wx.EmptyIcon(), self.__config__.result['name'])
        else:
            self.SetIcon(wx.EmptyIcon(), self.__config__.result['name'])

        # Choose an startup message
        msg = random.choice(self.__config__.findMessageByCondition({'startup': True}))
        if msg != []:
            self.show(msg.chooseMessage())

        # Set a timer
        self.__timer__ = timer.timer(self.__config__, self)
        self.__timer__.start()

    def CreatePopupMenu(self):
        menu = wx.Menu()
        item = wx.MenuItem(menu, -1, 'Exit') # Only one option
        menu.Bind(wx.EVT_MENU, self.on_exit, id = item.GetId())
        menu.AppendItem(item)
        return menu

    def Destroy(self):
        self.__timer__.stop()
        # Choose an end message
        msg = random.choice(self.__config__.findMessageByCondition({'end': True}))
        if msg != []:
            self.show(msg.chooseMessage())
        super(TaskBarIcon, self).Destroy()

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)

    def show(self, content):
        self.ShowBalloon(self.__config__.result['name'], content, config.BALLOON_TIME, wx.ICON_INFORMATION)
