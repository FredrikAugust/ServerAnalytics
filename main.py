'''All the code in this file is written by me (Fredrik A. Madsen-Malmo).
Feel free to use it however you'd like.
The code is written for the ServerStatus project (v3).
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pandas.tseries.offsets import Hour, Minute, Week, Month

__author__ = 'Fredrik A. Madsen-Malmo'

# Start importing files

loads, temps = [pd.read_csv(
                    '%s.csv' % x, header=None, index_col=0, parse_dates=True
                ) for x in ['loads', 'temps']]

def get_means(time_type, n):
    '''This function gets the `n` last `time_type` and calculates
    the mean value of said selection.
    '''
    last_times = [[y.index[-1] - time_type(x) for x in range(n)] for y in [loads, temps]]

    load_timed = [loads.ix[x : x + time_type(1)] for x in last_times[0]]
    temp_timed = [temps.ix[x : x + time_type(1)] for x in last_times[1]]

    return [[[x.index[0] for x in load_timed], [x.mean() for x in load_timed]],
            [[x.index[0] for x in temp_timed], [x.mean() for x in temp_timed]]

# Get the last times from each of the different "time-types"
means = [get_means(time_type, n) for time_type, n in [[Minute, 20], [Hour, 10]]], [Week, 5], [MonthBegin, 4]]]

