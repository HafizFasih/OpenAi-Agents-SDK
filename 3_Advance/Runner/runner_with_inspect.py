from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, RunConfig, enable_verbose_stdout_logging
from dotenv import load_dotenv
from rich import print
import inspect
import asyncio  
import os

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")

config = RunConfig(
    model=OpenAIChatCompletionsModel(
        model="gemini-1.5-flash",
        openai_client=AsyncOpenAI(
            api_key=API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai"
        )
    )
)

agent = Agent(
    name="Mathematician", 
    instructions="You are a helpful assistant", 
)

async def get_response():
    result_one = Runner.run(
        starting_agent=Agent(name="Assistant"), 
        input="What is the capital of Pakistan", 
        run_config=config
    )
    result_two = Runner.run(
        starting_agent=Agent(name="Assistant"), 
        input="What is the capital of India", 
        run_config=config
    )
    result_three = Runner.run(
        starting_agent=Agent(name="Assistant"), 
        input="What is the capital of America", 
        run_config=config
    )
    if (
        inspect.isawaitable(result_one) and 
        inspect.isawaitable(result_two) and 
        inspect.isawaitable(result_three)
    ):
        return [await result_one, await result_two, await result_three]

async def main():
    results = await get_response()
    print(results)

asyncio.run(main())