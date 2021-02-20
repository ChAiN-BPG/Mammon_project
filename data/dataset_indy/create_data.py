import numpy as np
import talib as ta 
import pandas as pd 
import datetime
all_data = []
for x in range(2010,2021):
    # print(x)
    df_data = pd.read_excel('data/dataset/XM_GBPUSD-'+str(x)+'_H1.xlsx',header=None)
    # all_data.append(res_data)
    df_data.columns = ['date','time','open','high','low','close','volume']
    ##  ================ add indicator ==================== 
    macd, macdsignal, macdhist = ta.MACD(df_data['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    ATR = ta.ATR(df_data['high'], df_data['low'], df_data['close'], timeperiod=14)
    slowk, slowd = ta.STOCH(df_data['high'], df_data['low'], df_data['close'], fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    WILL = ta.WILLR(df_data['high'], df_data['low'], df_data['close'], timeperiod=14)
    SAR = ta.SAR(df_data['high'], df_data['low'], acceleration=0, maximum=0)
    aroondown, aroonup = ta.AROON(df_data['high'], df_data['low'], timeperiod=14)
    ## ====================================================
    data = {
        'date' : df_data['date'],
        'time' : df_data['time'],
        'open' : df_data['open'],
        'high' : df_data['high'],
        'low'  : df_data['low'],
        'close' : df_data['close'],
        'volume' : df_data['volume'],
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
    # all_data = df_data
    all_data =  all_data.dropna()
    all_data = all_data.to_numpy()
    data_AllTick = len(all_data)
    data_column = len(all_data[0])
    count_tick = 0
    ## set datetime 
    for i in range(data_AllTick):
        date = all_data[i,0].split('.')
        time = all_data[i,1].split(':')
        all_data[i,0] = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),int(time[0]),int(time[1]))
    all_data = pd.DataFrame(all_data)
    all_data.to_excel('data/dataset_indy/XM_EURUSD-'+str(x)+'_H1_indy.xlsx',header=None,index=None)
    print("finsih dataset " + str(x))