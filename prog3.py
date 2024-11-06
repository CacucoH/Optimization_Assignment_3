import numpy as np

# Function to calculate the opportunity cost for each unfilled cell
def calculate_opportunity_cost(costs, supply, demand):
    m, n = len(costs), len(costs[0])
    opportunity_cost = np.zeros((m, n))

    # Calculate opportunity cost for each row and column
    for i in range(m):
        if supply[i] > 0:
            row_min = min([costs[i][j] for j in range(n) if demand[j] > 0])
            for j in range(n):
                if demand[j] > 0:
                    opportunity_cost[i][j] = costs[i][j] - row_min

    for j in range(n):
        if demand[j] > 0:
            col_min = min([costs[i][j] for i in range(m) if supply[i] > 0])
            for i in range(m):
                if supply[i] > 0:
                    opportunity_cost[i][j] = costs[i][j] - col_min

    return opportunity_cost

# Function to implement Russell's Approximation Method
def russells_approximation_method(supply, demand, costs):
    m, n = len(supply), len(demand)
    solution = np.zeros((m, n))

    while np.any(supply) and np.any(demand):
        # Calculate opportunity costs
        opportunity_cost = calculate_opportunity_cost(costs, supply, demand)

        # Find the cell with the highest opportunity cost
        max_cost = np.max(opportunity_cost)
        if max_cost == 0:  # If no opportunity cost is calculated, break out
            break

        # Get the position of the cell with the highest opportunity cost
        row_index, col_index = np.unravel_index(np.argmax(opportunity_cost), opportunity_cost.shape)

        # Allocate as much as possible to the selected cell
        allocation = min(supply[row_index], demand[col_index])
        solution[row_index][col_index] = allocation

        # Update supply and demand
        supply[row_index] -= allocation
        demand[col_index] -= allocation

        # If supply is exhausted, remove this row
        if supply[row_index] == 0:
            opportunity_cost[row_index, :] = -1  # Ignore this row in next iterations

        # If demand is satisfied, remove this column
        if demand[col_index] == 0:
            opportunity_cost[:, col_index] = -1  # Ignore this column in next iterations

    return solution

# Function to print the transportation table
def print_solution(solution):
    print("Initial Basic Feasible Solution (IBFS) using Russell's Approximation Method:")
    for row in solution:
        print(row)

# Input for supply, demand, and cost matrix
supply = [7, 9, 8]  # Example supply values
demand = [5, 4, 6, 9]  # Example demand values
costs = [
    [8, 6, 10, 9],  # Cost matrix
    [9, 7, 4, 2],
    [3, 6, 8, 7]
]

# Call the Russell's Approximation Method to get the solution
solution = russells_approximation_method(supply, demand, costs)

# Print the solution matrix
print_solution(solution)

