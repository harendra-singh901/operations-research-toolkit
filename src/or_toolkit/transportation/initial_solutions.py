"""Classical transportation initial-feasible-solution heuristics."""

import numpy as np
from .problem import TransportationProblem, TransportationSolution, total_cost


def _finalize(problem, x, method):
    return TransportationSolution(x, total_cost(problem, x), method)


def northwest_corner(problem: TransportationProblem):
    supply = problem.supply.copy()
    demand = problem.demand.copy()
    x = np.zeros(problem.shape)
    i = j = 0
    while i < len(supply) and j < len(demand):
        amount = min(supply[i], demand[j])
        x[i, j] = amount
        supply[i] -= amount
        demand[j] -= amount
        if np.isclose(supply[i], 0):
            i += 1
        if np.isclose(demand[j], 0):
            j += 1
    return _finalize(problem, x, "Northwest Corner")


def least_cost(problem: TransportationProblem):
    supply = problem.supply.copy()
    demand = problem.demand.copy()
    x = np.zeros(problem.shape)
    active_rows = set(range(len(supply)))
    active_cols = set(range(len(demand)))
    while active_rows and active_cols:
        candidates = [(problem.costs[i, j], i, j) for i in active_rows for j in active_cols]
        _, i, j = min(candidates)
        amount = min(supply[i], demand[j])
        x[i, j] = amount
        supply[i] -= amount
        demand[j] -= amount
        if np.isclose(supply[i], 0):
            active_rows.remove(i)
        if np.isclose(demand[j], 0):
            active_cols.remove(j)
    return _finalize(problem, x, "Least Cost")


def vogel_approximation(problem: TransportationProblem):
    supply = problem.supply.copy()
    demand = problem.demand.copy()
    x = np.zeros(problem.shape)
    active_rows = set(range(len(supply)))
    active_cols = set(range(len(demand)))

    while active_rows and active_cols:
        row_penalties = {}
        col_penalties = {}
        for i in active_rows:
            vals = sorted(problem.costs[i, j] for j in active_cols)
            row_penalties[i] = vals[1] - vals[0] if len(vals) > 1 else vals[0]
        for j in active_cols:
            vals = sorted(problem.costs[i, j] for i in active_rows)
            col_penalties[j] = vals[1] - vals[0] if len(vals) > 1 else vals[0]

        best_row = max(row_penalties.items(), key=lambda kv: (kv[1], -kv[0])) if row_penalties else (-1, -1)
        best_col = max(col_penalties.items(), key=lambda kv: (kv[1], -kv[0])) if col_penalties else (-1, -1)

        if best_row[1] >= best_col[1]:
            i = best_row[0]
            j = min(active_cols, key=lambda col: (problem.costs[i, col], col))
        else:
            j = best_col[0]
            i = min(active_rows, key=lambda row: (problem.costs[row, j], row))

        amount = min(supply[i], demand[j])
        x[i, j] = amount
        supply[i] -= amount
        demand[j] -= amount
        if np.isclose(supply[i], 0):
            active_rows.remove(i)
        if np.isclose(demand[j], 0):
            active_cols.remove(j)

    return _finalize(problem, x, "Vogel's Approximation Method")
