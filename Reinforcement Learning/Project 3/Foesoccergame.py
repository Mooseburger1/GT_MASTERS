from soccerfield import SoccerField
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import time
import argparse
from utils import solve_lp
import sys 
from cvxopt.modeling import op, variable
from cvxopt.solvers import options
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
ALPHA_MIN = 0.5

assert GAME_SPEED in ('slow', 'normal', 'fast', 'faster', 'fastest'), 'Game speed arguemnt [-s | --speed] can only be [slow | normal | fast | faster | fastest]'

GAME_SPEED = speeds[GAME_SPEED]
ALPHA_DECAY = (ALPHA - ALPHA_MIN) /ITERATIONS


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
    Q = np.ones((num_states, num_actions, num_actions))
    V1 = np.ones((num_states))
    PI = np.ones((num_states, num_actions)) / num_actions

    
    #q2 = np.zeros((num_states, num_actions, num_actions))


    if GAME_SPEED != 'headless':
        game.reset_environment()
        game.status = 'NEW GAME'
        game.render()
        render('NEW GAME')
        done = False
    else:
        game.reset_environment()
        done = False
    
   

    delta = []
    indices = []
    alphas = []
    epsilons = []

    s = game.state
    base_s = game.state_to_index(s)
    done = False

    for i in range(ITERATIONS):
        print('Iteration: ', i)


        if done:
            game.reset_environment()
            render('New Game')
            s = game.state
            done=False

        state_index = game.state_to_index(s)
        
        eps = np.random.rand()

        base_q = copy.deepcopy(Q[71, 1, 4])
        
        a1_index = np.random.randint(5)
        a2_index = np.random.randint(5)


        a = (actions[a1_index], actions[a2_index])

        s_prime, rewards, done = game.advance(a)
      
        s_prime_index = game.state_to_index(s_prime)

        ra = rewards[0]
        rb = rewards[1]


        

        Q[state_index, a1_index, a2_index] = (1-ALPHA) * Q[state_index, a1_index, a2_index] + ALPHA * (ra + GAMMA + V1[s_prime_index])

        

        v_star , probs = solve_lp(copy.deepcopy(Q[state_index]))
        
        V1[state_index] = v_star

        PI[state_index] = probs

        ALPHA *= np.e ** (-np.log(500.0) / 10 ** 6)


        if state_index == 71 and a1_index==1 and a2_index ==4:
            
            err = np.abs(Q[state_index, a1_index, a2_index] - base_q)
            delta.append(err)
            indices.append(i)
            alphas.append(ALPHA)

        s = s_prime
            

    
    
    plt.figure(figsize=(15,8))
    plt.ylim([0, 0.5])
    plt.plot(indices, delta, color='lightslategray')
    plt.savefig('Foesoccer2.png', bbox_inches='tight')
    plt.show()
    
    plt.figure(figsize=(15,8))
    plt.plot(alphas)
    plt.show()

    # plt.figure(figsize=(15,8))
    # plt.plot(epsilons)
    # plt.show()
            



            # done = True
 
    # for iter_ in range(ITERATIONS):
        
    #     if done:
            
    #         #reset environment
    #         game.reset_environment()
    #         render('NEW GAME')
    #         #intial state in the form (possession, player-A position, player-B position)
    #         s = game.state
    #         s_base = game.state_to_index(game.state)
        

    #     # guague performance against South action for player A and Stick for Player B
    #     base_q = (q1[s_base][1][4]).copy()
            
    #     # get index for state s
    #     state_index = game.state_to_index(s)
    #     current_q = (q1[state_index]).copy()
    #     a1_1_index = np.random.choice(np.arange(5))
    #     a1_1 = actions[a1_1_index]

    #     a2_1_index = np.random.choice(np.arange(5))
    #     a2_1 = actions[a2_1_index]


    #     a = (a1_1, a2_1)
    #     # if iter_ > 15:
    #     #     input('Action is: {}'.format(a))

    #     s_prime, reward, done = game.advance( a )

    #     render()
    #     # print('INPUT: \n', q1[state_index])
        
    #     # print('OUTPUT: \n', prime_objective)
    #     # input('enter')
    #     r1 = reward[0]
    #     r2 = reward[1]

    #     state_prime_index = game.state_to_index(s_prime)

    #     prime_objective = solve_maximin(current_q)
        


    #     q1[state_index][a1_1_index][a2_1_index] = (1 - ALPHA) * q1[state_index][a1_1_index][a2_1_index] + \
    #                 ALPHA * ((1 - GAMMA) * r1 + GAMMA * prime_objective)
        
    #     s = s_prime

    #     # EPSILON = EPSILON* ALPHA_DECAY

    #     ALPHA = ALPHA * .999999
    #     alphas.append(ALPHA)

    #     #print(episode, ': ', np.abs(q1[s_init, base_action] - base_q))
    #     if state_index == s_base and a1_1_index==1 and a2_1_index==4:
    #         delta.append(np.abs(q1[s_base][1][4] - base_q))
    #         #print('Error: ',np.abs(q1[s_init][4] - base_q) )
    #         print(iter_, np.abs(q1[s_base][1][4] - base_q))
    #         indices.append(iter_)


    




            