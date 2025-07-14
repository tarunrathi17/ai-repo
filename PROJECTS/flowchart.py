from langgraph.graph import StateGraph
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.llms import Ollama
from typing import TypedDict, Optional
import re
import json
import logging
import time

logging.getLogger().setLevel(logging.ERROR)

# Tools
def add_numbers_tool(input_text: str) -> str:
    matches = re.findall(r"[-+]?\d*\.\d+|\d+", input_text)
    if len(matches) >= 2:
        return str(float(matches[0]) + float(matches[1]))
    return "Please provide two numbers to add."

wiki_tool = WikipediaAPIWrapper()

tools = {
    "Calculator": add_numbers_tool,
    "Wikipedia": wiki_tool.run,
}

# LLM
llm = Ollama(model="llama3.2:3b")

# LangGraph State
class AgentState(TypedDict):  #structured state for langgraph.
    input: str
    agent_out: Optional[str]

# Agent Node
def run_agent_node(state: AgentState) -> AgentState:
    print("\n[Agent Node Running]")
    print(f"Input: {state['input']}")

    try:
        start = time.time()
        prompt = f"""You are an intelligent agent. Decide what tool to use.

Available tools:
- Calculator: use for adding two numbers
- Wikipedia: use for general knowledge

Input: {state['input']}

Output format:
Action:
{{
  "action": "ToolName",
  "action_input": "Input for tool"
}}"""

        output = llm(prompt)
        print(f"\nLLM Output:\n{output.strip()}")

        # Extract tool call
        match = re.search(r"Action:\s*({.*})", output, re.DOTALL)
        if not match:
            raise ValueError("Could not parse action block.")

        action_data = json.loads(match.group(1))
        tool_name = action_data["action"]
        tool_input = action_data["action_input"]

        if tool_name not in tools:
            raise ValueError(f"Unknown tool: {tool_name}")

        tool_func = tools[tool_name]
        observation = tool_func(tool_input)

        print("\nFlowchart Output:")
        print("   ↓")
        print(f"Tool: {tool_name}")
        print(f"   ↳ Input: {tool_input}")
        print(f"   ↳ Output: {observation}")
        print("   ↓")
        print(f"Final Answer: {observation}")
        print(f"Took: {time.time() - start:.2f}s")

        with open("agent_trace.log", "w") as f:
            f.write(f"Tool: {tool_name}\nInput: {tool_input}\nOutput: {observation}\n")

        return {"input": state["input"], "agent_out": observation}

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"input": state["input"], "agent_out": "Failed to process your input."}

# Build LangGraph
builder = StateGraph(AgentState)
builder.add_node("agent", run_agent_node)
builder.set_entry_point("agent")
builder.set_finish_point("agent")
graph = builder.compile()

# CLI Entry
if __name__ == "__main__":
    try:
        print("Welcome to the LangGraph Agent!")
        print("Try: 'Add 4.5 and 6.7' or 'Tell me about Mars'")
        user_input = input("Your question: ").strip()

        if user_input:
            result = graph.invoke({"input": user_input})
            print(f"\nFinal Output: {result['agent_out']}")
        else:
            print("Empty input. Try again.")

    except KeyboardInterrupt:
        print("\n Goodbye!")
