import pandas as pd
import numpy as np
import talib as ta 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import MetaTrader5 as mt5 

def Crossover(value1,value2,value3,value4):
    signal = bool(0)
    if value1 > value3 and value2 < value4:
        signal = bool(1)
    return signal


data = pd.read_excel('data/TimeFrame/2004/GBPUSD-2004_H1.xlsx',header=None)
data = data.iloc[:,:5]
data.columns = ["time","open","high","low","close"]
ema12 = ta.SMA(data.loc[:,"close"],12)
ema36 = ta.SMA(data.loc[:,"close"],36)
# adx14 = ta.ADX(data.loc[:,"high"],data.loc[:,"low"],data.loc[:,"close"],7)

answer = [None] * len(data)
answer2 = [None] * len(data)
for index,tick in data.iterrows() :
    if index == 0:
        continue
    if Crossover(ema36[index-1],ema36[index],ema12[index-1],ema12[index]):
        answer[index] = data.loc[index,"close"] + 0.00011
    if Crossover(ema12[index-1],ema12[index],ema36[index-1],ema36[index]):
        answer2[index] = data.loc[index,"close"] - 0.00011

fig =  go.Figure()
fig.add_trace(
    go.Candlestick(x=[x for x in range(len(data)) ],
        open=data.loc[:,"open"],
        high=data.loc[:,"high"],
        low=data.loc[:,"low"],
        close=data.loc[:,"close"])
)
fig.add_trace(
    go.Scatter(
        x=[x for x in range(len(data)) ],
        y = ema12,
        mode="lines",
        name = "ema12"
    )
)
fig.add_trace(
    go.Scatter(
        x=[x for x in range(len(data)) ],
        y = ema36,
        mode="lines",
        name = "ema36"
    )
)
fig.add_trace(
    go.Scatter(
        x=[x for x in range(len(data)) ],
        y = answer,
        mode="markers",
        name = "answer"
    )
)
fig.add_trace(
    go.Scatter(
        x = [x for x in range (len(data))],
        y = answer2,
        mode = "markers",
        name = "anwer2"
    )
)
fig.update_layout(xaxis_rangeslider_visible=False)
fig.show()




### ============================ save ==============================


    ## ============================== function core ===================================
    def __init__(self,balance = 200,lot = "standard",leverage = "1:100",spread = 0.00022):
        """
        this class use for simulate forex trading 
            list of paramiter:
            1.balance : the budget you want to trade [default by 200]
            2.lot : - 100000 = "standard"
                    - 10000  = "mini"
                    - 1000   = "micro"
                    - 100    = "nano"
            3.leverage : the amount of money that broker gave you [default by 1:100]
            4. spread : the amount of money that you have to pay more [default by 0.00022]
            5. mt5_service : you can link with metatrader5 by set True [default by False]
        """
        self.end = False
        self.budget = balance
        self.balance = balance
        self.spread = spread
        self.ready = False
        res = leverage.split(":")
        self.leverage =  int(res[1])
        if lot == "standard":
            res = 100000
        elif lot == "mini":
            res = 10000
        elif lot == "micro":
            res = 1000
        elif lot == "nano":
            res = 100
        self.lot = res
        ## ========== save indicator ===============
        self.last_cross = None
        ## ========= for ploting ===================


    # def GetData(self,money = "TEST",start_year = None,timeframe = None,end_year = None):
    #     """
    #     this function use for fatch data form the DATA file.
            
    #         list of paramiter:
    #         1. money : - pair of currancy you want to test. for example ("GBPUSD") 
    #                    - you can use sin graph for testing by ("TEST") [default by "TEST"]
    #         2. start_year : the year you want to start for testing  [default by None]
    #         3. timeframe : the timeframe you want to test [default by None]
    #         4. stop_year : the year you want to stop for testing [default by None]
    #     """
    #     if money == "TEST":
    #         data = pd.read_excel('data/Test_data/sin_dataset.xlsx',header=None)
    #         data.columns = ["time","open","high","low","close"]
    #         self.timeframe = "None"
    #         self.dataset = data
    #         self.ready = True
    #         self.currancy = money
    #         return
    #     else :
    #         data = pd.read_excel('data/TimeFrame/'+ str(start_year)+ '/'+ money +'-'+ str(start_year)+'_'+ timeframe +'.xlsx',header=None)
    #         data = data.iloc[:,:5]
    #         data.columns = ["time","open","high","low","close"]
    #     if end_year != None :
    #         for Index in range(start_year+1,end_year+1):
    #             resdata = pd.read_excel('data/TimeFrame/'+ str(Index)+ '/'+ money +'-'+ str(Index)+'_'+ timeframe +'.xlsx',header=None)
    #             data = pd.concat([data,resdata])
    #         data = data.iloc[:,:5]
    #         data.columns = ["time","open","high","low","close"]
    #     self.timeframe = timeframe
    #     self.ready = True
    #     self.currancy = money
    #     self.dataset = data
    #     # self.dataset.columns = ["time","open"]

    # def send_signal(self,index,tick,Type,amount = 0.5,order_id = None):
    #     if Type == "BUY":
    #         if (self.budget * self.leverage) >= (amount * self.lot):
    #             time = index
    #             value = tick[4] - (self.spread/2)
    #             price = (amount * self.lot) * (value)
    #             self.order.append([time,Type,amount,value,price])
    #             self.open.append([time,Type,amount,value,price])
    #         else:
    #             print("You cant afford order!! You lose!!")
    #             self.end = True
    #         pass
    #     elif Type == "SELL":
    #         if (self.budget * self.leverage) >= (amount * self.lot):
    #             time = index
    #             value = tick[4] + (self.spread/2)
    #             price = (amount * self.lot) * (value)
    #             self.order.append([time,Type,amount,value,price])
    #             self.open.append([time,Type,amount,value,price])
    #         else:
    #             print("You cant afford order!! You lose!!")
    #             self.end = True
    #         pass
    #     elif Type == "close" and order_id != None:
    #         mark = self.order.pop(order_id)
    #         if mark[1] == "BUY":
    #             value = tick[4] - (self.spread/2)
    #             price = (mark[2] * self.lot) * value
    #             total = price - mark[4]
    #             pass
    #         elif mark[1] == "SELL":
    #             value = tick[4] + (self.spread/2)
    #             price = (mark[2] * self.lot) * value
    #             total = mark[4] - price
    #             pass
    #         if total > 0:
    #             self.profit += total
    #         else: self.loss += total
    #         self.budget += total
    #         time = index
    #         Type = mark[1]
    #         amount = mark[2]
    #         time_open = mark[0]
    #         self.close.append([time,Type,amount,value,price])
    #         self.transection.append([time_open,time,Type,amount,total])
    #         pass

    # def run(self,strategy,money = "TEST",start_year = None,timeframe = None,end_year = None):
    #     if (not self.ready):
    #         self.GetData(money,start_year,timeframe,end_year)
    #     print("=======================================================")
    #     print("                 start simulation                      ")
    #     print("=======================================================")
    #     self.order = []
    #     self.open = []
    #     self.close = []
    #     self.transection = []
    #     self.trend = None
    #     self.profit = 0
    #     self.loss = 0
    #     for index,tick in self.dataset.iterrows() :
    #         s = strategy(index)
    #         self.trend = s.next(index,tick)
    #         if self.end : break
    #         ### percent ###
    #         percentage = (index/len(self.dataset))*100
    #         percentage = round(percentage,2)
    #         quarter = int((index/len(self.dataset))*25)
    #         Done = "#" * quarter
    #         remain = " " * (25-quarter)
    #         print("["+Done+remain+"] " + "completed : "+ str(percentage) + " %")
    #     ## calculate part ##
    #     df_transection = pd.DataFrame(self.transection)
    #     df_transection.columns =  ['OpenOrder','CloseOrder','Type','lot','outcome']
    #     T_loss = df_transection[df_transection.outcome < 0]
    #     T_profit = df_transection[df_transection.outcome >= 0]
    #     profit_per = (len(T_profit)/len(self.transection)) * 100
    #     loss_per = (len(T_loss)/len(self.transection)) * 100
    #     print("=======================================================")
    #     print("                   end simulation                      ")
    #     print("=======================================================")
    #     print("===================================== report =====================================")
    #     print("Money : " + self.currancy + "    " + "period : " + self.timeframe + "    " + "Bars in test : " + str(len(self.dataset))+ "    " +"Initial_budget : " + str(self.balance) )
    #     print("Gross_Porfit : "+str(round(self.profit,2))+ "    " + "Gross_Loss : "+str(round(self.loss,2))+ "    " + "Total net profit : " + str(round(self.loss + self.profit,2)) + "    " + "profit factor : " + str(round(abs(self.profit/self.loss),2)) )
    #     print("Total_Trade : " + str(len(self.transection)) + "    " + "Profit_trade : " + str(len(T_profit)) + "(" +str(round(profit_per,2))+ "%)"+ "    " + "Loss_trade : " + str(len(T_loss)) + "(" +str(round(loss_per,2))+ "%)" )
    #     print("==================================================================================")
    #     self.plot_graph()


    # def plot_graph(self):
    #     opendata = pd.DataFrame(self.open)
    #     opendata.columns = ['time','type','amount','value','price']
    #     closedata = pd.DataFrame(self.close)
    #     closedata.columns = ['time','type','amount','value','price']
    #     opendata_BUY = opendata.groupby('type').get_group('BUY')
    #     opendata_SELL = opendata.groupby('type').get_group('SELL')
    #     closedata_BUY = closedata.groupby('type').get_group('BUY')
    #     closedata_SELL = closedata.groupby('type').get_group('SELL')
    #     fig = make_subplots(rows=self.graph_row, cols=1, 
    #                 shared_xaxes=True, 
    #                 vertical_spacing=0.02)
    #     fig.add_trace(
    #         go.Candlestick(x=[x for x in range (len(self.dataset))],## x=self.dataset.loc[:,"time"]
    #             open=self.dataset.loc[:,"open"],
    #             high=self.dataset.loc[:,"high"],
    #             low=self.dataset.loc[:,"low"],
    #             close=self.dataset.loc[:,"close"]),row=1,col=1
    #     )
    #     fig.add_trace(
    #         go.Scatter(
    #             x= opendata_SELL['time'],
    #             y= opendata_SELL['value'],
    #             mode='markers',
    #             name="order sell",
    #             marker_color='rgba(255, 0, 255, 1)'
    #         ),row=1,col=1
    #     )
    #     fig.add_trace(
    #         go.Scatter(
    #             x= closedata_SELL['time'],
    #             y= closedata_SELL['value'],
    #             mode='markers',
    #             name="close sell",
    #             marker_color='rgba(132, 0, 132, 1)'
    #         ),row=1,col=1
    #     )
    #     fig.add_trace(
    #         go.Scatter(
    #             x= opendata_BUY['time'],
    #             y= opendata_BUY['value'],
    #             mode='markers',
    #             name="order buy",
    #             marker_color='rgba(0, 255, 0, 1)' 
    #         ),row=1,col=1
    #     )
    #     fig.add_trace(
    #         go.Scatter(
    #             x= closedata_BUY['time'],
    #             y= closedata_BUY['value'],
    #             mode='markers',
    #             name="close buy",
    #             marker_color='rgba(0, 132, 0, 1)' 
    #         ),row=1,col=1
    #     )

    #     ############ test ####################
    #     if self.plot_test:
    #         ema12 = ta.SMA(self.dataset.loc[:,"close"],12)
    #         ema36 = ta.SMA(self.dataset.loc[:,"close"],36)
    #         fig.add_trace(
    #             go.Scatter(
    #                 x=[x for x in range (len(self.dataset))],
    #                 y = ema12,
    #                 mode = "lines",
    #                 name = "ema12"
    #             ),col=1,row=1
    #         )
    #         fig.add_trace(
    #             go.Scatter(
    #                 x=[x for x in range (len(self.dataset))],
    #                 y = ema36,
    #                 mode = "lines",
    #                 name = "ema36"
    #             ),col=1,row=1
    #         )

    #     fig.update_layout(xaxis_rangeslider_visible=False)
    #     fig.show()
    #     pass


    # ## ========================= function indicator ================================

    # def SMA(self,index,Range):
    #     if index < Range :
    #         return [0,0]
    #     start = index - Range
    #     stop = index 
    #     data = self.dataset.loc[start:stop,"close"]
    #     sma = ta.SMA(data,Range)
    #     sma = np.array(sma)
    #     sma = sma[~(np.isnan(sma))]
    #     return sma

    # def EMA (self,index,Range):
    #     if index < Range :
    #         return [0,0]
    #     start = index - (Range)
    #     stop = index 
    #     data = self.dataset.loc[start:stop,"close"]
    #     ema = ta.EMA(data,Range)
    #     ema = np.array(ema)
    #     ema = ema[~(np.isnan(ema))]
    #     return ema

    # def ADX (self,index,Range):
    #     if index == 0 :
    #         self.graph_row += 1 
    #     if index < Range *2 :
    #         return [0,0]
    #     start = index - (Range*2)
    #     stop = index 
    #     data_close = self.dataset.loc[start:stop,"close"]
    #     data_high = self.dataset.loc[start:stop,"high"]
    #     data_low = self.dataset.loc[start:stop,"low"]
    #     adx = ta.ADX(data_high,data_low,data_close,timeperiod=Range)
    #     adx = np.array(adx)
    #     adx = adx[~(np.isnan(adx))]
    #     return adx


    # def stop_loss(self):
    #     pass

    # def tailing_stop(self):
    #     pass

    # def Crossover(self,value1,value2):
    #     signal = bool(0)
    #     if value1[0] > value2[0] and value1[1] < value2[1]:
    #         signal = bool(1)
    #     return signal

    # def SortOut(self):
    #     pass

    # def Touch(self,tick,value2):
    #     signal = False
    #     # if tick[2] >= value2[0] or tick[2] <= value2[1]:
    #     #     signal = True
    #     # if tick[3] <= value2[0] or tick[3] >= value2[1]:
    #     #     signal = True
    #     if value2[0] < value2[1]:
    #         if value2[1] <= tick[2] <= value2[0] or value2[1] <= tick[3] <= value2[0] :
    #             signal = True
    #     if value2[0] > value2[1]:
    #         if value2[0] <= tick[2] <= value2[1] or value2[0] <= tick[3] <= value2[1] :
    #             signal = True
    #     return signal








