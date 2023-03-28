import numpy as np
import copy
def tour_cost(state,adj_matrix):
    cost = 0
    N = len(state)
    for i in range(N):
        j = (i + 1) % N
        cost += adj_matrix[state[i], state[j]] if not np.isnan(adj_matrix[state[i], state[j]]) else 0
    return cost
def random_swap(state):
    idx1, idx2 = np.random.choice(len(state)-1, size=2, replace=False)
    new_state = copy.deepcopy(state)
    new_state[idx1], new_state[idx2] = new_state[idx2], new_state[idx1]
    return new_state

def simulated_annealing(initial_state, adj_matrix, initial_T=1000):
    curr = initial_state
    T = initial_T
    iters = 0
    while T > pow(10,-14):
        T *= 0.99
        if T < pow(10,-14):
            break
        next = random_swap(curr)
        deltaE = tour_cost(curr, adj_matrix) - tour_cost(next, adj_matrix)
        if deltaE > 0:
            curr = next
        else:
            u = np.random.uniform()
            if u <= np.exp(deltaE / T):
                curr = next
        iters += 1
    return curr, iters