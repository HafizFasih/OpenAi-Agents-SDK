from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, ModelProvider
from agents.run import RunConfig
from dotenv import load_dotenv
from rich import print
import os

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise KeyError("Error 405: Does not found an api key") 


client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

class CustomModelProvider(ModelProvider):
    def get_model(self, model_name):
        return OpenAIChatCompletionsModel(
            model=model_name or "gemini-2.0-flash",
            openai_client=client
        )


agent=Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
)

result=Runner.run_sync(
    starting_agent=agent,
    input="Hello",
    run_config=RunConfig(
        model_provider=CustomModelProvider()
    )
)

print(result.final_output)