"""Educational primal simplex implementation for max problems.

Model form supported:
    maximize c^T x
    subject to A x <= b, x >= 0

The implementation uses a tableau with slack variables. It is intended for
transparent educational/research demonstrations and small models; production
models should use a mature LP solver such as HiGHS through SciPy.
"""

from dataclasses import dataclass
import numpy as np


@dataclass
class SimplexResult:
    status: str
    x: np.ndarray
    objective: float
    iterations: int
    tableau: np.ndarray
    message: str


def primal_simplex_max(c, A, b, tol=1e-9, max_iter=10_000):
    c = np.asarray(c, dtype=float)
    A = np.asarray(A, dtype=float)
    b = np.asarray(b, dtype=float)
    if A.ndim != 2 or c.ndim != 1 or b.ndim != 1:
        raise ValueError("c, A and b must be one- or two-dimensional arrays")
    if A.shape[0] != b.size or A.shape[1] != c.size:
        raise ValueError("Dimension mismatch between A, b and c")
    if np.any(b < -tol):
        raise ValueError("This educational implementation requires b >= 0")

    m, n = A.shape
    tableau = np.zeros((m + 1, n + m + 1), dtype=float)
    tableau[:m, :n] = A
    tableau[:m, n:n + m] = np.eye(m)
    tableau[:m, -1] = b
    tableau[-1, :n] = -c

    basis = list(range(n, n + m))

    for iteration in range(max_iter):
        reduced = tableau[-1, :-1]
        entering_candidates = np.where(reduced < -tol)[0]
        if entering_candidates.size == 0:
            x = np.zeros(n)
            for row, col in enumerate(basis):
                if col < n:
                    x[col] = tableau[row, -1]
            return SimplexResult(
                "optimal", x, float(c @ x), iteration, tableau.copy(),
                "Optimal basic feasible solution found."
            )

        entering = int(entering_candidates[0])
        column = tableau[:m, entering]
        positive = column > tol
        if not np.any(positive):
            return SimplexResult(
                "unbounded", np.zeros(n), float("inf"), iteration,
                tableau.copy(), "Objective is unbounded in the selected direction."
            )

        ratios = np.full(m, np.inf)
        ratios[positive] = tableau[:m, -1][positive] / column[positive]
        leaving = int(np.argmin(ratios))
        pivot = tableau[leaving, entering]
        tableau[leaving, :] /= pivot
        for r in range(m + 1):
            if r != leaving:
                tableau[r, :] -= tableau[r, entering] * tableau[leaving, :]
        basis[leaving] = entering

    raise RuntimeError("Simplex iteration limit reached; inspect the model for cycling/degeneracy.")
