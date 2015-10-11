'''All the code in this file is written by me (Fredrik A. Madsen-Malmo).
Feel free to use it however you'd like.
The code is written for the ServerStatus project (v2.1).
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from os import system

import gui_logic

__author__ = 'FredrikAugust@GitHub'

# Folders and clean dirs
system('mkdir public/')  # create public/
system('rm public/*')  # del * in public/

# Configure matplotlib
font = gui_logic.get_python_obj('cfg/font.json')

# Apply settings
plt.rc('font', **font)

if gui_logic.get_key('cfg/general.json', 'xkcd'):
    plt.xkcd()  # amazin'.

# Start importing files
loads, temps = [pd.read_csv(
                    '%s.csv' % x, header=None, index_col=0, parse_dates=True
                ) for x in ['loads', 'temps']]

print '[main] Imported loads, temps from csv files'

# This is used to determine the names of the graphs
# I select from this object using the key and use the value as part of the name
# If you look further down you'll see why the strange key-names
times = gui_logic.decode_intervals_names()


def get_mean(item, time_type, n):
    '''This function gDets the `n` last `time_type` and calculates
    the mean value of said selection.
    '''

    # Downsample by n, e.g. Hour
    downsampled = item.resample(time_type)[-n:]

    # Array for the name parameter
    name = []

    # Just to see what the first part of the title should be
    if item.equals(loads):
        name.append('CPU Load')
    else:
        name.append('Temperature')

    # The second part should be e.g. Hour, Minute or Day
    name.append(times[time_type])

    # Create a title e.g. Temperature - Month
    name = ' - '.join(name)

    # Object with name and array with index and values
    return {
        'name': name,
        'items': [
            downsampled.index,
            downsampled.values
        ]
    }

    print '[main] Calculated mean for {}: {}*{}'.format(item, time_type, n)

# All the types of 'things' that should get plotted
items = gui_logic.decode_intervals(loads, temps)

# Get the last times from each of the different "time-types"
means = [get_mean(item, time_type, n) for item, time_type, n in items]

# For each "mean-set"
for mean in means:
    # Create figure and axis objects
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    print '[main] Created figure and subplot'

    h = gui_logic.get_key('cfg/style.json', 'height')
    w = gui_logic.get_key('cfg/style.json', 'width')

    # Set height and width
    fig.set_figheight(h)
    fig.set_figwidth(w)

    print '[main] Set width/height'

    # Set axis labels
    ax.set_xlabel(mean['name'].split(' - ')[1])
    ax.set_ylabel(mean['name'].split(' - ')[0])

    print '[main] Set label for axis-es'

    # Add grid for more pleasurable viewing experience
    ax.grid()

    # Set a title
    ax.set_title(mean['name'])

    print '[main] Set title for graph: %s' % mean['name']

    color = gui_logic.get_key('cfg/style.json', 'line_color')
    line_style = gui_logic.get_key('cfg/style.json', 'line_style')
    line_width = gui_logic.get_key('cfg/style.json', 'line_width')
    marker = gui_logic.get_key('cfg/style.json', 'marker_style')

    # Plot with dates on x axis
    ax.plot(mean['items'][0], mean['items'][1],
            color=color, ls=line_style, lw=line_width, marker=marker)

    print '[main] Created plot'

    dpi = gui_logic.get_key('cfg/general.json', 'dpi')

    print '[main] Got DPI from JSON'

    # Save the figure, implement naming system
    plt.savefig('public/%s.png' % mean['name'].replace(' ', ''),
                dpi=dpi, bbox_inches='tight')

    print '[main] Saved graph'

    # Cleanup
    del fig
    del ax

    print '[main] Deleted objects'
