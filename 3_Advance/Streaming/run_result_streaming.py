from agents import Agent, Runner, RunConfig, OpenAIChatCompletionsModel, RunResultStreaming, RunContextWrapper
from openai import AsyncOpenAI

from rich import print
import os


API_KEY=os.environ.get("GEMINI_API_KEY")

config=RunConfig(
    model=OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=AsyncOpenAI(
            api_key=API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai"
        )
    )
)


agent=Agent(
    name="Story Teller",
    instructions="You are a good story teller",
)

streamed_result = RunResultStreaming(
    input="Tell me the stroy of King and Queen",
    new_items=[],
    current_agent=agent,
    raw_responses=[],
    final_output=None,
    is_complete=False,
    current_turn=0,
    max_turns=10,
    input_guardrail_results=[],
    output_guardrail_results=[],
    _current_agent_output_schema=None,
    trace=None,
    context_wrapper=RunContextWrapper(context=None),
)
print(streamed_result)