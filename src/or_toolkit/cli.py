"""Command-line entry point."""

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))


def main():
    parser = argparse.ArgumentParser(description="Operations Research Toolkit")
    parser.add_argument("module", choices=["lp", "transportation", "assignment", "simulation", "all"])
    args = parser.parse_args()
    from examples.run_all import main as run_all
    # The complete demonstration is deliberately used for each module in v1.0.
    # Individual module-specific entry points can be added without changing the solvers.
    run_all()


if __name__ == "__main__":
    main()
