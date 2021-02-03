from numpy.testing._private.utils import print_assert_equal
import pandas as pd 
import numpy as np
import datetime
import talib as ta 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import MinMaxScaler
import pickle

data = pd.read_excel('data/dataset/XM_EURUSD-2020_H1.xlsx',header=None)
# # close_diff = data.iloc[1:,5] - data.iloc[:len(data),5]
# close_a = np.array(data.iloc[1:,5])
# close_b = np.array(data.iloc[:len(data)-1,5])
# close_rela = close_a - close_b 
# open_rela  = np.array(data.iloc[1:,2]) - np.array(data.iloc[:len(data)-1,2])
# high_rela = np.array(data.iloc[1:,3]) - np.array(data.iloc[:len(data)-1,3])
# low_rela = np.array(data.iloc[1:,4]) - np.array(data.iloc[:len(data)-1,4])
# macd, macdsignal, macdhist = ta.MACD(data.iloc[:,5], fastperiod=12, slowperiod=26, signalperiod=9)
# macd1, macdsignal1, macdhist = ta.MACD(data.iloc[:,5], fastperiod=24, slowperiod=26, signalperiod=9)
# macd2, macdsignal2, macdhist = ta.MACD(data.iloc[:,5], fastperiod=48, slowperiod=26, signalperiod=9)
# macd3, macdsignal3, macdhist = ta.MACD(data.iloc[:,5], fastperiod=12, slowperiod=26, signalperiod=18)


# fig = make_subplots(rows=4, cols=1,
#                     shared_xaxes=True,
#                     vertical_spacing=0.02)
# fig = go.Figure()
# # print(data)
# fig.add_trace(
#     go.Candlestick(x=[x for x in range(len(data))],
#         open=data.iloc[:,2],
#         high=data.iloc[:,3],
#         low=data.iloc[:,4],
#         close=data.iloc[:,5])
        # ,row=1, col=1
    # )
# fig.add_trace(
#     go.Scatter(x=[x for x in range(len(data))],
#     y = macd)
#     ,row=2, col=1
# )
# fig.add_trace(
#     go.Scatter(x=[x for x in range(len(data))],
#     y = macdsignal)
#     ,row=2, col=1
# )
# fig.add_trace(
#     go.Scatter(x=[x for x in range(len(data))],
#     y = macdsignal1)
#     ,row=3, col=1
# )
# fig.add_trace(
#     go.Scatter(x=[x for x in range(len(data))],
#     y = macd1)
#     ,row=3, col=1
# )
# fig.add_trace(
#     go.Scatter(x=[x for x in range(len(data))],
#     y = macdsignal2)
#     ,row=4, col=1
# )
# fig.add_trace(
#     go.Scatter(x=[x for x in range(len(data))],
#     y = macd2)
#     ,row=4, col=1
# )
# fig.add_trace(go.Scatter(
#     x=[x for x in range(1,len(data))],
#     y = open_rela),row=2, col=1
#     )
# fig.add_trace(go.Scatter(
#     x=[x for x in range(1,len(data))],
#     y = high_rela),row=3, col=1
#     )
# fig.add_trace(go.Scatter(
#     x=[x for x in range(1,len(data))],
#     y = low_rela),row=4, col=1
#     )
# fig.add_trace(go.Scatter(
#     x=[x for x in range(1,len(data))],
#     y = close_rela),row=5
#     , col=1
#     )
# fig.update_layout(xaxis_rangeslider_visible=False)
# fig.show()

# data = [i for i in range (100)]
# data = np.array(data)
# print(data)
# data = np.reshape(data,(-1,1))
# scaler = MinMaxScaler()
# norm = scaler.fit_transform(data)
# print(norm)
# test = [x for x in range(101,120)]
# test = np.array(test)
# test = np.reshape(test,(-1,1))
# print(test)
# norm_test = scaler.transform(test)
# print(norm_test)
# print("waiting...")

data = {'x' : 1,'y': 2}
print(data['x'])
print(data['y'])
print("----------------")

data = pd.read_excel('data/dataset/XM_EURUSD-2010_H1.xlsx',header=None)
# data1 = pd.read_excel('data/dataset/XM_EURUSD-2011_H1.xlsx',header=None)
print(len(data))
# print(len(data1))
# c_data = pd.concat([data,data1])
# print(len(c_data))
for x in range(2011,2021):
    res = pd.read_excel('data/dataset/XM_EURUSD-'+ str(x) +'_H1.xlsx',header=None)
    data = pd.concat([data,res])
data.columns = ['date','time','open','high','low','close','volume']
macd, macdsignal, macdhist = ta.MACD(data['close'], fastperiod=12, slowperiod=26, signalperiod=9)
ATR = ta.ATR(data['high'], data['low'], data['close'], timeperiod=14)
slowk, slowd = ta.STOCH(data['high'], data['low'], data['close'], fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
WILL = ta.WILLR(data['high'], data['low'], data['close'], timeperiod=14)
SAR = ta.SAR(data['high'], data['low'], acceleration=0, maximum=0)
aroondown, aroonup = ta.AROON(data['high'], data['low'], timeperiod=14)
data = {
    'date' : data['date'],
    'time' : data['time'],
    'open' : data['open'],
    'high' : data['high'],
    'low'  : data['low'],
    'close' : data['close'],
    'volume' : data['volume'],
    'macd' : macd,
    'macdsignal':macdsignal,
    'macdhist':  macdhist, 
    'ATR' : ATR , 
    'slowk' : slowk, 
    'slowd' : slowd, 
    'WILL' : WILL,
    'SAR' : SAR,
    'aroondown' : aroondown,
    'aroonup' : aroonup
    }
all_data = pd.DataFrame(data= data)
# # print(all_data)
# print(all_data.describe())
res = all_data.describe()
res.to_excel('test/describe.xlsx')
# res = all_data.iloc[:,2:]
# res = res.dropna()
# res1 = res.to_numpy()
# scaler = MinMaxScaler(feature_range=(-0.85,0.85))
# print(scaler.fit(res))
# print(scaler.data_max_)
# pickle.dump(scaler,open('model/scaler.pickle', 'wb'))
# test_scaler = pickle.load(open('model/scaler.pickle', 'rb'))
# normalixed = test_scaler.transform(res)
# print(normalixed)
# fig = go.Figure()
# fig.add_trace(
#     go.Histogram(x=normalixed)
# )


# fig = make_subplots(rows=2, cols=1,
#                     shared_xaxes=True,
#                     vertical_spacing=0.02)

# fig.add_trace(
#     go.Histogram(x=all_data['low']),row=1 ,col=1
# )

# fig.update_layout(xaxis_rangeslider_visible=False)
# fig.show()

# data = [x for x in range (100)]
# max_something = np.max(data)
# print(max_something)