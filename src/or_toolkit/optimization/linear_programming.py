"""Linear programming formulation, solving, validation and diagnostics."""

from dataclasses import dataclass
from typing import Sequence
import numpy as np
from scipy.optimize import linprog


@dataclass
class LinearProgram:
    name: str
    objective: Sequence[float]
    A_ub: Sequence[Sequence[float]]
    b_ub: Sequence[float]
    bounds: Sequence[tuple]
    maximize: bool = True


def solve_linear_program(model: LinearProgram):
    c = np.asarray(model.objective, dtype=float)
    scipy_c = -c if model.maximize else c
    result = linprog(
        scipy_c,
        A_ub=np.asarray(model.A_ub, dtype=float),
        b_ub=np.asarray(model.b_ub, dtype=float),
        bounds=list(model.bounds),
        method="highs",
    )
    if result.success:
        result.objective_original = float(c @ result.x)
    else:
        result.objective_original = None
    return result


def constraint_report(model: LinearProgram, x):
    A = np.asarray(model.A_ub, dtype=float)
    b = np.asarray(model.b_ub, dtype=float)
    lhs = A @ np.asarray(x, dtype=float)
    slack = b - lhs
    return {
        "lhs": lhs,
        "rhs": b,
        "slack": slack,
        "binding": np.isclose(slack, 0.0, atol=1e-7),
    }
