from os import sys, path
sys.path.append(path.dirname(__file__))

from Utils import makeLogger, strategy_parser, Dapp, open_browser
logger = makeLogger(__file__)

from Game import Player, BlackJack, Player_Factory
from Strategies.PlayingStrategies import dealer_strategy_stand_on_17
import numpy as np
import yaml

from threading import Timer




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
            logger.info('\nDealers cards: {}\nMy cards: {}\nBet: {}\nChips: {}'.format(dealers_cards, players_cards[0],bets[0], table.players[0].chips))
            # print('Bet: {}\nChips: {}'.format(bets[0], table.players[0].chips))
            hands += 1

        if trial > 0:
            lo = np.sum(resets)
        else:
            lo = 0
        table.reset_game()
        resets.append(hands)
        hi = np.sum(resets)
        table.players[0].record_max(lo,hi)
        hands=0

    
    Timer(1, open_browser).start()
    info = '''
    ##################################################################
    # Starting Dashboard - To terminate application press `Ctrl + c` #
    ##################################################################
    '''
    logger.warning(info)
    Dapp(table, resets).launch_dashboard()

    