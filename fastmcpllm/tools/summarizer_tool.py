# summarizer_server.py
from mcp.server.fastmcp import FastMCP
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

mcp = FastMCP("summarizer")

llm = Ollama(model="llama3.2:3b")
prompt = PromptTemplate(template="Summarize this text:\n\n{text}", input_variables=["text"])
chain = LLMChain(llm=llm, prompt=prompt)

@mcp.tool()
def summarize(text: str) -> str:
    return chain.run(text)

if __name__ == "__main__":
    mcp.run(transport="stdio")
