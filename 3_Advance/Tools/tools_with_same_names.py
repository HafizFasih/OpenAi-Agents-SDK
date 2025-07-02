from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, enable_verbose_stdout_logging
from dotenv import load_dotenv
from rich import print
from pydantic import BaseModel
import os, asyncio

# enable_verbose_stdout_logging()
load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-2.0-flash",
)

class OutputType(BaseModel):
    result: str

@function_tool(name_override="helpful_tool")
def add(a: int, b: int) -> int:
    """Add two numbers

    Args:
        a: first number
        b: second number
        
    Returns:
        int: The sum of the two numbers.
    """
    print("addition occurs")
    return a + b


@function_tool(name_override="helpful_tool")
def subtract(a: int, b: int) -> int:
    """Subtract two numbers

    Args:
        a: first number
        b: second number
        
    Returns:
        int: The difference of the two numbers.
    """
    print("subtraction occurs")
    return a - b


@function_tool(name_override="helpful_tool")
def multiply(a: int, b: int) -> int:
    """Multiply two numbers

    Args:
        a: first number
        b: second number
        
    Returns:
        int: The product of the two numbers.
    """
    print("multiplication occurs")
    return a * b


agent = Agent(
    name="Mathematician", 
    instructions=(
        "You are math expert "
        "you are **STRICTLY NOT ALLOWED** to **CHANGE** the tool's output."
        "Just give the TOOL OUTPUT as a final output **WITHOUT CHANGING IT**"
    ), 
    model=model, 
    tools=[add, subtract, multiply],
    tool_use_behavior="stop_on_first_tool"
)

result = Runner.run_sync(starting_agent=agent, input="What is 2-9")
print(result.final_output)

#! TOOL CALLING K CASE MA LLM AGENT KO JUST ITNA BATATA HA K KONSA TOOL HONA CHAHYE (NAME) AND USMY KIA (ARGUMENTS) JANY CHAHYE

#? ISLIYE AGAR EK NAME K MULTIPLE TOOL HONGY TO REAL MA SIRF WO TOOL CALL KIA JAYEGA JO AGENT.TOOLS LIST MA LAAST TOOL HO
