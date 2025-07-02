from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, ToolsToFinalOutputResult, function_tool, ModelSettings, RunContextWrapper, ToolCallItem, FunctionToolResult
from typing import List
from dotenv import load_dotenv
from rich import print
import os

set_tracing_disabled(disabled=True)
load_dotenv()

API_KEY=os.environ.get("GEMINI_API_KEY")

model=OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
    )
)

@function_tool
def sum(a: int, b: int) -> int:
    """Add two numbers
    Args:
        a: first number
        b: second number
    """
    return a + b

async def generate_final_output(ctx: RunContextWrapper[None], result: List[FunctionToolResult]) -> ToolsToFinalOutputResult:
    output=result[0].output
    return ToolsToFinalOutputResult(
        is_final_output=True,
        final_output=100
    )

agent=Agent(
    name="math_assistant",
    instructions="You are good at maths",
    model=model,
    tools=[sum],
    tool_use_behavior=generate_final_output,
    model_settings=ModelSettings(
        tool_choice="required"
    ),
)

result=Runner.run_sync(
    starting_agent=agent,
    input="What is the answer of 2 + 14"
)

print(result.final_output)
print(result.new_items)