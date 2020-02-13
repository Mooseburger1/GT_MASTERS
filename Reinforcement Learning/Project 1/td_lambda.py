import numpy as np

def experiment_1(training_set, alpha, gamma, q):
    lamdas=[0.0, 0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    ideal = np.array([(1.0/6.0, (1.0/3.0), (1.0/2.0), (2.0/3.0), (5.0/6.0))], dtype='float64')


    rmses =[]
    for lamda in lamdas:

        

        
        values_per_seq = []
        global_values = np.zeros(7, dtype='float64')

        converged = False

        while not converged:


            for sequence in training_set:

                values = global_values.copy()

                eligibility = np.zeros(7, dtype='float64')

                walk = sequence.Route
                rewards = sequence.Reward

                for step in range(len(walk)-1):
                    state = np.argmax(walk[step])
                    transition = np.argmax(walk[step+1])
                    eligibility[state] +=1
                    update = rewards[step] + gamma*values[transition] - values[state]
                    for pos, val in enumerate(values):
                        values[pos] = val + alpha * update * eligibility[pos]
                        eligibility[pos] = eligibility[pos] * lamda * gamma
                values_per_seq.append(values)

            new_values = np.mean(values_per_seq, axis=0, dtype='float64')
            diff = np.abs(new_values - global_values, dtype='float64')
            global_values = new_values.copy()
            values_per_seq = []

            if all(diff <= 0.001):
                converged = True

        rmse = np.sqrt(np.mean((global_values[1:-1]-ideal)**2, dtype='float64'))

        rmses.append(rmse)
    q.put(rmses)




def experiment_2(training_set, lamda, gamma, alphas):

    ideal = np.array([(1.0/6.0, (1.0/3.0), (1.0/2.0), (2.0/3.0), (5.0/6.0))], dtype='float64')


    rmses = []
    for alpha in alphas:

        

        state_weights = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[]}
        global_values = [0,0.5,0.5,0.5,0.5,0.5,0]





        for sequence in training_set:

            values = global_values.copy()
            assert values == global_values, 'Initialization of state values is not feeding forward to the next episode'
            eligibility = np.zeros(7, dtype='float64')

            walk = sequence.Route
            rewards = sequence.Reward

            for step in range(len(walk)-1):
                state = np.argmax(walk[step])
                transition = np.argmax(walk[step+1])
                eligibility[state] +=1
                update = rewards[step] + gamma*values[transition] - values[state]
                for pos, _ in enumerate(values):
                    state_weights[pos].append( alpha * update * eligibility[pos] )
                    eligibility[pos] = eligibility[pos] * lamda * gamma

            for k in state_weights.keys():
                weights_summed = np.sum(state_weights[k])
                global_values[k] = global_values[k] + weights_summed
            
            state_weights = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[]}
            
        rmse = np.sqrt(np.mean((global_values[1:-1]-ideal)**2))
        rmses.append(rmse)


    return rmses