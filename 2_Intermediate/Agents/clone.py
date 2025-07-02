from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv
import os

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
    )
)

first_agent = Agent(
    name="Helpfull Assistant",
    instructions="You are a helpful assistant",
    model=model
)

second_agent = first_agent.clone(
    name="General Knowledge Assistant"
)

result = Runner.run_sync(starting_agent=second_agent, input="Tell me about Sir Zia Khan, an AI professor")
print(result.last_agent)
print(result.final_output)