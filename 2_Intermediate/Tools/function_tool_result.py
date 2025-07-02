from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, enable_verbose_stdout_logging, ToolsToFinalOutputResult, RunContextWrapper, FunctionToolResult
from typing import List
from dotenv import load_dotenv
from rich import print
import os

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
    model="gemini-1.5-flash",
)

@function_tool
def add(a: int, b: int) -> int:
    """Add two numbers

    Args:
        a: first number
        b: second number
    
    """
    return a + b

def get_tool_result(
    ctx: RunContextWrapper[None], 
    result: List[FunctionToolResult]
)-> ToolsToFinalOutputResult:
    print(result)
    return ToolsToFinalOutputResult(
        is_final_output=True,
        final_output="Hello"
    )

agent = Agent(
    name="Mathematician", 
    instructions="You are math expert", 
    model=model, 
    tools=[add],
    tool_use_behavior=get_tool_result
)
result = Runner.run_sync(starting_agent=agent, input="What is 2+2")
print(result.final_output)