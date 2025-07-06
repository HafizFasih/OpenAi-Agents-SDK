# type: ignore
from agents import RunContextWrapper, Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, AsyncOpenAI, RunConfig, function_tool, enable_verbose_stdout_logging
from pydantic import BaseModel
from rich import print
import os

class UserInfo(BaseModel):
    name: str
    age: int
    def display_user_info(self):
        print(f"Username is {self.name} and his age is {self.age}") 

# enable_verbose_stdout_logging()
set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

config = RunConfig(
    model=OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=client
    )
)

class BrokenUserInfo(BaseModel):
    fake_user: str

@function_tool
def add(wrapper: RunContextWrapper[UserInfo], a: int, b: int) -> int:
    """Add two numbers

    Args:
        a: first number
        b: second number
    """
    print(wrapper.context.name)
    print(wrapper.context.age)
    wrapper.context.display_user_info()
    return a + b

agent=Agent[UserInfo](
    name="Assistant",
    instructions="You are a helpful assistant",
    tools=[add]
)

user=UserInfo(name="Muhammad Fasih", age=123)

result=Runner.run_sync(
    starting_agent=agent,
    input="What is the sum of 10 and 432",
    run_config=config,
    context=user
)

print(result.final_output)

