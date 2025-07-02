from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, handoff, HandoffInputData
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
from rich import print
import os
import asyncio

set_tracing_disabled(disabled=True)
load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
    ),
)

def input_filter_function(input_filter: HandoffInputData) -> HandoffInputData:
    print(input_filter)
    return input_filter

modern_physics_agent = Agent(
    name="Modern physicist", 
    instructions=(
        "You are an expert in Modern Physics. Solve problems accurately and explain your reasoning when needed."
    ),
    model=model,
    handoff_description="Handles all the MODERN PHYSICS RELATED tasks."
)

physics_expert_agent = Agent(
    name="Classical physicist", 
    instructions=(
        "You are an expert in physics. Provide clear and precise answers to physics-related problems and concepts."
        "**IMPORTANT**: If there is any thing related to MODERN PHYSICS you MUST handoffs to the Modern Physicist Agent"
    ),
    model=model,
    handoffs=[
        handoff(
            agent=modern_physics_agent,
            input_filter=input_filter_function
        )
    ]
)

async def main():
    result = Runner.run_streamed(
        starting_agent=physics_expert_agent, 
        input=(
            "Explain me the law of motions proposed by Newton"
            "What is the theory of relativity"
        )
    )
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, flush=True, end="")

asyncio.run(main())

