from langchain_community.llms import Ollama
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.tools import Tool

def run_helper_agent(input_text: str) -> str:
    # Use a smaller model if llama3.2:1b is too slow or stalls
    llm = Ollama(model="llama3.2:1b", base_url="http://localhost:11434")  # or try llama3:instruct or tinyllama

    # Use simple text splitting
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = splitter.create_documents([input_text])

    # Chain setup
    chain = load_summarize_chain(llm, chain_type="stuff")

    # Run summarization
    summary = chain.run(docs)
    return summary

# Export tool
helper_summarizer_tool = Tool(
    name="HelperSummarizerAgent",
    func=run_helper_agent,
    description="Use this tool only to summarize a large body of text. "
        "Input should be a long text, and the output will be a short summary. "
        "Do not use this tool for analysis, evaluation, or listing tasks."
)
