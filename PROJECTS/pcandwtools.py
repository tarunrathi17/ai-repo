import os
import json
import re
import logging
import traceback
from pprint import pprint

import pinecone
from langchain.agents import initialize_agent, AgentType
from langchain.chains import RetrievalQA
from langchain.tools import Tool
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun

# ------------------- Config -------------------
PINECONE_API_KEY = "pcsk_5gfS3P_BgjHLxRUGa6QcSXVvsXpbwFuz3wfQbpVoSJY6fXoHsWJjtJ6Aca4cyvbZaveH6B"
INDEX_NAME = "testing"
DIM = 384  # Should be int, not string
REGION = "us-east-1"

# Set env var for LangChain compatibility (optional)
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

# ------------------- Logging -------------------
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')

# ------------------- LLM & Embeddings -------------------
llm = Ollama(
    model="llama3.2:3b",
    system="""
You are an AI assistant. Your job is ONLY to select a tool and its input.

ALLOWED TOOLS:
- Memory
- Wikipedia

Respond ONLY with **strict valid JSON** in this exact format:

{
  "action": "ToolName",
  "action_input": "The user's query as a string"
}

Rules:
- Do NOT include explanations.
- Do NOT use markdown.
- Do NOT prefix with "Final Answer"
- Use double quotes for all keys and string values.
- DO NOT invent schema-like responses. Just return the query in action_input.

Example:
User: What is rural development?

Valid Output:
{
  "action": "Memory",
  "action_input": "What is rural development?"
}
"""
)

embedding = OllamaEmbeddings(model="all-minilm:latest")

# ------------------- Pinecone v3 Setup -------------------
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)

existing_indexes = pc.list_indexes().names()
if INDEX_NAME not in existing_indexes:
    pc.create_index(
        name=INDEX_NAME,
        dimension=DIM,
        metric="cosine",
        spec=pinecone.ServerlessSpec(cloud="aws", region=REGION)
    )

index = pc.Index(INDEX_NAME)
vectorstore = PineconeVectorStore(index=index, embedding=embedding, text_key="text")
retriever = vectorstore.as_retriever()
memory_qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# ------------------- Tools -------------------
wiki_wrapper = WikipediaAPIWrapper()
wiki_tool = WikipediaQueryRun(api_wrapper=wiki_wrapper)

def memory_tool_json(input_text):
    print("Using Memory Tool")
    try:
        # Ensure input_text is a string
        if isinstance(input_text, dict):
            input_text = input_text.get("action_input", "") or input_text.get("query", "")
        elif not isinstance(input_text, str):
            input_text = str(input_text)

        response = memory_qa.run(input_text)
        return {
            "tool": "Memory",
            "query": input_text,
            "answer": response
        }
    except Exception as e:
        return {"tool": "Memory", "error": str(e)}

def wikipedia_tool_json(input_text):
    print("Using Wikipedia Tool")
    try:
        result = wiki_tool.run(input_text)
        return {"tool": "Wikipedia", "query": input_text, "answer": result}
    except Exception as e:
        return {"tool": "Wikipedia", "error": str(e)}

tools = [
    Tool(name="Memory", func=memory_tool_json, description="For document memory on topic rural development"),
    Tool(name="Wikipedia", func=wikipedia_tool_json, description="For general world knowledge")
]

# ------------------- Agent Setup -------------------
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True,
    return_intermediate_steps=False
)

# ------------------- JSON Extractor -------------------
def safe_extract_action(response_text: str):
    """
    Extract and parse JSON object from LLM response string.
    Assumes response contains a single JSON object.
    """
    try:
        json_start = response_text.find("{")
        json_end = response_text.rfind("}") + 1
        if json_start != -1 and json_end != -1:
            json_text = response_text[json_start:json_end]
            return json.loads(json_text)
    except Exception as e:
        logging.warning(f"Failed to parse JSON: {e}")
    return None

# ------------------- Main Loop -------------------
def main():
    print("Ask your question! (Type 'exit' to quit)\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        try:
            logging.info(f"User input: {user_input}")
            response = agent.invoke(user_input)  # Returns a string from the LLM

            print("\nRaw Agent Response:")
            print(response)

            action_data = safe_extract_action(response)

            if not action_data:
                print("Could not parse JSON from agent response. Showing raw output:")
                print(response)
                continue

            tool_name = action_data.get("action")
            tool_input = action_data.get("action_input", "")

            # Find the tool by name (case insensitive)
            for tool in tools:
                if tool.name.lower() == tool_name.lower():
                    final_result = tool.func(tool_input)
                    print("\nTool Output:")
                    pprint(final_result)
                    break
            else:
                print(f"Tool '{tool_name}' not found in registered tools.")

        except Exception as e:
            logging.error("Exception occurred:")
            traceback.print_exc()
            print(f"Error: {e}\n")

# ------------------- Run -------------------
if __name__ == "__main__":
    main()
