import numpy as np
import pandas as pd 
import plotly.graph_objects as go
from plotly.subplots import make_subplots


path = "data/Raw_data/EUR_USD/EURUSD60.csv"
dataset = pd.read_csv(path,header=None)
set_year = "None"
set_data = []
for x in range(len(dataset)):
    print(x)
    res = dataset.iloc[x,0]
    year = res.split(sep=".")
    if x == 0 :
        set_year = year[0]
        
    elif set_year != year[0] :
        df = pd.DataFrame(data= set_data)
        df.to_excel("data/dataset/XM_EURUSD-"+set_year+"_H1.xlsx",header=None,index=None)
        set_year = year[0]
        set_data = []
        
    set_data.append(dataset.iloc[x])
df = pd.DataFrame(data= set_data)
df.to_excel("data/dataset/XM_EURUSD-"+set_year+"_H1.xlsx",header=None,index=None)
    

## ================= test ======================
# ans = []
# data = pd.read_csv("data/Raw_data/GBP_USD/GBPUSD60.csv",header=None)
# for x in range(10):
#     ans.append(data.iloc[x])
# ans = pd.DataFrame(data=ans)
# print(ans)
# print(data.iloc[0,0])
# Dates = data.iloc[0,0]
# sett = Dates.split(sep=".")
# print(sett)