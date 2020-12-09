import pandas as pd 
import numpy as np
import plotly.graph_objects as go

data = pd.read_excel('data/Test_data/sin_dataset.xlsx',header=None)
# print(data)
fig_data = go.Figure()
fig_data.add_trace(
    go.Candlestick(x=data.iloc[:,0],
        open=data.iloc[:,1],
        high=data.iloc[:,2],
        low=data.iloc[:,3],
        close=data.iloc[:,4])
    )
fig_data.update_layout(xaxis_rangeslider_visible=False)
fig_data.show()
