from soccerfield import SoccerField
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import time
import argparse
import sys

mpl.rcParams['agg.path.chunksize'] = 10000



parser = argparse.ArgumentParser()
parser.add_argument('-g', '--gamma', dest='gamma', help='gamma', default=0.9)
parser.add_argument('-a', '--alpha', dest='alpha', help='alpha', default=0.5)
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

np.random.seed(9611)

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
    q1 = np.random.rand(num_states, num_actions)
    q2 = np.random.rand(num_states, num_actions)


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
        

        # guague performance against going south
        base_q = q1[s_base][1]
            
        # get index for state s
        state_index = game.state_to_index(s)

        eps = np.random.rand()
        if eps < EPSILON:
            a1_1_index = np.random.randint(5)
            a1_1 = actions[a1_1_index]

            a2_1_index = np.random.randint(5)
            a2_1 = actions[a2_1_index]
        else:
            a1_1_index = np.argmax(q1[state_index])
            a1_1 = actions[a1_1_index]

            a2_1_index = np.random.randint(5)
            a2_1 = actions[a2_1_index]


        s_prime, reward, done = game.advance( (a1_1, a2_1) )

        render()

        r1 = reward[0]
        r2 = reward[1]

        state_prime_index = game.state_to_index(s_prime)

        a1_2_index = np.argmax(q1[state_prime_index])
        a2_2_index = np.argmax(q2[state_prime_index])

        q1[state_index, a1_1_index] = q1[state_index, a1_1_index] + ALPHA * (r1 + GAMMA * q1[state_prime_index, a1_2_index] - q1[state_index, a1_1_index])


        s = s_prime

        ALPHA *= np.e ** (-np.log(500.0) / 10 ** 6)
        

        #print(episode, ': ', np.abs(q1[s_init, base_action] - base_q))
        if state_index == s_base and a1_1_index==1 and iter_ %5 == 0:
            
            delta.append(np.abs(q1[s_base][1] - base_q))
            #print('Error: ',np.abs(q1[s_init][4] - base_q) )
            indices.append(iter_)
            alphas.append(ALPHA)


    plt.figure(figsize=(15,8))
    plt.ylim([0, 0.5])
    plt.plot(indices, delta, color='lightslategray')
    plt.title('Q')
    plt.xlabel('Simulation Iteration')
    plt.ylabel('Q-value Difference')

    plt.twinx()

    plt.plot(indices, alphas, color = 'k' , ls='--')
    plt.ylabel('alpha')
    plt.savefig('Qsoccer.png', bbox_inches='tight')
    plt.show()  
            




            