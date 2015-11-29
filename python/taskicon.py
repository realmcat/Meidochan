#!/usr/bin/python

import wx
import os

class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self, conf, icon = None):
        super(TaskBarIcon, self).__init__()
        if(icon != None):
            if(os.path.isfile(icon)):
                self.SetIcon(wx.IconFromBitmap(wx.Bitmap(icon)), conf['name'])
            else:
                self.SetIcon(wx.EmptyIcon(), conf['name'])
        else:
            self.SetIcon(wx.EmptyIcon(), conf['name'])

    def CreatePopupMenu(self):
        menu = wx.Menu()
        item = wx.MenuItem(menu, -1, 'Exit')
        menu.Bind(wx.EVT_MENU, self.on_exit, id = item.GetId())
        menu.AppendItem(item)
        return menu

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)