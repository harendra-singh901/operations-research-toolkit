"""Scenario and uncertainty analysis utilities."""

import numpy as np
import pandas as pd


def monte_carlo_demand(base_demand, cv=0.15, simulations=5000, seed=42):
    """Generate non-negative demand scenarios using a lognormal distribution."""
    base = np.asarray(base_demand, dtype=float)
    if np.any(base < 0) or cv < 0 or simulations < 1:
        raise ValueError("Demand, CV and simulations must be valid non-negative values")
    rng = np.random.default_rng(seed)
    sigma = np.sqrt(np.log1p(cv ** 2))
    mu = np.log(np.maximum(base, 1e-12)) - 0.5 * sigma ** 2
    draws = rng.lognormal(mean=mu, sigma=sigma, size=(simulations, base.size))
    return draws


def transportation_sensitivity(problem, allocations, cost_multiplier=1.0):
    rows = []
    for name, allocation in allocations.items():
        cost = float(np.sum(problem.costs * allocation * cost_multiplier))
        rows.append({"scenario": name, "cost": cost})
    return pd.DataFrame(rows).sort_values("cost").reset_index(drop=True)
