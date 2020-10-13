## import 
import pandas as pd 
import numpy as np 
import random
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, LabelEncoder, OneHotEncoder
import plotly.graph_objects as go
import talib
## ต้องสกัด feature เอง ไม่สามารถใช้ Raw data ได้ // think about it 

## TA ## 
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
    return(dfSeries)



##################### prepare dataset method #####################

## ================= dataset#1  ==========================


## ใช้ จุดกลับตัวในการ lable หากแท่งปัจจุบัน สูงกว่ารอบข้างใน "sell"  หากแท่งปัจจุบัน ต่ำกว่ารอบข้างใน "buy" ที่เหลือ "hold"
## nomalize โดยใช้ minmax ให้อยู่ระหว่าง (0 - 1)
## ใน set มีจำนวนแท่งเทียนตาม windows ที่กำหนด ใน code  
def dataset_1 (train_year,train_period,window):
    ## ------------------------------------------------------ // ตอนนี้ยังเซตเป็น ช่วงเวลาไม่ได้ // fucking do it
    data = pd.read_excel('ML_TEST/Data/Timeframe_data/'+ str(train_year)+ '/GBPUSD-'+ str(train_year)+'_'+ train_period +'.xlsx',header=None)
    # test = pd.read_excel('ML_TEST/Data/Timeframe_data/'+ str(train_year)+ '/GBPUSD-'+ str(train_year)+'_'+ train_period +'.xlsx',header=None)
    ## -------------------- labling -------------------------
    for index,tick in data.iterrows() :
        if index == 0 or index == len(data)-1 :
            data.iloc[index,5] = "hold"
            continue
        front = data.iloc[index-1]
        back = data.iloc[index+1]
        if front[4] > tick[4] and back[4] > tick[4] :
            data.iloc[index,5] = "buy"
        elif front[4] < tick[4] and back[4] < tick[4] :
            data.iloc[index,5] = "sell"
        else : data.iloc[index,5] = "hold"

    ## -------------------- nomalize & encode  ---------------------

    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data.iloc[:,1:5])
    # print(scaled_data)

    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(data.iloc[:,5])
    # print(integer_encoded)
    onehot_encoder = OneHotEncoder(sparse=False)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
    

    ## -------------------- cerate dataset -------------------------

    windows = window      ## กำหนด windows // here
    trainx_hold = []
    trainy_hold = []
    trainx_sell = []
    trainy_sell = []
    trainx_buy = []
    trainy_buy = []
    for index in range(len(data)):
        togo = index+windows
        subin = scaled_data[index:togo,:].tolist()
        subout = data.iloc[togo-1 , 5]
        enout = onehot_encoded[togo-1].tolist()
        if subout == 'buy':
            trainx_buy.append(subin)
            trainy_buy.append(enout)
        elif subout == 'sell': 
            trainx_sell.append(subin)
            trainy_sell.append(enout)
        else : 
            trainx_hold.append(subin) 
            trainy_hold.append(enout) 
        if index == len(scaled_data)-windows:
            break
    dataset_x = trainx_buy[0:1200] + trainx_sell[0:1200] + trainx_hold[0:1200]
    dataset_y = trainy_buy[0:1200] + trainy_sell[0:1200] + trainy_hold[0:1200]
    Test = trainx_buy[1200:1500] + trainx_sell[1200:1500] + trainx_hold[1200:1500]
    res = list(zip(dataset_x,dataset_y))
    random.shuffle(res)
    random.shuffle(Test)
    dataset_x,dataset_y = zip(*res)
    input_value = np.array(dataset_x)
    output_value = np.array(dataset_y)
    test_value = np.array(Test)
    return input_value,output_value,test_value
    
## ================= end dataset#1  ==========================




## ================= dataset#2  ==========================
## เปลี่ยนวิธีการ labling โดยใช้ zigzag เพื่อลด noise 

def dataset_2(start_year,train_period,windows,stop_year = None,minRetrace = 0.5):

    ## --------------------- gat data -----------------------------
    listOfdata = []
    if stop_year == None :
        stop_year = start_year
    for Index in range(start_year,stop_year+1):
        data = pd.read_excel('ML_TEST/Data/Timeframe_data/'+ str(Index)+ '/GBPUSD-'+ str(Index)+'_'+ train_period +'.xlsx',header=None)
        listOfdata.append(data)
    ## -------------------- labling -------------------------------
    for x in range(len(listOfdata)):
        listOfdata[x] = ZigZagPoints(listOfdata[x],minRetrace)
    answer = []
    for x in listOfdata:
        res = x.iloc[:,5]
        answer.append(res)
    answer = np.array(answer)
    ## --------------------- normalize ---------------------------
    resset = pd.concat([x for x in listOfdata], sort=False)
    scaler = MinMaxScaler()
    scaler.fit(resset.iloc[:,1:5])
    # print(scaler.data_max_)
    for index,data in enumerate (listOfdata):
        listOfdata[index] =  scaler.transform(data.iloc[:,1:5])
    
    ## ------------------ create dataset --------------------------

    trainx_hold = []
    trainy_hold = []
    trainx_sell = []
    trainy_sell = []
    trainx_buy = []
    trainy_buy = []
    for i,data in enumerate (listOfdata):
        for index in range(len(data)):
            togo = index+windows
            subin = data[index:togo,:]
            subout = answer[i].iloc[togo-1]
            if subout == -1:
                trainx_buy.append(subin)
                trainy_buy.append(subout)
            elif subout == 1: 
                trainx_sell.append(subin)
                trainy_sell.append(subout)
            else : 
                trainx_hold.append(subin) 
                trainy_hold.append(subout) 
            if index == len(data)-windows:
                break
    minset = min(len(trainy_buy),len(trainy_hold),len(trainy_sell))
    testsize = int((20 * minset)/100)
    trainsize = minset - testsize
    dataset_x =trainx_buy[0:trainsize] + trainx_sell[0:trainsize] + trainx_hold[0:trainsize]
    dataset_y = trainy_buy[0:trainsize] + trainy_sell[0:trainsize] + trainy_hold[0:trainsize]
    Test = trainx_buy[trainsize:minset] + trainx_sell[trainsize:minset] + trainx_hold[trainsize:minset]
    res = list(zip(dataset_x,dataset_y))
    random.shuffle(res)
    random.shuffle(Test)
    dataset_x,dataset_y = zip(*res)
    input_value = np.array(dataset_x)
    output_value = np.array(dataset_y)
    test_value = np.array(Test)
## ------------------ normalize answer ----------------
    output_value = output_value.reshape((len(output_value),1))
    onehot_encoder = OneHotEncoder(sparse=False)
    output_value = onehot_encoder.fit_transform(output_value)
    return input_value,output_value,test_value


## ================= end dataset#2  ==========================



## ================= dataset#3  ==========================

def dataset_3(start_year,train_period,windows,stop_year = None,minRetrace = 0.5):

    ## --------------------- gat data -----------------------------
    listOfdata = []
    if stop_year == None :
        stop_year = start_year
    for Index in range(start_year,stop_year+1):
        data = pd.read_excel('ML_TEST/Data/Timeframe_data/'+ str(Index)+ '/GBPUSD-'+ str(Index)+'_'+ train_period +'.xlsx',header=None)
        listOfdata.append(data)
    
    ## -------------------- labling -------------------------------
    for x in range(len(listOfdata)):
        listOfdata[x] = ZigZagPoints(listOfdata[x],minRetrace)
    answer = []
    for x in listOfdata:
        res = x.iloc[:,5]
        answer.append(res)
    answer = np.array(answer)
    ## --------------------- normalize ---------------------------
    resset = pd.concat([x for x in listOfdata], sort=False)
    scaler = MinMaxScaler()
    scaler.fit(resset.iloc[:,1:5])
    # print(scaler.data_max_)
    for index,data in enumerate (listOfdata):
        listOfdata[index] =  scaler.transform(data.iloc[:,1:5])
    
    ## ------------------ create dataset --------------------------
    trainx_hold = []
    trainy_hold = []
    trainx_sell = []
    trainy_sell = []
    trainx_buy = []
    trainy_buy = []
    for i,data in enumerate (listOfdata):
        for index in range (len(data)) :
            togo = index+windows
            subin = data[index:togo,3]
            subin = subin.reshape((len(subin),1))
            subout = answer[i].iloc[togo-1]
            if subout == -1:
                trainx_buy.append(subin)
                trainy_buy.append(subout)
            elif subout == 1: 
                trainx_sell.append(subin)
                trainy_sell.append(subout)
            else : 
                trainx_hold.append(subin) 
                trainy_hold.append(subout) 
            if index == len(data)-windows:
                break
    minset = min(len(trainy_buy),len(trainy_hold),len(trainy_sell))
    testsize = int((20 * minset)/100)
    trainsize = minset - testsize
    dataset_x =trainx_buy[0:trainsize] + trainx_sell[0:trainsize] + trainx_hold[0:trainsize]
    dataset_y = trainy_buy[0:trainsize] + trainy_sell[0:trainsize] + trainy_hold[0:trainsize]
    Test = trainx_buy[trainsize:minset] + trainx_sell[trainsize:minset] + trainx_hold[trainsize:minset]
    sol_Test = trainy_buy[trainsize:minset] + trainy_sell[trainsize:minset] + trainy_hold[trainsize:minset]
    res = list(zip(dataset_x,dataset_y))
    restest = list(zip(Test,sol_Test))
    random.shuffle(res)
    random.shuffle(restest)
    dataset_x,dataset_y = zip(*res)
    Test,sol_Test = zip(*restest)
    input_value = np.array(dataset_x)
    output_value = np.array(dataset_y)
    test_value = np.array(Test)
    # sol_value = np.array(sol_Test)
## ------------------ normalize answer ----------------
    output_value = output_value.reshape((len(output_value),1))
    onehot_encoder = OneHotEncoder(sparse=False)
    output_value = onehot_encoder.fit_transform(output_value)
    return input_value,output_value,test_value


## ================= end dataset#3  ==========================


## ================= dataset#4  ==========================

def dataset_4(start_year,train_period,windows,stop_year = None,minRetrace = 0.5):

    ## --------------------- gat data -----------------------------
    listOfdata = []
    if stop_year == None :
        stop_year = start_year
    for Index in range(start_year,stop_year+1):
        data = pd.read_excel('ML_TEST/Data/Timeframe_data/'+ str(Index)+ '/GBPUSD-'+ str(Index)+'_'+ train_period +'.xlsx',header=None)
        listOfdata.append(data)
    
    ## -------------------- labling -------------------------------
    for x in range(len(listOfdata)):
        listOfdata[x] = ZigZagPoints(listOfdata[x],minRetrace)
    answer = []
    for x in listOfdata:
        res = x.iloc[:,5]
        answer.append(res)
    answer = np.array(answer)
    ## --------------------- normalize ---------------------------
    resset = pd.concat([x for x in listOfdata], sort=False)
    scaler = MinMaxScaler()
    scaler.fit(resset.iloc[:,1:5])
    # print(scaler.data_max_)
    for index,data in enumerate (listOfdata):
        listOfdata[index] =  scaler.transform(data.iloc[:,1:5])
    
    ## ------------------ create dataset --------------------------



## ================= end dataset#4  ==========================