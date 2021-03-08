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
import random

class ForexEnv_test2(gym.Env):
    """
    this is environment for reinforcement learning. This environment is about that simulation for forex trading which can trade only 1 per any time.

    init data for gym : 
        action space : 
            HOLD(0) : Hold order
            BUY(1) : Buy order 
            SELL(2) : Sell order 
            
            
        observation space : 
    init data for trading :
        balance  : 200
        lot      : 0.05
        lot type : 100000
        leverage : (1 : 100)
        sperad   : 0.00022
    """
    def __init__(self,dataset,model):
        self.skip_time = True
        self.length_skip = 12
        self.unit_timestep = 3
        if self.skip_time :
            unit = 15 * self.unit_timestep + 1
            self.window_slide = self.length_skip * (self.unit_timestep - 1 )
        else :
            self.window_slide = 1
            unit = 15 * self.window_slide + 1
        self.action_space = spaces.Discrete(3) 
        self.observation_space = spaces.Box(low=-1, high=1, shape=(unit,), dtype=np.float32) ## แก้ observation with no preprocess 
        # init dataset 
        self.data_yearly = []
        self.num_data = dataset
        for x in range(dataset):
            df_data = pd.read_excel('data/dataset_indy/XM_EURUSD-'+str(2011 + x)+'_H1_indy.xlsx',header=None)
            df_data.columns = ['date','time','open','high','low','close','volume','macd','macdsignal','macdhist','ATR' , 'slowk' , 'slowd', 'WILL','SAR','aroondown','aroonup']
            df_data = df_data.to_numpy()
            self.data_yearly.append(df_data)
        ##  ================ add indicator ==================== 
        # macd, macdsignal, macdhist = ta.MACD(df_data['close'], fastperiod=12, slowperiod=26, signalperiod=9)
        # ATR = ta.ATR(df_data['high'], df_data['low'], df_data['close'], timeperiod=14)
        # slowk, slowd = ta.STOCH(df_data['high'], df_data['low'], df_data['close'], fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
        # WILL = ta.WILLR(df_data['high'], df_data['low'], df_data['close'], timeperiod=14)
        # SAR = ta.SAR(df_data['high'], df_data['low'], acceleration=0, maximum=0)
        # aroondown, aroonup = ta.AROON(df_data['high'], df_data['low'], timeperiod=14)
        ## ====================================================
        # data = {
        #     'date' : df_data['date'],
        #     'time' : df_data['time'],
        #     'open' : df_data['open'],
        #     'high' : df_data['high'],
        #     'low'  : df_data['low'],
        #     'close' : df_data['close'],
        #     'volume' : df_data['volume'],
        #     'macd' : macd,
        #     'macdsignal':macdsignal,
        #     'macdhist':  macdhist, 
        #     'ATR' : ATR , 
        #     'slowk' : slowk, 
        #     'slowd' : slowd, 
        #     'WILL' : WILL,
        #     'SAR' : SAR,
        #     'aroondown' : aroondown,
        #     'aroonup' : aroonup
        #     }
        # all_data = pd.DataFrame(data= data)
        # all_data = df_data
        # all_data =  all_data.dropna()
        # self.all_data = all_data.to_numpy()
        # self.data_AllTick = len(self.all_data)
        # self.data_column = len(self.all_data[0])
        # self.count_tick = 0
        # ## set datetime 
        # for x in range(self.data_AllTick):
        #     date = self.all_data[x,0].split('.')
        #     time = self.all_data[x,1].split(':')
        #     self.all_data[x,0] = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),int(time[0]),int(time[1]))
            # self.date_data = datetime.datetime(int(date.year),int(date.years),int(date.day),int(time[0]),int(time[1]))
        # init base for trading
        self.count_tick = 0
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
        self.swap_long = -5
        self.swap_short = -5
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
        self.count_yearly = [x for x in range (dataset)]
        random.shuffle(self.count_yearly)
        # =========== normalize data ============
        # scaler = MinMaxScaler(feature_range=(-1,1))
        # scaler.fit(self.all_data[:,1:15])
        self.encoder = pickle.load(open(model, 'rb'))
        # =========== render data ===============
        self.profit_order = 0
        self.loss_order = 0 
        # ========== data collector =============
        self.all_order = []
        # ========== debuff data ================
        self.all_reward =  0




        
    def _calculate_(self):
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
        _ = self._calculate_()


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
        #     data = self.all_data[self.tick_data,2:]
        #     data = np.array([data,data,data])
        # else :
        #     data = self.all_data[self.tick_data - 2 :self.tick_data + 1,2:]
        if self.skip_time :
            res_set = []
            res_set.append(self.dataset[self.tick_data,2:])
            for x in range(1,self.unit_timestep):
                rr = self.tick_data - (self.length_skip * x -1)
                res = self.dataset[rr,2:]
                res_set.append(res)
            data = res_set
        #     # data = self.all_data[self.tick_data - (self.window_slide - 1) : self.tick_data + 1,2:]
        else :
            data = self.dataset[self.tick_data - (self.window_slide - 1) : self.tick_data + 1,2:]

        ## ========= set one candle ===============
        # data = self.all_data[self.tick_data,2:]
        data = np.array(data)
        # obs_data = data
        obs_data = []
        for i in range (len(data)):
            res = data[i,:]
            res = self.encoder.transform([res]) 
            obs_data.append(res[0])

        # obs_data = self.encoder.transform(data) 
        obs_data = np.array(obs_data)
        obs_data = obs_data.flatten()
        obs_data = np.append(obs_data,self.order_state)
        obs_data = obs_data.astype('float32')
        # out = 0
        # if self.order_state == 2: out = -1
        # elif self.order_state == 1 : out = 1
        # obs = np.append(obs_data,out) ## ใส่ indicator ด้วยยยยย // done
        self.tick_data += 1
        return obs_data
        




    def _reward_(self): ## เกก้ reward 
        reward = 0
    
        ## กรณี เล่นผิด
        # if self.wrong_move :
        #     return (-10000)

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
        if self.tick_data >= self.yearsTick :
            episode_over = bool(1)
        if self.equity <= -(self.budget) :
            episode_over = bool(1)
            self.budget = 0
        obs = 0
        reward = 0 
        if episode_over == False :
            ## get currancy data each time
            # Date = date.iloc[0].split('.')
# time = date.iloc[1].split(':')
# asss = datetime.datetime(int(Date[0]),int(Date[1]),int(Date[2]),int(time[0]),int(time[1]))
            # date = self.all_data[self.tick_data,0].split('.')
            # date = self.all_data[self.tick_data,0]
            # date = date.split('.')
            # time = self.all_data[self.tick_data,1].split(':')
            # self.date_data = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),int(time[0]),int(time[1]))
            # self.date_data = datetime.datetime(int(date.year),int(date.years),int(date.day),int(time[0]),int(time[1]))
            # self.all_data[self.tick_data,0] = self.date_data
            self.date_data = self.dataset[self.tick_data,0]
            self.open_data = self.dataset[self.tick_data,2]
            self.high_data = self.dataset[self.tick_data,3]
            self.low_data = self.dataset[self.tick_data,4]
            self.close_data = self.dataset[self.tick_data,5]
            outcome = self._calculate_()
            if self.tick_data == self.yearsTick -2 :
                self._close_(outcome,self.order_state)
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
            reward = self._reward_()
            self.count_tick += 1
            if self.date_data.hour == 4 and self.order_state != 0:
                self.night += 1
            self.all_reward += reward
            self.pre_equity = self.equity
        return obs , reward , episode_over, {'reward' : reward, 'all_reward' : self.all_reward, 'pro_order' : self.profit_order, 'loss_order' : self.loss_order, 'budget' : self.budget}
        




    def reset(self):
        #### out ####
        self.render()
        if len(self.count_yearly) == 0 :
            self.count_yearly = [x for x in range (self.num_data)]
            random.shuffle(self.count_yearly)
        years = self.count_yearly.pop()
        self.dataset = self.data_yearly[years]
        # res_data = pd.DataFrame(self.all_data)
        # res_years = []
        # for x in range(self.data_AllTick):
        #     res_years.append(res_data.iloc[x,0].years)
        # res_data['years'] = res_years
        # res_data = res_data.groupby('years').get_group(years)
        # res_data = res_data.iloc[:,:-1]
        # self.dataset = res_data.to_numpy()
        self.yearsTick = len(self.dataset)
        #####
        self.count_tick = 0
        self.balance = 200
        self.budget = self.balance
        self.order_state = 0 # 0 = nop , 1 = buy order , -1 = sell order
        self.order_price = 0
        self.profit_order = 0
        self.loss_order = 0 
        self.count_ordered = 0
        # self.tick_data =  self.window_slide - 1 ##np.random.random_integers(self.data_AllTick - 1500)
        # if self.skip_time :
        #     self.window_slide = self.length_skip * (self.unit_timestep - 1)
        # else:
        #     se
        self.tick_data =  self.window_slide - 1 
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
        self.pre_equity = self.balance
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
            go.Candlestick(x=self.all_data[:,0],
                open=self.all_data[:,2],
                high=self.all_data[:,3],
                low=self.all_data[:,4],
                close=self.all_data[:,5])
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
