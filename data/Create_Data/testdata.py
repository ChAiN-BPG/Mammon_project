import pandas as pd 
import numpy as np
import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

data = pd.read_excel('data/dataset/XM_EURUSD-2011_H1.xlsx',header=None)
# close_diff = data.iloc[1:,5] - data.iloc[:len(data),5]
close_a = np.array(data.iloc[1:,5])
close_b = np.array(data.iloc[:len(data)-1,5])
close_rela = close_a - close_b 
open_rela  = np.array(data.iloc[1:,2]) - np.array(data.iloc[:len(data)-1,2])
high_rela = np.array(data.iloc[1:,3]) - np.array(data.iloc[:len(data)-1,3])
low_rela = np.array(data.iloc[1:,4]) - np.array(data.iloc[:len(data)-1,4])




fig = make_subplots(rows=5, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.02)

# print(data)
fig.add_trace(
    go.Candlestick(x=[x for x in range(len(data))],
        open=data.iloc[:,2],
        high=data.iloc[:,3],
        low=data.iloc[:,4],
        close=data.iloc[:,5]),row=1, col=1
    )
fig.add_trace(go.Scatter(
    x=[x for x in range(1,len(data))],
    y = open_rela),row=2, col=1
    )
fig.add_trace(go.Scatter(
    x=[x for x in range(1,len(data))],
    y = high_rela),row=3, col=1
    )
fig.add_trace(go.Scatter(
    x=[x for x in range(1,len(data))],
    y = low_rela),row=4, col=1
    )
fig.add_trace(go.Scatter(
    x=[x for x in range(1,len(data))],
    y = close_rela),row=5
    , col=1
    )
fig.update_layout(xaxis_rangeslider_visible=False)
fig.show()

