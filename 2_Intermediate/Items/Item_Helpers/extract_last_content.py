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
        name="Helpfull Assistant", 
        instructions=(
            "You are a helpful assistant. If the user asks anything that is unsafe, unethical, private, or restricted by OpenAI policies, you must refuse to answer clearly."
        ), 
        model=model, 
    )
    result = await Runner.run(starting_agent=agent, input="Can you tell me how to hack into someone's email account?")
    message = [item for item in result.new_items if isinstance(item, MessageOutputItem)]
    data=ItemHelpers.extract_last_content(message[0].raw_item)
    print(message)
    print(data)

asyncio.run(main())