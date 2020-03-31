from soccerfield import SoccerField
import numpy as np
import matplotlib.pyplot as plt
import time
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-g', '--gamma', dest='gamma', help='gamma', default=0.99)
parser.add_argument('-a', '--alpha', dest='alpha', help='alpha', default=0.5)
parser.add_argument('-e', '--epsilon', dest='epsilon', help='Epsilon Decay Factor', default=.5)
parser.add_argument('-s', '--speed', dest='game_speed', help='Game speed [slow | normal | fast | faster | fastest]', default='normal')
parser.add_argument('-i', '--iter', dest='iter', help='Number of training iterations', default=10000)
args = parser.parse_args()

speeds = {'slow': 3, 'normal': 1, 'fast': 0.1, 'faster': 0.01}

GAMMA = float(args.gamma)
ALPHA = float(args.alpha)
EPSILON = float(args.epsilon)
GAME_SPEED = args.game_speed
ITERATIONS = int(args.iter)
MAX_MOVES = 25

assert GAME_SPEED in ('slow', 'normal', 'fast', 'faster', 'fastest'), 'Game speed arguemnt [-s | --speed] can only be [slow | normal | fast | faster | fastest]'

GAME_SPEED = speeds[GAME_SPEED]


np.random.seed(2)

def render(status=None):
    if GAME_SPEED != 'fastest':
        game.status=status
        game.render()
        time.sleep(GAME_SPEED)

if __name__ == '__main__':

    game = SoccerField()

    # N-S-E-W-STICK
    actions = [(-1,0), (1,0), (0,1), (0,-1), (0,0)]
    
    # Number of states
    num_states = len(game.states)

    # Number of actions
    num_actions = len(actions)

    #initialize Q tables
    q1 = np.random.rand(num_states, num_actions)
    q2 = np.random.rand(num_states, num_actions)


    if GAME_SPEED != 'fastest':
        game.status = 'NEW GAME'
        game.render()
        render('NEW GAME')
    
   

    delta = []

    for episode in range(ITERATIONS):
        
        #reset environment
        game.reset_environment()
        render('NEW GAME')
        #intial state in the form (possession, player-A position, player-B position)
        s = game.state

        # guague performance against STICK action and STICK Q Value
        base_action = 4
        base_q = q1[game.state_to_index(s), base_action]

        counter = 0
        done = False
        while (not done) and (counter != MAX_MOVES):
            
            # get index for state s
            state_index = game.state_to_index(s)

            eps = np.random.rand()
            if eps <= EPSILON:
                a1 = actions[np.random.randint(5)]
                a2 = actions[np.random.randint(5)]
            else:
                a1 = actions[np.argmax(q1[state_index])]
                a2 = actions[np.argmax(q2[state_index])]


            s_prime, reward, done = game.advance( (a1, a2) )

            render()

            r1 = reward[0]
            r2 = reward[1]

            state_prime_index = game.state_to_index(s_prime)

            a1_2 = np.argmax(q1[state_prime_index])
            a2_2 = np.argmax(q2[state_prime_index])

            q1[state_index, a1] = q1[state_index, a1] + ALPHA * (r1 + GAMMA * q1[state_prime_index, a1_2] - q1[state_index, a1])
            q2[state_index, a2] = q2[state_index, a2] + ALPHA * (r2 + GAMMA * q2[state_prime_index, a2_2] - q2[state_index, a2])

            #Q[s][a] = Q[s][a] + alpha * (r + gamma * Q[s2][a2] - Q[s][a])
            # print('Current State: ', s)
            # print('Selected Actions: ', (a1,a2))
            # print('Next State: ', s_prime)
            s = s_prime

            
            print(done)
            print(counter)
            counter += 1


            




            