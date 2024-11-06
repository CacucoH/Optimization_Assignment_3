def nw_method(supply, demand):
    """
    Implements the North-West Corner Method to allocate the minimum supply to demand.
    
    - `supply` A list of supply quantities for each warehouse.
    - `demand` A list of demand quantities for each store.

    Returns `matrix` representing the transportation allocation.
    """
    m, n = len(supply), len(demand)
    solution = [[0] * n for _ in range(m)]  # Initial matrix

    i, j = 0, 0  # Start from the top-left corner of the matrix

    # Continue until all supply and demand are exhausted
    while i < m and j < n:
        # Allocate the minimum of supply[i] and demand[j]
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

def check_balance(supply, demand):
    """Checks if problem is balanced"""
    if sum(supply) != sum(demand):
        print("The problem is not balanced!")
        return False
    return True

def get_input():
    """gets input"""
    # Get supply coefficients
    supply = list(map(int, input("Enter the supply coefficients: ").split()))
    
    # Get the number of demand locations
    m = len(supply)
    n = int(input("Enter the number of demand locations: "))
    
    # Get cost matrix
    cost_matrix = []
    print("Enter the cost matrix row by row:")
    for i in range(m):
        row = list(map(int, input(f"Enter costs for supply {i+1}: ").split()))
        cost_matrix.append(row)

    # Get demand coefficients
    demand = list(map(int, input("Enter the demand coefficients: ").split()))
    
    return supply, cost_matrix, demand


def solution(init_matrix, solution_matrix) -> int:
    """
        ### Obtains a solution
        Goes through solution matrix and sum up obtained values multiplied by initial coefficients
        
        Returns `result`
    """
    result = 0
    for i in range(0, len(init_matrix)):
        for j in range(0, len(solution_matrix) + 1):
            final_val = solution_matrix[i][j]
            
            if final_val == 0:
                continue

            coeff = init_matrix[i][j]
            result += coeff * final_val
            print(f"{coeff} * {final_val}", end="")

            if not(i + 1 == len(init_matrix) and j == len(solution_matrix)):
                print(f" + ", end="")
            
        if i + 1 == len(init_matrix):
            print(f" = ", end="")
    
    return result


def print_init_problem(demand: list[int], cost_matrix: list[int], supply: list[int]):
    print(f"\nInitial problem:\n{'Supply\\Demand':<15}", end="")
    for d in demand:
        print(f"{d:<10}", end="")
    print()

    for i, row in enumerate(cost_matrix):
        print(f"Supply {i + 1:<8}", end="")
        for cost in row:
            print(f"{cost:<10}", end="")
        print()

def main():
    # Get input values from user
    supply, cost_matrix, demand = get_input()
    if not check_balance(supply, demand):
        return
    
    # Print the input table
    print_init_problem(demand, cost_matrix, demand)
    
    # Solve using North-West Corner Method
    solution_matrix = nw_method(supply, demand)  # Pass copies to avoid modifying the original lists
    
    # Print the solution matrix
    print("\nSolution:")
    for row in solution_matrix:
        print(row)

    print("\nTotal cost: ")
    total_cost = solution(cost_matrix, solution_matrix)

    print(total_cost)

if __name__ == "__main__":
    main()
