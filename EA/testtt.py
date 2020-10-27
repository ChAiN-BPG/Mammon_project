import pandas as pd
import numpy as np
import talib as ta 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import MetaTrader5 as mt5 


fig = go.Figure()
for y in range(3):
    data = [x*y for x in range(10)]
    fig.add_trace(
        go.Scatter(
            x = [x for x in range(10)],
            y = data,
            mode = "lines",
            name = "data" +str(y)

        )
    )
fig.update_layout(xaxis_rangeslider_visible=False)
fig.show()