def nw_method(supply, demand):
    # Initialize the solution matrix with zeros
    m, n = len(supply), len(demand)
    solution = [[0] * n for _ in range(m)]  # Create a 2D matrix of zeros

    # Set up pointers for supply and demand
    i, j = 0, 0
    
    # Loop until all supply and demand are exhausted
    while i < m and j < n:
        # Allocate the minimum of supply[i] and demand[j] to solution[i][j]
        allocation = min(supply[i], demand[j])
        solution[i][j] = allocation
        
        # Update the supply and demand after allocation
        supply[i] -= allocation
        demand[j] -= allocation
        
        # If supply[i] is exhausted, move to the next row
        if supply[i] == 0:
            i += 1
        # If demand[j] is satisfied, move to the next column
        if demand[j] == 0:
            j += 1

    return solution

# Function to print the transportation table (showing the cost matrix with supply and demand)
def print_input_table(supply, cost_matrix, demand):
    print("\nInput Parameter Table:")
    print(f"{'Supply\\Demand':<15}", end="")
    for d in demand:
        print(f"{d:<10}", end="")
    print()
    
    for i, row in enumerate(cost_matrix):
        print(f"Supply {i + 1:<5}", end="")
        for j, cost in enumerate(row):
            print(f"{cost:<10}", end="")
        print()

# Function to check if the problem is balanced
def check_balance(supply, demand):
    if sum(supply) != sum(demand):
        print("The problem is not balanced!")
        return False
    return True

# Function to take input from the user (or pre-define it for testing)
def get_input():
    # Taking vector of supply (S) from user input
    S = list(map(int, input("Enter the supply coefficients (space-separated): ").split()))
    
    # Taking matrix of costs (C) from user input
    m = len(S)
    n = int(input("Enter the number of demand locations: "))
    C = []
    print("Enter the cost matrix row by row:")
    for i in range(m):
        row = list(map(int, input(f"Enter costs for supply {i+1} (space-separated): ").split()))
        C.append(row)

    # Taking vector of demand (D) from user input
    D = list(map(int, input("Enter the demand coefficients (space-separated): ").split()))
    
    return S, C, D

# Main function to run the process
def main():
    # Get inputs from user or define them for testing
    supply, cost_matrix, demand = get_input()

    # Check if the problem is balanced
    if not check_balance(supply, demand):
        return
    
    # Print the input parameter table
    print_input_table(supply, cost_matrix, demand)
    
    # Call the North-West Corner Method to get the solution
    solution = nw_method(supply[:], demand[:])  # Pass copies to avoid modification in the original lists
    
    # Print the solution matrix
    print("\nInitial Basic Feasible Solution (IBFS) using North-West Corner Method:")
    for row in solution:
        print(row)
    
    # Optionally: You can print the cost of the solution if required
    total_cost = sum(solution[i][j] * cost_matrix[i][j] for i in range(len(supply)) for j in range(len(demand)))
    print(f"Total transportation cost: {total_cost}")

# Run the main function
if __name__ == "__main__":
    main()
