from collections import namedtuple

import numpy as np
import pandas as pd

from . import critical_power, heartrate_models, w_prime_balance


def mean_max_power(power):
    mmp = []

    for i in range(len(power)):
        mmp.append(power.rolling(i+1).mean().max())

    return pd.Series(mmp)


DataPoint = namedtuple('DataPoint', ['index', 'value'])


def mean_max_bests(power, duration, amount):
    moving_average = power.rolling(duration).mean()
    length = len(moving_average)
    mmp = []

    for _ in range(amount):
        if moving_average.isnull().all():
            mmp.append(DataPoint(np.nan, np.nan))
            continue

        max_value = moving_average.max()
        max_index = moving_average.idxmax()
        mmp.append(DataPoint(max_index, max_value))

        # Set moving averages that overlap with last found max to np.nan
        overlap_min_index = max(0, max_index-duration)
        overlap_max_index = min(length, max_index+duration)
        moving_average.loc[overlap_min_index:overlap_max_index] = np.nan

    return pd.Series(mmp)


def weighted_average_power(power):
    wap = power.rolling(30).mean().pow(4).mean().__pow__(1/4)
    return wap


def power_per_kg(power, weight):
    ppkg = power / weight
    return ppkg
