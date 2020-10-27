import gym
import tensorforce as tf 
from tensorforce import Runner , Agent
from tensorforce.environments.openai_gym import OpenAIGym
import FX_trading


environment = OpenAIGym(level='FXTrading-v0',visualize=False)
# agent = Agent.load(directory='test/testmodel_saver', format='checkpoint')
agent = dict(
        
        agent='ac',
        # Automatically configured network
        network=[
        dict(type='dense', size=10, activation='tanh')
<<<<<<< HEAD
    ],
        batch_size=5, learning_rate=3e-4,
=======
        # dict(type='dense', size=64, activation='tanh')
    ],
        batch_size=1, learning_rate=3e-4,
>>>>>>> 295c222794a1b6895661dccb254a8983c7675fae
        # Save agent every 10 updates and keep the 5 most recent checkpoints
        summarizer = dict(directory= 'test/summary_ac'),
        saver=dict(directory='test/testmodel_saver3', frequency=10, max_checkpoints=20),
        memory = 60000
    )
runner = Runner(agent=agent, environment=environment)

# Train for 200 episodes
runner.run(num_episodes=2000)
runner.close()


# agent = Agent.load(directory='test/testmodel_saver', format='checkpoint')

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