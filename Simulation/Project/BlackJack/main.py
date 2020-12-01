from os import sys, path
sys.path.append(path.dirname(__file__))

from Utils import makeLogger, strategy_parser
logger = makeLogger(__file__)

from Game import Player, BlackJack
from Strategies.BettingStrategies import bet_min, bet_max, bet_uniform_random, bet_triangular, bet_normal
from Strategies.PlayingStrategies import always_stand, dealer_strategy_stand_on_17, stand_on_17_or_higher, dealer_plus_10, stand_on_16_or_higher, stand_on_18_or_higher, fifty_fifty
import numpy as np
import yaml
import matplotlib.pyplot as plt




with open('config.yaml') as fh:
    data = yaml.load(fh, Loader=yaml.FullLoader)


SEED = data['RANDOM_SEED']
NUM_OF_DECKS= data['NUMBER_OF_DECKS']
NUM_OF_OTHER_PLAYERS = data['NUMBER_OF_OTHERS']
SHOE_CUT = data['SHOE_CUT_PERCENTAGE']
NUM_OF_HANDS = data['NUMBER_OF_HANDS']
CHIPS = data['CHIPS']
TABLE_MIN = data['TABLE_MIN_BET']
TABLE_MAX = data['TABLE_MAX_BET']
NAME = data['PLAYER_NAME']
PLAYER_POS = data['PLAYER_POSITION']
BETTING = data['BETTING']
PLAYING_STRATEGY = data['PLAYING_STRATEGY']

betting_strategy, playing_strategy = strategy_parser(BETTING, PLAYING_STRATEGY)

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

player1 = Player(strategy=playing_strategy,
                 betting_strategy=betting_strategy,
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
    print('Dealers cards: {}\nMy cards: {}'.format(dealers_cards, players_cards[0]))
    print('Bet: {}\nChips: {}'.format(bets[0], table.players[0].chips))
    NUM_OF_HANDS-=1



plt.subplots(nrows=1, ncols=2,figsize=(15,8))
ax1 = plt.subplot(121)
ax2 = plt.subplot(122)

for pos, player in enumerate(table.players):
    colors=['rx', 'gx']
    ax1.stem(range(len(player.winnings_per_hand)), player.winnings_per_hand, label=player.name, markerfmt=colors[pos])
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