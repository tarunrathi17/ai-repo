from orchestratoragent import orchestrator
from datainferenceagent import infer_sql
from visualizeragentt import visualize_salary_bar_chart

def run_session():
    print("Welcome to Employee Query Agent (type 'exit' to quit)\n")
    
    while True:
        user_query = input("Enter your query: ").strip()
        
        if user_query.lower() in ["exit", "quit"]:
            print("Session ended. Goodbye!")
            break

        response = orchestrator(user_query)

        if response["action"] == "InferSQL":
            result = infer_sql(response["input"])
            print("\nSQL Query:\n", result["sql_query"])
            print("CSV saved at:", result["csv_path"])
            print("\nQuery Results:\n", result["dataframe"])

        elif response["action"] == "Visualize":
            chart_path = visualize_salary_bar_chart()
            print(f"\nChart saved at: {chart_path}")

        print("\n────────────────────────────────────────────\n")

if __name__ == "__main__":
    run_session()
