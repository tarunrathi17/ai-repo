def orchestrator(user_query: str):
    user_query = user_query.lower()

    if "graph" in user_query and "salary" in user_query:
        return {
            "action": "Visualize",
            "inference": "User requested a bar chart of employee salaries.",
            "input": None
        }

    if "name" in user_query and "id" in user_query:
        return {
            "action": "InferSQL",
            "inference": "User wants to view employee names with their IDs.",
            "input": user_query
        }
    
    if "name" in user_query and "address" in user_query:
        return {
        "action": "InferSQL",
        "inference": "User wants to view employee names with their addresses.",
        "input": user_query
    }


    if "name" in user_query and "salary" in user_query:
        return {
            "action": "InferSQL",
            "inference": "User wants to view employee names with their salaries.",
            "input": user_query
        }

    if "name" in user_query and "department" in user_query:
        return {
            "action": "InferSQL",
            "inference": "User wants to view employee names with their departments.",
            "input": user_query
        }

    if "average salary" in user_query:
        return {
            "action": "InferSQL",
            "inference": "User wants to see average salary by department.",
            "input": user_query
        }

    if "hr" in user_query:
        return {
            "action": "InferSQL",
            "inference": "User wants to see employees in the HR department.",
            "input": user_query
        }

    return {
        "action": "InferSQL",
        "inference": "User wants to view all employee records.",
        "input": user_query
    }
