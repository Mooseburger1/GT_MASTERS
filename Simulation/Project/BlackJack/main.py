from os import sys, path
sys.path.append(path.dirname(__file__))

from Utils import makeLogger
logger = makeLogger(__file__)

from Game import Player, BlackJack
from Strategies.BettingStrategies import bet_min
from Strategies.PlayingStrategies import always_stand, dealer_strategy_stand_on_17
import numpy as np

SEED = 42
NUM_OF_DECKS=1 #8 is max 1 is MIN
NUM_OF_OTHER_PLAYERS=3 #6 is max
SHOE_CUT = 0.75 #1.0 is max
CHIPS = 5_000
TABLE_MIN =100
TABLE_MAX = 1_000
NAME = 'Scott'
PLAYER_POS = 1
STRATEGIES='basic'
np.random.seed(SEED)


dealer = Player(strategy=dealer_strategy_stand_on_17,
                betting_strategy=None,
                name='Dealer',
                chips=np.inf)

table = BlackJack(num_of_decks=NUM_OF_DECKS,
                  shoe_cut_perc=SHOE_CUT,
                  table_min=TABLE_MIN,
                  table_max=TABLE_MAX,
                  dealer=dealer)

player1 = Player(strategy=always_stand,
                 betting_strategy=bet_min,
                 chips=10_000,
                 name='Scott')

player2 = Player(strategy=always_stand,
                 betting_strategy=bet_min,
                 chips=10_000,
                 name='Hank')

table.add_player(player1, my_player=True)
table.add_player(player2, my_player=False)

logger.info(table.summary())

games = 100
while not player1.broke and games > 0:

    bets = table.table_bets()

    players_cards, dealers_cards = table.deal()

    for pos, player in enumerate(table.players):
        player_cards = players_cards[pos]
        other_players_cards = [player_cards[i] for i in range(len(table.players)) if i != pos]

        decision = 'hit'

        while decision is 'hit':

            cards = (player_cards, other_players_cards, dealers_cards)
            decision = player.decision(cards)

            if decision is 'hit':
                player_cards.append(table.hit())

                if np.sum(player_cards) >= 21:
                    decision = 'stand'


decision = 'hit'
dealers_cards.append(table.hit())
while decision is 'hit':
    cards = (dealers_cards, players_cards, None)
    decision = table.dealer.decision(cards)

    if decision is 'hit':
        dealers_cards.append(table.hit())