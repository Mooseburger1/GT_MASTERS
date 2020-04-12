from soccerfield import SoccerField
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import time
import argparse
from utils import solve_ceqLP
import sys 
import copy

mpl.rcParams['agg.path.chunksize'] = 10000



parser = argparse.ArgumentParser()
parser.add_argument('-g', '--gamma', dest='gamma', help='gamma', default=0.9)
parser.add_argument('-a', '--alpha', dest='alpha', help='alpha', default=0.9)
parser.add_argument('-e', '--epsilon', dest='epsilon', help='Epsilon Decay Factor', default=0.2)
parser.add_argument('-s', '--speed', dest='game_speed', help='Game speed [slow | normal | fast | faster | fastest]', default='normal')
parser.add_argument('-i', '--iter', dest='iter', help='Number of training iterations', default=1000000)
args = parser.parse_args()

speeds = {'slow': 3, 'normal': 1, 'fast': 0.1, 'faster': 0.01, 'fastest':'headless'}

GAMMA = float(args.gamma)
ALPHA = float(args.alpha)
EPSILON = float(args.epsilon)
GAME_SPEED = args.game_speed
ITERATIONS = int(args.iter)


assert GAME_SPEED in ('slow', 'normal', 'fast', 'faster', 'fastest'), 'Game speed arguemnt [-s | --speed] can only be [slow | normal | fast | faster | fastest]'

GAME_SPEED = speeds[GAME_SPEED]

np.random.seed(42)

def render(status=None):
    if GAME_SPEED != 'headless':
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
    q1, q2 = np.ones((num_states, num_actions, num_actions)) , np.ones((num_states, num_actions, num_actions))

    V1, V2 = np.ones((num_states)), np.ones((num_states))

    if GAME_SPEED != 'headless':
        game.status = 'NEW GAME'
        game.render()
        render('NEW GAME')
    
   

    delta = []
    indices = []
    alphas = []


    done = True
 
    for iter_ in range(ITERATIONS):
        print('Iteration: ', iter_)
        if done:
            #reset environment
            game.reset_environment()
            render('NEW GAME')
            #intial state in the form (possession, player-A position, player-B position)
            s = game.state
            s_base = game.state_to_index(game.state)
        

        # guague performance against South action for player A and Stick for Player B
        base_q = q1[s_base][1][4]
            
        # get index for state s
        state_index = game.state_to_index(s)

        a1_1_index = np.random.randint(5)
        a1_1 = actions[a1_1_index]

        a2_1_index = np.random.randint(5)
        a2_1 = actions[a2_1_index]

        a = (a1_1, a2_1)

        s_prime, reward, done = game.advance( a )

        render()

        r1 = reward[0]
        r2 = reward[1]

        state_prime_index = game.state_to_index(s_prime)

        def LP(q1, q2, state_index):

            lp = solve_ceqLP(copy.deepcopy(q1[state_index]), copy.deepcopy(q2[state_index]))

            if lp == None:
                return 0, 0, None
            else:
                
                q1_flat = copy.deepcopy(q1[state_index]).flatten().reshape(25,1)
                q2_flat = copy.deepcopy(q2[state_index].T).flatten().reshape(25,1)

                result_A = sum(lp[1:] * q1_flat)[0]
                result_B = sum(lp[1:] * q2_flat)[0]
                return result_A, result_B , lp

        result_A , result_B, probs = LP(q1, q2, state_prime_index)

        if probs != None:
            V1[state_prime_index] = result_A
            V2[state_prime_index] = result_B


        if r1 == 0:
    

            q1[state_index][a1_1_index][a2_1_index] = (1 - ALPHA) * q1[state_index][a1_1_index][a2_1_index] + \
                        ALPHA * ((1-GAMMA)*r1 + GAMMA * V1[state_prime_index])

            q2[state_index][a1_1_index][a2_1_index] = (1 - ALPHA) * q2[state_index][a1_1_index][a2_1_index] + \
                        ALPHA * ((1-GAMMA)*r2 + GAMMA * V2[state_prime_index])

        else:
            q1[state_index][a1_1_index][a2_1_index] = (1 - ALPHA) * q1[state_index][a1_1_index][a2_1_index] + \
                        ALPHA * ((1-GAMMA)*r1 + GAMMA * 0)

            q2[state_index][a1_1_index][a2_1_index] = (1 - ALPHA) * q2[state_index][a1_1_index][a2_1_index] + \
                        ALPHA * ((1-GAMMA)*r2 + GAMMA * 0)


        
        
        s = s_prime

        # EPSILON = EPSILON* ALPHA_DECAY

        ALPHA *= np.e ** (-np.log(500.0) / 10 ** 6)
        

        #print(episode, ': ', np.abs(q1[s_init, base_action] - base_q))
        if state_index == s_base and a1_1_index==1 and a2_1_index==4 and iter_ % 5 == 0:
            
            delta.append(np.abs(q1[s_base][1][4] - base_q))
            #print('Error: ',np.abs(q1[s_init][4] - base_q) )
            indices.append(iter_)
            alphas.append(ALPHA)



    print(q1[s_base])
    result_A , result_B, probs = LP(q1, q2, s_base)
    print(result_A)
    print()
    print(result_B)
    print()
    print(probs[1:])

    plt.figure(figsize=(15,8))
    plt.ylim([0, 0.5])
    plt.plot(indices, delta, color='lightslategray')
    plt.title('Correlated-Q')
    plt.xlabel('Simulation Iteration')
    plt.ylabel('Q-value Difference')

    plt.twinx()

    plt.plot(indices, alphas, color = 'k', ls='--')
    plt.ylabel('alpha')
    plt.savefig('CEQ.png', bbox_inches='tight')
    plt.show()





            