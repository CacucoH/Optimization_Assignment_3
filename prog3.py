def russells_method_solver(S, C, D):
    # Step 1: Check if the input is valid
    if not S or not D or not C or len(S) != len(C) or any(len(row) != len(D) for row in C):
        return "The method is not applicable!"
    
    # Step 2: Check if the problem is balanced
    if sum(S) != sum(D):
        return "The problem is not balanced!"
    
    # Step 3: Print the input parameter table (cost matrix with supply and demand)
    print("Input parameter table:")
    
    # Print the column headers (Demand values)
    demand_header = "        " + "  ".join([f"Demand {i+1}" for i in range(len(D))])
    print(demand_header)
    
    # Print the cost matrix with supply values at the end of each row
    for i in range(len(S)):
        row = "Supply " + str(i+1) + " " + "  ".join(map(str, C[i])) + "  " + str(S[i])
        print(row)
    
    # Print the total demand row
    total_demand = "Demand " + "  ".join(map(str, D)) + "  "
    print(total_demand)
    
    # Step 4: Apply the Least Cost Method (Russell's Method) to find the initial solution
    # Create a solution matrix to store the transport plan
    transport_plan = [[0 for _ in range(len(D))] for _ in range(len(S))]
    
    # Copy of supply and demand for manipulation
    supply = S[:]
    demand = D[:]
    
    # Step 5: Track exhausted supply and demand
    exhausted_supply = [False] * len(S)
    exhausted_demand = [False] * len(D)
    
    # Step 6: Apply Least Cost Method
    while any(s > 0 for s in supply) and any(d > 0 for d in demand):
        # Find the cell with the minimum cost in the cost matrix that is still valid
        min_cost = float('inf')
        min_row, min_col = -1, -1
        for i in range(len(S)):
            if exhausted_supply[i]:
                continue
            for j in range(len(D)):
                if exhausted_demand[j]:
                    continue
                if supply[i] > 0 and demand[j] > 0 and C[i][j] < min_cost:
                    min_cost = C[i][j]
                    min_row, min_col = i, j
        
        # Allocate the supply to the selected cell
        allocated = min(supply[min_row], demand[min_col])
        transport_plan[min_row][min_col] = allocated
        supply[min_row] -= allocated
        demand[min_col] -= allocated
        
        # If supply for a row is exhausted, mark the row as exhausted
        if supply[min_row] == 0:
            exhausted_supply[min_row] = True
        
        # If demand for a column is fulfilled, mark the column as exhausted
        if demand[min_col] == 0:
            exhausted_demand[min_col] = True

    # Step 7: Print the solution (transportation plan)
    print("\nTransportation plan (solution):")
    total_cost = 0
    for i in range(len(S)):
        for j in range(len(D)):
            if transport_plan[i][j] > 0:
                print(f"From Supply {i+1} to Demand {j+1}: {transport_plan[i][j]} units")
                total_cost += transport_plan[i][j] * C[i][j]
    
    # Print the total transportation cost
    print(f"\nTotal transportation cost: {total_cost}")
    
    return "Solution printed successfully!"

# Example usage
S = [10, 20, 30]  # Supply vector
C = [[3, 2, 4],    # Cost matrix
     [2, 5, 3],
     [6, 4, 7]]
D = [15, 25, 20]   # Demand vector

result = russells_method_solver(S, C, D)
print(result)
