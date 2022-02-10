"""End-to-end demonstration of the toolkit."""

from pathlib import Path
import sys
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from or_toolkit.optimization import LinearProgram, solve_linear_program, primal_simplex_max
from or_toolkit.transportation import TransportationProblem, northwest_corner, least_cost, vogel_approximation, modi_optimize
from or_toolkit.assignment import solve_assignment
from or_toolkit.analytics import monte_carlo_demand


def load_transportation():
    raw = pd.read_csv(ROOT / "data" / "transportation_costs.csv")
    costs = raw.iloc[:-1, 1:-1].to_numpy(dtype=float)
    supply = raw["supply"].iloc[:-1].to_numpy(dtype=float)
    demand = raw.iloc[-1, 1:-1].to_numpy(dtype=float)
    origins = raw["origin"].iloc[:-1].tolist()
    destinations = raw.columns[1:-1].tolist()
    return TransportationProblem(costs, supply, demand, origins, destinations)


def main():
    print("=" * 72)
    print("OPERATIONS RESEARCH TOOLKIT — END-TO-END DEMONSTRATION")
    print("=" * 72)

    model = LinearProgram(
        name="Industrial production mix",
        objective=[40, 55, 30],
        A_ub=[[2, 1, 2], [1, 3, 2]],
        b_ub=[100, 120],
        bounds=[(0, None)] * 3,
        maximize=True,
    )
    lp = solve_linear_program(model)
    simplex = primal_simplex_max(model.objective, model.A_ub, model.b_ub)
    print("\n[1] LINEAR PROGRAMMING")
    print("HiGHS status:", lp.message)
    print("HiGHS x:", np.round(lp.x, 4))
    print("HiGHS objective:", round(lp.objective_original, 4))
    print("Educational simplex x:", np.round(simplex.x, 4))
    print("Educational simplex objective:", round(simplex.objective, 4))

    tp = load_transportation()
    print("\n[2] TRANSPORTATION PROBLEM")
    initial = {
        "Northwest Corner": northwest_corner(tp),
        "Least Cost": least_cost(tp),
        "VAM": vogel_approximation(tp),
    }
    for name, sol in initial.items():
        print(f"{name:20s}: cost = {sol.total_cost:,.2f}")
    optimized = modi_optimize(tp, initial["VAM"])
    print(f"{'MODI optimum':20s}: cost = {optimized.total_cost:,.2f}")
    print("Allocation matrix:\n", optimized.allocation)

    print("\n[3] ASSIGNMENT PROBLEM")
    assignment_df = pd.read_csv(ROOT / "data" / "assignment_costs.csv")
    result = solve_assignment(
        assignment_df.iloc[:, 1:].to_numpy(),
        assignment_df.iloc[:, 0].tolist(),
        assignment_df.columns[1:].tolist(),
    )
    print("Assignment:", result.assignment)
    print("Minimum total cost:", result.total_cost)

    print("\n[4] UNCERTAINTY / SCENARIO ANALYSIS")
    scenarios = monte_carlo_demand(tp.demand, cv=0.15, simulations=5000, seed=2026)
    totals = scenarios.sum(axis=1)
    print("Expected total simulated demand:", round(float(totals.mean()), 2))
    print("P90 total demand:", round(float(np.quantile(totals, 0.90)), 2))
    print("P95 total demand:", round(float(np.quantile(totals, 0.95)), 2))
    print("\nCompleted successfully.")


if __name__ == "__main__":
    main()
