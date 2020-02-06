import numpy as np

def td_lambda(training_set, alpha, gamma, q):
    lamdas=[0.0, 0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    ideal = np.array([(1.0/6.0, (1.0/3.0), (1.0/2.0), (2.0/3.0), (5.0/6.0))])


    rmses =[]
    for lamda in lamdas:

        

        
        values_per_seq = []
        global_values = np.zeros(7)

        converged = False

        while not converged:


            for sequence in training_set:

                values = global_values.copy()

                eligibility = np.zeros(7)

                walk = sequence.Route
                rewards = sequence.Reward

                for step in range(len(walk)-1):
                    state = np.argmax(walk[step])
                    transition = np.argmax(walk[step+1])
                    eligibility[state] =1
                    update = rewards[step] + gamma*values[transition] - values[state]
                    for pos, val in enumerate(values):
                        values[pos] = val + alpha * update * eligibility[pos]
                        eligibility[pos] = eligibility[pos] * lamda * gamma
                values_per_seq.append(values)

            new_values = np.mean(values_per_seq, axis=0)
            diff = np.abs(new_values - global_values)
            global_values = new_values.copy()
            values_per_seq = []

            if all(diff <= 0.001):
                converged = True

        rmse = np.sqrt(np.mean((global_values[1:-1]-ideal)**2))

        rmses.append(rmse)
    q.put(rmses)