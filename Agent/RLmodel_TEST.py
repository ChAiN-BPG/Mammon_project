import gym
import tensorforce as tf 
from tensorforce import Runner , Agent
from tensorforce.environments.openai_gym import OpenAIGym
import FX_trading


environment = OpenAIGym(level='FXTrading-v0',visualize=False)
# agent = Agent.load(directory='test/testmodel_saver', format='checkpoint')
agent = dict(
        
        agent='dqn',
        # Automatically configured network
        network=[
        # dict(type='gru', size=20,horizon = 1)
        # dict(type='lstm', size=20, activation='tanh')
        # dict(type='dense',size=25, activation='tanh'),
        # dict(type='dense',size=50, activation='tanh'),
        # dict(type='dense',size=50, activation='tanh'),
        # dict(type='dense',size=50, activation='tanh'),
        # dict(type='dense',size=25, activation='tanh')
        # dict(type='dense',size=10, activation='sigmoid')
        dict(type='lstm', size=10,horizon = 1)
    ],
        batch_size=5, learning_rate=3e-4,max_episode_timesteps = 1000,
        # Save agent every 10 updates and keep the 5 most recent checkpoints
        summarizer = dict(directory= 'test/summaries_dqn1'),
        saver=dict(directory='test/testmodel_saver_dqn1', frequency=10, max_checkpoints=1000),
        memory = 60000
    )
runner = Runner(agent=agent, environment=environment)

# Train for 200 episodes
runner.run(num_episodes=1200)
runner.close()


# agent = Agent.load(directory='test/testmodel_saver_dqn', format='checkpoint')

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