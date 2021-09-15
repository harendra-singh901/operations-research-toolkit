"""Assignment optimization using SciPy's exact linear-sum assignment solver."""

from dataclasses import dataclass
import numpy as np
from scipy.optimize import linear_sum_assignment


@dataclass
class AssignmentResult:
    row_indices: np.ndarray
    col_indices: np.ndarray
    total_cost: float
    assignment: dict


def solve_assignment(cost_matrix, row_labels=None, col_labels=None):
    costs = np.asarray(cost_matrix, dtype=float)
    if costs.ndim != 2:
        raise ValueError("Cost matrix must be two-dimensional")
    rows, cols = linear_sum_assignment(costs)
    assignment = {
        (row_labels[i] if row_labels else i): (col_labels[j] if col_labels else j)
        for i, j in zip(rows, cols)
    }
    return AssignmentResult(rows, cols, float(costs[rows, cols].sum()), assignment)
