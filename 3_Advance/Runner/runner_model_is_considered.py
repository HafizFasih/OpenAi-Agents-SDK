from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, RunConfig
from dotenv import load_dotenv
from rich import print
import os

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

runner_model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-2.0-flash",
)

agent_model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-1.5-flash",
)

run_config = RunConfig(
    model=runner_model
)

agent = Agent(
    name="Mathematician", 
    instructions="You are a helpful assistant", 
    model=agent_model, 
)

#! Runner ka model mana jayega agent wala nhi chalega
#! ham issy ese bh prove kr skty hain
Runner._get_model(
    agent=agent,
    run_config=run_config
) 
#! Backend ma model ko ese get kia jata ha.