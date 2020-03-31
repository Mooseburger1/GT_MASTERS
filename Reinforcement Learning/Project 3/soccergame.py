from soccerfield import SoccerField, player
import numpy as np
import matplotlib.pyplot as plt
import time

np.random.seed(2)
GAME_SPEED = 0.01

if __name__ == '__main__':

    game = SoccerField()
    episodes = 3

    for ep in range(episodes):
        game.reset_environment()
        game.status = 'New Game'
        game.render()
        game.status = 'New Game'
        game.render()
        time.sleep(GAME_SPEED)

        done = False

        counter = 0
        while not done:
            print('Move # ', counter)
            action = game.random_action()

            print(action)
            
            s_prime, reward, done = game.advance(action)
            print('STATUS: ',game.status)
            print('HAS BALL: ', game.playerA.possession, game.playerB.possession)
            game.render()
            time.sleep(GAME_SPEED)
            print('\n\n')
            

            # print('Next State: ', s_prime)
            # print('Reward: ', reward)
            # print('Done: ', done)
            if counter == 25:
                done = True

            counter +=1
        

            