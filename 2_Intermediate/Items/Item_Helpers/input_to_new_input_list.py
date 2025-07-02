from agents import OpenAIChatCompletionsModel, Agent, Runner, set_tracing_disabled, ItemHelpers
from openai import AsyncOpenAI
from rich import print
import os
import asyncio

set_tracing_disabled(True)

model=OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=AsyncOpenAI(
        api_key=os.environ.get("GEMINI_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
)

async def main():
    agent = Agent(
        name="Mathematician", 
        instructions="You are a helpful assistant", 
        model=model, 
    )
    user_input=input("Enter your query: ")
    user_input=ItemHelpers.input_to_new_input_list(user_input)
    result = await Runner.run(
        starting_agent=agent, 
        input=user_input
    )
    print(result.input)
    print(result.final_output)

asyncio.run(main())