import numpy as np
import copy
def tour_cost(state, adj_matrix):
    cost = 0
    for i in range(len(state)):
        if i == len(state) - 1:
            j = 0
        else:
            j = i + 1
        if np.isnan(adj_matrix[state[i], state[j]]):
            # If the edge does not exist, return infinity
            return np.nan
        cost += adj_matrix[state[i], state[j]]
    return cost

def random_swap(state):
    idx1, idx2 = np.random.choice(len(state), size=2, replace=False)
    new_state = copy.deepcopy(state)
    new_state[idx1], new_state[idx2] = new_state[idx2], new_state[idx1]
    return new_state

def simulated_annealing(initial_state, adj_matrix, initial_T=1000):
    current_state = initial_state
    T = initial_T
    iters = 0

    while T >= 1e-14:
        T *= 0.99
        if T < 1e-14:
            break

        next_state = random_swap(current_state)
        deltaE = tour_cost(current_state, adj_matrix) - tour_cost(next_state, adj_matrix)

        if deltaE > 0:
            current_state = next_state
        elif np.random.uniform() <= np.exp(deltaE/T):
            current_state = next_state

        iters += 1

    return current_state, iters
