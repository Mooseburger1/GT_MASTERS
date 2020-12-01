from os import sys, path
sys.path.append(path.dirname(__file__))

from Utils import makeLogger, strategy_parser
logger = makeLogger(__file__)

import numpy as np
import copy

class Player:
    '''
    This class is responsible for instantiating a player in the game of blackjack
    
    Args:
        strategy (object): A strategy class the player will use as main strategy in the game
        betting_strategy (object): A betting strategy class the player will use
        chips (int): The number of chips the player will sit down at the table with
        name (str): The unique name of the player
    
    Returns:
        None
    '''
    def __init__(self, strategy: object, betting_strategy: object, chips: float, name: str):

        self.strategy = strategy()
        self.betting_strategy = betting_strategy
        self.chips = chips
        self.broke = False if chips > 0 else True
        self.name = name
        self.winnings_per_hand = []
        self.chips_per_hand = [chips]
        
        
    def __repr__(self):
        return "{}\nChips:    ${}\nPlaying Strategy: {}\nBetting Strategy: {}".format(self.name, self.chips, self.strategy, self.betting_strategy)
    
    def _set_table_rules(self, min_, max_):
        '''
        This method informs the player of the table min and max for betting so that the 
        betting strategy can be adjusted accordingly

        Args:
            min_ (int): Table Minimum
            max_ (int): Table Maximum
        '''
        self.table_min = min_
        self.table_max = max_
        self.betting_strategy = self.betting_strategy(self)
        
    def decision(self, cards):
        '''
        Method used to inform the dealer whether the player is going to "hit" or "stand"
        with respect to the cards the player has in their hands

        Args:
            cards (list): List containing the cards dealt to the player

        Returns:
            decision (str): Player's decision to "hit" or "stand"
        '''
        return self.strategy._decision(cards)

    
    def bet(self):
        '''
        Method the player utilizes to place bets. The player bets with respect to
        the betting strategy the player was instantiated with
        '''
        if self.broke: print('{} is broke!'.format(self.name))
        if not self.broke:
            amount = self.betting_strategy.bet()

            #adjust the amount so that it isn't greater than the amount actually held by player
            amount = min(copy.deepcopy(self.chips), amount)
            
            #reduce player's chip amount according to bet size
            self.chips -= amount
            
            #if no more chips, set flag to broke
            if self.chips <= 0: self.broke = True

            return amount
        
        else:
            return -1

    def track_winnings(self, winnings: int):
        self.winnings_per_hand.append(winnings[0])
        self.chips_per_hand.append(self.chips)

    def pay(self, winnings):
        self.chips += winnings[0]



class player_name_generator:
    '''
    This class is utilized to randomly generate names for players sitting at the table that aren't the main player
    '''
    def __init__(self):
        self.names = ['Frank', 'Jeff', 'Alex', 'Steve', 'John', 'Eddie', 'Brian', 
                      'Richard', 'Nick', 'James', 'Tony','Rhonda', 'Rachel', 
                      'Emily', 'Brianna', 'Peyton', 'Alexis', 'Lisa', 'Jennifer', 'Olivia']
    def _sample_name(self):
        pos = np.random.randint(low=0, high=len(self.names))
        return self.names.pop(pos)



class Cards:
    '''
    This class is utilized to keep track, shuffle, and deal the deck of cards used at the table

    Args:
        num_of_decks (int): The number of playing 52 card decks to use in the shoe - default is 6
    '''
    def __init__(self, num_of_decks=6):
        assert isinstance(num_of_decks, int), "Number of decks specified must be of type 'int'"
        
        #number of standard 52-card playing decks in the game
        self.num_of_decks = num_of_decks
        
        #aces and number cards
        aces_and_nums = np.array([[x]*4*num_of_decks for x in range(1,11)]).ravel()
        
        #faces
        faces = np.array([10] * 4 * 3 * num_of_decks)
        
        #combine deck
        self.deck = np.concatenate((aces_and_nums, faces))

        self._shuffle_deck()
        
    def __repr__(self):
        return 'Deck of {} cards\n{} cards remaining'.format(52*self.num_of_decks, len(self.deck))
        
    def _shuffle_deck(self):
        
        np.random.shuffle(self.deck)
        np.random.shuffle(self.deck)
        
        return self
    
    def _cards_left_percentage(self):
        return len(self.deck) / (52 * self.num_of_decks)
    
    def _deal(self):
        card = self.deck[0].copy()
        self.deck = np.delete(self.deck, 0)
        return card
    
    def _reset_deck(self):
        self.__init__(self.num_of_decks)
        return self._shuffle_deck()


class BlackJack:
    """Blackjack main object. This class controls the flow of the game from taking bets, dealing cards,
       adding players to the table, and adjusting where your player sits

        Args:
            num_of_decks (int): Number of standard 52 card decks to use at the table.
            shoe_cut_perc (float): Decimal percentage of deck usage before cards are shuffled again.
            table_min (int): The minimum allowable bet at the table
            table_max (int): The maximum allowable bet at the table
            dealer (object): Player object to be utilized as the dealer
            num_of_other_players (int): Number of simulated players at the table
            
        """
    def __init__(self, num_of_decks, shoe_cut_perc, table_min,table_max, dealer):
        
        assert isinstance(num_of_decks, int), 'num_of_decks parameter must be an integer'
        assert isinstance(shoe_cut_perc, float), 'shoe_cut_perc parameter must be a float with value 0.0 <= x <=1.0'
        assert isinstance(table_min, int), 'min_bet must be an integer'
        assert isinstance(table_max, int), 'max_bet must be an integer'
        assert 0.0 <= shoe_cut_perc <= 1.0, 'shoe_cut_perc must be a float value x with 0.0 <= x <= 1.0'
        assert 1 <= num_of_decks <= 8, 'num_of_decks must be an integer between 1 and 8'
        assert table_min <= table_max, 'min_bet must be less than or equal to max_bet'
        
        #how many cards must be left in the deck before a reshuffle is executed 
        self._shoe_cut_perc = 1 - shoe_cut_perc
        
        #shoe containing all cards of N decks
        self._shoe = Cards(num_of_decks=num_of_decks)._shuffle_deck()
        
        #minmum bet
        self.table_min = table_min
        
        #max bet
        self.table_max = table_max
        
        #player stack
        self.players = []
        
        #flag for my player added
        self.in_the_game = False
        
        self.dealer = dealer
        
    def deal(self):
        
        #check for cut card
        if self._shoe._cards_left_percentage() <= self._shoe_cut_perc:
            logger.info('{}% cards left in the shoe. Reshuffling Deck'.format(int(self._shoe._cards_left_percentage() * 100)))
            self._shoe._reset_deck()
            
        cards = [[] for _ in range(len(self.players))]
        dealers_cards = []
        
        for i in range(2):
            #for each player at the table
            for pos, player in enumerate(self.players):
                if player.broke: continue
                else:cards[pos].append(self._shoe._deal())
                
        dealers_cards.append(self._shoe._deal())
                
        return cards , dealers_cards
    
    
    def table_bets(self):
        
        bets = np.empty(shape=(len(self.players), 1))
        
        #bets
        for pos, p in enumerate(self.players):
            bets[pos] = p.bet()
            
        return bets
    
    def hit(self):
        
        return self._shoe._deal()

    def add_player(self, player, my_player=False):
        '''
        method for adding players to the game
        '''
        #give the player the table betting rules
        player._set_table_rules(min_=self.table_min, max_=self.table_max)
        
        if len(self.players) < 8:
            if my_player and not self.in_the_game:
                self.players.insert(0, player)
                self.in_the_game = True
                self.my_player_pos = 0
                
            elif my_player and self.in_the_game:
                logger.info('Your player is already sitting at the table. No change applied.')
            
            elif not my_player:
                self.players.append(player)
            
            else:
                logger.critical('Fail through on add_player() method. Unknown condition encountered')
            
        else:
            logger.warn('Too many players sitting at the table. Max players allowed: 7')
            
    def _reposition_player(self, pos):
        my_player = self.players.pop(0)
        
        if pos < 0:
            self.players.append(my_player)
            self.my_player_pos = pos
            logger.info('Your player is at the last seat of the table.')
            
        else:
            self.players.insert(pos, my_player)
            self.my_player_pos = pos
            logger.info('Your player is at position {} out of 7 seats at the table'.format(pos))

    def evaluate(self, cards, bets):
        players_cards = cards[0]
        dealers_cards = cards[1]
        dealer_score = np.sum(dealers_cards)

        if dealer_score > 21:
            for pos, player in enumerate(self.players):
                if not player.broke:
                    player_score = np.sum(players_cards[pos])
                    if player_score <= 21:
                        winnings= bets[pos] * 2
                        player.pay(winnings)
                        player.track_winnings(winnings)

                    else:
                        losses = -bets[pos]
                        player.track_winnings(losses)
                        continue

        else:
            for pos, player in enumerate(self.players):
                if not player.broke:
                    player_score = np.sum(players_cards[pos])
                    
                    if player_score <= 21 and player_score > dealer_score:
                        winnings = bets[pos] * 2
                        player.pay(winnings)
                        player.track_winnings(winnings)

                    elif player_score <= 21 and player_score == dealer_score:
                        winnings = bets[pos]
                        player.pay(winnings)
                        player.track_winnings(winnings)

                    else:
                        print('Bust')
                        losses = -bets[pos]
                        player.track_winnings(losses)
                        continue

    def summary(self):
        summary = []
        for pos, p in enumerate(self.players):
            summary.append('\nSeat: {}\n------------------------\n{}\n************************************\n'.format(pos,p))

        return '\n'.join(summary)


class Player_Factory:

    def __init__(self, player_info, chips):
        self.info = player_info

        self.name_generator = player_name_generator()

        self.chips = chips

        self.players = []

        self._create_players()

    def _create_players(self):

        for player in self.info:

            data = self.info[player]

            betting = data['BETTING']
            strategy = data['PLAYING_STRATEGY']

            betting_strategy, playing_strategy = strategy_parser(betting, strategy)

            name = self.name_generator._sample_name()

            self.players.append( Player(strategy=playing_strategy, betting_strategy=betting_strategy, chips=self.chips, name=name) )

    def __iter__(self):

        n = len(self.players)
        i = 0
        while i != n:
            yield self.players[i]

            i += 1



