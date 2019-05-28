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

    durations_serie = pd.Series(
        durations,
        index=pd.date_range(
            min(when),
            max(when),
            periods=len(durations),
        )
    )
    durations_serie.plot()
    codes_df = pd.DataFrame.from_dict(codes, orient='index')
    codes_df.plot.bar()
    plt.show()
