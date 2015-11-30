#!/usr/bin/python

import wx
import os
import config
import random

class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self, cf, icon = None):
        super(TaskBarIcon, self).__init__()
        self.__config__ = cf
        if(icon != None):
            if(os.path.isfile(icon)):
                self.SetIcon(wx.IconFromBitmap(wx.Bitmap(icon)), self.__config__.result['name'])
            else:
                self.SetIcon(wx.EmptyIcon(), self.__config__.result['name'])
        else:
            self.SetIcon(wx.EmptyIcon(), self.__config__.result['name'])
        
        msg = self.__config__.findCondition('startup')[0]
        if msg != []:
            self.ShowBalloon(self.__config__.result['name'], self.__config__.chooseMessage(msg), 3000, wx.ICON_INFORMATION)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        item = wx.MenuItem(menu, -1, 'Exit')
        menu.Bind(wx.EVT_MENU, self.on_exit, id = item.GetId())
        menu.AppendItem(item)
        return menu

    def on_exit(self, event):
        msg = self.__config__.findCondition('end')[0]
        if msg != []:
            self.ShowBalloon(self.__config__.result['name'], self.__config__.chooseMessage(msg), 3000, wx.ICON_INFORMATION)
        wx.CallAfter(self.Destroy)