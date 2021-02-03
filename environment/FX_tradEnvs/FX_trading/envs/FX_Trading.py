import gym
from numpy import genfromtxt
from gym import utils
from gym import spaces
import pickle
import numpy as np
import talib as ta 
import pandas as pd 
import datetime
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler, LabelEncoder, OneHotEncoder

class ForexEnv(gym.Env):
    """
    this is environment for reinforcement learning. This environment is about that simulation for forex trading which can trade only 1 per any time.

    init data for gym : 
        action space : 
            Hold(0) : do nothing 
            BUY(1) : order buy 
            SELL(2) : order sell 
            CLOSE(3): close all of order 
            
        observation space : 
    init data for trading :
        balance  : 200
        lot      : 0.05
        lot type : 100000
        leverage : (1 : 100)
        sperad   : 0.00022
    """
    ## this emvirpnment has no spread and magin calculate // todo
    def __init__(self,dataset):
        self.window_slide = 1
        unit = 15 * self.window_slide + 1
        self.action_space = spaces.Discrete(3) 
        self.observation_space = spaces.Box(low=-1, high=1, shape=(unit,), dtype=np.float32) ## แก้ observation with no preprocess 
        # init dataset 
        df_data = pd.read_excel(dataset,header=None)
        # df_data = df_data.iloc[:,0:6]
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
        self.my_data = all_data.to_numpy()
        self.data_AllTick = len(self.my_data)
        self.data_column = len(self.my_data[0])
        self.count_tick = 0
        ## set datetime 
        for x in range(self.data_AllTick):
            date = self.my_data[x,0].split('.')
            time = self.my_data[x,1].split(':')
            self.my_data[x,0] = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),int(time[0]),int(time[1]))
            # self.date_data = datetime.datetime(int(date.year),int(date.month),int(date.day),int(time[0]),int(time[1]))
        # init base for trading
        self.balance = 200
        self.budget = self.balance
        self.amount = 0.05
        self.lot = 100000 # 100000 is standard lot , 10000 is mini lot , 1000 is nicro lot , 100 is nano lot
        self.leverage = 100 
        self.sperad = 0.00022
        ## add margin profit and equity 
        # self.profit = 0 # if total(unclose_order) < 0 :  
        self.equity = self.balance # self.balance + sum(unclose_order) 
        self.margin = 0 # Margin = ราคาในขณะที่เปิด x amount x self.lot / Leverage
        self.margin_free = self.balance # self.balance - self.margin
        self.pre_equity = self.balance
        self.swap_long = 0 ##-0.2
        self.swap_short = 0  ##-2.2
        # the order details
        self.order_state = 0 # 0 = nop , 1 = buy order , 2 = sell order
        self.order_price = 0
        self.count_ordered = 0
        # currancy data
        self.night = 0
        self.tick_data = self.window_slide - 1
        self.date_data = 0
        self.open_data = 0
        self.close_data = 0
        self.high_data = 0
        self.low_data = 0
        self.wrong_move = False
        # =========== normalize data ============
        # scaler = MinMaxScaler(feature_range=(-1,1))
        # scaler.fit(self.my_data[:,1:15])
        self.encoder = pickle.load(open('model/scaler.pickle', 'rb'))
        # =========== render data ===============
        self.profit_order = 0
        self.loss_order = 0 
        # ========== data collector =============
        self.all_order = []
        # ========== debuff data ================
        self.all_reward =  0




        
    def _calculate_(self,action):
        outcome = 0
        if self.order_state == 0 : return outcome
        if self.order_state == 1 :
            outcome = ((self.close_data - (self.sperad/2)) * self.lot * self.amount) - self.order_price
        elif self.order_state == -1 :
            outcome = self.order_price - ((self.close_data + (self.sperad/2)) * self.lot * self.amount) 
        if self.date_data.hour == 4 :
            self.night += 1
        self.equity = outcome + self.budget
        return outcome







    def _order_(self,action):
        if self.order_state != 0 : 
            self.wrong_move = True
            return
        start_cur = self.close_data + (self.sperad/2) if action == 1 else self.close_data - (self.sperad/2)
        current_price = start_cur * self.lot * self.amount
        self.order_price = current_price
        self.order_state = 1 if action ==1 else -1
        ## collect data // สามารถใส่ info เพื่อออก ไปทำอย่างอื่นได้
        data_date = self.date_data
        data_type = "BUY" if action == 1 else "SELL"
        data_tick = start_cur
        data_price = current_price
        data_status = "order"
        self.all_order.append([data_date,data_status,data_type,data_tick,data_price])
        ## add margin  
        self.margin = self.order_price/ self.leverage
        self.margin_free = self.budget - self.margin



    def _close_(self,value,action):
        action = 1 if action ==1 else -1
        if self.order_state == 0 :
            self.wrong_move = True
            return
        if action == self.order_state :
            self.wrong_move = True
        ## collect data
        data_type  = "BUY" if self.order_state == 1 else "SELL"
        end_cur = self.close_data - (self.sperad/2) if self.order_state == 1 else self.close_data + (self.sperad/2)
        data_price = end_cur * self.lot * self.amount
        data_price = data_price + (self.night * self.swap_long) if self.order_state == 1 else data_price + (self.night * self.swap_short)
        data_status = "close"
        data_tick = self.close_data
        data_date = self.date_data
        self.all_order.append([data_date,data_status,data_type,data_tick,data_price])
        ## reset 
        self.order_state = 0 
        self.order_price = 0
        self.count_ordered += 1
        if value < 0 :
            self.loss_order += 1
        else :
            self.profit_order += 1
        self.budget += value
        self.margin_free = self.budget
        self.equity = self.budget
        self.margin = 0
        self.night = 0
        


    def _next_observation (self): ## แก้ยาวๆๆ
        """
        all value should be [(-1) - 1] 

        observation = [data(t),order_state,order_price]
        """
        # if self.tick_data < 2 :
        #     data = self.my_data[self.tick_data,2:]
        #     data = np.array([data,data,data])
        # else :
        #     data = self.my_data[self.tick_data - 2 :self.tick_data + 1,2:]
        data = self.my_data[self.tick_data - (self.window_slide - 1) : self.tick_data + 1,2:]

        ## ========= set one candle ===============
        # data = self.my_data[self.tick_data,2:]
        data = np.array(data)
        # obs_data = data
        obs_data = self.encoder.transform(data) 

        obs_data = obs_data.flatten()
        obs_data = np.append(obs_data,self.order_state)
        obs_data = obs_data.astype('float32')
        # out = 0
        # if self.order_state == 2: out = -1
        # elif self.order_state == 1 : out = 1
        # obs = np.append(obs_data,out) ## ใส่ indicator ด้วยยยยย // done
        self.tick_data += 1
        return obs_data
        




    def _reward_(self,action,value): ## เกก้ reward 
        reward = 0
    
        ## กรณี เล่นผิด
        if self.wrong_move :
            return (-10000)

        ## กรณี ยังไม่order
        Longterm = 0
        # Longterm += -(self.count_tick/self.data_AllTick)  ##  ไม่ยอมเปิด order 
        # Longterm += (self.budget - self.balance)##  balance ที่เพิ่มขึ้น-ลดลงมีผล
        # Longterm = self.pre_equity - self.equity
        Longterm = self.equity - self.pre_equity
        ## กรณี order แล้ว
        Shortterm = 0 
        # if self.order_state > 0 :
        #     Shortterm +=  (value + 1) * 100 ##  เปิด order 
        reward = Longterm + Shortterm
        return reward
    




    def step(self,action):
        """
        step - get data form dataset using count_tick to catch up step
                - check profit 
                - check action : 0 = do not thing , 1 = buy order , 2 = sell order , 3 = close
                - create observation that include state and reward
        """
        episode_over = bool(0)
        self.wrong_move = bool(0)
        ## check can afford order
        if ((self.budget * self.leverage) < (self.lot * self.amount)):
            episode_over = bool(1)
        if self.tick_data >= self.data_AllTick :
            episode_over = bool(1)
        obs = 0
        reward = 0 
        if episode_over == False :
            ## get currancy data each time
            # Date = date.iloc[0].split('.')
# time = date.iloc[1].split(':')
# asss = datetime.datetime(int(Date[0]),int(Date[1]),int(Date[2]),int(time[0]),int(time[1]))
            # date = self.my_data[self.tick_data,0].split('.')
            # date = self.my_data[self.tick_data,0]
            # date = date.split('.')
            # time = self.my_data[self.tick_data,1].split(':')
            # self.date_data = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),int(time[0]),int(time[1]))
            # self.date_data = datetime.datetime(int(date.year),int(date.month),int(date.day),int(time[0]),int(time[1]))
            # self.my_data[self.tick_data,0] = self.date_data
            self.date_data = self.my_data[self.tick_data,0]
            self.open_data = self.my_data[self.tick_data,2]
            self.high_data = self.my_data[self.tick_data,3]
            self.low_data = self.my_data[self.tick_data,4]
            self.close_data = self.my_data[self.tick_data,5]
            outcome = self._calculate_(action)
            if action == 0:
                pass
            # elif action == 3 :
            #     self._close_(outcome)
            elif self.order_state != 0 : 
                self._close_(outcome,action)
                self._order_(action)
            else:
                self._order_(action)
            obs = self._next_observation()
            reward = self._reward_(action,outcome)
            self.count_tick += 1
            self.all_reward += reward
        return obs , reward , episode_over, {'reward' : reward, 'all_reward' : self.all_reward, 'pro_order' : self.profit_order, 'loss_order' : self.loss_order, 'budget' : self.budget}
        




    def reset(self):
        #### out ####
        self.render()
        #####
        self.count_tick = 0
        self.balance = 200
        self.budget = self.balance
        self.order_state = 0 # 0 = nop , 1 = buy order , -1 = sell order
        self.order_price = 0
        self.profit_order = 0
        self.loss_order = 0 
        self.count_ordered = 0
        self.tick_data =  self.window_slide - 1 ##np.random.random_integers(self.data_AllTick - 1500)
        self.date_data = 0
        self.open_data = 0
        self.close_data = 0
        self.high_data = 0
        self.low_data = 0
        ## add reset margin profit and equity
        self.margin = 0
        self.margin_free = self.balance
        self.profit = 0
        self.equity = self.balance
        # ========== debuff data ================
        self.all_reward =  0
        return self._next_observation()





    def render(self, mode='human'):
        # Render the environment to the screen
        profit = self.budget - self.balance 
        if self.count_ordered != 0 :
            profit_percentage = round((self.profit_order/self.count_ordered) * 100 , 2)
            loss_percentage = round((self.loss_order/self.count_ordered) * 100 , 2)
        else : 
            profit_percentage = 0
            loss_percentage = 0
        print("===============================================================================================")
        print(f'Step : {self.count_tick}')
        print(f'budget : {self.budget}')
        print(
            f'Total tick : {self.count_tick} (Total ordered : {self.count_ordered})')
        print(
            f'Profit order : {self.profit_order} ({profit_percentage}%)')
        print(
            f'loss order : {self.loss_order} ({loss_percentage}%)')
        print(f'Profit: {profit}')
        print("===============================================================================================")





    def plot_data(self,):
        df_order = pd.DataFrame(data= self.all_order)
        df_order.columns = ['data_time','data_status','data_type','data_tick','data_price']
        try:
            sell_order = df_order.groupby('data_type').get_group('SELL')
        except:
            sell_order = []
        try:
            buy_order = df_order.groupby('data_type').get_group('BUY')
        except:
            buy_order = []
        try:
            sell_ordered = sell_order.groupby('data_status').get_group("order")
            sell_closed = sell_order.groupby('data_status').get_group("close")
        except:
            sell_closed = []
            sell_ordered = []
        try:
            buy_ordered = buy_order.groupby('data_status').get_group("order")
            buy_closed = buy_order.groupby('data_status').get_group("close")
        except:
            buy_closed = []
            buy_ordered = []
        fig_data = go.Figure()
        fig_data.add_trace(
            go.Candlestick(x=self.my_data[:,0],
                open=self.my_data[:,2],
                high=self.my_data[:,3],
                low=self.my_data[:,4],
                close=self.my_data[:,5])
        )
        fig_data.add_trace(
            go.Scatter(
                x= sell_ordered['data_time'],
                y= sell_ordered['data_tick'],
                mode='markers',
                name="order sell",
                marker_color='rgba(255, 0, 255, 1)'
            )
        )
        fig_data.add_trace(
            go.Scatter(
                x= sell_closed['data_time'],
                y= sell_closed['data_tick'],
                mode='markers',
                name="close sell",
                marker_color='rgba(132, 0, 132, 1)'
            )
        )
        fig_data.add_trace(
            go.Scatter(
                x= buy_ordered['data_time'],
                y= buy_ordered['data_tick'],
                mode='markers',
                name="order buy",
                marker_color='rgba(0, 255, 0, 1)' 
            )
        )
        fig_data.add_trace(
            go.Scatter(
                x= buy_closed['data_time'],
                y= buy_closed['data_tick'],
                mode='markers',
                name="close buy",
                marker_color='rgba(0, 132, 0, 1)' 
            )
        )
        fig_data.update_layout(xaxis_rangeslider_visible=False)
        fig_data.show()

### ======================== test ==========================================
# data = pd.read_excel('data/dataset/XM_EURUSD-2020_H1.xlsx',header=None)
# print(data)

# fig = go.Figure()
# fig.add_trace(
#         go.Candlestick(x=[x for x in range(len(data))],
#             open=data.iloc[:,2],
#             high=data.iloc[:,3],
#             low=data.iloc[:,4],
#             close=data.iloc[:,5])
#     )
# fig.update_layout(xaxis_rangeslider_visible=False)
# fig.show()