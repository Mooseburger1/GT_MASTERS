import numpy as np
import gym
import os
import time


tick = time.time()
clear = lambda: os.system('clear')

env = gym.make('Taxi-v2').env

alpha = 0.5
epsilon = 0.3
gamma = 0.9


#env.reset()
#observation, reward, done, info = env.step(a)
'''
Action Space
0=south
1=north
2=east
3=west
4=pickup
5=dropoff
'''

Q = np.zeros([env.observation_space.n, env.action_space.n])

for i in range(200000):
    s = env.reset()

    done = False


    while not done:

        if np.random.random() < epsilon:
            a = np.random.randint(0, 6)
        else:
            a = np.argmax(Q[s])

        s2, r, done, info = env.step(a)

        a2 = np.argmax(Q[s2])

        Q[s][a] = Q[s][a] + alpha * (r + gamma * Q[s2][a2] - Q[s][a])

        s = s2



print('Q(18, 3): ', Q[18,3])
print('Q(19, 3): ', Q[19,3])
print('Q(496, 1): ', Q[496,1])
print('Q(82, 5): ', Q[82,5])
print('Q(373, 0): ', Q[373,0])
print('Q(132, 3): ', Q[132,3])
print('Q(252, 4): ', Q[252,4])
print('Q(343, 1): ', Q[343,1])
print('Q(136, 3): ', Q[136,3])
print('Q(442, 0): ', Q[442,0])
print('\n\n')
print('Q(462, 4): ', Q[462,4])
print('Q(398, 3): ', Q[398,3])
print('Q(253, 0): ', Q[253,0])
print('Q(377, 1): ', Q[377,1])
print('Q(83, 5): ', Q[83,5])

print('Took {} seconds'.format(time.time() - tick))