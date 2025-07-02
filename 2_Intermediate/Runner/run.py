from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, RunContextWrapper, enable_verbose_stdout_logging, RunHooks
from pydantic import BaseModel
from agents.run import RunConfig
from dotenv import load_dotenv
from rich import print
import os, asyncio

load_dotenv()
set_tracing_disabled(disabled=True)
enable_verbose_stdout_logging()

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

class UserInfo(BaseModel):
    username: str

class CustomRunHook(RunHooks):
    async def on_agent_start(self, context, agent ):
        print(context)
        print(f"{agent.name} is started")
    
    async def on_tool_start(self, context, agent, tool):
        print(f"{agent.name} has called tool named {tool.name}")

    async def on_tool_end(self, context, agent, tool, result):
        print(f"{agent.name}'s tool({tool.name}) ended with result: {result}")

    async def on_agent_end(self, context, agent, output):
        print(f"The agent named {agent.name} is ended with final_output: {output}")

@function_tool
def get_user_info(ctx: RunContextWrapper[UserInfo]):
    """Tells the name if the user"""
    return f"username is {ctx.context.username}"

agent=Agent[UserInfo](
    name="Assistant",
    instructions="You are a helpful assistant",
    tools=[get_user_info],
)

async def main():
    result = await Runner.run(
        starting_agent=agent,
        input="What is my name?",
        context=UserInfo(username="Muhammad Fasih"),
        max_turns=5,
        hooks=CustomRunHook(),
        run_config=config
    )
    print(result.final_output)

asyncio.run(main())