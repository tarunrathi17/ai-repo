from langchain_community.llms import Ollama
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool

# 1. Define custom Python evaluator tool
def safe_python_eval(code: str) -> str:
    try:
        return str(eval(code))
    except Exception as e:
        return str(e)

python_tool = Tool.from_function(
    name="Python Calculator",
    func=safe_python_eval,
    description="Evaluate basic Python expressions like math operations. Input should be a valid expression like '5 * 9' or 'sqrt(81)'."
)

# 2. Use your local LLaMA 3 model from Ollama
llm = Ollama(model="llama3.2:3b")  

# 3. Initialize agent with better agent type
agent = initialize_agent(
    tools=[python_tool],
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

# 4. Run question
question = "What is 5 * 9 and who is the president of India?"
response = agent.run(question)
print("\nAnswer:", response)
