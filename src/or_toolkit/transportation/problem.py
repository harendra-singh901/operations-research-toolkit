"""Transportation problem data model and feasibility helpers."""

from dataclasses import dataclass, field
import numpy as np


@dataclass
class TransportationProblem:
    costs: np.ndarray
    supply: np.ndarray
    demand: np.ndarray
    origins: list[str] = field(default_factory=list)
    destinations: list[str] = field(default_factory=list)

    def __post_init__(self):
        self.costs = np.asarray(self.costs, dtype=float)
        self.supply = np.asarray(self.supply, dtype=float)
        self.demand = np.asarray(self.demand, dtype=float)
        if self.costs.shape != (len(self.supply), len(self.demand)):
            raise ValueError("Cost matrix dimensions must match supply and demand")
        if np.any(self.costs < 0) or np.any(self.supply < 0) or np.any(self.demand < 0):
            raise ValueError("Costs, supply and demand must be non-negative")
        if not np.isclose(self.supply.sum(), self.demand.sum()):
            raise ValueError("Problem must be balanced; balance it before solving")
        if not self.origins:
            self.origins = [f"Origin_{i+1}" for i in range(len(self.supply))]
        if not self.destinations:
            self.destinations = [f"Destination_{j+1}" for j in range(len(self.demand))]

    @property
    def shape(self):
        return self.costs.shape


@dataclass
class TransportationSolution:
    allocation: np.ndarray
    total_cost: float
    method: str
    iterations: int = 0
    reduced_costs: np.ndarray | None = None
    potentials_u: np.ndarray | None = None
    potentials_v: np.ndarray | None = None

    def route_utilization(self):
        return self.allocation / np.maximum(self.allocation.sum(axis=1, keepdims=True), 1e-12)


def total_cost(problem: TransportationProblem, allocation):
    allocation = np.asarray(allocation, dtype=float)
    if allocation.shape != problem.costs.shape:
        raise ValueError("Allocation shape does not match cost matrix")
    return float(np.sum(problem.costs * allocation))


def validate_allocation(problem: TransportationProblem, allocation, tol=1e-7):
    x = np.asarray(allocation, dtype=float)
    return {
        "nonnegative": bool(np.all(x >= -tol)),
        "supply_satisfied": bool(np.allclose(x.sum(axis=1), problem.supply, atol=tol)),
        "demand_satisfied": bool(np.allclose(x.sum(axis=0), problem.demand, atol=tol)),
    }
