# import gym

# from stable_baselines.common.policies import MlpPolicy
# from stable_baselines.common.vec_env import DummyVecEnv
# from stable_baselines import PPO2

# env = gym.make('CartPole-v1')
# # Optional: PPO2 requires a vectorized environment to run
# # the env is now wrapped automatically when passing it to the constructor
# # env = DummyVecEnv([lambda: env])

# model = PPO2(MlpPolicy, env, verbose=1)
# model.learn(total_timesteps=10000)

# obs = env.reset()
# for i in range(1000):
#     action, _states = model.predict(obs)
#     obs, rewards, dones, info = env.step(action)
#     env.render()
# from mpi4py import MPI
# comm = MPI.COMM_WORLD
# rank = comm.Get_rank()
# print ("hello world from process ", rank)

import numpy as np
from numpy.core.fromnumeric import mean
res1 = np.random.randint(1,25,[10])
res2 = np.random.randint(4,15,[10])
Mres1 = mean(res1)
Mres2 = mean(res2)
Ans1 = Mres1 + Mres2
Sres = res1 + res2
Ans2 = mean(Sres)
print(Ans1)
print(Ans2)