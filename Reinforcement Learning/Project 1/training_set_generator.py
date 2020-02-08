import numpy as np
from collections import namedtuple


Walk = namedtuple('Walk', ['Route','Reward'])
np.random.seed =1

class walkGenerator:
    def __init__(self):
        
        #Dictionary to encode state position to a vector
        self.state_arrays = {
                'A':np.array([1,0,0,0,0,0,0], dtype='float64'),
                'B':np.array([0,1,0,0,0,0,0], dtype='float64'),
                'C':np.array([0,0,1,0,0,0,0], dtype='float64'),
                'D':np.array([0,0,0,1,0,0,0], dtype='float64'),
                'E':np.array([0,0,0,0,1,0,0], dtype='float64'),
                'F':np.array([0,0,0,0,0,1,0], dtype='float64'),
                'G':np.array([0,0,0,0,0,0,1], dtype='float64')
               }
        #Possible states
        self.states = ('A','B','C','D','E','F','G')

        #state 0 (A) has a reward of 0
        #state 6 (G) has a reward of 1
        self.rewards = {0:0, 6:1}


        #End at state A or G
        self.terminal_states = (0,6)
        
    def take_a_walk(self):
        #initialize empty array to hold the walk progression
        walk = []
        #rewards for the walk
        r = []
        #Always start at position 3 (D)
        current_state = 3
        
        while True:
            #add initial state to walk
            walk.append(self.states[current_state])

            #take a random left or right walk
            action = np.random.choice([-1,1], p=[0.5,0.5])

            #update state position
            current_state = current_state + action

            #check for terminal state
            if current_state in self.terminal_states:
                walk.append(self.states[current_state])
                r.append(self.rewards[current_state])
                break
            else:
                r.append(0)
                
        state_matrix = []

        for position in walk:
            state_matrix.append(self.state_arrays[position])

        state_matrix = np.array(state_matrix, dtype='float64')
        
        return Walk(state_matrix, r)
    
    def generate_training_sets(self, num_samples, sequences_per_sample):
        assert isinstance(num_samples, int), 'num_samples param must be integer'
        assert num_samples > 0, 'num_samples param must be greater than 0'
        assert isinstance(sequences_per_sample, int), 'sequences_per_sample param must be integer'
        assert sequences_per_sample > 0, 'sequences_per_sample param must be greater than 0'
        
        training_sets = []
        for _ in range(num_samples):
            current_set = []
            for _ in range(sequences_per_sample):
                
                walk = self.take_a_walk()
                current_set.append(walk)
                
            training_sets.append(current_set)
        return training_sets