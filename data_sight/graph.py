from typing import TypedDict
from langgraph.graph import StateGraph, END
from agents.data_inference import data_inference_agent

# Define state structure
class AppState(TypedDict):
    user_query: str
    sql_query: str
    csv_path: str
    plot_path: str
    inference: str  
    message: str


# Build LangGraph flow
workflow = StateGraph(AppState)
workflow.add_node("data_inference", data_inference_agent)
workflow.set_entry_point("data_inference")
workflow.set_finish_point("data_inference")

app = workflow.compile()
