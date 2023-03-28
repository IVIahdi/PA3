import copy
def ac3(csp, arcs_queue=None, current_domains=None, assignment=None):
    # Create a deep copy of the domains to avoid modifying the original CSP
    if current_domains is None:
        current_domains = {}
        for var in csp.variables:
            current_domains[var] = copy.deepcopy(csp.domains)

    # Create the queue of arcs to be processed
    if arcs_queue is None:
        arcs_queue = set()
        for var1 in csp.variables:
            for var2 in csp.adjacency[var1]:
                arcs_queue.add((var1, var2))

    # Initialize the assignment if not given
    if assignment is None:
        assignment = {}

    # Helper function to check if a constraint is consistent
    def revise(var1, var2):
        revised = False
        for val1 in current_domains[var1]:
            if all(not csp.constraint_consistent(var1, val1, var2, val2) for val2 in current_domains[var2]):
                current_domains[var1].remove(val1)
                revised = True
        return revised

    # Enforce arc-consistency
    while arcs_queue:
        var1, var2 = arcs_queue.pop()
        if revise(var1, var2):
            if not current_domains[var1]:
                return False, current_domains
            for neighbor in csp.adjacency[var1]:
                if neighbor != var2 and neighbor not in assignment:
                    arcs_queue.add((neighbor, var1))

    return True, current_domains