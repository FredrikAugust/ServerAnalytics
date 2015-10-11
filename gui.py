"""This is where I will work with GUI-related stuff. I do know the code
is not exactly well-written, but that is because this is my first ever
project with wxpython
"""

import wx
import threading

from os import system

# This is another file
import gui_main

__author__ = 'FredrikAugust@GitHub'

# Folders-work
system('mkdir cfg/')  # just incase it doesn't exist

# Create wx application
app = gui_main.App(False)

# Start app thread
mainLoop_t = threading.Thread(target=app.MainLoop)

# Start the thread
mainLoop_t.run()
