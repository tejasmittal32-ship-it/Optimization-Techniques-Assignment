def balance_problem(cost, supply, demand):
    total_supply = sum(supply)
    total_demand = sum(demand)

    if total_supply == total_demand:
        return cost, supply, demand

    if total_supply > total_demand:
        extra = total_supply - total_demand
        for row in cost:
            row.append(0)

        demand.append(extra)

    else:

        extra = total_demand - total_supply

        n = len(cost[0])
        cost.append([0] * n)
        supply.append(extra)

    return cost, supply, demand

def vogel_approximation(cost, supply, demand):

    m = len(supply)
    n = len(demand)

    allocation = [[0 for j in range(n)] for i in range(m)]

    supply = supply[:]
    demand = demand[:]

    active_rows = [True] * m
    active_cols = [True] * n

    while sum(demand) > 0:

        row_penalty = [-1] * m
        col_penalty = [-1] * n

        for i in range(m):

            if not active_rows[i]:
                continue

            values = []

            for j in range(n):

                if active_cols[j]:
                    values.append(cost[i][j])

            values.sort()

            if len(values) >= 2:
                row_penalty[i] = values[1] - values[0]

            elif len(values) == 1:
                row_penalty[i] = values[0]

        for j in range(n):

            if not active_cols[j]:
                continue

            values = []

            for i in range(m):

                if active_rows[i]:
                    values.append(cost[i][j])

            values.sort()

            if len(values) >= 2:
                col_penalty[j] = values[1] - values[0]

            elif len(values) == 1:
                col_penalty[j] = values[0]

        max_row = max(row_penalty)
        max_col = max(col_penalty)

        if max_row >= max_col:
            i = row_penalty.index(max_row)
            j = -1
            minimum_cost = float('inf')

            for col in range(n):

                if active_cols[col] and cost[i][col] < minimum_cost:
                    minimum_cost = cost[i][col]
                    j = col

        else:
            j = col_penalty.index(max_col)
            i = -1
            minimum_cost = float('inf')
            for row in range(m):

                if active_rows[row] and cost[row][j] < minimum_cost:
                    minimum_cost = cost[row][j]
                    i = row

        amount = min(supply[i], demand[j])

        allocation[i][j] = amount
        supply[i] -= amount
        demand[j] -= amount
        if supply[i] == 0:
            active_rows[i] = False
        if demand[j] == 0:
            active_cols[j] = False

    return allocation
def calculate_uv(cost, allocation):

    m = len(cost)
    n = len(cost[0])
    u = [None] * m
    v = [None] * n

    u[0] = 0

    changed = True
    while changed:

        changed = False

        for i in range(m):

            for j in range(n):
                if allocation[i][j] > 0:
                    if u[i] is not None and v[j] is None:
                        v[j] = cost[i][j] - u[i]
                        changed = True
                    elif v[j] is not None and u[i] is None:
                        u[i] = cost[i][j] - v[j]
                        changed = True
    return u, v
def calculate_deltas(cost, allocation, u, v):

    m = len(cost)
    n = len(cost[0])

    delta = [[0 for j in range(n)] for i in range(m)]

    minimum = 0
    entering = None

    for i in range(m):
        for j in range(n):
            if allocation[i][j] == 0:
                delta[i][j] = cost[i][j] - (u[i] + v[j])
                if delta[i][j] < minimum:
                    minimum = delta[i][j]
                    entering = (i, j)

    return delta, entering
def find_loop(allocation, start):

    m = len(allocation)
    n = len(allocation[0])

    cells = set()
    for i in range(m):

        for j in range(n):

            if allocation[i][j] > 0:
                cells.add((i, j))
    cells.add(start)
    def search(path, move_row):

        current = path[-1]

        i, j = current
        if move_row:

            candidates = [
                cell for cell in cells
                if cell[0] == i
            ]
        else:

            candidates = [
                cell for cell in cells
                if cell[1] == j
            ]

        for cell in candidates:
            if cell == current:
                continue
            if cell == start:

                if len(path) >= 4:
                    return path + [start]

                continue
            if cell in path:
                continue
            result = search(
                path + [cell],
                not move_row
            )

            if result is not None:
                return result

        return None
    loop = search([start], True)

    if loop is None:
        loop = search([start], False)

    return loop
def modi(cost, allocation):

    while True:
        u, v = calculate_uv(
            cost,
            allocation
        )

        print("\nU values:", u)
        print("V values:", v)

        delta, entering = calculate_deltas(
            cost,
            allocation,
            u,
            v
        )
        print("\nDelta Table:")
        for row in delta:
            print(row)
        if entering is None:
            print("\nCurrent solution is OPTIMAL.")
            break

        print("\nEntering cell:", entering)
        loop = find_loop(
            allocation,
            entering
        )
        if loop is None:
            print("Loop NOT FOUND")
            break

        loop = loop[:-1]
        print("Loop:", loop)
        signs = []

        for k in range(len(loop)):
            if k % 2 == 0:
                signs.append(1)
            else:
                signs.append(-1)
        theta = float('inf')

        for k in range(len(loop)):
            if signs[k] == -1:
                i, j = loop[k]
                if allocation[i][j] < theta:
                    theta = allocation[i][j]
        for k in range(len(loop)):
            i, j = loop[k]
            if signs[k] == 1:
                allocation[i][j] += theta
            else:
                allocation[i][j] -= theta
    return allocation
def calculate_cost(cost, allocation):
    total = 0
    for i in range(len(cost)):
        for j in range(len(cost[0])):
            total += cost[i][j] * allocation[i][j]
    return total

def print_allocation(allocation):
    print("\nAllocation:")
    for row in allocation:
        print(row)

print("TRANSPORTATION PROBLEM")
m = int(input("Enter no of sources: "))
n = int(input("Enter no of destinations: "))
print("\nEnter transportation cost matrix:")
cost = []

for i in range(m):
    row = list(
        map(
            int,
            input(
                f"Enter costs for Source {i + 1}: "
            ).split()
        )
    )

    cost.append(row)
print("\nsupply of each source:")

supply = list(
    map(
        int,
        input().split()
    )
)
print("\ndemand of each destination:")

demand = list(
    map(
        int,
        input().split()
    )
)
cost, supply, demand = balance_problem(cost,supply,demand)

allocation = vogel_approximation(cost,supply,demand)
print("VAM Solution")
print_allocation(allocation)
initial_cost = calculate_cost(cost, allocation
)
print("\nTransportation Cost:",    initial_cost)
allocation = modi(cost, allocation)
final_cost = calculate_cost(cost,allocation)
print("       OPTIMAL SHIPMENT PLAN")
print_allocation(allocation)
print("\nTransportation Cost:",final_cost)