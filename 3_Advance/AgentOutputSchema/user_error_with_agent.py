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

#! output_type: dict[str, str] Error
#! agar ham ese output type define krengy to 'UserError' ayega (AgentOutputSchema).
agent = Agent(
    name="Rating Agent",
    output_type=dict[str, str]
)

async def main():
    result = await Runner.run(
        starting_agent=agent, 
        input="Tell me the 5 cities with population of Pakistan", 
        run_config=config
    )
    print(result.final_output)

asyncio.run(main())
