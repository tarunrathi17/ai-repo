import requests

def chat_with_ollama(message, model="llama3.2:3b"):
    url = "http://localhost:11434/api/chat"

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": message}
        ],
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        return data['message']['content']
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Simple loop to chat
print("Chatbot (Ollama) is ready! Type 'exit' to quit.\n")
while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        print("Bye!")
        break
    response = chat_with_ollama(user_input)
    print(f"Bot: {response}\n")
