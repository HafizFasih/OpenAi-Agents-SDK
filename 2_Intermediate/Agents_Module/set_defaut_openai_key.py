from agents import Agent, Runner, set_default_openai_key
from dotenv import load_dotenv
from rich import print
import os

load_dotenv()
API_KEY = os.environ.get("OPENAI_API_KEY")

if not API_KEY:
    raise KeyError("Error 405: Does not found an api key") 

#!Set the default OpenAI API key to use for LLM requests (and optionally tracing(). This is only necessary if the OPENAI_API_KEY environment variable is not already set.
set_default_openai_key(key=API_KEY, use_for_tracing=False)

agent=Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
)

result=Runner.run_sync(
    starting_agent=agent,
    input="Hello"
)

print(result.final_output)
print(result._last_agent)