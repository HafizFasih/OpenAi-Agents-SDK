from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, function_tool, enable_verbose_stdout_logging
from agents.agent import StopAtTools
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Literal
from rich import print
import os, asyncio

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

class ResultFormat(BaseModel):
    first_operand: int
    second_operand: int
    operator: Literal["+", "-", "x", "/"]
    result: int
    
@function_tool
def add(a: int, b: int) -> ResultFormat:
    """Add two numbers
    Args:
        a: the first number
        b: the second number
    """
    return ResultFormat(
        first_operand=a,
        second_operand=b,
        operator="+",
        result=a+b
    )
    
@function_tool
def subtract(a: int, b: int) -> ResultFormat:
    """Subtract two numbers
    Args:
        a: the first number
        b: the second number
    """
    return ResultFormat(
        first_operand=a,
        second_operand=b,
        operator="-",
        result=a-b
    )

@function_tool
def multiply(a: int, b: int) -> ResultFormat:
    """Multiply two numbers
    Args:
        a: the first number
        b: the second number
    """
    return ResultFormat(
        first_operand=a,
        second_operand=b,
        operator="x",
        result=a*b
    )

@function_tool
def divide(a: int, b: int) -> ResultFormat:
    """Divide two numbers
    Args:
        a: the first number
        b: the second number
    """
    return ResultFormat(
        first_operand=a,
        second_operand=b,
        operator="/",
        result=a//b
    )

async def main(stopping_tool: Literal["add", "subtract", "multiply", "divide"]):
    agent=Agent(
        name="Mathematician",
        instructions="You are good at maths, you MUST call tools ONE by ONE to solve the user's query",
        model=model,
        tool_use_behavior=StopAtTools(
            stop_at_tool_names=[stopping_tool]
        ),
        tools=[add, subtract, multiply, divide]
    )

    result= await Runner.run(
        starting_agent=agent,
        input="Q1.What is the product of 10 and 213"
        "Q2.What is the division of 15 and 5"
    )

    print(result.final_output)


asyncio.run(main("multiply"))