def initialize_problem(supply, demand, cost):
    return supply.copy(), demand.copy(), cost.copy()

def calculate_ui_and_vj(cost, allocation):
    rows = len(allocation)
    cols = len(allocation[0])
    u = [float('nan')] * rows
    v = [float('nan')] * cols

    # Set initial u0 = 0 for the first supply
    u[0] = 0

    # Fill u and v based on the current allocation
    for i in range(rows):
        for j in range(cols):
            if allocation[i][j] > 0:
                if not (u[i] is float('nan')) and (v[j] is float('nan')):
                    v[j] = cost[i][j] - u[i]
                elif not (v[j] is float('nan')) and (u[i] is float('nan')):
                    u[i] = cost[i][j] - v[j]

    # Fill remaining u and v if possible
    for _ in range(rows + cols):
        for i in range(rows):
            for j in range(cols):
                if allocation[i][j] > 0:
                    if (u[i] is float('nan')) and not (v[j] is float('nan')):
                        u[i] = cost[i][j] - v[j]
                    if (v[j] is float('nan')) and not (u[i] is float('nan')):
                        v[j] = cost[i][j] - u[i]

    return u, v

def calculate_reduced_costs(cost, u, v):
    reduced_costs = []
    for i in range(len(cost)):
        row_costs = []
        for j in range(len(cost[0])):
            reduced_cost = cost[i][j] - (u[i] + v[j] if not (u[i] is float('nan')) and not (v[j] is float('nan')) else 0)
            row_costs.append(reduced_cost)
        reduced_costs.append(row_costs)
    return reduced_costs

def allocate_cost(allocation, supply, demand, i, j, allocation_amount):
    allocation[i][j] += allocation_amount
    supply[i] -= allocation_amount
    demand[j] -= allocation_amount

def transport_problem(supply, demand, cost):
    supply, demand, cost = initialize_problem(supply, demand, cost)
    rows, cols = len(supply), len(demand)
    allocation = [[0 for _ in range(cols)] for _ in range(rows)]

    # Step 1: Initial Allocation
    while any(supply) and any(demand):
        u, v = calculate_ui_and_vj(cost, allocation)
        reduced_costs = calculate_reduced_costs(cost, u, v)

        # Find the most negative reduced cost Δij
        min_cost_value = float('inf')
        min_cost_index = (-1, -1)
        for i in range(rows):
            for j in range(cols):
                if reduced_costs[i][j] < min_cost_value:
                    min_cost_value = reduced_costs[i][j]
                    min_cost_index = (i, j)

        # If there are no negative reduced costs, break
        if min_cost_value >= 0:
            break

        i, j = min_cost_index

        # Allocate the minimum of supply and demand
        allocation_amount = min(supply[i], demand[j])
        allocate_cost(allocation, supply, demand, i, j, allocation_amount)

        print(f"Allocating {allocation_amount} from S{i+1} to D{j+1}")
        print("Updated Allocation Table:")
        for row in allocation:
            print(row)

    # Final allocation and costs
    total_cost = sum(allocation[i][j] * cost[i][j] for i in range(rows) for j in range(cols))
    print("Final Allocation Table:")
    for row in allocation:
        print(row)
    print(f"Minimum Total Transportation Cost: {total_cost}")


def main():
    # Example input based on your example
    supply = [7, 9, 18]  # S1, S2, S3
    demand = [5, 8, 7, 14]  # D1, D2, D3, D4
    cost = [[19, 30, 50, 10],
            [70, 30, 40, 60],
            [40, 8, 70, 20]]

    transport_problem(supply, demand, cost)

if __name__ == "__main__":
    main()
