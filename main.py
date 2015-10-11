'''All the code in this file is written by me (Fredrik A. Madsen-Malmo).
Feel free to use it however you'd like.
The code is written for the ServerStatus project (v2.1).
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import gui_logic

__author__ = 'FredrikAugust@GitHub'

# Configure matplotlib
font = {
    'family': 'monospace',
    'size': 10
}

# Apply settings
plt.rc('font', **font)

# Start importing files
loads, temps = [pd.read_csv(
                    '%s.csv' % x, header=None, index_col=0, parse_dates=True
                ) for x in ['loads', 'temps']]

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

# All the types of 'things' that should get plotted
items = gui_logic.decode_intervals(loads, temps)

# Get the last times from each of the different "time-types"
means = [get_mean(item, time_type, n) for item, time_type, n in items]

# For each "mean-set"
for mean in means:
    # Create figure and axis objects
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # Set height and width
    fig.set_figheight(7)
    fig.set_figwidth(12)

    # Set axis labels
    ax.set_xlabel(mean['name'].split(' - ')[1])
    ax.set_ylabel(mean['name'].split(' - ')[0])

    # Add grid for more pleasurable viewing experience
    ax.grid()

    # Set a title
    ax.set_title(mean['name'])

    # Plot with dates on x axis
    ax.plot(mean['items'][0], mean['items'][1], 'o-')

    # Invert x-axis so that newest is to the left
    # ax.invert_xaxis()

    # Save the figure, implement naming system
    plt.savefig('public/%s.png' % mean['name'].replace(' ', ''),
                dpi=200, bbox_inches='tight')

    # Cleanup
    del fig
    del ax
