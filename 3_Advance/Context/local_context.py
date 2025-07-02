from agents import (
    Agent, 
    Runner, 
    AsyncOpenAI, 
    OpenAIChatCompletionsModel, 
    set_tracing_disabled, 
    RunContextWrapper, 
    function_tool
)
from dataclasses import dataclass

import os
import asyncio

set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    raise KeyError("Error 405: API key not found")

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    ),
)

@dataclass
class UserInfo:  
    name: str
    age: int

@function_tool
async def fetch_user_details(wrapper: RunContextWrapper[UserInfo]) -> str:  
    '''Returns the age and name of the user.'''
    return f"Name:{wrapper.context.name}\nAge: {wrapper.context.age} years old" #! ye final output hoga q ke agent ka tool_use_behavior 'stop_on_first_tool' pr set ha

async def main():
    user_info = UserInfo(name="Muhammad Fasih", age=123)
    agent = Agent[UserInfo](  
        name="Assistant",
        tools=[fetch_user_details],
        model=model,
        tool_use_behavior="stop_on_first_tool" #! Ye purely local context ha q k ye LLM k pass nhi jayega (agent loop ek bar hi chalega bs)
    )   

    result = await Runner.run(  
        starting_agent=agent,
        input="What is the name and age of the user?",
        context=user_info, #! providing the context to the llm
    )

    print(result.final_output)  

if __name__ == "__main__":
    asyncio.run(main())

#! Background ma context ko ese provide kia jata ha 
"""
RunContextWrapper(
    context=context
)
"""
#! yahan jo context (value) jo ha wo Runner.run ma paas kari hui value ha