#!/usr/bin/python

import wx
import os

# User-defined modules here
import taskicon
import config

def main():
    # Read config file
    cf = config.configFile(r'.\config.xml')
    # Parse XML
    cf.parse()
    # Create app
    app = wx.App()

    # Parsing error
    if cf.error:
        wx.MessageDialog(None, 'An error occurred when parsing the XML file.', 'Meidochan');
        return

    # Create tray icon
    tray = taskicon.TaskBarIcon(cf, icon = None) # During beta test icon is empty
    # Mainloop
    app.MainLoop()

if __name__ == '__main__':
    main()
