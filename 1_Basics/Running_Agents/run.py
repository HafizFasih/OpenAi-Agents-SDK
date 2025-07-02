from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
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
    result = await Runner.run(
        starting_agent=agent,
        input="Hello",
    )

    print(result.final_output)

asyncio.run(main())