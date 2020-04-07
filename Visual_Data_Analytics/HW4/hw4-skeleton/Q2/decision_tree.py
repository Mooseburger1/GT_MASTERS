import numpy as np 
import ast
from util import best_split
import sys

        
        # processing for starting at the stump
class DecisionTree(object):
    def __init__(self, max_depth):
        # Initializing the tree as an empty dictionary or list, as preferred
        self.tree = None
        self.max_depth = max_depth
        self.min_size = 20
    
    def learn(self, X, y, par_node = {}, depth=0):
        # TODO: Train the decision tree (self.tree) using the the sample X and labels y
        # You will have to make use of the functions in utils.py to train the tree

        # Use the function best_split in util.py to get the best split and 
        # data corresponding to left and right child nodes
        
        # One possible way of implementing the tree:
        #    Each node in self.tree could be in the form of a dictionary:
        #       https://docs.python.org/2/library/stdtypes.html#mapping-types-dict
        #    For example, a non-leaf node with two children can have a 'left' key and  a 
        #    'right' key. You can add more keys which might help in classification
        #    (eg. split attribute and split value)
        ### Implement your code here
        #############################################
        #set the root of the tree

        
        # processing for starting at the stump
        if len(par_node) == 0:
            #find best split of the stump
            (X_left, X_right, y_left, y_right, split_attribute, split_value) = best_split(X, y)
            

            self.tree = { 'depth': 1,
                          'split_attr': split_attribute,
                          'split_value': split_value,
                          'left': (X_left, y_left),
                          'right': (X_right, y_right)
                          
                        }
            #call self.learn recursively - no need for X and y parameter since it is contained in the dictionary passed to par_node
            self.learn(X = None, y = None, par_node = self.tree, depth=depth)

        
        else:
            # left[0], right[0] = X-vals
            # left[1], right[1] = y-vals
            left, right = par_node['left'] , par_node['right']
            

            #No split
            if len(left[0]) == 0 or len(right[0]) == 0:
                par_node['left'] = par_node['right'] = self._make_terminal( par_node['left'][1] + par_node['right'][1])
                return

          
            #check max depth constraint
            if par_node['depth'] >= self.max_depth:
                par_node['left'], par_node['right'] = self._make_terminal(par_node['left'][1]) , self._make_terminal(par_node['right'][1])
                return

            
         
            
            #process left child - check if pure already
            if all(ele == left[1][0] for ele in left[1]):
                par_node['left'] = self._make_terminal(par_node['left'][1])
            
            #check if meets minimum records constraint
            elif len(left[1]) <= self.min_size:
                par_node['left'] = self._make_terminal(par_node['left'][1])

            #check if there's only 1 attribute
            elif len(left[0]) == 1:
                par_node['left'] = self._make_terminal(par_node['left'][1])
  
            #check if depth has been met
            elif par_node['depth'] >= depth:
                par_node['left'] = self._make_terminal(par_node['left'][1])
            


            # left_split[0] = X_left
            # left_split[1] = X_right
            # left_split[2] = y_left
            # left_split[3] = y_right
            # left_split[4] = split_attribute
            # left_split[5] = split_value

            else:
                left_split = best_split(*left)

                
                left_node = { 'depth': par_node['depth'] + 1,
                              'split_attr': left_split[4],
                              'split_value': left_split[5],
                              'left': (left_split[0], left_split[2]),
                              'right': (left_split[1], left_split[3]),
                            }
  
                par_node['left'] = left_node
                self.learn(X=None, y=None, par_node=par_node['left'], depth=depth)



            #prcess right child - check if pure already
            if all(ele == right[1][0] for ele in right[1]): 
                par_node['right'] = self._make_terminal(par_node['right'][1])

            #check if it meets minimum record constraint   
            elif len(right[1]) <= self.min_size:
                par_node['right'] = self._make_terminal(par_node['right'][1])

            #check if there's only 1 attribute
            elif len(right[0][0]) == 1:
                par_node['right'] = self._make_terminal(par_node['right'][1])

            #check if depth has been met
            elif par_node['depth'] >= depth:
                par_node['right'] = self._make_terminal(par_node['right'][1])



            # right_split[0] = X_left
            # right_split[1] = X_right
            # right_split[2] = y_left
            # right_split[3] = y_right
            # right_split[4] = split_attribute
            # right_split[5] = split_value

            else:
                right_split = best_split(*right)
                right_node = { 'depth': par_node['depth'] + 1,
                               'split_attr': right_split[4],
                               'split_value': right_split[5],
                               'left': (right_split[0], right_split[2]),
                               'right': (right_split[1], right_split[3]),
                            }
                
                par_node['right'] = right_node
                self.learn(X=None, y=None, par_node=par_node['right'], depth=depth)
            
        #############################################
    def _make_terminal(self, y):
        return max(set(y), key=y.count)
    

    def classify(self, record, par_node=None):
        # TODO: classify the record using self.tree and return the predicted label
        ### Implement your code here
        #############################################
        if par_node is None:
            par_node = self.tree
    
        if record[par_node['split_attr']] <= par_node['split_value']:
            if isinstance(par_node['left'], dict):
                return self.classify(record, par_node['left'])
            else:
                return par_node['left']
        else:
            if isinstance(par_node['right'], dict):
                return self.classify(record, par_node['right'])
            else:
                return par_node['right']
        #############################################



if __name__ == '__main__':

    X = [[2.771244718,1.784783929,1, 2],
        [1.728571309,1.169761413, 1, 3],
        [3.678319846,2.81281357, 1, 2],
        [3.961043357,2.61995032, 1, 3],
        [2.999208922,2.209014212, 1, 3],
        [7.497545867,3.162953546, 5, 5],
        [9.00220326,3.339047188, 8, 7],
        [7.444542326,0.476683375, 10, 6],
        [10.12493903,3.234550982, 4, 9],
        [6.642287351,3.319983761, 9, 10]]

    y = [0,0,0,0,0,1,1,1,1,1]

    tree = DecisionTree(max_depth=3)

    tree.learn(X, y)

    print(tree.tree)
    print(X[0], y[0])
    print(tree.classify(X[0]))