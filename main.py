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

# Get the last times
# E.g.
# We need to get the last 20 minutes to be able
# to calculate the 20 last averages/minute

def get_last_time(items, time_type, n):
    '''Returns the `n` last `time_type` as a list before
    the last entry of `item`.
    '''

    return [[y.index[-1] - Minute(x) for x in range(20)] for y in items]
