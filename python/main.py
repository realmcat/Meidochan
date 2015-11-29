#!/usr/bin/python

import wx
import os
import sys
import random

sys.path.append(os.getcwd())

# User-defined modules here
import taskicon
import config
# User-defined modules end

def main():
    cf = config.configFile(r'.\config.xml')
    conf = cf.parse()
    app = wx.App()
    if cf.error:
        print conf
        wx.MessageDialog(None, 'An error occurred when parsing the XML file.', 'Meidochan');
        return

    tray = taskicon.TaskBarIcon(conf)
    
    for msg in conf['messages']:
        found = False
        for cond in msg['conditions']:
            if cond.type == 'startup':
                found = True
                break
        if found:
            tray.ShowBalloon(conf['name'], random.choice(msg['contents']).replace('{NAME}', conf['name']), 3000, wx.ICON_INFORMATION)
    app.MainLoop()
    
if __name__ == '__main__':
    main()