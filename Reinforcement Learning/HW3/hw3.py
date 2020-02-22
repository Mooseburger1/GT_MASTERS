import gym
import numpy as np
from numpy import random


actions = {0: '<', 1:'v', 2:'>', 3:'^'}


custom_map = 'SFFG'
GAMMA = 0.93
ALPHA = 0.23
EPSILON = 0.14
EPISODES = 42425
seed = 359700


MAP_ = np.array([x for x in custom_map])
reshape = int(np.sqrt(len(MAP_)))
MAP_ = MAP_.reshape(reshape,-1)


ENV = gym.make('FrozenLake-v0', desc=MAP_).unwrapped


random.seed(seed)
ENV.seed(seed)

num_states = MAP_.shape[0] * MAP_.shape[1]
num_actions = 4

Q = np.zeros((num_states, num_actions))


for t in range(EPISODES):
    done = 0
    s = ENV.reset()
    
    if np.random.random() < EPSILON:
        a = np.random.randint(0,4)
    else:
        a = np.argmax(Q[s])
    
    while not done:
        s2, r, done, info = ENV.step(a)
       
        if np.random.random() < EPSILON:
            a2 = np.random.randint(0,4)
        else:
            a2 = np.argmax(Q[s2])

        Q[s][a] = Q[s][a] + ALPHA * (r + GAMMA * Q[s2][a2] - Q[s][a])

        s = s2
        a = a2

results = []
for row in Q:
    results.append(actions[np.argmax(row)])

print(','.join(results))