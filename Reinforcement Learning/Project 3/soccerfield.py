import numpy as np
from collections import OrderedDict
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

np.random.seed(42)


class SoccerField:
        def __init__(self, size = (2,4)):

            self.size = size
            self.field = np.zeros(self.size)
            self._build_environment()
            self.reset_environment()
            self.done = False
            self.status = None
            self.status2 = None
            

        def _build_environment(self):
            self.states = {}
            self.rewards = []
            self.actions = OrderedDict()
            counter = 0
            grid = np.zeros(self.size)

            list_of_actions = [(-1,0), (1,0), (0,1), (0,-1), (0,0)]
            #Im possesion 0
            for possession in [0,1]:
                for row in range(grid.shape[0]):
                    for column in range(grid.shape[1]):

                        for i in range(2):
                            for j in range(4):

                                if (row,column) == (i,j):
                                    continue
                                else:
                                    state = (possession, (row,column), (i,j))
                                    self.states[state] = counter
                                    counter += 1
                                    

                                    #check if left side goal and opp has possession - reward should be [-100, 100] - I lose 100 he gains 100 for scoring in my goal
                                    #or
                                    #check if left side goal and I have possession - reward should be [-100, 100] - I lose 100 he gains 100 for me scoring in my own goal
                                    if ((i,j) in [(0,0), (1,0)] and possession == 1) | ((row,column) in [(0,0), (1,0)] and possession == 0):
                                        reward = [100, -100]
                                        self.rewards.append(reward)
                                    #check if right side goal and opp has possession - reward should be [100, -100] - I gain 100 he loses 100 for scoring in his own goal
                                    #or
                                    #check if right side goal and I have possession - reward should be [100, -100] - I gain 100 he loses 100 for me scoring in his goal
                                    elif ((i,j) in [(0,3), (1,3)] and possession == 1) or ((row,column) in [(0,3), (1,3)] and possession==0):
                                        reward = [-100, 100]
                                        self.rewards.append(reward)
                                    #no rewards for anything else
                                    else:
                                        reward = [0 , 0]
                                        self.rewards.append(reward)
            counter = 0
            for a in list_of_actions:
                for b in list_of_actions:
                    action = (b,a)
                    self.actions[action] = counter
                    counter+=1

            self.arrows = {(0,0): '--', (-1,0): '↑', (1,0):'↓', (0,1):'→', (0,-1):'←'}

##################################################################################################

        def random_action(self):
            idx  = np.random.randint(low=0, high=len(self.actions))
            return list(self.actions.keys())[idx]

##################################################################################################

        def _check_posession(self, state):
            if state[0] == 1:
                self.playerB.possession = True
                self.playerA.possession = False
            else:
                self.playerA.possession = True
                self.playerB.possession = False

        def _get_current_posession(self):
            if self.playerB.possession == True and self.playerA.possession == True:
                raise ValueError("There's an error in possession logic - both players have possession")
            elif self.playerB.possession == False and self.playerA.possession == False:
                raise ValueError("There's an error in possession logic - neither player has possession")
            elif self.playerB.possession:
                return 1
            elif self.playerA.possession:
                return 0

        def _swap_possession(self):

            #use _get_current_position error checking to make sure no value error is raise
            _ = self._get_current_posession

            if self.playerA.possession:
                self.playerA.possession = False
                self.playerB.possession = True
            elif self.playerB.possession:
                self.playerB.possession = False
                self.playerA.possession = True
            else:
                raise ValueError("Something went wrong in swapping possession")

##################################################################################################

        def _move_and_check_for_out_of_bounds(self, current_position, next_move):
            next_position = (current_position[0] + next_move[0] , current_position[1] + next_move[1])

            #check if out of bounds moving North or South - if OOB then don't move player
            if next_position[0] < 0 or next_position[0] > 1:
                next_position = current_position

            #check if out of bounds moving East or West - if OOB then don't move player
            if next_position[1] < 0 or next_position[1] > 3:
                next_position = current_position

            return next_position

##################################################################################################

        def state_to_index(self, state):
            return self.states[state]

        def action_to_index(self, action):
            return self.actions[action]

##################################################################################################

        def reset_environment(self):
            self.playerA = player()
            self.playerB = player()

            self.state = (1, (0,2), (0,1))
            #initialize player A's position on the right side of the field
            self.playerA.position = self.state[1]

            #initialize player B's position on the left side of the field
            self.playerB.position = self.state[2]

            #Give player B the ball first
            self._check_posession(self.state) 

            #reset done flag
            self.done = False

            #initial actions
            self.moves = ((0,0), (0,0))

            #reset scores
            self.playerAScore = 0
            self.playerBScore = 0

##################################################################################################
        def advance(self, actions):
            
            self.moves = actions

            playerA_move = actions[0]
            playerB_move = actions[1]

            current_state = self.state

            playerA_curr = current_state[1]
            playerB_curr = current_state[2]

            playerA_next = self._move_and_check_for_out_of_bounds(current_position=playerA_curr, next_move=playerA_move)
            playerB_next = self._move_and_check_for_out_of_bounds(current_position=playerB_curr, next_move=playerB_move)


            coin_flip = np.random.randint(2)
            #if 1 A goes first
            if coin_flip:
                #print('PLAYER A IS MOVING FIRST')
                self._step(first=(playerA_curr, playerA_next, self.playerA), second=(playerB_curr, playerB_next, self.playerB))
            else:
                #print('PLAYER B IS MOVING FIRST')
                self._step(first=(playerB_curr, playerB_next, self.playerB), second=(playerA_curr, playerA_next, self.playerA))


            next_state = (self._get_current_posession(), self.playerA.position, self.playerB.position)
            
            reward = self.rewards[self.states[next_state]]

            #if reward contains 100 or -100, then someone scored and game is over - return done flag set to true
            if 100 in reward:
                self.done = True

            #update positions and score attributes for plotting
            self.playerAScore = reward[0]
            self.playerBScore = reward[1]

            if coin_flip:
                self.status2 = 'Player A moved first'
            else:
                self.status2 = 'Player B moved first'

            if reward[0] == -100 and self.playerA.possession:
                self.status = 'GAME OVER - A SCORED IN OWN GOAL'
            elif reward[0] == -100 and self.playerB.possession:
                self.status = 'GAME OVER - B SCORED IN A GOAL'
            elif reward[0] == 100 and self.playerA.possession:
                self.status = 'GAME OVER - A SCORED IN B GOAL'
            elif reward[0] == 100 and self.playerB.possession:
                self.status = 'GAME OVER - B SCORED IN OWN GOAL'
            else:
                pass

            #update current state tracking
            self.state = next_state



            return (next_state, reward, self.done)



        def _step(self, first, second):

            p1_start = first[0]
            #print('player 1 is at {}'.format(p1_start))
            p1_end = first[1]
            #print('player 1 is trying to get to {}'.format(p1_end))
            p1 = first[2]

            p2_start = second[0]
            #print('player 2 is at {}'.format(p2_start))
            p2_end = second[1]
            #print('player 2 is trying to get to {}'.format(p2_end))
            p2 = second[2]

            if p1_end != p2_start:
                p1.position = p1_end
                #print('player 1 if clear to move to next spot {}'.format(p1.position))
            else:
                p1.position = p1_start
                p1.possession = False
                p2.possession = True
                #print('player 1 is going to run into player 2 - player 1 will stay at {}'.format(p1.position))
                #print('player 1 current ball state (should not have ball) {}'.format(p1.possession))
                #print('player 2 current ball state (should have ball) {}'.format(p2.possession))


            if p2_end != p1.position:
                p2.position = p2_end
                #print('player 2 is clear to move to next spot {}'.format(p2.position))
            else:
                p2.position = p2_start
                p2.possession = False
                p1.possession = True
                #print('player 2 is going to run into player 1 - player 2 will stay at {}'.format(p2.position))
                #print('player 2 current ball state (should not have ball) {}'.format(p2.possession))
                #print('player 1 current ball state (should have ball) {}'.format(p1.possession))
            
            #print('\n')
##################################################################################################
        

        def advance2(self, actions):
            #actions = (my_move, their_move)

            #this is only for rendering
            self.moves = actions
            
            current_state = self.state

            #current positions
            my_current_position = current_state[1]
            
            their_current_position = current_state[2]
            
            #move chosen
            my_move = actions[0]
            
            their_move = actions[1]
            
            #position after move
            my_next_position = self._move_and_check_for_out_of_bounds(current_position=my_current_position, next_move=my_move)
            
            their_next_position = self._move_and_check_for_out_of_bounds(current_position=their_current_position, next_move=their_move)
            
            #flip to see who moves first - 0 they go first - 1 i go first
            coin_flip = np.random.choice((0,1), size=1)[0]

            ######################### LOGIC FOR MOVING TO THE SAME SPOT ####################################

            #if I have ball and move first - I keep ball and move - you stay
            if my_next_position == their_next_position and self.playerA.possession and coin_flip:
                #unless I'm moving into your spot you're are already in - then I stay AND lose ball
                if their_next_position == their_current_position:
                    my_next_position = my_current_position
                    self._swap_possession()
                #do what I said at first
                else:
                    their_next_position = their_current_position

            #if I don't have ball and move first - I get ball and move - you stay and lose ball
            elif my_next_position == their_next_position and self.playerB.possession and coin_flip:
                #Unless I'm moving into your spot you're already in - then I stay BUT get the ball
                if their_next_position == their_current_position:
                    my_next_position = my_current_position
                    self._swap_possession()
                #do what I said at first
                else:
                    their_next_position = their_current_position
                    self._swap_possession()

            #if you have ball and move first - you keep ball and move - I stay
            elif my_next_position == their_next_position and self.playerB.possession and not coin_flip:
                #Unless you are moving into my spot I'm already in - then you stay AND lose the ball
                if my_next_position == my_current_position:
                    their_next_position = their_current_position
                    self._swap_possession()
                #do what I said at first
                else:
                    my_next_position = my_current_position

            #if you don't have ball and move first - You get ball and move - I stay and lose ball
            elif my_next_position == their_next_position and self.playerA.possession and not coin_flip:
                #Unless you are moving into my spot I'm already in - then you stay BUT get the ball
                if my_next_position == my_current_position:
                    their_next_position = their_current_position
                    self._swap_possession()
                #do what I said at first
                else:
                    my_next_position = my_current_position
                    self._swap_possession()

            #if all these fail - then it is safe to perform move step
            else:
                pass


            #################### LOGIC FOR BUMPING INTO EACH OTHER ##################################

            #CHECK FOR A BUMP - IF I'M GOING WHERE YOU CURRENTLY ARE AND YOU ARE GOING WHER I'M CURRENTLY AT, WE BUMP 
            #IF I HAVE BALL AND GO FIRST - NOTHING HAPPENS
            if my_next_position == their_current_position and their_next_position == my_current_position and coin_flip and self.playerA.possession:
                my_next_position = my_current_position
                their_next_position = their_current_position
            #HOWEVER IF I HAVE BALL AND GO SECOND - SWAP POSSESSION
            elif my_next_position == their_current_position and their_next_position == my_current_position and not coin_flip and self.playerA.possession:
                my_next_position = my_current_position
                their_next_position = their_current_position
                self._swap_possession()
            #IF YOU HAVE BALL AND GO FIRST - NOTHING HAPPENS
            elif my_next_position == their_current_position and their_next_position == my_current_position and not coin_flip and self.playerB.possession:
                my_next_position = my_current_position
                their_next_position = their_current_position
            #HOWEVER IF YOU HAVE BALL AND GO SECOND - SWAP POSSESSION
            elif my_next_position == their_current_position and their_next_position == my_current_position and coin_flip and self.playerB.possession:
                my_next_position = my_current_position
                their_next_position = their_current_position
                self._swap_possession()
            else:
                pass

            next_state = (self._get_current_posession(), my_next_position, their_next_position)
            
            reward = self.rewards[self.states[next_state]]

            #if reward contains 100 or -100, then someone scored and game is over - return done flag set to true
            if 100 in reward:
                self.done = True

            #update positions and score attributes for plotting
            self.playerA.position = my_next_position
            self.playerB.position = their_next_position
            self.playerAScore = reward[0]
            self.playerBScore = reward[1]

            if reward[0] == -100 and self.playerA.possession:
                self.status = 'GAME OVER - A SCORED IN OWN GOAL'
            elif reward[0] == -100 and self.playerB.possession:
                self.status = 'GAME OVER - B SCORED IN A GOAL'
            elif reward[0] == 100 and self.playerA.possession:
                self.status = 'GAME OVER - A SCORED IN B GOAL'
            elif reward[0] == 100 and self.playerB.possession:
                self.status = 'GAME OVER - B SCORED IN OWN GOAL'
            else:
                pass

            #update current state tracking
            self.state = np.copy(next_state)



            return (next_state, reward, self.done)

################################################################################################################################

        def advance3(self, actions):
            #actions = (my_move, their_move)

            #this is only for rendering
            self.moves = actions
            
            current_state = self.state

            #current positions
            my_current_position = current_state[1]
            
            their_current_position = current_state[2]
            
            #move chosen
            my_move = actions[0]
            
            their_move = actions[1]
            
            #position after move
            my_next_position = self._move_and_check_for_out_of_bounds(current_position=my_current_position, next_move=my_move)
            
            their_next_position = self._move_and_check_for_out_of_bounds(current_position=their_current_position, next_move=their_move)
            
            #flip to see who moves first - 0 they go first - 1 i go first
            coin_flip = np.random.choice((0,1), size=1)[0]

            ######################### LOGIC FOR MOVING TO THE SAME SPOT ####################################

            ###### I MOVE FIRST #####
            #if i move first with ball and bump into your current location i lose ball and stay
            if my_next_position == their_current_position and coin_flip and self.playerA.possession:
                my_next_position = my_current_position
                self._swap_possession()
            
            #if i move first without ball and bump into your current location I stay
            elif my_next_position == their_current_position and coin_flip and self.playerB.possession:
                my_next_position = my_current_position

            #otherwise it is clear to move
            else:
                pass

            ###### THEY MOVE FIRST #####
            #if they move first with ball and bump into my current location they lose ball and stay
            if their_next_position == my_current_position and not coin_flip and self.playerB.possession:
                their_next_position = their_current_position
                self._swap_possession()
            #if they move first without ball and bump into my current location they stay
            elif their_next_position == my_current_position and not coin_flip and self.playerA.possession:
                their_next_position = their_current_position
            #otherwise it is clear for them to move
            else:
                pass
            

            ###### I MOVE SECOND #######
            #if i move second with ball and bump into their next location I lose ball and stay
            if my_next_position == their_next_position and not coin_flip and self.playerA.possession:
                my_next_position = my_current_position
                self._swap_possession()

            #if i move second without ball and bump into their next location I stay
            elif my_next_position == their_next_position and not coin_flip and self.playerB.possession:
                my_next_position = my_current_position

            #otherwise it is free to move
            else:
                pass

            ###### THEY MOVE SECOND ######
            #if they move second with ball and bump into my next location they lose ball and stay
            if their_next_position == my_next_position and coin_flip and self.playerB.possession:
                their_next_position = their_current_position
                self._swap_possession()

            #if they move second without ball and bump into my next location they stay
            elif their_next_position == my_next_position and coin_flip and self.playerA.possession:
                their_next_position = their_current_position

            #otherwise it is free to move
            else:
                pass

            next_state = (self._get_current_posession(), my_next_position, their_next_position)
            
            reward = self.rewards[self.states[next_state]]

            #if reward contains 100 or -100, then someone scored and game is over - return done flag set to true
            if 100 in reward:
                self.done = True

            #update positions and score attributes for plotting
            self.playerA.position = my_next_position
            self.playerB.position = their_next_position
            self.playerAScore = reward[0]
            self.playerBScore = reward[1]

            if coin_flip:
                self.status2 = 'Player A moved first'
            else:
                self.status2 = 'Player B moved first'

            if reward[0] == -100 and self.playerA.possession:
                self.status = 'GAME OVER - A SCORED IN OWN GOAL'
            elif reward[0] == -100 and self.playerB.possession:
                self.status = 'GAME OVER - B SCORED IN A GOAL'
            elif reward[0] == 100 and self.playerA.possession:
                self.status = 'GAME OVER - A SCORED IN B GOAL'
            elif reward[0] == 100 and self.playerB.possession:
                self.status = 'GAME OVER - B SCORED IN OWN GOAL'
            else:
                pass

            #update current state tracking
            self.state = next_state



            return (next_state, reward, self.done)

        def render(self):
            
            plt.gcf().set_size_inches(10,5)
            plt.clf()
            plt.xlim([-0.5,3.5])
            plt.ylim([1.5,-0.5])
            plt.xticks([-0.5, 0.5, 1.5, 2.5, 3.5], color='white')
            plt.yticks([1.5, 0.5, -0.5], color='white')
            plt.grid()

            
            plt.fill_between(x=np.linspace(-0.5,0.5,100), y1=[1.5]*100, y2=[-0.5]*100, color='red')
            plt.fill_between(x=np.linspace(2.5,3.5,100), y1=[1.5]*100, y2=[-0.5]*100, color='blue')
            plt.fill_between(x=np.linspace(0.5,2.5,100), y1=[1.5]*100, y2=[-0.5]*100, color='green')

            #plot ball based off of possession
            if self.playerA.possession:
                plt.scatter(self.playerA.position[1], self.playerA.position[0], color='white', s=2000, edgecolors='black')
            elif self.playerB.possession:
                plt.scatter(self.playerB.position[1], self.playerB.position[0], color='white', s=2000, edgecolors='black')
            else:
                plt.text(0, 1.5, 'ERROR - NO ONE HAS BALL', fontsize=25)


            #plot player A - shift the letter a little to be centered in the box
            aa = plt.text(self.playerA.position[1]-0.03, self.playerA.position[0]+0.03, 'A', fontsize=25, color='purple', weight=200)
            aa.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'), path_effects.Normal()])

            #plot player B - shift the letter a little to be centered in the box
            bb=plt.text(self.playerB.position[1]-0.03, self.playerB.position[0]+0.03, 'B', fontsize=25, color='orange', weight=200)
            bb.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'), path_effects.Normal()])

            #plot player A's score
            a = plt.text (2.8, 1.6, 'Player A: {}'.format(self.playerAScore), fontsize=15, weight=1000, color='purple')
            a.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'), path_effects.Normal()])
            #plot player B's score
            b = plt.text(-0.5, 1.6, 'Player B: {}'.format(self.playerBScore), fontsize=15, color='orange', weight=1000)
            b.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'), path_effects.Normal()])

            #plot player A's move
            aarrow = plt.text (2.0, 1.6, self.arrows[self.moves[0]], fontsize=25, color='purple', weight=1000)
            aarrow.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'), path_effects.Normal()])

            #plot player B's move
            barrow = plt.text(1, 1.6, self.arrows[self.moves[1]], fontsize=25, color='orange', weight=1000)
            barrow.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'), path_effects.Normal()])


            if self.status != None:
                t= plt.title(self.status, fontsize=30, weight=1000, color='white')
                t.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'), path_effects.Normal()])

            if self.status2 != None:
                move = plt.text(1.0, 1.7, self.status2, fontsize=15, weight=500, color='k')
            plt.show(block=False)
            plt.pause(0.001)
            
            

            self.status = None

#####################################################################################################################

class player:
    def __init__(self):
        #storing position on the field
        self.position = None
        #attribute boolean for having possession of the ball
        self.possession = False
