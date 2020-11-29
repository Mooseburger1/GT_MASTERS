
import numpy as np

class bet_min:
    '''
    Betting strategy that makes player always bet the table minimum

    Args:
        Player (object): Player instance that is utilizing this betting strategy so 
        it can be aware of what the table minimum is
    '''
    def __init__(self, Player):
        self.table_min = Player.table_min

    def bet(self):
        return self.table_min

    def __repr__(self):
        return 'Always bet table minimum'


class bet_max:
    '''
    Betting strategy that makes player always bet the table maximum

    Args:
        Player (object): Player instance that is utilizing this betting strategy so 
        it can be aware of what the table maximum is
    '''
    def __init__(self, Player):
        self.table_max = Player.table_max

    def bet(self):
        return self.table_max

    def __repr__(self):
        return 'Always bet table maximum'

class bet_uniform_random:
    def __init__(self, Player):
        self.table_max = Player.table_max
        self.table_min = Player.table_min
        

    def __repr__(self):
        return 'Bet Uniform Random'

    def bet(self):
        return np.max([self.table_min, round(np.random.uniform() * self.table_max, -1)])