import pandas as pd
import numpy as np
import talib as ta 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import MetaTrader5 as mt5 

data = pd.read_excel('data/Test_data/sin_dataset.xlsx',header=None)
data = data.iloc[:,:5]
data.columns = ["time","open","high","low","close"]
# BU,BM,BD = ta.BBANDS(data.loc[:,"close"],12,2,2,0)
# BU1,BM1,BD1 = ta.BBANDS(data.loc[:,"close"],12,4,4,0)
# DD = []
# BU = np.array(BU)
# BM = np.array(BM)
# BD = np.array(BD)
# BU = np.where(np.isnan(BU),0,BU)
# BM = np.where(np.isnan(BM),0,BM)
# BD = np.where(np.isnan(BD),0,BD)
# BU = BU.tolist()
# BM = BM.tolist()
# BD = BD.tolist()
# DD.append(BM)
# DD.append(BU)
# DD.append(BD)
# AA = DD[0]
# print(AA[0])
# sma12 = ta.SMA(data.loc[:,"close"],36)
# macd, macdsignal, macdhist = ta.MACD(data.loc[:,"close"],12,26,9)
# answer = 
# answer = [None] * len(data)
# data2 = data.to_numpy()
# for x in range(len(data2)):
#     # high = data2[x,2]
#     # sma = sma12[x]

#     if data2[x,3] <= sma12[x] <= data2[x,2]:
#         answer[x] = sma12[x]

# print(data)
fig = make_subplots(rows=1, cols=1, shared_xaxes=True, vertical_spacing=0.02)
fig.add_trace(
    go.Candlestick(x=[x for x in range (len(data))],## x=self.dataset.loc[:,"time"]
                open=data.loc[:,"open"],
                high=data.loc[:,"high"],
                low=data.loc[:,"low"],
                close=data.loc[:,"close"]),col= 1, row = 1
)

# fig.add_trace(
#     go.Scatter(
#         x = [x for x in range(len(data))],
#         y = macd,
#         mode = "lines",
#         name = "macd"
#     ),row= 2,col = 1
# )
# fig.add_trace(
#     go.Scatter(
#         x = [x for x in range(len(data))],
#         y = macdsignal,
#         mode = "lines",
#         name = "macdsignal"
#     ),row=2,col=1
# )
# fig.add_trace(
#     go.Scatter(
#         x = [x for x in range(len(data))],
#         y = macdhist,
#         mode = "lines",
#         name = "macdhist"
#     ),row=2,col=1
# )
# fig.add_trace(
#     go.Scatter(
#         x = [x for x in range(len(data))],
#         y = BM,
#         mode = "lines",
#         name = "mid"
#     ),row=1,col=1
# )
# fig.add_trace(
#     go.Scatter(
#         x = [x for x in range(len(data))],
#         y = BU,
#         mode = "lines",
#         name = "up"
#     ),row=1,col=1
# )
# fig.add_trace(
#     go.Scatter(
#         x = [x for x in range(len(data))],
#         y = BD,
#         mode = "lines",
#         name = "down"
#     ),row=1,col=1
# )
# fig.add_trace(
#     go.Scatter(
#         x = [x for x in range(len(data))],
#         y = BM1,
#         mode = "lines",
#         name = "mid1"
#     ),row=1,col=1
# )
# fig.add_trace(
#     go.Scatter(
#         x = [x for x in range(len(data))],
#         y = BU1,
#         mode = "lines",
#         name = "up1"
#     ),row=1,col=1
# )
# fig.add_trace(
#     go.Scatter(
#         x = [x for x in range(len(data))],
#         y = BD1,
#         mode = "lines",
#         name = "down1"
#     ),row=1,col=1
# )
fig.update_layout(xaxis_rangeslider_visible=False)
fig.show()




# answer = []
# test1 = [1,2,3,4,3,2,-2]
# test2 = [1,2,3,4,3,2,-2,-4,-3,-1,3]
# test = [1,2,3,4,3,2,-2,-4,-3,-1,3,6,1,-1,-4,-3,-5,-2,1,2,3,4,5]
# count = 1
# dataset = []
# if test1[len(test1)-1] < 0 :
# test1 = [1,2,3,4,5]
# test2 = [2,3,4,5,6]
# test3 = [3,4,5,6,7]

# test = []
# test.append([test1])
# test.append([test2])
# test.append([test3])
# print(test)
