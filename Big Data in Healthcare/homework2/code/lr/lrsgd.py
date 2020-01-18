# Do not use anything outside of the standard distribution of python
# when implementing this class

#Note: eta is learning rate
#Note: mu is regularization parameter
import math 
#import matplotlib.pyplot as plt

class LogisticRegressionSGD:
    """
    Logistic regression with stochastic gradient descent
    """

    def __init__(self, eta, mu, n_feature):
        """
        Initialization of model parameters
        """
        self.eta = eta
        self.weight = [0.0] * n_feature
        self.b = 0
        self.count = 0
        self.costs = []
        self.mu = mu

        
    def fit(self, X, y):
        """
        Update model using a pair of training sample
        """
        self.cost = self.optimize(X,y)
        
        
        # self.count+=1
        # if self.count % 100 == 0:
        #     print('Cost at Observation {}: {}'.format(self.count, self.cost))
        # #     self.costs.append(cost)
        # # if self.count == 2971:
        # #     self.costs.append(cost)
        # #     self.plotit(self.costs)

    def predict(self, X):
        """
        Predict 0 or 1 given X and the current weights in the model
        """
        return 1 if self.predict_prob(X) > 0.5 else 0

    def predict_prob(self, X):
        """
        Sigmoid function
        """
        return 1.0 / (1.0 + math.exp(-math.fsum((self.weight[f]*v for f, v in X))+self.b))

    
    def propagate(self, w, b, X, Y):
        #X is in the form [(position, value), (position, value), ...]
        #forwardprop
        z = math.fsum([x[1]*w[x[0]] for x in X]) + b
        A = 1.0 / (1.0 + math.exp(-z))
        cost = -(Y*math.log(A) + (1-Y)*math.log(1-A)) + ((self.mu) * math.fsum([v**2 for v in w]))
        
        #backprop
        dz = A - Y
        dw = [(x[0],x[1]*dz + (self.mu*2*w[x[0]])) for x in X]
        db = dz
        
        grads = {"dw":dw, "db":db}
        
        return grads, cost
    
    def optimize(self,X, Y):
        
        grads, cost = self.propagate(self.weight, self.b, X, Y)
        
        dw = grads["dw"]
        db = grads["db"]
        
        
        for idx, value in dw:
            self.weight[idx] = self.weight[idx] - (self.eta * value)
            
        self.b = self.b - (self.eta*db)
        
        
        return cost    

    # def plotit(self,cost):
    #     idx = len(cost) * 100
    #     idx = range(0,idx,100)
    #     plt.figure(figsize=(15,8))
    #     plt.plot(idx, cost, marker='*', ls='--', label='Cost')
    #     plt.xlabel('Epoch')
    #     plt.ylabel('Cost')
    #     plt.title('Cost per Epoch - Learning Rate: {}, Regularization: {}'.format(self.eta, self.mu))
    #     plt.show()