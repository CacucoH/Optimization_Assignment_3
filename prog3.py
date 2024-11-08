def russells_approximation_method(supply, demand, costs):
    m, n = len(supply), len(demand)
    solution = [[0] * n for _ in range(m)]  # Initialize solution matrix

    while any(supply) and any(demand):
        # Step 1: Calculate ˉUi for each row
        Ui = [max(costs[i][j] for j in range(n) if demand[j] > 0) if supply[i] > 0 else float('-inf') for i in range(m)]

        # Step 2: Calculate ˉVj for each column
        Vj = [max(costs[i][j] for i in range(m) if supply[i] > 0) if demand[j] > 0 else float('-inf') for j in range(n)]

        # Step 3: Compute reduced cost Δij
        delta = [[costs[i][j] - (Ui[i] + Vj[j]) for j in range(n)] for i in range(m)]

        # Print current state
        print("Current Table:")
        print_table(costs, delta, supply, demand, Ui, Vj)

        # Step 4: Find the most negative Δij
        min_delta = float('inf')
        min_i, min_j = -1, -1
        for i in range(m):
            for j in range(n):
                if demand[j] > 0 and supply[i] > 0 and delta[i][j] < min_delta:
                    min_delta = delta[i][j]
                    min_i, min_j = i, j
        print(f"!!! The MOST negative is {costs[min_i][min_j]}")

        # Step 5: Allocate as much as possible
        if min_i != -1 and min_j != -1:
            allocation_amount = min(supply[min_i], demand[min_j])
            solution[min_i][min_j] += allocation_amount
            supply[min_i] -= allocation_amount
            demand[min_j] -= allocation_amount

            # Print allocation
            print(f"Allocating {allocation_amount} from S{min_i + 1} to D{min_j + 1}")

            # Mark rows/columns exhausted
            if supply[min_i] == 0:
                for j in range(n):
                    delta[min_i][j] = float('inf')  # Mark row as eliminated
            if demand[min_j] == 0:
                for i in range(m):
                    delta[i][min_j] = float('inf')  # Mark column as eliminated

    return solution

def print_table(costs, delta, supply, demand, Ui, Vj):
    m, n = len(costs), len(costs[0])
    print("\t" + "\t".join(f"D{j + 1}{'':<5}" for j in range(n)) + "\tSupply\tˉUi")
    for i in range(m):
        row_str = f"S{i + 1}\t" + "\t".join(f"{costs[i][j]} [{delta[i][j]}]{'':<5}" for j in range(n))
        print(row_str + f"\t{supply[i]}\t{Ui[i]}")
    print("\t" + "\t".join(f"{d:<5}" for d in demand) + "\t\tˉVj")
    print("\t" + "\t".join(f"{v:<5}" for v in Vj) + "\n")

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

def main():
    supply = [250, 300, 150]  # Supply at each source
    demand = [150, 250, 300]  # Demand at each destination
    costs = [
        [13, 20,23 ],
        [17, 16, 22],
        [21, 10, 14],
    ]

    initial_solution = russells_approximation_method(supply, demand, costs)
    print("Final Solution using Russell's Approximation Method:")
    for row in initial_solution:
        print(row)
    
    result = calculate_total_cost(costs, initial_solution)

if __name__ == "__main__":
    main()
