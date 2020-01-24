import numpy as np
import mdptoolbox


no_rolls = 200
N = np.array([1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0])

#bad numbers
bad = [x[0]+1 for x in np.argwhere(N ==1)]
#good numbers
good = [x[0]+1 for x in np.argwhere(N==0)]
#probability of rolling a good number
good_ratio = (1.0/len(N))
#probability of rolling a bad number
bad_ratio = float((len(bad)/len(N)))

#Number of states to create is the largest good number times the number of rolls
max_reward = max(good) * no_rolls
#Lowest number achievable after N rolls 
min_max_reward = min(good) * no_rolls

#used to add new states while constructing the graph
next_state = 1

#empty dictionary to store graph nodes and edges
graph = {}
#empty list for reward tuples of (s, s_prime, reward, action)
rewards = []
#map a state in the graph to its value
state_to_val = {0:0}
# map a value to it's state in the graph
val_to_state = {0:0}
# keep track of states that aren't terminal
non_terminal = [0]
# kep track of states that are terminal
terminal = []


# arbitrarliy long loop to construct the graph of state addtions
for i in range(1000):
    state = i
    current_val = state_to_val[state]

    #if enough states have been created w.r.t to how many rolls, then break
    if current_val == min_max_reward:
        break
    
    #initilize empty graph state for current state i
    graph[state] = {'bad':state, 'good':[], 'terminal':state}
    
    
    #Action = Roll & It's Good
    for roll in good:
        #get the current state's value and add the roll
        tot = state_to_val[state] + roll
        
        #logic for if the current total already has a state
        if tot in val_to_state.keys():
            #add edge to graph of current state to total state
            graph[state]['good'].append(val_to_state[tot])

            #construct the reward tuple and append it
            r = (state, val_to_state[tot], roll, 'good_roll')
            rewards.append(r)

        #logic for if the current total doesn't have a state
        else:
            #next_state is now the state for current total
            state_to_val[next_state] = tot
            #current total is now next_state
            val_to_state[tot] = next_state
            #add edge to graph of current state to total state
            graph[state]['good'].append(next_state)
            #Since it's good rolls, the new state is NOT a terminal state
            non_terminal.append(next_state)
            #construct the reward tuple and append it
            r = (state, next_state, roll, 'good_roll')
            rewards.append(r)
            #increment the value for the next state to be created
            next_state += 1


#get the number for the last state added to the graph
last_state_added_to_graph = list(graph.keys())[-1]
#get the last state actually created but loop broke before it was added to the graph
last_state_created = non_terminal[-1]

#The states that were created but not added to the graph are terminal, make their edges connect to themselves (terminal meaning the tranition nowhere)
for i in range(last_state_added_to_graph+1, last_state_created+1):
    state = i
    graph[state] = {'bad':state, 'good':[state], 'terminal':state}


#Find the index position of the last non terminal state
current_graph_states = list(graph.keys())
state_values = [state_to_val[x] for x in current_graph_states]
last_index = np.squeeze(np.argwhere(state_values==min_max_reward))

#These are more terminal staes, make sure their edges navigate only back to the same state
for state in current_graph_states[last_index:]:
    graph[state] = {'bad':state, 'good':[state], 'terminal':state}

#Each non terminal state needs two moere states added - the "bad roll" state and the "quit" state
for state in current_graph_states[:last_index]:
    #Action = Bad Roll
    graph[state]['bad'] = next_state
    terminal.append(next_state)
    r = (state, next_state, -state_to_val[state], 'bad_roll')
    rewards.append(r)
    graph[next_state] = {'bad':next_state, 'good':[next_state], 'terminal':next_state}
    state_to_val[next_state] = 0
    next_state += 1
    
    #Action = Quit
    graph[state]['terminal'] = next_state
    terminal.append(next_state)
    r = (state, next_state, 0, 'quit')
    rewards.append(r)
    graph[next_state] = {'bad':next_state, 'good':[next_state], 'terminal':next_state}
    state_to_val[next_state] = 0
    next_state += 1






#construction the transition matrix (Actions, Number of states, Number of states)
states = max(graph.keys()) + 1
probs = np.zeros((2,states,states))

#Iterate through the graph and fill in the Transition matrix
for key,value in graph.items():
    state = key
    
    #quiting
    probs[0][state][value['terminal']] = 1.0
    
    
    #rolling - bad
    probs[1][state][value['bad']] = bad_ratio
    
    #rolling - good
    for node in value['good']:
        if len(value['good']) > 1:
            probs[1][state][node] = good_ratio
        elif (len(value['good']) ==1) & (value['good'][0] != value['bad']):
            probs[1][state][node] = good_ratio
        else:
            probs[1][state][node] = 1.0


#construct the rewards matrix (Actions, Number of states, Number of states)
rwds = np.zeros((2,states,states))

#iterate through the rewards list and fill in the rewards matrix
for i in rewards:
    s = i[0]
    s_prime = i[1]
    r = i[2]
    
    #quitting rewards
    if i[-1] == 'quit':
        continue
        
    else:
        rwds[1][s][s_prime] = r


#Run the MDP with gamma = 1.0
vi = mdptoolbox.mdp.ValueIteration(probs, rwds, 1.0)
vi.run()

vi.V