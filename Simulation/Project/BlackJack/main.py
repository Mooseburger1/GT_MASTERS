from os import sys, path
sys.path.append(path.dirname(__file__))

from Utils import makeLogger, strategy_parser
logger = makeLogger(__file__)

from Game import Player, BlackJack, Player_Factory
from Strategies.PlayingStrategies import dealer_strategy_stand_on_17
import numpy as np
import yaml
import matplotlib.pyplot as plt




with open('config.yaml') as fh:
    data = yaml.load(fh, Loader=yaml.FullLoader)


SEED = data['RANDOM_SEED']
NUM_OF_DECKS= data['NUMBER_OF_DECKS']
OTHER_PLAYERS = data['OTHER_PLAYERS']
SHOE_CUT = data['SHOE_CUT_PERCENTAGE']
NUM_OF_HANDS = data['NUMBER_OF_HANDS']
CHIPS = data['CHIPS']
TABLE_MIN = data['TABLE_MIN_BET']
TABLE_MAX = data['TABLE_MAX_BET']
NAME = data['PLAYER_NAME']
PLAYER_POS = data['PLAYER_POSITION']
BETTING = data['BETTING']
PLAYING_STRATEGY = data['PLAYING_STRATEGY']
NUMBER_OF_TRIALS = data['NUMBER_OF_TRIALS']

betting_strategy, playing_strategy = strategy_parser(BETTING, PLAYING_STRATEGY)

np.random.seed(SEED)

if OTHER_PLAYERS is not None:
    factory = Player_Factory(player_info=OTHER_PLAYERS, chips=CHIPS)


dealer = Player(strategy=dealer_strategy_stand_on_17,
                betting_strategy=None,
                name='Dealer',
                chips=np.inf)

table = BlackJack(num_of_decks=NUM_OF_DECKS,
                  shoe_cut_perc=SHOE_CUT,
                  table_min=TABLE_MIN,
                  table_max=TABLE_MAX,
                  dealer=dealer)

MyPlayer = Player(strategy=playing_strategy,
                 betting_strategy=betting_strategy,
                 chips=CHIPS,
                 name='Scott')


table.add_player(MyPlayer, my_player=True)

for player in factory:
    table.add_player(player, my_player=False)

logger.info(table.summary())
hands = 0
resets = []
if __name__ == '__main__':

    for trial in range(NUMBER_OF_TRIALS):
        print('################### TRIAL {} ###################'.format(trial))
        while not MyPlayer.broke and hands < NUM_OF_HANDS:

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
            hands += 1

        table.reset_game()
        resets.append(hands)
        hands=0



    plt.subplots(nrows=2, ncols=2,figsize=(15,8))
    ax1 = plt.subplot(221)
    ax2 = plt.subplot(222)
    ax3 = plt.subplot(223)
    ax4 = plt.subplot(224)

    player = table.players[0]
    ax1.bar(range(len(player.winnings_per_hand)), player.winnings_per_hand, label=player.name, color=['green' if x > 0 else 'red' for x in player.winnings_per_hand])
    ax1.set_xlabel('Hand Number')
    ax1.set_ylabel('Winnings/Losses')
    ax1.set_title('Winnings per Hand')

    for pos, player in enumerate(table.players):
        ax2.plot(range(len(player.chips_per_hand)), player.chips_per_hand, marker='*', label=player.name)
        ax2.legend()
        ax2.set_xlabel('Hand Number')
        ax2.set_ylabel('Chips Total')
        ax2.set_title('Chip Total per Hand')

    for pos, hand in enumerate(resets):
        if pos != 0:
            hand = hand + np.sum( resets[:pos] )


        ax2.plot([hand]*(CHIPS*2), range(CHIPS*2), color='k', ls='--')
        

    ax3.hist(table.players[0].totals_per_hand, color='k')
    ax4.bar(['wins', 'losses'], [table.players[0].wins, table.players[0].losses], color=['black','red'])
    plt.show()

    print(resets)
