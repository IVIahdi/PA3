import numpy as np
import copy

def tour_cost(state, adj_matrix):
    cost = 0
    for i in range(len(state)):
        j = (i + 1) % len(state)
        if not np.isnan(adj_matrix[state[i], state[j]]):
            if state[i] < state[j]:
                cost += adj_matrix[state[i], state[j]]
        else:
            return np.nan
    if state[0] != state[-1]:
        return np.nan
    visited = set()
    for loc in state:
        if loc in visited:
            return np.nan
        visited.add(loc)
    return cost

def random_swap(state):
    idx1, idx2 = np.random.choice(len(state), size=2, replace=False)
    new_state = copy.deepcopy(state)
    new_state[idx1], new_state[idx2] = new_state[idx2], new_state[idx1]
    return new_state

def simulated_annealing(initial_state, adj_matrix, initial_T=1000):
    T = initial_T
    current = initial_state
    iters = 0
    while T >= 1e-14:
        T *= 0.99
        if T < 1e-14:
            break
        next_state = random_swap(current)
        deltaE = tour_cost(next_state, adj_matrix) - tour_cost(current, adj_matrix)
        if deltaE > 0:
            current = next_state
        elif np.exp(deltaE / T) > np.random.uniform():
            current = next_state
        iters += 1
    return current, iters
