class BalancedProlemSolver:
    def __init__(self, supply: list[int], demand: list[int], cost: list[list[int]]):
        self.balanced = True 
        self.supply = supply
        self.demand = demand
        self.costs = cost
        
        if self.is_degenerate() or self.has_zero_or_negative_costs():
            print("The method is not applicable!")
            exit(0)

        if not self.is_balanced():
            self.balanced = False
            print("The problem is not balanced!")
            exit(0)

    # Function to calculate penalties (Vogel's)
    def calculate_penalties(self):
        row_penalties = []
        col_penalties = []
        
        # Row penalties
        for i in range(len(self.costs)):
            if self.supply[i] > 0:
                sorted_row = sorted([(self.costs[i][j], j) for j in range(len(self.costs[i])) if self.demand[j] > 0], key=lambda x: x[0])
                if len(sorted_row) > 1:
                    row_penalties.append(sorted_row[1][0] - sorted_row[0][0])
                else:
                    row_penalties.append(float('inf'))  # No second smallest cost, assign infinity
            else:
                row_penalties.append(-1)  # If supply is zero, ignore this row

        # Column penalties
        for j in range(len(self.costs[0])):
            if self.demand[j] > 0:
                sorted_col = sorted([(self.costs[i][j], i) for i in range(len(self.costs)) if self.supply[i] > 0], key=lambda x: x[0])
                if len(sorted_col) > 1:
                    col_penalties.append(sorted_col[1][0] - sorted_col[0][0])
                else:
                    col_penalties.append(float('inf'))  # No second smallest cost, assign infinity
            else:
                col_penalties.append(-1)  # If demand is zero, ignore this column
        
        return row_penalties, col_penalties
    
    def nw_method(self):
        """
        Implements the North-West Corner Method to allocate the minimum self.supply to self.demand.
        """
        if not self.balanced:
            print("The problem is not balanced!")
            exit(0)

        m, n = len(self.supply), len(self.demand)
        solution = [[0] * n for _ in range(m)]  # Initialize matrix

        i, j = 0, 0  # Start from the top-left corner of the matrix

        while i < m and j < n:
            allocation = min(self.supply[i], self.demand[j])
            solution[i][j] = allocation
            
            # Update the supply and demand after allocation
            self.supply[i] -= allocation
            self.demand[j] -= allocation
            
            # Move to the next row if the current supply is exhausted
            if self.supply[i] == 0:
                i += 1
            # Move to the next column if the current demand is satisfied
            if self.demand[j] == 0:
                j += 1

        return solution

    def vogels_approximation_method(self):
        """
        Implements the Vogel's approximation method to allocate the minimum self.supply to self.demand.
        """
        if not self.balanced:
            print("The problem is not balanced!")
            exit(0)

        m, n = len(self.supply), len(self.demand)
        solution = [[0] * n for _ in range(m)]  # Initialize solution matrix

        while any(self.supply) and any(self.demand):
            # Calculate penalties
            row_penalties, col_penalties = self.calculate_penalties()

            # Find the row/column with the maximum penalty
            max_row_penalty = max(row_penalties)
            max_col_penalty = max(col_penalties)

            if max_row_penalty >= max_col_penalty:
                row_index = row_penalties.index(max_row_penalty)
                # Select the cell with the minimum cost in this row
                col_index = min(
                    ((j, self.costs[row_index][j]) for j in range(n) if self.demand[j] > 0),
                    key=lambda x: x[1], default=(None, None)
                )[0]
            else:
                col_index = col_penalties.index(max_col_penalty)
                row_index = min(
                    ((i, self.costs[i][col_index]) for i in range(m) if self.supply[i] > 0),
                    key=lambda x: x[1], default=(None, None)
                )[0]

            # Allocate as much as possible to the selected cell
            allocation = min(self.supply[row_index], self.demand[col_index])
            solution[row_index][col_index] = allocation

            # Update supply and demand
            self.supply[row_index] -= allocation
            self.demand[col_index] -= allocation

            # If supply is exhausted, remove this row
            if self.supply[row_index] == 0:
                row_penalties[row_index] = -1  # Ignore this row in the next iterations

            # If demand is satisfied, remove this column
            if self.demand[col_index] == 0:
                col_penalties[col_index] = -1  # Ignore this column in the next iterations

        return solution

    def russells_approximation_method(self):
        """
        Implements the Russel's approximation method to allocate the minimum self.supply to self.demand.
        """
        if not self.balanced:
            print("The problem is not balanced!")
            exit(0)

        m, n = len(self.supply), len(self.demand)
        solution = [[0] * n for _ in range(m)]  # Initialize solution matrix

        while any(self.supply) and any(self.demand):
            # Step 1: Calculate MAX for each row
            Ui = [max(self.costs[i][j] for j in range(n) if self.demand[j] > 0) if self.supply[i] > 0 else float('-inf') for i in range(m)]

            # Step 2: Calculate MAX for each column
            Vj = [max(self.costs[i][j] for i in range(m) if self.supply[i] > 0) if self.demand[j] > 0 else float('-inf') for j in range(n)]

            # Step 3: Compute deltas (current - (Max_row + Max_col))
            delta = [[self.costs[i][j] - (Ui[i] + Vj[j]) for j in range(n)] for i in range(m)]

            # Step 4: Find the most negative Δij
            min_delta = float('inf')
            min_i, min_j = -1, -1
            for i in range(m):
                for j in range(n):
                    if self.demand[j] > 0 and self.supply[i] > 0 and delta[i][j] < min_delta:
                        min_delta = delta[i][j]
                        min_i, min_j = i, j

            # Step 5: Allocate as much as possible
            if min_i != -1 and min_j != -1:
                allocation_amount = min(self.supply[min_i], self.demand[min_j])
                solution[min_i][min_j] += allocation_amount
                self.supply[min_i] -= allocation_amount
                self.demand[min_j] -= allocation_amount

                if self.supply[min_i] == 0:
                    for j in range(n):
                        delta[min_i][j] = float('inf')  # Mark row as eliminated
                if self.demand[min_j] == 0:
                    for i in range(m):
                        delta[i][min_j] = float('inf')  # Mark column as eliminated

        return solution
    
    # Function to print the input parameter table (Cost Matrix C, supply S, demand D)
    def print_input_table(self):
        m, n = len(self.supply), len(self.demand)
        print("\nInput Parameter Table:\n------------------------------------------------------")
        # Print the header for the cost matrix
        print("dem\\sup", end=" | ")
        for j in range(n):
            print(f"Dest {j + 1}", end=" | ")
        print("supply")
        print("------------------------------------------------------")

        # Print the cost matrix and supply values
        for i in range(m):
            print(f"  Src {(i + 1):<3}", end=" | ")
            for j in range(n):
                print(f"{self.costs[i][j]:<6}", end=" | ")
            print(f"{self.supply[i]}")
 
        # Print the demand values
        print("------------------------------------------------------")
        print(f"  Demand:", end=" | ")
        for j in range(len(self.demand)):
            print(f" {self.demand[j]:<5}", end=" | ")
        print("\n------------------------------------------------------")

    """
        Three functions to check if problem is:
        a) Balanced
        b) Matrices and vectors has no negaitves
        c) There is no degeneracy
    """
    def is_balanced(self) -> bool:
        total_supply = sum(self.supply)
        total_demand = sum(self.demand)
        if total_supply != total_demand:
            return False  # Problem is not balanced
        return True
    
    def has_zero_or_negative_costs(self) -> bool:
        for row in self.costs:
            if any(cost <= 0 for cost in row):
                return True # Has zeros/negatives
        return False

    def is_degenerate(self) -> bool:
        # Check the number of allocations with m + n - 1
        m = len(self.supply)
        n = len(self.demand)
        # Simple check: If there are fewer allocations than m + n - 1, degeneracy might be an issue.
        total_allocations = sum(sum(1 for value in row if value > 0) for row in self.costs)
        if total_allocations < m + n - 1:
            return True # Probably degenerative
        return False
    

# Function to print the solution matrix
def print_solution(solution):
    print("\nSolution Matrix:")
    for row in solution:
        print(row)
    

# Function to handle input and processing
def get_input():
    """Gets input for self.supply, self.demand, and cost matrix."""
    supply = list(map(int, input("Enter the supply values (space-separated): ").split()))
    demand = list(map(int, input("Enter the demand values (space-separated): ").split()))

    cost_matrix = []
    print(f"Enter the cost matrix ({len(supply)} rows, {len(demand)} columns):")
    for i in range(len(supply)):
        row = list(map(int, input(f"Enter the costs for supply point {i + 1}: ").split()))
        cost_matrix.append(row)
    
    return supply, demand, cost_matrix


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
    print(f"\nTotal cost: {equation} = {total_cost}\n\n")
    return total_cost


def main():
    # Receive inp.
    supply, demand, cost_matrix = get_input()

    solver = BalancedProlemSolver(supply.copy(), demand.copy(), cost_matrix)
    solver.print_input_table()

    '''
    # FIRST INPUT:

    Input Parameter Table:
    ------------------------------------------------------
    dem \ sup | Dest 1 | Dest 2 | Dest 3 | Dest 4 | supply
    ------------------------------------------------------
    Src 1   | 19     | 30     | 40     | 60     | 7
    Src 2   | 70     | 30     | 40     | 60     | 9
    Src 3   | 40     | 8      | 70     | 20     | 18
    ------------------------------------------------------
    Demand: |  5     |  8     |  7     |  14    | 
    ------------------------------------------------------

    # SECOND INPUT:

    The method is not applicable!

    # THIRD INPUT:

    The problem is not balanced!

    # FOURTH INPUT:

    Input Parameter Table:
    ------------------------------------------------------
    dem \ sup | Dest 1 | Dest 2 | Dest 3 | Dest 4 | supply
    ------------------------------------------------------
    Src 1   | 6      | 3      | 5      | 4      | 22
    Src 2   | 5      | 9      | 2      | 7      | 15
    Src 3   | 5      | 7      | 8      | 6      | 8
    ------------------------------------------------------
    Demand: |  7     |  12    |  17    |  9     | 
    ------------------------------------------------------
    '''

    print("-- Solution with NW method --")
    solution_matrix = solver.nw_method()
    print_solution(solution_matrix)
    total_cost = calculate_total_cost(cost_matrix, solution_matrix)

    '''
    # FIRST INPUT:

    -- Solution with NW method --

    Solution Matrix:
    [5, 2, 0, 0]
    [0, 6, 3, 0]
    [0, 0, 4, 14]

    Total cost: 19 * 5 + 30 * 2 + 30 * 6 + 40 * 3 + 70 * 4 + 20 * 14 = 1015

    # FOURTH INPUT:

    -- Solution with NW method --

    Solution Matrix:
    [7, 12, 3, 0]
    [0, 0, 14, 1]
    [0, 0, 0, 8]

    Total cost: 6 * 7 + 3 * 12 + 5 * 3 + 2 * 14 + 7 * 1 + 6 * 8 = 176
    '''
    
    print("-- Solution with Vogel's approx. --")
    solver = BalancedProlemSolver(supply.copy(), demand.copy(), cost_matrix)
    solution_matrix = solver.vogels_approximation_method()
    print_solution(solution_matrix)
    total_cost = calculate_total_cost(cost_matrix, solution_matrix)
    
    '''
    # FIRST INPUT:

    -- Solution with Vogel's approx. --

    Solution Matrix:
    [5, 0, 0, 2]
    [0, 0, 7, 2]
    [0, 8, 0, 10]

    Total cost: 19 * 5 + 10 * 2 + 40 * 7 + 60 * 2 + 8 * 8 + 20 * 10 = 779

    # FOURTH INPUT:

    -- Solution with Vogel's approx. --

    Solution Matrix:
    [0, 12, 2, 8]
    [0, 0, 15, 0]
    [7, 0, 0, 1]

    Total cost: 3 * 12 + 5 * 2 + 4 * 8 + 2 * 15 + 5 * 7 + 6 * 1 = 149
    '''
    
    print("-- Solution with Russel's approx. --")
    solver = BalancedProlemSolver(supply.copy(), demand.copy(), cost_matrix)
    solution_matrix = solver.russells_approximation_method()
    print_solution(solution_matrix)
    total_cost = calculate_total_cost(cost_matrix, solution_matrix)

    '''
    # FIRST INPUT:

    -- Solution with Russel's approx. --

    Solution Matrix:
    [5, 2, 0, 0]
    [0, 2, 7, 0]
    [0, 4, 0, 14]

    Total cost: 19 * 5 + 30 * 2 + 30 * 2 + 40 * 7 + 8 * 4 + 20 * 14 = 807

    # FOURTH INPUT:

    -- Solution with Russel's approx. --

    Solution Matrix:
    [0, 12, 2, 8]
    [0, 0, 15, 0]
    [7, 0, 0, 1]

    Total cost: 3 * 12 + 5 * 2 + 4 * 8 + 2 * 15 + 5 * 7 + 6 * 1 = 149
    '''


if __name__ == "__main__":
    main()
