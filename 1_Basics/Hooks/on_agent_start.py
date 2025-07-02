from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, RunHooks, RunContextWrapper, function_tool, AgentHooks
from agents.tool import ToolErrorFunction
from dotenv import load_dotenv
from dataclasses import dataclass
from pydantic import BaseModel
from rich import print
from typing import TypeVar, Any
import os

T = TypeVar("T")

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

class MyContext(BaseModel):
    name: str
    age: str

@function_tool
def get_user_info(ctx: RunContextWrapper[MyContext]) -> str:
    """Tells the name and and the age of the user"""
    return f"The User name is {ctx.context.name} and age is {ctx.context.age}"

@dataclass
class CustomRunHook(RunHooks[T]):
    async def on_agent_start(self, context: RunContextWrapper[T], agent: Agent[T]) -> None:
        print("Runner is started")
    async def on_agent_end(self, context: RunContextWrapper[T], agent: Agent[T], output: Any) -> None:
        print("Runner is ended")

@dataclass
class CustomAgentHook(AgentHooks[T]):
    async def on_start(self, context: RunContextWrapper[T], agent: Agent[T]) -> None:
        print("Agent is started")

    async def on_end(self, context: RunContextWrapper[T], agent: Agent[T], output: Any) -> None:
        print("Agent is stopped")

agent = Agent[MyContext](
    name="Assistant", 
    instructions="You are a helpful assistant", 
    model=model,
    tools=[get_user_info],
    hooks=CustomAgentHook[MyContext](),
)

context: MyContext = MyContext(name="Muhammad Fasih", age="10")
result = Runner.run_sync(agent, "Tell me my name", hooks=CustomRunHook[MyContext](), context=context)
print(result.final_output)

