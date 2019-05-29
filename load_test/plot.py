"""Plot stuffs."""

import matplotlib.pyplot as plt
import pandas as pd


def render_plot(statics):
    """Render plot."""
    durations = []
    when = []
    codes = {}
    for item in statics:
        durations.append(item['duration'])
        when.append(item['when'])
        codes[item['code']] = code = codes.get(item['code'], 0)
        codes[item['code']] = code + 1

    # durations chart
    durations_serie = pd.Series(
        durations,
        index=pd.date_range(
            min(when),
            max(when),
            periods=len(durations),
        )
    )
    # durations_serie.plot()

    # mean duration chart
    durations_serie.resample('3s').mean().plot(
        title='median per 3s')

    # codes chart
    codes_df = pd.DataFrame.from_dict(codes, orient='index')
    codes_df.plot.bar(title='response codes count')

    # show charts
    plt.show()
