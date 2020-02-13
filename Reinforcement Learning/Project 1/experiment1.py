from training_set_generator import walkGenerator
import numpy as np
import matplotlib.pyplot as plt
import argparse
from td_lambda import experiment_1
from multiprocessing import Process, Queue
import pickle

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--load_training_set', dest='load', help='Load the saved training set if true, generate new training set if false', default='true')
parser.add_argument('-t', '--training_sets', dest='num_train_sets', help="Number of training sets to be generated", default=100)
parser.add_argument('-s', '--sequences', dest='num_sequences', help='Number of sequences per training set', default=10)
parser.add_argument('-a', '--alpha', dest='alpha', help='Learning rate Alpha', default=0.2)
parser.add_argument('-v', '--initial_values', dest='values', help='Initial values of states', default=0.0)
parser.add_argument('-g', '--gamma', dest='gamma', help='Gamma value', default=1.0)
args = parser.parse_args()

if __name__ == '__main__':

    '''generated sets is a list of lists of arrays where each list of arrays
    is a single training set of desired number of sequences (default 10)
    each sequnce is a randomly generated walk in the form of a namedtuple

    Walk(Route=numpy.array, Reward=list)

    The Route array is a numpy array of size 
    M x 7 - M variable based on how many steps it took to complete the walk
            7 columns for each possible position in the walk

    The Reward list is the reward for each transition taken in the walk
    '''
    assert args.load in ['true', 'false'], 'Argument -l or --load_training_set can only be [true, false]'


    if args.load == 'true':
        print('loading training data from training_set.pickle')
        with open('training_set.pickle', 'rb') as file:
            generated_sets = pickle.load(file)
    else:
        #generate training sets
        print('Generating Random Walk Training Sets')
        generated_sets = walkGenerator().generate_training_sets(num_samples=args.num_train_sets, sequences_per_sample=args.num_sequences)
        print('Saving New Generated Data Set to "training_set.pickle"')
        with open('training_set.pickle', 'wb') as file:
            pickle.dump(generated_sets, file)



    #create a global queue to be shared across the processes
    q = Queue()
    #list to store the processes
    processes = []
    #list to store the rmses from all the processes
    rmses = []

    #iterate through each training set and assign it to its own process
    for i in range(len(generated_sets)):
        print('Creating Process #',i)
        p = Process(target=experiment_1, args=(generated_sets[i], float(args.alpha), float(args.gamma), q))
        p.start()
        processes.append(p)
    #get results from each training set  
    print('\n\n ---------------------------------------------\n\n')  
    for pos, p in enumerate(processes):
        print('Getting RMSE From Process', pos)
        p.join()
        rmses.append(q.get())

    print('Averaging RMSEs')
    rmses = np.mean(rmses, axis=0)

    #plot the rmses
    lamdas=[0.0, 0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    plt.figure(figsize=(15,8))
    plt.plot(lamdas, rmses, marker ='o')
    plt.ylabel('Error Using Best {}'.format(chr(945)))
    plt.xlabel('λ')
    plt.show()