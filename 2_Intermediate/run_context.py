from agents import (
    Agent, 
    Runner, 
    AsyncOpenAI, 
    OpenAIChatCompletionsModel, 
    set_tracing_disabled, 
    RunContextWrapper, 
    function_tool,
    AgentHooks
)
from rich import print
from dataclasses import dataclass
from dotenv import load_dotenv
import os
import asyncio

class CAH(AgentHooks):
    async def on_end(self, context, agent, output):
        usage = context.usage
        usage2 = context.usage
        print(usage.input_tokens)
        print(usage.input_tokens_details)
        print(usage.output_tokens)
        print(usage.output_tokens_details)
        print(usage.total_tokens)
        usage.add(usage2)
        print(usage)
        
load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise KeyError("Error 405: API key not found")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client,
)

@dataclass
class UserInfo:  
    name: str
    age: int

@function_tool
async def fetch_user_details(ctx: RunContextWrapper[UserInfo]) -> str:  
    '''Returns the age and name of the user.'''
    return f"Name:{ctx.context.name}\nAge: {ctx.context.age} years old"


async def main():
    user_info = UserInfo(name="Muhammad Ahmed", age=1000)
    agent = Agent(  
        name="Assistant",
        tools=[fetch_user_details],
        model=model,
        hooks=CAH()
    )   
    result = await Runner.run(  
        starting_agent=agent,
        input="What is the name and age of the user?",
        context=user_info,
    )

    print(result.final_output)  

if __name__ == "__main__":  
    asyncio.run(main())