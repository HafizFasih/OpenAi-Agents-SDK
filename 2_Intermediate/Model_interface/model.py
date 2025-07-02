from agents import OpenAIChatCompletionsModel, set_tracing_disabled, Agent, Runner
from agents._run_impl import RunImpl
from agents.models.interface import ModelTracing
from openai import AsyncOpenAI
from agents import ModelSettings 
from agents.handoffs import handoff
from rich import print
from openai.types.responses import ResponseTextDeltaEvent
import os, asyncio

set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash", 
    openai_client=client,
)

agent=Agent(
    name="Physics Master",
    instructions="You are a physics expert",
    handoff_description="You are the best physics teacher"
)
# print(agent.instructions)
# RunImpl.process_model_response()

async def normal_response():
    response = await model.get_response(
        system_instructions=None,
        input="Tell me about the theory of realtivity",
        model_settings=ModelSettings(),
        tools=[],  
        output_schema=None, 
        handoffs=[handoff(agent)],
        tracing=ModelTracing.DISABLED, 
        previous_response_id=None,
    )
    print(response)
    for item in response.output:
        print(item.type if hasattr(item, "type") else item)

async def streamed_response():
    response = model.stream_response(
        system_instructions=None,
        input="Tell me 5 jokes about chemistry",
        model_settings=ModelSettings(),
        tools=[],
        output_schema=None,
        handoffs=[],
        tracing=ModelTracing.DISABLED,
        previous_response_id=None
    )
    async for item in response:
        print(item)

asyncio.run(streamed_response())
