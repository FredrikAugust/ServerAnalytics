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

def get_last_time(item, time_type, n=20):
    '''Returns the `n` last `time_type` as a list before
    the last entry of `item`.
    '''

    return [[item.index[-1] - time_type(x) for x in range(n)]]
