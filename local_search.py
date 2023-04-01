import numpy as np
import copy

def tour_cost(state, adj_matrix):
    cost = 0
    for i in range(len(state)):
        j = (1+i) % len(state)
        if not np.isnan(adj_matrix[state[i],state[j]]):
            cost+= adj_matrix[state[i],state[j]]
        else:
            return np.nan
    return cost

def random_swap(state):
    idx1, idx2 = np.random.choice(len(state), size=2, replace=False)
    new_state = copy.deepcopy(state)
    new_state[idx1], new_state[idx2] = new_state[idx2], new_state[idx1]
    return new_state

def schedule(t):
    return t*0.99
def simulated_annealing(initial_state, adj_matrix, initial_T=1000):
    T = initial_T
    current = initial_state
    iters = 0
    while True:
        T = schedule(T)
        if T < 10e-14:
            break
        next_state = random_swap(current)
        deltaE = tour_cost(current, adj_matrix) - tour_cost(next_state, adj_matrix)
        u = np.random.uniform()
        if deltaE > 0:
            current = next_state
        elif deltaE <= 0 and u <= np.exp(deltaE / T):
            current = next_state
        
        iters += 1
    return current, iters
