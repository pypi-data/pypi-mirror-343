from gemini_agent import Agent
from dotenv import load_dotenv
import os

load_dotenv()

# Load multiple API keys
api_keys = os.getenv("GEMINI_APIs").split(",")
current_key_idx = 0

def get_current_api_key():
    return api_keys[current_key_idx]

def switch_to_next_api_key():
    global current_key_idx
    current_key_idx = (current_key_idx + 1) % len(api_keys)
    print(f"🔄 [DEBUG] Switching to API key index {current_key_idx}: {api_keys[current_key_idx][:10]}...")

# Define your tools
@Agent.description("Multiplies two numbers.")
@Agent.parameters({
    'a': {'type': int, 'description': 'The first number'},
    'b': {'type': int, 'description': 'The second number'}
})
def multiply(a: int, b: int) -> int:
    return a * b

@Agent.description("Adds two numbers.")
@Agent.parameters({
    'a': {'type': int, 'description': 'The first number'},
    'b': {'type': int, 'description': 'The second number'}
})
def add(a: int, b: int) -> int:
    return a + b

# Create agent with the first API key
agent = Agent(api_key=get_current_api_key(), tools=[multiply, add])

# Define a wrapper to rotate API key AFTER the call
def agent_prompt_with_key_rotation(agent,*args, **kwargs):
    # global agent
    print(f"🚀 [DEBUG] Using API key index {current_key_idx}: {agent.api_key[:10]}...")
    response = agent.prompt(*args, **kwargs)
    switch_to_next_api_key()
    agent.api_key = get_current_api_key()
    return response

# Use the agent
response = agent_prompt_with_key_rotation(agent,
    user_prompt="multiply 3 and 7 then add 5 to the result",
    system_prompt="You are a helpful assistant. Give your response always with ❤️ at the start of the line. In your response you should mention the function you used.",
    response_structure={
        "type": "object",
        "properties": {
            "used_functions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "function_name": {"type": "string"},
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "a": {"type": "integer"},
                                "b": {"type": "integer"}
                            }
                        }
                    }
                }
            },
            "answer": {"type": "string"}
        }
    }
)

print(response)