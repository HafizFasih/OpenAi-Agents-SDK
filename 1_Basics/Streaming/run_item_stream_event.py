import asyncio
import random
from agents import Agent, ItemHelpers, Runner, function_tool, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from rich import print
from rich.pretty import pretty_repr
import os
from openai.types.responses import ResponseCreatedEvent 

set_tracing_disabled(disabled=True)

API_KEY=os.environ.get("GEMINI_API_KEY")

model=OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
    )
)

@function_tool
def how_many_jokes() -> int:
    """Tell the amount of jokes"""
    return random.randint(1, 10)


async def main():
    agent = Agent(
        name="Joker",
        instructions="First call the `how_many_jokes` tool, from where you would get the amount then tell me those amount of jokes. You are an expert in telling jokes",
        tools=[how_many_jokes],
        model=model
    )

    result = Runner.run_streamed(
        agent,
        input="Tell me the x amount of jokes",
    )

    async for event in result.stream_events():
        print(pretty_repr(event))
        if event.type == "agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
        if event.type == "raw_response_event" and isinstance(event.data, ResponseCreatedEvent):
            # print(event.data)
            pass



if __name__ == "__main__":
    asyncio.run(main())

"""
=== Run starting ===
Agent updated: Joker
-- Tool was called
-- Tool output: 1
-- Message output:
 Sure, here's a joke for you:

Why did the scarecrow win an award?

Because he was outstanding in his field!
=== Run complete ===
"""






