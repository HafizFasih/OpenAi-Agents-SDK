from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
from agents.run import RunConfig
from dotenv import load_dotenv
from rich import print
import os, asyncio

load_dotenv()
set_tracing_disabled(disabled=True)

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
class OutputType:
    output: str


agent=Agent[OutputType](
    name="Assistant",
    instructions="You are a helpful assistant",
    model=model,
)

async def main():
    system_prompt = await agent.get_system_prompt(run_context=OutputType)
    print(system_prompt)

asyncio.run(main())