from scipy import stats
import numpy as np

# This method computes entropy for information gain
def entropy(class_y):
    # Input:            
    #   class_y         : list of class labels (0's and 1's)
    
    # TODO: Compute the entropy for a list of classes
    #
    # Example:
    #    entropy([0,0,0,1,1,1,1,1,1]) = 0.92
        
    entropy = 0
    ### Implement your code here
    #############################################
        
    unique_vals, counts = np.unique(class_y, return_counts=True)
    tot = np.sum(counts)

    probs = {x[0]:x[1]/tot for x in zip(unique_vals,counts)}

    entropy = np.sum([-(val * np.log2(val)) for val in probs.values()])
    #############################################
    return entropy


def partition_classes(X, y, split_attribute, split_val):
    # Inputs:
    #   X               : data containing all attributes
    #   y               : labels
    #   split_attribute : column index of the attribute to split on
    #   split_val       : either a numerical or categorical value to divide the split_attribute
    
    # TODO: Partition the data(X) and labels(y) based on the split value - BINARY SPLIT.
    # 
    # You will have to first check if the split attribute is numerical or categorical    
    # If the split attribute is numeric, split_val should be a numerical value
    # For example, your split_val could be the mean of the values of split_attribute
    # If the split attribute is categorical, split_val should be one of the categories.   
    #
    # You can perform the partition in the following way
    # Numeric Split Attribute:
    #   Split the data X into two lists(X_left and X_right) where the first list has all
    #   the rows where the split attribute is less than or equal to the split value, and the 
    #   second list has all the rows where the split attribute is greater than the split 
    #   value. Also create two lists(y_left and y_right) with the corresponding y labels.
    #
    # Categorical Split Attribute:
    #   Split the data X into two lists(X_left and X_right) where the first list has all 
    #   the rows where the split attribute is equal to the split value, and the second list
    #   has all the rows where the split attribute is not equal to the split value.
    #   Also create two lists(y_left and y_right) with the corresponding y labels.

    '''
    Example:
    
    X = [[3, 'aa', 10],                 y = [1,
         [1, 'bb', 22],                      1,
         [2, 'cc', 28],                      0,
         [5, 'bb', 32],                      0,
         [4, 'cc', 32]]                      1]
    
    Here, columns 0 and 2 represent numeric attributes, while column 1 is a categorical attribute.
    
    Consider the case where we call the function with split_attribute = 0 and split_val = 3 (mean of column 0)
    Then we divide X into two lists - X_left, where column 0 is <= 3  and X_right, where column 0 is > 3.
    
    X_left = [[3, 'aa', 10],                 y_left = [1,
              [1, 'bb', 22],                           1,
              [2, 'cc', 28]]                           0]
              
    X_right = [[5, 'bb', 32],                y_right = [0,
               [4, 'cc', 32]]                           1]

    Consider another case where we call the function with split_attribute = 1 and split_val = 'bb'
    Then we divide X into two lists, one where column 1 is 'bb', and the other where it is not 'bb'.
        
    X_left = [[1, 'bb', 22],                 y_left = [1,
              [5, 'bb', 32]]                           0]
              
    X_right = [[3, 'aa', 10],                y_right = [1,
               [2, 'cc', 28],                           0,
               [4, 'cc', 32]]                           1]
               
    ''' 
    
    X_left = []
    X_right = []
    
    y_left = []
    y_right = []
    ### Implement your code here
    #############################################
    
    #check if split attribute is numeric
    if isinstance(split_val, (float,int)):
        assert isinstance(X[0][split_attribute], (float,int)), 'split_val is a numerical criteria, yet a test of the data type on one of the values in the specified column is not numeric'

        #split the data on the specified column (split_attribute) by the specified criteria (split_val)
        _ = [(X_left.append(row), y_left.append(y[pos])) if row[split_attribute] <= split_val else (X_right.append(row), y_right.append(y[pos])) for pos,row in enumerate(X)]

    
    #check if split attribute is categorical
    elif isinstance(split_val, str):
        assert isinstance(X[0][split_attribute], str), 'split_val is a categorical criteria, yet a test of the data type on one of the values in the specified column is not categorical'

        #split the data on the specified column (split_attribute) by the specified criteria (split_val)
        _ = [(X_left.append(row), y_left.append(y[pos])) if row[split_attribute] == split_val else (X_right.append(row), y_right.append(y[pos])) for pos,row in enumerate(X)]

    #No clue what they did
    else:
        raise ValueError('Bad arguments for method partition_classes')
        
    
    
    #############################################
    return (X_left, X_right, y_left, y_right)

    
def information_gain(previous_y, current_y):
    # Inputs:
    #   previous_y: the distribution of original labels (0's and 1's)
    #   current_y:  the distribution of labels after splitting based on a particular
    #               split attribute and split value
    
    # TODO: Compute and return the information gain from partitioning the previous_y labels
    # into the current_y labels.
    # You will need to use the entropy function above to compute information gain
    # Reference: http://www.cs.cmu.edu/afs/cs.cmu.edu/academic/class/15381-s06/www/DTs.pdf
    
    """
    Example:
    
    previous_y = [0,0,0,1,1,1]
    current_y = [[0,0], [1,1,1,0]]
    
    info_gain = 0.45915
    """

    info_gain = 0
    ### Implement your code here
    #############################################
        
    # H = entropy of original set 
    H = entropy(previous_y)

    # HL = entropy of left split
    HL = entropy(current_y[0])

    # PL = # of obs in the left split / count(previous_y)
    PL = len(current_y[0]) / len(previous_y)

    # HR = entropy of right split
    HR = entropy(current_y[1])

    #PR = # of obs in the right split / count(previous_y)
    PR = len(current_y[1]) / len(previous_y)

    info_gain = H - (HL * PL + HR * PR)
    #############################################
    return info_gain
    
    
def best_split(X, y):
    # Inputs:
    #   X       : Data containing all attributes
    #   y       : labels
    # TODO: For each node find the best split criteria and return the 
    # split attribute, spliting value along with 
    # X_left, X_right, y_left, y_right (using partition_classes)
    '''
    
    NOTE: Just like taught in class, don't use all the features for a node.
    Repeat the steps:

    1. Select m attributes out of d available attributes
    2. Pick the best variable/split-point among the m attributes
    3. return the split attributes, split point, left and right children nodes data 

    '''
    split_attribute = 0
    split_value = 0
    X_left, X_right, y_left, y_right = [], [], [], []
    ### Implement your code here
    #############################################
    
    #infomration gain value
    ig = -np.inf

    # Num of attributes
    d = len(X[0])

    # set m attributes
    m = int(d/2)
    if m <= 0:
        m = 1

    # choice of m attributes out of d available attributes
    col_idxs = np.random.choice(a=range(d), size=m, replace=False).tolist()

    #subset the data on the randomly chosen columns
    X_subset = [[row[i] for i in col_idxs] for row in X]

    #loop through each column and find best split
    for pos, col in enumerate(col_idxs):
        #process logic for categorical col
        if isinstance(X_subset[0][pos], str):
            #get the unique categories
            categories = np.unique([row[pos] for row in X_subset])
            #loop through each category type and gauge split on it
            for cat in categories:
                #split on category
                xl, xr, yl, yr = partition_classes(X=X_subset, y=y, split_attribute=pos, split_val=cat)
                #information gain
                new_ig = information_gain(previous_y=y, current_y=[yl, yr])
                #check if ig is better
                if new_ig > ig:
                    ig = new_ig
                    split_attribute = col
                    split_value = cat
                    X_left = xl
                    X_right = xr
                    y_left = yl
                    y_right = yr

        #process logic for continuous col
        if isinstance(X_subset[0][pos], (float,int)):
            #calculate the median
            criteria_val = np.median([row[pos] for row in X_subset])
            #split on criteria val
            xl, xr, yl, yr = partition_classes(X=X_subset, y=y, split_attribute=pos, split_val=criteria_val)
            #information gain
            new_ig = information_gain(previous_y=y, current_y=[yl, yr])
            #check if ig is better
            if new_ig > ig:
                ig = new_ig
                split_attribute = col
                split_value = criteria_val
                X_left = xl
                X_right = xr
                y_left = yl
                y_right = yr

    return (X_left, X_right, y_left, y_right, split_attribute, split_value)



    #############################################
