


class bet_min:
    '''
    Betting strategy that makes player always bet the table minimum

    Args:
        Player (object): Player instance that is utilizing this betting strategy so 
        it can be aware of what the table minimum is
    '''
    def __init__(self, Player):
        self.table_min = Player.table_min

    def bet(self):
        return self.table_min

    def __repr__(self):
        return 'Always bet table minimum'