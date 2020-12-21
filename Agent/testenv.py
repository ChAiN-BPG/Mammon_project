import gym
import FX_trading
import pandas as pd 
import  numpy as np 
from tensorforce import Agent
import datetime

import plotly.graph_objects as go


def ZigZagPoints(dfSeries, minSegSize=2):
    minRetrace = minSegSize
    answer = [0] * len(dfSeries)
    answer = pd.DataFrame(answer)
    curVal = dfSeries.iloc[0,3]
    curPos = dfSeries.index[0]
    curDir = 1
    # dfRes = pd.DataFrame(index=dfSeries.index, columns=["Dir", "Value"])
    for ln in dfSeries.index:
        if((dfSeries.iloc[ln,3] - curVal)*curDir >= 0):
            curVal = dfSeries.iloc[ln,3] 
            curPos = ln
        else:      
            retracePrc = abs((dfSeries.iloc[ln,3] -curVal)/curVal*100)
            if(retracePrc >= minRetrace):
                # dfRes.loc[curPos, 'Value'] = curVal
                # dfRes.loc[curPos, 'Dir'] = curDir
                answer.iloc[curPos] = curDir
                curVal = dfSeries.iloc[ln,3] 
                curPos = ln
                curDir = -1*curDir
    # dfRes[['Value']] = dfRes[['Value']].astype(float)
    # dfRes = dfRes.interpolate(method='linear')
    answer = answer.replace(0,0)
    answer = answer.replace(1,2)
    answer = answer.replace(-1,1)
    
    return(answer)


data = pd.read_excel('data/dataset/XM_EURUSD-2011_H1.xlsx', header=None)
date = data.iloc[0,:2]
data= data.iloc[:,2:]
# Date = date.iloc[0].split('.')
# time = date.iloc[1].split(':')
# asss = datetime.datetime(int(Date[0]),int(Date[1]),int(Date[2]),int(time[0]),int(time[1]))
# print(data.iloc[0,4])
Answer = ZigZagPoints(data,0.15)
Answer = Answer.to_numpy()
Answer = Answer.flatten()
# for x in range (len(data)):
#     if out.iloc[x,0] != 0 :
#         out.iloc[x,0] = data.iloc[x,3]
#     else :
#         out.iloc[x,0] = None
# for x in range(len(data)):
#     if x == len(data)-1 : continue
#     if out.iloc[x + 1,0] != 0 and out.iloc[x,0] == 0 :
#         out.iloc[x,0] = 3
# print(data)
# print(out)
# out = out.to_numpy()
# out = out.flatten()
# fig_data = go.Figure()
# fig_data.add_trace(
#     go.Candlestick(x=[x for x in range(len(data))],
#         open=data.iloc[:,0],
#         high=data.iloc[:,1],
#         low=data.iloc[:,2],
#         close=data.iloc[:,3])
# )
# fig_data.add_trace(
#     go.Scatter(x=[x for x in range(len(data))],
#     y = out,
#     connectgaps=True )
# )
# fig_data.update_layout(xaxis_rangeslider_visible=False)
# fig_data.show()





# data = pd.read_excel('data/Test_data/sin_dataset.xlsx', header=None)
# data1 = data.iloc[:len(data)-1,4]
# data2 = data.iloc[1:,4]
# data1 = np.array(data1)
# data2 = np.array(data2)
# answer = data1 - data2
# # print(data1)
# # print(data2)
# Answer = []
# for x in answer :
#     if x > 0:
#         Answer.append(0)
#     else:
#         Answer.append(1)
# print(len(Answer))
# answer = [1]
# # answer.extend(Answer)
# Answer.extend(answer)
# print(len(Answer))

env = gym.make('FXTrading-v99')
# env.reset()
for index in range(len(data)):
    env.render()
    env.step(Answer[index]) 
env.plot_data()
env.close()

