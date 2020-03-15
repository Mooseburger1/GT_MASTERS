import tensorflow as tf
import numpy as np 
from tensorflow.keras.models import load_model


#Agent for learning
class Agent():
    def __init__(self,lr, gamma, n_actions, epsilon, batch_size, input_dims, epsilon_dec=1e-3, epsilon_end=0.01, mem_size=1000000, saveModel='default.h5'):
        self.action_space = [i for i in range(n_actions)]
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_dec = epsilon_dec
        self.eps_min = epsilon_end
        self.batch_size = batch_size
        self.model_file = saveModel
        self.memory = MemoryBuffer(mem_size, input_dims)
        self.q_eval = DQN(lr, n_actions, input_dims, 256, 256)

    def train(self):

        #Check for enough saved memory
        if self.memory.mem_cntr < self.batch_size:
            return

        #get a batch from memory to train on
        states, actions, rewards, states_, dones = self.memory.sample_memory(self.batch_size)

        #Use NN to predict Qvals on s and s'
        q_eval = self.q_eval.predict(states)
        q_next = self.q_eval.predict(states_)


        q_target = np.copy(q_eval)
        batch_index = np.arange(self.batch_size, dtype=np.int32)

        #Calculate total expected returns for the Q-target
        q_target[batch_index, actions] = rewards + self.gamma * np.max(q_next, axis=1)*dones

        #Train NN
        self.q_eval.train_on_batch(states, q_target)

        #Decay epsilon
        self.epsilon = self.epsilon - self.epsilon_dec if self.epsilon > self.eps_min else self.epsilon


    def save_model(self):
        self.q_eval.save(self.model_file)

    def load_model(self):
        self.q_eval = load_model(self.model_file)

    def store_memory(self, state, action, reward, new_state, done):
        self.memory.store_memory(state, action, reward, new_state, done)

    def choose_action(self, observation):
        if np.random.random() < self.epsilon:
            action = np.random.choice(self.action_space)
        else:
            state = np.array([observation])
            actions = self.q_eval.predict(state)

            action = np.argmax(actions)

        return action

#This will be used to keep track of memory of agent actions
class MemoryBuffer():
    def __init__(self, mem_size, input_dims):
        #how much memory the agent can store
        self.mem_size = mem_size
        #How much memory has been added
        self.mem_cntr = 0
        #Initalize empty memory 
        self.state_memory = np.zeros((self.mem_size, *input_dims), dtype=np.float32)
        #Initialize empty memory for new states
        self.new_state_memory = np.zeros((self.mem_size, *input_dims), dtype=np.float32)
        #Initialize empty memory for actions
        self.action_memory = np.zeros(self.mem_size, dtype=np.int32)
        #Initialize empty memory for rewards
        self.reward_memory = np.zeros(self.mem_size, dtype=np.float32)
        #Initialize empty memory for done checks
        self.terminal_memory = np.zeros(self.mem_size, dtype=np.int32)

    #Method for persiting actions, states, rewards, dones to memory
    def store_memory(self, state, action, reward, state_, done):
        index = self.mem_cntr % self.mem_size
        self.state_memory[index] = state
        self.new_state_memory[index] = state_
        self.reward_memory[index] = reward
        self.action_memory[index] = action
        self.terminal_memory[index] = 1 - int(done)
        self.mem_cntr += 1

    #smaple memory for training
    def sample_memory(self, batch_size):
        max_mem = min(self.mem_cntr, self.mem_size)
        batch = np.random.choice(max_mem, batch_size, replace=False)

        states = self.state_memory[batch]
        states_ = self.new_state_memory[batch]
        rewards = self.reward_memory[batch]
        actions = self.action_memory[batch]
        terminal = self.terminal_memory[batch]

        return states, actions, rewards, states_, terminal


def DQN(lr, n_actions, input_dims, fc1_dims, fc2_dims):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(fc1_dims, activation='relu'),
        tf.keras.layers.Dense(fc2_dims, activation='relu'),
        tf.keras.layers.Dense(n_actions, activation=None)
    ])

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=lr), loss='mse')
    return model