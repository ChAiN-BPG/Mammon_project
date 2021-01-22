import gym
import tensorforce as tf 
from tensorforce import Runner , Agent
import numpy as np 
import os
from tensorforce.environments.openai_gym import OpenAIGym
import FX_trading

def finished_ep(r,_):
    # print("==================================================")
    # print("Finished episode {ep} after {ts} timesteps".format(ep=r.episodes + 1, ts=r.timesteps + 1))
    # print("Episode reward: {}".format(r.episode_rewards[-1]))
    # print("Max Episode reward: {}".format(max(r.episode_rewards[:])))
    # # print("profit: {}".format(r.))
    # print(r.environments[0].render())
    # if r.episodes % 10 == 0:
    #     print("Average of last 10 rewards: {}".format(np.mean(r.episode_rewards[-10:])))
    # print("==================================================")
    pathfile = 'test/saved'
    if r.episode_rewards[-1] >= np.max(r.episode_rewards[:]) :
        if os.path.exists(pathfile):
            os.remove(pathfile)
        r.agent.save(directory=pathfile, format='checkpoint',append=None)
        print("#### save best model suceeded at reward : {} ####".format(r.episode_rewards[-1]))
        pass
    return True

environment = OpenAIGym(level='FXTrading-v2011',visualize=False)
# # agent = Agent.load(directory='test/testmodel_saver', format='checkpoint')
agent = dict(
        
        agent='ppo',
        # Automatically configured network
        network=[
        # dict(type='gru', size=20,horizon = 1)
        # dict(type='dense', size=20, activation='tanh')
        dict(type='dense',size=25, activation='relu'),
        dict(type='dense',size=50, activation='relu'),
        # dict(type='dense',size=50, activation='tanh'),
        # dict(type='dense',size=50, activation='tanh'),
        dict(type='dense',size=25, activation='relu')
        # dict(type='dense',size=10, activation='sigmoid')
        # dict(type='lstm', size=10,horizon = 1)
    ],
        batch_size=5, learning_rate=3e-4,max_episode_timesteps = 7000,
        # Save agent every 10 updates and keep the 5 most recent checkpoints
        summarizer = dict(directory= 'test/summaries_test'),
        saver=dict(directory='test/testmodel_saver_test', frequency=10, max_checkpoints=1000),
        memory = 60000
    )
runner = Runner(agent=agent, environment=environment)

# Train for 200 episodes
runner.run(num_episodes=1200,callback=finished_ep)
runner.close()


# agent = Agent.load(directory='test11/testmodel_saver_dqn1', format='checkpoint')

# env = gym.make('FXTrading-v0')
# observation = env.reset()
# for t in range(1000):
#     env.render()
#     print(observation)
#     action = agent.act(states=  observation)
#     observation, reward, done, _ = env.step(action)
#     agent.observe(reward=reward,terminal=done)
#     if done:
#         print("Episode finished after {} timesteps".format(t+1))
#         break
# env.plot_data()
# env.close()