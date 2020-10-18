import talib as ta 
import pandas as pd 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

Fs = 1001
f = 50
sample = 1001
x = np.arange(sample)
y = np.sin(2 * np.pi * f  * x / Fs) 
y = np.round(y,5)
y = y + 2
print(y)
open_data = (y[:(len(y))-1])
close_data = (y[1:])
high_data = (y[1:] + 0.5 )
low_data = (y[1:] - 0.5  )
data = {
    "time"        : x[:(len(x)-1)] ,
    "open price"  : open_data,
    "high price"  : high_data,
    "low price"   : low_data,
    "close price" : close_data
}
new_dataset = pd.DataFrame(data)
new_dataset.to_excel("data/Test_data/sin_dataset1.xlsx")
# print(new_dataset)
fig_data = go.Figure()

fig_data.add_trace(
    go.Candlestick(x=x,
    open=open_data,
    high=high_data,
    low=low_data,
    close=close_data)
)

# fig_data.add_trace(
#     go.Scatter(x=x,
#     y = y,
#     mode = 'lines')
# )

fig_data.update_layout(xaxis_rangeslider_visible=False)
fig_data.show()

# print()