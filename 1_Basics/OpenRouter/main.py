from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv
import os

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "google/gemini-2.0-flash-lite-preview-02-05:free"

model = OpenAIChatCompletionsModel(
    model=MODEL,
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url=BASE_URL
    )
)

agent = Agent(name="assistant", instructions="You are a helpful assistant", model=model)
result = Runner.run_sync(agent, "hello")
print(result.final_output)