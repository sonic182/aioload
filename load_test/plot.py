"""Plot stuffs."""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def render_plot(statics, durations_serie):
    """Render plot."""
    codes = []
    for item in statics:
        codes.append(str(item['code']))

    # mean duration chart
    durations_serie.resample('1s').mean().plot(
        title='median duration per 1s')

    # req per second chart
    plt.figure()
    durations_serie.resample('1s').count().plot(
        title='req/s')

    # codes chart
    plt.figure()
    codes_df = pd.Series(np.array(codes))
    codes_df.value_counts().plot(kind='bar', title='response codes count')
    # codes_df.plot.pie(y='code', title='response codes count')

    # show charts
    plt.show()
