"""This is where I will write out all of the classes that will be used
for the GUI.
"""

import wx

import gui_buttons

__author__ = 'FredrikAugust@GitHub'


class App(wx.App):
    def OnInit(self):
        '''This is called by the __init__ method of the
        wx.App if I understood correctly, so this is to not
        overwrite that method.
        '''

        # Create the frame
        frame = MainFrame(None, 'Configuration')

        # Set the window/frame to be 'on the top of the screen'
        self.SetTopWindow(frame)

        # Render the window/frame
        frame.Show()

        # This is so the __init__ function knows that this succeeded
        return True


class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        # Create a wx.Frame object
        # Styling:
        # minimize button, normal menus on windows and GTK+, captions,
        # close button, clip children (whatever that is)
        wx.Frame.__init__(self, parent, -1, title,
                          style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION |
                          wx.CLOSE_BOX, size=wx.Size(200, 300))

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

        # This is the tooltip helper area
        self.SetStatusText('Configuration Menu')

        # Bind dropdown-elements with methods
        # EVT_MENU is an event that is called when activating a menu-element
        # You bind with the ID
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=wx.ID_CLOSE_FRAME)

        # ------------
        # ELEMENTS
        # ------------

        # Create the panel to hold the rest of the elements
        panel = wx.Panel(self)

        # This is like a .table in bootstrap iirc
        sizer = wx.GridBagSizer(1, 8)

        # Main heading
        settings = wx.StaticText(panel, label='Settings')

        # Quit button
        quit = wx.Button(panel, label='Quit')

        # Sep. x2
        sep = wx.StaticLine(panel)
        quit_sep = wx.StaticLine(panel)

        # Setting-buttons
        general = wx.Button(panel, label='General')
        font = wx.Button(panel, label='Font')
        style = wx.Button(panel, label='Style')
        intervals = wx.Button(panel, label='Intervals')

        # Set tooltips for buttons
        general.SetToolTip('General settings regarding \
creation of graphs.')
        font.SetToolTip('Settings regarding the appearance of the font')
        style.SetToolTip('Settings regarding the visual properties of a \
graph.')
        intervals.SetToolTip('Settings regarding the interval-settings of \
the graphs.')
        quit.SetToolTip('Quit the application.')

        button_flags = wx.EXPAND | wx.BOTTOM

        # Append everything to the grid layout
        sizer.Add(settings, pos=(0, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM,
                  border=10)  # Settings text

        sizer.Add(sep, pos=(1, 0), span=(1, 1),
                  flag=wx.EXPAND | wx.BOTTOM, border=10)  # Separator line

        sizer.Add(general, pos=(2, 0), flag=button_flags, border=5)  # Buttons
        sizer.Add(font, pos=(3, 0), flag=button_flags, border=5)
        sizer.Add(style, pos=(4, 0), flag=button_flags, border=5)
        sizer.Add(intervals, pos=(5, 0), flag=button_flags, border=5)  # End

        sizer.Add(quit_sep, pos=(6, 0), flag=wx.EXPAND | wx.BOTTOM, border=10)
        sizer.Add(quit, pos=(7, 0), flag=button_flags, border=5)

        # Make the first column able to expand since it has the wx.EXPAND flag
        sizer.AddGrowableCol(0)

        # Make sizer in control of assigning the size of elements in panel
        panel.SetSizer(sizer)

        # -----------
        # BINDINGS
        # -----------

        general.Bind(wx.EVT_BUTTON, self.OnGeneral)
        font.Bind(wx.EVT_BUTTON, self.OnFont)
        style.Bind(wx.EVT_BUTTON, self.OnStyle)
        intervals.Bind(wx.EVT_BUTTON, self.OnIntervals)

        quit.Bind(wx.EVT_BUTTON, self.OnQuit)

    def OnQuit(self, event):
        self.Close()

    def OnAbout(self, event):
        wx.MessageBox('This is an application for configuring the \
plots rendered by main.py')

    def OnGeneral(self, event):
        frame = gui_buttons.General(None, 'General', 2, 4)
        frame.Show()

        return True

    def OnFont(self, event):
        frame = gui_buttons.Font(None, 'Font', 2, 6)
        frame.Show()

        return True

    def OnStyle(self, event):
        frame = gui_buttons.Style(None, 'Style', 2, 8)
        frame.Show()

        return True

    def OnIntervals(self, event):
        frame = gui_buttons.Intervals(None, 'Intervals', 3, 7)
        frame.Show()

        return True
