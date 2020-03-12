import gym
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.optimizers import Adam
from collections import deque
import numpy as np
import random
from datetime import datetime
import os
from tqdm import tqdm
import time
from agent import DQNAgent
'''
State representation
(x, y, vx, vy, theta, v_theta, leg_l, leg_r)

x and y = coordinates of the lander
vx and vy = velocity components
theta = angle of lander
v_theta = angular velocity
leg_l and leg_r = indication of leg touching the ground
'''


# REPLAY_MEMORY_SIZE = 50_000
# MIN_REPLAY_MEMORY_SIZE = 1_000
# MODEL_NAME = 'DENSE'
# ENV_OBSERVATION_SPACE = (1,8)
ACTION_SPACE = 4
# MINIBATCH_SIZE = 64
# UPDATE_TARGET_EVERY = 5
DISCOUNT=0.99


# Environment settings
EPISODES = 1_000


# Exploration settings
EPSILON = 1  # not a constant, going to be decayed
EPSILON_DECAY = 0.99
MIN_EPSILON = 0.001


if __name__ == '__main__':
    
    agent = DQNAgent()
    
    if not os.path.isdir('models'):
        os.makedirs('models')


    env = gym.make('LunarLander-v2')
    
    random.seed(42)
    env.seed(42)
    tf.random.set_seed(42)

    for episode in tqdm(range(1, EPISODES+1), ascii=True, unit='Episodes'):
        
                # agent.model.save_weights('models/checkpoint_{}'.format(episode / 10))
        

        
        episode_reward = 0
        step = 1
        agent.episode = episode
        current_state = env.reset()

        done = False
        while not done:

            if np.random.random() > EPSILON:
                action = np.argmax(agent.get_qs(current_state))

            else:
                action = np.random.randint(0, ACTION_SPACE)


            new_state, reward, done, info = env.step(action)


            episode_reward += reward

            agent.update_replay_memory((current_state, action, reward, new_state, done))

            agent.train(done, step)

            current_state = new_state

            step += 1

        if episode % 5 == 0:
            current_state = env.reset()
            done = False
            while not done:
                action = np.argmax(agent.get_qs(current_state))
                print('Current state is: ', current_state)
                print('Action is: ', action)
                print('Actions available: ', agent.get_qs(current_state))
                print('\n')
                new_state, reward, done, info = env.step(action)
                env.render()
                current_state = new_state



        with open('rewards.txt', 'a') as file:
            file.write(str(time.time()))
            file.write(',' + str(episode))
            file.write(',' + str(episode_reward))
            file.write('\n')



        print('Episode: {}\tReward: {}'.format(episode, episode_reward))

        with open('epsilon_decay.txt', 'a') as file:
            file.write(str(time.time()))
            file.write(',' + str(episode))
            file.write(',' + str(EPSILON))
            file.write('\n')

        if EPSILON > MIN_EPSILON:
            EPSILON *= EPSILON_DECAY
            EPSILON = max(MIN_EPSILON, EPSILON)
    
            
