from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, RunContextWrapper, function_tool, default_tool_error_function, ModelSettings, enable_verbose_stdout_logging, ToolsToFinalOutputResult, FunctionToolResult
from agents.run import RunConfig
from dotenv import load_dotenv
from rich import print
import os

enable_verbose_stdout_logging()
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

def final_output_function(ctx: RunContextWrapper[None], results: list[FunctionToolResult]) -> ToolsToFinalOutputResult:
    print("final_output_function")
    return ToolsToFinalOutputResult(
        is_final_output=False,
        final_output="final_output_function result"
    )

def error_function(ctx: RunContextWrapper[None], error: Exception) -> str:
    print("Error aaya haina", str(error))
    return "Type error is occured" #! Ye wala msg llm k paas jayega

@function_tool(failure_error_function=error_function)
def add(a: int, b: int) -> int:
    """Add two numbers

    Args:
        a: first number
        b: second number
    
    """
    raise ValueError("Error")

agent = Agent(
    name="Mathematician", 
    instructions="You are math expert", 
    model=model, 
    tools=[add],
    tool_use_behavior=final_output_function,
)
result = Runner.run_sync(starting_agent=agent, input="what is 2+2", run_config=config)
print(result.final_output)
