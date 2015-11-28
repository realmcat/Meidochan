#!/usr/bin/python

import wx
import os
import sys

sys.path.append(os.getcwd())

# User-defined modules here
import taskicon
# User-defined modules end

def main():
    app = wx.App()
    tray = taskicon.TaskBarIcon()
    tray.ShowBalloon('test', '123', 5000, wx.ICON_INFORMATION)
    app.MainLoop()
    
if __name__ == '__main__':
    main()