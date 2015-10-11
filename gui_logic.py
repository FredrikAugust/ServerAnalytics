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

    # Create and show a modal
    dialog = wx.MessageDialog(None, 'Save successful.')
    dialog.ShowModal()


def decode_intervals(loads, temps):
    """This will return the python-ified version of the json objects that
    contain the interval
    """

    intervals = None

    with open('cfg/intervals.json', 'r') as file:
        intervals = json.load(file)

    print 'Loaded Python object from JSON file'

    main_intervals = []

    for interval in intervals:
        main_intervals.append([loads, interval['name'], interval['amt']])
        main_intervals.append([temps, interval['name'], interval['amt']])

    print 'Created main.py compatible array.'

    return main_intervals
