# Operations Research Toolkit

A graduate-level Python toolkit for operations research and industrial logistics optimization.

## Scope

The project combines:

- Linear programming with SciPy HiGHS and an educational primal simplex implementation.
- Transportation optimization using Northwest Corner, Least Cost, Vogel's Approximation Method (VAM), and MODI/transportation simplex optimization.
- Assignment optimization using the Hungarian algorithm.
- Scenario analysis and Monte Carlo demand simulation.
- Cost, utilization, and solution diagnostics.
- CSV-driven workflows and a command-line interface.
- Automated unit tests and reproducible example datasets.

The architecture is intentionally modular so that additional industrial models can be added without rewriting the core solvers.

> **Data note:** this release includes published Ahmedabad freight/industrial observations in addition to the original reproducible optimization examples. The published data are sourced from peer-reviewed/research reports and are explicitly marked by provenance. The original route-level monetary cost matrix remains a demonstration dataset because the cited public studies do not publish a complete observed route-cost matrix.

## Project structure

```text
operations_research_toolkit/
├── data/
│   ├── transportation_costs.csv
│   ├── assignment_costs.csv
│   ├── lp_scenario.csv
│   ├── ahmedabad_freight_observations.csv
│   ├── ahmedabad_industrial_clusters.csv
│   ├── ahmedabad_warehouse_clusters.csv
│   └── ahmedabad_data_provenance.md
├── examples/
│   └── run_all.py
├── src/or_toolkit/
│   ├── __init__.py
│   ├── cli.py
│   ├── optimization/
│   │   ├── __init__.py
│   │   ├── linear_programming.py
│   │   └── simplex.py
│   ├── transportation/
│   │   ├── __init__.py
│   │   ├── problem.py
│   │   ├── initial_solutions.py
│   │   └── modi.py
│   ├── assignment/
│   │   ├── __init__.py
│   │   └── hungarian.py
│   └── analytics/
│       ├── __init__.py
│       └── scenarios.py
├── tests/
├── requirements.txt
└── README.md
```

## Installation

Python 3.10+ is recommended.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the complete demonstration

```bash
python examples/run_all.py

# Analyze the published Ahmedabad observations
python examples/run_ahmedabad_real_data.py
```

## Command-line interface

```bash
python -m or_toolkit.cli lp
python -m or_toolkit.cli transportation
python -m or_toolkit.cli assignment
python -m or_toolkit.cli simulation
```

If using the `src` layout directly without installing the package:

```bash
# Windows PowerShell
$env:PYTHONPATH="src"
python examples/run_all.py

# Analyze the published Ahmedabad observations
python examples/run_ahmedabad_real_data.py

# Linux/macOS
export PYTHONPATH=src
python examples/run_all.py

# Analyze the published Ahmedabad observations
python examples/run_ahmedabad_real_data.py
```

## Research/academic extensions

The toolkit is suitable as a foundation for a master's-level project because it separates mathematical formulation, algorithms, diagnostics, scenario analysis, and reproducibility. For a dissertation or publication, document the actual industrial dataset, assumptions, data-cleaning process, model validation, sensitivity analysis, computational complexity, and managerial implications.

## Published Ahmedabad data sources

The real-data layer is based primarily on Swamy & Baindur (2014), *Managing urban freight transport in an expanding city — Case study of Ahmedabad*, Research in Transportation Business & Management, 11, DOI 10.1016/j.rtbm.2014.06.010, together with 2021 Ahmedabad property-tax figures reported in the *Planning Framework for Low Emission Zone (LEZ) In Core Areas of Indian Cities* report.

The source material reports, among other observations, approximately 34,182 freight vehicles/day crossing Ahmedabad's eight major entry/exit points in the baseline survey, an estimated 48,485 vehicles/day for 2012, more than 1,500 trucks/day attracted by the Vatva/Naroda/Odhav industrial estates, and 2,180/1,133/755 vehicles/day for Aslali/Sarkhej/Narol respectively. The later report gives approximately 135,025 industrial units and 39,000 transporter/warehouse properties in 2021. See `data/ahmedabad_data_provenance.md` for the full provenance record.
