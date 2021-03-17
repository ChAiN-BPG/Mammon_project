import pandas as pd
import numpy as np
import talib as ta 
import sys
import plotly.graph_objects as go
import datetime
from plotly.subplots import make_subplots
import MetaTrader5 as mt5 

class traderFX:
    def __init__(self,balance = 200,lot = "standard",leverage = "1:100",spread = 0.00022,path_save = "test/test_something.csv"):
        ## ประกาศตัวแปลที่จำเป็นต้องใช้ เงินที่จะใช้ ปร้เภท lot lerverage และ speard
        self.path = path_save
        self.balance = balance
        self.budget = balance
        self.spread = spread
        self.swap_long = -0.2
        self.swap_short = -2.2
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
        



    def get_data(self,currancy = "EURUSD",timeframe = "H1",start_year = 2011):
        # if currancy == "TEST":
        #     data = pd.read_excel('data/Test_data/sin_dataset.xlsx',header=None)
        # else:
        data = pd.read_excel('data/dataset/XM_'+ currancy + '-'+ str(start_year) + '_H1.xlsx',header=None)
        for x in range(len(data)):
            date = data.iloc[x,0].split('.')
            time = data.iloc[x,1].split(':')
            data.iloc[x,0] = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),int(time[0]),int(time[1]))
        # if stop_year != None :
        #     for Index in range(start_year+1,stop_year+1):
        #         resdata = pd.read_excel('data/TimeFrame/'+ str(Index)+ '/'+ currancy +'-'+ str(Index)+'_'+ timeframe +'.xlsx',header=None)
        #         resdata = resdata.iloc[:,:5]
        #         data =  data.append(resdata,ignore_index=True)
        # if currancy == "TEST":
        #     self.timeframe = "None"
        #     self.years = "None"
        # else:
        self.timeframe = timeframe
        self.years = str(start_year) 
        data.columns = ['date','time','open','high','low','close','volume']
        self.currancy = currancy
        self.dataset = data
        self.ready = True
        pass
        ## ดึงค่าเงินจาก file ประกาศตัวแปรเป็น คู่เงิน timeframe ปีที่ใช้





    def send_order(self,index,tick,Type,amount = 0.5,order_id = None,TP = None,SL = None):
        if Type == "BUY":
            if (self.budget * self.leverage) >= (amount * self.lot):
                time = tick[0]
                value = tick[4] + (self.spread/2)
                price = (amount * self.lot) * (value)
                self.order.append([time,Type,amount,value,price,TP,SL])
                self.open.append([time,Type,amount,value,price])
                self.step_action = "ORDER_BUY"
            else:
                print("You cant afford order!! You lose!!")
                self.end = True
            pass
        elif Type == "SELL":
            if (self.budget * self.leverage) >= (amount * self.lot):
                time = tick[0]
                value = tick[4] - (self.spread/2)
                price = (amount * self.lot) * (value)
                self.order.append([time,Type,amount,value,price,TP,SL])
                self.open.append([time,Type,amount,value,price])
                self.step_action = "ORDER_SELL"
            else:
                print("You cant afford order!! You lose!!")
                self.end = True
            pass
        elif Type == "close" and order_id != None:
            mark = self.order.pop(order_id)
            spending_time = mark[0] - tick[0]
            night = 0
            if spending_time.days > 0 or spending_time.seconds >= 3600 :
                night = round(((spending_time.days * 3600) + spending_time.seconds)/3600 )
            if mark[1] == "BUY":
                value = tick[4] - (self.spread/2)
                price = (mark[2] * self.lot) * value
                total = price - mark[4] - (night * self.swap_long)
                self.step_action = "CLOSE_BUY"
                pass
            elif mark[1] == "SELL":
                value = tick[4] + (self.spread/2)
                price = (mark[2] * self.lot) * value
                total = mark[4] - price - (night * self.swap_short)
                self.step_action = "CLOSE_SELL"
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
        self.action = []
        self.profit = 0
        self.loss = 0
        Strategy = strategy(self.dataset)
        
        for index,tick in self.dataset.iterrows() :
            self.step_action = "HOLD"
            if index == 0 :
                self.action.append(self.step_action)
                continue
            Strategy.next(index,tick)
            self.action.append(self.step_action)
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
        # self.plot_graph()
        # self.write_data(round(self.loss + self.profit,2),len(T_profit),len(T_loss))
        self.write_action()
        






    def write_action(self):
            res = pd.DataFrame(self.action)
            res.to_csv(self.path)
            pass

    def write_data(self,Profit,P_order,L_order):
        res = [self.years,Profit,str(P_order)+" ("+str(round((P_order/len(self.transection)) * 100,1))+"%)",str(L_order)+" ("+str(round((L_order/len(self.transection)) * 100,1))+"%)"]
        res = pd.DataFrame([res])
        res.columns = ["year","Profit","P_order","L_order"]
        res.to_csv(self.path)
        pass


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

    def Take_profit(self,index,tick,id):
        x = self.order[id]
        if x[1] == "BUY":
            if tick[4] >= x[5]:
                self.send_order(index,tick,"close",order_id=id)
        if x[1] == "SELL":
            if tick[4] <= x[5]:
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
                        x = [x for x in range(len(macd))],
                        y = macd,
                        mode = "lines",
                        name = "macd"
                    ),row= count_row,col = 1
                )
                self.graph.add_trace(
                    go.Scatter(
                        x = [x for x in range(len(macdsignal))],
                        y = macdsignal,
                        mode = "lines",
                        name = "macdsignal"
                    ),row=count_row,col=1
                )
                self.graph.add_trace(
                    go.Scatter(
                        x = [x for x in range(len(macdhist))],
                        y = macdhist,
                        mode = "lines",
                        name = "macdsignal"
                    ),row=count_row,col=1
                )
                macd = np.array(macd)
                macdhist = np.array(macdhist)
                macdsignal = np.array(macdsignal)
                macd = np.where(np.isnan(macd),0,macd)
                macdhist = np.where(np.isnan(macdhist),0,macdhist)
                macdsignal = np.where(np.isnan(macdsignal),0,macdsignal)
                macd = macd.tolist()
                macdhist = macdhist.tolist()
                macdsignal = macdsignal.tolist()
                data = []
                data.append(macd)
                data.append(macdsignal)
                data.append(macdhist)
                set_indicator.append(data)
                count_row += 1
            
            if x[0] == "BB":
                B_up,B_mindle,B_down = ta.BBANDS(self.dataset.loc[:,"close"],x[1],x[2],x[2],0)
                self.graph.add_trace(
                    go.Scatter(
                        x = [x for x in range(len(B_up))],
                        y = B_up,
                        mode = "lines",
                        name = "B_up"
                    ),row=1,col=1
                )
                self.graph.add_trace(
                    go.Scatter(
                        x = [x for x in range(len(B_mindle))],
                        y = B_mindle,
                        mode = "lines",
                        name = "B_mindle"
                    ),row=1,col=1
                )
                self.graph.add_trace(
                    go.Scatter(
                        x = [x for x in range(len(B_down))],
                        y = B_down,
                        mode = "lines",
                        name = "B_down"
                    ),row=1,col=1
                )
                B_up = np.array(B_up)
                B_mindle = np.array(B_mindle)
                B_down = np.array(B_down)
                B_up = np.where(np.isnan(B_up),0,B_up)
                B_mindle = np.where(np.isnan(B_mindle),0,B_mindle)
                B_down = np.where(np.isnan(B_down),0,B_down)
                B_up = B_up.tolist()
                B_mindle = B_mindle.tolist()
                B_down = B_down.tolist()
                data = []
                data.append(B_mindle)
                data.append(B_up)
                data.append(B_down)
                set_indicator.append(data)
                count_row += 1
        return set_indicator
## ================================ test ==================================




