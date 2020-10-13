## import 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, LabelEncoder, OneHotEncoder
import tensorflow as tf 
import random
from tensorflow import keras
from keras.models import Model
from keras.layers import Input, Dense, LSTM, Dropout, Activation, Concatenate ,GRU
from keras.utils import to_categorical
import plotly.graph_objects as go
import talib
from sklearn.metrics import confusion_matrix
from keras.callbacks import ModelCheckpoint
from pickle import dump

## ----------- function -----------------------

def ZigZagPoints(dfSeries, minSegSize=2):
    minRetrace = minSegSize
    
    curVal = dfSeries.iloc[0,4]
    curPos = dfSeries.index[0]
    curDir = 1
    # dfRes = pd.DataFrame(index=dfSeries.index, columns=["Dir", "Value"])
    for ln in dfSeries.index:
        if((dfSeries.iloc[ln,4] - curVal)*curDir >= 0):
            curVal = dfSeries.iloc[ln,4] 
            curPos = ln
        else:      
            retracePrc = abs((dfSeries.iloc[ln,4] -curVal)/curVal*100)
            if(retracePrc >= minRetrace):
                # dfRes.loc[curPos, 'Value'] = curVal
                # dfRes.loc[curPos, 'Dir'] = curDir
                dfSeries.iloc[curPos,5] = curDir
                curVal = dfSeries.iloc[ln,4] 
                curPos = ln
                curDir = -1*curDir
    # dfRes[['Value']] = dfRes[['Value']].astype(float)
    # dfRes = dfRes.interpolate(method='linear')
    dfSeries[5] = dfSeries[5].replace(0,'HOLD')
    dfSeries[5] = dfSeries[5].replace(-1,'BUY')
    dfSeries[5] = dfSeries[5].replace(1,'SELL')
    return(dfSeries)

def differ_data(dfSeries, size=1):
    answer = dfSeries.iloc[:,5]
    data = dfSeries.iloc[:,1:5]
    new_data = []
    for tick in range(len(dfSeries)):
        diff_open = data.iloc[tick,0] - data.iloc[tick+size,0]
        diff_high = data.iloc[tick,1] - data.iloc[tick+size,1]
        diff_low = data.iloc[tick,2] - data.iloc[tick+size,2]
        diff_close = data.iloc[tick,3] - data.iloc[tick+size,3]
        diff_answer = answer.iloc[tick + size]
        new_data.append([diff_open,diff_high,diff_low,diff_close,diff_answer])
        if tick == len(dfSeries) - (size+1):
            break
    dfdata = pd.DataFrame(new_data)
    return dfdata



## ------------ init data ------------------
namedataset = "dataset_1"
start_year = 2003
stop_year = None
train_period = "H1"
min_retrace = 0.3
size = None

## ======================================= labled dataset ============================================
# ------------ get data -------------------
listOfdata = []
if stop_year == None :
    stop_year = start_year
for Index in range(start_year,stop_year+1):
    data = pd.read_excel('ML_TEST/Data/Timeframe_data/'+ str(Index)+ '/GBPUSD-'+ str(Index)+'_'+ train_period +'.xlsx',header=None)
    listOfdata.append(data)

## -------------------- labling -------------------------------
for x in range(len(listOfdata)):
    listOfdata[x] = ZigZagPoints(listOfdata[x],min_retrace)
    ## papappap 
fuck = listOfdata[0]
you = fuck.iloc[:,5]
you = you.replace({"HOLD": 0,"BUY" : 1, "SELL":2})
you.to_csv('rr.csv')

# ## --------------------- write to excel -----------------------
# listofyear = [x for x in range(start_year,stop_year+1)]
# for I,data in enumerate (listOfdata):
#     data.to_excel('ML_TEST/Data/labled_data/'+ str(listofyear[I])+ '/GBPUSD-'+ str(listofyear[I])+'_'+ train_period +'_labled.xlsx',header=None,index=None)

## ======================================= ================= ============================================

# ## ======================================= diff dataset ============================================
# listOfdata = []
# if stop_year == None :
#     stop_year = start_year
# for Index in range(start_year,stop_year+1):
#     data = pd.read_excel('ML_TEST/Data/labled_data/'+ str(Index)+ '/GBPUSD-'+ str(Index)+'_'+ train_period +'_labled.xlsx',header=None)
#     listOfdata.append(data)
# ## -------------------- change data ----------------------------
# for x in range(len(listOfdata)):
#     listOfdata[x] = differ_data(listOfdata[x])
# ## --------------------- write to excel -----------------------
# listofyear = [x for x in range(start_year,stop_year+1)]
# for I,data in enumerate (listOfdata):
#     data.to_excel('ML_TEST/Data/labled_data/'+ str(listofyear[I])+ '/GBPUSD-'+ str(listofyear[I])+'_'+ train_period +'_diff.xlsx',header=None,index=None)
# ## ======================================= ================= ============================================