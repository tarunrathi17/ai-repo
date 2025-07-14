
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_community.llms import Ollama

llm = Ollama(model="llama3.2:1b")

prompt = PromptTemplate.from_template("""
You are a strict tool router.

Choose one tool to respond to the user's input. Available tools:
- get_datetime

ONLY respond with one tool name. No explanation. No formatting. No code.

User input: {user_input}

Tool name (only): 
""")

def llm_router_node(state: dict) -> dict:
    chain = prompt | llm | RunnableLambda(lambda x: x.strip().lower())

    tool_name = chain.invoke({"user_input": state["user_input"]}).strip().lower()
    
    # 🧹 Filter out anything extra
    if "get_datetime" in tool_name:
        tool_name = "get_datetime"
    else:
        tool_name = "error"  # (optional) fallback or error handling

    print("Router chose:", tool_name)
    return {"next": tool_name}
