
import numpy as np

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


class bet_max:
    '''
    Betting strategy that makes player always bet the table maximum

    Args:
        Player (object): Player instance that is utilizing this betting strategy so 
        it can be aware of what the table maximum is
    '''
    def __init__(self, Player):
        self.table_max = Player.table_max

    def bet(self):
        return self.table_max

    def __repr__(self):
        return 'Always bet table maximum'

class bet_uniform_random:
    def __init__(self, Player):
        self.table_max = Player.table_max
        self.table_min = Player.table_min
        

    def __repr__(self):
        return 'Bet Uniform Random'

    def bet(self):
        return np.max([self.table_min, round(np.random.uniform() * self.table_max, -1)])


class bet_triangular:
    def __init__(self, left, med, right):
        assert (0 <= left <= 1), 'left boundary for triangular distribution must be 0 <= left <= 1'
        assert(0 <= med <= 1), 'med boundary for triangular distribution must be 0 <= med <= 1'
        assert (0 <= right <= 1), 'right boundary for triangular distribution must be 0 <= med <= 1'
        assert (left < med < right), 'boundary conditions for triangular distribution must be left < med < right'

        self.left = left
        self.med = med
        self.right = right
        

    def initialize(self):
        return triangular(left=self.left, med=self.med, right=self.right)


class triangular:
    def __init__(self, left, med, right):
        self.left = left
        self.med = med
        self.right = right

    def __call__(self, Player):
        self.table_max = Player.table_max
        self.table_min = Player.table_min
        return self

    def bet(self):
        return np.max([self.table_min, round(np.random.triangular(left=self.left, mode=self.med, right=self.right) * self.table_max, -1)])

class bet_normal:
    def __init__(self, mean, std):
        assert (0 <= mean <= 1), 'mean for normal distribution must be 0 <= mean <= 1'
        assert(0 <= std <= 1), 'std boundary for normal distribution must be 0 <= std <= 1'
        

        self.mean = mean
        self.std = std
        
        

    def initialize(self):
        return normal(mean=self.mean, std=self.std)


class normal:
    def __init__(self, mean, std):
        self.mean = mean
        self.std = std
        

    def __call__(self, Player):
        self.table_max = Player.table_max
        self.table_min = Player.table_min
        return self

    def bet(self):
        return np.min([np.max([self.table_min, round(np.random.normal(loc=self.mean, scale=self.std) * self.table_max, -1)]), self.table_max])


class bet_exponential:
    def __init__(self, lam):
        assert (0 <= lam <= 1), 'lam for exponential distribution must be 0 <= lam <= 1'
        
        self.lam = lam


    def initialize(self):
        return exponential(lam=self.lam)


class exponential:
    def __init__(self, lam):
        self.lam = lam
        

    def __call__(self, Player):
        self.table_max = Player.table_max
        self.table_min = Player.table_min
        return self

    def bet(self):
        return np.min([np.max([self.table_min, round(np.random.exponential(scale=self.lam) * self.table_max, -1)]), self.table_max])


class bet_poisson:
    def __init__(self, lam):
        assert (0 <= lam <= 1), 'lam for poisson distribution must be 0 <= lam <= 1'
        
        self.lam = lam


    def initialize(self):
        return poisson(lam=self.lam)


class poisson:
    def __init__(self, lam):
        self.lam = lam
        

    def __call__(self, Player):
        self.table_max = Player.table_max
        self.table_min = Player.table_min
        return self

    def bet(self):
        return np.min([np.max([self.table_min, round(np.random.poisson(lam=self.lam) * self.table_max, -1)]), self.table_max])




if __name__ == '__main__':
    test = bet_poisson(0.5).initialize()

    class player:
        def __init__(self, min_, max_):
            self.table_min = min_
            self.table_max = max_

    p = player(100, 1000)

    test(p)

    data = [test.bet() for _ in range(10000)]
    import matplotlib.pyplot as plt

    plt.figure()
    plt.hist(data, bins=20)
    plt.show()
