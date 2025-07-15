from orchestratoragent import orchestrator
from datainferenceagent import infer_sql
from visualizeragentt import visualize_salary_bar_chart
import pandas as pd
import json
import os

# In-memory session memory
session_memory = []

def run_session():
    print(" Welcome to Employee Query Agent (type 'exit' to quit, 'history' to see memory)\n")

    while True:
        user_query = input("Enter your query: ").strip()

        if user_query.lower() in ["exit", "quit"]:
            print(" Session ended. Goodbye!")
            break

        if user_query.lower() == "history":
            print(f"\n Session History ({len(session_memory)} entries):")

            for i, entry in enumerate(session_memory, 1):
                print(f"\n{i}. QUERY: {entry['query']}")
                print(f"   INFERENCE: {entry['inference']}")
                print(f"   SQL: {entry['sql_query']}")
                print("   RESPONSE:")
                df = pd.DataFrame(entry['response'])
                print(df.to_string(index=False))

            print("\n─────────────────────────────\n")
            continue

        response = orchestrator(user_query)

        if response["action"] == "InferSQL":
            result = infer_sql(response["input"])

            # Store session entry
            session_memory.append({
                "query": user_query,
                "inference": response["inference"],
                "sql_query": result["sql_query"],
                "response": result["dataframe"].to_dict(orient="records")
            })

            print("\n Inference:", response["inference"])
            print(" SQL Query:\n", result["sql_query"])
            print("\n Query Result:\n", result["dataframe"])
            print(" CSV saved at:", result["csv_path"])

        elif response["action"] == "Visualize":
            chart_path = visualize_salary_bar_chart()
            print(" Bar Chart saved at:", chart_path)

        print("\n─────────────────────────────\n")

def save_session_memory():
    os.makedirs("output", exist_ok=True)
    with open("output/session_memory.json", "w") as f:
        json.dump(session_memory, f, indent=2)
    print(" Session memory saved to output/session_memory.json")

if __name__ == "__main__":
    try:
        run_session()
    finally:
        save_session_memory()
