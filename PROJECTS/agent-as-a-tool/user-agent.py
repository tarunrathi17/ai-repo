# main_agent.py

import os
import sys
from langchain.agents import initialize_agent, AgentType
from langchain_community.llms import Ollama
from helper_tool import helper_summarizer_tool

def read_text_file(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# Setup LLM (Switch to faster model if needed)
llm = Ollama(model="llama3.2:1b", base_url="http://localhost:11434")

# Initialize Agent with tool
agent_executor = initialize_agent(
    tools=[helper_summarizer_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # Ensures tool usage by name
    verbose=True  # Debug output: shows tool calls and steps
)

# Run Agent
if __name__ == "__main__":
    file_path = "C:/Users/91827/Desktop/ai/PROJECTS/agent-as-a-tool/textfile.txt"
    text = read_text_file(file_path)

    # Force tool routing with explicit instruction
    query = f"Use the HelperSummarizerAgent tool to summarize this text:\n\n{text}"
    
    try:
        result = agent_executor.run(query)
        print("\n=== SUMMARY ===\n")
        print(result)
    except Exception as e:
        print("Agent failed:", e)
        sys.exit(1)
    
    sys.exit(0)
