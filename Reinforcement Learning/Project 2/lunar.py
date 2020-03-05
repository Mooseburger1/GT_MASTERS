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
'''
State representation
(x, y, vx, vy, theta, v_theta, leg_l, leg_r)

x and y = coordinates of the lander
vx and vy = velocity components
theta = angle of lander
v_theta = angular velocity
leg_l and leg_r = indication of leg touching the ground
'''


REPLAY_MEMORY_SIZE = 50_000
MIN_REPLAY_MEMORY_SIZE = 1_000
MODEL_NAME = 'DENSE'
ENV_OBSERVATION_SPACE = (8,1)
ACTION_SPACE = 4
MINIBATCH_SIZE = 64
UPDATE_TARGET_EVERY = 5
DISCOUNT=0.99
EPISODES = 20_000
EPSILON = 1
EPSILON_DECAY = 0.99975
MIN_EPSILON = 0.001

class DQNAgent:
    def __init__(self):

        #main model - gets trained every step
        self.model = self.create_model()

        #Target model this is what we predict against every step
        self.target_model = self.create_model()
        self.target_model.set_weights(self.model.get_weights())

        #An array with last n steps for training
        self.replay_memory = deque(maxlen=REPLAY_MEMORY_SIZE)
        logdir = "logs/scalars/" + datetime.now().strftime("%Y%m%d-%H%M%S")
        self.callbacks = tf.keras.callbacks.TensorBoard(log_dir = logdir)
        
        #used to count when to update target network with main network's weights
        self.target_update_counter = 0

    def create_model(self):
        model = Sequential()
        model.add(tf.keras.layers.Dense(units=28, activation='tanh', input_shape=ENV_OBSERVATION_SPACE))
        model.add(tf.keras.layers.Dense(units=56, activation='tanh'))
        model.add(tf.keras.layers.Dense(units=28, activation='tanh'))
        model.add(tf.keras.layers.Dense(units=ACTION_SPACE))

        model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])

        return model

    #Adds step's data to a memory replay array
    #(observation space, action, reward, new observation space, done)
    def update_replay_memory(self, transition):
        self.replay_memory.append(transition)

    #Queries main network for Q values given current observation space (environment state)
    def get_qs(self, state):
        pred = self.model.predict(np.array(state).reshape(-1, 8,1))[0]
        print('PREDICTION IS !!!!!!!!!!!!', pred)
        return pred
    def train(self, terminal_state, step):

        # Start training only if certain number of samples is already saved
        if len(self.replay_memory) < MIN_REPLAY_MEMORY_SIZE:
            return

        #Get minibatch of random samples from memory replay table
        minibatch = random.sample(self.replay_memory, MINIBATCH_SIZE)

        #Get future states from minibatch, then query NN model for Q values
        current_states = np.array(transition[0] for transition in minibatch)
        current_qs_list = self.model.predict(current_states)

        #Get future states from minibatch, then query NN model for Q values
        new_current_states = np.array([transition[3] for transition in minibatch])
        future_qs_list = self.target_model.predict(new_current_states)

        X = []
        y = []

        for index, (current_state, action, reward, new_current_state, done) in enumerate(minibatch):

            #if not a terminal state, get new q from future states, otherwise set it to 0
            #almost like with Q learning, but we use just part of equation here
            if not done:
                max_future_q = np.max(future_qs_list[index])
                new_q = reward + DISCOUNT * max_future_q
            else:
                new_q = reward

            #Update Q value for given state
            current_qs = current_qs_list[index]
            current_qs[action] = new_q

            # appen to training data
            X.append(current_state)
            y.append(current_qs)

            #fit on all samples as one batch, log only on terminal state
            self.model.fit(np.array(X), np.array(y), batch_size=MINIBATCH_SIZE, verbose=0, shuffle=False, callbacks = [self.callbacks] if terminal_state else None)

            #update target network counter every episode
            if terminal_state:
                self.target_update_counter += 1

            #if counter reaches set value, update target network with weights of main network
            if self.target_update_counter > UPDATE_TARGET_EVERY:
                self.target_model.set_weights(self.model.get_weights())
                self.target_update_counter = 0

if __name__ == '__main__':
    
    agent = DQNAgent()

    ep_rewards = []

    if not os.path.isdir('models'):
        os.makedirs('models')

    env = gym.make('LunarLander-v2')
    
    random.seed(1)
    env.seed(1)
    tf.random.set_seed(1)

    for episode in tqdm(range(1, EPISODES+1), ascii=True, unit='Episodes'):
        agent.callbacks.step = episode

        episode_reward = 0
        step = 1

        current_state = env.reset()

        done = False
        while not done:

            if np.random.random() > EPSILON:
                action = np.argmax(agent.get_qs(current_state))

            else:
                action = np.random.randint(0, ACTION_SPACE)


            new_state, reward, done, info = env.step(action)

            episode_reward += reward

            if episode % 10 == 0:
                env.render()

            agent.update_replay_memory((current_state, action, reward, new_state, done))

            agent.train(done, step)

            current_state = new_state

            step += 1

        ep_rewards.append(episode_reward)
        print('Episode: {}\tReward: {}'.format(episode, episode_reward))

        if EPSILON > MIN_EPSILON:
            EPSILON *= EPSILON_DECAY
            EPSILON = max(MIN_EPSILON, EPSILON)
