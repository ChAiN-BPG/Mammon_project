import pandas as pd
import numpy as np
import talib as ta 
import sys
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import MetaTrader5 as mt5 

class traderFX:
    def __init__(self,balance = 200,lot = "standard",leverage = "1:100",spread = 0.00022):
        ## ประกาศตัวแปลที่จำเป็นต้องใช้ เงินที่จะใช้ ปร้เภท lot lerverage และ speard
        self.balance = balance
        self.budget = balance
        self.spread = spread
        if lot == "standard":
            res = 100000
        elif lot == "mini":
            res = 10000
        elif lot == "micro":
            res = 1000
        elif lot == "nano":
            res = 100
        self.lot = res
        res = leverage.split(":")
        self.leverage =  int(res[1])
        ## ========== parameter for simmulate =============
        self.end = False
        self.ready = False
        ## ========== for graph ================
        self.graph_row = 1
        pass
        



    def get_data(self,currancy = "TEST",timeframe = "H1",start_year = 2004,stop_year = None):
        if currancy == "TEST":
            data = pd.read_excel('data/Test_data/sin_dataset.xlsx',header=None)
        else:
            data = pd.read_excel('data/TimeFrame/'+ str(start_year)+ '/'+ currancy +'-'+ str(start_year)+'_'+ timeframe +'.xlsx',header=None)
            data = data.iloc[:,:5]
        if stop_year != None :
            for Index in range(start_year+1,stop_year+1):
                resdata = pd.read_excel('data/TimeFrame/'+ str(Index)+ '/'+ currancy +'-'+ str(Index)+'_'+ timeframe +'.xlsx',header=None)
                resdata = resdata.iloc[:,:5]
                data =  data.append(resdata,ignore_index=True)
        if currancy == "TEST":
            self.timeframe = "None"
            self.years = "None"
        else:
            self.timeframe = timeframe
            self.years = str(start_year) + " - " + str(stop_year)
        data.columns = ["time","open","high","low","close"]
        self.currancy = currancy
        self.dataset = data
        self.ready = True
        pass
        ## ดึงค่าเงินจาก file ประกาศตัวแปรเป็น คู่เงิน timeframe ปีที่ใช้





    def send_order(self,index,tick,Type,amount = 0.5,order_id = None,TP = None,SL = None):
        if Type == "BUY":
            if (self.budget * self.leverage) >= (amount * self.lot):
                time = index
                value = tick[4] - (self.spread/2)
                price = (amount * self.lot) * (value)
                self.order.append([time,Type,amount,value,price,TP,SL])
                self.open.append([time,Type,amount,value,price])
            else:
                print("You cant afford order!! You lose!!")
                self.end = True
            pass
        elif Type == "SELL":
            if (self.budget * self.leverage) >= (amount * self.lot):
                time = index
                value = tick[4] + (self.spread/2)
                price = (amount * self.lot) * (value)
                self.order.append([time,Type,amount,value,price,TP,SL])
                self.open.append([time,Type,amount,value,price])
            else:
                print("You cant afford order!! You lose!!")
                self.end = True
            pass
        elif Type == "close" and order_id != None:
            mark = self.order.pop(order_id)
            if mark[1] == "BUY":
                value = tick[4] - (self.spread/2)
                price = (mark[2] * self.lot) * value
                total = price - mark[4]
                pass
            elif mark[1] == "SELL":
                value = tick[4] + (self.spread/2)
                price = (mark[2] * self.lot) * value
                total = mark[4] - price
                pass
            if total > 0:
                self.profit += total
            else: self.loss += total
            self.budget += total
            time = index
            Type = mark[1]
            amount = mark[2]
            time_open = mark[0]
            self.close.append([time,Type,amount,value,price])
            self.transection.append([time_open,time,Type,amount,total])
            pass
        ## ส่งคำสั่งทั้งหมด order buy , order sell , close order 




    def run (self,strategy):
        ## สั่ง simmulate รับ class ที่เป็น strategy มา 
        if (not self.ready) :
            self.get_data()
        print("============================================")
        print("              start simmulate               ")
        print("============================================")
        self.order = []
        self.open = []
        self.close = []
        self.transection = []
        self.profit = 0
        self.loss = 0
        Strategy = strategy(self.dataset)
        
        for index,tick in self.dataset.iterrows() :
            if index == 0 :
                continue
            Strategy.next(index,tick)
            if self.end : break
            percentage = (index/len(self.dataset))*100
            percentage = round(percentage,2)
            quarter = int((index/len(self.dataset))*25)
            Done = "#" * quarter
            remain = " " * (25-quarter)
            print("["+Done+remain+"] " + "completed : "+ str(percentage) + " %")
        
        ## ====================== calculate ========================
        df_transection = pd.DataFrame(self.transection)
        df_transection.columns =  ['OpenOrder','CloseOrder','Type','lot','outcome']
        T_loss = df_transection[df_transection.outcome < 0]
        T_profit = df_transection[df_transection.outcome >= 0]
        profit_per = (len(T_profit)/len(self.transection)) * 100
        loss_per = (len(T_loss)/len(self.transection)) * 100
        print("=======================================================")
        print("                   end simulation                      ")
        print("=======================================================")
        print("===================================== report =====================================")
        print("Money : " + self.currancy + "    " + "period : " + self.timeframe + "    " + "Bars in test : " + str(len(self.dataset))+ "    " +"Initial_budget : " + str(self.balance) )
        print("Gross_Porfit : "+str(round(self.profit,2))+ "    " + "Gross_Loss : "+str(round(self.loss,2))+ "    " + "Total net profit : " + str(round(self.loss + self.profit,2)) + "    " + "profit factor : " + str(round(abs(self.profit/self.loss),2)) )
        print("Total_Trade : " + str(len(self.transection)) + "    " + "Profit_trade : " + str(len(T_profit)) + "(" +str(round(profit_per,2))+ "%)"+ "    " + "Loss_trade : " + str(len(T_loss)) + "(" +str(round(loss_per,2))+ "%)" )
        print("==================================================================================")
        self.plot_graph()
        

    def plot_graph(self):
        opendata = pd.DataFrame(self.open)
        opendata.columns = ['time','type','amount','value','price']
        closedata = pd.DataFrame(self.close)
        closedata.columns = ['time','type','amount','value','price']
        opendata_BUY = opendata.groupby('type').get_group('BUY')
        opendata_SELL = opendata.groupby('type').get_group('SELL')
        closedata_BUY = closedata.groupby('type').get_group('BUY')
        closedata_SELL = closedata.groupby('type').get_group('SELL')
        
        self.graph.add_trace(
            go.Candlestick(x=[x for x in range (len(self.dataset))],## x=self.dataset.loc[:,"time"]
                open=self.dataset.loc[:,"open"],
                high=self.dataset.loc[:,"high"],
                low=self.dataset.loc[:,"low"],
                close=self.dataset.loc[:,"close"]),row=1,col=1
        )
        self.graph.add_trace(
            go.Scatter(
                x= opendata_SELL['time'],
                y= opendata_SELL['value'],
                mode='markers',
                name="order sell",
                marker_color='rgba(255, 0, 255, 1)'
            ),row=1,col=1
        )
        self.graph.add_trace(
            go.Scatter(
                x= closedata_SELL['time'],
                y= closedata_SELL['value'],
                mode='markers',
                name="close sell",
                marker_color='rgba(132, 0, 132, 1)'
            ),row=1,col=1
        )
        self.graph.add_trace(
            go.Scatter(
                x= opendata_BUY['time'],
                y= opendata_BUY['value'],
                mode='markers',
                name="order buy",
                marker_color='rgba(0, 255, 0, 1)' 
            ),row=1,col=1
        )
        self.graph.add_trace(
            go.Scatter(
                x= closedata_BUY['time'],
                y= closedata_BUY['value'],
                mode='markers',
                name="close buy",
                marker_color='rgba(0, 132, 0, 1)' 
            ),row=1,col=1
        )
        self.graph.update_layout(xaxis_rangeslider_visible=False)
        self.graph.show()

    def Crossover(self,index,value1,value2):
        signal = bool(0)
        if value1[index-1] > value2[index-1] and value1[index] < value2[index]:
            signal = bool(1)
        return signal

    def Crossprice(self,index,value):
        signal = False
        if self.dataset.loc[index,"low"] <= value[index] <= self.dataset.loc[index,"high"] :
            signal = True
        return signal

    def stop_loss (self,index,tick,id):
        x = self.order[id]
        if x[1] == "BUY":
            if tick[4] <= x[6]:
                self.send_order(index,tick,"close",order_id=id)
        if x[1] == "SELL":
            if tick[4] >= x[6]:
                self.send_order(index,tick,"close",order_id=id)

    def tailing_stop(self):

        pass

    def set_indicator(self,list_ind):
        set_indicator = []
        for x in list_ind:
            if x[0] in ["MACD","ADX"] :
                self.graph_row += 1
        self.graph = make_subplots(rows=self.graph_row, cols=1, shared_xaxes=True, vertical_spacing=0.02)
        count_row = 2
        for x in list_ind:
            if x[0] == "EMA":
                data = ta.EMA(self.dataset.loc[:,"close"],x[1])
                # set_indicator.append(data)
                self.graph.add_trace(
                    go.Scatter(
                        x = [x for x in range(len(data))],
                        y = data,
                        mode = "lines",
                        name = "EMA" + str(x[1]) 
                    ),col=1 , row = 1
                )
                data = np.array(data)
                data = np.where(np.isnan(data),0,data)
                data = data.tolist()
                set_indicator.append(data)


            if x[0] == "ADX" :
                data = ta.ADX(self.dataset.loc[:,"high"],self.dataset.loc[:,"low"],self.dataset.loc[:,"close"],x[1])
                # set_indicator.append(data)
                self.graph.add_trace(
                    go.Scatter(
                        x=[x for x in range(len(data))],
                        y = data,
                        mode = "lines",
                        name = "ADX" + str(x[1])
                    ),col=1,row = count_row
                )
                data = np.array(data)
                data = np.where(np.isnan(data),0,data)
                data = data.tolist()
                set_indicator.append(data)
                count_row += 1

            if x[0] == "MACD":
                macd, macdsignal, macdhist = ta.MACD(self.dataset.loc[:,"close"],x[1],x[2],x[3])
                self.graph.add_trace(
                    go.Scatter(
                        x=[x for x in range(len(data))],
                        y = macd,
                        mode = "lines",
                        name = "macd"
                    )
                )
                self.graph.add_trace(
                    go.Scatter(
                        x=[x for x in range(len(data))],
                        y = macdsignal,
                        mode = "lines",
                        name = "macd"
                    )
                )
                # self.graph.add_trace(
                #     go.
                # )
        return set_indicator
## ================================ test ==================================



test = traderFX(balance=200,lot= "mini")
test.get_data(currancy="GBPUSD",start_year=2004)
test.last_cross = None
# # print(test.balance)
# # print(test.budget)
# # print(test.spread)
# # print(test.lot)
# # print(test.leverage)
class test_strategy:
    def __init__(self,dataset):
        # self.sma12 = ta.SMA(dataset.loc[:,"close"],12)
        # self.sma36 = ta.SMA(dataset.loc[:,"close"],36)
        list_indicator = test.set_indicator([["EMA",12],["EMA",36],["ADX",7]])
        self.ema12 = list_indicator[0]
        self.ema36 = list_indicator[1]
        self.adx14 = list_indicator[2]
    def next (self,index,tick):
        if test.Crossover(index,self.ema12,self.ema36):
            test.last_cross = "SELL"
        if test.Crossover(index,self.ema36,self.ema12):
            test.last_cross = "BUY"
        if len(test.order) >= 1:
            if self.adx14[index] < 40:
                test.send_order(index,tick,"close",order_id=0)
            else : test.stop_loss(index,tick,0)
        if len(test.order) < 1 :
            if test.last_cross == "SELL" and test.Crossprice(index,self.ema12) and self.adx14[index] > 40:
                SL = self.ema36[index] if self.ema36[index] > tick[4] + 0.0003 else tick[4] + 0.0003
                test.send_order(index,tick,"SELL",SL=SL)
                test.last_cross = None
            if test.last_cross == "BUY" and test.Crossprice(index,self.ema12) and self.adx14[index] > 40:
                SL = self.ema36[index] if self.ema36[index] < tick[4] + 0.0003 else tick[4] + 0.0003
                test.send_order(index,tick,"BUY",SL=SL)
                test.last_cross = None

test.run(test_strategy)
# # print(test.dataset)
# # print(test.ready)
