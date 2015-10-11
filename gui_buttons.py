"""This is where I will put the code regarding settings-menus."""

import wx
import wx.lib.intctrl
import threading

import gui_logic

__author__ = 'FredrikAugust@GitHub'


class BaseSettings(wx.Frame):
    def __init__(self, parent, title, width, height, *args, **kwargs):
        wx.Frame.__init__(self, parent, -1, title,
                          style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION |
                          wx.CLOSE_BOX, size=wx.Size(300, 450))

        menuFile = wx.Menu()

        # This is an entry that shows an about dialog
        menuFile.Append(wx.ID_ABOUT, '&About')

        menuFile.AppendSeparator()

        # Create a new entry in the drop-down which for now is exit
        # the &x means that 'x' is the shortcut to close the app
        menuFile.Append(wx.ID_CLOSE_FRAME, 'E&xit')

        # This is shown in other apps when pressing 'alt'
        menuBar = wx.MenuBar()
        menuBar.Append(menuFile, '&File')

        self.SetMenuBar(menuBar)

        self.CreateStatusBar()

        # This is the tooltip helper area
        self.SetStatusText('%s Settings Menu' % title)

        # Bind dropdown-elements with methods
        # EVT_MENU is an event that is called when activating a menu-element
        # You bind with the ID
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=wx.ID_CLOSE_FRAME)

        self.mainPanel = wx.Panel(self)

        # Set grid layout
        self.sizer = wx.GridBagSizer(width, height)

        # Main heading
        settings = wx.StaticText(self.mainPanel, label='%s Settings' % title)

        # Sep.
        sep = wx.StaticLine(self.mainPanel)

        # Save button
        save = wx.Button(self.mainPanel, label='Save changes')

        # Flags
        text_f = wx.TOP | wx.LEFT | wx.BOTTOM
        input_flags = wx.TOP | wx.RIGHT | wx.BOTTOM | wx.EXPAND

        # Append everything to the grid layout

        # Settings text
        self.sizer.Add(settings, pos=(0, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM,
                       border=10)
        # Separator line
        self.sizer.Add(sep, pos=(1, 0), span=(1, width),
                       flag=wx.EXPAND | wx.BOTTOM, border=10)

        # Save button
        self.sizer.Add(save, pos=(height, 0), span=(1, width), flag=wx.LEFT | wx.RIGHT |
                       wx.TOP | wx.BOTTOM | wx.EXPAND, border=10)

        # Make the second column able to expand since it has the wx.EXPAND flag
        self.sizer.AddGrowableCol(1)

        # Make sizer in control of assigning the size of elements in panel
        self.mainPanel.SetSizer(self.sizer)

        # Flags
        self.text_f = wx.TOP | wx.LEFT | wx.BOTTOM
        self.input_flags = wx.TOP | wx.RIGHT | wx.BOTTOM | wx.EXPAND

        # Bind save to the save_to_file function
        save.Bind(wx.EVT_BUTTON, self.OnSave)

    def OnSave(self, event):
        pass  # Will be rewritten by children

    def OnQuit(self, event):
        self.Close()

    def OnAbout(self, event):
        wx.MessageBox('This is a menu for configuring the \
plots rendered by main.py')


class General(BaseSettings):
    def __init__(self, *args, **kwargs):
        # Run the init from BaseSettings
        super(General, self).__init__(*args, **kwargs)

        # to avoid having to write `self.x` everywhere
        sizer = self.sizer
        mainPanel = self.mainPanel
        text_f = self.text_f
        input_flags = self.input_flags

        # Input text
        dpi = wx.StaticText(mainPanel, label='DPI')
        dash_cap = wx.StaticText(mainPanel, label='Dash cap-style')
        dash_join = wx.StaticText(mainPanel, label='Dash join-style')
        xkcd = wx.StaticText(mainPanel, label='XKCD-style')

        # Choices
        self.dash_cap_choices = ['butt', 'round', 'projecting']
        self.dash_join_choices = ['miter', 'round', 'bevel']

        # Inputs
        self.dpi_input = wx.lib.intctrl.IntCtrl(mainPanel, min=100,
                                                max=2000,
                                                allow_none=False, value=200)
        self.dash_cap_input = wx.Choice(mainPanel,
                                        choices=self.dash_cap_choices)
        self.dash_join_input = wx.Choice(mainPanel,
                                         choices=self.dash_join_choices)
        self.xkcd_input = wx.CheckBox(mainPanel)

        # Append everything to the grid layout

        # DPI
        sizer.Add(dpi, pos=(2, 0), flag=text_f, border=10)
        sizer.Add(self.dpi_input, pos=(2, 1), flag=input_flags, border=10)

        # Dash cap-style
        sizer.Add(dash_cap, pos=(3, 0), flag=text_f, border=10)
        sizer.Add(self.dash_cap_input, pos=(3, 1), flag=input_flags, border=10)

        # Dash join-style
        sizer.Add(dash_join, pos=(4, 0), flag=text_f, border=10)
        sizer.Add(self.dash_join_input, pos=(4, 1), flag=input_flags,
                  border=10)

        # XKCD
        sizer.Add(xkcd, pos=(5, 0), flag=text_f, border=10)
        sizer.Add(self.xkcd_input, pos=(5, 1), flag=input_flags, border=10)

    def OnSave(self, event):
        dpi = self.dpi_input.GetValue()  # Get value in longInt
        # Get index of selection
        dash_cap = self.dash_cap_input.GetCurrentSelection()
        dash_join = self.dash_join_input.GetCurrentSelection()
        # Choice will return -1 if empty on Windows
        if dash_cap < 0:
            dash_cap = 0

        if dash_join < 0:
            dash_join = 0

        # Get bool selection
        xkcd = self.xkcd_input.GetValue()

        # Format nicely
        temp_obj = {
            'dpi': dpi,
            'dash_cap': self.dash_cap_choices[dash_cap],
            'dash_join': self.dash_join_choices[dash_join],
            'xkcd': xkcd
        }

        # Thread that will save with args
        save_t = threading.Thread(target=gui_logic.save_to_file,
                                  args=[temp_obj, 'general'])

        save_t.run()  # Off you go!


class Font(BaseSettings):
    def __init__(self, *args, **kwargs):
        # Run the init from BaseSettings
        super(Font, self).__init__(*args, **kwargs)

        # to avoid having to write `self.x` everywhere
        sizer = self.sizer
        mainPanel = self.mainPanel
        text_f = self.text_f
        input_flags = self.input_flags

        # Texts
        family = wx.StaticText(self.mainPanel, label='Font Family')
        size = wx.StaticText(self.mainPanel, label='Font Size')
        style = wx.StaticText(self.mainPanel, label='Font Style')
        weight = wx.StaticText(self.mainPanel, label='Font Weight')

        # Choices
        self.family_choices = ['serif', 'sans-serif', 'cursive',
                               'fantasy', 'monospace']
        self.size_choices = ['xx-small', 'x-small', 'small', 'medium', 'large',
                             'x-large', 'xx-large']
        self.style_choices = ['normal', 'italic', 'oblique']
        self.weight_choices = ['light', 'normal', 'medium',
                               'semibold', 'bold', 'heavy', 'black']

        # Inputs
        self.family_choice = wx.Choice(mainPanel,
                                       choices=self.family_choices)
        self.size_choice = wx.Choice(mainPanel, choices=self.size_choices)
        self.style_choice = wx.Choice(mainPanel,
                                      choices=self.style_choices)
        self.weight_choice = wx.Choice(mainPanel,
                                       choices=self.weight_choices)

        # Append everything to the grid layout

        # Font-family
        sizer.Add(family, pos=(2, 0), flag=text_f, border=10)
        sizer.Add(self.family_choice, pos=(2, 1), flag=input_flags, border=10)

        # Font-size
        sizer.Add(size, pos=(3, 0), flag=text_f, border=10)
        sizer.Add(self.size_choice, pos=(3, 1), flag=input_flags, border=10)

        # Font-style
        sizer.Add(style, pos=(4, 0), flag=text_f, border=10)
        sizer.Add(self.style_choice, pos=(4, 1), flag=input_flags, border=10)

        # Font-style
        sizer.Add(weight, pos=(5, 0), flag=text_f, border=10)
        sizer.Add(self.weight_choice, pos=(5, 1), flag=input_flags, border=10)

    def OnSave(self, event):
        family = self.family_choice.GetCurrentSelection()
        size = self.size_choice.GetCurrentSelection()
        if size < 0:
            size = 3

        style = self.style_choice.GetCurrentSelection()
        if style < 0:
            style = 0

        weight = self.weight_choice.GetCurrentSelection()
        if weight < 0:
            weight = 2

        # Format nicely
        temp_obj = {
            'family': self.family_choices[family],
            'size': self.size_choices[size],
            'style': self.style_choices[style],
            'weight': self.weight_choices[weight]
        }

        # Thread that will save with args
        save_t = threading.Thread(target=gui_logic.save_to_file,
                                  args=[temp_obj, 'font'])

        save_t.run()  # Off you go!


class Style(BaseSettings):
    def __init__(self, *args, **kwargs):
        # Run the init from BaseSettings
        super(Style, self).__init__(*args, **kwargs)

        # to avoid having to write `self.x` everywhere
        sizer = self.sizer
        mainPanel = self.mainPanel
        text_f = self.text_f
        input_flags = self.input_flags

    def OnSave(self, event):
        print 'TODO: implement save on style'

class Intervals(BaseSettings):
    def __init__(self, *args, **kwargs):
        # Run the init from BaseSettings
        super(Intervals, self).__init__(*args, **kwargs)

        # to avoid having to write `self.x` everywhere
        sizer = self.sizer
        mainPanel = self.mainPanel
        text_f = self.text_f
        input_flags = self.input_flags

    def OnSave(self, event):
        print 'TODO: implement save on style'
