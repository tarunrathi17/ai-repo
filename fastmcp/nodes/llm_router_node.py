# nodes/llm_router_node.py

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_community.llms import Ollama

llm = Ollama(model="llama3.2:3b")  # Or use OpenAI(model="gpt-4")

prompt = PromptTemplate.from_template("""
You are a router. Based on the user input, decide which tool to call.

Available tools:
- get_datetime: Use when the user asks for date or time.

User input: {user_input}
Tool to call (just return the name): 
""")

def llm_router_node(state: dict) -> str:
    chain = prompt | llm | RunnableLambda(lambda x: x.strip())
    tool_name = chain.invoke({"user_input": state["user_input"]})
    return tool_name
