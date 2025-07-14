import uuid
from langchain_ollama import OllamaEmbeddings
from langchain_pinecone import Pinecone as PineconeStore
from langchain_community.llms import Ollama
from langchain.schema import Document
from pinecone import Pinecone, ServerlessSpec

# NEW Pinecone SDK v3 import
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key="pcsk_5gfS3P_BgjHLxRUGa6QcSXVvsXpbwFuz3wfQbpVoSJY6fXoHsWJjtJ6Aca4cyvbZaveH6B")

INDEX_NAME = "ragbot-memory"

# === Create serverless index if it doesn't exist ===
if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",        
            region="us-east-1"    
        )
    )

index = pc.Index(INDEX_NAME)  # <- This replaces pinecone.Index()

# === LangChain Embeddings and Vectorstore ===
embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")
vectorstore = PineconeStore(index=index, embedding=embeddings, text_key="page_content")
llm = Ollama(model="llama3.2:1b")

def chat_with_ragbot(user_input, session_id):
    results = vectorstore.similarity_search(query=user_input, k=3, namespace=session_id)
    memory = "\n".join([doc.page_content for doc in results])

    prompt = f"""
The following is a conversation between a user and a helpful AI assistant.
Previous conversation:
{memory}

Current input:
User: {user_input}
Assistant:"""

    response = llm(prompt)

    vectorstore.add_documents([
        Document(page_content=f"User: {user_input}"),
        Document(page_content=f"Bot: {response}")
    ], namespace=session_id)

    return response

if __name__ == "__main__":
    print("RAGBot with Pinecone Serverless (v3) + Ollama is ready!")
    session_id = input("Enter your session ID or name: ").strip() or str(uuid.uuid4())

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit']:
            print("👋 Bye!")
            break
        answer = chat_with_ragbot(user_input, session_id)
        print(f"Bot: {answer}")
