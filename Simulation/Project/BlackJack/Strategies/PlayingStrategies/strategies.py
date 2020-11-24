
import numpy as np

class always_stand:
    '''
    This strategy results in a player always standing for each hand. It has a dummy
    input for its _decision method that is not used
    '''
    def _decision(self, not_used):
        '''
        Args:
            not_used (None): Dummy input that is not used

        Returns:
            decision (str): stand
        '''
        return 'stand'
    
    def __repr__(self):
        return 'Always Stand'


class dealer_strategy_stand_on_17:
    '''
    This class acts as the strategy for the dealer during blackjack. It is normal
    convention that the dealer must stand when the cards total 17 or higher. It utilizes
    the staticmethod from strategy class stand_on_17_or_higher as the decision engine
    '''
    def _decision(self, cards):
        '''
        Args:
            cards (tuple): Tuple containing all cards of the players at the table. Index 0
            is the dealers cards, index 1 is a list of list of all the players cards

        Returns:
            decision (str): Dealer's decision to hit or stand
        '''
        dealers_cards = cards[0]
        other_players_cards = cards[1]
        
        #check if all players have busted
        totals = np.array([np.sum(x) for x in other_players_cards])
        not_busted = totals[totals < 22]
        if not_busted.size == 0: return 'stand'
        
        
        #follow 'stand on 17 or higher' strategy
        return stand_on_17_or_higher._decision(cards=dealers_cards)
        
        
    def __repr__(self):
        return 'Stand on 17 (Dealer)'



class stand_on_17_or_higher:
    '''
    Strategy class that advises player to stand for any total >= 17.
    If player's cards total <17, it will advise the player to "hit"
    '''
    
    @staticmethod
    def _decision(cards):
        '''
        Static method that advises player to stand for any total >= 17.
        If player's cards total <17, it will advise the player to "hit"
        '''
        total = np.sum(cards)
        
        if total >= 17: return 'stand'
        else: return 'hit'
        
    def __repr__(self):
        return 'Stand on 17 and higher'