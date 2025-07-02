from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, function_tool, enable_verbose_stdout_logging, ToolsToFinalOutputResult, RunContextWrapper, FunctionToolResult
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
from rich import print
import os

enable_verbose_stdout_logging()
set_tracing_disabled(disabled=True)
load_dotenv()

API_KEY=os.environ.get("GEMINI_API_KEY")

model=OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
)

class Weather(BaseModel):
    city: str
    temperature: str
    condition: str
 
@function_tool
def get_weather(city: str) -> Weather:
    """Return the weather of the city
    Args:
        city: The name of the city
    """
    return Weather(city=city, temperature="22-24C", condition="cloudy")

async def gives_final_output(ctx: RunContextWrapper, results: List[FunctionToolResult]) -> ToolsToFinalOutputResult:
    print("gives_final_output is running")
    weather: Weather = results[0].output
    return ToolsToFinalOutputResult(
        is_final_output=True, final_output=weather
    )


agent=Agent(
    name="Asssitant",
    instructions="You are a helpful assistant",
    model=model,
    tools=[get_weather],
    tool_use_behavior=gives_final_output
)

result=Runner.run_sync(
    agent,
    "Tell me the weather of tokyo"
)

print(result.final_output)
print(result.new_items)