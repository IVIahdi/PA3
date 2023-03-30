import numpy as np
import copy
def tour_cost(state, adj_matrix):
    cost = 0
    for i in range(len(state)-1):
        if np.isnan(adj_matrix[state[i], state[i+1]]): # non-existent edge
            return np.nan
        cost += adj_matrix[state[i], state[i+1]]
        if np.isnan(adj_matrix[state[-1], state[0]]): # non-existent edge
            return np.nan
        cost += adj_matrix[state[-1], state[0]]

    return cost
def random_swap(state):
    idx1, idx2 = np.random.choice(len(state), size=2, replace=False)
    new_state = copy.deepcopy(state)
    new_state[idx1], new_state[idx2] = new_state[idx2], new_state[idx1]
    return new_state

def simulated_annealing(initial_state, adj_matrix, initial_T=1000):
    T = initial_T
    curr = initial_state
    iters = 0
    scheduler = lambda x: x * 0.99
    while T > pow(10,-14):
        T = scheduler(T)
        if T < 1e-14:
            break
        random_successor = random_swap(curr)
        deltaE = tour_cost(curr, adj_matrix) - tour_cost(random_successor, adj_matrix)
        if deltaE > 0:
            curr = random_successor
        elif deltaE <= 0:
            u = np.random.uniform()
            if u <= np.exp(deltaE / T):
                curr = random_successor
        iters += 1
    return curr, iters
