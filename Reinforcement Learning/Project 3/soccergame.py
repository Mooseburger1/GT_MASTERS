from soccerfield import SoccerField, player
import numpy as np
import matplotlib.pyplot as plt
import time

np.random.seed(42)


if __name__ == '__main__':

    game = SoccerField(epsilon=0.001)
    episodes = 10000

    for ep in range(episodes):
        game.reset_environment()
        game.status = 'New Game'
        game.render()
        time.sleep(1)
        done = False

        while not done:
            
            done = game.advance()
            print('Player A position: ', game.playerA.position)
            print('Player A has ball: ', game.playerA.possession)
            print('Player B position: ', game.playerB.position)
            print('Player B has ball: ', game.playerB.possession)
            print('Done: ', game.done)

            print('\n\n\n')

            game.render()
            time.sleep(1)
            