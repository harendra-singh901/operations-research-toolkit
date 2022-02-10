import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from or_toolkit.optimization import LinearProgram, solve_linear_program, primal_simplex_max


def test_lp_matches_simplex():
    model = LinearProgram("test", [40, 55], [[2, 1], [1, 3]], [100, 120], [(0, None), (0, None)], True)
    result = solve_linear_program(model)
    simplex = primal_simplex_max(model.objective, model.A_ub, model.b_ub)
    assert result.success
    assert np.allclose(result.x, simplex.x, atol=1e-7)
    assert np.isclose(result.objective_original, simplex.objective, atol=1e-7)
