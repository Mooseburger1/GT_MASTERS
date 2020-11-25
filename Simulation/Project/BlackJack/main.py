from os import sys, path
sys.path.append(path.dirname(__file__))

from Utils import makeLogger
logger = makeLogger(__file__)

from Game import Player, BlackJack
from Strategies.BettingStrategies import bet_min
from Strategies.PlayingStrategies import always_stand, dealer_strategy_stand_on_17, stand_on_17_or_higher
import numpy as np
import matplotlib.pyplot as plt

SEED = 42
NUM_OF_DECKS=8 #8 is max 1 is MIN
NUM_OF_OTHER_PLAYERS=3 #6 is max
SHOE_CUT = 0.75 #1.0 is max
NUM_OF_HANDS = 1000
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

player1 = Player(strategy=stand_on_17_or_higher,
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

while not player1.broke and NUM_OF_HANDS > 0:
    print('Hand No: {}'.format(NUM_OF_HANDS))
    bets = table.table_bets()

    players_cards, dealers_cards = table.deal()

    for pos, player in enumerate(table.players):
        if player.broke: continue
        player_cards = players_cards[pos]
        other_players_cards = [players_cards[i] for i in range(len(table.players)) if i != pos]

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


    table.evaluate(cards=(players_cards, dealers_cards), bets=bets)

    NUM_OF_HANDS-=1

plt.subplots(nrows=1, ncols=2,figsize=(15,8))
ax1 = plt.subplot(121)
ax2 = plt.subplot(122)

for player in table.players:
    ax1.plot(range(len(player.winnings_per_hand)), player.winnings_per_hand, marker='*', label=player.name)
    ax1.legend()
    ax1.set_xlabel('Hand Number')
    ax1.set_ylabel('Winnings/Losses')
    ax1.set_title('Winnings per Hand')

    ax2.plot(range(len(player.chips_per_hand)), player.chips_per_hand, marker='*', label=player.name)
    ax2.legend()
    ax2.set_xlabel('Hand Number')
    ax2.set_ylabel('Chips Total')
    ax2.set_title('Chip Total per Hand')
plt.show()