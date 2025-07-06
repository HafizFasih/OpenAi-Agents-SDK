from agents import Agent, Runner, RunConfig, OpenAIChatCompletionsModel, set_tracing_disabled, RunContextWrapper
from openai import AsyncOpenAI
from rich import print
import os

set_tracing_disabled(True)

#! LLM Context 4 tareeekon se LLM k paas jaa skty hain
#? 1. system prompt
#? 2. user prompt
#? 3. result of any tool call
#? 4. Hosted Tools like FileSearch, WebSearch etc.

API_KEY=os.environ.get("GEMINI_API_KEY")

config = RunConfig(
    model=OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=AsyncOpenAI(
            api_key=API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai"
        )
    )
)

#! 1. By System Prompt
agent = Agent(
    name="Helpfull Assistant",
    instructions=(
        "You are a helpful assistant. "
        "Help user by solving his queries "
        "The name of the user is Muhammad Ali and he is 20 years old "
        "So maintain the level of understanding according to it"
    )
)

#? Yahan pr hamny system prompt k zariye context (overloaded information) ko inject krdia ha 
print(
    Runner.run_sync(
        starting_agent=agent, 
        input="Tell me the basics of programming", 
        run_config=config
    ).final_output
)

#! 2. By User Prompt
agent = Agent(
    name="Helpfull Assistant",
    instructions="You are a helpful assistant"
)

#? Yahan pr hamny user prompt k zariye context ko inject kia ha
print(
    Runner.run_sync(
        starting_agent=agent, 
        input="Given the fact: 'The capital of France is Paris.' What is the capital of France?", run_config=config
    ).final_output
)

#! 3. Result of any tool call

from pydantic import BaseModel
from agents import function_tool

class UserInfo(BaseModel):
    name: str
    age: int

@function_tool
def get_user_info(ctx: RunContextWrapper[UserInfo]):
    """Fetch the user details"""
    return f"The name of user is {ctx.context.name} and age is {ctx.context.age}"


agent = Agent(
    name="Helpfull Assistant",
    instructions=(
        "You are a helpful assistant "
        "You have tool to get the user details."
    ),
    tools=[get_user_info]
)

user=UserInfo(name="Muhammad Ali", age=30)
print(
    Runner.run_sync(
        starting_agent=agent,
        input="What is user name and age?",
        context=user,
        run_config=config
    ).final_output
)

#! IMPORTANT: The system prompt generally has a higher priority and a more foundational influence than the user prompt