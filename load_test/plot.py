"""Plot stuffs."""

import matplotlib.pyplot as plt
import pandas as pd


def render_plot(statics, durations_serie):
    """Render plot."""
    codes = {}
    for item in statics:
        codes[item['code']] = code = codes.get(item['code'], 0)
        codes[item['code']] = code + 1

    # durations chart
    fig, axes = plt.subplots(nrows=2, ncols=1)

    # mean duration chart
    durations_serie.resample('1s').mean().plot(
        title='median duration per 1s', ax=axes[0])
    # req per second chart
    durations_serie.resample('1s').count().plot(
        title='req/s', ax=axes[1])

    # codes chart
    codes_df = pd.DataFrame.from_dict(codes, orient='index')
    codes_df.plot.bar(title='response codes count')

    # show charts
    plt.show()
