from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, RunConfig, set_default_openai_api, set_default_openai_client
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

story_writer = Agent(
    name="Story Writer", 
    instructions="You are a story writer", 
)

rating_agent = Agent(
    name="Rating Agent", 
    instructions="You are given the story you have to rate it out of 10", 
)

async def main():
    story = await Runner.run(
        starting_agent=story_writer, 
        input="Write a 5 line story on Agentic AI", 
        run_config=config
    )
    rating = await Runner.run(
        starting_agent=rating_agent, 
        input=story.to_input_list(), 
        run_config=config
    )
    print(rating.final_output)

asyncio.run(main())
