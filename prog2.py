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
            print(f"{costs[i][j]:<6}", end=" | ")
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

# Function to print the transportation table
def print_solution(solution):
    print("\IBFS using Vogel’s Approximation Method:")
    for row in solution:
        print(row)

# Main function to process input and apply the algorithm
def main():
    # Get the supply vector from the user (space-separated)
    supply = list(map(int, input("Enter the supply values (space-separated): ").split()))

    # Get the cost matrix from the user (space-separated rows)
    costs = []
    for i in range(len(supply)):
        row = list(map(int, input(f"Enter the costs for supply row {i + 1}: ").split()))
        costs.append(row)

    # Get the demand vector from the user (space-separated)
    demand = list(map(int, input("Enter the demand values (space-separated): ").split()))

    # Check if the problem is balanced
    if not is_balanced(supply, demand):
        print("The problem is not balanced!")
        return
    
    # Print the input table
    print_input_table(costs, supply, demand)
    
    # Call the Vogel's Approximation Method to get the solution
    solution = vogels_approximation_method(supply, demand, costs)
    
    # Print the solution matrix
    print_solution(solution)

# Execute the main function
if __name__ == "__main__":
    main()
