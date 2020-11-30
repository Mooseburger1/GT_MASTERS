from os import sys, path

sys.path.append(path.dirname(__file__))

from strategies import (always_stand, dealer_strategy_stand_on_17, stand_on_17_or_higher, dealer_plus_10, stand_on_18_or_higher, stand_on_16_or_higher, fifty_fifty)