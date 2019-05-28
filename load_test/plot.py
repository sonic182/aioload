"""Plot stuffs."""

import matplotlib.pyplot as plt
import pandas as pd


def render_plot(statics):
    """Render plot."""
    durations = []
    when = []
    for item in statics:
        durations.append(item['duration'])
        when.append(item['when'])

    serie = pd.Series(
        durations,
        index=pd.date_range(
            min(when),
            max(when),
            periods=len(durations),
        )
    )
    serie.plot()
    plt.show()
