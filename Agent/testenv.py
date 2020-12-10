import gym
import FX_trading
import pandas as pd 
import  numpy as np 

data = pd.read_excel('data/Test_data/sin_dataset.xlsx', header=None)
data1 = data.iloc[:len(data)-1,4]
data2 = data.iloc[1:,4]
data1 = np.array(data1)
data2 = np.array(data2)
answer = data1 - data2
# print(data1)
# print(data2)
Answer = []
for x in answer :
    if x > 0:
        Answer.append(0)
    else:
        Answer.append(1)
print(len(Answer))
answer = [1]
# answer.extend(Answer)
Answer.extend(answer)
print(len(Answer))

env = gym.make('FXTrading-v1')
# env.reset()
for index in range(1000):
    env.render()
    env.step(Answer[index]) 
env.plot_data()
env.close()

