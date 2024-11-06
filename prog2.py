import numpy as np

# Function to calculate penalties for rows and columns
def calculate_penalties(costs, supply, demand):
    row_penalties = []
    col_penalties = []
    
    # Row penalties
    for i in range(len(costs)):
        if supply[i] > 0:
            sorted_row = sorted([(costs[i][j], j) for j in range(len(costs[i])) if demand[j] > 0], key=lambda x: x[0])
            if len(sorted_row) > 1:
                row_penalties.append(sorted_row[1][0] - sorted_row[0][0])
            else:
                row_penalties.append(float('inf'))  # No second smallest cost, assign infinity
        else:
            row_penalties.append(-1)  # If supply is zero, ignore this row

    # Column penalties
    for j in range(len(costs[0])):
        if demand[j] > 0:
            sorted_col = sorted([(costs[i][j], i) for i in range(len(costs)) if supply[i] > 0], key=lambda x: x[0])
            if len(sorted_col) > 1:
                col_penalties.append(sorted_col[1][0] - sorted_col[0][0])
            else:
                col_penalties.append(float('inf'))  # No second smallest cost, assign infinity
        else:
            col_penalties.append(-1)  # If demand is zero, ignore this column
    
    return row_penalties, col_penalties

# Function to implement Vogel's Approximation Method
def vogels_approximation_method(supply, demand, costs):
    m, n = len(supply), len(demand)
    solution = np.zeros((m, n))

    while np.any(supply) and np.any(demand):
        # Calculate penalties for rows and columns
        row_penalties, col_penalties = calculate_penalties(costs, supply, demand)

        # Find the row or column with the maximum penalty
        max_row_penalty = max(row_penalties)
        max_col_penalty = max(col_penalties)

        if max_row_penalty >= max_col_penalty:
            # Row with maximum penalty
            row_index = row_penalties.index(max_row_penalty)
            # Select the cell with the minimum cost in this row
            col_index = np.argmin([costs[row_index][j] if demand[j] > 0 else float('inf') for j in range(n)])
        else:
            # Column with maximum penalty
            col_index = col_penalties.index(max_col_penalty)
            # Select the cell with the minimum cost in this column
            row_index = np.argmin([costs[i][col_index] if supply[i] > 0 else float('inf') for i in range(m)])

        # Allocate as much as possible to the selected cell
        allocation = min(supply[row_index], demand[col_index])
        solution[row_index][col_index] = allocation

        # Update supply and demand
        supply[row_index] -= allocation
        demand[col_index] -= allocation

        # If supply is exhausted, remove this row
        if supply[row_index] == 0:
            row_penalties[row_index] = -1  # Ignore this row in the next iterations

        # If demand is satisfied, remove this column
        if demand[col_index] == 0:
            col_penalties[col_index] = -1  # Ignore this column in the next iterations

    return solution

# Function to print the transportation table
def print_solution(solution):
    print("Initial Basic Feasible Solution (IBFS) using Vogel’s Approximation Method:")
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

# Call the Vogel's Approximation Method to get the solution
solution = vogels_approximation_method(supply, demand, costs)

# Print the solution matrix
print_solution(solution)

