from retriever import Retriever
from rag_bot import query_ollama

def main():
    retriever = Retriever("C:/Users/91827/Desktop/ai/PROJECTS/Ragbot/knowledge.txt")
    print("RAG Chatbot (type 'exit' to quit)")
    
    while True:
        question = input("\nYou: ")
        if question.lower() == "exit":
            break
        
        context = retriever.get_relevant_context(question)
        full_prompt = f"Use the following context to answer the question:\n\n{context}\n\nQuestion: {question}"
        answer = query_ollama(full_prompt)
        print(f"\nBot: {answer.strip()}")

if __name__ == "__main__":
    main()