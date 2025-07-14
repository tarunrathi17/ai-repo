from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import uuid
import requests

# ---------- CONFIG ----------
PINECONE_API_KEY = "pcsk_5gfS3P_BgjHLxRUGa6QcSXVvsXpbwFuz3wfQbpVoSJY6fXoHsWJjtJ6Aca4cyvbZaveH6B"
INDEX_NAME = "bot"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
OLLAMA_URL = "http://localhost:11434/api/generate"
LLM_MODEL = "llama3.2:1b"

# ---------- INIT ----------
# Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(name=INDEX_NAME, dimension=384, metric="cosine")

index = pc.Index(INDEX_NAME)

# Embedding model
embedder = SentenceTransformer(EMBEDDING_MODEL)

# ---------- MEMORY FUNCTIONS ----------
def save_to_memory(user_input, bot_response):
    memory_text = f"User: {user_input}\nBot: {bot_response}"
    embedding = embedder.encode(memory_text).tolist()
    memory_id = str(uuid.uuid4())
    index.upsert([(memory_id, embedding, {"text": memory_text})])

def retrieve_memory(query, top_k=3):
    query_vec = embedder.encode(query).tolist()
    results = index.query(vector=query_vec, top_k=top_k, include_metadata=True)
    return [match["metadata"]["text"] for match in results["matches"]]

# ---------- OLLAMA CHAT ----------
def call_llama3(prompt):
    response = requests.post(OLLAMA_URL, json={
        "model": LLM_MODEL,
        "prompt": prompt,
        "system": "You are a helpful assistant.",
        "stream": False
    })

    if response.status_code == 200:
        return response.json().get("response", "").strip()
    else:
        return "Error: Could not connect to Ollama."

# ---------- CHATBOT ----------
def chatbot(user_input):
    memory = retrieve_memory(user_input)
    context = "\n".join(memory)
    prompt = f"{context}\n\nUser: {user_input}\nBot:"
    bot_response = call_llama3(prompt)
    save_to_memory(user_input, bot_response)
    return bot_response

# ---------- MAIN LOOP ----------
if __name__ == "__main__":
    print("Chatbot with Pinecone Memory + LLaMA3\nType 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        reply = chatbot(user_input)
        print("Bot:", reply)
