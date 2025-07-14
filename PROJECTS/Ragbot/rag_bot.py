import subprocess

def query_ollama(prompt, model="llama3.2:1b"): #llama3.2:1b #llama3:2b
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return result.stdout.decode("utf-8")