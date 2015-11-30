#!/usr/bin/python

import wx
import os
import sys

sys.path.append(os.getcwd())

# User-defined modules here
import taskicon
import config
# User-defined modules end

def main():
    cf = config.configFile(r'.\config.xml')
    cf.parse()
    app = wx.App()
    if cf.error:
        wx.MessageDialog(None, 'An error occurred when parsing the XML file.', 'Meidochan');
        return

    tray = taskicon.TaskBarIcon(cf)
    app.MainLoop()
    
if __name__ == '__main__':
    main()