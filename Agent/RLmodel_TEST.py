import gym
import tensorforce as tf 
from tensorforce import Runner , Agent
from tensorforce.environments.openai_gym import OpenAIGym
import FX_trading


<<<<<<< Updated upstream
environment = OpenAIGym(level='FXTrading-v0',visualize=False)
agent = dict(
        
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        agent='ac',
=======
        agent='dqn',
>>>>>>> Stashed changes
        # Automatically configured network
        network='auto',
        batch_size=1, update_frequency=2, learning_rate=3e-4,
        # Save agent every 10 updates and keep the 5 most recent checkpoints
<<<<<<< Updated upstream
        summarizer = dict(directory= 'test/summaries'),
        saver=dict(directory='test/testmodel_saver', frequency=10, max_checkpoints=20),
=======
        summarizer = dict(directory= 'test/summary_dqn'),
        saver=dict(directory='test/testmodel_saver', frequency=10, max_checkpoints=1000),
>>>>>>> Stashed changes
=======
        agent='ppo',
        # Automatically configured network
        network=[
        dict(type='dense', size=10, activation='tanh'),
        dict(type='dense', size=20, activation='tanh'),
        dict(type='dense', size=10, activation='tanh')
=======
environment = OpenAIGym(level='FXTrading-v99',visualize=False)
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
>>>>>>> Stashed changes
    ],
        batch_size=5, learning_rate=3e-4,max_episode_timesteps = 1000,
        # Save agent every 10 updates and keep the 5 most recent checkpoints
        summarizer = dict(directory= 'test/summary'),
        saver=dict(directory='test/testmodel_saver', frequency=10, max_checkpoints=1000),
>>>>>>> Stashed changes
        memory = 60000
    )
runner = Runner(agent=agent, environment=environment)

<<<<<<< Updated upstream
# Train for 200 episodes
<<<<<<< Updated upstream
<<<<<<< Updated upstream
runner.run(num_episodes=1000)
=======
runner.run(num_episodes=1500)
>>>>>>> Stashed changes
=======
runner.run(num_episodes=1000)
>>>>>>> Stashed changes
runner.close()
# agent = Agent.load(directory='model', format='checkpoint')
=======
# # Train for 200 episodes
runner.run(num_episodes=500,save_best_agent='C:/Users/Z77X/Documents/GitHub/Mammon_project/test')
runner.close()


# agent = Agent.load(directory='test11/testmodel_saver_dqn1', format='checkpoint')
>>>>>>> Stashed changes

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