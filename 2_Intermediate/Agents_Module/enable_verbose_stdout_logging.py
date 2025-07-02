from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, enable_verbose_stdout_logging
from agents.items import MessageOutputItem, ItemHelpers
from agents.run import RunConfig
from dotenv import load_dotenv
from rich import print
import os

load_dotenv()
set_tracing_disabled(disabled=True)
enable_verbose_stdout_logging()

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise KeyError("Error 405: Does not found an api key") 

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client,
)
config=RunConfig(
    model=model
)

agent=Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model=model
)

result=Runner.run_sync(
    starting_agent=agent,
    input="Hello"
)

print(result.final_output)
print(result._last_agent)