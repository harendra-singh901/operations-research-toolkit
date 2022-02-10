import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from or_toolkit.transportation import TransportationProblem, northwest_corner, least_cost, vogel_approximation, modi_optimize


def problem():
    return TransportationProblem(
        np.array([[4, 7, 6], [5, 4, 7], [6, 5, 3]], dtype=float),
        np.array([20, 30, 25], dtype=float),
        np.array([25, 25, 25], dtype=float),
    )


def test_initial_solutions_feasible():
    p = problem()
    for solver in [northwest_corner, least_cost, vogel_approximation]:
        sol = solver(p)
        assert np.allclose(sol.allocation.sum(axis=1), p.supply)
        assert np.allclose(sol.allocation.sum(axis=0), p.demand)


def test_modi_not_worse_than_vam():
    p = problem()
    vam = vogel_approximation(p)
    opt = modi_optimize(p, vam)
    assert opt.total_cost <= vam.total_cost + 1e-7
