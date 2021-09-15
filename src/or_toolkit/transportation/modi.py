"""MODI (u-v) optimization for balanced transportation problems."""

import numpy as np
from .problem import TransportationProblem, TransportationSolution, total_cost


def _basis_from_allocation(x, tol=1e-9):
    return {(i, j) for i in range(x.shape[0]) for j in range(x.shape[1]) if x[i, j] > tol}


def _ensure_basis(problem, x):
    """Add zero basic cells until there are m+n-1 independent basic cells."""
    m, n = x.shape
    basis = _basis_from_allocation(x)
    target = m + n - 1
    parent = list(range(m + n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra
            return True
        return False

    # Rebuild an acyclic basis first.
    clean = set()
    for i, j in sorted(basis):
        if union(i, m + j):
            clean.add((i, j))

    for i in range(m):
        for j in range(n):
            if len(clean) >= target:
                break
            if (i, j) not in clean and union(i, m + j):
                clean.add((i, j))
    return clean


def _potentials(costs, basis):
    m, n = costs.shape
    u = np.full(m, np.nan)
    v = np.full(n, np.nan)
    u[0] = 0.0
    changed = True
    while changed:
        changed = False
        for i, j in basis:
            if not np.isnan(u[i]) and np.isnan(v[j]):
                v[j] = costs[i, j] - u[i]
                changed = True
            elif np.isnan(u[i]) and not np.isnan(v[j]):
                u[i] = costs[i, j] - v[j]
                changed = True
    # A disconnected degenerate basis is repaired by zero-filling unresolved potentials.
    u[np.isnan(u)] = 0.0
    v[np.isnan(v)] = 0.0
    return u, v


def _cycle_from_entering(basis, entering, shape):
    """Find a closed alternating cycle through an entering cell."""
    m, n = shape
    row_to_cols = {i: [] for i in range(m)}
    col_to_rows = {j: [] for j in range(n)}
    for i, j in basis:
        row_to_cols[i].append(j)
        col_to_rows[j].append(i)

    start = entering
    path = [start]

    def dfs(cell, move_row):
        i, j = cell
        if move_row:
            candidates = [(i, jj) for jj in row_to_cols[i]]
            if i == start[0] and len(path) >= 4:
                candidates.append(start)
        else:
            candidates = [(ii, j) for ii in col_to_rows[j]]
            if j == start[1] and len(path) >= 4:
                candidates.append(start)

        for nxt in candidates:
            if nxt == start and len(path) >= 4:
                return path + [start]
            if nxt in path:
                continue
            path.append(nxt)
            result = dfs(nxt, not move_row)
            if result:
                return result
            path.pop()
        return None

    return dfs(start, True) or dfs(start, False)


def modi_optimize(problem: TransportationProblem, initial=None, max_iter=1000, tol=1e-9):
    if initial is None:
        from .initial_solutions import vogel_approximation
        initial = vogel_approximation(problem)
    x = np.array(initial.allocation, dtype=float, copy=True)
    basis = _ensure_basis(problem, x)

    for iteration in range(max_iter):
        u, v = _potentials(problem.costs, basis)
        reduced = problem.costs - u[:, None] - v[None, :]
        for i, j in basis:
            reduced[i, j] = 0.0
        entering_candidates = [(reduced[i, j], i, j) for i in range(x.shape[0]) for j in range(x.shape[1]) if (i, j) not in basis]
        entering = min(entering_candidates, default=(0.0, -1, -1))
        if entering[0] >= -tol:
            return TransportationSolution(x, total_cost(problem, x), "MODI", iteration, reduced, u, v)

        _, ei, ej = entering
        cycle = _cycle_from_entering(basis, (ei, ej), x.shape)
        if not cycle:
            raise RuntimeError("Could not construct a transportation pivot cycle; check degeneracy.")

        minus_cells = cycle[1:-1:2]
        theta = min(x[i, j] for i, j in minus_cells)
        for k, (i, j) in enumerate(cycle[:-1]):
            x[i, j] += theta if k % 2 == 0 else -theta
        basis.add((ei, ej))
        # Remove one zero-valued minus cell to preserve m+n-1 basis size.
        zero_candidates = [(i, j) for i, j in minus_cells if np.isclose(x[i, j], 0.0, atol=tol)]
        if zero_candidates:
            basis.remove(zero_candidates[0])

    raise RuntimeError("MODI iteration limit reached")
