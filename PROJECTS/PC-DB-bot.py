import uuid
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec

# --- Config ---pcsk_5gfS3P_BgjHLxRUGa6QcSXVvsXpbwFuz3wfQbpVoSJY6fXoHsWJjtJ6Aca4cyvbZaveH6B
PINECONE_API_KEY = "pcsk_5gfS3P_BgjHLxRUGa6QcSXVvsXpbwFuz3wfQbpVoSJY6fXoHsWJjtJ6Aca4cyvbZaveH6B"
INDEX_NAME = "testing"
TXT_FILE_PATH = "C:/Users/91827/Desktop/ai/PROJECTS/Rural.txt"  
CHUNK_SIZE = 768
EMBED_MODEL = "all-mpnet-base-v2"

# --- Initialize Pinecone (v3.x client) ---
pc = Pinecone(api_key=PINECONE_API_KEY)
if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
index = pc.Index(INDEX_NAME)

# --- Load local embedding model ---
model = SentenceTransformer(EMBED_MODEL)

# --- Read and chunk .txt file ---
def read_and_chunk_txt(path, chunk_size=CHUNK_SIZE):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# --- Upsert text chunks into Pinecone ---
def upsert_chunks(chunks):
    vectors = []
    for chunk in chunks:
        embedding = model.encode(chunk).tolist()
        vectors.append({
            "id": str(uuid.uuid4()),
            "values": embedding,
            "metadata": {"text": chunk}
        })
    index.upsert(vectors)
    print(f"Upserted {len(vectors)} chunks to Pinecone.")

# --- Query Pinecone with user question ---
def query_pinecone(query, top_k=3):
    query_vector = model.encode(query).tolist()
    results = index.query(vector=query_vector, top_k=top_k, include_metadata=True)
    return [match["metadata"]["text"] for match in results["matches"]]

# --- MAIN Execution ---
chunks = read_and_chunk_txt(TXT_FILE_PATH)
upsert_chunks(chunks)

# --- Chatbot loop ---
print("TXT Chatbot Ready! (type 'exit' to quit)")
while True:
    user_input = input("\nYou: ")
    if user_input.lower() == "exit":
        break
    results = query_pinecone(user_input)
    if results:
        print("Bot:", results[0])
    else:
        print("Bot: I couldn't find anything relevant.")
