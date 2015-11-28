#!/usr/bin/python

import wx
import os

TRAY_TOOLTIP = 'Meido Project'

class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self, icon = None):
        super(TaskBarIcon, self).__init__()
        if(icon != None):
            if(os.path.isfile(icon)):
                self.SetIcon(wx.IconFromBitmap(wx.Bitmap(icon)), TRAY_TOOLTIP)
            else:
                self.SetIcon(wx.EmptyIcon(), TRAY_TOOLTIP)
        else:
            self.SetIcon(wx.EmptyIcon(), TRAY_TOOLTIP)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        item = wx.MenuItem(menu, -1, 'Exit')
        menu.Bind(wx.EVT_MENU, self.on_exit, id = item.GetId())
        menu.AppendItem(item)
        return menu

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)