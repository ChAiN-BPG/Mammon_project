
from numpy.testing._private.utils import print_assert_equal
import pandas as pd 
import numpy as np
import datetime
import talib as ta 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import MinMaxScaler
import pickle
import random

data = pd.read_excel('data/dataset/XM_EURUSD-2019_H1.xlsx',header=None)
# # close_diff = data.iloc[1:,5] - data.iloc[:len(data),5]
# # close_a = np.array(data.iloc[1:,5])
# # close_b = np.array(data.iloc[:len(data)-1,5])
# # close_rela = close_a - close_b 
# # open_rela  = np.array(data.iloc[1:,2]) - np.array(data.iloc[:len(data)-1,2])
# # high_rela = np.array(data.iloc[1:,3]) - np.array(data.iloc[:len(data)-1,3])
# # low_rela = np.array(data.iloc[1:,4]) - np.array(data.iloc[:len(data)-1,4])

# macd, macdsignal, macdhist = ta.MACD(data.iloc[:,5], fastperiod=12, slowperiod=26, signalperiod=9) ####
# ATR = ta.ATR(data.iloc[:,3], data.iloc[:,4], data.iloc[:,5], timeperiod=14)
# slowk, slowd = ta.STOCH(data.iloc[:,3], data.iloc[:,4], data.iloc[:,5], fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)###
# WILL = ta.WILLR(data.iloc[:,3], data.iloc[:,4], data.iloc[:,5], timeperiod=14)
# SAR = ta.SAR(data.iloc[:,3], data.iloc[:,4], acceleration=0, maximum=0)
# aroondown, aroonup = ta.AROON(data.iloc[:,3], data.iloc[:,4], timeperiod=14)


# ###################### 
 
# macd1, macdsignal1, macdhist1 = ta.MACD(data.iloc[:35,5], fastperiod=12, slowperiod=26, signalperiod=9)
# ATR1 = ta.ATR(data.iloc[:35,3], data.iloc[:35,4], data.iloc[:35,5], timeperiod=14)
# slowk1, slowd1 = ta.STOCH(data.iloc[:35,3], data.iloc[:35,4], data.iloc[:35,5], fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)###
# WILL1 = ta.WILLR(data.iloc[:35,3], data.iloc[:35,4], data.iloc[:35,5], timeperiod=14)
# SAR1 = ta.SAR(data.iloc[:35,3], data.iloc[:35,4], acceleration=0, maximum=0)
# aroondown1, aroonup1 = ta.AROON(data.iloc[:35,3], data.iloc[:35,4], timeperiod=14)

# ###################### 
 
# macd2, macdsignal2, macdhist2 = ta.MACD(data.iloc[:36,5], fastperiod=12, slowperiod=26, signalperiod=9)
# ATR2 = ta.ATR(data.iloc[:36,3], data.iloc[:36,4], data.iloc[:36,5], timeperiod=14)
# slowk2, slowd2 = ta.STOCH(data.iloc[:36,3], data.iloc[:36,4], data.iloc[:36,5], fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)###
# WILL2 = ta.WILLR(data.iloc[:36,3], data.iloc[:36,4], data.iloc[:36,5], timeperiod=14)
# SAR2 = ta.SAR(data.iloc[:36,3], data.iloc[:36,4], acceleration=0, maximum=0)
# aroondown2, aroonup2 = ta.AROON(data.iloc[:36,3], data.iloc[:36,4], timeperiod=14)
# # macd1, macdsignal1, macdhist = ta.MACD(data.iloc[:,5], fastperiod=24, slowperiod=26, signalperiod=9)
# # macd2, macdsignal2, macdhist = ta.MACD(data.iloc[:,5], fastperiod=48, slowperiod=26, signalperiod=9)
# # macd3, macdsignal3, macdhist = ta.MACD(data.iloc[:,5], fastperiod=12, slowperiod=26, signalperiod=18)
# print("wait")

# fig = make_subplots(rows=4, cols=1,
#                     shared_xaxes=True,
#                     vertical_spacing=0.02)
fig = go.Figure()
# print(data)
fig.add_trace(
    go.Candlestick(x=[x for x in range(len(data))],
        open=data.iloc[:,2],
        high=data.iloc[:,3],
        low=data.iloc[:,4],
        close=data.iloc[:,5])
        # ,row=1, col=1
    )
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
fig.update_layout(xaxis_rangeslider_visible=False)
fig.show()

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

# data = {'x' : 1,'y': 2}
# print(data['x'])
# print(data['y'])
# print("----------------")

# data = pd.read_excel('data/dataset/XM_EURUSD-201ๅ_H1.xlsx',header=None)
# data1 = pd.read_excel('data/dataset/XM_EURUSD-2011_H1.xlsx',header=None)
# print(len(data))
# print(len(data1))
# c_data = pd.concat([data,data1])
# print(len(c_data))
# data = []
# for x in range(2010,2021):
#     res = pd.read_excel('data/dataset/XM_EURUSD-'+ str(x) +'_H1.xlsx',header=None)
#     # data = pd.concat([data,res])
#     res.columns = ['date','time','open','high','low','close','volume']
#     macd, macdsignal, macdhist = ta.MACD(res['close'], fastperiod=12, slowperiod=26, signalperiod=9)
#     ATR = ta.ATR(res['high'], res['low'], res['close'], timeperiod=14)
#     slowk, slowd = ta.STOCH(res['high'], res['low'], res['close'], fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
#     WILL = ta.WILLR(res['high'], res['low'], res['close'], timeperiod=14)
#     SAR = ta.SAR(res['high'], res['low'], acceleration=0, maximum=0)
#     aroondown, aroonup = ta.AROON(res['high'], res['low'], timeperiod=14)
#     data = {
#         'date' : res['date'],
#         'time' : res['time'],
#         'open' : res['open'],
#         'high' : res['high'],
#         'low'  : res['low'],
#         'close' : res['close'],
#         'volume' : res['volume'],
#         'macd' : macd,
#         'macdsignal':macdsignal,
#         'macdhist':  macdhist, 
#         'ATR' : ATR , 
#         'slowk' : slowk, 
#         'slowd' : slowd, 
#         'WILL' : WILL,
#         'SAR' : SAR,
#         'aroondown' : aroondown,
#         'aroonup' : aroonup
#         }
#     res_data = pd.DataFrame(data= data)
#     data.append(res_data)
# # print(all_data)
# print(all_data.describe())
# res = all_data.describe()
# res.to_excel('test/describe.xlsx')
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


################## test #######################3
# data = pd.read_excel('data/dataset/XM_EURUSD-2013_H1.xlsx',header=None)
# for x in range(len(data)):
#             date = data.iloc[x,0].split('.')
#             time = data.iloc[x,1].split(':')
#             data.iloc[x,0] = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),int(time[0]),int(time[1]))
# # print(data.iloc[0,0].month)
# month = []
# for x in range(len(data)):
#     month.append(data.iloc[x,0].month)
#     # pass
# data['month'] = month
# print(data)
# res = data.groupby('month').get_group(1)
# res = res.iloc[:,:-1]
# print(res)
# print([ x for x in range (1,13)])
# print(random.randrange(1,12))



# all_data = []
# for x in range(2010,2021):
#     res = pd.read_excel('data\dataset_indy\XM_EURUSD-'+str(x)+'_H1_indy.xlsx')
#     res = res.iloc[:,2:]
#     res = res.to_numpy()
#     all_data.extend(res)
# # all_data.pop(0)
# all_data = pd.DataFrame(all_data)
# print(all_data.describe())
# res = all_data.describe()
# res.to_excel('test/describe.xlsx')
# # res = res.dropna()
# res1 = all_data.to_numpy()
# scaler = MinMaxScaler(feature_range=(-0.85,0.85))
# print(scaler.fit(res1))
# print(scaler.data_max_)
# pickle.dump(scaler,open('model/scaler.pickle', 'wb'))