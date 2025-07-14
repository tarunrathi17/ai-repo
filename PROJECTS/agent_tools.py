import math
import logging
from langchain_ollama import OllamaLLM  
from langchain_community.utilities import WikipediaAPIWrapper

# Silence internal logs
logging.getLogger().setLevel(logging.ERROR)

# Wikipedia tool
wikipedia = WikipediaAPIWrapper()

# Calculator tool with structured output
def calculator(expression: str) -> str:
    try:
        result = eval(expression, {"__builtins__": {}}, math.__dict__)

        if "+" in expression:
            operation = "addition"
        elif "-" in expression:
            operation = "subtraction"
        elif "*" in expression:
            operation = "multiplication"
        elif "/" in expression:
            operation = "division"
        elif "sqrt" in expression:
            operation = "square root"
        elif "log" in expression:
            operation = "logarithm"
        else:
            operation = "calculation"

        trace = {
            "input": expression,
            "operation": operation,
            "steps": [f"{expression} = {result}"],
            "result": result
        }

        output = (
            f"Operation: {trace.get('operation', 'unknown')}\n"
            f"Steps: {trace['steps'][0] if trace.get('steps') else 'N/A'}\n"
            f"Result: {trace.get('result', 'N/A')}"
        )
        return output

    except Exception as e:
        return f"Calculator error: {e}"

# Wikipedia tool with structured output (only first page summary)
def run_wikipedia_tool(query: str) -> str:
    try:
        summary = wikipedia.run(query)

        # Only use the first summary if multiple pages are returned
        if isinstance(summary, list):
            summary = summary[0]

        trace = {
            "input": query,
            "source": "wikipedia",
            "summary": summary,
            "status": "success"
        }

        output = (
            f"Source: {trace.get('source', '').capitalize()}\n"
            f"Summary: {trace.get('summary', 'N/A')}\n"
            f"Status: {trace.get('status', 'N/A')}"
        )
        return output

    except Exception as e:
        trace = {
            "input": query,
            "source": "wikipedia",
            "summary": f"Wikipedia error: {e}",
            "status": "error"
        }

        output = (
            f"Source: {trace.get('source', '').capitalize()}\n"
            f"Summary: {trace.get('summary', 'N/A')}\n"
            f"Status: {trace.get('status', 'N/A')}"
        )
        return output

# Stateless LLM instance
def fresh_llm():
    return OllamaLLM(model="llama3.2:1b", temperature=0.0)

# Tool classifier with robust output parsing
def decide_tool_only(question: str, debug=False) -> str:
    prompt = f"""
You are an assistant that selects the appropriate tool for answering questions.

There are only two tools:
- calculator → for mathematical expressions like "12 + 3", "sqrt(49)", "log(100)"
- wikipedia → for general knowledge or factual questions like "Who discovered gravity?", "What is the capital of Japan?"

Only reply with one word: calculator or wikipedia

Examples:

Q: What is 12 * 5?
A: calculator

Q: sqrt(121) + 3
A: calculator

Q: Who is Albert Einstein?
A: wikipedia

Q: What is the population of India?
A: wikipedia

Q: What is the square root of 144 plus 6?
A: calculator

Q: Who invented the computer?
A: wikipedia

Q: {question}
A:"""

    llm = fresh_llm()
    raw_result = llm.invoke(prompt, stop=["\n", " "])
    clean = raw_result.strip().lower()

    if debug:
        print(f"[DEBUG] Raw tool response: {repr(raw_result)} → Parsed: {clean}")

    if "calc" in clean:
        return "calculator"
    elif "wiki" in clean:
        return "wikipedia"
    else:
        return "wikipedia"  # fallback

# Heuristic fallback math checker
def is_likely_math(expr: str) -> bool:
    try:
        result = eval(expr, {"__builtins__": {}}, math.__dict__)
        return isinstance(result, (int, float))
    except:
        return False

# Main chat loop
if __name__ == "__main__":
    print("LLaMA3 Tool Agent (Ollama) — Calculator & Wikipedia\nType 'exit' to quit.")

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ("exit", "quit"):
            break

        tool = decide_tool_only(user_input)

        if tool == "calculator":
            if is_likely_math(user_input):
                answer = calculator(user_input)
            else:
                # Fallback to Wikipedia if it's not real math
                tool = "wikipedia"

        if tool == "wikipedia":
            answer = run_wikipedia_tool(user_input)

        elif tool not in ("calculator", "wikipedia"):
            print("Unrecognized tool. Defaulting to Wikipedia.")
            answer = run_wikipedia_tool(user_input)

        print(answer)
