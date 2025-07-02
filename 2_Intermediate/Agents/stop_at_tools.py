from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
from agents.agent import StopAtTools
from agents.run import RunConfig
from dotenv import load_dotenv
from typing import Literal
from rich import print
import os, asyncio

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise KeyError("Error 405: Does not found an api key") 

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client,
)
config=RunConfig(
    model=model
)

@function_tool
def sum(a: int, b: int) -> int:
    """Returns the sum of two numbers
    Args:
        a: the first number
        b: the second number
    """
    return a + b
    
@function_tool
def subtract(a: int, b: int) -> int:
    """Returns the difference of two numbers
    Args:
        a: the first number
        b: the second number
    """
    return a - b
    
@function_tool
def multiply(a: int, b: int) -> int:
    """Returns the product of two numbers
    Args:
        a: the first number
        b: the second number
    """
    return a * b

@function_tool
def divide(a: int, b: int) -> int:
    """Divides two numbers
    Args:
        a: the first number
        b: the second number
    """
    return a // b

async def main(tool_name: Literal["sum", "subtract", "multiply", "divide"]):
    agent=Agent(
        name="Assistant",
        instructions="You are a helpful assistant",
        model=model,
        tools=[sum, subtract, multiply, divide],
        tool_use_behavior=StopAtTools(
            stop_at_tool_names=[tool_name]
        )
    )

    result = await Runner.run(
        starting_agent=agent,
        input="What is the sum of 10 and 53"
    )

    print(result.final_output)
    print(result.new_items)

asyncio.run(main("sum"))