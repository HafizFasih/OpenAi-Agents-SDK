from __future__ import annotations
from agents import Agent, Runner, function_tool, RunContextWrapper, set_tracing_disabled, enable_verbose_stdout_logging, AsyncOpenAI, OpenAIChatCompletionsModel, FunctionToolResult
from agents.agent import ToolsToFinalOutputResult, StopAtTools, ToolsToFinalOutputFunction
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Literal, List
import os, asyncio

API_KEY=os.environ.get("GEMINI_API_KEY")

load_dotenv()
set_tracing_disabled(disabled=True)
enable_verbose_stdout_logging()

STOPPING_TOOL_NAME="get_fact"

model=OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
    )
)

class Weather(BaseModel):
    city: str
    temperature: str
    weather: str

@function_tool
def get_weather(city: str) -> Weather:
    """Returns the weather of the city
    Args:
        city: The name of the city
    """
    print("get_weather is called")
    return Weather(city=city, temperature="24C", weather="Cloudy")

@function_tool
def get_fact(city: str) -> str:
    """Tells the fact about the city
    Args:
        city: The name of the city
    """
    return f"The fact about the {city} is that, it is very beautiful"

@function_tool(name_override=STOPPING_TOOL_NAME)
def stopping_tool() -> None:
    print("Stopping tool is called")

async def custom_func(
        ctx: RunContextWrapper[Weather], 
        results: List[FunctionToolResult]
    ) -> ToolsToFinalOutputResult:
    weather: Weather = results[0].output
    return ToolsToFinalOutputResult(
        is_final_output=True, final_output=weather, 
    )

async def main(
    tool_behavior: 
        Literal["default", "stop_on_first_tool", "custom_tool", "stop"] = (
            "default"
        )
    ):

    behavior: Literal["run_llm_again", "stop_on_first_tool"] | StopAtTools | ToolsToFinalOutputFunction = (
        "run_llm_again"
    )
    if tool_behavior == "stop_on_first_tool":
        behavior="stop_on_first_tool"
    elif tool_behavior == "custom_tool":
        behavior=custom_func
    elif tool_behavior == "stop":
        behavior=StopAtTools(
            stop_at_tool_names=[STOPPING_TOOL_NAME]
        )
    else:
        behavior="run_llm_again"

    agent=Agent(
        name="Weather Assistant",
        instructions="You are a helpful weather assistant, you should run tools one by one not simultaneously",
        model=model,
        tools=[get_weather, get_fact],
        tool_use_behavior=behavior
    )
    result = await Runner.run(
        starting_agent=agent,
        input="Tell me the weather of Tokyo and the fact about it"
    )
    print(result.final_output)


if __name__ == "__main__":
    behavior: Literal["default", "stop_on_first_tool", "custom_tool", "stop"] = "default"
    asyncio.run(main(behavior))