"""This is where I will put the code regarding settings-menus."""

import wx
import wx.lib.intctrl as intctrl
import wx.lib.agw.hyperlink as hl

import threading

import gui_logic

__author__ = 'FredrikAugust@GitHub'


class BaseSettings(wx.Frame):
    '''This is the main class/prototype which all of the GUI _pages_ inherits
    from. Edit here if you're going to add something that should be displayed
    on all of the pages.
    '''

    def __init__(self, parent, title, width, height, *args, **kwargs):
        wx.Frame.__init__(self, parent, -1, title,
                          style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION |
                          wx.CLOSE_BOX, size=wx.Size(400, 450))

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
        wx.MessageBox('This is a menu for configuring the plots from main.py')


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
        xkcd = wx.StaticText(mainPanel, label='XKCD-style')

        # Inputs
        self.dpi_input = intctrl.IntCtrl(mainPanel, min=100,
                                                max=2000,
                                                allow_none=False, value=200)
        self.xkcd_input = wx.CheckBox(mainPanel)

        # Append everything to the grid layout

        # DPI
        sizer.Add(dpi, pos=(2, 0), flag=text_f, border=10)
        sizer.Add(self.dpi_input, pos=(2, 1), flag=input_flags, border=10)

        # XKCD
        sizer.Add(xkcd, pos=(3, 0), flag=text_f, border=10)
        sizer.Add(self.xkcd_input, pos=(3, 1), flag=input_flags, border=10)

    def OnSave(self, event):
        dpi = self.dpi_input.GetValue()  # Get value in longInt

        # Get bool selection
        xkcd = self.xkcd_input.GetValue()

        # Format nicely
        temp_obj = {
            'dpi': dpi,
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
        family = wx.StaticText(mainPanel, label='Font Family')
        size = wx.StaticText(mainPanel, label='Font Size')
        style = wx.StaticText(mainPanel, label='Font Style')
        weight = wx.StaticText(mainPanel, label='Font Weight')

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

        # Text
        sizer.Add(family, pos=(2, 0), flag=text_f, border=10)
        sizer.Add(size, pos=(3, 0), flag=text_f, border=10)
        sizer.Add(style, pos=(4, 0), flag=text_f, border=10)
        sizer.Add(weight, pos=(5, 0), flag=text_f, border=10)

        # Inputs
        sizer.Add(self.family_choice, pos=(2, 1), flag=input_flags, border=10)
        sizer.Add(self.size_choice, pos=(3, 1), flag=input_flags, border=10)
        sizer.Add(self.style_choice, pos=(4, 1), flag=input_flags, border=10)
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

        # Texts
        # s_ is short for style_page. I'm just worried about interference
        # from the main class
        s_height = wx.StaticText(mainPanel, label='Graph height (in)')
        s_width = wx.StaticText(mainPanel, label='Graph width (in)')
        line_style = hl.HyperLinkCtrl(mainPanel, -1, 'Line style', URL='http://matplotlib.org/api/lines_api.html#matplotlib.lines.Line2D.set_linestyle')
        line_color = wx.StaticText(mainPanel, label='Line color')
        line_width = wx.StaticText(mainPanel, label='Line width')

        # Choices
        self.line_style_choices = ['--', '-.', ':', '', '-']
        self.line_color_choices = ['blue', 'green', 'red', 'cyan', 'magenta',
                                   'yellow', 'white', 'black']

        # Inputs
        self.s_height_input = intctrl.IntCtrl(mainPanel, min=1,
                                              max=20,
                                              allow_none=False, value=7)
        self.s_width_input = intctrl.IntCtrl(mainPanel, min=2,
                                             max=40,
                                             allow_none=False, value=12)
        self.line_style_choice = wx.Choice(mainPanel,
                                           choices=self.line_style_choices)
        self.line_color_choice = wx.Choice(mainPanel,
                                           choices=self.line_color_choices)
        self.line_width_input = intctrl.IntCtrl(mainPanel, min=1, max=20,
                                                allow_none=False, value=1)

        # Append everything to the grid layout
        sizer.Add(s_height, pos=(2, 0), flag=text_f, border=10)
        sizer.Add(s_width, pos=(3, 0), flag=text_f, border=10)
        sizer.Add(line_style, pos=(4, 0), flag=text_f, border=10)
        sizer.Add(line_color, pos=(5, 0), flag=text_f, border=10)
        sizer.Add(line_width, pos=(6, 0), flag=text_f, border=10)

        sizer.Add(self.s_height_input, pos=(2, 1), flag=input_flags, border=10)
        sizer.Add(self.s_width_input, pos=(3, 1), flag=input_flags, border=10)
        sizer.Add(self.line_style_choice, pos=(4, 1), flag=input_flags, border=10)
        sizer.Add(self.line_color_choice, pos=(5, 1), flag=input_flags, border=10)
        sizer.Add(self.line_width_input, pos=(6, 1), flag=input_flags, border=10)

    def OnSave(self, event):
        s_height = self.s_height_input.GetValue()
        s_width = self.s_height_input.GetValue()
        line_style = self.line_style_choice.GetCurrentSelection()
        line_color = self.line_color_choice.GetCurrentSelection()
        line_width = self.line_width_input.GetValue()

        # Format nicely
        temp_obj = {
            'height': s_height,
            'width': s_width,
            'line_style': self.line_style_choices[line_style],
            'line_color': self.line_color_choices[line_color],
            'line_width': line_width
        }

        # Thread that will save with args
        save_t = threading.Thread(target=gui_logic.save_to_file,
                                  args=[temp_obj, 'style'])

        save_t.run()  # Off you go!


class Intervals(BaseSettings):
    def __init__(self, *args, **kwargs):
        # Run the init from BaseSettings
        super(Intervals, self).__init__(*args, **kwargs)

        # to avoid having to write `self.x` everywhere
        sizer = self.sizer
        mainPanel = self.mainPanel
        text_f = self.text_f
        input_flags = self.input_flags

        # Texts
        name = wx.StaticText(mainPanel, label='Name')
        freq = hl.HyperLinkCtrl(mainPanel, -1, 'Freq.', URL='http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases')
        amt = wx.StaticText(mainPanel, label='Amt.')

        # Inputs

        # Names
        self.i_name = wx.TextCtrl(mainPanel, value='Realtime')
        self.ii_name = wx.TextCtrl(mainPanel, value='Hour')
        self.iii_name = wx.TextCtrl(mainPanel, value='Day')
        self.iv_name = wx.TextCtrl(mainPanel, value='Week')

        # Freqencies
        self.i_freq = wx.TextCtrl(mainPanel, value='5S')
        self.ii_freq = wx.TextCtrl(mainPanel, value='H')
        self.iii_freq = wx.TextCtrl(mainPanel, value='D')
        self.iv_freq = wx.TextCtrl(mainPanel, value='W-mon')

        # Amounts
        self.i_amt = intctrl.IntCtrl(mainPanel, min=2, max=40, allow_none=False, value=30)
        self.ii_amt = intctrl.IntCtrl(mainPanel, min=2, max=40, allow_none=False, value=24)
        self.iii_amt = intctrl.IntCtrl(mainPanel, min=2, max=40, allow_none=False, value=14)
        self.iv_amt = intctrl.IntCtrl(mainPanel, min=2, max=40, allow_none=False, value=16)

        # This grid uses special Flags
        left_text_f = wx.LEFT | wx.BOTTOM | wx.TOP
        middle_text_f = wx.BOTTOM | wx.TOP
        right_text = wx.RIGHT | wx.BOTTOM | wx.TOP

        left_input_f = left_text_f | wx.EXPAND
        middle_input_f = middle_text_f | wx.EXPAND
        right_input_f = right_text | wx.EXPAND

        # Append everything to the grid layout
        sizer.Add(name, pos=(2, 0), flag=left_text_f, border=10)
        sizer.Add(freq, pos=(2, 1), flag=middle_text_f, border=10)
        sizer.Add(amt, pos=(2, 2), flag=right_text, border=10)

        sizer.Add(self.i_name, pos=(3, 0), flag=left_input_f, border=10)
        sizer.Add(self.i_freq, pos=(3, 1), flag=middle_input_f, border=10)
        sizer.Add(self.i_amt, pos=(3, 2), flag=right_input_f, border=10)

        sizer.Add(self.ii_name, pos=(4, 0), flag=left_input_f, border=10)
        sizer.Add(self.ii_freq, pos=(4, 1), flag=middle_input_f, border=10)
        sizer.Add(self.ii_amt, pos=(4, 2), flag=right_input_f, border=10)

        sizer.Add(self.iii_name, pos=(5, 0), flag=left_input_f, border=10)
        sizer.Add(self.iii_freq, pos=(5, 1), flag=middle_input_f, border=10)
        sizer.Add(self.iii_amt, pos=(5, 2), flag=right_input_f, border=10)

        sizer.Add(self.iv_name, pos=(6, 0), flag=left_input_f, border=10)
        sizer.Add(self.iv_freq, pos=(6, 1), flag=middle_input_f, border=10)
        sizer.Add(self.iv_amt, pos=(6, 2), flag=right_input_f, border=10)

    def OnSave(self, event):
        i = {
            'name': self.i_name.GetValue(),
            'freq': self.i_freq.GetValue(),
            'amt': self.i_amt.GetValue()
        }

        ii = {
            'name': self.ii_name.GetValue(),
            'freq': self.ii_freq.GetValue(),
            'amt': self.ii_amt.GetValue()
        }

        iii = {
            'name': self.iii_name.GetValue(),
            'freq': self.iii_freq.GetValue(),
            'amt': self.iii_amt.GetValue()
        }

        iv = {
            'name': self.iv_name.GetValue(),
            'freq': self.iv_freq.GetValue(),
            'amt': self.iv_amt.GetValue()
        }

        temp_obj = [i, ii, iii, iv]

        # Thread that will save with args
        save_t = threading.Thread(target=gui_logic.save_to_file,
                                  args=[temp_obj, 'intervals'])

        save_t.run()  # Off you go!
