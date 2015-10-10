"""This is where I will put the code regarding settings-menus."""

import wx

__author__ = 'FredrikAugust@GitHub'


class BaseSettings(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title,
                          style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION |
                          wx.CLOSE_BOX | wx.CLIP_CHILDREN)

        # Create a menu object, this is the drop-down
        menuFile = wx.Menu()

        # This is an entry that shows an about dialog
        menuFile.Append(wx.ID_ABOUT, '&About')

        # Simple separator (line)
        menuFile.AppendSeparator()

        # Create a new entry in the drop-down which for now is exit
        # the &x means that 'x' is the shortcut to close the app
        menuFile.Append(wx.ID_CLOSE_FRAME, 'E&xit')

        # Create the menu bar
        # This is shown in other apps when pressing 'alt'
        menuBar = wx.MenuBar()

        # Add the dropdown to the menuBar
        # The shortcut to open this is to press 'alt+f'
        # specified by the '&F'
        menuBar.Append(menuFile, '&File')

        # Link the frame and the MenuBar obj
        self.SetMenuBar(menuBar)

        # Create/Render the bar
        self.CreateStatusBar()

        # Bind dropdown-elements with methods
        # EVT_MENU is an event that is called when activating a menu-element
        # You bind with the ID
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=wx.ID_CLOSE_FRAME)

        # Set a panel for everything else
        self.mainPanel = wx.Panel(self)

    def OnQuit(self, event):
        self.Close()

    def OnAbout(self, event):
        wx.MessageBox('This is a menu for configuring the \
plots rendered by main.py')


class General(BaseSettings):
    def __init__(self, *args, **kwargs):
        # Run the init from BaseSettings
        super(General, self).__init__(*args, **kwargs)

        # Use self.mainPanel for assigning things
