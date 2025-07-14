from langchain.agents import initialize_agent, AgentType
from langchain_community.llms import Ollama
from langchain.chains.summarize import load_summarize_chain
from langchain_core.tools import Tool
from langchain.text_splitter import CharacterTextSplitter
import os
import sys

# === Step 1: LLM Setup ===
llm = Ollama(model="llama3.2:3b") 

# === Step 2: Summarizer Function ===
def summarize_text(text: str) -> str:
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = splitter.create_documents([text])
    chain = load_summarize_chain(llm, chain_type="stuff")
    return chain.run(docs)

# === Step 3: Create the Tool ===
summarizer_tool = Tool(
    name="TextSummarizer",
    func=summarize_text,
    description="Use this to summarize long text. Input should be the full text."
)

# === Step 4: Simple Agent Setup ===
tools = [summarizer_tool]
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)

# === Step 5: Read Input from .txt File ===
def read_text_file(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# === Step 6: Run the Agent ===
if __name__ == "__main__":
    file_path = "C:/Users/91827/Desktop/ai/PROJECTS/Rural.txt" 
    long_text = read_text_file(file_path)
    query = f"Summarize this: {long_text}"
    output = agent_executor.run(query)
    print("\nSummary:\n", output)
    sys.exit(0)

