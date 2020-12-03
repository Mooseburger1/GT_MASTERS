from os import sys, path
sys.path.append(path.dirname(__file__))

from Utils import makeLogger, strategy_parser, Dapp, open_browser
logger = makeLogger(__file__)

from Game import Player, BlackJack, Player_Factory
from Strategies.PlayingStrategies import dealer_strategy_stand_on_17
import numpy as np
import yaml

from threading import Timer



# get and parse the config yaml file
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

# convert config parameters to betting and playing strategies for the player class
betting_strategy, playing_strategy = strategy_parser(BETTING, PLAYING_STRATEGY)

# set random seed
np.random.seed(SEED)



# instantiate the dealer of the table
dealer = Player(strategy=dealer_strategy_stand_on_17,
                betting_strategy=None,
                name='Dealer',
                chips=np.inf)

# instantiate the black jack table
table = BlackJack(num_of_decks=NUM_OF_DECKS,
                  shoe_cut_perc=SHOE_CUT,
                  table_min=TABLE_MIN,
                  table_max=TABLE_MAX,
                  dealer=dealer)

# instantiate my player
MyPlayer = Player(strategy=playing_strategy,
                 betting_strategy=betting_strategy,
                 chips=CHIPS,
                 name='Scott')

# add my player to the black jack table
table.add_player(MyPlayer, my_player=True)

# if other players exist in the config file, create them and add them to the table
if OTHER_PLAYERS != 'NONE':
    factory = Player_Factory(player_info=OTHER_PLAYERS, chips=CHIPS)
    for player in factory:
        table.add_player(player, my_player=False)

# send table summary to std.out
logger.info(table.summary())
# counter for total hands played
hands = 0
# keep track at which hand number did the game reset and the next trial started
resets = []


if __name__ == '__main__':

    # for each trial
    for trial in range(NUMBER_OF_TRIALS):
        print('################### TRIAL {} ###################'.format(trial))

        #while my player isn't broke and total hands haven't been reached
        while not MyPlayer.broke and hands < NUM_OF_HANDS:
            
            #get bets from everyone at the table
            bets = table.table_bets()

            #deal everyones cards
            players_cards, dealers_cards = table.deal()

            #go around the table and get each player's decision whether to "hit" or "stand"
            for pos, player in enumerate(table.players):

                #skip player if they're broke
                if player.broke: continue

                player_cards = players_cards[pos]
                other_players_cards = [players_cards[i] for i in range(len(table.players)) if i != pos]

                decision = 'hit'

                while decision is 'hit':

                    cards = (player_cards, other_players_cards, dealers_cards)
                    #get current players decision from their strategy class
                    decision = player.decision(cards)

                    #deal card if player wants to "hit"
                    if decision is 'hit':
                        player_cards.append(table.hit())

                        #check if player has busted
                        if np.sum(player_cards) >= 21:
                            decision = 'stand'


            # dealers turn to "hit" or "stand"
            decision = 'hit'
            dealers_cards.append(table.hit())
            while decision is 'hit':
                cards = (dealers_cards, players_cards, None)
                decision = table.dealer.decision(cards)

                if decision is 'hit':
                    dealers_cards.append(table.hit())
            

            #evaluate who won and who lost and pay out winnings
            table.evaluate(cards=(players_cards, dealers_cards), bets=bets)

            #log round to std.out
            logger.info('\nDealers cards: {}\nMy cards: {}\nBet: {}\nChips: {}'.format(dealers_cards, players_cards[0],bets[0], table.players[0].chips))
            
            #increase hand counter
            hands += 1
        
        #get hand range that this trial was executed over 
        if trial > 0:
            lo = np.sum(resets)
        else:
            lo = 0
        
        #reset the game
        table.reset_game()

        #track reset hand number
        resets.append(hands)

        #get the upper bound for this previous trial
        hi = np.sum(resets)
        
        #track the highest chip total achieved this trial
        table.players[0].record_max(lo,hi)

        #reset hands played for the next trial
        hands=0

    
    # automatically open browser to the port the Dashboard will be served on
    Timer(1, open_browser).start()
    info = '''
    ##################################################################
    # Starting Dashboard - To terminate application press `Ctrl + c` #
    ##################################################################
    '''
    logger.warning(info)

    # start the dashboard server
    Dapp(table, resets).launch_dashboard()

    