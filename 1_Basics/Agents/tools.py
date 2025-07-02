from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, enable_verbose_stdout_logging, ModelSettings
from dotenv import load_dotenv
from rich import print
from pydantic import BaseModel
import os

enable_verbose_stdout_logging()
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


@function_tool(name_override="add")
def add(a: int, b: int) -> int:
    """Add two numbers
    Args:
        a: first number
        b: second number
        
    Returns:
        int: The sum of the two numbers.
    """

    return a + b

@function_tool
def subtract(a: int, b: int) -> int:
    """Subtract two numbers
    Args:
        a: first number
        b: second number
        
    Returns:
        int: The difference of the two numbers.
    """

    return a - b


agent = Agent(
    name="Mathematician", 
    instructions=(
        "You are math expert "
        "You also greet back peoples if they greet you. "
    ), 
    model=model, 
    tools=[add, subtract],
    model_settings=ModelSettings(
        tool_choice="subtract"
    ),
)
result = Runner.run_sync(starting_agent=agent, input="Hello")
print(result.final_output)
