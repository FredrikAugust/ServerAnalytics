'''All the code in this file is written by me (Fredrik A. Madsen-Malmo).
Feel free to use it however you'd like.
The code is written for the ServerStatus project (v3).
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pandas.tseries.offsets import Hour, Minute, Week, MonthBegin

__author__ = 'Fredrik A. Madsen-Malmo'

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

times = {
    'M': 'Minute',
    'H': 'Hour',
    'W': 'Week',
    'M': 'Month'
}

def get_mean(item, time_type, n):
    '''This function gets the `n` last `time_type` and calculates
    the mean value of said selection.
    '''

    # Downsample by n, e.g. Hour
    downsampled = item.resample(time_type)[:n]

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

    return {
        'name': name,
        'items': [
            downsampled.index,
            downsampled.values
        ]
    }

# Get the last times from each of the different "time-types"
means = [get_mean(item, time_type, n) for item, time_type, n in [[Minute, 20], [Hour, 10], [Week, 5], [MonthBegin, 4]]]

###
# TODO:
# Implement naming
###

# For each time
for mean in means:
    # For load/temp inside of this
    for type in mean:
        # Create figure and axis-es
        fig = plt.figure(); ax = fig.add_subplot(1,1,1)

        # Add grid for easier viewing
        ax.grid()

        # Set a title
        ax.set_title('name')

        # Plot with dates on x axis
        ax.plot(type[0], type[1], 'k-')

        # Save the figure, implement naming system
        plt.savefig('name.png', dpi=400, bbox_inches='tight')

        # Cleanup
        del fig
        del ax
