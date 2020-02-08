from training_set_generator import walkGenerator
import numpy as np
import matplotlib.pyplot as plt
import argparse
from td_lambda import experiment_1
from multiprocessing import Process, Queue

parser = argparse.ArgumentParser()
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

    #generate training sets
    generated_sets = walkGenerator().generate_training_sets(num_samples=args.num_train_sets, sequences_per_sample=args.num_sequences)



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




















    # '''
    # Steps

    # 1.) Iterate through each training set of sequences in generated_sets
    # 2.) Iterate through each sequence in a training set
    # 3.) for a given sequence initialize values and eligibilty array
    # 4.) Iterate through each transition and update values based off of eligbility
    # '''
    # lamdas=[0.0, 0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    # ideal = np.array([(1.0/6.0, (1.0/3.0), (1.0/2.0), (2.0/3.0), (5.0/6.0))])

    # err = []
    # for lamda in lamdas:

    #     rmses =[]

    #     for set_ in generated_sets:
    #         values_per_seq = []
    #         global_values = np.zeros(7)

    #         next_set = False

    #         while not next_set:


    #             for sequence in set_:

    #                 values = global_values.copy()

    #                 eligibility = np.zeros(7)

    #                 walk = sequence.Route
    #                 rewards = sequence.Reward

    #                 for step in range(len(walk)-1):
    #                     state = np.argmax(walk[step])
    #                     transition = np.argmax(walk[step+1])
    #                     eligibility[state] =1
    #                     update = rewards[step] + float(args.gamma)*values[transition] - values[state]
    #                     for pos, val in enumerate(values):
    #                         values[pos] = val + float(args.alpha) * update * eligibility[pos]
    #                         eligibility[pos] = eligibility[pos] * lamda * float(args.gamma)
    #                 values_per_seq.append(values)

    #             new_values = np.mean(values_per_seq, axis=0)
    #             diff = np.abs(new_values - global_values)
    #             global_values = new_values.copy()
    #             values_per_seq = []

    #             if all(diff <= 0.001):
    #                 next_set = True

    #         rmse = np.sqrt(np.mean((global_values[1:-1]-ideal)**2))

    #         rmses.append(rmse)
    #     err.append(np.mean(rmses))


    # plt.figure(figsize=(15,8))
    # plt.plot(lamdas, err, marker ='o')
    # plt.ylabel('Error Using Best {}'.format(chr(945)))
    # plt.xlabel('λ')
    # plt.show()