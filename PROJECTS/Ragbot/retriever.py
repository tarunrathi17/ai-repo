from langchain_experimental.tools import PythonREPLTool
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
    

class Retriever:
    def __init__(self, knowledge_path):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.knowledge_path = knowledge_path
        self.paragraphs = self.load_paragraphs()
        self.embeddings = self.embed_paragraphs()

    def load_paragraphs(self):
        if not os.path.exists(self.knowledge_path):
            raise FileNotFoundError(f"{self.knowledge_path} does not exist.") 
        with open(self.knowledge_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

    def embed_paragraphs(self):
        return self.model.encode(self.paragraphs)

    def get_relevant_context(self, query, top_k=1):
        query_vec = self.model.encode([query])
        similarities = cosine_similarity(query_vec, self.embeddings)[0]
        top_indices = similarities.argsort()[-top_k:][::-1]
        return "\n".join([self.paragraphs[i] for i in top_indices])


if __name__ == "__main__":
    # Path to your knowledge file
    knowledge_file = "knowledge.txt"

    # Create Retriever and test it
    retriever = Retriever(knowledge_file)
    query = "What is Pythagoras theorem?"
    context = retriever.get_relevant_context(query, top_k=2)
    print("Retrieved Context:\n", context)

    # Math tool usage via LangChain
    python_tool = PythonREPLTool()

    # Sample math question
    question = "Calculate the square root of 256 + 4**2"
    tool_result = python_tool.run(question)
    print("\nPython Tool Output:\n", tool_result)
