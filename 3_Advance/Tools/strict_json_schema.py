from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
from dotenv import load_dotenv
from rich import print
from typing import Optional
import os

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
    ),
)


@function_tool(strict_mode=False)
def add(a: int, b: int, reasoning: Optional[str] = None) -> int:
    """Add two numbers

    Args:
        a: first number
        b: second number
        c: reasoning that waht are you doing

    Returns:
        int: The sum of the two numbers.
    """
    print(reasoning)
    return a + b


agent = Agent(
    name="Mathematician", 
    instructions=(
        "You are math expert"
    ), 
    model=model, 
    tools=[add],
)

result = Runner.run_sync(starting_agent=agent, input="What is 2+2")
print(result.final_output)
