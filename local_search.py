import numpy as np
import copy

def tour_cost(state, adj_matrix):
    cost = 0
    for i in range(len(state)-1):
        j = (1+i)
        # If there is a valid distance between the two cities, add it to the cost
        if not np.isnan(adj_matrix[state[i],state[j]]):
            cost += adj_matrix[state[i],state[j]]
        # If there is no valid distance, return NaN (not a number)
        else:
            return np.nan
    # Return the total cost of the tour
    return cost

def random_swap(state):
    # Choose two distinct indices at random
    idx1, idx2 = np.random.choice(len(state), size=2, replace=False)

    # Create a copy of the state and swap the cities at the chosen indices
    new_state = copy.deepcopy(state)
    new_state[idx1], new_state[idx2] = new_state[idx2], new_state[idx1]

    # Return the new state
    return new_state

def simulated_annealing(initial_state, adj_matrix, initial_T=1000):
    # Initialize the current state, temperature, and iteration count
    current = initial_state
    T = initial_T
    iters = 0

    # Loop until the temperature falls below a very small value
    while T > 1e-14:
        # Decrease the temperature according to a cooling schedule
        T *= 0.99
        if T < 1e-14:
            return current, iters

        # Generate a new state by randomly swapping two cities
        next_state = random_swap(current)

        # Calculate the difference in tour cost between the current and new states
        deltaE = tour_cost(current, adj_matrix) - tour_cost(next_state, adj_matrix)

        # If the new state is better, accept it
        if deltaE > 0:
            current = next_state
        # If the new state is worse, accept it with a certain probability
        elif deltaE <= 0:
            p_accept = np.exp(deltaE / T)
            if np.random.uniform() <= p_accept:
                current = next_state

        # Increment the iteration count
        iters += 1

    # Return the final state and iteration count
    return current, iters