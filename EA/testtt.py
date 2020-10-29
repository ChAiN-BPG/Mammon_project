import pandas as pd
import numpy as np
import talib as ta 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import MetaTrader5 as mt5 

data = pd.read_excel('data/TimeFrame/2004/GBPUSD-2004_H1.xlsx',header=None)
data = data.iloc[:,:5]
data.columns = ["time","open","high","low","close"]
sma12 = ta.SMA(data.loc[:,"close"],36)
macd, macdsignal, macdhist = ta.MACD(data.loc[:,"close"],12,26,9)
# answer = [None] * len(data)
# data2 = data.to_numpy()
# for x in range(len(data2)):
#     # high = data2[x,2]
#     # sma = sma12[x]

#     if data2[x,3] <= sma12[x] <= data2[x,2]:
#         answer[x] = sma12[x]

# print(data)
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02)
fig.add_trace(
    go.Candlestick(x=[x for x in range (len(data))],## x=self.dataset.loc[:,"time"]
                open=data.loc[:,"open"],
                high=data.loc[:,"high"],
                low=data.loc[:,"low"],
                close=data.loc[:,"close"]),col= 1, row = 1
)
fig.add_trace(
    go.Scatter(
        x = [x for x in range(len(data))],
        y = macd,
        mode = "lines",
        name = "macd"
    ),row= 2,col = 1
)
fig.add_trace(
    go.Scatter(
        x = [x for x in range(len(data))],
        y = macdsignal,
        mode = "lines",
        name = "macdsignal"
    ),row=2,col=1
)
fig.add_trace(
    go.Scatter(
        x = [x for x in range(len(data))],
        y = macdhist,
        mode = "lines",
        name = "macdsignal"
    ),row=2,col=1
)
fig.update_layout(xaxis_rangeslider_visible=False)
fig.show()




# answer = []
# test = [1,2,3,4,5,6,7]
# for _ in range (len(test)):
#     data = test.pop(0)
#     if data > 4 :
#         answer.append(data)
#     print(data)
# print(answer)