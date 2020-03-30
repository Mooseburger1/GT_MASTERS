from soccerfield import SoccerField, player
import numpy as np
import matplotlib.pyplot as plt
import time

np.random.seed(42)


if __name__ == '__main__':

    game = SoccerField(epsilon=0.001)
    episodes = 1

    for ep in range(episodes):
        game.reset_environment()
        game.status = 'New Game'
        #game.render()
        time.sleep(1)
        done = False

        
            
        print(game.states)
            # print(game.rewards)
            # print(game.actions)
            