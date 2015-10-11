"""This is where I will put all code that has something to do with GUI logic,
mostly regarding saving to the config file.
"""

import json
import wx

__author__ = 'FredrikAugust@GitHub'


def save_to_file(obj, path):
    """This file will save a python obj to a file in JSON format."""
    json_str = json.dumps(obj)

    with open('cfg/%s.json' % path, 'w') as file:
        file.write(json_str)

    dialog = wx.MessageDialog(None, 'Save successful.')
    dialog.ShowModal()
