import numpy as np

# Function to implement the North-West Corner Method
def north_west_corner_method(supply, demand):
    # Initialize the solution matrix with zeros
    m, n = len(supply), len(demand)
    solution = np.zeros((m, n))

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

# Function to print the transportation table
def print_solution(solution):
    print("Initial Basic Feasible Solution (IBFS) using North-West Corner Method:")
    for row in solution:
        print(row)

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
    
    # Call the North-West Corner Method to get the solution
    solution = north_west_corner_method(supply, demand)
    
    # Print the solution matrix
    print_solution(solution)
    
    # Optionally: You can print the cost of the solution if required
    total_cost = np.sum(np.multiply(solution, cost_matrix))  # Element-wise multiplication of cost and allocation
    print(f"Total transportation cost: {total_cost}")

# Run the main function
if __name__ == "__main__":
    main()
