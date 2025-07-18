from agents import OpenAIChatCompletionsModel, Agent, Runner, set_tracing_disabled, ItemHelpers, MessageOutputItem
from agents._run_impl import RunImpl
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
    result = await Runner.run(starting_agent=agent, input="What is the capital of Pakistan")
    extracted_message = ItemHelpers.text_message_outputs(result.new_items)
    print(extracted_message)

asyncio.run(main())