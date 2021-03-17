from os import path
import gym
import pandas as pd
import tensorforce as tf 
from tensorforce import Runner , Agent
import numpy as np 
import shutil
import os
from tensorforce.environments.openai_gym import OpenAIGym
import FX_trading
import plotly.graph_objects as go

data = pd.read_excel('data/dataset_indy/XM_EURUSD-2019_H1_indy.xlsx',header=None)
data = data.iloc[:,:10]
# print(data)
up_trand = 0
down_trand = 0
order_state = False
# pre_state  = 1 if data.iloc[0,9] > 0 else -1
answers = []
for x in range(0,len(data)):
    res_data = data.iloc[x,:]
    init_state = 1 if data.iloc[x,9] > 0 else -1
    if init_state == 1 and not(order_state):
        if res_data[8] > res_data[9] :
            answers.append(2)
            order_state = True
        else : answers.append(0)
    elif init_state == -1 and not(order_state):
        if res_data[8] < res_data[9] :
            answers.append(1)
            order_state = True
        else : answers.append(0)
    elif init_state == 1 and order_state :
        if res_data[8] < res_data[9] :
            answers.append(3)
            order_state = False
        else : answers.append(0)
    elif init_state == -1 and order_state :
        if res_data[8] > res_data[9] :
            answers.append(4)
            order_state = False
        else : answers.append(0)
    else : answers.append(0)



env = gym.make('FXTrading-v2')
# filepath = 'testtest/testmodel_saver_test_1'
# print(filepath)
# agent = Agent.load(directory=("test/test3/save_model_all"), format='checkpoint')
record = []
for i in range(1):
    observation = env.reset()
    for t in range(6210):
        # env.render()
        # print(observation)
        action =  answers[t] #agent.act(states=  observation)
        observation, reward, done, infos = env.step(action)
        # agent.observe(reward=reward,terminal=done)
        print("+++++++++++++++++++++++++")
        # print("reward : {0}, ALL_reward : {1} ").format(infos['reward'],infos['all_reward'])
        print("profit order : " + str(infos['pro_order']))
        print("loss order : " + str(infos['loss_order']))
        print("budget : " + str(infos['budget']))
        print("profit : " + str(infos['budget'] - 200))
        print("reward : " + str(infos['reward']))
        print("All_reward : " + str(infos['all_reward']))
        print("+++++++++++++++++++++++++")
        # data = [i,action,infos['reward'],infos['all_reward'],infos['budget'],infos['pro_order'],infos['loss_order']]
        # record.append(data)
        if done:
            data = [i,action,infos['reward'],infos['all_reward'],infos['budget'],infos['pro_order'],infos['loss_order']]
            record.append(data)
            print("Episode finished after {} timesteps".format(t+1))
            break
    # env.plot_data()
env.close()
#================== export data =====================
record = pd.DataFrame(record)
record.columns = ["num_record","action","reward","all_reward","budget","profit_order","loss_order"]
record.to_csv('test/record_test_2019_test_MACD.csv',index=False)