import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from or_toolkit.assignment import solve_assignment


def test_assignment():
    result = solve_assignment([[4, 1, 3], [2, 0, 5], [3, 2, 2]])
    assert result.total_cost == 5
    assert len(result.assignment) == 3
