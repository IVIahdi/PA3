import copy
import matplotlib.pyplot as plt
import seaborn as sns
# Function to perform the AC-3 algorithm on a CSP
def ac3(csp, arcs_queue=None, current_domains=None, assignment=None):
    # Function to revise the domain of a variable based on its constraints with another variable
    def revise(csp, var1, var2, current_domains):
        revised = False
        # Iterate over a copy of the domain set to avoid modifying it during iteration
        for val1 in list(current_domains[var1]):
            has_valid_neighbor = False
            for val2 in current_domains[var2]:
                if csp.constraint_consistent(var1, val1, var2, val2):
                    has_valid_neighbor = True
                    break
            if not has_valid_neighbor:
                current_domains[var1].remove(val1)
                revised = True
        return revised

    # Initialize the queue of arcs to be processed
    arcs_queue = {(var1, var2) for var1 in csp.variables for var2 in csp.adjacency[var1]} if arcs_queue is None else set(arcs_queue)

    # Make a copy of the initial domains if none is provided
    current_domains = copy.deepcopy(csp.domains) if current_domains is None else current_domains

    # Loop until the queue is empty
    while arcs_queue:
        # Pop an arc from the queue
        (var1, var2) = arcs_queue.pop()

        # Revise the domain of var1 based on its constraints with var2
        if revise(csp, var1, var2, current_domains):
            # If var1's domain is empty, the CSP is inconsistent
            if not current_domains[var1]:
                return False, current_domains

            # Add all arcs (var3, var1) to the queue, where var3 is a neighbor of var1
            for neighbor in csp.adjacency[var1]:
                if neighbor != var2 and (assignment is None or neighbor not in assignment):
                    arcs_queue.add((neighbor, var1))

    # If the queue is empty, the CSP is consistent
    return True, current_domains

def backtracking(csp):
    def mrv_variable(assignment, current_domains):
        unassigned_vars = []
        
        # Find all unassigned variables
        for var in csp.variables:
            if var not in assignment:
                unassigned_vars.append(var)
        
        # Find the variable with the smallest domain
        min_var = unassigned_vars[0]
        for var in unassigned_vars:
            if len(current_domains[var]) < len(current_domains[min_var]):
                min_var = var
    
        return min_var
    
    def backtracking_helper(assignment, current_domains):
        # If all variables have been assigned, return the assignment
        if len(assignment) == len(csp.variables):
            return assignment

        # Select the variable with the smallest domain
        var = mrv_variable(assignment, current_domains)

        # Try each value in the domain of the selected variable
        for value in current_domains[var]:
            new_assignment = assignment.copy()
            new_assignment[var] = value

            # Check if the new assignment is consistent with the constraints
            if csp.check_partial_assignment(new_assignment):
                new_domains = copy.deepcopy(current_domains)
                new_domains[var] = [value]

                # Update the domains of the neighboring variables using AC-3
                unassigned_neighbors = [neighbor for neighbor in csp.adjacency[var] if neighbor not in new_assignment]
                arcs_queue = [(neighbor, var) for neighbor in unassigned_neighbors]
                is_consistent, updated_domains = ac3(csp, arcs_queue=arcs_queue, current_domains=new_domains, assignment=new_assignment)

                # If the updated domains are consistent, continue the search
                if is_consistent:
                    result = backtracking_helper(new_assignment, updated_domains)
                    if result is not None:
                        return result

        # If no consistent assignment was found, backtrack
        return None

    # Make a copy of the initial domains of all variables
    initial_domains = {}
    for var in csp.variables:
        initial_domains[var] = copy.deepcopy(csp.domains[var])

    # Call the backtracking helper function with an empty assignment
    return backtracking_helper({}, initial_domains)
class SudokuCSP:
    def __init__(self, partial_assignment={}):
        # Initialize the variables and domains
        self.variables = [(i, j) for i in range(1, 10) for j in range(1, 10)]
        self.domains = {var: [1, 2, 3, 4, 5, 6, 7, 8, 9] for var in self.variables}

        # Update the domains with the partial assignment
        for var in partial_assignment:
            self.domains[var] = [partial_assignment[var]]

        # Initialize the adjacency list of each variable
        self.adjacency = {var: [] for var in self.variables}
        for var in self.variables:
            # Add row constraints
            for j in range(1, 10):
                if j != var[1]:
                    self.adjacency[var].append((var[0], j))

            # Add column constraints
            for i in range(1, 10):
                if i != var[0]:
                    self.adjacency[var].append((i, var[1]))

            # Add square constraints
            square_x, square_y = (var[0] - 1) // 3, (var[1] - 1) // 3
            for i in range(3):
                for j in range(3):
                    x, y = square_x * 3 + i + 1, square_y * 3 + j + 1
                    if x != var[0] and y != var[1] and (x, y) not in self.adjacency[var]:
                        self.adjacency[var].append((x, y))

    # Function to check if two variable-value pairs are consistent
    def constraint_consistent(self, var1, val1, var2, val2):
        return True if var2 not in self.adjacency[var1] or val1 != val2 else False

    # Function to check if a partial assignment is consistent with the constraints
    def check_partial_assignment(self, assignment):
        if assignment is None:
            return False

        for var1 in assignment:
            for var2 in self.adjacency[var1]:
                if var2 in assignment:
                    if not self.constraint_consistent(var1, assignment[var1], var2, assignment[var2]):
                        return False

        return True

    # Function to check if an assignment is complete and consistent
    def is_goal(self, assignment):
        # Check if assignment is complete
        if assignment is None or set(assignment.keys()) != set(self.variables):
            return False

        # Check if assignment is consistent
        return self.check_partial_assignment(assignment)

# Function to visualize a Sudoku solution as a heatmap
def visualize_sudoku_solution(assignment_solution, file_name):
    # Convert the solution dictionary to a 9x9 array
    sudoku_array = [[0] * 9 for i in range(9)]
    for k, v in assignment_solution.items():
        row, col = k
        sudoku_array[row-1][col-1] = v

    # Create a heatmap using Seaborn
    plt.figure(figsize=(9, 9))
    sns.heatmap(data=sudoku_array, annot=True, linewidths=1.5, linecolor='k', cbar=False)
    plt.gca().invert_yaxis()

    # Save the plot as a file
    plt.savefig(file_name)
    plt.close()