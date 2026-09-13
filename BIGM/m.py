import numpy as np
 
M = 10**6
TOL = 1e-8
 
 
def big_m_simplex(c, A, b, signs, maximize=True):
    """Solve an LPP using the Big-M simplex method.
 
    c       : objective coefficients
    A       : constraint coefficient matrix
    b       : RHS values
    signs   : <=, >= or = for each constraint
    maximize: True for maximization, False for minimization
    """
    c = np.array(c, dtype=float)
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
 
    if not maximize:
        c = -c

    for i in range(len(b)):
        if b[i] < 0:
            A[i] *= -1
            b[i] *= -1
            if signs[i] == "<=":
                signs[i] = ">="
            elif signs[i] == ">=":
                signs[i] = "<="
 
    n = len(c)
    names = [f"x{i+1}" for i in range(n)]
    rows = [list(A[i]) for i in range(len(A))]
    basis = [None] * len(A)
    cb = [0.0] * len(A)
    c_extended = list(c)

    for i, sign in enumerate(signs):
        if sign == "<=":
            name = f"s{i+1}"
            for row in rows:
                row.append(0.0)
            rows[i][-1] = 1.0
            names.append(name)
            c_extended.append(0.0)
            basis[i] = len(names) - 1
            cb[i] = 0.0
 
        elif sign == ">=":
            name = f"s{i+1}"
            for row in rows:
                row.append(0.0)
            rows[i][-1] = -1.0
            names.append(name)
            c_extended.append(0.0)

            name = f"A{i+1}"
            for row in rows:
                row.append(0.0)
            rows[i][-1] = 1.0
            names.append(name)
            c_extended.append(-M)
            basis[i] = len(names) - 1
            cb[i] = -M
 
        elif sign == "=":
            name = f"A{i+1}"
            for row in rows:
                row.append(0.0)
            rows[i][-1] = 1.0
            names.append(name)
            c_extended.append(-M)
            basis[i] = len(names) - 1
            cb[i] = -M
        else:
            raise ValueError("Constraint sign must be <=, >= or =")
 
    T = np.array(rows, dtype=float)
    rhs = b.reshape(-1, 1)
 
    print("\nVariables:", names)
    print("Initial basis:", [names[j] for j in basis])
 
    iteration = 0
    while iteration < 100:
        iteration += 1
 
        zj = np.array(cb) @ T
        cj_zj = np.array(c_extended) - zj
 
        print(f"\nIteration {iteration}")
        print("Basis:", [names[j] for j in basis])
        print("Cj-Zj:", [round(float(v), 4) for v in cj_zj])
        print("RHS:", [round(float(v), 4) for v in rhs[:, 0]])
 
        entering_candidates = [
            j for j in range(len(names)) if cj_zj[j] > TOL
        ]
 
        if not entering_candidates:
            break
 
        entering = max(entering_candidates, key=lambda j: cj_zj[j])
 
        ratios = []
        for i in range(len(b)):
            if T[i, entering] > TOL:
                ratios.append((rhs[i, 0] / T[i, entering], i))
 
        if not ratios:
            raise ValueError("LPP is unbounded.")
 
        _, leaving_row = min(ratios)
        pivot = T[leaving_row, entering]
 
        print(
            f"Entering: {names[entering]}, "
            f"Leaving: {names[basis[leaving_row]]}, "
            f"Pivot: {pivot:.6g}"
        )

        T[leaving_row] /= pivot
        rhs[leaving_row] /= pivot
 
        for i in range(len(b)):
            if i != leaving_row:
                factor = T[i, entering]
                T[i] -= factor * T[leaving_row]
                rhs[i] -= factor * rhs[leaving_row]
 
        basis[leaving_row] = entering
        cb[leaving_row] = c_extended[entering]

    solution = np.zeros(len(names))
    for i, j in enumerate(basis):
        solution[j] = rhs[i, 0]
 
    artificial_values = [
        solution[j] for j, name in enumerate(names)
        if name.startswith("A")
    ]
 
    if any(v > 1e-6 for v in artificial_values):
        print("\nNo feasible solution: an artificial variable remains positive.")
        return None
 
    z_for_max_problem = np.dot(c, solution[:n])
    z_original = z_for_max_problem if maximize else -z_for_max_problem
 
    print("\nOptimal solution")
    for i in range(n):
        print(f"x{i+1} = {solution[i]:.6f}")
    print(f"Optimal objective value = {z_original:.6f}")
 
    return solution[:n], z_original
 
 
if __name__ == "__main__":

    c = [3, 5]
    A = [[2, 1], [1, 2]]
    b = [8, 6]
    signs = ["<=", ">="]
 
    big_m_simplex(c, A, b, signs, maximize=True)
