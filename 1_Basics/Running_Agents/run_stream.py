from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
import os, asyncio

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY=os.environ.get("GEMINI_API_KEY")

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
)

agent = Agent(
    name="Helpful Assistant",
    instructions="You are a helpful assistant",
    model=model
)
async def main():
    result = Runner.run_streamed(
        starting_agent=agent,
        input="Explain me in detail about agentic ai"
    )
    async for event in result.stream_events():
      if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
          print(event.data.delta, end="", flush=True)

asyncio.run(main())