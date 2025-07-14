def orchestrator(user_query):
    if "graph" in user_query.lower():
        return {"action": "Visualize", "input": user_query}
    else:
        return {"action": "InferSQL", "input": user_query}
