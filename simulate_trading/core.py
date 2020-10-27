import MetaTrader5 as mt5 
import matplotlib.pyplot as plt 
from datetime import datetime
import pandas as pd
import numpy as np
import sys
import talib as ta 
from pickle import load
from keras.models import load_model
import plotly.graph_objects as go

## เพิ่ม value ในการลงทุนตามเงินลงทุน / do it 

class Simforex :
    def __init__ (self):
        self.order = []
        self.open = []
        self.close = []
        self.loss = 0
        self.profit = 0
        self.type_money = ""
        self.period = ""
        self.budget = 10000
        self.balance = 10000
        self.risk = 0
        self.spread = 0.00022
        self.leverage = 1
        self.lot = 100000
        self.data = []
        self.transection = []
        self.stopLoss = 150
        self.Tstop = 150
        ## ต้องเก็บ เวลาที่เข้าออกของแต่ละ order // done

    def add_stopLoss(self,pips):
        self.stopLoss = pips
        

    def add_Tstop(self,pips):
        self.Tstop = pips
        

    def add_budget (self,amount):
        self.budget = amount
        self.balance = amount
        self.risk = amount /100
    
    def change_risk (self,amount):
        self.risk = amount

    def set_lot (self,size):
        if size == "standard":
            self.lot = 100000
        elif size == "mini":
            self.lot = 10000
        elif size == "micro":
            self.lot = 1000
        elif size == "nano":
            self.lot = 100
        else : sys.exit("What size is it?!")
    

    def set_Leverage (self,ratio):
        res = ratio.split(":")
        self.leverage =  int(res[1])


    
    def add_period (self,money,start_time,period,stop_time = None):
        ## เปลี่ยนวิธี fatch ข้อมูลใหม่ เพราะ เราจัด file ใหม่ // done
        data = pd.read_excel('data/TimeFrame/'+ str(start_time)+ '/'+ money +'-'+ str(start_time)+'_'+ period +'.xlsx',header=None)
        if stop_time == None:
            self.period = str(period)
            self.type_money = money
            self.data = data
            return
        for Index in range(start_time+1,stop_time+1):
            resdata = pd.read_excel('data/TimeFrame/'+ str(Index)+ '/'+ money +'-'+ str(Index)+'_'+ period +'.xlsx',header=None)
            data = pd.concat([data,resdata])
        self.period = str(period)
        self.type_money = money
        self.data = data


    def add_indicator(self,active):
        if len(active) != 7 :
            print("error")
            return
        self.signal = np.zeros((7,len(self.data)-1))
        self.active = active
        ## MACD
        if active[0] == 1 :
            macd, macdsignal, _ = ta.MACD(self.data[4], fastperiod=12, slowperiod=26, signalperiod=9)
            macd = np.where(np.isnan(macd),0,macd)
            macdsignal = np.where(np.isnan(macdsignal),0,macdsignal)
            macd_signal = np.where((macd > macdsignal),1.0,0.0)
            macd_threshold = np.where(((macd <= 0.00002) & (macd >= -0.00002)), 0.0 , 1.0)
            macd_threshold = np.delete(macd_threshold,0,0)
            macd_signal = np.diff(macd_signal)
            macd_signal = np.where(macd_threshold == 1.0 ,macd_signal,0.0)
            macd_center = np.where(macd > 0 ,-1.0,1.0)
            macd_center = np.delete(macd_center,0,0)
            macd_signal = np.where(macd_signal == macd_center, macd_signal,0)

            self.signal[0] = macd_signal
        ## MA
        if active[1] == 1:
            ema = ta.EMA(self.data[4],timeperiod=26)
            ema = np.where(np.isnan(ema),0,ema)
            ema_signal = np.diff(ema)
            ema_signal = np.where(ema_signal >= 0,1.0,-1.0)
            self.signal[1] = ema_signal
        ## STOCH
        ## FIBO 
        ## SAR
        pass

    def stop_loss(self,num_order,data):
        order = self.order[num_order]
        SL_close = bool(0) 
        cur_pips = order[4] - data[4] if order[1] == "SELL" else data[4] - order[4] 
        ## check order that loss too much
        if -(cur_pips * 100000) > self.stopLoss : SL_close = bool(1)
        return SL_close

    def trailing_stop(self,num_order,data):  ### /// ใช้งานไม่ได้
        order = self.order[num_order]
        TS_close = bool(0)
        if abs(order[5]) == 9999:
            if data[4] > order[4]  + (self.Tstop/100000) and order[2] == "BUY" :
                order[5] = order[4]
            if data[4] < order[4]  - (self.Tstop/100000) and order[2] == "SELL" :
                order[5] = order[4]
            return

        expect_value = order[5] + (self.Tstop/100000) if order[2] == "BUY" else order[5] - (self.Tstop/100000)
        # ## up date Tstop
        # if data[4] > expect_value and order[2] == "BUY" :
        #     self.order[num_order][5] += (data[4] - expect_value) 
        # if data[4] < expect_value and order[2] == "SELL" :
        #     self.order[num_order][5] += -(data[4] - expect_value)
        # ## check order that has to set trailing_stop 
        # if data[4] < order[5] and order[2] == "BUY" :
        #     Is_close = bool(1)
        # if data[4] > order[5] and order[2] == "SELL" :
        #     Is_close = bool(1)
        

        if order[1] == "BUY":
            
            if data[4] < order[5] :
                TS_close = bool(1)
            elif data[4] > expect_value :
                self.order[num_order][5] += (data[4] - expect_value) 
        else:
            if data[4] > order[5] :
                TS_close = bool(1)
            elif data[4] < expect_value :
                self.order[num_order][5] += -(expect_value - data[4])
            
        return TS_close
        


    def _order_ (self,data,Type,amount): ## ใช้กรณีของ ค่าเงินเดียว (GBP / USD) เท่านั้น // do it later
        if Type == "HOLD" : return
        if (self.budget * self.leverage) >= (amount * self.lot):
            trade_value = data[4] + (self.spread/2) if Type == "BUY" else data[4] - (self.spread/2)
            op = (amount * self.lot) * (trade_value)
        else :
            print("You cant afford order!! You lose!!")
            self.budget = -1
            return
        order_open = data[0]
        order_type = Type
        open_price = op
        open_value = trade_value
        T_Stop = -9999 if Type == "BUY" else 9999
        self.order.append([order_open,order_type,amount,open_price,open_value,T_Stop])
        self.open.append([order_open,order_type,amount,open_price,open_value])

    def _close_ (self,data,num_order):
        Order = self.order.pop(num_order)

        ## ลบ order ที่ต้องการปิดด้วย // done (pop ออกไปแล้ว)
        ## ที่จริง... มันต้องบันทึกการซื้อ-ขายทั้งหมดด้วย // done
        ## เรื่องของอัตราการแลกเปลี่ยนยังคงเป็น ต่าเงินเดียวอยู่ // do it later
        # cp = (Order[2] * self.lot) * (data[1])
        if Order[1] == "BUY":
            cp = (Order[2] * self.lot) * (data[1] - (self.spread/2))
            total = cp - Order[3]
        elif Order[1] == "SELL" :
            cp = (Order[2] * self.lot) * (data[1] + (self.spread/2))
            total = Order[3] - cp
        else :
            return
        if total >= 0 :
            self.profit += total
        else : self.loss += total
        self.budget += total
        Order_close = data[0]
        Close_type = Order[1]
        amount = Order[2]
        close_price = cp
        close_value = data[4]
        self.close.append([Order_close,Close_type,amount,close_price,close_value])
        ## บันทึก transection ด้วย // done
        Type = Order[1] 
        OpenOrder = Order[0]
        CloseOrder = data[0]
        lot = round(Order[2],2)
        Profit = round(self.profit,2)
        Loss = round(self.loss,2)
        budget = round(self.budget,2)
        outcome = round(total,2)
        self.transection.append([Type,OpenOrder,CloseOrder,lot,outcome,Profit,Loss,budget])


    def run_sim(self,method):
        print("=======================================================")
        print("                 start simulation                      ")
        print("=======================================================")
        length = len(self.data)
        if length == 0:
            print("there is no data for simulate")
            return
        ## เตรียม model and encoder
        if method > 0:
            scaler = load(open('test/scaler.pkl', 'rb'))
            emcoder = load(open('test/onehot.pkl', 'rb'))
            model = load_model('test/location.h5') 
        for index,tick in self.data.iterrows() :
            ## วน for ผ่าน method ที่ตั้งไว้ // done
            if method == 0 :
                self.NOOB_method(tick,index)
            elif method == 1:
                self.first_method(tick,index,model,scaler,emcoder)
            elif method == 2:
                self.diff_method(tick,index,model,scaler,emcoder)
            elif method == -1 :
                self.first_EA(tick,index)
            ## check ด้วยว่า order ทั้งหมดยังไม่ได้ ติดลบจนเท่ากับ budget // done (แต่ยังเป็นระบบคู่เงินเดียว)
            price_total = 0
            for order in self.order:
                price_tick = (order[2]*self.lot)*(tick[4])
                if order[1] == 'BUY':
                    res = price_tick - order[3]
                else :
                    res = order[3] - price_tick
                price_total += res
            if ((price_total*(-1))>=self.budget) or (self.budget <= 0) : 
                print("Game over")
                break
            ## ทำ percentage // done
            percentage = (index/length)*100
            percentage = round(percentage,2)
            quarter = int((index/length)*25)
            Done = "#" * quarter
            remain = " " * (25-quarter)
            print("["+Done+remain+"] " + "completed : "+ str(percentage) + " %")
        
        ## ทำ visulize ให้เข้าใจง่าย // still understandable
        # try:
        
        ## ------------------------------------ prepare data ------------------------------------------------------
        Alldata = pd.DataFrame(self.data)
        opendata = pd.DataFrame(self.open)
        opendata.columns = ['order_open','order_type','amount','open_price','open_value']
        closedata = pd.DataFrame(self.close)
        closedata.columns = ['order_close','close_type','amount','close_price','close_value']
        opendata_BUY = opendata.groupby('order_type').get_group('BUY')
        opendata_SELL = opendata.groupby('order_type').get_group('SELL')
        closedata_BUY = closedata.groupby('close_type').get_group('BUY')
        closedata_SELL = closedata.groupby('close_type').get_group('SELL')

        ## แสดง transection ออกมาเป็น csv // done

        df_transection = pd.DataFrame(self.transection)
        df_transection.columns =  ['Type','OpenOrder','CloseOrder','lot','outcome','Profit','Loss','budget']
        df_transection.to_csv('test/transaction/transection.csv')
        T_loss = df_transection[df_transection.outcome < 0]
        T_profit = df_transection[df_transection.outcome >= 0]
        profit_per = (len(T_profit)/len(self.transection)) * 100
        loss_per = (len(T_loss)/len(self.transection)) * 100
        ## ทำ report ผลประกอบการ ของ Model ที่ run ไป // do it

        print("===================================== report =====================================")
        print("Money : " + self.type_money + "    " + "period : " + self.period + "    " + "Bars in test : " + str(len(self.data))+ "    " +"Initial_budget : " + str(self.balance) )
        print("Gross_Porfit : "+str(round(self.profit,2))+ "    " + "Gross_Loss : "+str(round(self.loss,2))+ "    " + "Total net profit : " + str(round(self.loss + self.profit,2)) + "    " + "profit factor : " + str(round(abs(self.profit/self.loss),2)) )
        print("Total_Trade : " + str(len(self.transection)) + "    " + "Profit_trade : " + str(len(T_profit)) + "(" +str(round(profit_per,2))+ "%)"+ "    " + "Loss_trade : " + str(len(T_loss)) + "(" +str(round(loss_per,2))+ "%)" )
        print("==================================================================================")
        ## -------------------------------------- plot ------------------------------------------------------------

        # Alldata.plot(x=0,y=4,kind='line',ax=ax,label= 'data')
        # opendata_BUY.plot(x='order_open', y='open_value',style='b^',ax = ax,label= 'open_buy')
        # opendata_SELL.plot(x='order_open',y='open_value',style='rv',ax = ax,label= 'open_sell')
        # closedata_BUY.plot(x='order_close',y='close_value',style='bx',ax = ax,label= 'close_buy')
        # closedata_SELL.plot(x='order_close',y='close_value',style='rx',ax = ax,label= 'close_sell')

        # plt.show()

        fig_data = go.Figure()
        fig_data.add_trace(
            go.Candlestick(x=Alldata.iloc[:,0],
                open=Alldata.iloc[:,1],
                high=Alldata.iloc[:,2],
                low=Alldata.iloc[:,3],
                close=Alldata.iloc[:,4])
        )
        fig_data.add_trace(
            go.Scatter(
                x= opendata_SELL['order_open'],
                y= opendata_SELL['open_value'],
                mode='markers',
                name="order sell",
                marker_color='rgba(255, 0, 255, 1)'
            )
        )
        fig_data.add_trace(
            go.Scatter(
                x= closedata_SELL['order_close'],
                y= closedata_SELL['close_value'],
                mode='markers',
                name="close sell",
                marker_color='rgba(132, 0, 132, 1)'
            )
        )
        fig_data.add_trace(
            go.Scatter(
                x= opendata_BUY['order_open'],
                y= opendata_BUY['open_value'],
                mode='markers',
                name="order buy",
                marker_color='rgba(0, 255, 0, 1)' 
            )
        )
        fig_data.add_trace(
            go.Scatter(
                x= closedata_BUY['order_close'],
                y= closedata_BUY['close_value'],
                mode='markers',
                name="close buy",
                marker_color='rgba(0, 132, 0, 1)' 
            )
        )
        fig_data.update_layout(xaxis_rangeslider_visible=False)
        fig_data.show()

        # except:
            # print("somthing went wrong with ploting")
        
        



        print("=======================================================")
        print("                   end simulation                      ")
        print("=======================================================")
        


##=============================== strategy ==============================
    ## reminder ต้อง check ว่า order ที่สั่งไปจ้องไม่เกิน risk * budget และ กะได้ด้วยว่า เท่าไร
    ## reminder ต้อง check ด้วย ตัวไหนควรปิด ตัวไหนเปิดไว้
    ## ================ EA =======================

    def NOOB_method (self,data,num):
        ## ทำการดู เทรน สัก 2-3 แท่งก่อนตัดสินใจ buy-sell แล้วรอจนกว่าจะเปลี่ยน เทรน แล้วเอาออก // done 
        Trend = ""
        if num - 1 < 0:
            return
        F_data = self.data.iloc[num-1]
        S_data = self.data.iloc[num]
        #------------- check trend -----------
        if F_data[1] > S_data[1] and F_data[4] > S_data[4]:
            Trend = 'SELL'
        elif F_data[1] < S_data[1] and F_data[4] < S_data[4]:
            Trend = 'BUY'
        else : return
        allAmount = 0
        maxAmount = 0
        lam = len(self.order)
        for x in range(lam):
            x = self.order[0] ## ยังใช้ไม่ได้ในกรณี ถือไม้ทิ้งไว้ // do it later
            if x[1] == Trend : allAmount += x[2]
            if x[1] != Trend:
                Index = self.order.index(x)
                self._close_(data,Index)
            elif maxAmount < x[2] : maxAmount = x[2]
        if allAmount >= self.risk:
            return
        else:
            if len(self.order) == 0 : amt = 0.1
            else: amt = maxAmount * 2
            self._order_(data,Trend,amt)
        # if len(self.order) == 0 :
        #     if Trend == 'BUY':
        #         self._order_(data,'BUY',0.1)
        #     if Trend == "SELL" :
        #         self._order_(data,'SELL',0.1)
        # elif len(self.order) != 0 :
        #     if Trend != self.order[0][1]:
        #         self._close_(data,0)
            
## -------------------------------------------------------------------
    def first_EA(self,data,num):
        if len(self.signal) == 0 :
            print("error")
            return
        Trend = ""
        if num == 0 :
            return
        ## check signal
        Allsignal = [0] * 7
        ## check indicators
        Allsignal[0] = self.signal[0,num-1]
        Allsignal[1] = self.signal[1,num-1]

        # Allsignal = [x for x in Allsignal if x != 0]
        # if sum(Allsignal) == 0:
        #     return
        # else:
        if sum(self.active) == sum(Allsignal):
            Trend = "BUY"
        elif sum(self.active) == -(sum(Allsignal)):
            Trend = "SELL"
        else:
            Trend = "HOLD"
        allAmount = 0
        maxAmount = 0
        lam = len(self.order)
        for x in range(lam):
            x = self.order[0] ## ยังใช้ไม่ได้ในกรณี ถือไม้ทิ้งไว้ // do it later
            if Trend == "HOLD" : continue
            Index = self.order.index(x)
            # res1 = self.stop_loss(Index,data)
            # res2 = self.trailing_stop(Index,data)
            # if  res2 or res1 :
            if x[1] != Trend or self.stop_loss(Index,data)  :
            # if x[1] != Trend :
                if Trend != "HOLD" :
                    self._close_(data,Index)
                    continue
            allAmount += x[2]
            if maxAmount < x[2] : maxAmount = x[2]
        if allAmount >= self.risk:
            return
        else:
            if len(self.order) == 0 : amt = 0.1
            else: amt = maxAmount * 2
            self._order_(data,Trend,amt)
            
            
        

    def second_EA(self,data,num):
        pass


## ================ AI EA =======================
    def first_method (self,data,num,model,scaler,emcoder):
        size = 6
        if num + 1 <= size -1:
            return
        h_data = self.data.iloc[(num + 1)-size:num+1,1:5]
        h_data = scaler.transform(h_data)
        h_data = h_data.reshape(1,(h_data.shape[0]*h_data.shape[1]))
        predicted =  model.predict(h_data)
        predicted = emcoder.inverse_transform(predicted)
        predicted = predicted.reshape(len(predicted))
        #------------- check trend -----------
        # if predicted[0] == 1:
        #     Trend = 'SELL'
        # elif predicted[0] == -1:
        #     Trend = 'BUY'
        # else : return
        Trend = predicted[0]
        if Trend == 'HOLD': return
        allAmount = 0
        maxAmount = 0
        lam = len(self.order)
        for x in range(lam):
            x = self.order[0] ## ยังใช้ไม่ได้ในกรณี ถือไม้ทิ้งไว้ // do it later
            if x[1] == Trend : allAmount += x[2]
            if x[1] != Trend:
                Index = self.order.index(x)
                self._close_(data,Index)
            elif maxAmount < x[2] : maxAmount = x[2]
        if allAmount >= self.risk:
            return
        else:
            if len(self.order) == 0 : amt = 0.1
            else: amt = maxAmount * 2
            self._order_(data,Trend,amt)

    def diff_method(self,data,num,model,scaler,emcoder):
        size = 3
        size = size + 1
        
        if num   <= size - 1  :
            return
        h_data = self.data.iloc[(num + 1)-size:num+1,1:5]
        D1 = h_data.iloc[:(size-1),:].to_numpy()
        D2 = h_data.iloc[1:,:].to_numpy()
        diff_data = D1 - D2
        diff_data = pd.DataFrame(diff_data)
        h_data = scaler.transform(diff_data)
        h_data = h_data.reshape(1,(h_data.shape[0]*h_data.shape[1]))
        predicted =  model.predict(h_data)
        predicted = emcoder.inverse_transform(predicted)
        predicted = predicted.reshape(len(predicted))
        #------------- check trend -----------
        Trend = predicted[0]
        # if res == 1:
        #     Trend = 'SELL'
        # elif res == -1:
        #     Trend = 'BUY'
        # else : return

        # if len(self.order) == 0 :
        #     if res == 'BUY':
        #         self._order_(data,res,0.1)
        #     elif res == 'SELL': 
        #         self._order_(data,res,0.1)
        #     else : return
        # elif len(self.order) != 0 :
        #     if res != self.order[0][1]:
        #         self._close_(data,0)
        if Trend == 'HOLD': return
        allAmount = 0
        maxAmount = 0
        lam = len(self.order)
        for x in range(lam):
            x = self.order[0] ## ยังใช้ไม่ได้ในกรณี ถือไม้ทิ้งไว้ // do it later
            if x[1] == Trend : allAmount += x[2]
            if x[1] != Trend:
                Index = self.order.index(x)
                self._close_(data,Index)
            elif maxAmount < x[2] : maxAmount = x[2]
        if allAmount >= self.risk:
            return
        else:
            if len(self.order) == 0 : amt = 0.1
            else: amt = maxAmount * 2
            self._order_(data,Trend,amt)