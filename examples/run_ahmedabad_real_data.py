"""Analyze the published Ahmedabad freight observations bundled with the toolkit."""
from pathlib import Path
import sys
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

DATA = ROOT / "data"
OUT = ROOT / "results" / "ahmedabad"
OUT.mkdir(parents=True, exist_ok=True)


def main():
    observations = pd.read_csv(DATA / "ahmedabad_freight_observations.csv")
    clusters = pd.read_csv(DATA / "ahmedabad_industrial_clusters.csv")
    warehouses = pd.read_csv(DATA / "ahmedabad_warehouse_clusters.csv")

    # Save a clean analytical extract.
    observations.to_csv(OUT / "published_freight_observations_used.csv", index=False)

    warehouse_plot = warehouses[warehouses["cluster"] != "Total"].copy()
    ax = warehouse_plot.plot(
        x="cluster", y="vehicles_per_day", kind="bar", legend=False,
        title="Published Ahmedabad Warehouse/Transport Cluster Freight Flow"
    )
    ax.set_xlabel("Cluster")
    ax.set_ylabel("Vehicles per day")
    plt.tight_layout()
    plt.savefig(OUT / "warehouse_cluster_freight_flow.png", dpi=220)
    plt.close()

    industrial_plot = clusters[clusters["cluster"].isin(["Vatva", "Naroda"])].copy()
    ax = industrial_plot.plot(
        x="cluster", y="trucks_per_day", kind="bar", legend=False,
        title="Published Truck Flow for Ahmedabad Industrial Clusters"
    )
    ax.set_xlabel("Industrial cluster")
    ax.set_ylabel("Trucks per day")
    plt.tight_layout()
    plt.savefig(OUT / "industrial_cluster_truck_flow.png", dpi=220)
    plt.close()

    summary = pd.DataFrame([
        {"metric": "Cordon freight vehicles/day (2006 baseline)", "value": 34182},
        {"metric": "Estimated freight vehicles/day (2012)", "value": 48485},
        {"metric": "Industrial units (2021)", "value": 135025},
        {"metric": "Vatva/Odhav/Naroda units (2021)", "value": 8700},
        {"metric": "Transport/warehouse properties (2021)", "value": 39000},
        {"metric": "Vatva/Naroda/Odhav trucks/day (study period)", "value": 1500},
        {"metric": "Aslali/Sarkhej/Narol vehicles/day (study period)", "value": 4313},
    ])
    summary.to_csv(OUT / "ahmedabad_real_data_summary.csv", index=False)

    print("Ahmedabad published-data analysis completed.")
    print(summary.to_string(index=False))
    print(f"Outputs written to: {OUT}")


if __name__ == "__main__":
    main()
