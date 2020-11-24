from os import sys, path

sys.path.append(path.dirname(__file__))

from strategies import (always_stand, dealer_strategy_stand_on_17, stand_on_17_or_higher)