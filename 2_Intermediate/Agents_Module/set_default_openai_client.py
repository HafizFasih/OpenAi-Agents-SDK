from agents import Agent, Runner, set_default_openai_key, set_default_openai_client, AsyncOpenAI, set_tracing_export_api_key
from dotenv import load_dotenv
from rich import print
import os

load_dotenv()
API_KEY = os.environ.get("OPENAI_API_KEY")

if not API_KEY:
    raise KeyError("Error 405: Does not found an api key") 

client=AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://api.openai.com/v1/openai"
)

set_default_openai_client(client=client, use_for_tracing=False)

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