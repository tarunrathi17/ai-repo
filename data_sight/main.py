from graph import app  # your compiled LangGraph app

def run_session():
    print("Hello, Welcome to the Smart Sales Agent!")
    print("Type 'exit' or 'quit' to end the session.\n")

    while True:
        user_query = input(" Ask your query: ").strip()

        # Exit condition
        if user_query.lower() in ("exit", "quit"):
            print(" Goodbye!")
            break

        # Build initial state
        initial_state = {
            "user_query": user_query
        }

        # Run LangGraph app
        final_state = app.invoke(initial_state)

        # Print final state (excluding inference)
        print("\n Final Output:")
        for key, value in final_state.items():
            if key != "inference":
                print(f"{key}: {value}")

        # Print inference nicely
        if "inference" in final_state:
            print("\n Inference:")
            print(final_state["inference"])

        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    run_session()
