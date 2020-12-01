from os import sys, path

sys.path.append(path.dirname(path.dirname(__file__)))

from Strategies.BettingStrategies import bet_min, bet_max, bet_uniform_random, bet_triangular, bet_normal, bet_exponential, bet_poisson
from Strategies.PlayingStrategies import always_stand, dealer_strategy_stand_on_17, stand_on_17_or_higher, dealer_plus_10, stand_on_16_or_higher, stand_on_18_or_higher, fifty_fifty
import numpy as np

def strategy_parser(betting_strategy, playing_strategy):
    bet = betting_parser(betting_strategy)
    play = playing_parser(playing_strategy)

    return bet, play





def betting_parser(strategy):

    if strategy['STRATEGY'] == 'TRIANGULAR':
        assert 'LEFT' in strategy, 'LEFT parameter missing from config for betting strategy "TRAINGULAR"'
        assert 'RIGHT' in strategy, 'RIGHT parameter missing from config for betting strategy "TRAINGULAR"'
        assert 'MED' in strategy, 'MED parameter missing from config for betting strategy "TRAINGULAR"'

        left = strategy['LEFT']
        right = strategy['RIGHT']
        med = strategy['MED']

        return bet_triangular(left=left, med=med, right=right).initialize()

    elif strategy['STRATEGY'] == 'MINIMUM':
        return bet_min

    elif strategy['STRATEGY'] == 'MAXIMUM':
        return bet_max

    elif strategy['STRATEGY'] == 'UNIFORM':
        return bet_uniform_random

    elif strategy['STRATEGY'] == 'NORMAL':
        assert 'MEAN' in strategy, 'MEAN parameter missing from config for betting strategy "NORMAL"'
        assert 'STD' in strategy, 'STD parameter missing from config for betting strategy "NORMAL"'

        mean = strategy['MEAN']
        std = strategy['STD']

        return bet_normal(mean=mean, std=std).initialize()

    elif strategy['STRATEGY'] == 'EXPONENTIAL':
        assert 'LAMBDA' in strategy, 'LAMBDA parameter missing from config for betting strategy "EXPONENTIAL"'

        lam = strategy['LAMBDA']

        return bet_exponential(lam=lam).initialize()

    elif strategy['STRATEGY'] == 'RANDOM':
        
        return np.random.choice([bet_min, bet_max, bet_uniform_random, bet_normal(mean=0.5, std=0.1).initialize(), bet_exponential(lam=0.5).initialize()])

    else:
        raise "Invalid Betting Strategy detected in config"

def playing_parser(strategy):

    if strategy == '17+':
        return stand_on_17_or_higher

    elif strategy == '16+':
        return stand_on_16_or_higher

    elif strategy == '18+':
        return stand_on_18_or_higher

    elif strategy == 'STAND':
        return always_stand

    elif strategy == r'50/50':
        return fifty_fifty

    elif strategy =='D+10':
        return dealer_plus_10

    elif strategy == 'RANDOM':
        return np.random.choice([stand_on_16_or_higher, stand_on_17_or_higher, stand_on_18_or_higher, always_stand, fifty_fifty, dealer_plus_10])

    else:
        raise "Invalid Playing Strategy detected in config"




