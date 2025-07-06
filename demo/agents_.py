from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    AsyncOpenAI,
    set_tracing_disabled,
    RunConfig,
    RunContextWrapper,
    function_tool,
    enable_verbose_stdout_logging,
    ModelSettings
)
import os
from rich import print

set_tracing_disabled(disabled=True)
enable_verbose_stdout_logging()
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


# class Person:
#     def __init__(self, name, age=10):
#         self.name = name
#         self.age = age

# first_person = Person("Fasih")

# from dataclasses import dataclass
# from pydantic import BaseModel
# @dataclass
# class Person(BaseModel):
#    name: str
#    age: int = 10

# first_person = Person(name="muhammad")

def dynamic_instructions(wrapper: RunContextWrapper, agent) ->str:
    return "You are a helpfull assistant"

# agent=Agent(
#     name="Assistant",
#     instructions="You are a helpful assistant"
# )

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

# print(add)
# import json
# json.loads("{}")
# json.dumps({"a":53})

agent=Agent(
    name="Assistant",
    instructions=dynamic_instructions,
    model=model,
    tools=[subtract, add],
    model_settings=ModelSettings(
        tool_choice="add"
    )
)

result=Runner.run_sync(
    starting_agent=agent,
    input="What is 2 - 2",
    # run_config=config
)
print(result.final_output)

# data: int | str = "str"



# class A:
#     pass

# class B(A):
#     pass

# a=A()
# b=B()

# print(isinstance(b, A))