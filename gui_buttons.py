"""This is where I will put the code regarding settings-menus."""

import wx
import wx.lib.intctrl
import threading

import gui_logic

__author__ = 'FredrikAugust@GitHub'


class BaseSettings(wx.Frame):
    def __init__(self, parent, title, *args, **kwargs):
        wx.Frame.__init__(self, parent, -1, title,
                          style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION |
                          wx.CLOSE_BOX, size=wx.Size(300, 450))

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

        # This is the tooltip helper area
        self.SetStatusText('General Settings Menu')

        # Set grid layout
        sizer = wx.GridBagSizer(2, 6)

        # Main heading
        settings = wx.StaticText(self.mainPanel, label='General Settings')

        # Sep.
        sep = wx.StaticLine(self.mainPanel)

        # Inputs
        dpi_text = wx.StaticText(self.mainPanel, label='DPI')
        self.dpi_input = wx.lib.intctrl.IntCtrl(self.mainPanel, min=100, max=2000,
                                                allow_none=False, value=200)

        dash_cap_style_text = wx.StaticText(self.mainPanel,
                                            label='Dash cap-style')
        self.dash_cap_style_choices = ['butt', 'round', 'projecting']
        self.dash_cap_style_input = wx.Choice(self.mainPanel,
                                              choices=self.dash_cap_style_choices)

        dash_join_style_text = wx.StaticText(self.mainPanel,
                                             label='Dash join-style')
        self.dash_join_style_choices = ['miter', 'round', 'bevel']
        self.dash_join_style_input = wx.Choice(self.mainPanel,
                                               choices=self.dash_join_style_choices)

        xkcd_text = wx.StaticText(self.mainPanel, label='XKCD-style')
        self.xkcd_input = wx.CheckBox(self.mainPanel)

        save = wx.Button(self.mainPanel, label='Save changes')

        input_text_flags = wx.TOP | wx.LEFT | wx.BOTTOM
        input_flags = wx.TOP | wx.RIGHT | wx.BOTTOM | wx.EXPAND

        # Append everything to the grid layout
        sizer.Add(settings, pos=(0, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM,
                  border=10)  # Settings text

        sizer.Add(sep, pos=(1, 0), span=(1, 2),
                  flag=wx.EXPAND | wx.BOTTOM, border=10)  # Separator line

        sizer.Add(dpi_text, pos=(2, 0), span=(1, 1), flag=input_text_flags,
                  border=10)  # dpi text
        sizer.Add(self.dpi_input, pos=(2, 1), span=(1, 1), flag=input_flags,
                  border=10)  # dpi input

        sizer.Add(dash_cap_style_text, pos=(3, 0), span=(1, 1),
                  flag=input_text_flags, border=10)  # dash cap-style text
        sizer.Add(self.dash_cap_style_input, pos=(3, 1), span=(1, 1),
                  flag=input_flags, border=10)  # dash cap-style input

        sizer.Add(dash_join_style_text, pos=(4, 0), span=(1, 1),
                  flag=input_text_flags, border=10)  # dash join-style text
        sizer.Add(self.dash_join_style_input, pos=(4, 1), span=(1, 1),
                  flag=input_flags, border=10)  # dash join-style input

        sizer.Add(xkcd_text, pos=(5, 0), span=(1, 1),
                  flag=input_text_flags, border=10)  # dash join-style text
        sizer.Add(self.xkcd_input, pos=(5, 1), span=(1, 1),
                  flag=input_flags, border=10)  # dash join-style input

        sizer.Add(save, pos=(6, 0), span=(1, 2),
                  flag=wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM |
                  wx.EXPAND, border=10)

        # Make the second column able to expand since it has the wx.EXPAND flag
        sizer.AddGrowableCol(1)

        # Make sizer in control of assigning the size of elements in panel
        self.mainPanel.SetSizer(sizer)

        # Bind save to the save_to_file function
        save.Bind(wx.EVT_BUTTON, self.OnSave)

    def OnSave(self, event):
        dpi = self.dpi_input.GetValue()
        dash_cap_style = self.dash_cap_style_input.GetCurrentSelection()
        dash_join_style = self.dash_join_style_input.GetCurrentSelection()
        xkcd = self.xkcd_input.GetValue()

        temp_obj = {
            'dpi': dpi,
            'dash_cap_style': self.dash_cap_style_choices[dash_cap_style],
            'dash_join_style': self.dash_join_style_choices[dash_join_style],
            'xkcd': xkcd
        }

        save_t = threading.Thread(target=gui_logic.save_to_file,
                                  args=[temp_obj, 'general'])

        save_t.run()
