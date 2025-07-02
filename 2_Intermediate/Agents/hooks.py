from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, RunHooks, AgentHooks, RunContextWrapper, AgentOutputSchema
from dotenv import load_dotenv
from rich import print
from typing import TypeVar
from pydantic import BaseModel
import os

load_dotenv()
set_tracing_disabled(disabled=True)

T = TypeVar("T")
API_KEY = os.environ.get("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-1.5-flash",
)

class MathOutput(BaseModel):
    first_operand: int
    second_operand: int
    result: int

@function_tool
def add(a: int, b: int) -> int:
    """Add two numbers

    Args:
        a: first number
        b: second number
    
    """
    return a + b

class SubAgentHook(AgentHooks[T]):
    async def on_start(self, ctx: RunContextWrapper[T], agent: Agent[T]):
        print(ctx)
        print(f"{agent.name} is started")
    
    async def on_end(self, ctx: RunContextWrapper[T], agent: Agent[T], output: str):
        print(f"{agent.name} is stopped with output -> {output}")


agent = Agent[MathOutput](
    name="Mathematician", 
    instructions="You are math expert", 
    # model=model, 
    tools=[add],
    hooks=SubAgentHook(),
    output_type=AgentOutputSchema(output_type=MathOutput, strict_json_schema=True)
)
example=MathOutput(first_operand=10, second_operand=5, result=15)
result = Runner.run_sync(starting_agent=agent, input="What is 2+2", context=example)
print(result.final_output)