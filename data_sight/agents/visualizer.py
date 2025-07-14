import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

def visualizer_agent(state):
    print("[VisualizerAgent] Generating plot...")

    if not os.path.exists(state["csv_path"]):
        raise FileNotFoundError(f"CSV file not found at {state['csv_path']}")

    df = pd.read_csv(state["csv_path"])
    sns.set(style="whitegrid")

    plt.figure(figsize=(10, 6))
    sns.barplot(x="state", y="sales", hue="region", data=df)

    plt.title("Sales by State and Region")
    plt.xlabel("State")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()

    os.makedirs("output", exist_ok=True)
    plot_path = "output/sales_plot.png"
    plt.savefig(plot_path)
    plt.close()

    return {"plot_path": plot_path}
