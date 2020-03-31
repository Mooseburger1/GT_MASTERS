import numpy as np
from collections import OrderedDict
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

np.random.seed(2)


class SoccerField:
        def __init__(self, size = (2,4)):

            self.size = size
            self.field = np.zeros(self.size)
            self._build_environment()
            self.reset_environment()
            self.done = False
            self.status = None
            

        def _build_environment(self):
            self.states = {}
            self.rewards = []
            self.actions = OrderedDict()
            counter = 0
            grid = np.zeros(self.size)

            list_of_actions = [(-1,0), (1,0), (0,1), (0,-1), (0,0)]
            #Im possesion 1
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
                                    if ((i,j) in [(0,0), (1,0)] and possession == 0) | ((row,column) in [(0,0), (1,0)] and possession == 1):
                                        reward = [100, -100]
                                        self.rewards.append(reward)
                                    #check if right side goal and opp has possession - reward should be [100, -100] - I gain 100 he loses 100 for scoring in his own goal
                                    #or
                                    #check if right side goal and I have possession - reward should be [100, -100] - I gain 100 he loses 100 for me scoring in his goal
                                    elif ((i,j) in [(0,3), (1,3)] and possession == 0) or ((row,column) in [(0,3), (1,3)] and possession==1):
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

##################################################################################################

        def random_action(self):
            idx  = np.random.randint(low=0, high=len(self.actions))
            return list(self.actions.keys())[idx]

##################################################################################################

        def _check_posession(self, state):
            if state[0] == 0:
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
                return 0
            elif self.playerA.possession:
                return 1

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

            self.state = (0, (0,2), (0,1))
            #initialize player A's position on the right side of the field
            self.playerA.position = self.state[1]

            #initialize player B's position on the left side of the field
            self.playerB.position = self.state[2]

            #Give player B the ball first
            self._check_posession(self.state) 

            #reset done flag
            self.done = False

            #reset scores
            self.playerAScore = 0
            self.playerBScore = 0

##################################################################################################

        def advance(self, actions):
            #actions = (my_move, their_move)
            
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

            #if I have ball and move first - I keep ball and move - you stay
            if my_next_position == their_next_position and self.playerA.possession and coin_flip:
                their_next_position = their_current_position

            #if I don't have ball and move first - I get ball and move - you stay and lose ball
            elif my_next_position == their_next_position and self.playerB.possession and coin_flip:
                their_next_position = their_current_position
                self._swap_possession()

            #if you have ball and move first - you keep ball and move - I stay
            elif my_next_position == their_next_position and self.playerB.possession and not coin_flip:
                my_next_position = my_current_position

            #if you don't have ball and move first - You get ball and move - I stay and lose ball
            elif my_next_position == their_next_position and self.playerA.possession and not coin_flip:
                my_next_position = my_current_position
                self._swap_possession()

            #if all these fail - then it is safe to perform move step
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
            self.state = next_state



            return (next_state, reward, self.done)

################################################################################################################################

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
            a = plt.text (-0.5, 1.6, 'Player A: {}'.format(self.playerAScore), fontsize=15, weight=1000, color='purple')
            a.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'), path_effects.Normal()])
            #plot player B's score
            b = plt.text(2.8, 1.6, 'Player B: {}'.format(self.playerBScore), fontsize=15, color='orange', weight=1000)
            b.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'), path_effects.Normal()])


            if self.status != None:
                t= plt.title(self.status, fontsize=30, weight=1000, color='white')
                t.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'), path_effects.Normal()])
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



















































# #randomly choose who goes first
#             choice = np.random.choice([0,1])
            
#             #Choice 0 means A goes first
#             if choice == 0:
#                 cardinal, direction = self.playerA.choose_action()
#                 move_check = self._validate_move(direction=direction, player='A')
#                 self.update_board(move_check, 'A')

#                 cardinal, direction = self.playerB.choose_action()
#                 move_check = self._validate_move(direction=direction, player='B')
#                 self.update_board(move_check, 'B')

#             else:
#                 cardinal, direction = self.playerB.choose_action()
#                 move_check = self._validate_move(direction=direction, player='B')
#                 self.update_board(move_check, 'B')

#                 cardinal, direction = self.playerA.choose_action()
#                 move_check = self._validate_move(direction=direction, player='A')
#                 self.update_board(move_check, 'A')

#             return self.done

#         def _update_score(self, player):
#             if player == 'A':
#                 self.playerAScore = self.playerAScore + self.playerAReward
#             else:
#                 self.playerBScore = self.playerBScore + self.playerBReward


#         def update_board(self, move_check, player):
            

#             booleans = [v for k,v in move_check.items() if k != 'next_pos']


#             #if all checks are false, it is safe to update the player
#             if not any(booleans) and player=='A':
#                 self.playerA.position = move_check['next_pos']
#                 self.playerAReward = 0
#                 self._update_score(player='A')
#                 return
#             elif not any(booleans) and player=='B':
#                 self.playerB.position = move_check['next_pos']
#                 self.playerBReward = 0
#                 self._update_score(player='B')
#                 return
#             else:
#                 pass

#             #check if the player went out of bounds
#             if player=='A' and move_check['out_of_bounds']:
#                 self.playerAReward = 0
#                 self._update_score(player='A')
#                 #do nothing
#                 return
#             elif player=='B' and move_check['out_of_bounds']:
#                 self.playerBReward = 0
#                 self._update_score(player='B')
#                 #do nothing
#                 return
#             else:
#                 pass

#             #check if own goal with the ball
#             if player=='A' and move_check['own_goal']:
#                 print('Player A Went Into His Goal!!!')
#                 if self.playerA.possession:
#                     self.playerA.position = move_check['next_pos']
#                     self.playerAReward = -100
#                     self._update_score(player='A')
#                     self.done = True
#                     return
#                 #if he doesn't have the ball - it's ok to move and games not over
#                 else:
#                     self.playerA.position = move_check['next_pos']
#                     self.playerAReward = 0
#                     self._update_score(player='A')
#                     return

#             elif player=='B' and move_check['own_goal']:
#                 print('Player B Went Into His Goal!!!')
#                 if self.playerB.possession:
#                     self.playerB.position = move_check['next_pos']
#                     self.playerBReward = -100
#                     self._update_score(player='B')
#                     self.done = True
#                     return
#                 else:
#                     self.playerB.position = move_check['next_pos']
#                     self.playerBReward = 0
#                     self._update_score(player='B')
#                     return

#             else: 
#                 pass


#             #check if opp goal with the ball
#             if player=='A' and move_check['opp_goal']:
#                 if self.playerA.possession:
#                     print('Player A Scored!!!!!')
#                     self.playerA.position = move_check['next_pos']
#                     self.playerAReward = 100
#                     self._update_score(player='A')
#                     self.done = True
#                     return
#                 #if he doesn't have the ball - it's ok to move and games not over
#                 else:
#                     self.playerAReward = 0
#                     self._update_score(player='A')
#                     self.playerA.position = move_check['next_pos']
#                     return

#             elif player=='B' and move_check['opp_goal']:
#                 if self.playerB.possession:
#                     print('Player B Scored')
#                     self.playerB.position = move_check['next_pos']
#                     self.playerBReward = 100
#                     self._update_score(player='B')
#                     self.done = True
#                     return
#                 else:
#                     self.playerB.position = move_check['next_pos']
#                     self.playerBReward = 0
#                     self._update_score(player='B')
#                     return

#             else: 
#                 pass

#             #check if moving into opponent's grid with ball
#             if player == 'A' and move_check['occupied']:
#                 if self.playerA.possession:
#                     self.playerB.possession = True
#                     self.playerA.possession = False
#                     self.playerAReward = -10
#                     self._update_score(player='A')
#                     return
#                 else:
#                     #do nothing
#                     return
#             elif player == 'B' and move_check['occupied']:
#                 if self.playerB.possession:
#                     self.playerA.possession = True
#                     self.playerB.possession = False
#                     self.playerBReward = -10
#                     self._update_score(player='B')
#                     return
#                 else:
#                     #do nothing
#                     return





#         def _validate_move(self, direction, player):

#             occupied = False
#             out_of_bounds = False
#             own_goal = False
#             opp_goal = False
            

#             A_goal = [(0,0), (1,0)]
#             B_goal = [(0,3), (1,3)]

#             if player == 'A':
                
#                 curr_pos = self.playerA.position
#                 print('PlayerAs current location: ', curr_pos)
#                 check_pos = self.playerB.position
#                 print('PlayerBs current location: ', check_pos)
#             else:
                
#                 curr_pos = self.playerB.position
#                 print('PlayerBs current location: ', curr_pos)
#                 check_pos = self.playerA.position
#                 print('PlayerAs current location: ', check_pos)

            
#             next_pos = (curr_pos[0] + direction[0] , curr_pos[1] + direction[1])

#             #check if the players move puts him in the opponents space
#             if next_pos == check_pos:
#                 print('Next move puts player {} in opponents space'.format(player))
#                 occupied = True

#             #check if the players move puts him outside the grid
#             if next_pos[0] > self.size[0]-1 or next_pos[0] < 0 \
#                 or next_pos[1] > self.size[1]-1 or next_pos[1] < 0:
#                 print('Next move puts player {} outside of the field'.format(player))
#                 out_of_bounds = True
            
#             #check if the players move puts him in a goal
#             if next_pos in A_goal and player == 'A':
#                 print('Next move puts player A in own goal')
#                 own_goal = True

#             elif next_pos in B_goal and player == 'A':
#                 print('Next move puts player A in opponents goal')
#                 opp_goal = True

#             elif next_pos in A_goal and player == 'B':
#                 print('Next move puts player B in opponents goal')
#                 opp_goal = True
            
#             elif next_pos in B_goal and player == 'B':
#                 print('Next move puts player B in own goal')
#                 own_goal = True
            
#             else:
#                 pass#raise ValueError('BAD LOGIC IN GOAL CHECKING')
            
#             move_check = {'occupied':occupied,
#                     'out_of_bounds':out_of_bounds,
#                     'own_goal':own_goal,
#                     'opp_goal':opp_goal,
#                     'next_pos':next_pos}

#             print('Player {} move check: '.format(player), move_check)
#             return move_check
   




