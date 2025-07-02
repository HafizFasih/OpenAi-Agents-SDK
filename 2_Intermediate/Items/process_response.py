from agents import OpenAIChatCompletionsModel, ModelSettings, ModelTracing, RunContextWrapper, RunConfig, RunHooks, Agent, Tool
from agents._run_impl import RunImpl
from openai import AsyncOpenAI
from rich import print
from typing import Any
import os, asyncio

API_KEY=os.environ.get("GEMINI_API_KEY")

model=OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
    )
)

async def main():
    response = await model.get_response(
        input="What is the capital of Paskitan",
        system_instructions="You are a helpful asisstant",
        handoffs=[],
        model_settings=ModelSettings(),
        output_schema=None,
        tools=[],
        tracing=ModelTracing.DISABLED,
        previous_response_id=None,
    )
    processed_response = RunImpl.process_model_response(
        agent=None,
        all_tools=[],
        handoffs=[],
        output_schema=None,
        response=response
    )
    single_turn_result = await RunImpl.execute_tools_and_side_effects(
        processed_response=processed_response,
        agent=Agent(name="assistant"),
        context_wrapper=RunContextWrapper(
            context=None
        ),
        hooks=RunHooks[Any](),
        new_response=response,
        pre_step_items=[],
        original_input="What is the capital of Paskitan",
        output_schema=None,
        run_config=RunConfig()
    )
    print(response)
    print(processed_response)
    print(single_turn_result)

asyncio.run(main())