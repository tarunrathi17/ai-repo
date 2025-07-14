import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from typing import TypedDict
from langgraph.graph import StateGraph

from nodes.get_datetime_node import get_datetime_node
from nodes.llm_router_node import llm_router_node

class State(TypedDict):
    user_input: str
    tool_name: str
    date: str
    time: str
    next: str

workflow = StateGraph(State)

workflow.add_node("router", llm_router_node)
workflow.add_node("get_datetime", get_datetime_node)

workflow.add_conditional_edges(
    "router",
    lambda state: state["next"],  # grab the tool name
    {
        "get_datetime": "get_datetime"
    }
)

workflow.set_entry_point("router")
app = workflow.compile()

output = app.invoke({"user_input": "what is the time right now?"})
print(output)
