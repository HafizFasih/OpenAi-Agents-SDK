from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    AsyncOpenAI,
    set_tracing_disabled,
    RunConfig,
    enable_verbose_stdout_logging,
    AgentOutputSchema,
    function_tool,
    StopAtTools,
    ToolsToFinalOutputResult,
    RunContextWrapper,
    FunctionToolResult
)

import os
from rich import print
enable_verbose_stdout_logging()
set_tracing_disabled(disabled=True)
API_KEY = os.environ.get("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model=OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

config = RunConfig(
    model=model
)

from pydantic import BaseModel

class OutputType(BaseModel):
    city: str
    population: str

@function_tool
def add(a: int, b: int) -> int:
    """Add two numbers

    Args:
        a: int
        b: int
    """
    return a + b
    
@function_tool
def subtract(a: int, b: int) -> int:
    """Subtract two numbers

    Args:
        a: int
        b: int
    """
    return a - b


def my_func(wrapper: RunContextWrapper, tool_result: list[FunctionToolResult]) -> ToolsToFinalOutputResult:
    print(tool_result)
    print("My_func executed")
    return ToolsToFinalOutputResult(
        is_final_output=True,
        final_output="hello world"
    )

agent=Agent(
    name="Assistant",
    instructions="You are a helpfull assistant",
    tools=[add, subtract],
    # output_type=AgentOutputSchema(OutputType),
    # tool_use_behavior=StopAtTools(
    #     stop_at_tool_names=["subtract"]
    # ),
    tool_use_behavior=my_func
)

result=Runner.run_sync(
    starting_agent=agent,
    input="What is 2+2 and 32-5",
    run_config=config,
)

print(result.final_output)