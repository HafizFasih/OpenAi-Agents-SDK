from agents import Agent, Runner, ModelSettings
from agents.extensions.models.litellm_model import LitellmModel
from rich import print
import os

API_KEY=os.environ.get("GEMINI_API_KEY")
BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai"
MODEL="gemini-2.0-flash"

model=LitellmModel(
    api_key=API_KEY,
    model="gemini/gemini-1.5"
)

agent = Agent(name="Assistant", model=model) 
result=Runner.run_sync(agent, "hello")
print(result.final_output)
