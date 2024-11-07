# Function to print the input parameter table (Cost Matrix C, Supply S, Demand D)
def print_input_table(costs, supply, demand):
    m, n = len(supply), len(demand)
    print("\nInput Parameter Table:")
    print("------------------------------------------------------")
    # Print the header for the cost matrix
    print("Supply \\ Demand", end=" | ")
    for j in range(n):
        print(f"Store {j + 1}", end=" | ")
    print("Supply")
    print("")

    # Print the cost matrix and supply values
    for i in range(m):
        print(f"Warehouse {(i + 1):<5}", end=" | ")
        for j in range(n):
            print(f"{costs[i][j]:<7}", end=" | ")
        print(f"{supply[i]}")

    # Print the demand values
    print("------------------------------------------------------")
    print(f"Demand: {', '.join(map(str, demand))}")
    print("------------------------------------------------------")

# Function to check if the problem is balanced
def is_balanced(supply, demand):
    total_supply = sum(supply)
    total_demand = sum(demand)
    if total_supply != total_demand:
        return False  # Problem is not balanced
    return True

# North-West Corner Method
def nw_method(supply, demand):
    """
    Implements the North-West Corner Method to allocate the minimum supply to demand.
    """
    m, n = len(supply), len(demand)
    solution = [[0] * n for _ in range(m)]  # Initialize matrix

    i, j = 0, 0  # Start from the top-left corner of the matrix

    while i < m and j < n:
        allocation = min(supply[i], demand[j])
        solution[i][j] = allocation
        
        # Update the supply and demand after allocation
        supply[i] -= allocation
        demand[j] -= allocation
        
        # Move to the next row if the current supply is exhausted
        if supply[i] == 0:
            i += 1
        # Move to the next column if the current demand is satisfied
        if demand[j] == 0:
            j += 1

    return solution

# Function to calculate penalties for rows and columns (used in Vogel's Approximation Method)
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

# Vogel's Approximation Method
def vogels_approximation_method(supply, demand, costs):
    m, n = len(supply), len(demand)
    solution = [[0] * n for _ in range(m)]  # Initialize solution matrix

    while any(supply) and any(demand):
        # Calculate penalties for rows and columns
        row_penalties, col_penalties = calculate_penalties(costs, supply, demand)

        # Find the row or column with the maximum penalty
        max_row_penalty = max(row_penalties)
        max_col_penalty = max(col_penalties)

        if max_row_penalty >= max_col_penalty:
            # Row with maximum penalty
            row_index = row_penalties.index(max_row_penalty)
            # Select the cell with the minimum cost in this row
            col_index = min(
                ((j, costs[row_index][j]) for j in range(n) if demand[j] > 0),
                key=lambda x: x[1], default=(None, None)
            )[0]
        else:
            # Column with maximum penalty
            col_index = col_penalties.index(max_col_penalty)
            # Select the cell with the minimum cost in this column
            row_index = min(
                ((i, costs[i][col_index]) for i in range(m) if supply[i] > 0),
                key=lambda x: x[1], default=(None, None)
            )[0]

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

# Russell’s Approximation Method
def russells_approximation_method(supply, demand, costs):
    m, n = len(supply), len(demand)
    solution = [[0] * n for _ in range(m)]  # Initialize solution matrix

    while any(supply) and any(demand):
        row_penalties = []
        col_penalties = []

        # Calculate row penalties (weighted by supply)
        for i in range(m):
            if supply[i] > 0:
                sorted_row = sorted([(costs[i][j], j) for j in range(n) if demand[j] > 0], key=lambda x: x[0])
                if len(sorted_row) > 1:
                    penalty = (sorted_row[1][0] - sorted_row[0][0]) * supply[i]
                    row_penalties.append(penalty)
                else:
                    row_penalties.append(float('inf'))  # No second smallest cost, assign infinity
            else:
                row_penalties.append(-1)

        # Calculate column penalties (weighted by demand)
        for j in range(n):
            if demand[j] > 0:
                sorted_col = sorted([(costs[i][j], i) for i in range(m) if supply[i] > 0], key=lambda x: x[0])
                if len(sorted_col) > 1:
                    penalty = (sorted_col[1][0] - sorted_col[0][0]) * demand[j]
                    col_penalties.append(penalty)
                else:
                    col_penalties.append(float('inf'))  # No second smallest cost, assign infinity
            else:
                col_penalties.append(-1)

        # Select the row or column with the highest penalty
        max_row_penalty = max(row_penalties)
        max_col_penalty = max(col_penalties)

        if max_row_penalty >= max_col_penalty:
            row_index = row_penalties.index(max_row_penalty)
            col_index = min(
                ((j, costs[row_index][j]) for j in range(n) if demand[j] > 0),
                key=lambda x: x[1], default=(None, None)
            )[0]
        else:
            col_index = col_penalties.index(max_col_penalty)
            row_index = min(
                ((i, costs[i][col_index]) for i in range(m) if supply[i] > 0),
                key=lambda x: x[1], default=(None, None)
            )[0]

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

# Function to print the solution matrix
def print_solution(solution):
    print("\nSolution Matrix:")
    for row in solution:
        print(row)

# Function to calculate and print the total cost with equation form
def calculate_total_cost(init_matrix, solution_matrix):
    total_cost = 0
    equation_parts = []

    # Calculate the total cost and construct the equation parts
    for i in range(len(init_matrix)):
        for j in range(len(solution_matrix[0])):
            if solution_matrix[i][j] != 0:
                coeff = init_matrix[i][j]
                allocation = solution_matrix[i][j]
                total_cost += coeff * allocation
                equation_parts.append(f"{coeff} * {allocation}")

    # Print the equation form
    equation = " + ".join(equation_parts)
    print(f"\nTotal cost: {equation} = {total_cost}")
    return total_cost

# Function to handle input and processing
def get_input():
    """Gets input for supply, demand, and cost matrix."""
    supply = list(map(int, input("Enter the supply values (space-separated): ").split()))
    demand = list(map(int, input("Enter the demand values (space-separated): ").split()))
    
    cost_matrix = []
    print(f"Enter the cost matrix ({len(supply)} rows, {len(demand)} columns):")
    for i in range(len(supply)):
        row = list(map(int, input(f"Enter the costs for supply point {i + 1}: ").split()))
        cost_matrix.append(row)

    return supply, demand, cost_matrix

def main():
    # Get the supply, demand, and cost matrix from the user
    supply, demand, cost_matrix = get_input()

    # Check if the problem is balanced
    if not is_balanced(supply, demand):
        print("The problem is not balanced!")
        return

    # Print the input table
    print_input_table(cost_matrix, supply, demand)

    # Uncomment method you want to use

    # solution_matrix = nw_method(supply.copy(), demand.copy())
    # solution_matrix = vogels_approximation_method(supply.copy(), demand.copy(), cost_matrix)
    solution_matrix = russells_approximation_method(supply.copy(), demand.copy(), cost_matrix)

    print_solution(solution_matrix)
    total_cost = calculate_total_cost(cost_matrix, solution_matrix)

if __name__ == "__main__":
    main()
