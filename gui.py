"""This is where I will work with GUI-related stuff. I do know the code
is not exactly well-written, but that is because this is my first ever
project with wxpython
"""

import wx
import json
import threading

# This is another file
import gui_classes

__author__ = 'FredrikAugust@GitHub'

# Create wx application
app = wx.App()

# Create main frame, this is like Window in tkinter
frame = wx.Frame(None, -1, 'Configuration')
