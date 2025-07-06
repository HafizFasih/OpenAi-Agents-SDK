from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, RunConfig, enable_verbose_stdout_logging, AgentOutputSchema
from dotenv import load_dotenv
from rich import print
import os
import asyncio

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

config = RunConfig(
    model=OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=client
    )
)

#! output_type: list[str]
#! Examples: int, list, tuple, bool, set etc.
#! Ye acceptable ha or ismy kia hoga ek dict banai jayegi jismy ek key hogi with name 'response' and then us key ki value ma hamara answer ayega 

agent = Agent(
    name="Rating Agent",
    output_type=list[str]
)

async def main():
    result = await Runner.run(
        starting_agent=agent, 
        input="Tell me the 5 cities with population of Pakistan", 
        run_config=config
    )
    print(result.raw_responses)

asyncio.run(main())

