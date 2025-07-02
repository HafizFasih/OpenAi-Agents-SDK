import asyncio, os
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv
from rich import print
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY=os.environ.get("GEMINI_API_KEY")

model=OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
    )
)

async def main():
    agent = Agent(
        name="Joker",
        instructions="You are a helpful assistant.",
        model=model
    )
    # print("Started")
    # await asyncio.sleep(10)
    # print("Ended")
    result = Runner.run_streamed(agent, input="Write an 1000 words essay on Iran Current War")
    async for event in result.stream_events():
        if(event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent)):
            pass
            # print(event.data.delta, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())