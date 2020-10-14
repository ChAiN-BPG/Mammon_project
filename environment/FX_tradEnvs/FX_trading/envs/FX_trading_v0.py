import gym
from numpy import genfromtxt
from gym import utils
from gym import spaces
import numpy as np
import talib as ta 
import pandas as pd 
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler, LabelEncoder, OneHotEncoder

class ForexEnv_test(gym.Env):
    """
    this is environment for reinforcement learning. This environment is about that simulation for forex trading which can trade only 1 per any time.

    init data for gym : 
        action space : 
            BUY(0) : order buy 
            SELL(1) : order sell 
            
            
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
        self.action_space = spaces.Discrete(2) 
        self.observation_space = spaces.Box(low=float(-1.0), high=float(1.0), shape=(13,), dtype=np.float32)
        # init dataset 
        df_data = pd.read_excel(dataset,header=None)
        df_data = df_data.iloc[:,0:5]
        df_data.columns = ['time','open','high','low','close']
        self.my_data = df_data.to_numpy()
        self.data_AllTick = len(self.my_data)
        self.data_column = len(self.my_data[0])
        self.count_tick = 0
        # init base for trading
        self.balance = 200
        self.budget = self.balance
        self.amount = 0.05
        self.lot = 100000 # 100000 is standard lot , 10000 is mini lot , 1000 is nicro lot , 100 is nano lot
        self.leverage = 100 
        self.sperad = 0.00022
        # the order details
        self.order_state = None #  1 = buy order , 0 = sell order
        self.order_time = 0
        self.order_price = 0
        self.count_ordered = 0
        # currancy data
        self.tick_data = 0
        self.time_data = 0
        self.open_data = 0
        self.close_data = 0
        self.high_data = 0
        self.low_data = 0
        self.wrong_move = False
        # normalize data
        scaler = MinMaxScaler(feature_range=(-1,1))
        scaler.fit(self.my_data[:,1:15])
        self.encoder = scaler
        # render data
        self.profit_order = 0
        self.loss_order = 0 
        # data collector
        self.all_order = []
        




        
    def _calculate_(self,action):
        profit = 0
        if self.order_state == None : return profit
        if self.order_state == 1 :
            profit = ((self.close_data - (self.sperad/2)) * self.lot * self.amount) - self.order_price
        elif self.order_state == -1 :
            profit = self.order_price - ((self.close_data + (self.sperad/2)) * self.lot * self.amount) 
        return profit







    def _order_(self,action):
        if self.order_state != None : 
            # self.wrong_move = True
            return
        start_cur = self.close_data + (self.sperad/2) if action == 1 else self.close_data - (self.sperad/2)
        current_price = start_cur * self.lot * self.amount
        self.order_price = current_price
        self.order_state = 1 if action == 1 else -1
        self.order_time = self.time_data
        ## collect data // สามารถใส่ info เพื่อออก ไปทำอย่างอื่นได้
        data_time = self.order_time
        data_type = "BUY" if action == 1 else "SELL"
        data_tick = self.close_data
        data_price = current_price
        data_status = "order"
        self.all_order.append([data_time,data_status,data_type,data_tick,data_price])


    def _close_(self,value):
        if self.order_state == None :
            # self.wrong_move = True
            return
        ## collect data
        data_type  = "BUY" if self.order_state == 1 else "SELL"
        end_cur = self.close_data - (self.sperad/2) if self.order_state == 1 else self.close_data + (self.sperad/2)
        data_price = end_cur * self.lot * self.amount
        data_status = "close"
        data_tick = self.close_data
        data_time = self.time_data
        self.all_order.append([data_time,data_status,data_type,data_tick,data_price])
        ## reset 
        self.order_state = None
        self.order_time = 0
        self.order_price = 0
        self.count_ordered += 1
        if value < 0 :
            self.loss_order += 1
        else :
            self.profit_order += 1
        self.budget += value
        


    def _next_observation (self):
        """
        all value should be [(-1) - 1] 

        observation = [data(t),order_state,order_price]
        """
        if self.tick_data < 2 :
            data = self.my_data[self.tick_data,1:]
            data = np.array([data,data,data])
        else :
            data = self.my_data[self.tick_data - 2 :self.tick_data + 1,1:15]
        obs_data = self.encoder.transform(data) 
        obs_data = obs_data.flatten()
        out = 0
        if self.order_state == 2: out = -1
        elif self.order_state == 1 : out = 1
        obs = np.append(obs_data,out) ## ใส่ indicator ด้วยยยยย // done
        self.tick_data += 1
        return obs
        




    def _reward_(self,action,value):
        reward = 0
    
        ## กรณี เล่นผิด
        # if self.wrong_move :
        #     return (-10000)

        ## กรณี ยังไม่order
        Longterm = 0
        Longterm += -(self.count_tick/self.data_AllTick)  ##  ไม่ยอมเปิด order 
        Longterm += (self.budget - self.balance)##  balance ที่เพิ่มขึ้น-ลดลงมีผล
        
        ## กรณี order แล้ว
        Shortterm = 0 
        if self.order_state != None :
            Shortterm +=  (value + 1) * 10 ##  เปิด order 
        reward = Longterm + Shortterm

        ## กรณีที่ปิดถูก
        
        return reward
    




    def step(self,action):
        """
        step - get data form dataset using count_tick to catch up step
                - check profit 
                - check action : 0 = do not thing , 1 = buy order , 2 = sell order , 3 = close
                - create observation that include state and reward
        """
        episode_over = bool(0)
        # self.wrong_move = False
        ## check can afford order
        if ((self.budget * self.leverage) < (self.lot * self.amount)):
            episode_over = bool(1)
        if self.tick_data >= self.data_AllTick :
            episode_over = bool(1)
        obs = 0
        reward = 0 
        if episode_over == False :
            ## get currancy data each time
            self.time_data = self.my_data[self.tick_data,0]
            self.open_data = self.my_data[self.tick_data,1]
            self.high_data = self.my_data[self.tick_data,2]
            self.low_data = self.my_data[self.tick_data,3]
            self.close_data = self.my_data[self.tick_data,4]
            outcome = self._calculate_(action)
              
            if action != self.order_state :
                self._close_(outcome)
                self._order_(action)
            obs = self._next_observation()
            reward = self._reward_(action,outcome)
            self.count_tick += 1
            
        return obs , reward , episode_over, {}
        




    def reset(self):
        self.count_tick = 0
        self.balance = 200
        self.budget = self.balance
        self.order_state = None # 0 = nop , 1 = buy order , 2 = sell order
        self.order_time = 0
        self.order_price = 0
        self.profit_order = 0
        self.loss_order = 0 
        self.count_ordered = 0
        self.tick_data = 0 ##np.random.random_integers(self.data_AllTick - 1500)
        self.time_data = 0
        self.open_data = 0
        self.close_data = 0
        self.high_data = 0
        self.low_data = 0
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
        try:
            df_order = pd.DataFrame(data= self.all_order)
            df_order.columns = ['data_time','data_status','data_type','data_tick','data_price']
            sell_order = df_order.groupby('data_type').get_group('SELL')
            buy_order = df_order.groupby('data_type').get_group('BUY')
            sell_ordered = sell_order.groupby('data_status').get_group("order")
            sell_closed = sell_order.groupby('data_status').get_group("close")
            buy_ordered = buy_order.groupby('data_status').get_group("order")
            buy_closed = buy_order.groupby('data_status').get_group("close")
        except: print("An exception occurred")
        fig_data = go.Figure()
        fig_data.add_trace(
            go.Candlestick(x=self.my_data[:,0],
                open=self.my_data[:,1],
                high=self.my_data[:,2],
                low=self.my_data[:,3],
                close=self.my_data[:,4])
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
