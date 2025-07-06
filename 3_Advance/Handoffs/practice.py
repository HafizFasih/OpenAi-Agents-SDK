from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, RunConfig, HandoffInputData, handoff, HandoffCallItem, HandoffOutputItem
from dotenv import load_dotenv
from rich import print
from typing import Any
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


agent=Agent(
    name="Mathematician",
    instructions="You are good at maths."
)


triage_agent=Agent(
    name="Triage Agent",
    instructions=(
        "You are a helpfull assistant "
        "If user asked about any math question so handoff to Math Expert Agent."
    ),
    handoffs=[
        handoff(
            agent=agent,
        )
    ]
)

result = Runner.run_sync(
    starting_agent=triage_agent,
    input="What is the basic concepts of algebra?",
    run_config=config
)

print(result.final_output)