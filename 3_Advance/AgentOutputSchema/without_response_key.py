from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, RunConfig, enable_verbose_stdout_logging, AgentOutputSchema
from dotenv import load_dotenv
from rich import print
from pydantic import BaseModel
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

class MyOutputType(BaseModel):
    city: str
    populaton_range: str

agent = Agent(
    name="Rating Agent",
    output_type=MyOutputType
)

async def main():
    result = await Runner.run(
        starting_agent=agent, 
        input=(
            "Tell me most populated city of Pakistan. "
            "Make sure that you provide the latest data"
        ), 
        run_config=config
    )
    print(result.raw_responses)

asyncio.run(main())

#! Is case ma hamary paas LLM direct hamary given type k instance ma hi output dega (no response key here)