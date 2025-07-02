from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, set_tracing_disabled, function_tool, ModelSettings
from dotenv import load_dotenv
import os

set_tracing_disabled(disabled=True)
load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
)

@function_tool
def add(a: int, b: int) -> int:
    """Add two numbers

    Args:
        a: first number
        b: second number
    """
    return a + b + 10

model_setting=ModelSettings(
    # tool_choice: ["required", "auto", "none"]
    tool_choice="required" 
)

agent = Agent(
    name="Assistant",
    instructions="You are a helpful asssitant",
    model=model,
    tools=[add],
    model_settings=model_setting
)

result = Runner.run_sync(
    starting_agent=agent,
    input="Sum 1000 and 3213"
)

print(result.final_output)