from soccerfield import SoccerField
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import time
import argparse
import matplotlib.patheffects as path_effects

mpl.rcParams['agg.path.chunksize'] = 10000



parser = argparse.ArgumentParser()
parser.add_argument('-g', '--gamma', dest='gamma', help='gamma', default=0.9)
parser.add_argument('-a', '--alpha', dest='alpha', help='alpha', default=1.0)
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
ALPHA_MIN = 0.001

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

    #dictionary of the 25 joint actions available as an Orderdict
    actions = game.actions
    
    # Number of states
    num_states = len(game.states)

    # Number of actions
    num_actions = len(actions)

    #initialize Q tables
    q1 = np.zeros((num_states, num_actions))
    q2 = np.zeros((num_states, num_actions))


    if GAME_SPEED != 'headless':
        game.status = 'NEW GAME'
        game.render()
        render('NEW GAME')
    
   

    delta = []
    indices = []
    alphas = []
    epsilons = []

    done = True
    for iter_ in range(ITERATIONS):
        
        if done:
            #reset environment
            game.reset_environment()
            render('NEW GAME')
            #intial state in the form (possession, player-A position, player-B position)
            s = game.state
            s_base = game.state_to_index(game.state)
        

        # gauge performance where action is player A goes South and player B sticks
        base_action = game.action_to_index(((1,0), (0,0)))
        base_q = q1[s_base][base_action]

            
        # get index for state s
        state_index = game.state_to_index(s)

        eps = np.random.rand()
        if eps < EPSILON:
            a1_1_index = np.random.randint(num_actions)
            a1_1 = list(game.actions.keys())[a1_1_index]

            a2_1_index = np.random.randint(num_actions)
            a2_1 = list(game.actions.keys())[a2_1_index]
        else:
            a1_1_index = np.argmax(q1[state_index])
            a1_1 = list(game.actions.keys())[a1_1_index]

            a2_1_index = np.argmax(q2[state_index])
            a2_1 = list(game.actions.keys())[a2_1_index]


        a = (a1_1[0], a2_1[1])

        s_prime, reward, done = game.advance( a )

        render()

        r1 = reward[0]
        r2 = reward[1]

        state_prime_index = game.state_to_index(s_prime)

        a1_2_index = np.argmax(q1[state_prime_index])
        a2_2_index = np.argmax(q2[state_prime_index])

        a_index = game.action_to_index(a)
        
        q1[state_index][a_index] = (1 - ALPHA) * q1[state_index][a_index] + \
                ALPHA * ((1 - GAMMA) * r1 + GAMMA * q1[state_prime_index][a1_2_index])
        
        
        q2[state_index][a_index] = (1 - ALPHA) * q2[state_index][a_index] + \
                ALPHA * ((1 - GAMMA) * r2 + GAMMA * q2[state_prime_index][a2_2_index])

        


        s = s_prime



    
        # EPSILON = EPSILON* ALPHA_DECAY

        ALPHA *= .999999
        alphas.append(ALPHA)
        # epsilons.append(EPSILON)

    

        
        #print(episode, ': ', np.abs(q1[s_init, base_action] - base_q))
        if state_index == s_base and a_index == base_action:
            
            delta.append(np.abs(q1[s_base][base_action] - base_q))
            #print('Error: ',np.abs(q1[s_init][4] - base_q) )
            indices.append(iter_)
            


    plt.figure(figsize=(15,8))
    plt.ylim([0, 0.5])
    plt.plot(indices, delta, color='dodgerblue', ls='--',lw=2, path_effects=[path_effects.Stroke(linewidth=3, foreground='black'), path_effects.Normal()])
    plt.savefig('Freinds.png', bbox_inches='tight')
    plt.show()
    
    plt.figure(figsize=(15,8))
    plt.plot(alphas)
    plt.show()

    # plt.figure(figsize=(15,8))
    # plt.plot(epsilons)
    # plt.show()
            




            